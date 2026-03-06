#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 16 14:33:46 2023

@author: -
"""
import numpy as np
import matplotlib.pyplot as plt
from math import log


def diffractionAngle(p, wl, theta=0, m=1):
    # Use grating equation to determine diffraction angle  
    # (m = order; wl = wavelength; p = period)
    return np.arcsin(np.sin(theta) + m*wl/p)

def wl(E):
        #return wavelength for energy E in keV
        return  12.39e-10/E

def opticalAxisIntercept(p, wl, offset, theta=0, m = 1):
    """ return distance from grating plane at which m= 1 order intercepts optical axis
    when grating is displaced by 'offset' from optical axis."""
    
    #tan theta = d / offset   CHECK THIS  46r
    #return offset*np.tan(diffractionAngle(d,l,theta,m))
    return offset / (2*np.tan(diffractionAngle(p,wl,theta,m)))

def aerialImageDistance(d,p,m,wl):
    z = (d*np.sqrt((p**2) - ((m**2)*(wl**2))))/(2*m*wl)
    return z

def TMvisibility(p,wl):
    V = 1 - 2*((wl/p)**2)
    return V

def thicknessForPhaseShift(wl,ps,delta):
    T = (wl*ps)/(np.pi*delta)
    return T

def thicknessForTransmission(wl,trans,beta):
    k = (2*np.pi) / wl
    T = - ( log(trans) / (2 * k * beta) )
    return T

def transmissionFromContamination(n,eta,contam):
    trans = (n * eta * contam) / (1 - contam) 
    return trans

def diffractionAngle(wl,p,m=1,theta_i=0):
    theta_m = np.arcsin(((m*wl)/p) + np.sin(theta_i))
    return theta_m

def lateralShift(wl,p,m,z,theta_i=0):
    theta = np.arcsin((m*wl)/p + np.sin(theta_i))
    dx = z*np.tan(theta)
    # dx = (z*m*wl) / (np.sqrt((p**2) - ((m**2)*(wl**2))))
    return dx

def propDistFromLatShift(dx,wl,p,m):
    z = (dx*(np.sqrt((p**2) - ((m**2)*(wl**2)))))/(m*wl)
    return z

def outerD4MultiGratings(d,p,wl,m=1):
    alpha = np.sqrt(((4*(p**2)) - ((m**2)*(wl**2))) / ((p**2) - ((m**2)*(wl**2))))
    d_outer = d*alpha
    # print('alpha', alpha)
    # print(d_outer / d)
    return d_outer

def ZRangeforTalbot(p,WL,dWL,G,verbose=True):
    """
    Parameters
    ----------
    p : float
        pitch of grating.
    WL : float
        wavelength of incident radiation
    dWL : float (assuming >> 1/2)
        wavelength bandwidth of incident radiation.
    G : float
        grating side length
    Returns
    -------
    Zt : Talbot distance (grating self-image is produced at integers of this distance)
    Zm : minimum distance for stationary talbot interference.
    ZM : maximum distance for stationary talbot interferemce.
    """
    Zt = (2*(p**2)) / WL
    Zm = (2*(p**2)) / dWL
    ZM = G * (p / WL)
    
    if verbose:
        print(f"\n Talbot Distance:                           {Zt} m")
        print(f"Z range for stationary talbot interference:   {Zm} -- {ZM} m")
    
    return Zt, Zm, ZM

def detectorRange(z,wl,p,d0):
    """
    Parameters
    ----------
    z : float
        total propagation distance from mask to detector.
    wl : float
        incident wavelength.
    p : float
        grating pitch.
    d0 : float
        photon block size.
    Returns
    -------
    R : Range needed on detector to see 1st order beams.

    """
    R = 2*((z * (wl / (np.sqrt((p**2) - (wl**2))))) - (d0/2))
    return R

def firstOrderOverlap(wl,p,D,G):
    """
    Parameters
    ----------
    wl : TYPE
        wavelength.
    p : TYPE
        pitch.
    D : TYPE
        separation.
    G : TYPE
        size.

    Returns
    -------
    None.

    """
    
    wl3 = wl/3.0
    z = (D*(np.sqrt((p**2) - ((wl**2))))) / (2*wl)              # plane at which 1st order beams interfere (1st harmonic)
         
    dX_1 = lateralShift(wl3, p, m=1, z=z)                       # lateral shift of 1st order diffracted beams (3rd harmonic)
    dX_3 = lateralShift(wl3, p, m=3, z=z)                       # lateral shift of 3rd order diffracted beams (3rd harmonic)
    
    if (dX_1 + G) > dX_3:
        print("Overlap occuring! :(")
    else:
        print("No overlap occuring! :)")
    
    overlap = (dX_1 + G) - dX_3
    
    
    # t1 = np.arcsin(wl/p)                                       # diffraction angle of 1st order beam
    # dX = z*np.tan(t1)                                          # furthest lateral distance 1st order beams move
    # dX_a = (D/2 - G)                                           # allowable distance for 1st orders to move without contamination of 3rd order
    
    if overlap > 0:
        print(f"Overlap of 1st and 3rd order beams:            {overlap*1e6} [um]")
    else:
        print(f"1st and 3rd order beams separated by:          {-1e6*overlap} [um]")
    
    
    return overlap

def minGratingSep(p,wl):
    """
    Parameters
    ----------
    p : float
        Grating pitch [m].
    wl : float
        fundamental wavelength [m].

    Returns
    -------
    d : Minimum grating separation to avoid overlap of 1st and 3rd order diffracted beams from the 3rd undulator harmonic.
        [given in multiples of grating size]

    """
    # a = np.sqrt(((p**2)-(wl**2)) / (9*(p**2)-(wl**2)))
    # b = ((((np.sqrt(9*(p**4) + (wl**4) - 10*(p**2)*(wl**2))) / (p**2)) + ((wl**2) / (p**2)) + 9) / 4)
    # print(f"beta = {b}")
    # d1 = -2/(a-1)
    # d = ((((np.sqrt(9*(p**4) + (wl**4) - 10*(p**2)*(wl**2))) / (p**2)) + ((wl**2) / (p**2)) + 9) / 4)
    d = ((((np.sqrt(4*(p**4) + (wl**4) - 5*(p**2)*(wl**2))) / (p**2)) + ((wl**2) / (p**2)) + 4) / 3)
    # print(f"d1 = {d1}")
    print(f"Minimum grating separation = {d} x Grating Size")
    return d

def maxGratingSize(wl,p,n=2):
    a = wl/p    
    
    b = (n**2 - a + np.sqrt((1 - a)*(n**2 - a))) / (n**2 - 1)
    
    # d/G = 2*b
    
    print(2 * b)

def focalDepth(p,d,G,wl,m=1):
    d_min = d-G
    d_max = d+G
    z_min = aerialImageDistance(d_min, p, m, wl)
    z_max = aerialImageDistance(d_max, p, m, wl)    
    # z_min = 0.5 * (d-G) * ((np.sqrt((p**2) - ((m**2)*(wl**2)))) / (2*m*wl))
    # z_max = 0.5 * (d+G) * ((np.sqrt((p**2) - ((m**2)*(wl**2)))) / (2*m*wl))
    
    print(f'Min z: {z_min} m')
    print(f'Max z: {z_max} m')
    
    f = z_max-z_min
    
    return z_min,z_max,f

def minGratingSize(f,p,wl):
    """
    ----------
    f : float
        Minimum focal depth needed (thickness of photoresist).
    p : float
        Grating pitch.
    wl : float
        Incident wavelength.

    Returns
    -------
    Gmin: Minimum grating size.
    """
    
    Gmin = (2*f*wl) / (np.sqrt(p**2 - wl**2))
    return Gmin

def minGratingSep2(G,wl,p):
    a = wl/p
    d = 2 * G * ((4*(p**2) - wl + (np.sqrt(((4*(p**2) - wl) * ((p**2) - wl)) / (3*(p**2))))))
    # d = (2/3)*(4 - a**2 - np.sqrt((1 - a**2) * (4 - a**2))) # in units of gratingg
    
    return d

def reqDoseOnMask(DE,T,n,DoW=30):
    """
    Parameters
    ----------
    DE : float between 0 and 1
        Diffraction efficiency of grating used.
    T : float between 0 and 1
        Transmission of substrate.
    n : int
        Number of gratings in IL mask.
    DoW : float, optional
        Required dose-on-wafer in mJ/cm^2. The default is 30.

    Returns
    -------
    DoM : required dose-on-mask in mJ/cm^2.
    """
    
    DoM = DoW / (n*DE * T)
    return DoM
    
def getMaterialProperties(name,E,D):
    import xraydb
    
    delta, beta, atlen = xraydb.xray_delta_beta(name, density=D, energy=E)

def transmission(wl,T,beta):
    k = (2*np.pi) / wl
    trans = np.exp((-2*k * beta * T)) # np.exp(((-k) / (beta * T))) # changed to -2k from -1k by JK - 29/10/24
    return trans

def test():
    wl = 6.7e-9
    p = [100e-9/a for a in range(1,16)]
    D = 100e-6
    G = 100e-6
    
    # D_a = 300e-6
    
    # firstOrderOverlap(wl, p, D, G)
    # d1 = minGratingSep(p, wl)
    # firstOrderOverlap(wl, p, d1*G, G)
    
    
    # d = range(-1,2)
    # DO = []
    # for i in d:
    #     D_a = firstOrderOverlap(wl, p, D=i*10e-6, G=(i*10e-6)/3)
    #     DO.append(D_a)
    # plt.plot(d,DO,'.:')#,color='black')    
    # plt.xlabel('separation [m]')
    # plt.ylabel('overlap [m]')
    # plt.show()
    
    # f = focalDepth(p, D, G, wl)
    
    # print(f)
    
    # Gmin = minGratingSize(f=1000e-9, p=100.0e-9, wl=wl)
    
    # print(Gmin)
    # maxGratingSize(wl, p)
    
    D = []
    for P in p:
        d2 = minGratingSep2(G, wl, P)
    
    # print("Min grating sep #1: ", d1)
        print(" ")
        print("p (nm) = ", P*1e9)
        print("Min grating sep #2 (um): ", d2*1e6)
        D.append(d2)
    
    plt.plot([wl/P for P in p],D,':x')
    plt.show()
    
def testDetectorRange():
    from grating import wl
    z = 3.88#0.1
    E = 8340.0
    WL = wl(E*1e-3)
    p = 90.0e-9
    d0 = 0.0 #60.0e-6
    px = 75.0e-6
    
    R = detectorRange(z, WL, p, d0)
    print('Required detector range: ', R, ' m')
    
    dx = lateralShift(WL, p, 1, z)
    
    print('Distance from 0th to 1st order beams at detector: ', dx, ' m')
    print('Distance in detector pixels: ', dx/px, ' pixels')
    
    
def lateralShift(wl,p,m,z,theta_i=0):
    theta = np.arcsin((m*wl)/p + np.sin(theta_i))
    dx = z*np.tan(theta)
    # dx = (z*m*wl) / (np.sqrt((p**2) - ((m**2)*(wl**2))))
    return dx

    
    
    
def testDoseOnMask():
    DE = 0.01
    n = 4
    T = 0.82
    
    DoM = reqDoseOnMask(DE, T, n, DoW=30)
    
    print(DoM)
    
if __name__ == '__main__':
    # test()
    testDetectorRange()
    # testDoseOnMask()
    
    
    
