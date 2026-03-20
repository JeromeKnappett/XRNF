#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 27 12:31:21 2021
@author: jknappett
"""

import action
from wpg.srwlib import SRWLWfr, SRWLStokes
from wpg.wavefront import Wavefront
import numpy as np

class wfStokes(action.Action):
    '''
    This action generates the Stokes parameters of the wavefield using the SRWLStokes() function.    
    '''   
    def __init__(self):
        super().__init__()
        self.description = 'Action: Get Stokes Parameters'
        
    def perform_operation(self, *args, **kwargs):
        
        
        # allow disable if {self.__class__.__name__: True}
        try:
            if kwargs['parameters'][self.__class__.__name__] == False:
                print('...disabled.')
                return {}
        except: pass
        
        w = kwargs['wavefront']
        
        
        """ Converting wavefront to SRWLWfr() structure"""
        wfr = SRWLWfr() #Initial Electric Field Wavefront
        wfr.allocate(1, w.params.Mesh.nx, w.params.Mesh.ny) #Numbers of points vs Photon Energy (1), Horizontal and Vertical Positions (dummy)
        wfr.mesh.zStart = w.params.Mesh.zCoord #Longitudinal Position [m] at which Electric Field has to be calculated, i.e. the position of the first optical element
        wfr.mesh.eStart = w.params.Mesh.sliceMin #Initial Photon Energy [eV]
        wfr.mesh.eFin = w.params.Mesh.sliceMax #Final Photon Energy [eV]
        wfr.mesh.xStart = w.params.Mesh.xMin #Initial Horizontal Position [m]
        wfr.mesh.xFin = w.params.Mesh.xMax #Final Horizontal Position [m]
        wfr.mesh.yStart = w.params.Mesh.yMin #Initial Vertical Position [m]
        wfr.mesh.yFin = w.params.Mesh.yMax #Final Vertical Position [m]
        wfr.arEx = w._srwl_wf.arEx
        wfr.arEy = w._srwl_wf.arEy
        
        """ Converting Gaussian to Wavefront() structure"""
        # wf = Wavefront(srwl_wavefront=w)
        
        print("-----Getting Stokes Parameters-----")
    
        #wf = Wavefront(srwl_wavefront=w)           
        #if(isinstance(w, SRWLWfr) == False):
        #    w = SRWLWfr(w)
        stk = SRWLStokes()
        
        stk.allocate(wfr.mesh.ne, wfr.mesh.nx, wfr.mesh.ny, _mutual = 0) #numbers of points vs photon energy, horizontal and vertical positions
        stk.mesh.zStart = wfr.mesh.zStart #longitudinal position [m] at which UR has to be calculated
        stk.mesh.eStart = wfr.mesh.eStart #initial photon energy [eV]
        stk.mesh.eFin = wfr.mesh.eFin #final photon energy [eV]
        stk.mesh.xStart = wfr.mesh.xStart #initial horizontal position of the collection aperture [m]
        stk.mesh.xFin = wfr.mesh.xFin #final horizontal position of the collection aperture [m]
        stk.mesh.yStart = wfr.mesh.yStart #initial vertical position of the collection aperture [m]
        stk.mesh.yFin = wfr.mesh.yFin #final vertical position of the collection aperture [m]  
            
        wfr.calc_stokes(stk)
        
        s = np.reshape(stk.arS,(4,stk.mesh.nx,stk.mesh.ny))
    
        s0 = np.reshape(s[0,:,:],(stk.mesh.nx,stk.mesh.ny))
        s1 = np.reshape(s[1,:,:],(stk.mesh.nx,stk.mesh.ny))
        s2 = np.reshape(s[2,:,:],(stk.mesh.nx,stk.mesh.ny))
        s3 = np.reshape(s[3,:,:],(stk.mesh.nx,stk.mesh.ny))
    
        _s0 = s0/s0
        _s1 = s1/s0
        _s2 = s2/s0
        _s3 = s3/s0

        _s = np.array([[_s0.mean(),_s1.mean(),_s2.mean(),_s3.mean()]]).T
        print("Normalised Stokes vector:")
        print(_s)
        
        # degree of polarization.  Alternatively, we could use D = Ip/(Ip + Itot) where Ip is the polarised intensity and It is the total intensity.
        D = (np.sqrt((s1**2 + s2**2 + s3**2)))/s0
    
        Davg = np.mean(D)

        # eccentricity.  e = 1 => linear polarization (no chirality) 
        e = np.sqrt(s2*np.sqrt(s1**2 + s2**2)/(1+np.sqrt(s1**2 + s2**2))) # added sqrt - jerome
    
        #making sure eccentricity agrees with s3
        # e_3 = (2*(-1 + s3**2 + np.sqrt(-1*(1 - s3**2))))/(s3**2)
        # print('Eccentricity from s3 = {}'.format(e_3))
    
        # inclination of polarization ellipse (radians)
        i = 0.5*np.arctan(s2/s1)

        # chirality, c, defined for convenience 
        s3m = np.mean(s3)
        if s3m < 0:
            c = 'ccw'
        if s3m >0:
            c = 'cw'
        if s3m ==0:
            c = None
        
        # return a dictionary.
        return {'stk0': s0,'stk1': s1,'stk2': s2,'stk3': s3, 'stkNormS': _s, 'stkDpol': D, 'stkDavg': Davg, 'stkEccentricity': e, 'stkI': i}
