#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 18 12:31:23 2022

@author: jerome
"""
import numpy as np

# %%
def getComplex(w, polarization=None, verbose=False):
    """ 
    Give the complex representation of a wavefield
    Parameters
    ----------
    w: scalar wavefield
    polarization: polarization component of wavefield to extract. Can be "total", "horizontal" or "vertical".
    returns:
        cwf: complex wavefield
    """
    
    re = w.get_real_part(polarization = polarization)      # get real part of wavefield
    im = w.get_imag_part(polarization = polarization)      # get imaginary part of wavefield
    
    
    cwf = re + im*1j
    
    if verbose:
        print("Shape of real part of wavefield: {}".format(np.shape(re)))
        print("Shape of imaginary part of wavefield: {}".format(np.shape(im)))
        print("Shape of complex wavefield: {}".format(np.shape(cwf)))
        print("Polarization of complex wavefield: {}".format(polarization))
    else:
        pass
    
    return cwf