#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mutual Intensity Action

Created on Thu Oct  1 17:13:50 2020

@author: gvanriessen
"""


import action
import numpy as np
import time
from wfCoherence import getComplex, sampleField

class wfMutualIntensity(action.Action):
    '''
    This action returns the mutual intensity matrix J which it then uses to find the Stokes parameters and degree of polarisation.
    '''   
    def __init__(self):
        super().__init__()
        self.description = 'Action: Mutual intensity, Spatial Coherence Properties and Polarisation Properties'
        
    def perform_operation(self, *args, **kwargs):
        
   
        # allow disable if {self.__class__.__name__: True}
        try:
            if kwargs['parameters'][self.__class__.__name__] == False:
                print('...disabled.')
                return {}
        except: pass

        w = kwargs['wavefront']
        #p = kwargs['parameters']

        
        print("----Starting Mutual Intensity Function---")
    
        print("Converting to complex wavefields and extracting each polarisation component")
        start1 = time.time()
        cfrT = getComplex(w, polarization = "total")
        cfrH = getComplex(w, polarization = "horizontal")
        cfrV = getComplex(w, polarization = "vertical")
        end1 = time.time()
        print('Time taken to convert to complex wavefield (s): {}'.format(end1 - start1))

        limit = 200 # maximum number of pixels in each direction to be sampled (can't be too large due to memory restrictions) 

        FxT = limit/np.shape(cfrT)[1]
        FyT = limit/np.shape(cfrT)[0] 
        FxH = limit/np.shape(cfrH)[1]
        FyH = limit/np.shape(cfrH)[0] 
        FxV = limit/np.shape(cfrV)[1]
        FyV = limit/np.shape(cfrV)[0]


        """ Taking sample area at centre of each complex wavefield array """
        A_T = sampleField(cfrT, Fx=FxT, Fy=FxT, Limit = limit)
        A_H = sampleField(cfrH, Fx=FxH, Fy=FyH, Limit = limit)
        A_V = sampleField(cfrV, Fx=FxV, Fy=FyV, Limit = limit)

        """ Mutual Intensity Functions (J, Jxx, Jxy, Jyx, Jyy) """
        print(" ")
        print("-----Calculating Mutual Intensity array (J)-----")
        start2 = time.time()
        J = np.array([A_T.conjugate()*a for a in A_T.flatten()])
        Jxx = np.array([A_H.conjugate()*a for a in A_H.flatten()])
        Jxy = np.array([A_H.conjugate()*a for a in A_V.flatten()])
        Jyx = np.array([A_V.conjugate()*a for a in A_H.flatten()])
        Jyy = np.array([A_V.conjugate()*a for a in A_V.flatten()])
        end2 = time.time()
        print('Time taken to calculate Mutual Intensity Functions [J] (s): {}'.format(end2 - start2))

        print("Shape of each Mutual Intensity array:")
        print("J: {}".format(np.shape(J)))
        print("Jxx: {}".format(np.shape(Jxx)))
        print("Jxy: {}".format(np.shape(Jxy)))
        print("Jyx: {}".format(np.shape(Jyx)))
        print("Jyy: {}".format(np.shape(Jyy)))

        """ Averaging each Mutual Intensity Array """
        j = abs(J.mean(0))
        jxx = abs(Jxx.mean(0))
        jxy = abs(Jxy.mean(0))
        jyx = abs(Jyx.mean(0))
        jyy = abs(Jyy.mean(0))

        
        print("-----Getting Stokes Parameters and Degree of Polarisation from J-----")
        
        J = np.array([[jxx, jxy], [jyx, jyy]])
        
        print("Shape of J: {}".format(np.shape(J)))
        
        import cmath
        """ Getting Stokes Parameters """
        S0 = jxx + jyy
        S1 = jxx - jyy
        S2 = jxy + jyx
        S3 = cmath.sqrt(-1)*(jxy - jyx)
        
        """ Normalising Stokes Parameters """
        s0 = S0/S0
        s1 = S1/S0
        s2 = S2/S0
        s3 = S3/S0
        
        """ Normalised Stokes Vector """
        s = np.array([[s0.mean(),s1.mean(),s2.mean(),s3.mean()]]).T
        
        """ Getting Degree of Polarisation """
        detJ = (jxx*jyy - jxy*jyx) #np.linalg.det(J)
        P = (1 - ((4*detJ)/((jxx + jyy)**2)))**(1/2)
        


        # return a dictionary.
        return {'mutualIn_j': j, 'mutualIn_jxx': jxx, 'mutualIn_jxy': jxy, 'mutualIn_jyx': jyx, 'mutualIn_jyy': jyy, 'S0': S0, 'S1': S1, 'S2': S2, 'S3': S3, 'stokesVector': s, 'degOfPolarisation': P}
