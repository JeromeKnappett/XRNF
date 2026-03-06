#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 15:07:50 2023

@author: -
"""

import numpy as np
import matplotlib.pyplot as plt
import pylab
import usefulUndulator as UU
import usefulGrating as UG
import usefulWavefield_old as UW
import grating as GR
import xraydb as xrdb


pylab.rcParams['figure.figsize'] = (2.0, 2.0)

def lithoExperimentParams(wl,pU,pG,d,G,m=1,E_storage=3.01e9,grating='SiO2'):
    E = UW.WLtoE(wl)
    """ First we obtain the undulator parameters """
    # finding lorentz factor for storage ring
    gamma = UU.lorentzFactor(E_storage)
    # finding magnetic field for fundamental peak at desired wavelength
    B = UU.magfield4Wavelength(pU, gamma, wl)
    
    """ Next we obtain the mask requirements """
    # assuming at least 8 pixels per grating period
    dx = pG/8
    NG = G/dx
    Nlines = G/pG
    N = (d+G)/dx
    D = xrdb.get_material(grating)
    print(D)
    # D = ['Ni3Al',0.95]
    delta,beta,atlen = xrdb.xray_delta_beta(grating, D[1], E)
    d_outer = UG.outerD4MultiGratings(d, pG, wl,m)
    
    """ Next we obtain the propagation distance from the mask to the aerial image """
    z_min, z_max, f = UG.focalDepth(pG, d, G, wl,m)
    # Z = UG.opticalAxisIntercept(p=pG,wl=wl,offset=d,m=m) 
    Z = UG.aerialImageDistance(d=d,p=pG,m=m,wl=wl)
    T = UG.thicknessForPhaseShift(wl,ps=np.pi,delta=delta)
    
#         zEUV = opticalAxisIntercept(_p*1e-9,WL,offset=2*(_r*1e-6),m=M)
#         # zBEUV = opticalAxisIntercept(_p*1e-9,6.7e-9,offset=2*(_r*1e-6))
# #        Veuv = TMvisibility(_p*1e-9,wl=13.5e-9)
# #        Vbeuv = TMvisibility(_p*1e-9,wl=6.7e-9)
#         Z = aerialImageDistance(2*(_r*1e-6),_p*1e-9,M,WL)
    
    print("\n ------- INPUT PARAMETERS ------- ")
    print(f'Wavelength:                                                        {wl*1e9} nm')
    print(f'Undulator period:                                                  {pU*1e3} mm')
    print(f'Grating period:                                                    {pG*1e9} nm')
    print(f'Grating spacing:                                                   {d*1e6} um')
    print(f'Grating size:                                                      {G*1e6} um')
    print(f'Diffraction order:                                                 {m}')
    print(f'Storage ring energy:                                               {E_storage*1e-9} GeV')
    print(f'Grating material:                                                  {grating}')
    
    print("\n ------- UNDULATOR PARAMETERS -------")
    print(f"Magnetic field for {UW.round_sig(wl*1e9,3)} nm wavelength:                             {B} T")
    
    print("\n ------- GRATING PARAMETERS ------- ")
    print(f"Minimum resolution for grating mask:                               {dx}")
    print(f"Number of lines/spaces in grating:                                 {Nlines}")
    print(f"Linear size of grating (pixels):                                   {NG}")
    print(f"Linear size of grating mask object (pixels):                       {N}")
    print(f"Density of grating material ({grating}):                                {D[1]} g/cm^3")
    print(f"(delta, beta, attenuation length) of grating ({grating}):               {(delta, beta, atlen/100)}")
    print(f"Grating thickness for a \u03C0 phase shift:                             {T*1e6} um")
    print(f"Outer grating separation (assuming multi-grating mask):            {d_outer*1.0e9} nm ")
    
    print("\n ------- AERIAL IMAGE PARAMETERS ------- ")
    print(f"Minimum propagation distance for {m}th order interference:           {z_min} m")
    print(f"Maximum propagation distance for {m}th order interference:           {z_max} m")
    print(f"Focal depth:                                                       {f} m")
    # print(f"Optimal propagation distance:                                      {Z} m")    
    print(f"Optimal propagation distance:                                      {Z} m")
    print(f"Half pitch of aerial image:                                        {(pG/(4*m))} m")
    print(f"Minimum resolution at aerial image:                                {(pG/(4*m*7))} m ")
    
    

def test():
    # # SXR at AS
    # pU = 75.0e-3
    # E = 190.19 # peak flux/intensity for 4x3mm WBS
    # #185 # 8340 #185 #293 #6000 #293 
    # WL = UW.EtoWL(E)
    # print(WL)
    # pG = 88e-9 #50.0e-9 #40.0e-9 # 200.0e-9 #20.0e-9
    # d = 200e-6#4.018e-6 #60.0e-6 #6.0e-6   
    # G = 100e-6 #2.0e-6 #30.0e-6 #2.0e-6
    # m = 1
    # material = 'C'#'Ni'# 'Ni3Al' #'SiO2'#'Au' #'SiO2'
    
    #HERMES at SOLEIL
    E_s = 2.75e9
    pU = 40.48e-3
    E = 91.0 #185.0#200.0#185.0 
    WL = UW.EtoWL(E)
    pG = 200.0e-9#200.0e-9#88e-9
    d = 75.0e-6#200e-6
    G = 35.0e-6#100e-6
    m = 1
    material ='Ni'# 'Au'#'Ni'
    
    lithoExperimentParams(WL, pU, pG, d, G,m=m,E_storage=E_s,grating=material)
    
    
def findBestD():
    E = 90 #6000 #293 
    WL = UW.EtoWL(E)
    # print(WL)
    pG = 40.0e-9 #40.0e-9 # 200.0e-9 #20.0e-9
    d_start = 1.0e-6
    d_stop = 16.0e-6
    Dd = 0.5e-9
    n = round((d_stop - d_start) / Dd)
    print(n)
    d = np.linspace(d_start,d_stop,n)  
    G = 5.0e-6 #30.0e-6 #2.0e-6
    m = 2
    
    Dout,Din,R = [],[],[]
    for _d in d:
        _d = round(_d*1e9)*1e-9
        d_outer = UG.outerD4MultiGratings(_d, pG, WL,m)
        
        r = d_outer*1e9 - round((d_outer*1e9))
        
        if d_outer > _d + 2*G:
            Dout.append(d_outer)
            Din.append(_d)
            R.append(r)
        
    plt.plot([_d*1e9 for _d in Dout],R,'.')
    plt.xlabel('outer grating separation [nm]')
    plt.ylabel('residual separation needed for phase matching [nm]')
    plt.show()
    
    print(np.min([abs(r) for r in R]))
    ind = np.argmin([abs(r) for r in R])
    print(R[ind])
    print(f'Best outer grating separation for {Dd} m resolution mask:          {Dout[ind]*1e6} um')
    print(f'Best inner grating separation for {Dd} m resolution mask:          {Din[ind]*1e6} um')
    
    print((Dout[ind]-G) - (Din[ind] + G))
    
    # lithoExperimentParams(WL,75.0e-3, pG,Din[ind], G,m=m)
    
if __name__ == "__main__":
    test()
    # findBestD()