#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 11:29:05 2019

@author: -
"""

# to do:  create custom error handlers

#from wpg.beamline import Beamline
from wpg.srwlib import srwl
#from wpg.wavefront import Wavefront

from wpg.useful_code.wfrutils import calculate_fwhm_x, calculate_fwhm_y, get_mesh
from beamlineExt import bl
from wpg.srwlib import SRWLOptD
from wpg.srwlib import SRWLOptC

from utils import propagationParameters  # should replace with Use_PP
from wpg.optical_elements import Use_PP, WPGOpticalElement


class oeResample(WPGOpticalElement):
    """Optical element: Empty.
    This is empty propagator used for sampling and zooming wavefront
    """

    def __init__(self, D=None, R=None, N=None):
        super(oeResample, self).__init__()
        self.D = D
        self.R = R
        self.N = N

    def __str__(self):
        return ''

    def propagate(self, wfr, propagation_parameters=None):
        """
        Propagate wavefront through empty propagator for ,
        sampling and resizing wavefront. See modifyDimensions for explanation of
        parameters.
        If propagation_paramters is None then parameters are computed from the 
        parameters supplied at initilisation (D, R and N)
        """
        if propagation_parameters is None:
            modifyDimensions(wf, D = self.D, R = self.R, N = self.N)
        else:
            beamline = wpg.srwlib.SRWLOptC([], propagation_parameters)
            srwl.PropagElecField(wfr._srwl_wf, beamline)


def getDimensions(wf):
    [nx, ny, xmin, xmax, ymin, ymax] = get_mesh(wf)
    dx = (xmax-xmin)/nx
    dy = (ymax-ymin)/ny
    rx = xmax-xmin
    ry = ymax-ymin
    
    return nx, ny, dx, dy, rx, ry


def resizeWFEiger(wf, Nx=1024, Ny=1024, Dx = 75e-6, Dy=75e-6):
    
    modifyResolutionWF(wf, Dx, Dy)
    modifyPixelsWF(wf, Nx, Ny)

def modifyDimensions(wf, D = None, R = None, N = None):
    
    # Modifies wf according to optional parameters, N, D and R
    # N:  tuple (Nx, Ny) number of pixels in x and y
    # D:  tuple (Dx, Dy) resolution unit, i.e. length of pixel, in x and y
    # R:  tuple (Rx, Ry) range in units of m along x and y
    # only N or R  should be used, but if both are present number of pixels will be
    # changed after the length is changed.
    
    if D is not None:
        Dx, Dy = D
        modifyResolutionWF(wf, Dx, Dy)
        
    if R is not None:
        Rx, Ry = R
        modifyRangeWF(wf, Rx, Ry)
        
    if N is not None:
        Nx, Ny = N
        modifyPixelsWF(wf, Nx, Ny)

def modifyResolutionWF(wf, Dx, Dy):
        # Dx, Dy:  target pixel size in x and y
        
        [nx, ny, dx, dy, rx, ry] = getDimensions(wf)       
                
        print('Before Rescale: Number={}, {}, Range={}, {}, Step={}, {}'.format(nx,ny,rx,ry,dx,dy))
        elResc = bl(SRWLOptC(_arOpt=[SRWLOptD(0)], 
                    _arProp=[propagationParameters(ResolutionX=dx/Dx, ResolutionY=dy/Dy)]), 
                    description='Rescaling')
        metrics = elResc.propagate(wfr=wf, describe=False)              
        
        [nx, ny, dx, dy, rx, ry] = getDimensions(wf)               
        print('After Rescale: Number={}, {}, Range={}, {}, Step={}, {}'.format(nx,ny,rx,ry,dx,dy))
        

def modifyPixelsWF(wf, Nx, Ny):
        # Nx, Ny:  target number of pixels in x and y.  
        # Resizes WF by changing number of pixels, without changing pixel size        
        
        [nx, ny, dx, dy, rx, ry] = getDimensions(wf)       
        Rx, Ry = Nx*dx, Ny*dy      
        
        print('Before Resize: Number={}, {}, Range={}, {}, Step={}, {}'.format(nx,ny,rx,ry,dx,dy))
        elResc = bl(SRWLOptC(_arOpt=[SRWLOptD(0)], 
                            _arProp=[propagationParameters(RangeX=Rx/rx, RangeY=Ry/ry)]), 
                            description='Resizing')
        metrics = elResc.propagate(wfr=wf, describe=False)              
            
        [nx, ny, dx, dy, rx, ry] = getDimensions(wf)       
        print('After Resize: Number={}, {}, Range={}, {}, Step={}, {}'.format(nx,ny,rx,ry,dx,dy))
        

def modifyRangeWF(wf, Rx, Ry):
        # Rx, Ry:  target range.
        # Resizes WF without changing resolution
        
        [nx, ny, dx, dy, rx, ry] = getDimensions(wf)               
                
        print('Before Resize: Number={}, {}, Range={}, {}, Step={}, {}'.format(nx,ny,rx,ry,dx,dy))
        elResc = bl(SRWLOptC(_arOpt=[SRWLOptD(0)], 
                            _arProp=[propagationParameters(RangeX=Rx/rx, RangeY=Ry/ry)]), 
                            description='Resizing')
        metrics = elResc.propagate(wfr=wf, describe=False)              
            
        [nx, ny, dx, dy, rx, ry] = getDimensions(wf)       
        print('After Resize: Number={}, {}, Range={}, {}, Step={}, {}'.format(nx,ny,rx,ry,dx,dy))



def calculate_fwhm(wfr):
    """
    Calculate FWHM of the beam calculating number of point bigger then max / 2 throuhgt center of the image

    :param wfr:  wavefront
    :return: {'fwhm_x':fwhm_x, 'fwhm_y': fwhm_y} in [m]
    """
    ## Function replicated from wpg_uti_wf here as we intend to modify it.
    
    
#    intens = wfr.get_intensity(polarization='total')
    intens = wfr.get_intensity(polarization='total').sum(axis=-1)

    mesh = wfr.params.Mesh
    if (wfr.params.wSpace == 'R-space'):
        dx = (mesh.xMax - mesh.xMin) / mesh.nx
        dy = (mesh.yMax - mesh.yMin) / mesh.ny
    elif (wfr.params.wSpace == 'Q-space'):
        dx = (mesh.qxMax - mesh.qxMin) / mesh.nx
        dy = (mesh.qyMax - mesh.qyMin) / mesh.ny
    else:
        return

    x_center = intens[intens.shape[0] // 2, :]
    fwhm_x = len(x_center[x_center > x_center.max() / 2]) * dx

    y_center = intens[:, intens.shape[1] // 2]
    fwhm_y = len(y_center[y_center > y_center.max() / 2]) * dy
    if (wfr.params.wSpace == 'Q-space'):
        print(wfr.params.wSpace)
        wl = 12.398 * 1e-10 / (wfr.params.photonEnergy * 1e-3)  # WaveLength
        fwhm_x = fwhm_x * wl
        fwhm_y = fwhm_y * wl

    return {'fwhm_x': fwhm_x, 'fwhm_y': fwhm_y}



def check_sampling(wavefront):
    """ Utility to check the wavefront sampling. """
    " adapted from wpg_uti_wf.py, distributed as part of WPG "
    
    xMin = wavefront.params.Mesh.xMin;xMax = wavefront.params.Mesh.xMax;nx = wavefront.params.Mesh.nx;
    yMin = wavefront.params.Mesh.yMin;yMax = wavefront.params.Mesh.yMax;ny = wavefront.params.Mesh.ny;
    dx = (xMax-xMin)/(nx-1); dy = (yMax-yMin)/(ny-1)
    xx=calculate_fwhm(wavefront); fwhm_x = xx[u'fwhm_x']; fwhm_y = xx[u'fwhm_y'];
    Rx =  wavefront.params.Rx; Ry =  wavefront.params.Ry;
    ekev = wavefront.params.photonEnergy*1e-3
    dr_ext_x = 12.39e-10/ekev*Rx/(2*fwhm_x);
    dr_ext_y = 12.39e-10/ekev*Ry/(2*fwhm_y);

    format_string = '|{:4.3e}|{:4.3e}|{:4.3e}|{:4.3e}|{:4.3e}|{:4.3e}|{:4.3e}|'

    ret = 'WAVEFRONT SAMPLING REPORT\n'
    ret += '+----------+---------+---------+---------+---------+---------+---------+---------+\n'
    ret += '|x/y       |FWHM     |px       |ROI      |R        |Fzone    |px*7     |px*10    |\n'
    ret += '+----------+---------+---------+---------+---------+---------+---------+---------+\n'
    ret += "|Horizontal"+format_string.format(fwhm_x,dx,(xMax-xMin),Rx,dr_ext_x,dx*7,dx*10) + '\n'
    ret+= "|Vertical  "+format_string.format(fwhm_y,dy,(yMax-yMin),Ry,dr_ext_y,dy*7,dy*10) + '\n'
    ret += '+----------+---------+---------+---------+---------+---------+---------+---------+\n\n'

    report=dict([
            ('Horizontal Resolution', None),
            ('Vertical Respolution', None),
            ('Horizontal Range', None), 
            ('Vertical Range', None),
            ('Horizontal Focus', None),
            ('Vertical Focus',  None),
            ('dx', dx),
            ('dy', dy),
            ('Rx', Rx),
            ('Ry', Ry),
            ('fwhmx' , fwhm_x),
            ('fwhmy' , fwhm_y),
            ('ekev'  , ekev)])
            
            


    if 7*dx < dr_ext_x and 10*dx > dr_ext_x:
        report['Horizontal Resolution'] = True
        ret += 'Horizontal Fresnel zone extension within [7,10]*pixel_width -> OK\n'
    else:
        report['Horizontal Resolution'] = False
        ret += 'Horizontal Fresnel zone extension NOT within [7,10]*pixel_width -> Check pixel width."\n'

    if 7*dy < dr_ext_y and 10*dy > dr_ext_y:
        report['Vertical Resolution'] = True
        ret += 'Vertical Fresnel zone extension within [7,10]*pixel_height -> OK\n'
    else:
        report['Vertical Resolution'] = False
        ret += 'Vertical Fresnel zone extension NOT within [7,10]*pixel_height -> Check pixel width."\n'

    if Rx >= 3* fwhm_x:
        report['Horizontal Range'] = True
        ret+= 'Horizontal ROI > 3* FWHM(x) -> OK\n'
    else:
        report['Horizontal Range'] = False
        ret+= 'Horizontal ROI !> 3* FWHM(x) -> Increase ROI width (x).\n'

    if Ry >= 3* fwhm_y:
        report['Vertical Range'] = True
        ret+= 'Vertical ROI > 3* FWHM(y) -> OK\n'        
    else:
        report['Vertical Range'] = False
        ret+= 'Vertical ROI !> 3* FWHM(y) -> Increase ROI height (y).\n'

    
    if fwhm_x <= 10*dx :
        report['Horizontal Focus'] = True
        ret+= 'Focus Sampling: FWHM > 10*px(x) -> OK\n'
    else:
        report['Horizontal Focus'] = False
        ret+= 'Focus Sampling: FWHM > 10*px(x) -> Reduce pixel width (x).\n'

    if fwhm_y <= 10*dy:
        report['Vertical Focus'] = True
        ret += 'Focus sampling: FWHM > 10*px(y) -> OK\n'        
    else:
        report['Vertical Focus'] = False
        ret += 'Focus sampling: FWHM <= 10*px(y) -> Reduce pixel height (y).\n'

    
    
    

    return ret, report, 
