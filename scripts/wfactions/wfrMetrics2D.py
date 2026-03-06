
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  1 09:53:21 2020

@author: gvanriessen
"""

import xl.interferenceGratingModels as gm
import numpy as np
from xl.action import Action
import matplotlib.pyplot as plt
 
class wfInterferencePatternProperties2D(Action):
    '''
    This action returns multiple metrics relevant to the contrast and quality of an
    interference pattern.
    '''   
    
    def __init__(self):
        super().__init__()
        self.description = 'Action: 2D Interference Pattern Properties'


    def perform_operation(self, *args, **kwargs):
        
        # allow disable if {self.__class__.__name__: True}
        try:
            if kwargs['parameters'][self.__class__.__name__] == True:
                print('...disabled.')
                return {}
        except:
            pass
        
        wfr = kwargs['wavefront']
        
        x =  np.linspace(wfr.params.xCentre-wfr.params.Rx/2,
                          wfr.params.xCentre+wfr.params.Rx/2,
                          wfr.params.Mesh.nx)
        y =  np.linspace(wfr.params.yCentre-wfr.params.Ry/2,
                          wfr.params.yCentre+wfr.params.Ry/2,
                          wfr.params.Mesh.ny)
        metrics = {}
        metrics['x'] = x
        metrics['y'] = y
         

        for pol in ['total']:
        #for pol in ['total','horizontal','vertical']:
            I = wfr.get_intensity(polarization=pol)
        
            P = wfr.get_phase(polarization=pol)
            #for prop,W in zip(['intensity','phase'],[I,P]):
            for prop, W in zip(['intensity'],[I]):    
                try:
                    
                    ''' analyse 2D combinations of polarisation modes and type (intensity | phase) '''
                    akey = '{}{}'.format(prop.capitalize(), pol.capitalize()) 
                    print('Area: '+ akey)
                    Cm = gm.gratingContrastMichelson(W)
                    Crms = gm.gratingContrastRMS(W)
                    C, C1, C2 = gm.meanDynamicRange(W) 
                    IOD, IODM, H, binEdges, binCenters = gm.integralOpticalDensity(W)
                    
                    pkey = prop.capitalize() + '/' +  pol.capitalize() + '/' 

                    metrics.update( {pkey+'contrastMichelson' : Cm,
                                     pkey+'contrastRMS': Crms,
                                     pkey+'meanDynamicRangeC' : C,
                                     pkey+'meanDynamicRangeC1' : C1,
                                     pkey+'meanDynamicRangeC2' : C2,
                                     pkey+'integratedOpticalDensity' : IOD,
                                     pkey+'integratedOpticalDensityMax' : IODM,
                                     pkey+'histogram' : H,
                                     pkey+'histogramBins' : binEdges
                                     } )
                except Exception as e: print(e)
    
                #for debugging - should define a variable to enable/disable
                #plt.imshow(I[:,:,0])
                #plt.imshow(P[:,:,0])
                
                
               # ''' analyse 1D (profiles) combinations of polarisation modes and type (intensity | phase) '''
               #  for axis, index in zip(['x','y'],[0,1]):
               #       try:
               #           pkey = prop.capitalize() + '/' +  pol.capitalize() + '/' + axis.capitalize() + '/'
               #           print('Profile: '+ pkey)
               #           ny=wfr.params.Mesh.ny
               #           nx=wfr.params.Mesh.nx
               #           if  axis == 'x':
               #               ROI = ((0,ny//2),(nx,ny//2+1))
               #               axisVals = x
               #           if axis == 'y':
               #               ROI = ((nx//2,0),(nx//2+1,ny))
               #               axisVals = y
                         
               #           prof = gm.lineProfile(W, ROI=ROI, AXIS = index)
               #           Cm = gm.gratingContrastMichelson(prof)
               #           Crms = gm.gratingContrastRMS(prof)
                         
               #           C, C1, C2 = gm.meanDynamicRange(prof) 
               #           IOD, IODM, H, binEdges, binCenters =gm.integralOpticalDensity(prof)
               #           Cf,  Am, Fr, peakFr  = gm.gratingContrastFourier(prof,axisVals, show=False)
                         
               #           #for debugging - should define a variable to enable/disable
               #           #plt.plot(axisVals,prof)
               #           #plt.show()
                         
               #           metrics.update({
               #                   pkey+'profile' : prof,
               #                   pkey+'contrastMichelson' : Cm,
               #                   pkey+'contrastRMS': Crms,
               #                   pkey+'meanDynamicRangeC' : C,
               #                   pkey+'meanDynamicRangeC1' : C1,
               #                   pkey+'meanDynamicRangeC2' : C2,
               #                   pkey+'integratedOpticalDensity' : IOD,
               #                   pkey+'integratedOpticalDensityMax' : IODM,
               #                   pkey+'histogram' : H,
               #                   pkey+'histogramBins' : binEdges,
               #                   pkey+'contrastFourier' : Cf,
               #                   pkey+'fundamentalFrequency' : peakFr,
               #                   pkey+'fourierFrequency' : Fr,
               #                   pkey+'fourierAmplitude' : Am
               #                   })
                     
               #       except Exception as e: print(e)
                     
        return metrics
