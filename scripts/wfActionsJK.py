#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 16:03:36 2022

@author: -
"""

import numpy as np
from wpg.useful_code.wfrutils import get_mesh
from wpg.wavefront import Wavefront
import matplotlib.pyplot as plt


def getFWatValue(I,dx,dy,frac=0.5):
    """
    Calculate FW of the beam at arbitrary fraction of maximum,
    calculating number of point bigger than max/value through center of the image

    :param 
        I:  intensity
        dx,dy: resolution in x and y
    :return: fw_x, fw_y in [m]
    """
    
    x_center = I[I.shape[0]//2,:]
    fw_x = len(x_center[x_center>x_center.max()*frac])*dx

    y_center = I[:,I.shape[1]//2]
    fw_y = len(y_center[y_center>y_center.max()*frac])*dy
    
    print(f'Full width at {frac} maximum:')
    print(f'horizontal:      {fw_x} [m]')
    print(f'vertical:        {fw_y} [m]')
    return fw_x, fw_y

def getInPAboveValue(wf,value):
    """
    Take a wavefront and make all elements 0 below a certain threshold intensity value.
    """
    
    I = wf.get_intensity(polarization='total')
    P = wf.get_phase(polarization='total')
    
    I[I<value]=0
    P[I<value]=0

    return I, P
    
#    In [8]: a[a > 10] = 0
    

def test():
    
#    # TESTING getFWatValue()
#    import tifffile
#    path = '/user/home/opt/xl/xl/experiments/focusedOffAxis2/data/atFZPuf375x200/driftVol/intensity/'
#    files = ['000000.tif','000004.tif']
#    
#    I = [tifffile.imread(path + f) for f in files]
#    
#    dx,dy = 9.57713358e-7, 7.253495748e-7
#    z = 9.5
#    
#    fwx = []
#    fwy = []
#    for i in I:
#        fx,fy = getFWatValue(i,dx,dy,frac=1/10)
#        fwx.append(fx)
#        fwy.append(fy)
#    
#    dX = fwx[1]-fwx[0]
#    dY = fwy[1]-fwy[0]
#    
#    divx = 2*np.arctan((0.5*dX)/z)
#    divy = 2*np.arctan((0.5*dY)/z)
#    
#    print(f"Div x:    {divx*1e6:.5g} urad")
#    print(f"Div y:    {divy*1e6:.5g} urad")

    # TESTING getWfAboveValue()
    path = '/user/home/opt/xl/xl/experiments/focusedOffAxis2/data/atFZPuf375x200/'
    savePath = path + '/propagationPlot.png'
    
    wf = Wavefront()
    wf.load_hdf5(path + 'wf_final.hdf')
    
    
    I = wf.get_intensity(polarization='total')
    value = np.max(I)/10
    
    I, P = getInPAboveValue(wf,value)
        
if __name__ == '__main__':
    test()