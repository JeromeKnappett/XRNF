#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 18 12:31:23 2022

@author: jerome
"""
import numpy as np
from wpg.srwlib import SRWLStokes, SRWLWfr
import matplotlib.pyplot as plt
import pickle
from wpg.wavefront import Wavefront

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

def wavefieldFromE(Ex,Ey,res,E):
    """
    Ex, Ey: x/y components of complex electric field array
    res: x/y resolution
    E: Energy
    -----------
    returns: SRWLWfr object
    """
    
    # Defining parameters
    nx,ny = int(np.shape(E)[1]/2), int(np.shape(E)[0]/2)
    
    wf = SRWLWfr() #Initial Electric Field Wavefront    
    wf.allocate(1, nx, ny) #Numbers of points vs Photon Energy (1), Horizontal and Vertical Positions (dummy)
    wf.mesh.zStart = 0 #Longitudinal Position [m] at which Electric Field has to be calculated, i.e. the position of the first optical element
    wf.mesh.eStart = E #Initial Photon Energy [eV]
    wf.mesh.eFin = E #Final Photon Energy [eV]
    wf.mesh.xStart = (-nx/2)*res[0] #Initial Horizontal Position [m]
    wf.mesh.xFin = (nx/2)*res[0] #Final Horizontal Position [m]
    wf.mesh.yStart = (-ny/2)*res[1] #Initial Vertical Position [m]
    wf.mesh.yFin = (ny/2)*res[1] #Final Vertical Position [m]
    wf.arEx = Ex
    wf.arEy = Ey
    wf.mesh.ne = 1
    
    return wf

def getIPfromComplex(Ex,Ey,res,E):
    
    wf = wavefieldFromE(Ex,Ey,res,E)
    w = Wavefront(srwl_wavefront=wf)
    
    I = w.get_intensity(polarization='total')
    P = w.get_phase(polarization='total')
    
    return I,P
    

def colorize(z):
    from colorsys import hls_to_rgb
    n,m = z.shape
    c = np.zeros((n,m,3))
    c[np.isinf(z)] = (1.0, 1.0, 1.0)
    c[np.isnan(z)] = (0.5, 0.5, 0.5)

    idx = ~(np.isinf(z) + np.isnan(z))
    A = (np.angle(z[idx]) + np.pi) / (2*np.pi)
    A = (A + 0.5) % 1.0
    B = 1.0 - 1.0/(1.0+abs(z[idx])**0.3)
    c[idx] = [hls_to_rgb(a, b, 0.8) for a,b in zip(A,B)]
    return c
    
def photonEnergy(wl):
    
    c = 299792458
    h = 6.626e-34
    f = c/wl
    
    E = h*f   #in Joules
    return E

def test():
    
    # E = 184.76  #photon energy
    # picks = [pickle.load(open(f, 'rb')) for f in files]
    # N = [(int(p[2]),int(p[3])) for p in picks]
    # nTot = [n[0]*n[1] for n in N]
    # res = [(p[4],p[5]) for p in picks]
    # Ex = [p[0] for p in picks]
    # Ey = [p[1] for p in picks]
    
    E_ph = photonEnergy(6.7e-9)
    E_mm = 1.4e12*E_ph
    E_cm = E_mm*100
    print(E_cm)
    