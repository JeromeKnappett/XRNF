# -*- coding: utf-8 -*-
#############################################################################
# Extension to SRWLib SR Beamline Base Class (oauthors: O.C., Maksim Rakitin, distributed in SirepoRW fork)
# Contains a set of member objects and functions for simulating basic operation and characteristics
# of a complete user beamline in a synchrotron radiation source.
# Under development!!!
#
# Authors/Contributors: G van Riessen
#############################################################################
'''
##  GVR: Under development with modifications to allow propagation of wavefront with 
##  a form of data data persistence for more convenient use of simulation to analyse
##  some subset of the optical sequence without having to re-generate the source 
##  and propagate through preceding optical elements.
##  


Notes:   h5?, json w/json-tricks, pickle, shelve, klepto or joblib (no - as of python 3.8, pickle protocol 5 handles large objects)?

    
will need to replace calc_wfr_prop and include functions to 
load and to save(cache) wfr.


'''

import os

#from srwlib import *
from srwlib import *
from srwl_uti_und import *
from uti_plot import *
import uti_math
import wpg.optical_elements
from wpg.wavefront import Wavefront
from srwl_bl import SRWLBeamline

import functools
import time


            
def timer(func):
    """Print the runtime of the decorated function"""
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()    # 1
        value = func(*args, **kwargs)
        end_time = time.perf_counter()      # 2
        run_time = end_time - start_time    # 3
        print(f"Finished {func.__name__!r} in {run_time:.4f} secs")
        return value
    return wrapper_timer

def debug(func):
    """Print the function signature and return value"""
    @functools.wraps(func)
    def wrapper_debug(*args, **kwargs):
        args_repr = [repr(a) for a in args]                      # 1
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]  # 2
        signature = ", ".join(args_repr + kwargs_repr)           # 3
        print(f"Calling {func.__name__}({signature})")
        value = func(*args, **kwargs)
        print(f"{func.__name__!r} returned {value!r}")           # 4
        return value
    return wrapper_debug


class beamline(SRWLBeamline):
    
    def __init__(self,  v, _e_beam=None, _mag_approx=None, _mag=None, _gsn_beam=None, _op=None):
        
        """
         Init beamline.  Effectively wraps the SRWLBeamline init but avoids initialising the Optics member of the  SRWLBeamline instance
         
        :param _name: beamline name string
        :param _e_beam: electron beam (SRWLPartBeam instance)
        :param _mag_approx: approximate magnetic field container (SRWLMagFldC instance)
        :param _mag: accurate magnetic field container (SRWLMagFldC instance)
        :param _gsn_beam: coherent Gaussian beam (SRWLGsnBm instance)
        :param _op: optics sequence (SRWLOptC instance, defines the beamline in other contexts).
                    If provided it will be used for initialisation.
        
        """

        self.name=v.name

        self.opticalElements = [] 
    
        super().__init__(_name=v.name, 
                         _e_beam=_e_beam, 
                         _mag_approx=_mag_approx, 
                         _mag=_mag, 
                         _gsn_beam=_gsn_beam, 
                         _op=None)
    
        if _op is not None:
            opticalElementCount = max(
                len(_op.arProp), len(_op.arOpt))
            for ti in range(opticalElementCount):
                try:
                    elem = _op.arOpt[ti]
                except IndexError:
                    elem = wpg.optical_elements.Empty()

                try:
                    pp = _op.arProp[ti]
                except IndexError:
                    pp = None
                
                #print('Loading element {} [{}]'.format(ti, elem.__doc__))
                if v.opList:
                    try:
                        strOE =  v.opList[ti]
                    except:
                        strOE = 'empty'   #testing.... deals with opList being shorter by one that the list of OE - final element?
                        
                    ena = True   # default enabled = True
                    ca = 0   # default cache = false
                    for arg in vars(v):
                        if arg  =='op_' + strOE + '_enabled':
                            ena = True if (getattr(v, arg) is 1) else  False
                        if arg == 'op_' + strOE + '_cache':
                            ca = int(getattr(v, arg))
                           
                    print('Found Element {}: {} {} '.format(strOE, ena, ca))

                else:
                    strOE = '{} {}'.format(elem.__doc__,ti)
                    ena = True # default enabled = True
                    ca =  0 #default cache  = False
                
 
                self.appendOE(elem, pp, enabled=ena, 
                              label = strOE,
                              cache=ca, cachePath=None)
                
        # debuging
        print ('Number of optical elements: {}'.format(len(self.opticalElements)))
        '''for op in self.opticalElements:
            print(op)
        '''
        

    def appendOE(self, optical_element, propagation_parameters, label=None, enabled=True, cache=0, cachePath=None):
        """
        Appends optical element and propagation propagation parameters to the end of beamline

        :param optical_element: SRW or wpg optical element
        :param propagation_parameters: SRW propagation parameters list or wpg.optical_elements.UsePP object
       
        :param cache:  caching action to be taken when wavefront is propagated through this element.
                       Options[0= no cache, 1 = memory cache, 2 = disk cache]
        """



             
        self.opticalElements.append({'optical_element': optical_element,
                             'propagation_parameters': propagation_parameters,
                             'enabled': enabled,
                             'cache': cache,
                             'label': label,
                             'cache_path':cachePath})
    
#        # if current parameter is SRWOpt and last parameter was SRWOpt lets
#        # stack it
#        
#        if isinstance(optical_element, SRWLOpt) or isinstance(optical_element, srwlib.SRWLOpt):
#                        
#            self.opticalElements.append({'optical_element': optical_element,
#                                 'propagation_parameters': propagation_parameters,
#                                 'enabled': enabled,
#                                 'cache': cache,
#                                 'label': label,
#                                 'cache_path':cachePath})
#
#        # support resizing element
#        if optical_element == [] or isinstance(optical_element,   wpg.optical_elements.Empty):
#          
#            self.opticalElements.append({'optical_element':None,
#                                 'propagation_parameters': propagation_parameters,
#                                 'enabled': enabled,
#                                 'cache': cache,
#                                 'label': label,
#                                 'cache_path':cachePath})
    

    def show(self,wfr,_v, _pol=6, _int_type=0):
        '''
        :param _pol: polarization component to extract: 
            0- Linear Horizontal; 
            1- Linear Vertical; 
            2- Linear 45 degrees; 
            3- Linear 135 degrees; 
            4- Circular Right; 
            5- Circular Left; 
            6- Total
        :param _int_type: "type" of a characteristic to be extracted:
           -1- No Intensity / Electric Field components extraction is necessary (only Wavefront will be calculated)
            0- "Single-Electron" Intensity; 
            1- "Multi-Electron" Intensity; 
            2- "Single-Electron" Flux; 
            3- "Multi-Electron" Flux; 
            4- "Single-Electron" Radiation Phase; 
            5- Re(E): Real part of Single-Electron Electric Field;
            6- Im(E): Imaginary part of Single-Electron Electric Field;
            7- "Single-Electron" Intensity, integrated over Time or Photon Energy (i.e. Fluence);
        '''
        depType = -1
        if((wfr.mesh.ne >= 1) and (wfr.mesh.nx == 1) and (wfr.mesh.ny == 1)): depType = 0
        elif((wfr.mesh.ne == 1) and (wfr.mesh.nx > 1) and (wfr.mesh.ny == 1)): depType = 1
        elif((wfr.mesh.ne == 1) and (wfr.mesh.nx == 1) and (wfr.mesh.ny > 1)): depType = 2
        elif((wfr.mesh.ne == 1) and (wfr.mesh.nx > 1) and (wfr.mesh.ny > 1)): depType = 3
        elif((wfr.mesh.ne > 1) and (wfr.mesh.nx > 1) and (wfr.mesh.ny == 1)): depType = 4
        elif((wfr.mesh.ne > 1) and (wfr.mesh.nx == 1) and (wfr.mesh.ny > 1)): depType = 5
        elif((wfr.mesh.ne > 1) and (wfr.mesh.nx > 1) and (wfr.mesh.ny > 1)): depType = 6
        if(depType < 0): Exception('Incorrect numbers of points in the mesh structure')
        
        sNumTypeInt = 'f'
        if(_int_type == 4): sNumTypeInt = 'd'
        arI = array(sNumTypeInt, [0]*wfr.mesh.ne*wfr.mesh.nx*wfr.mesh.ny)
        srwl.CalcIntFromElecField(arI, wfr, 
                                  _pol, 
                                  _int_type, depType, 
                                  wfr.mesh.eStart, wfr.mesh.xStart, wfr.mesh.yStart)
        
        
        #if _v.ws and (len(_v.ws_pl) > 0):
        if (_v.ws or _v.wg) and (len(_v.ws_pl) > 0): #OC01062016
            if (_v.ws_pl == 'xy') or (_v.ws_pl == 'yx') or (_v.ws_pl == 'XY') or (_v.ws_pl == 'YX'):
                #print('2D plot panel is to be prepared')
                
                sValLabel = 'Flux per Unit Surface'
                sValUnit = 'ph/s/.1%bw/mm^2'
                if(_v.w_u == 0):
                    sValLabel = 'Intensity'
                    sValUnit = 'a.u.'
                elif(_v.w_u == 2):
                    if(_v.w_ft == 't'):
                        sValLabel = 'Power Density'
                        sValUnit = 'W/mm^2'
                    elif(_v.w_ft == 'f'):
                        sValLabel = 'Spectral Fluence'
                        sValUnit = 'J/eV/mm^2'

                uti_plot2d1d(
                    arI,
                    [wfr.mesh.xStart, wfr.mesh.xFin, wfr.mesh.nx],
                    [wfr.mesh.yStart, wfr.mesh.yFin, wfr.mesh.ny],
                    0, #0.5*(mesh_si.xStart + mesh.xFin),
                    0, #0.5*(mesh.yStart + mesh.yFin),
                    ['Horizontal Position', 'Vertical Position', sValLabel + ' Before Propagation'],
                    ['m', 'm', sValUnit],
                    True)

        uti_plot_show()
        
            
    def enable(self, label):
        '''
        Enable an optical element
        
        param label: a string matching the label of an optical element
        '''
        try:
            for dict_ in (x for x in self.opticalElements if x["label"] == label):
                dict_['enabled']=True
        except ValueError:
            print('Element not found')

        
    def disable(self, label):
        '''
        Disable an optical element
        '''
        try:
            for dict_ in (x for x in self.opticalElements if x["label"] == label):
                dict_['enabled']=False
                print('{} disabled'.format(label))
        except ValueError:
            print('Element not found')

    def toggleEnabledState(self, labels):
        '''
        For optical elements identified in labels (a list), enable it if disabled and  disable if enabled
        '''
        for l in labels:
            self.enable(l) if self.enabled(l) is False else self.disable(l)
                
    def enabled(self, label):
        '''return enabled stated of optical element identified by label'''
        try:
            state=-1
            for dict_ in (x for x in self.opticalElements if x["label"] == label):
                state =  dict_['enabled']
        except ValueError:
            state = -1
            print('Element not found')
        return state

    def setCachePath(self, label, path):
        try:
            for dict_ in (x for x in self.opticalElements if x["label"] == label):
                print(dict_)
                dict_['cache_path']=path
        except ValueError:
            print('Element not found')
        
    def setCachePath(self, label, path):
        try:
            for dict_ in (x for x in self.opticalElements if x["label"] == label):
                print(dict_)
                dict_['cache_path']=path
        except ValueError:
            print('Element not found')
        
#    def enableCache(self,element):
#    
#    def disableCache(self, element):
        
        
 
    def __str__(self):
        """
        String representaion of beamline (used with print function).

        :return: string
        """
        res = ''
        for po in self.opticalElements:
            tolal_elements = max(
                len(po['optical_elements']), len(po['propagation_parameters']))
            for ti in range(tolal_elements):
                try:
                    elem = po['optical_elements'][ti]
                except IndexError:
                    elem = wpg.optical_elements.Empty()
                s1 = elem.__doc__    

                try:
                    pp = po['propagation_parameters'][ti]
                except IndexError:
                    pp = None
                s2 = 'Prop. parameters = {0}'.format(pp)

                if isinstance(elem, srwlib.SRWLOpt):
                    s3 = '\t' + '\n\t'.join(srw_obj2str(elem).split('\n'))
                else:
                    s3 = '\t' + str(elem)
                    
                try:
                    ena = po['enabled'][ti]
                except IndexError:
                    ena = 'Not set'
                s4 = 'Enabled = {}'.format(ena)

                try:
                    caching = po['cache'][ti]
                except IndexError:
                    caching = 'Not set'
                s5 = 'Cache = {}'.format(caching)
                
                try:
                    lbl = po['label'][ti]
                except IndexError:
                    lbl = None
                s6 = 'Label = {}'.format(lbl)
                
                try:
                    cached = po['cache_path'][ti]
                except IndexError:
                    cached= None
                s7 = 'Label = {}'.format(cached)

                res += '{0}\n{1}\n{2}\n'.format(s1, s2, s3, s4, s5, s6, s7)
        return res
    
    def printOE(self):
        '''
        pretty print a list of optical elements
        '''
        from termcolor import colored
        from beautifultable import BeautifulTable
        table = BeautifulTable()
        table.set_style(BeautifulTable.STYLE_GRID)
        table.column_headers = ["Element Label", "Type", "Enabled", "Caching", "Cache", "Propagation Parameters" ]

        for oe in self.opticalElements:
            table.append_row([oe['label'],
                             oe['optical_element'].__doc__,
                             colored('Enabled','blue') if oe['enabled']==1 else colored('Disabled','red'),
                             oe['cache'],
                             oe['cache_path'],
                             '-' if oe['propagation_parameters'] is None else oe['propagation_parameters'][:10]])

        #print(table)
    
    def cacheWFR(self,wfr,filename,label):
        print('Writing wavefront file (cache): ', filename)
        w = Wavefront(srwl_wavefront=wfr)
        w.store_hdf5(filename)
        self.setCachePath(label,filename) # store path of saved file

            
    #@debug
    def calc_wfr_prop(self, _wfr,  _pres_ang=0, _pol=6, _int_type=0, _dep_type=3, _fname='', _rad_view=None):    # added _rad_view - JK 03/07/23
        """
        Propagate wavefront through ....

        :param wfr: Input wavefront (modified in place)
        :type wfr: wpg.wavefront.Wavefront
        """       
        

        # define a new temporary beamlines
        listOE, listPP,  subOptC = [], [], []  # this had grown into something ugly
        for oe in self.opticalElements:
            
            print('\n{} {}'.format(oe['label'], oe['enabled']))#'Enabled' if oe['enabled'] else 'Disabled'))
            
            if oe['enabled'] is True:
                listOE.append(oe['optical_element'])
                listPP.append(oe['propagation_parameters'])

                if oe['cache'] is 1:
                    subOptC.append( [SRWLOptC(listOE, listPP), oe['label'], oe['cache']] )
                    listOE, listPP =  [], [] # reset
        if listOE:
            subOptC.append( [SRWLOptC(listOE, listPP), '', 0] )

        #print(subOptC)

        for soe, label, cache in subOptC:
            print (soe)
            self.optics = soe
            path = os.path.join(self.dir_main, slugify(label) + '.h5')
            #path = _fname + '.h5'  # this wwould be more consistent, more sensible...
            # print('aaaaaaaa')
            ws_res, mesh_ws, rad_intermed_ws = super().calc_wfr_prop(_wfr,                   # added ws_res, mesh_ws, rad_intermed_ws - JK 03/07/23
                                                                     _pres_ang=0, 
                                                                     _pol=6, 
                                                                     _int_type=0, 
                                                                     _dep_type=3, 
                                                                     _fname=_fname, 
                                                                     _rad_view=_rad_view)    # added _rad_view - JK 03/07/23
            # print('aaaaaaaab')
            if cache == 1:
                self.cacheWFR(_wfr, path, label)


    '''
    change below may not be necessary as the parent class will use the overridden child instance of calc_wfr_prop, but
    it is more consistent to avoid case where the op (optical container) is not predefined.
    
     multielectron propagation is not modified and so will ignore caching etc...unless we override calc_wfr_emit_prop_me
    '''
    @timer
    def calc_all(self, _v):
        """Performs setup of electron beam, magnetic field, and performs calculations according to options specified in _v
        :param _v: an object containing set of variables / options defining SR source and required calculations
        :param _op: optical element container (SRWLOptC instance) that is assumed to be set up before calling this function and eventually used for wavefront propagation
        """
        
        if hasattr(_v, 'fdir'): self.dir_main = _v.fdir

         # define a new temporary beamlines
        listOE = []; listPP = []
        for oe in self.opticalElements:
            if oe['enabled'] is True:
                listOE.append(oe['optical_element'])
                listPP.append(oe['propagation_parameters'])
        op = SRWLOptC(listOE, listPP)
        
        #super(SRWLBeamline,self).calc_all(_v, _op=op)
        return super().calc_all(_v, _op=op)

    @timer
    def calc_part(self, _v, wfr=None):
    
        """ performs propatoin according to options specified in _v, using wfr supplied
        ONLY single-electron (coherent propagation implemented at this stage)
        :param _v: an object containing set of variables / options defining SR source and required calculations
        :param _op: optical element container (SRWLOptC instance) that is assumed to be set up before calling this function and eventually used for wavefront propagation
        """


        if hasattr(_v, 'fdir'): self.dir_main = _v.fdir
        

        int_ws = self.calc_wfr_prop(
                    wfr,
                    _pres_ang = _v.ws_ap,
                    _pol = _v.si_pol,
                    _int_type = _v.si_type,
                    _dep_type=3, #consider adding other cases (e.g. for TD FEL calculations)
                    _fname = os.path.join(_v.fdir, _v.ws_fni) if(len(_v.ws_fni) > 0) else '')

        return wfr  # gvr 201022, was int_ws

''' utility functions below '''
import re
from unicodedata import normalize

_punctuation_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')

def slugify(text, delim='-'):
    """
    Generate an ASCII-only slug.
    """

    result = []
    for word in _punctuation_re.split(text.lower()):
        word = normalize('NFKD', word) \
               .encode('ascii', 'ignore') \
               .decode('utf-8')

        if word:
            result.append(word)

    return delim.join(result)
