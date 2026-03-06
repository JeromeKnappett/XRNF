#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 17 17:26:05 2021

@author: jerome
"""

import action
from wpg.srwlib import SRWLWfr, SRWLStokes
from wpg.wavefront import Wavefront
import numpy as np

class wfStokes1D(action.Action):
    '''
    This action generates the Stokes parameters of the wavefield using the SRWLStokes() function and saves the x and y cuts.
    This is a more memory efficiency version of wfStokes    
    '''   
    def __init__(self):
        super().__init__()
        self.description = 'Action: Get x & y cuts of each Stokes parameter and degree of polarisation'
        
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
        
        
        print("-----Getting Stokes Parameters-----")

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
        
        # CHANGED TO TEST IF DIMENSIONS WERE CORRECT
        s = np.reshape(stk.arS,(4,stk.mesh.ny,stk.mesh.nx))
    
        s0x = np.reshape(s[0,:,:],(stk.mesh.ny,stk.mesh.nx))[int(stk.mesh.ny/2),:]
        s1x = np.reshape(s[1,:,:],(stk.mesh.ny,stk.mesh.nx))[int(stk.mesh.ny/2),:]
        s2x = np.reshape(s[2,:,:],(stk.mesh.ny,stk.mesh.nx))[int(stk.mesh.ny/2),:]
        s3x = np.reshape(s[3,:,:],(stk.mesh.ny,stk.mesh.nx))[int(stk.mesh.ny/2),:]
    
        s0y = np.reshape(s[0,:,:],(stk.mesh.ny,stk.mesh.nx))[:,int(stk.mesh.nx/2)]
        s1y = np.reshape(s[1,:,:],(stk.mesh.ny,stk.mesh.nx))[:,int(stk.mesh.nx/2)]
        s2y = np.reshape(s[2,:,:],(stk.mesh.ny,stk.mesh.nx))[:,int(stk.mesh.nx/2)]
        s3y = np.reshape(s[3,:,:],(stk.mesh.ny,stk.mesh.nx))[:,int(stk.mesh.nx/2)]
    
        _s0x = s0x/s0x
        _s1x = s1x/s0x
        _s2x = s2x/s0x
        _s3x = s3x/s0x
    
        _s0y = s0y/s0y
        _s1y = s1y/s0y
        _s2y = s2y/s0y
        _s3y = s3y/s0y

        _sX = np.array([[_s0x.mean(),_s1x.mean(),_s2x.mean(),_s3x.mean()]]).T
        _sY = np.array([[_s0y.mean(),_s1y.mean(),_s2y.mean(),_s3y.mean()]]).T
        print("Normalised Stokes vector (x-cut):")
        print(_sX)
        print("Normalised Stokes vector (y-cut):")
        print(_sY)
        
        # degree of polarization.  Alternatively, we could use D = Ip/(Ip + Itot) where Ip is the polarised intensity and It is the total intensity.
        Dx = (np.sqrt((s1x**2 + s2x**2 + s3x**2)))/s0x
        Dy = (np.sqrt((s1y**2 + s2y**2 + s3y**2)))/s0y
    
        DavgX = np.mean(Dx)
        DavgY = np.mean(Dy)
        
        # return a dictionary.
        return {'stk0X': s0x,'stk1X': s1x,'stk2X': s2x,'stk3X': s3x,'stk0Y': s0y,'stk1Y': s1y,'stk2Y': s2y,'stk3Y': s3y, 'stkNormSx': _sX, 'stkNormSy': _sY, 'stkDpolX': Dx, 'stkDpolY': Dy, 'stkDavgX': DavgX, 'stkDavgY': DavgY}
