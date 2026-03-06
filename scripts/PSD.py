#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 14 10:39:37 2025

@author: -
"""

import numpy as np
import matplotlib.pyplot as plt

def analyticalPSD_biased(f,PSD0,H,c,sigma):
    dx = 1/f[-1]
    N = 2*len(f) - 2
    PSD = PSD0 / (1 + ((abs(2 * np.pi * f * c))**((2*H + 1))))
    PSD = PSD + dx*N*(sigma**2)
    return PSD

def analyticalPSD_unbiased(f,PSD0,H,c):
    PSD = PSD0 / (1 + ((abs(2 * np.pi * f * c))**((2*H + 1))))
    return PSD

def test():
        
    PSD0 = 4e-26
    H = 1.0
    c = 4e-9
    f = np.linspace(4e5,2e9,5000)
    dx = 0.25e-9 
    N = 10000
    sigma= 1e-12
    
    PSD = analyticalPSD_biased(f, PSD0, H, c,dx,N,sigma)
    
    # PSD = PSD + dy*L*4e-20
    # slopeX = np.logspace(2e-2,2e-1,500)
    # slopeY = np.logspace(2e-27,3e-29,500)
    # slope = [s * (2*H+1) for s in slopeX]
    
    # print([s/1e9 for s in slope])
    plt.plot([_f/1e9 for _f in f],PSD,'black')
    # plt.plot(slopeX,slopeY, label='$2H + 1$')
    # plt.plot([s/1e9 for s in slopeX],[s/1e9 for s in slope], label='$2H + 1$')
    # plt.vlines(1/(2*np.pi*c)/1e9, 0, PSD0, colors='gray',linestyles = '--', label = '$1/2\pi c$')
    # plt.hlines(PSD0, 0*np.min(f)/1e9, 1e-2, colors='red',linestyles = '--',label='$PSD(0)$')
    
    plt.xscale('log')
    plt.yscale('log')
    # plt.ylim(1e-30,6e-27)
    plt.legend()
    plt.show()
    
    print('PSD(0):             ', PSD[0])
    print('PSD(lim):           ', PSD[-1])
    print('Inflection point:   ', 1/(2*np.pi*c))
    print('Slope:              ', 2*H + 1)
    print('rms:                ', 3*np.sum(PSD))
    
    
if __name__ == '__main__':
    test()