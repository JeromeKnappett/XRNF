#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 14:31:46 2023

@author: -
"""
from usefulWavefield import intensity2power

def neededDoseOnMask(D0,N,eff,T):
    """
    D0: Required dose-on-wafer to remove 50% of resist, in mJ/s/cm^2
    N: Number of gratings in mask
    eff: Grating efficiency
    T: Substrate transmission
    
    returns:
        Dm: Required dose-on-mask, in mJ/s/cm^2
    """
    Dm = D0 / ((N**3)*eff*T)
    return Dm

def DoseOnWafer(Dm,N,eff,T):
    """
    Dm: Dose-on-mask, in mJ/s/cm^2
    N: Number of gratings in mask
    eff: Grating efficiency
    T: Substrate transmission
    
    returns:
        Dw: Resulting dose-on-wafer
    """
    
    Dw = Dm*(N**3)*eff*T
    
    return Dw
    

def test():
    d0 = 11.0 #30.0 #33.2#80#33.2#80
    N = 4
    e = 0.06 #0.10 #0.28
    #0.06#1175 # Efficiency value from Wang. et al
    T = 0.86455 # transmission of 40 nm SiO2 @ 293 eV
    # 0.67177
    # 0.81962   # Transmission of 40 nm SiO2
    # 0.71 # Transmission of 40 nm Si3N4
    #redone below
    # Si02 transmission:         0.67177
    # Si3N4 transmission:        0.50396
    E = 293
    DM = neededDoseOnMask(d0, N, e, T)
    print(DM)
    print(f'\n Needed Dose-On-Mask for {d0} mJ/cm^2:  {DM}  mJ/cm^2')
    flux = 48736016906214.91 #2.4e13
    # 24301083781652.6
    # 17132489347445.75
    # 16423487217521.844
    # 18797196469572.484
    # 3.0e8#5.85e13
    #3e15
    # 64707430235494.3
    # 5.85e13
    # 29558032758953.895, 64707430235494.3
    # 5.86e13#6.6e13 #(300,300)
    # 6.6e13 #(300,300)
    #2.3E12  # (1500,1500)
    #1.6e8
    #2.6e13 # (900,300)
    # 2.9e12#4.0e13#4.5e12# 2.0e13# 0.93e15 #1.2e13
    
    Dm = intensity2power(flux,E)#92)#185)
    print(f'\n Dose-On-Mask:  {Dm}  mJ/s/cm^2')
    
    # Dm = 5
    DW = DoseOnWafer(Dm,N,e,T)
    
    print(f'\n Dose-On-Wafer:  {DW}  mJ/s/cm^2')
    
    
    print(f'\n Exposure time for current dose-on-mask:  {(d0 / DW)} seconds')
    print(f' Exposure time for current dose-on-mask:  {(d0 / DW)/60} minutes')
    
    # print((DM/11.856132))

if __name__ == '__main__':
    test()
    
