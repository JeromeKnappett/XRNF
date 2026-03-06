#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 13 09:57:11 2022

@author: jerome
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.pyplot import figure
from scipy.signal import find_peaks
#from useful import round_sig
from mpl_toolkits.axes_grid1.axes_divider import make_axes_locatable
from matplotlib.colors import LogNorm


def round_sig(x, sig=2):
    if x != 0:
        return round(x, sig-int(floor(log10(abs(x))))-1)
    else:
            return x

def moirePeriod(p1,p2):
    """
    Parameters
    ----------
    p1 : Pitch of 2nd & 4th quadrants of centosymmetric square grating.
    p2 : Pitch of 1st & 3rd quadrants of centosymmetric square grating.

    Returns
    -------
    P : Period of moire fringe.
    """
    P = (p1*p2)/(p2-p1)
    return P

def displacementRatio(p1,p2):
    """
    Parameters
    ----------
    p1 : Pitch of 2nd & 4th quadrants of centosymmetric square grating.
    p2 : Pitch of 1st & 3rd quadrants of centosymmetric square grating.

    Returns
    -------
    Z : ratio of moire fringe displacement to actual misalignment.
    """
    Z = (p1+p2)/(p2-p1)
    return Z

def maxMisalignment(p1,p2):
    """
    Parameters
    ----------
    p1 : Pitch of 2nd & 4th quadrants of centosymmetric square grating.
    p2 : Pitch of 1st & 3rd quadrants of centosymmetric square grating.

    Returns
    -------
    dXmax : Maximum misalignment measurement.
    """
    dXmax = (p1*p2)/(p1+p2)
    return dXmax

def minGratingSize(p1,p2):
    """
    Parameters
    ----------
    p1 : Pitch of 2nd & 4th quadrants of centosymmetric square grating.
    p2 : Pitch of 1st & 3rd quadrants of centosymmetric square grating.

    Returns
    -------
    Lmin : Minimum size of moire grating.
    """
    Lmin = 2*moirePeriod(p1, p2)
    return Lmin

def misalignmentFromMoire(DX,p1,p2):
    """
    Parameters
    ----------
    DX : Moire fringe displacement
    p1 : Pitch of 2nd & 4th quadrants of centosymmetric square grating.
    p2 : Pitch of 1st & 3rd quadrants of centosymmetric square grating.

    Returns
    -------
    dx : Actual misalignment.
    """
    dx = DX/displacementRatio(p1, p2)
    return dx

def minMisalignment(p1,p2,N,Re,C):
    """
    Parameters
    ----------
    p1 : Pitch of 2nd & 4th quadrants of centosymmetric square grating.
    p2 : Pitch of 1st & 3rd quadrants of centosymmetric square grating.
    N : Number of pixels in visual field
    Re : Resolution of microscope
    C : Recognition coefficient of image processing (>1, C=10 for normal image processing)
    
    Returns
    -------
    dXmin : Minimum resolvable misalignment.
    """
    dXmin = max((Re/C)*((p2-p1)/(p1+p2)),(p1/(C*N)))
    return dXmin

def minPitchDiff(e):
    """
    Parameters
    ----------
    e : Fabrication tolerance of p1 or p2.

    Returns
    -------
    dpmin : Minimum pitch discrepency for centrosymmetric square grating
    """
    dpmin = np.sqrt(2)*e
    return dpmin

def gratingTransmittance(p1,p2,L,N):
    """
    Parameters
    ----------
    p1 : Pitch of 2nd & 4th quadrants of centosymmetric square grating.
    p2 : Pitch of 1st & 3rd quadrants of centosymmetric square grating.
    L : Length of grating
    R : Number of points (could be detector pixels)
    """    
    x = np.linspace(-L/2,L/2,N)
    
    T1 = 0.5*(1 + np.cos((2*np.pi*x)/p1))
    T2 = 0.5*(1 + np.cos((2*np.pi*x)/p2))
    I = T1*T2
    
    plt.plot(x,T1, ':', label='T1')
    plt.plot(x,T2, ':', label='T2')
    plt.plot(x,I, label='I')
    plt.xlabel('x')
    plt.ylabel('T')
    plt.legend()
    plt.show()

def moireIntensity(p1,p2,L,R,dX):
    """
    Parameters
    ----------
    p1 : Pitch of 2nd & 4th quadrants of centosymmetric square grating.
    p2 : Pitch of 1st & 3rd quadrants of centosymmetric square grating.
    L : Length of grating
    N : Resolution of detector
    dX : Grating misalignment
    
    
    Returns
    ----------
    DX : Moire fringe displacement
    """
    
    P = moirePeriod(p1, p2)
    x = np.linspace(-P,P,int(2*P/R))
    print(x)
    dx = x[1]-x[0]
    
    I = np.cos(2*np.pi*((1/p2)-(1/p1))*x)
    Is = np.cos(2*np.pi*((1/p2)-(1/p1))*x - 2*np.pi*((1/p2)+(1/p1))*dX)
    
    pI, _I = find_peaks(I)
    pIs, _Is = find_peaks(Is)
    
    plt.plot(x,I,label='I(x)')
    plt.plot(x,Is,label='$I_{shift}(x)$')
    plt.plot(x[pI],I[pI],'x')
    plt.plot(x[pIs],Is[pIs],'x')
    plt.xlabel('x')
    plt.ylabel('I')
    plt.legend()
    plt.show()
    
    print(pI)
    print(pIs)
    DX = abs(pI[0]-pIs[0])*dx
    
    return DX
    
def test():
    
    p1 = 2e-6
    p2 = 2.5e-6
    dX = 50e-9
    e = 10e-9
    N = 2048
    Re = 11e-6
    C = 1
    L = 50e-6 #Re*N
    Lmin = minGratingSize(p1, p2)
    
    gratingTransmittance(p1, p2, L, N)
    DX = moireIntensity(p1, p2, L, Re, dX)
    
    P = moirePeriod(p1, p2)
    Z = displacementRatio(p1, p2)
    dXmax = maxMisalignment(p1, p2)
    dXmin = minMisalignment(p1, p2, N, Re, C)
    dx = misalignmentFromMoire(DX, p1, p2)
    dPmin = minPitchDiff(e)
    
    print(f'Moire pitch difference (p2 - p1):    {round_sig((p2-p1)*1e6)} um')
    print(f'Input misalignment:                  {dX*1e6} um')
    print(f"Measured misalignment from Moire:    {dx*1e6} um")
    print(f'Minimum grating size:                {Lmin*1e6} um')
    print(f"Moire fringe displacement:           {DX*1e6} um")
    print(f"Moire fringe period:                 {P*1e6} um")
    print(f"Displacement Ratio:                  {round_sig(Z)}")
    print(f"Maximum measurable misalignment:     {dXmax*1e6} um")
    print(f"Minimum measurable misalignment:     {dXmin*1e9} nm")
    print(f"Minimum pitch difference:            {dPmin*1e9} nm")
#    
def testTolerances():
    
    e = 10e-9
    N = 2048
    Re = 11e-6
    C = 10
    W = Re*N
    pMin = 2e-6
    pMax = 100e-6
    dpMin = 100e-9
    dpMax = 3.0e-6
    p1 = np.linspace(pMin,pMax,1000)
    dp = np.linspace(dpMin,dpMax,1000)
    
    P = []
    Z = []
    L = []
    dXmax = []
    dXmin = []
    for p in p1:
        _P = [moirePeriod(p, p+d)*1e3 for d in dp]
        _Z = [displacementRatio(p, p+d) for d in dp]
        _L = [minGratingSize(p,p+d)*1e3 for d in dp]
        _dxmin = [minMisalignment(p, p+d, N, Re, C)*1e9 for d in dp]
        _dxmax = [maxMisalignment(p, p+d)*1e6 for d in dp]
        
        P.append(_P)
        Z.append(_Z)
        L.append(_L)
        dXmax.append(_dxmax)
        dXmin.append(_dxmin)
    
#    plt.plot(dp,dXmin[0])
#    plt.plot(dp,dXmin[9])
#    plt.show()
#    
    no_labels = 8
    ndp = dp.shape[0]
    np1 = p1.shape[0]
    step_dp = int(ndp / (no_labels - 1))
    step_p1 = int(np1 / (no_labels - 1))
    dp_positions = np.arange(0,ndp,step_dp)
    p1_positions = np.arange(0,np1,step_p1)
    dp_labels = [round_sig(a*1e6) for a in dp[::step_dp]]
    p1_labels = [round_sig(a*1e6) for a in p1[::step_p1]]
    
    fig, ax = plt.subplots(1,3, figsize=(12,10), dpi=100)
    
    i1 = ax[0].imshow(P, norm=LogNorm(vmin=np.min(P), vmax=np.max(P)))
    i2 = ax[1].imshow(Z, norm=LogNorm(vmin=np.min(Z), vmax=np.max(Z)))
    i3 = ax[2].imshow(L, norm=LogNorm(vmin=np.min(L), vmax=np.max(L)))
    for a in ax:
        a.set_xticks(dp_positions)
        a.set_xticklabels(dp_labels)
        a.set_yticks(p1_positions)
        a.set_yticklabels(p1_labels)
        a.set_xlabel('$\Delta p$ [$\mu$m]')
        a.set_ylabel('$p_1$ [$\mu$m]')
    
    div1 = make_axes_locatable(ax[0])
    div2 = make_axes_locatable(ax[1])
    div3 = make_axes_locatable(ax[2])
    cax1 = div1.append_axes("right", size="3%", pad=0.05)
    cax2 = div2.append_axes("right", size="3%", pad=0.05)
    cax3 = div3.append_axes("right", size="3%", pad=0.05)
    plt.colorbar(i1, cax=cax1, label='Moire fringe period (P) [mm]')
    plt.colorbar(i2, cax=cax2, label='Displacement ration (Z)')
    plt.colorbar(i3, cax=cax3, label='Minimum grating size [mm]')
    
    fig.tight_layout()
    plt.show()
    
    value = 10
    tolerance = 3
#    dXmin[dXmin == value] = -1
#
    cmap = matplotlib.cm.get_cmap("viridis_r").copy()
#    cmap.set_bad("red")
#
#    cmap = matplotlib.cm.get_cmap("viridis_r").copy()  # Can be any colormap that you want after the cm
#    cmap.set_bad(color='red',alpha=1)#,value)
        
    fig, ax = plt.subplots(1,2, figsize=(12,10), dpi=100)
    
    i1 = ax[0].imshow(dXmin, cmap="viridis_r", vmin = value-tolerance, vmax = value+tolerance)#, norm=LogNorm(vmin=np.min(dXmin), vmax=np.max(dXmin)))
    i2 = ax[1].imshow(dXmax)#, norm=LogNorm(vmin=np.min(dXmax), vmax=np.max(dXmax)))
    for a in ax:
        a.set_xticks(dp_positions)
        a.set_xticklabels(dp_labels)
        a.set_yticks(p1_positions)
        a.set_yticklabels(p1_labels)
        a.set_xlabel('$\Delta p$ [$\mu$m]')
        a.set_ylabel('$p_1$ [$\mu$m]')
    
    div1 = make_axes_locatable(ax[0])
    div2 = make_axes_locatable(ax[1])
    cax1 = div1.append_axes("right", size="3%", pad=0.05)
    cax2 = div2.append_axes("right", size="3%", pad=0.05)
    plt.colorbar(i1, cax=cax1, label='Minimum measurable misalignment [nm]')
    plt.colorbar(i2, cax=cax2, label='Maximum measurable misalignment [$\mu$m]')
    
    fig.tight_layout()
    plt.show()
    
    index_min = np.argwhere(dXmin==np.min(dXmin))
#    print(f"Minimum measurable misalignment:                  {np.min(dXmin)} nm")
#    print(f"Pitch for minimum measurable misalignment:        {p1[index_min[0][0]]*1e6} um")
#    print(f"Pitch difference minimum measurable misalignment: {dp[index_min[0][1]]*1e6} um")
#    print(f"Maximum measurable misalignment for pitches:      {dXmax[index_min[0][0]][index_min[0][1]]} um")
    
    
        
    # plt.imshow(P)
    # plt.xticks(dp_positions,dp_labels)
    # plt.yticks(p1_positions,p1_labels)
    # plt.xlabel('dp [nm]')
    # plt.ylabel('p1 [nm]')
    # plt.colorbar(label='Moire fringe period (P)')
    # plt.show()
    
    # plt.imshow(Z)
    # plt.xticks(dp_positions,dp_labels)
    # plt.yticks(p1_positions,p1_labels)
    # plt.xlabel('dp [nm]')
    # plt.ylabel('p1 [nm]')
    # plt.colorbar(label='Displacement ration (Z)')
    # plt.show()
    
    # plt.imshow(dXmax)
    # plt.xticks(dp_positions,dp_labels)
    # plt.yticks(p1_positions,p1_labels)
    # plt.xlabel('dp [nm]')
    # plt.ylabel('p1 [nm]')
    # plt.colorbar(label='Maximum measurable misalignment')
    # plt.show()
    
if __name__ == '__main__':
    test()
    # testTolerances()