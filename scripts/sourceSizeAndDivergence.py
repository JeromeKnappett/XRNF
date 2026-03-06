#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 16 15:57:50 2024

@author: jerome
"""
import numpy as np

def sourceSizeDiv(e_size,e_div,p_size,p_div):
    "From Ivanyan et al, Proc of EPAC (2002)"
    
    s_size = np.sqrt((e_size**2) + (p_size**2))
    s_div = np.sqrt((e_div**2) + (p_div**2))
    
    return s_size, s_div

def photonBeamSizeDiv(wl,L):
    "From Ivanyan et al, Proc of EPAC (2002)"
    
    p_size = (np.sqrt((wl * L) / 2)) / (2 * np.pi)
    p_div = np.sqrt((wl / (2 * L)))
    
    return p_size, p_div

def electronBeamSizeDiv(emX,emY,betaX,betaY,eta,dE):
    e_sizeX = np.sqrt((emX * betaX) + ((dE**2) * (eta**2)))
    e_sizeY = np.sqrt((emY * betaY))
    e_divX = np.sqrt((emX / betaX))
    e_divY = np.sqrt((emY / betaY))
    
    return e_sizeX, e_sizeY, e_divX, e_divY

def beamSizeAfterProp(s_size,s_div,z):
#    size = s_size + (2 * s_div * z)
#    size = np.sqrt((s_size**2) + (((2*s_div)**2) * (z**2)))
#    size = (s_size**2) + ((s_div**2) * (z**2))
    size = s_size + (2 * z * np.tan(s_div))
    return size


def sourceEmittanceDiluted(emX,emY,e_sizeX,e_sizeY,e_divX,e_divY,p_size,p_div,betaX,betaY,Pu,L,K,gamma,eta):
    a = (Pu * K) / (2 * np.pi * gamma)
#    if plane == 'x':
    d_sqX = ((e_sizeX**2)*(eta**2)) + (p_size**2) + (a**2)
#    elif plane == 'y':
    d_sqY = (p_size**2)
    
    pX = ((L**2) / 12) + ((d_sqX) / (p_div**2))
    pY = ((L**2) / 12) + ((d_sqY) / (p_div**2))
    
#    p_s = np.sqrt(2)*p_size
#    p_d = np.sqrt(2)*p_div
#    sizeX_sq = 0.5*(p_s**2) + 
    
    em_dilX_sq = ((emX**2)*(1 + ((L**2) / (12 * (betaX**2))))) + (emX * (p_div**2) * betaX) + ((emX * (p_div**2) * pX) / (betaX)) + ((d_sqX) / (p_div**2))
    em_dilY_sq = ((emY**2)*(1 + ((L**2) / (12 * (betaY**2))))) + (emY * (p_div**2) * betaY) + ((emY * (p_div**2) * pY) / (betaY)) + ((d_sqY) / (p_div**2))
    
    em_dilX = np.sqrt(em_dilX_sq)
    em_dilY = np.sqrt(em_dilY_sq)
    
    return em_dilX, em_dilY
#    
#    emit_sqr = ((emit_e**2) * (1 + ((L**2) / (12 * (beta**2)))) + 
#                (emit_e * (p_div**2) * beta) + 
#                ((emit_e * (p_div**2) * p) / beta) + 
#                ((d**2)*(p_div**2)))
    



def diffractionLimit(wl):
    dl = wl / (4 * np.pi)
    return dl

def test():
    # undulator properties
    wl = 6.7e-9 # wavelength
    Lu = 1.875 # undulator length
    Pu = 75e-3 # undulator period
    K = 3.224659 # deflection parameter for E = 185 eV
    
    # electron beam properties
    betaX = 9
    betaY = 3
    emX = 10.0e-9
    emY = 0.009e-9
    eta = 0.1 # horizontal dispersion
    dE = 0.001021 
    gamma = 5890.423 # Lorentz factor
    
    Z = 14.3 # distance to WBS
    
    # electron beam size and divergence
    e_sizeX, e_sizeY, e_divX, e_divY = electronBeamSizeDiv(emX,emY,betaX,betaY,eta,dE)
#    e_sizeX = np.sqrt(emX * betaX)
#    e_sizeY = np.sqrt(emY * betaY)
#    e_divX = np.sqrt(emX / betaX)
#    e_divY = np.sqrt(emY / betaY)
    
    DL = diffractionLimit(wl)
    print(' ')
    print("Diffraction Limit [nm rad]:                ", DL*1e9)
    
    print(' ')
    print('Electron beam size (x,y) [um]:         ', (e_sizeX*1e6, e_sizeY*1e6))
    print('Electron beam divergence (x,y) [urad]: ', (e_divX*1e6, e_divY*1e6))
    print('Electron beam emittance (x,y) [nm rad]: ', (e_sizeX*e_divX*1e9,e_sizeY*e_divY*1e9))
    
    
    p_size, p_div = photonBeamSizeDiv(wl,Lu)
    
    
    print(' ')
    print('Single photon beam size [um]:         ', (p_size*1e6))
    print('Single photon beam divergence [urad]: ', (p_div*1e6))
    print('Single photon beam emittance (x,y) [nm rad]: ', (p_size*p_div*1e9))
    
    s_sizeX, s_divX = sourceSizeDiv(e_sizeX,e_divX,p_size,p_div)
    s_sizeY, s_divY = sourceSizeDiv(e_sizeY,e_divY,p_size,p_div)
    
    print(' ')
    print('Source size (x,y) [um]:         ', (s_sizeX*1e6, s_sizeY*1e6))
    print('Source divergence (x,y) [urad]: ', (s_divX*1e6, s_divY*1e6))
    print('Source emittance (x,y) [nm rad]: ', (s_sizeX*s_divX*1e9,s_sizeY*s_divY*1e9))
    
    propX = beamSizeAfterProp(s_sizeX,s_divX,Z)
    propY = beamSizeAfterProp(s_sizeY,s_divY,Z)
    
    print(' ')
    print('Beam size at WBS (x,y) [mm]:       ', (propX*1e3, propY*1e3))
    
#    emdX, emdY = sourceEmittanceDiluted(emX,emY,e_sizeX,e_sizeY,e_divX,e_divY,p_size,p_div,betaX,betaY,Pu,Lu,K,gamma,eta)
#    
#    print('Diluted source emittance (x,y) [nm rad]: ', (emdX,emdY))
#    
if __name__ == '__main__':
    test()