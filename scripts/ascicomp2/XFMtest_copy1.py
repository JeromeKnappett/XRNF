#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 12:37:39 2024

@author: -
"""

def dN(z,wl,s):
    dN = (z * wl) / s
    return dN

def fardist(wl,s,dn):
    Z = (dn*s) / wl
    return Z


def test():
    z = 1.0e-5
    wl = 0.1486627e-9
    s = 5.0e-6
    
    dn = dN(z,wl,s)
    
    dn = 10.0e-6
    
    Z = fardist(wl, s, dn)
    
    print(Z)
    
    
if __name__ == '__main__':
    test()
    
    lam = 0.1486627e-9
    w = 75.0e-6
    R = 5.0e-6
    
    Lsd =(2* w * R) / lam
    print(Lsd)
    
    # w = (lam * Lsd) / (2 * R)