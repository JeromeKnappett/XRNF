#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 17:03:05 2023

@author: -
"""
import numpy as np
import matplotlib.pyplot as plt
import xraydb
import usefulGrating

def fluxDensityDist_Grating(I0,wl,N,p,theta):
    k = 2*np.pi/wl
    b = p/2
    A = (k*p/2)*np.sin(theta)
    B = (k*b/2)*np.sin(theta)
    
    part1 =  ((np.sin(B))/B)
    part2 = ((np.sin(N*A)) / (np.sin(A)))
    
    I = I0 * (part1**2) * (part2**2)
    return I

def fluxFromGrating(I0,wl,N,p):
    theta = np.linspace(-np.pi/4,np.pi/4,500)
    k = 2*np.pi/wl
    b = p/2
    A = (k*p/2)*np.sin(theta)
    B = (k*b/2)*np.sin(theta)
    
    part1 =  ((np.sin(B))/B)
    part2 = ((np.sin(N*A)) / (np.sin(A)))
    
    I = I0 * (part1**2) * (part2**2)
    
    plt.plot(A,I)
    # plt.plot(theta,A)
    # plt.plot(theta,B)
    # plt.plot(theta,part1)
    # plt.plot(theta,part2)
    plt.show()
    
    theta1 = usefulGrating.diffractionAngle(wl, p)
    
    I0 = fluxDensityDist_Grating(I0, wl, N, p, theta=0)
    I1 = fluxDensityDist_Grating(I0, wl, N, p, theta1)
    
    print(I0)
    print(I1)
    print(I1/I0)
    
    # p2I = [int(p) for p in part2]
    # mi = np.where(p2I==N) #part2.index(N)
    # print(mi)
    # I_I[part2==N]
    
    
def efficiency(p,T,k,delta):
    I_0 = (p**2 / 2) * (1 + np.exp(-4*np.pi*T*k))
    I_m = (np.exp(-2*np.pi*T*k) * np.cos(2*np.pi*T*delta)*(p/np.pi) + (np.cos(p)*np.sin(p/2)))**2 + (np.exp(-2*np.pi*T*k) * np.sin(2*np.pi*T*delta) * (p/np.pi))**2
    
    eff = I_m / I_0
    
    return eff

def test():
    p = 100e-9
    T = 20e-9
    k = 1.22e-2
    delta = 2.53e-2
    
    # e = efficiency(p,T,k,delta)
    
    # print(e*100)
    
    fluxFromGrating(1,6.7e-9,50, 100e-9)
    
    
    
    
if __name__ == '__main__':
    test()