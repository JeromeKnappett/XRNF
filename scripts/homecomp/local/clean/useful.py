#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 16 09:39:27 2022

@author: jerome
"""

import numpy as np
from math import log10, floor, sqrt
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# %%
def round_sig(x, sig=2):
    if x != 0:
        return round(x, sig-int(floor(log10(abs(x))))-1)
    else:
            return x
        
# %%
def getLineProfile(a,axis=0, mid=None, show=False):
    nx, ny = np.shape(a)[1], np.shape(a)[0]
    if mid == None:
        midX, midY = int(nx/2), int(ny/2)
    else:
        midX, midY = int(mid[1]), int(mid[0])    
    # print(midX)
    
    if axis == 0:
        p = a[:,midX]
        title = 'vertical profile'
    elif axis == 1:
        p = a[midY,:]
        title = 'horizontal profile'
    
    if show:
        plt.plot(p)
        plt.title(title)
        plt.show()
    
    return p
# %%
def sampleField(A,Fx,Fy,limit = 75, verbose=False, show=False):
    """
    Parameters
    ----------
    A : 2D array to be sampled.
    Fx : Fraction of array to be sampled in horizontal.
    Fy : Fraction of array to be sampled in vertical.
    Limit: Maximum number of pixels allowed in any dimension
    Returns
    -------
    B: 2D array sampled from centre of A.
    """
    if verbose:
        print("-----Sampling middle part of array-----")
    else:
        pass
    
    Ax = np.shape(A)[1]
    Ay = np.shape(A)[0]
    Sx = Fx*(Ax-1)
    Sy = Fy*(Ay-1)
    
    if Sx > limit or Sy > limit:
        print("Error: Sampled area of wavefront is too large. Change Fx/Fy to a smaller value")
        import sys
        sys.exit()
    
    try:
        _x1 = int(np.max(np.shape(A[:,0,0]))) # These are in _pixel_ coordinates!!
        _y1 = int(np.max(np.shape(A[0,:,0])))
    except IndexError:
        _x1 = int(np.max(np.shape(A[:,0]))) # These are in _pixel_ coordinates!!
        _y1 = int(np.max(np.shape(A[0,:])))
    
    midX = int((Ax-1)/2)
    midY = int((Ay-1)/2)

    ROI = ((int(midX-(Sx/2)),int(midY-(Sy/2))),
           (int(midX+(Sx/2)),int(midY+(Sy/2))))
    
    x0,y0 = ROI[0][0], ROI[0][1]
    x1,y1 = ROI[1][0], ROI[1][1]
    
    lX = ROI[1][0]-ROI[0][0]
    lY = ROI[1][1]-ROI[0][1]
    
    if verbose:
        print("Original size of array [pixels]: {}".format((Ax,Ay)))
        print("Sampled area size (pixels): {}".format([Sx,Sy]))
        print("Nx (pixels): {}".format(_x1))
        print("Ny (pixels): {}".format(_y1))
        print("mid x: {}".format(midX))
        print("mid y: {}".format(midY))
        print("Region of interest (pixels): {}".format(ROI))
        print("Starting point for sample area (x,y): {}".format((x0,y0)))
        print("Size of sample area (x,y): {}".format((lX,lY)))
    else:
        pass
    
    
    if show:
        I = abs(A.conjugate()*A)
        figure, ax = plt.subplots(1) 
        rect = patches.Rectangle((x0,y0),lX,lY, edgecolor='r', facecolor="none")
        
        # Xh, Xv = [midX,midX], [_x1,0]
        # Yh, Yv = [_y1,0], [midY,midY]
        plt.imshow(I, aspect='auto')
        # plt.plot(Xh,Yh,':')
        # plt.plot(Xv,Yv,':')
        ax.add_patch(rect)
        plt.title("Original Wavefield with Sampled Area")
        plt.show()
        plt.clf()
        plt.close()
    else:
        pass
    
    B = A[y0:y1,x0:x1]
    
    return B

# %%
def fromPickle(path):
    import pickle
    
    with open(path, 'rb') as a:
        w = pickle.load(a)
        
    return w

# %%
def normVec(x,y,z):
    N = np.sqrt((x**2)+(y**2)+(z**2))
    nx, ny, nz = x/N, y/N, z/N
    
    return nx,ny,nz

def nFromAng(theta):
    y=0
    z=1
    x=z*np.tan(theta)
    
    N = np.sqrt((x**2)+(y**2)+(z**2))
    nx, ny, nz = x/N, y/N, z/N
    
    return nx,ny,nz
    
def getDeltaBeta(material,energy,density=None):
    """
    material: chemical formula (if pure element, density can be none)
    energy: x-ray energy in eV
    density: material density in g/cm^3    
    """
    import xraydb
    if density == None:
        density = xraydb.atomic_density(material)
    delta, beta, atlen = xraydb.xray_delta_beta(material,density,energy)
    return delta, beta, atlen*1e-2

def thicknessForPhaseShift(wl,ps,delta):
    T = (wl*ps)/(delta*np.pi)
    return T
    
# %%
def test():
#    path = '/home/jerome/Downloads/FZP.pkl'
#    
#    fzp = fromPickle(path)
#    
#    plt.imshow(fzp)#[100:200,200:250])
#    plt.show()
    x = 100e-6
    y = 0
    z = 10.888e-3
    theta = np.arctan(x/z)
    
    nx,ny,nz = normVec(x,y,z)
    print(nx,ny,nz)
    nx,ny,nz = nFromAng(theta)
    print(nx,ny,nz)

if __name__ == '__main__':
#    test()
    m = 'Ni' #'Ni3Al' #'Ni'
    density = None #7.44 #0.95 #None #8.902
    e = 186 #91.84 
    wl = 6.7e-9 #13.5e-9
    ps = 2*np.pi*0.01
    d,b,a = getDeltaBeta(m,energy=e,density=density)
    print('delta = ',d,', beta = ',b,', atten len = ',a)
    t = thicknessForPhaseShift(wl=wl,ps=ps,delta=d)
    print('Thickness for 1% phase shift: ',t*1e9, ' nm')