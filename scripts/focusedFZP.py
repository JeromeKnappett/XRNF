#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 12:49:00 2024

@author: -
"""

import numpy as np
# from usefulWavefield import intensity2power

def focusedFZP(focus_size,f0,eff,hv,Dr):
    """
    Parameters
    ----------
    focus_size : 
        size of focused beam [m].
    f0 : 
        incident flux [ph/s].
    eff : 
        zone plate effiency.
    hv : 
        photon energy [eV].
    Dr : 
        required dose [mJ/cm^2].

    Returns
    -------
    Ff = Flux at ZP focus [ph/s]
    If = Intensity at ZP focus [ph/s/cm^2]
    D = Dose at ZP focus [mJ/s/cm^2]
    S = Write speed [mm/s]
    """
        
    # beam fwhm [m]
    Bfwhm = focus_size
    
    # beam area [m^2]
    Barea = np.pi * (0.5*Bfwhm) * (0.5*Bfwhm)
    
    # ZP efficiency
    n = eff
    
    # flux at ZP focus [ph/s]
    Ff = n*f0
    
    print('Flux at ZP focus {} ph/s'.format(Ff))
    
    # intensity at ZP focus [ph/s/cm^2]
    If = Ff / (Barea * 10000)
    
    print('Intensity at ZP focus {} ph/cm^2/s'.format(If))
    
    # Dose at ZP focus [mJ/s/m^2]
    q = 1.60218e-19
    Ef = Ff * hv         # energy at focus [ev/s]
    E_mJ = Ef * q * 1000 # energy at focus [mJ/s]
    Df = E_mJ / (Barea * 10000) # dose at focus [mJ/cm^2/s]
    
    
    print('Dose = {} mJ/cm^2/s'.format(Df))
    
    # P = intensity2power(If, hv)
    
    # print('Dose = {} mJ/cm^2/s'.format(P))
    
    # Df = P
    
    # write speed [m/s]
    s = Df/Dr
    
    # write speeed [m/s]
    s_ms = s*Bfwhm
    
    S = s_ms*1e3
    
    
    print('Write speed {} mm/s'.format(S))
    
    return Ff,If,Df,S