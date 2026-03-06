#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 09:44:23 2023

@author: jerome
"""

import numpy as np
import matplotlib.pyplot as plt

def imageDistance(wl,p,d,m=1):
    z = (d * np.sqrt((p**2) - ((m**2)*(wl**2)))) / (2*m*wl)
    return z

def gratingSep4z(wl,p,z,m=1):
    d = (2*m*wl*z) / (np.sqrt((p**2) - ((m**2)*(wl**2))))
    return d

def test(): 
    w1 = 6.7e-9
    w2 = 13.5e-9
    p = [120.0e-9,160.0e-9,200.0e-9]
    d = [200e-6,200e-6,200.0e-6]
    
    for P,D in zip(p,d):
        z1 = imageDistance(w1,P,D)
        z2 = imageDistance(w2,P,D)
        
#        print("wl = 6.7 nm, p = ", P*1e9, " nm, d = ", D*1e6, " um,  z = ", z1*1e6, " um")
        print("wl = 13.5 nm, p = ", P*1e9, " nm, d = ", D*1e6, " um,  z = ", z2*1e6, " um")
#        print("$\lambda = 13.5$ nm, $z=$", z2*1e6, " um")
        
    z = imageDistance(w2,160.0e-9,200.0e-6)
    for P in p:
        D = gratingSep4z(w2,P,z)
        print(D*1e6)

if __name__ == '__main__':
    test()