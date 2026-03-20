#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 24 12:31:21 2021
@author: jknappett
"""


import action
import numpy as np
import time

class wfComplexProfile(action.Action):
    '''
    This action returns the horizontal and vertical line profiles through the centre of the complex wavefield for each polarisation component.
    '''   
    def __init__(self):
        super().__init__()
        self.description = 'Action: Complex Wavefield line profiles'
        
    def perform_operation(self, *args, **kwargs):
        
        
        # allow disable if {self.__class__.__name__: True}
        try:
            if kwargs['parameters'][self.__class__.__name__] == False:
                print('...disabled.')
                return {}
        except: pass
        
        w = kwargs['wavefront']
        
        print("----Starting wfComplexProfile---")
        
        from wfCoherence import getComplex
        
        print("Converting to complex wavefields and extracting each polarisation component")
        start1 = time.time()
        cfrT = getComplex(w, polarization = "total")
        cfrH = getComplex(w, polarization = "horizontal")
        cfrV = getComplex(w, polarization = "vertical")
        end1 = time.time()
        print('Time taken to convert to complex wavefield (s): {}'.format(end1 - start1))

        """ Finding number of points in each line profile """
        numX = int(np.max(np.shape(cfrT[:,0,0]))) # These are in pixels
        numY = int(np.max(np.shape(cfrT[0,:,0])))

        midX = int(numX/2) # centre pixel in horizontal line profile
        midY = int(numY/2) # centre pixel in vertical line profile

        """ Taking line profiles through each array """
        P_Tx = cfrT[:,midY]
        P_Ty = cfrT[midX,:]
        P_Hx = cfrH[:,midY]
        P_Hy = cfrH[midX,:]
        P_Vx = cfrV[:,midY]
        P_Vy = cfrV[midX,:]

        # return a dictionary.
        return {'cpX_totP': P_Tx, 'cpY_totP': P_Ty, 'cpX_horP': P_Hx, 'cpY_horP': P_Hy, 'cpX_verP': P_Vx, 'cpY_verP': P_Vy}
