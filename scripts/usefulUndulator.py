#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 09:30:51 2023

@author: jerome
"""

import numpy as np
import matplotlib.pyplot as plt
from usefulWavefield_old import EtoWL, WLtoE



def deflectionK(B, period):
    e = 1.602176634e-19  # fundamental electron charge
    me = 9.1093837e-31  # electron mass
    c = 299792458  # speed of light
    K = (e * B * period) / (2 * np.pi * me * c)

    return K


def lorentzFactor(E):
    e = 1.602176634e-19  # fundamental electron charge
    me = 9.1093837e-31  # electron mass
    c = 299792458  # speed of light

    print(me * (c**2))

    gamma = E / ((me * (c**2) * (1 / e)))
    # gamma = 1957 * E

    return gamma

def detuning(gamma_new,gamma,N):
    zeta = ((4 * np.pi * N) * (gamma_new - gamma)) / (gamma)
    return zeta


def centralRadiationCone(gamma, N):
    theta = 1 / (gamma * np.sqrt(N))

    return theta


def undulatorEquation(period, gamma, K, m=1, theta=0):
    wl = (
        (1 / m)
        * (period / (2 * (gamma**2)))
        * (1 + ((K**2) / 2) + ((gamma**2) * (theta**2)))
    )

    return wl

def magfield4K(K,period):
    e = 1.602176634e-19  # fundamental electron charge
    me = 9.1093837e-31  # electron mass
    c = 299792458  # speed of light
    B = (2 * np.pi * K * me * c) / (e * period)
    
    return B
    

def magfield4Wavelength(period,gamma,wl,m=1,theta=0):
    Ksqrd = (((4*wl*(gamma**2))/period) - (2*(gamma**2)*(theta**2)) - 2)
    print('K^2  ', Ksqrd)
    K = np.sqrt(abs(Ksqrd)) #np.sqrt((((4*wl*(gamma**2))/period) - (2*(gamma**2)*(theta**2)) - 2))
    print('K  ', K)
    B = magfield4K(K, period)
    print('B  ', B)
    return B

# def photonFlux(N,I,n,C)

def test():
    import usefulWavefield_old
    E = 3.01e9
    Emax = 3.01307321e9 # maximum energy spread 
    Emin = 3.0069267899999996e9 # minimum energy spread
    #3.01e9 no energy spread
    period = 75e-3
    N = 25
    B =  0.46111878 
    # 0.4605460984332241
    # 0.46111878
    
    offsetE = 87.7268
    offsetWL = usefulWavefield_old.EtoWL(offsetE)
    
    Ep = 187.35
    #190.19
    #185.0
    WL = usefulWavefield_old.EtoWL(Ep)
    
    gamma = lorentzFactor(E)
    gamma_min = lorentzFactor(Emin)
    gamma_max = lorentzFactor(Emax)
    print("gamma = ", gamma)

    D_min = detuning(gamma_min, gamma, N)
    D_max = detuning(gamma_max, gamma, N)
    print("Detuning (min): ", D_min)
    print("Detuning (max): ", D_max)

    K = deflectionK(B, period)
    print("K = ", K)

    wl = undulatorEquation(period, gamma, K)
    print("wavelength = ", wl)
    wl_min = undulatorEquation(period, gamma_min, K)
    print("wavelength (Emin) = ", wl_min)
    wl_max = undulatorEquation(period, gamma_max, K)
    print("wavelength (Emax) = ", wl_max)
    
    print('Detuned E (min): ', usefulWavefield_old.WLtoE(wl_min))   
    print('Detuned E (max): ', usefulWavefield_old.WLtoE(wl_max))   
    
    B0 = magfield4Wavelength(period, gamma, wl=WL)
    print("wavelength = ", WL)
    
    print('E = ', usefulWavefield_old.WLtoE(WL))
    
    print("Mag Field = ", B0)
    
    Exfm = 8.34e3 / 7
    WLxfm = EtoWL(Exfm)
    Pxfm = 22.0e-3
    print('WL = ', WLxfm)
    Bxfm = magfield4Wavelength(Pxfm, gamma, WLxfm)
    # Kxfm = 
    print('Mag field (XFM): ', Bxfm)


if __name__ == "__main__":
    test()