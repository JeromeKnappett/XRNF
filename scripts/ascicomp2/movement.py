#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 29 12:32:10 2023

@author: -
"""
import numpy as np
import matplotlib.pyplot as plt

def distB(v,r,t):
    x = 2*v*t
    _b = np.sqrt(abs((r**2) - (((2*x)**2)/4)))
    b = r - np.sqrt(abs((r**2) - (((2*x)**2)/4)))
    # print(" ")
    # print(x)
    # print(_b)
    # print(b)
    return b


def test():
    ve = 460
    re = 6.371e6
    vs1 = 8.138889
    vs2 = 8.416667
    rs = 151.9e9
    
    29.3,30.3
    
    T = range(0,10)
    
    for t in T:
        
        de = distB(ve,re,t)
        ds = distB(vs1,rs,t)
        # print(str(t) + ': ' + str(ds))
        
        D = de + ds
        
        plt.plot(t,D,'.',color='r')
    plt.xlabel('time (s)')
    plt.ylabel('distance (m)')
    plt.show()
    
    
if __name__ == '__main__':
    test()
    
    91.435 - 90.44
187.5 - 184.76