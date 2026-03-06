
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
 
class wfInterferencePatternProperties1D(Action):
    '''
    This action returns multiple metrics relevant to the contrast and quality of an
    interference pattern.
    '''   
    
    def __init__(self):
        super().__init__()
        self.description = 'Action: 1D Interference Pattern Properties (testing strip)'


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
            nilsNominalLinewidth = kwargs['parameters']['NILSNominalLinewidth']
        except:
            nilsNominalLinewidth = 1.e-9    
        
        print('DEBUG: nilsNominalLinewidth ',nilsNominalLinewidth)

        try:
            profileWidth = kwargs['parameters']['profileWidth']
            
        except:
            profileWidth =1
            
        print('DEBUG: profileWidth ', profileWidth)

        if profileWidth > 1:
            profilelo, profilehi = profileWidth//2, profileWidth//2
        else:    
            profilelo, profilehi = 1, 0 
            
        x =  np.linspace(wfr.params.xCentre-wfr.params.Rx/2,
                          wfr.params.xCentre+wfr.params.Rx/2,
                          wfr.params.Mesh.nx)
        y =  np.linspace(wfr.params.yCentre-wfr.params.Ry/2,
                          wfr.params.yCentre+wfr.params.Ry/2,
                          wfr.params.Mesh.ny)
        metrics = {}
        metrics['x'] = x
        metrics['y'] = y
         

        #for pol in ['total']:
        for pol in ['total','horizontal','vertical']:
            I = wfr.get_intensity(polarization=pol)
        
            P = wfr.get_phase(polarization=pol)
            #for prop,W in zip(['intensity','phase'],[I,P]):
            for prop, W in zip(['intensity'],[I]):    

                #for debugging - should define a variable to enable/disable
                #plt.imshow(I[:,:,0])
                #plt.imshow(P[:,:,0])
                
                
                ''' analyse 1D (profiles) combinations of polarisation modes and type (intensity | phase) '''
                #for axis, index in zip(['x','y'],[0,1]):
                for axis, index in zip(['y'],[1]):
                      try:
                          pkey = prop.capitalize() + '/' +  pol.capitalize() + '/' + axis.capitalize() + '/'
                          #print('Profile: '+ pkey)
                          print('ProfileWide: '+ pkey)
                          
                          ny=wfr.params.Mesh.ny
                          nx=wfr.params.Mesh.nx
                          if  axis == 'x':
                              ROI = ((0,ny//2-profilelo),(nx,ny//2+profilehi))
                              axisVals = x
                          if axis == 'y':
                              ROI = ((nx//2-profilelo,0),(nx//2+1,ny+profilehi))
                              axisVals = y
                         
                          prof = gm.lineProfile(W, ROI=ROI, AXIS = index)
                          Cm = gm.gratingContrastMichelson(prof)
                          Crms = gm.gratingContrastRMS(prof)
                         
                          C, C1, C2 = gm.meanDynamicRange(prof) 
                          IOD, IODM, H, binEdges, binCenters =gm.integralOpticalDensity(prof)
                          Cf,  Am, Fr, peakFr  = gm.gratingContrastFourier(prof,axisVals, show=False)
                          NILS = gm.NILS(prof,axisVals, nilsNominalLinewidth, show=False)

                          #for debugging - should define a variable to enable/disable
                          #plt.plot(axisVals,prof)
                          #plt.show()
                         
                          metrics.update({
                                  pkey+'profile' : prof,
                                  pkey+'contrastMichelson' : Cm,
                                  pkey+'contrastRMS': Crms,
                                  pkey+'meanDynamicRangeC' : C,
                                  pkey+'meanDynamicRangeC1' : C1,
                                  pkey+'meanDynamicRangeC2' : C2,
                                  pkey+'integratedOpticalDensity' : IOD,
                                  pkey+'integratedOpticalDensityMax' : IODM,
                                  pkey+'histogram' : H,
                                  pkey+'histogramBins' : binEdges,
                                  pkey+'contrastFourier' : Cf,
                                  pkey+'fundamentalFrequency' : peakFr,
                                  pkey+'fourierFrequency' : Fr,
                                  pkey+'fourierAmplitude' : Am,
                                  pkey+'NILS': NILS
                                  })
                     
                      except Exception as e: print(e)
                     
        return metrics
