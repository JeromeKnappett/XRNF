#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Stokes parameters and degree of polarisation action

Created on Thu Oct  1 17:13:50 2020

@author: gvanriessen
"""


import action

class wfPolarisation(action.Action):
    '''
    This action returns the Stokes parameters and the degree of polarisation.
    '''   
    def __init__(self):
        super().__init__()
        self.description = 'Action: Mutual intensity and Spatial Coherence Properties'
        
    def perform_operation(self, *args, **kwargs):
        
        w = kwargs['wavefront']
        Jxx = kwargs['parameters']['mutualIn_jxx']
        Jxy = kwargs['parameters']['mutualIn_jxy']
        Jyx = kwargs['parameters']['mutualIn_jyx']
        Jyy = kwargs['parameters']['mutualIn_jyy']
        
        # allow disable if {self.__class__.__name__: True}
        try:
            if kwargs['parameters'][self.__class__.__name__] == True:
                return {}
        except: pass
        
        print(" ")
        print("-----Getting Stokes Parameters and Degree of Polarisation from J-----")
        
        J = np.array([[Jxx, Jxy], [Jyx, Jyy]])
        
        print("Shape of J: {}".format(np.shape(J)))
        
        import cmath
        """ Getting Stokes Parameters """
    	S0 = Jxx + Jyy
    	S1 = Jxx - Jyy
    	S2 = Jxy + Jyx
    	S3 = cmath.sqrt(-1)*(Jxy - Jyx)
    	
    	""" Normalising Stokes Parameters """
        s0 = S0/S0
        s1 = S1/S0
        s2 = S2/S0
        s3 = S3/S0
        
        """ Normalised Stokes Vector """
        s = np.array([[s0.mean(),s1.mean(),s2.mean(),s3.mean()]]).T
    
    	""" Getting Degree of Polarisation """
    	detJ = (Jxx*Jyy - Jxy*Jyx) #np.linalg.det(J)
    	P = (1 - ((4*detJ)/((Jxx + Jyy)**2)))**(1/2)

        
        # return a dictionary.
        return {'S0': S0, 'S1': S1, 'S2': S2, 'S3': S3, 'stokesVector': s, 'degOfPolarisation': P}
