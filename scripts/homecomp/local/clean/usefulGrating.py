#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 14:18:09 2022

@author: jerome
"""

import numpy as np
import matplotlib.pyplot as plt


""" Useful Diffraction Grating Equations """

def maxOrder(p,wl,n=1):
    """
    Finds the maximum diffracted order of a transmission grating 
    at normal incidence.
    ------
    p: grating pitch
    wl: incident wavelength
    n: refractive index of of region after grating
    ------
    returns
    m_max: maximum diffraction order
    """
    m_max = int((n*p)/wl)
    return m_max

def totalOrders(p,wl,n=1):
    """
    Finds the total number of diffracted orders from a transmission 
    grating at normal incidence.
    ------
    p: grating pitch
    wl: incident wavelength
    n: refractive index of of region after grating
    ------
    returns
    M: total diffracted orders
    """
    m_max = maxOrder(p,wl,n)
    M = 2*m_max + 1
    return M

def gratingEquation(p,wl,m,ti=0,phi=np.pi/2,ni=1,nt=1):
    """
    Grating equation - Finds the diffraction angle from a diffraction grating.
    ------
    p: grating pitch
    wl: incident wavelength
    m: diffracted order
    ti: angle of incident light
    phi: rotation angle of grating
    ni: refractive index of of region before grating
    nt: refractive index of of region after grating
    ------
    returns
    tm: angle of transmitted order m
    """
    tm = np.arcsin( (1/nt) * (ni*np.sin(ti) - m*(wl/p)*np.sin(phi)))
    return tm


def visibilityTM(wl,p):
    """
    Visibility of an aerial image formed by TM incident light.
    ------
    wl: incident wavelength
    p: grating pitch
    ------
    returns:
    V: Visibility
    """
    V = 1 - (2*((wl/p)**2))
    return V

def zComponentTM(wl,p):
    """
    z component of electric field introduced after diffraction of TM incident 
    light from a grating.
    ------
    wl: incident wavelength
    p: grating pitch
    ------
    returns:
    xComp: x-component of electric field
    zComp: z-component of electric field
    """
    theta = diffractionAngle(p,wl)
    xComp = np.cos(theta)
    zComp = np.sin(theta)
    return xComp, zComp

def opticalAxisIntercept(wl,p,d,m=1,theta=0):
    """
    Distance to aerial image from a multiple-grating mask.
    ------
    wl: incident wavelength
    p: grating pitch
    d: grating sepatation (centre-to-centre)
    theta: incident angle
    m: diffraction order
    ------
    return
    z: distance from grating plane at which order intercepts optical axis"""
    
    z = d/(2*np.tan(gratingEquation(p,wl,m,ti=theta)))
    
    return abs(z)


def aerialImageDistance(wl,p,d,m=1):
    """
    Alternative method for calculating the distance to aerial image 
    from a multiple-grating mask.
    ------
    wl: incident wavelength
    p: grating pitch
    d: grating sepatation (centre-to-centre)
    m: diffraction order
    ------
    return
    z: distance from grating plane at which order intercepts optical axis"""
    
    z = (d*(np.sqrt((p**2) - ((m**2)*(wl**2)))))/(2*m*wl)
    
    return z

def test():
    p = 50e-9
    wl = 6.7e-9
    wl3, wl5 = wl/3, wl/5
    m = 1
    d = 100e-6 #27.5e-6
    ni=1
    nt=1
    
    m_max = maxOrder(p,wl,n=nt)
    M = totalOrders(p,wl,n=nt)
    T = gratingEquation(p,wl,m=m_max,ni=ni,nt=nt)
    Z = opticalAxisIntercept(wl,p,d,m=m_max)
    z = aerialImageDistance(wl,p,d,m=14)
    
    print(m_max)
    print(M)
    print(np.rad2deg(T))
    print(Z)
    print(z)
    
    P = np.linspace(wl,p,1000)
    
    mMax = [maxOrder(_p,wl) for _p in P]
    mMax3 = [maxOrder(_p,wl3) for _p in P]
    mMax5 = [maxOrder(_p,wl5) for _p in P]
    
    plt.plot(P*1e9,mMax, label='fundamental')
    plt.plot(P*1e9,mMax3, label='3rd')
    plt.plot(P*1e9,mMax5, label='5th')
    plt.xlabel('Grating pitch [nm]')
    plt.ylabel('Maximum Diffracted Order')
    plt.legend()
    plt.show()    

if __name__ == '__main__':
    test()
    