#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 15:04:04 2022

@author: -
"""
import numpy as np
import matplotlib.pyplot as plt

# %%
def getLineProfile(a,axis=0, mid=None, show=False):
    nx, ny = np.shape(a)[1], np.shape(a)[0]
    if mid == None:
        midX, midY = int(nx/2), int(ny/2)
    else:
        midX, midY = int(mid[1]), int(mid[0])    
    # print(midX)
    
    if axis == 0:
        p = a[:,midX]
        title = 'vertical profile'
    elif axis == 1:
        p = a[midY,:]
        title = 'horizontal profile'
    
    if show:
        plt.plot(p)
        plt.title(title)
        plt.show()
    
    return p