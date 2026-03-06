#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 11 13:17:00 2022

@author: jerome
"""
import numpy as np


def effRes(px, sigma, f, z1, z2, delta=1):
    """From A.J Morgan et al (2020).
    px: detector pixel size
    sigma: source size
    f: focal length of illuminating optic
    z1: focus-to-sample distance
    z2: sample-to-detector distance
    delta: resolution blur due to partial coherence
    """
    eR = delta * (px + (sigma * z2 * f) / z1)
    return eR


def refRes(px, sigma, f, z1, z2, delta=1):
    """From A.J Morgan et al (2020).
    px: detector pixel size
    sigma: source size
    f: focal length of illuminating optic
    z1: focus-to-sample distance
    z2: sample-to-detector distance
    delta: resolution blur due to partial coherence
    """
    M = (z1 + z2) / z2
    eR = effRes(px, sigma, f, z1, z2, delta)
    rR = eR / M
    return rR


def angResSample(px, sigma, f, z1, z2, delta=1):
    """From A.J Morgan et al (2020).
    px: detector pixel size
    sigma: source size
    f: focal length of illuminating optic
    z1: focus-to-sample distance
    z2: sample-to-detector distance
    delta: resolution blur due to partial coherence
    """
    eR = effRes(px, sigma, f, z1, z2, delta)
    aRs = np.arctan(eR / z2)
    return aRs


def angResDetector(px, sigma, f, z1, z2, delta=1):
    """From A.J Morgan et al (2020).
    px: detector pixel size
    sigma: source size
    f: focal length of illuminating optic
    z1: focus-to-sample distance
    z2: sample-to-detector distance
    delta: resolution blur due to partial coherence
    """
    rR = refRes(px, sigma, f, z1, z2, delta)
    aRd = np.arctan(rR / z2)
    return aRd


def phaseRes(px, sigma, f, z1, z2, lam, delta=1):
    """From A.J Morgan et al (2020).
    px: detector pixel size
    sigma: source size
    f: focal length of illuminating optic
    z1: focus-to-sample distance
    z2: sample-to-detector distance
    lam: incident wavelength
    delta: resolution blur due to partial coherence
    """
    M = (z1 + z2) / z2
    eR = effRes(px, sigma, f, z1, z2, delta)
    pR = ((2 * np.pi) / lam) * (eR / M)
    return pR


def bestDist(z, px, f, sigma):
    """From A.J Morgan et al (2020).
    z: focus-to-detector distance
    px: detector pixel size
    f: focal length of illuminating optic
    sigma: source size
    """
    Zb = z / (1 + np.sqrt(px / (f * sigma)))
    return Zb


def bestAngResSample(z, px, f, sigma):
    """From A.J Morgan et al (2020).
    z: focus-to-detector distance
    px: detector pixel size
    f: focal length of illuminating optic
    sigma: source size
    """
    aRs = (px / z) * ((1 + np.sqrt((f * sigma) / px)) ** 2)
    return aRs


def speckleWidth(lam, R, Lsd):
    """
    From L Fan, D Paterson, I McNulty, MMJ Treacy, and JM Gibson. Fluctuation
    x-ray microscopy: a novel approach for the structural study of disordered
    materials.
    ----------
    lam : Wavelength
    R : Probe size at sample.
    Lsd : Distance from sample to detector.

    Returns
    -------
    w : speckle width.
    """
    w = (lam * Lsd) / (2 * R)
    return w


def probeSizeForSpeckle(lam, Lsd, w):
    R = (lam * Lsd) / (2 * w)
    return R


def test():
    px = 75.0e-6       # pixel size
    sigma = 50e-6   # source size
    f = 1.0         # focal length of optic
    z1 = 0.30       # focus-to-sample distance
    z2 = 1.0        # sample-to-detector distance
    z = z1 + z2     # focus-to-detector distance 
    lam = 2.25e-10  # wavelength
    delta = 1.0       # resolution blur due to partial coherence

    eR = effRes(px, sigma, f, z1, z2, delta)
    rR = refRes(px, sigma, f, z1, z2, delta)
    aRs = angResSample(px, sigma, f, z1, z2, delta)
    aRd = angResDetector(px, sigma, f, z1, z2, delta)
    pR = phaseRes(px, sigma, f, z1, z2, delta)
    Zb = bestDist(z, px, f, sigma)
    aRsb = bestAngResSample(z, px, f, sigma)

    eRb = effRes(px, sigma, f, Zb, z - Zb, delta)
    rRb = refRes(px, sigma, f, Zb, z - Zb, delta)
    aRdb = angResDetector(px, sigma, f, Zb, z - Zb, delta)
    pRb = phaseRes(px, sigma, f, Zb, z - Zb, delta)

    wMinZ = speckleWidth(lam, 2e-6, 30e-3)
    wMaxZ = speckleWidth(lam, 2e-6, 3)

    PminZ = probeSizeForSpeckle(lam, 30e-3, px / 4)
    PmaxZ = probeSizeForSpeckle(lam, 3, px / 4)

    wMinZminP = speckleWidth(lam, PminZ, 30e-3)
    wMaxZminP = speckleWidth(lam, PminZ, 3)

    print("Current parameters ----------------------------------")
    print("-----------------------------------------------------")
    print(f"Effective Resolution:                     {eR*1e6:.3g} um")
    print(f"Demagnified Resolution:                   {rR*1e6:.3g} um")
    print(f"Angular Resolution (Sample):              {aRs*1e3:.3g} mrad")
    print(f"Angular Resolution (Detector):            {aRd*1e3:.3g} mrad")
    print(f"Phase Resolution:                         {pR*1e3:.3g} mrad")
    print(" ")
    print(f"Optimised parameters for z = {z} m  ---------------")
    print("-----------------------------------------------------")
    print(f"Best focus-to-sample distance:            {Zb:.3g} m")
    print(f"Best sample-to-detector distance:         {z-Zb:.3g} m")
    print(" ")
    print(f"Best Effective Resolution:                {eRb*1e6:.3g} um")
    print(f"Best Demagnified Resolution:              {rRb*1e6:.3g} um")
    print(f"Best Angular Resolution (Sample):         {aRsb*1e3:.3g} mrad")
    print(f"Best Angular Resolution (Detector):       {aRdb*1e3:.3g} mrad")
    print(f"Best Phase Resolution:                    {pRb*1e3:.3g} mrad")

    print(" ")
    print("Speckle Width calculations ------------------------------------")
    print(f"Speckle Width for min z (30 mm), (R=2 microns): {wMinZ*1e6:.3g} um")
    print(f"Speckle Width for max z (1 m), (R=2 microns):   {wMaxZ*1e6:.3g} um")
    print(" ")
    print(f"Max probe size for visible speckle, min z (30 mm):    {PminZ*1e6:.3g} um")
    print(f"Max probe size for visible speckle, max z (1 m):      {PmaxZ*1e6:.3g} um")
    print(" ")
    print(f"Speckle width for minimum probe size, min z (30 mm):  {wMinZminP*1e6:.3g} um")
    print(f"Speckle width for minimum probe size, max z (1 m):    {wMaxZminP*1e6:.3g} um")


if __name__ == "__main__":
    test()
