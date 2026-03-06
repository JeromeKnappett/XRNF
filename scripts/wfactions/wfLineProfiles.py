
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created May 21

@author: gvanriessen
"""

import numpy as np
import xl.interferenceGratingModels as gm
from xl.action import Action

class wfLineProfiles(Action):
    '''
    This action returns line profiles through properties derived from wavefronts.
    '''   
    def __init__(self):
        super().__init__()
        self.description = 'Action: extract line profiles through properties derived from wavefronts'


    def perform_operation(self, *args, **kwargs):

        # allow disable if {self.__class__.__name__: True}
        try:
            if kwargs['parameters'][self.__class__.__name__] == False:
                print('...disabled.')
                return {}
        except:
            pass
        
        wfr = kwargs['wavefront']

        try:
            profileWidth = kwargs['wfProfileOptions']['width']
        except:
            profileWidth = 1 

        if profileWidth > 1:
            profilelo, profilehi = profileWidth//2, profileWidth//2
        else:    
            profilelo, profilehi = 1, 0 


        try:
            polarizationModes = kwargs['wfProfileOptions']['polarization'] 
        except:
            polarizationModes = ['total','horizontal','vertical']   



        x =  np.linspace(wfr.params.xCentre-wfr.params.Rx/2,
                          wfr.params.xCentre+wfr.params.Rx/2,
                          wfr.params.Mesh.nx)
        y =  np.linspace(wfr.params.yCentre-wfr.params.Ry/2,
                          wfr.params.yCentre+wfr.params.Ry/2,
                          wfr.params.Mesh.ny)
        metrics = {}
        metrics['x'] = x
        metrics['y'] = y
         
        for pol in polarizationModes:
            I = wfr.get_intensity(polarization=pol)
            P = wfr.get_phase(polarization=pol)
            for prop,W in zip(['intensity','phase'],[I,P]):
                for axis, index in zip(['x','y'],[0,1]):
                      try:
                          pkey = prop.capitalize() + '/' +  pol.capitalize() + '/' + axis.capitalize() + '/'
                          print('Profile: '+ pkey)
                          
                          ny=wfr.params.Mesh.ny
                          nx=wfr.params.Mesh.nx
                          if  axis == 'x':
                              ROI = ((0,ny//2-profilelo),(nx,ny//2+profilehi))
                              axisVals = x
                          if axis == 'y':
                              ROI = ((nx//2-profilelo,0),(nx//2+1,ny+profilehi))
                              axisVals = y
                         
                          prof = gm.lineProfile(W, ROI=ROI, AXIS = index)

                          metrics.update({
                                  pkey+'profile' : prof
                                  })
                     
                      except Exception as e: print(e)
                     
        return metrics
