#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  1 16:48:56 2022

@author: jerome
"""

#import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

from diffractio import degrees, mm, plt, sp, um, np
from diffractio.scalar_fields_XY import Scalar_field_XY
from diffractio.utils_drawing import draw_several_fields
from diffractio.scalar_masks_XY import Scalar_mask_XY
from diffractio.scalar_sources_XY import Scalar_source_XY

from matplotlib import rcParams


def apertureDiffraction(nX,nY,X,Y,Ax,Ay,wl,Z, display=True,verbose=True):
    """

    Parameters
    ----------
    nX : int
        Number of pixels in horizontal direction in final array.
    nY : int
        Number of pixels in vertical direction in final array.
    g : int/float
        aperture size in microns
    wl : int/float
        wavelength in nm.
    Z : int/float
        propagation distance.
    display : TYPE, optional
        DESCRIPTION. The default is True.

    Returns
    -------
    u3 : TYPE
        DESCRIPTION.
    image : TYPE
        DESCRIPTION.

    """
    rcParams['figure.figsize']=(7,5)
    rcParams['figure.dpi']=125
    
    lengthX = X
    lengthY = Y
    x0 = np.linspace(-lengthX / 2, lengthX / 2, nX)
    y0 = np.linspace(-lengthY / 2, lengthY / 2, nY)
    wavelength = wl
    
    u1 = Scalar_source_XY(x=x0, y=y0, wavelength=wavelength)
    u1.plane_wave(A=1, theta=0 * degrees, phi=0 * degrees)
    # u1.laguerre_beam(p=2, l=1, r0=(0 * um, 0 * um), w0=7 * um, z=0.01 * um)
    
    t1 = Scalar_mask_XY(x=x0, y=y0, wavelength=wavelength)
    t1.square(r0=(0, 0), size=(Ax, Ay), angle=0 * degrees)
    
    u2 = u1 * t1
    
    u3 = u2.RS(z=Z, new_field=True,verbose=verbose)
    
    # c = u3[0]
    exitI = np.abs(u2.u)**2
    image = np.abs(u3.u)**2
    
    if display:
        fig, ax = plt.subplots(1,2)
        ax[0].imshow(exitI,aspect='auto')
        # ax[0].set_title("aperture exit plane")
        ax[1].imshow(image, aspect='auto')
        # ax[1].set_title()
        plt.show()
    else:
        pass
    
    return u3

def doubleApertureDiffraction(nX,nY,X,Y,sep,Ax,Ay,wl,Z,orient='hor',display=True,verbose=True):

    rcParams['figure.figsize']=(7,5)
    rcParams['figure.dpi']=125
    
    lengthX = X
    lengthY = Y
    x0 = np.linspace(-lengthX / 2, lengthX / 2, nX)
    y0 = np.linspace(-lengthY / 2, lengthY / 2, nY)
    wavelength = wl
    
    u1 = Scalar_source_XY(x=x0, y=y0, wavelength=wavelength)
    u1.plane_wave(A=1, theta=0 * degrees, phi=0 * degrees)
    # u1.laguerre_beam(p=2, l=1, r0=(0 * um, 0 * um), w0=7 * um, z=0.01 * um)
    
    ap1 = Scalar_mask_XY(x=x0, y=y0, wavelength=wavelength)
    ap2 = Scalar_mask_XY(x=x0, y=y0, wavelength=wavelength)
    
    if orient == 'hor':
        ap1.square(r0=((0 + sep)/2,0), size=(Ax, Ay), angle=0 * degrees)
        ap2.square(r0=((0 - sep)/2,0), size=(Ax, Ay), angle=0 * degrees)
    elif orient == 'ver':
        ap1.square(r0=(0,(0 + sep)/2), size=(Ax, Ay), angle=0 * degrees)
        ap2.square(r0=(0,(0 - sep)/2), size=(Ax, Ay), angle=0 * degrees)
    else:
        pass
    
    doubleAp = ap1 + ap2

    u2 = u1 * doubleAp
    
    u3 = u2.RS(z=Z, new_field=True, verbose=verbose)
    
    # c = u3[0]
    exitI = np.abs(u2.u)**2
    image = np.abs(u3.u)**2

    if display:
        fig, ax = plt.subplots(1,2)
        ax[0].imshow(exitI, aspect='auto')
        # ax[0].set_title("aperture exit plane")
        ax[1].imshow(image, aspect='auto')
        # ax[1].set_title()
        plt.show()

    # t1.square(r0=(0, 0), size=(Ax, Ay), angle=0 * degrees)
    return u3

def sumTwoE(E_1,P_1,E_2,P_2,A):
    
    E_0 = np.sqrt(E_1**2 + E_2**2 + (2*A*E_1*E_2*np.cos(P_1 - P_2)))
    
    P_0 = np.arctan((E_1*np.sin(P_1) + E_2*np.sin(P_2))/(E_1*np.cos(P_1) + E_2*np.cos(P_2)))
    
    E = E_0*np.cos(P_0)
    
    return E
    

def testDiffraction():
    Nx = 2000
    Ny = 500
    x = 50e-6
    y = 20e-6
    Ax = 10e-6
    Ay = 10e-6
    w = 6.7e-9
    Z = 0.00020443924880224158
    s = 27.5e-6
    
    resX, resY = x/Nx, y/Ny
    
    print("res (x,y): ", (resX,resY))
    
    apD = apertureDiffraction(Nx,Ny, x, y, Ax, Ay, w, Z)
    blockD = doubleApertureDiffraction(Nx,Ny, x, y, s, Ax, Ay,w,Z,orient='hor')
    
def testAerialImageEnvelope():
    import interferenceGratingModelsJK
    
    Nx = 10000
    Ny = 400
    x = 50e-6
    y = 20e-6
    Ax = 10e-6
    Ay = 10e-6
    w = 6.7e-9
    Z = 0.00020443924880224158
    s = 27.5e-6
    
    resX, resY = x/Nx, y/Ny
    
    print("res (x,y): ", (resX,resY))
    
    apD = apertureDiffraction(Nx,Ny, x, y, Ax, Ay, w, Z, display=False)
    blockD = doubleApertureDiffraction(Nx,Ny, x, y, s, Ax, Ay,w,Z,display=False,orient='hor')
    
    samX, samY = 10e-6, 0.1e-6
    samNx, samNy = samX/resX, samY/resY
    
    print("Pixels needed for sampled area (x,y): ", (samNx, samNy))
    
    # print(apD.u)

    eAP = apD.u[int((Ny-samNy)/2):int((Ny+samNy)/2),int((Nx-samNx)/2):int((Nx+samNx)/2)].mean(0)
    eBLOCK = blockD.u[int((Ny-samNy)/2):int((Ny+samNy)/2),int((Nx-samNx)/2):int((Nx+samNx)/2)].mean(0)
        
    xP = np.linspace(int(-samNx*resX), int(samNx*resX),int(2*samNx))
    xAE = np.linspace(-Nx*resX, Nx*resX,2*Nx)


    # Amplitude of both beams (assumed equal)
    A = 1.35e5 #0.148e5 #0.078e5  0.37e5 #0.3e5  # this may be scaled to  match simulated intensity
    k = 2*np.pi/w
    m = 1 # order of diffracted beams from each grating
    d = 100e-9 #24e-9 #100e-9 # grating spacing
    # angle between the beams from each grating
    theta = np.arcsin( m *w/d)
    IP = interferenceGratingModelsJK.interferenceIntensity(xAE,k,theta,A=A)
    IPsam = IP[int((Nx-samNx)/2) : int((Nx+samNx)/2)]
    
    # plt.plot(IPsam)
    # plt.show()
    
    # eAreal = np.real(eAP)
    # eBreal = np.real(eBLOCK)

    realE = [np.real(eAP), np.real(eBLOCK)]
    imagE = [np.imag(eAP), np.imag(eBLOCK)]
    
    sumE = sumTwoE(realE[0], imagE[0], realE[1], imagE[1],A=0.1)
    
    plt.plot(sumE)
    plt.show()
    
    # B = 0.1
    # E = np.sqrt(realE[0]**2+realE[1]**2) + B*2*np.sqrt(np.sqrt(abs(realE[0]*realE[1])))*np.sin(imagE[0]-imagE[1])#np.cos(imagE[0]-imagE[1])#*np.sin(imagE[1]-imagE[0])
    # E_0 = np.sqrt(realE[0]**2+realE[1]**2)
    
    # profSUB = (E/np.max(E))*((IPsam)/np.max(IPsam))
    
    # plt.plot(abs(realE[0])/np.max(abs(realE[0])), label='ap E')
    # # plt.plot(abs(realE[1])/np.max(abs(realE[1])), label='block E')
    # plt.plot(E_0/np.max(E_0), label='Esum')
    # plt.plot(E/np.max(E), label='Esum1')
    # # plt.plot(profileAE/np.max(profileAE), label='AE')
    # # plt.plot(IPsam/np.max(IPsam), label='aerial image')
    # plt.plot(profSUB/np.max(profSUB), label='E*Ideal')
    # # plt.xlim(-int(plotRange/2), int(plotRange/2))
    # plt.ylim(bottom=0)
    # plt.legend()
    # plt.show()


if __name__ == '__main__':
    # testDiffraction()
    testAerialImageEnvelope()
    
    