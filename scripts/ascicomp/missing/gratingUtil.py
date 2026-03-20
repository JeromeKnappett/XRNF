#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 15:57:18 2022

@author: -
"""
import numpy as np
import matplotlib.pyplot as plt

def convertToBinary(tiff):
    mn,mx = np.min(tiff),np.max(tiff)
    nx,ny = np.shape(tiff)[1],np.shape(tiff)[0]
    
    print(f'max value: {mx}')
    print(f'min value: {mn}')
    print(f'nx: {nx}')
    print(f'ny: {ny}')

    tiff[tiff<(mx/2)]=0
    tiff[tiff>(mx/2)]=255
    
    return tiff

def test():
    import tifffile
    path = '/user/home/opt/xl/xl/experiments/maskLER1/masks/20000020.00000_3.00000_10.00000_mask.tif'
    
    T = tifffile.imread(path)
    
    t = convertToBinary(T)
    
#    tifffile.imwrite('/user/home/opt/xl/xl/experiments/BEUVcoherence/masks/200p25.0rMask.tif',t)
    
if __name__=='__main__':
    test()