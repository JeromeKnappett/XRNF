#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mutual Intensity Action

Created on Thu Oct  1 17:13:50 2020

@author: gvanriessen
"""


import action

class wfMutualIntensity(action.Action):
    '''
    This action returns the mutual intensity matrix J.
    '''   
    def __init__(self):
        super().__init__()
        self.description = 'Action: Mutual intensity and Spatial Coherence Properties'
        
    def perform_operation(self, *args, **kwargs):
        
        w = kwargs['wavefront']
        #p = kwargs['parameters']
        
        
        # allow disable if {self.__class__.__name__: True}
        try:
            if kwargs['parameters'][self.__class__.__name__] == True:
                return {}
        except: pass
        
        print("----Starting Mutual Intensity Function---")
    
        print("Converting to complex wavefields and extracting each polarisation component")
        start1 = time.time()
        cfrT = getComplex(w, polarization = "total")
        cfrH = getComplex(w, polarization = "horizontal")
        cfrV = getComplex(w, polarization = "vertical")
        end1 = time.time()
        print('Time taken to convert to complex wavefield (s): {}'.format(end1 - start1))

        """ Taking sample area at centre of each complex wavefield array """
        A_T = sampleField(cfrT, Fx=Fx, Fy=Fy, Limit = 200)
        A_H = sampleField(cfrH, Fx=Fx, Fy=Fy, Limit = 200)
        A_V = sampleField(cfrV, Fx=Fx, Fy=Fy, Limit = 200)

        """ Mutual Intensity Functions (J, Jxx, Jxy, Jyx, Jyy) """
        print(" ")
        print("-----Calculating Mutual Intensity arrays-----")
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


        print(" ")
        print("-----Getting Stokes Parameters and Degree of Polarisation from J-----")
        path ='/data/YDStest/13nm/' 
        extra = "_200nm"
        pathSJ = path + "Stokes" + extra + ".png" # Save path for Stokes plot
        pathP = path + "Polarisation" + extra + ".png" # Save path for degree of Polarisation plot

        stokesFromJ(jxx,jxy,jyx,jyy,pathSJ, pathP)
        
        # return a dictionary.
        return {'mutualIn_j': j, 'mutualIn_jxx': jxx, 'mutualIn_jxy': jxy, 'mutualIn_jyx': jyx, 'mutualIn_jyy': jyy}
