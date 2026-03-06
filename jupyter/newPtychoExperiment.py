#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 15:48:08 2024

@author: -
"""

import numpy as np
from usefulWavefield_old import EtoWL

def gainFactor(Lx,Ly,dr):
    """
    Ptychographic Gain Factor

    Parameters
    ----------
    Lx : Probe size in x.
    Ly : Probe size in y.
    dr : Spatial resolution.

    Returns
    -------
    Gp: Gain factor.
    """
    
    Gp = np.sqrt( (Lx * Ly) / (dr**2) )
    return Gp

def overlap(R,L):
    """
    Overlap in a ptychographic experiment
    
    Parameters
    ----------
    R : Distance between probe points.
    L : Probe size.

    Returns
    -------
    Olap : Overlap.
    """
    
    Olap = 1 - (R / L)
    return Olap

def numPositions(A,Lx,Ly,Olap):
    
    N = A / ((Lx * Ly) * ((1 - Olap)**2))
    return N

def checkSampling(wl,Zsd,L,px,overlap=None,verbose=False):
    """

    Parameters
    ----------
    wl : Wavelength
    Zsd : Sample-to-detector distance
    L : Probe/Sample size.
    px : Pixel size.
    
    -------
    SR: Sampling ratio (must be >2 for oversampling) .
    """
    
    if overlap == None:
        SR = (wl * Zsd) / (L * px)
    else:
        SR = ( (wl * Zsd) / ( (1 - overlap) * L * px) )**2
        
    if verbose:
        print(f"Sampling Ratio = {SR}")
    
        if SR>=2:
            print("(:  !!! Adequate sampling !!!  :)")
        else:
            print("):  !!! Inadequate sampling !!!  :(")
    else:
        pass
        
    return SR
        

def minDistanceForSampling(wl,L,px,dims=1,overlap=None):
    if overlap == None:
        Zsd = ((2**(1.0/dims)) * L * px) / (wl)
    else:
        Zsd = ((2**(1.0/dims)) * (1 - overlap) * L * px) / wl
    return Zsd

def minDistSampling_NoProb(wl,R,px):
    z = (R * px) / wl
    return z

def minDistanceForSpeckle(wl,L,px):
    """
    Parameters
    ----------
    wl :Wavelength
    L : Probe size at sample.
    px : Pixel size of detector.

    Returns
    -------
    Zmin : Minimum sample-to-detector distance to resolve speckle
    """
    Ws = 2*px # speckle width needs to be at least 2 pixels to resolve
    
    print('Speckle width check:     ', Ws*1e6, ' um')

    Z = (Ws * L) / wl
  
    # lam = 0.1486627e-9
    # w = 75.0e-6
    # R = 5.0e-6
    
    # Lsd =(2* w * R) / lam
    # print(Lsd)
    # Lsd = (w * R) / wl
    return Z

def speckleWidth(lam, L, Zsd):
    """
    From L Fan, D Paterson, I McNulty, MMJ Treacy, and JM Gibson. Fluctuation
    x-ray microscopy: a novel approach for the structural study of disordered
    materials.
    ----------
    lam : Wavelength
    L : Probe size at sample.
    Zsd : Distance from sample to detector.

    Returns
    -------
    w : speckle width.
    """
    w = (lam * Zsd) / (L)
    return w

    

def reconstructedResolution(wl,Zsd,N,px):
    dXs = (wl * Zsd) / (N * px)
    return dXs



def test():
    # Experimental setup A: Conventional ptychography of a FZP
    Lx = 2.0e-6         # probe size in x
    Ly = 2.0e-6         # probe size in y
    dr  = 45.0e-9       # required resolution
    R = 260.0e-9     #0.2*Lx          # Distance between probe positions
    A = 50.0e-6**2      # Area to be imaged
    E = 8332.9            # Photon energy (eV)
    wl = EtoWL(E)
    Np = 2048            # number of detector pixels
    px = 75.0e-6        # pixel size
    
    print(f'Wavelength: {wl}')
    
    G = gainFactor(Lx, Ly, dr)
    O = overlap(R, Lx)
    N = numPositions(A, Lx, Ly, O)
    
    Zsd = minDistanceForSampling(wl, Lx, px, dims=2)#, overlap=O)
    sr = checkSampling(wl, Zsd, Lx, px)#, overlap=O)
    dXs = reconstructedResolution(wl, Zsd, Np, px)
    Ws = speckleWidth(wl, Lx, Zsd)
    
    zmin = minDistanceForSpeckle(wl,Lx,px)
    SR = checkSampling(wl, zmin, Lx, px)#, overlap=O)
    DXS = reconstructedResolution(wl, zmin, Np, px)
    WS = speckleWidth(wl, Lx, zmin)
    
    # Zcheck = minDistSampling_NoProb(wl, R, px)

    print('\n ---- Conventional ptychography parameters ----')
    print(f'Scan step size:                {R} m ')
    print(f'Gain factor:                   {G}')
    print(f'Overlap:                       {O}')
    print(f'Number of positions:           {N}')
    print(f'Minimum distance for sampling: {Zsd}')
    print(f' -Sampling Ratio:                {sr}')
    print(f' -Resolution of Resonstruction:  {dXs}')
    print(f' -Speckle Width:                 {Ws}')
    print(f'Minimum distance for speckle:  {zmin}')
    print(f' -Sampling Ratio:                {SR}')
    print(f' -Resolution of Resonstruction:  {DXS}')
    print(f' -Speckle Width:                 {WS}')
    # print(f'Minimum distance for sampling (CHECK): {Zcheck}')
    
    
    # Experimental setup A: Tele-ptychography of a FZP exit wavefield
    Lx = 5.0e-6         # Aperture size in x
    Ly = 5.0e-6         # Aperture size in y
    dr  = 45.0e-9       # required resolution
    R = 260.0e-9          # Distance between probe positions
    A = 130.0e-6*70.0e-6      # Area to be imaged
    
    G = gainFactor(Lx, Ly, dr)
    O = overlap(R, Lx)
    N = numPositions(A, Lx, Ly, O)
    
    Zsd = minDistanceForSampling(wl, Lx, px/10, dims=2)#, overlap=O)
    sr = checkSampling(wl, Zsd, Lx, px)#, overlap=O)
    dXs = reconstructedResolution(wl, Zsd, Np, px)
    Ws = speckleWidth(wl, Lx, Zsd)
    
    zmin = minDistanceForSpeckle(wl,Lx,px)
    SR = checkSampling(wl, zmin, Lx, px)#, overlap=O)
    DXS = reconstructedResolution(wl, zmin, Np, px)
    WS = speckleWidth(wl, Lx, zmin)
    
    # Zcheck = minDistSampling_NoProb(wl, R, px)

    print('\n ---- Tele-ptychography parameters ----')
    print(f'Scan step size:                {R} m ')
    print(f'Gain factor:                   {G}')
    print(f'Overlap:                       {O}')
    print(f'Number of positions:           {N}')
    print(f'Minimum distance for sampling: {Zsd}')
    print(f' -Sampling Ratio:                {sr}')
    print(f' -Resolution of Resonstruction:  {dXs}')
    print(f' -Speckle Width:                 {Ws}')
    print(f'Minimum distance for speckle:  {zmin}')
    print(f' -Sampling Ratio:                {SR}')
    print(f' -Resolution of Resonstruction:  {DXS}')
    print(f' -Speckle Width:                 {WS}')
    # print(f'Minimum distance for sampling (CHECK): {Zcheck}')
    
    
if __name__ == '__main__':
    test()