#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  3 10:58:14 2022

@author: jerome
"""

import matplotlib.pyplot as plt
import numpy as np
plt.style.use('thesis')

def magnification(z,rc):
    M = 1 + z/rc
    return M

def fresnelNo(a,z,lam):
    """
    Parameters
    ----------
    a : int/float
        Characteristic size of the aperture [m].
    z : int/float
        Propagation distance [m].
    lam : int/float
        Wavelength [m].
    Returns
    -------
    F : fresnel number
    """
    F = (a**2)/(z*lam)
    return F

def minDistOverSFF(w,dx,lam):
    """
    Only valid for far-field!
    
    w: width of object
    dx: detector pixel width
    lam: wavelength
    
    returns:
        z: minimum propagation distance for oversampling
    """
    z = (2*w*dx)/lam
    return z

def maxWidthOverSFF(z,lam,dx):
    """
    Only valid for far-field!
    
    z: distance from object to detector
    lam: wavelength
    dx: detector pixel width
    
    returns:
        w: maximum width of object
    """  
    w = (z*lam)/(2*dx)
    return w

def objectResFF(lam,z,N,dx):
    """
    Only valid for far-field!
    
    lam: wavelength
    z: distance from sample to detector
    N: number of pixels in detector
    dx: detector pixel width
    
    returns:
        dxs: resolution at sample
    """
    dxs = (lam*z)/(N*dx)
    return dxs

def minDistOverSNF(w,dXd,dXo,lam,N):
    """
    Valid for Fresnel propagation.
    
    w: width of object
    dXd: detector plane pixel width
    dXo: object plane pixel width
    lam: wavelength
    N: number of pixels in detector
    
    returns:
        z: minimum propagation distance for oversampling
    """
    D = N*dXd
#    z = ((w*dXd + D*dXo)/lam)
    z = ((dXd*w)/lam) - ((dXo*D)/lam)
#    u = (w*N*dXd)
#    d = ((lam*(N - (D/dXd))))
#    z = u/d #(w*N*dXd)/((lam*(N - (D/dXd))))
    return z
    
def maxWidthOverSNF(z,lam,dXd,dXo,N):
    """
    Valid for Fresnel propagation
    
    z: distance from object to detector
    lam: wavelength
    dXd: detector plane pixel width
    dXo: object plane pizel width
    N: number of 
    
    returns:
        w: maximum width of object
    """  
    D = N*dXd
    w = ((D*dXo)/dXd) + ((lam*z)/dXd)
    return w

def objectResNF(lam,z,N,dx,w):
    """
    Valid for Fresnel propagation.
    
    lam: wavelength
    z: distance from sample to detector
    N: number of pixels in detector
    dx: detector pixel width
    w = width of object
    
    returns:
        dxs: resolution at sample
    """
    D = N*dx
    dxs = ((dx*w)/D)-((lam*z)/D)
    return dxs

def propReq(lam,z,N,dx,rc):
    print("Checking Sampling Requirements... ")
    
    M = magnification(z, rc)
    rCon = (2*np.sqrt(2)*lam*z)/(M*N*(dx**2)) #(2*np.sqrt(2)*lam*z)/(N*(dx**2))
    rFFT = (2*np.sqrt(2)*M*N*(dx**2))/(lam*z) #(2*np.sqrt(2)*N*(dx**2))/(lam*z)
    rAngSpec = (2*np.sqrt(2)*lam*z)/((M*N*(dx**2))*np.sqrt(1-((lam**2)/(2*(dx**2)))))
    
    print(f"magnification: {M}")
    print("|=============================================|")
    print("|Propagator       ||     Requirment Met (y/n)|")
    print("|-----------------||-------------------------|")
    if rCon < 1:
        print("|Convolution      ||                     yes |")
    else:
        print("|Convolution      ||                      no |")
    if rFFT < z:
        print("|FFT              ||                     yes |")
    else:
        print("|FFT              ||                      no |")
    if rAngSpec < 1:
        print("|Angular Spectrum ||                     yes |")
    else:
        print("|Angular Spectrum ||                      no |")
    print("|=============================================|")
    
def usefulRange(lam,N,dx):
                
    angSpec = (N*(dx**2)*(np.sqrt( (1-(lam**2))/(2*(dx**2)) )))/lam
    fft_conv = (N*(dx**2))/lam
    
    print("|=============================================|")
    print("|Propagator       ||             Useful Range|")
    print("|-----------------||-------------------------|")
    print(f"|Angular Spectrum ||           z < {angSpec:.3g} m|")
    print(f"|Convolution      ||           z < {fft_conv:.3g} m|")
    print(f"|FFT              ||           z > {fft_conv:.3g} m|")
    print("|=============================================|")

def pixelSample(lam,z,rc,N,dx):
    _z = z/(1+(z/rc))
    angSpec = dx
    fft = 1/(lam*_z*N*dx)
    conv = dx*magnification(z, rc)
    print(_z)
    print("|=============================================|")
    print("|Propagator       ||               Pixel Size|")
    print("|-----------------||-------------------------|")
    print(f"|Angular Spectrum ||           z < {angSpec:.3g} m|")
    print(f"|FFT              ||           z > {fft:.3g} m|")
    print(f"|Convolution      ||           z < {conv:.3g} m|")
    print("|=============================================|")

def testSampling(lam, px,N,zMax,zMin,Gx,Mx,Bx,field):
    """
    Parameters
    ----------
    lam : wavelength [m].
    px : detector pixel width [m].
    N : number of detector pixels.
    zMax : maximum propagation distance [m].
    zMin : minimum propagation distance [m].
    Gx : grating size [m].
    Mx : mask size [m].
    Bx : beam size [m].
    field : 'near' or 'far'.
    Returns
    -------
    None.
    """
    
    dZ = np.linspace(zMin,0.1,1000)
    dW = np.linspace(Gx,Mx*4,1000)
    
    fig, ax = plt.subplots(1,3)
    print(f"Detector resolution:                    {px*1e6} um")
    print(f"Number of pixels in detector:           {N}")
    print(f"Minimum allowable propagation distance: {zMin*1e3} mm")
    print(f"Maximum allowable propagation distance: {zMax} m")
    print(f"Size of grating:                        {Gx*1e6} um")
    print(f"Size of four grating mask:              {Mx*1e6} um")
    
    for l in lam:
        if field == 'near':
            print("NEAR-FIELD SAMPLING REQUIREMENTS")
            print(" ")
            ax[1].set_title('Near field')
            dx_zmin = objectResFF(l,zMin,N,px)  # object resolution for minimum propagation distance
            dx_zmax = objectResFF(l,zMax,N,px)  # object resolution for maximum propagation distance
            
            # dX_zmin = testN(l,zMin,px,Bx,N)  # object resolution for minimum propagation distance
            # dX_zmax = testN(l,zMin,px,Bx,N)  # object resolution for maximum propagation distance
            
            W_zmax = maxWidthOverSNF(zMax,l,px,dx_zmax,N) # maximum object width for maximum propagation distance 
            W_zmin = maxWidthOverSNF(zMin,l,px,dx_zmin,N) # maximum object width for minimum propagation distance
    
            z_g = minDistOverSNF(Gx,px,dx_zmin,l,N)   # minimum propagation distance to oversample grating
            z_m = minDistOverSNF(Mx,px,dx_zmax,l,N)   # minimum propagation distance to oversample mask
            
            oRes = [objectResNF(l,z,N,px,Mx)*1e9 for z in dZ]
            oWidth = [maxWidthOverSNF(z,l,px,d,N)*1e3 for z,d in zip(dZ,oRes)]
            propD = [minDistOverSNF(w,px,d,l,N)*1e3 for w,d in zip(dW,oRes)]
            
        elif field == 'far':
            print("FAR-FIELD SAMPLING REQUIREMENTS")
            print(" ")
            ax[1].set_title('Far field')
            W_zmax = maxWidthOverSFF(zMax,l,px) # maximum object width for maximum propagation distance 
            W_zmin = maxWidthOverSFF(zMin,l,px) # maximum object width for minimum propagation distance
            
            z_g = minDistOverSFF(Gx,px,l)   # minimum propagation distance to oversample grating
            z_m = minDistOverSFF(Mx,px,l)   # minimum propagation distance to oversample mask
            
            dx_zmin = objectResFF(l,zMin,N,px)  # object resolution for minimum propagation distance
            dx_zmax = objectResFF(l,zMax,N,px)  # object resolution for maximum propagation distance
            
            oWidth = [maxWidthOverSFF(z,l,px)*1e3 for z in dZ]
            propD = [minDistOverSFF(w,px,l)*1e3 for w in dW]
            oRes = [objectResFF(l,z,N,px)*1e9 for z in dZ]
        else:
            print("Invalid field... must be 'near' or 'far' ")
            break
        
#        w,dXd,dXo,lam,N
        
        print("===========================================================================")
        print(f'|| Beam wavelength:       {l*1e9:.3g} nm')
        print("||")
        print(f'|| Maximum object width for minimum propagation distance:    || {W_zmin*1e6:.3g} um')
        print(f'|| Maximum object width for maximum propagation distance:    || {W_zmax*1e6:.3g} um')
        print('|| -')
        print(f'|| Minumum propagation distance to oversample grating:       || {z_g*100:.3g} cm')
        print(f'|| Minumum propagation distance to oversample mask:          || {z_m*100:.3g} cm')
        print('|| -')
        print(f'|| Object resolution for minimum propagation distance:       || {dx_zmin*1e9:.3g} nm')
        print(f'|| Object resolution for maximum propagation distance:       || {dx_zmax*1e9:.3g}  nm')
        
        print("===========================================================================")
        
        # oRes = [objectResNF(l,z,N,px,Mx)*1e9 for z in dZ]
        # oRes1 = [objectResFF(l,z,N,px)*1e9 for z in dZ]
        # oRes2 = [testN(l,z,px,Mx,N)*1e9 for z in dZ]
        
        # oWidth = [maxWidthOverSNF(z,l,px,d,N)*1e3 for z,d in zip(dZ,oRes2)]
        # propD = [minDistOverSNF(w,px,d,l,N)*1e3 for w,d in zip(dW,oRes2)]
        
        
        ax[0].plot(dZ,oWidth, label=f'$\lambda =${l*1e9:.3g} nm')
        ax[0].set_xlabel('Propagation Distance [m]')
        ax[0].set_ylabel('Maximum Object Width [mm]')
#        ax[1].plot(dZ,oRes, label=f'$\lambda =${l*1e9:.3g} nm')
        ax[1].plot(dZ,oRes, ':', label=f'$\lambda =${l*1e9:.3g} nm')
        # ax[1].plot(dZ,oRes2, label=f'$\lambda =${l*1e9:.3g} nm - NF')
        ax[1].set_xlabel('Propagation Distance [m]')
        ax[1].set_ylabel('Object Resolution [nm]')
        ax[1].legend()
        ax[2].plot(dW*1e6,propD, label=f'$\lambda =${l*1e9:.3g} nm')
        ax[2].set_xlabel('Object Width [microns]')
        ax[2].set_ylabel('Minimum Propagation Distance [mm]')
    plt.legend()
    plt.tight_layout()
    plt.plot()
    
    # testN(lam2,zMin,px,Mx,N)

def test():
    
    lam1 = 6.7e-9   # BEUV wavelength
    lam2 = 13.5e-9  # EUV wavelength
    px = 11e-6      # detector pixel size
    N = 2048        # number of detector pixels
    zMax = 1        # maximum allowable propagation distance
    zMin = 30e-3    # minimum allowable propagation distance
    
    Gx = 40e-6       # size of grating
    Mx = 120e-6      # size of four-grating mask
    Bx = 500e-6      # size of beam at mask
    
    rc = 9.7
    
    NearField = False
    FarField = True
    checkReq = False
    checkRange = False
    checkPixelSize = False
    
    if checkReq:
        print(" ")
        print(f'Wavelength =  {lam1*1e9:.3g} nm, z = {zMin:.3g} m')
        propReq(lam1,zMin,N,px,rc)
        f = fresnelNo(Gx, zMin, lam1)
        print(f'Fresnel Number = {f}')
        print(" ")
        print(f'Wavelength =  {lam1*1e9:.3g} nm, z = {zMax:.3g} m')
        propReq(lam1,zMax,N,px,rc)
        f = fresnelNo(Gx, zMax, lam1)
        print(f'Fresnel Number = {f}')
        print(" ")
        print(f"Wavelength =  {lam2*1e9:.3g} nm, z = {zMin:.3g} m")
        propReq(lam2,zMin,N,px,rc)
        f = fresnelNo(Gx, zMin, lam2)
        print(f'Fresnel Number = {f}')
        print(" ")
        print(f"Wavelength =  {lam2*1e9:.3g} nm, z = {zMax:.3g} m")
        propReq(lam2,zMax,N,px,rc)
        f = fresnelNo(Gx, zMax, lam2)
        print(f'Fresnel Number = {f}')
    else:
        pass
    if checkRange:
        print(" ")
        print(f'Wavelength =  {lam1*1e9:.3g}')
        usefulRange(lam1, N, px)
        print(" ")
        print(f'Wavelength =  {lam2*1e9:.3g}')
        usefulRange(lam2, N, px)
    else:
        pass
    if checkPixelSize:
        print(" ")
        print(f'Wavelength =  {lam1*1e9:.3g} nm, z = {zMin:.3g} m')
        pixelSample(lam1, zMin, rc, N, px)
        print(" ")
        print(f'Wavelength =  {lam1*1e9:.3g} nm, z = {zMax:.3g} m')
        pixelSample(lam1, zMin, rc, N, px)
        print(" ")
        print(f'Wavelength =  {lam2*1e9:.3g} nm, z = {zMin:.3g} m')
        pixelSample(lam1, zMin, rc, N, px)
        print(" ")
        print(f'Wavelength =  {lam2*1e9:.3g} nm, z = {zMax:.3g} m')
        pixelSample(lam1, zMin, rc, N, px)
        
    if NearField:
        testSampling([lam1,lam2],px,N,zMax,zMin,Gx,Mx,Bx, field='near')
    else:
        pass
    if FarField:
        testSampling([lam1,lam2],px,N,zMax,zMin,Gx,Mx,Bx, field='far')
    else:
        pass
    
def testN(lam,z,dx,w,N):
    D = dx*N
#    dxs_n = ((lam*z)*(1 - np.sqrt((1 + ((4*D*w)/(lam*z*N))))))/(2*D)
    dxs_p = ((lam*z)*(1 + np.sqrt((1 + ((4*D*w)/(lam*z*N))))))/(2*D)
    
#    print(dxs_n)
#    print(dxs_p)
    return dxs_p

if __name__ == "__main__":

#    testSamplingFF()
    test()
#    testSamplingNF()