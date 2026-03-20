#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  2 10:58:17 2022

@author: jerome
"""
import numpy as np

def emittanceSE(lam):
    """
    Parameters
    ----------
    lam : int/float
        Wavelength of radiation in [m].
    Returns
    -------
    e : diffraction limited radiation emittance from a single electron in [m rad].
    """
    return lam/(2*np.pi)

def eSizeAndDiv(lam,L):
    """
    Parameters
    ----------
    lam : int/float
        Wavelength of radiation in [m].
    L : int/float
        Length of undulator in [m].
    Returns
    -------
    s : Undulator radiation source size from single electron in [m].
    _s : Undulator radiation source divergence from single electron in [rad].
    """
    s = np.sqrt((lam*L)/(2*(np.pi**2)))
    _s = np.sqrt((lam)/(2*L))
    return s, _s

def photonSizeAndDiv(beta,e):
    """
    Parameters
    ----------
    beta : int/float
        Betatron function in [m].
    e : int/float
        Electron beam emittance in [m rad].
    Returns
    -------
    s : Photon beam size in [m].
    _s : Photon beam divergence in [rad].
    """
    

def test():
    ex = 10e-9
    ey = 0.009e-9
    Bx = 9
    By = 3
    L = 1.875
    
    

