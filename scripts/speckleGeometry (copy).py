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
    px = 11e-6
    sigma = 100e-6
    f = 100e-6
    z1 = 1e-3
    z2 = 0.5
    z = z1 + z2
    lam = 6.7e-9
    delta = 1

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

    wMinZ = speckleWidth(lam, 500e-6, 30e-3)
    wMaxZ = speckleWidth(lam, 500e-6, 1)

    PminZ = probeSizeForSpeckle(lam, 30e-3, px / 4)
    PmaxZ = probeSizeForSpeckle(lam, 1, px / 4)

    wMinZminP = speckleWidth(lam, PminZ, 30e-3)
    wMaxZminP = speckleWidth(lam, PminZ, 1)

    print("Current parameters ----------------------------------")
    print("-----------------------------------------------------")
    print(f"Effective Resolution:                     {eR:.3g} m")
    print(f"Demagnified Resolution:                   {rR:.3g} m")
    print(f"Angular Resolution (Sample):              {aRs:.3g} rad")
    print(f"Angular Resolution (Detector):            {aRd:.3g} rad")
    print(f"Phase Resolution:                         {pR:.3g} rad")
    print(" ")
    print(f"Optimised parameters for z = {z} m  ---------------")
    print("-----------------------------------------------------")
    print(f"Best focus-to-sample distance:            {Zb:.3g} m")
    print(f"Best sample-to-detector distance:         {z-Zb:.3g} m")
    print(" ")
    print(f"Best Effective Resolution:                {eR:.3g} m")
    print(f"Best Demagnified Resolution:              {rR:.3g} m")
    print(f"Best Angular Resolution (Sample):         {aRsb:.3g} rad")
    print(f"Best Angular Resolution (Detector):       {aRd:.3g} rad")
    print(f"Best Phase Resolution:                    {pR:.3g} rad")

    print(" ")
    print("Speckle Width calculations ------------------------------------")
    print(f"Speckle Width for min z (30 mm), (R=500 microns): {wMinZ:.3g} m")
    print(f"Speckle Width for max z (1 m), (R=500 microns):   {wMaxZ:.3g} m")
    print(" ")
    print(f"Max probe size for visible speckle, min z (30 mm):    {PminZ:.3g} m")
    print(f"Max probe size for visible speckle, max z (1 m):      {PmaxZ:.3g} m")
    print(" ")
    print(f"Speckle width for minimum probe size, min z (30 mm):  {wMinZminP:.3g} m")
    print(f"Speckle width for minimum probe size, max z (1 m):    {wMaxZminP:.3g} m")


if __name__ == "__main__":
    test()
