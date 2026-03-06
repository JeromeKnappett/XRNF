#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 17 17:26:05 2021

@author: jerome
"""

import action
import pickle
import os
from wpg.wavefront import Wavefront

class pickleWavefront(action.Action):
    '''
    This action generates the Stokes parameters of the wavefield using the SRWLStokes() function and saves the x and y cuts.
    This is a more memory efficiency version of wfStokes    
    '''   
    def __init__(self):
        super().__init__()
        self.description = 'Action: Pickle wavefront object for further analysis/propagation'
        
    def perform_operation(self, *args, **kwargs):
        
        
        # allow disable if {self.__class__.__name__: True}
        try:
            if kwargs['parameters'][self.__class__.__name__] == False:
                print('...disabled.')
                return {}
        except: 
            pass
        
        """The actual implementation of the  plugin 
        """
        try:
            w = kwargs['wavefront']
            fdir = kwargs['parameters']['fdir']
        except:
            # todo: improve by printing descriptive error / arg checking
            print('FAILED:' + self.description)
        
        else:
            
            path = os.path.join(fdir,'wavefrontParams.pkl') 
            print(" ")
            print("..HERE WE ARE...")
            print(path)
            print(" ")
            nx,ny = w.params.Mesh.nx, w.params.Mesh.ny #Numbers of points vs Photon Energy (1), Horizontal and Vertical Positions
            zStart = w.params.Mesh.zCoord #Longitudinal Position [m] at which Electric Field has to be calculated, i.e. the position of the first optical element
            eStart = w.params.Mesh.sliceMin #Initial Photon Energy [eV]
            eFin = w.params.Mesh.sliceMax #Final Photon Energy [eV]
            xStart = w.params.Mesh.xMin #Initial Horizontal Position [m]
            xFin = w.params.Mesh.xMax #Final Horizontal Position [m]
            yStart = w.params.Mesh.yMin #Initial Vertical Position [m]
            yFin = w.params.Mesh.yMax #Final Vertical Position [m]
            Ex = w._srwl_wf.arEx
            Ey = w._srwl_wf.arEy
            with open(path, "wb") as f:
                    pickle.dump([nx,ny,zStart,eStart,eFin,xStart,xFin,yStart,yFin,Ex,Ey], f)
        
        return {'pickledWavefrontPath': path,'picklesWavefrontParams': ['nx','nx','zStart','eStart','eFin','xStart','xFin','yStart','yFin','Ex','Ey']} 