#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  3 10:58:14 2022

@author: jerome
"""

import matplotlib.pyplot as plt
import numpy as np


def minDistOverSFF(w, dx, lam):
    """
    Only valid for far-field!

    w: width of object
    dx: detector pixel width
    lam: wavelength

    returns:
        z: minimum propagation distance for oversampling
    """
    z = (2 * w * dx) / lam
    return z


def maxWidthOverSFF(z, lam, dx):
    """
    Only valid for far-field!

    z: distance from object to detector
    lam: wavelength
    dx: detector pixel width

    returns:
        w: maximum width of object
    """
    w = (z * lam) / (2 * dx)
    return w


def objectResFF(lam, z, N, dx):
    """
    Only valid for far-field!

    lam: wavelength
    z: distance from sample to detector
    N: number of pixels in detector
    dx: detector pixel width

    returns:
        dxs: resolution at sample
    """
    dxs = (lam * z) / (N * dx)
    return dxs


def minDistOverSNF(w, dXd, dXo, lam, N):
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
    D = N * dXd
    #    z = ((w*dXd + D*dXo)/lam)
    z = ((dXd * w) / lam) - ((dXo * D) / lam)
    #    u = (w*N*dXd)
    #    d = ((lam*(N - (D/dXd))))
    #    z = u/d #(w*N*dXd)/((lam*(N - (D/dXd))))
    return z


def maxWidthOverSNF(z, lam, dXd, dXo, N):
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
    D = N * dXd
    w = ((D * dXo) / dXd) + ((lam * z) / dXd)
    return w


def objectResNF(lam, z, N, dx, w):
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
    D = N * dx
    dxs = ((dx * w) / D) - ((lam * z) / D)
    return dxs


def propReq(lam, z, N, dx):
    print("Checking Sampling Requirements... ")

    rCon = (2 * np.sqrt(2) * lam * z) / (N * (dx**2))
    rFFT = (2 * np.sqrt(2) * N * (dx**2)) / (lam * z)
    rAngSpec = (2 * np.sqrt(2) * lam * z) / (
        (N * (dx**2)) * np.sqrt(1 - ((lam**2) / (2 * (dx**2))))
    )

    print("|=============================================|")
    print("|Propagator       ||     Requirment Met (y/n)|")
    print("|-----------------||-------------------------|")
    if rCon < 1:
        print("|Convolution      ||                     yes |")
    else:
        print("|Convolution      ||                      no |")
    if rFFT < 1:
        print("|FFT              ||                     yes |")
    else:
        print("|FFT              ||                      no |")
    if rAngSpec < 1:
        print("|Angular Spectrum ||                     yes |")
    else:
        print("|Angular Spectrum ||                      no |")
    print("|=============================================|")

    print(rCon)
    print(rFFT)
    print(rAngSpec)


def targetFresnel(N, dx, T, lam, z):
    D = N * dx
    Nf = (D * T) / (lam * z)
    Ws = (lam * z) / T

    print(f"Target Fresnel Number: {Nf:.3g}")
    print(f"Speckle Width          {Ws:.3g} m")

    return Nf, Ws


def convSampling(lam, z=None, N=None, dx=None):
    if lam and z and N and dx != None:
        print("Are sampling requirements met for convolution propagator?? ... ")
        check = (2 * np.sqrt(2) * lam * z) / (N * (dx**2))
        if check >= 1:
            print("No")
        elif check < 1:
            print("Yes")

        return check
    elif z == None:
        zmax = (N * (dx**2)) / (2 * np.sqrt(2) * lam)
        return zmax
    elif N == None:
        Nreq = (2 * np.sqrt(2) * lam * z) / (dx**2)
        return Nreq
    elif dx == None:
        dxReq = np.sqrt((2 * np.sqrt(2) * lam * z) / N)
        return dxReq


def fftSampling(lam, z=None, N=None, dx=None):
    if lam and z and N and dx != None:
        print("Are sampling requirements met for FFT propagator?? ... ")
        check = (2 * np.sqrt(2) * N * (dx**2)) / (lam * z)
        if check >= 1:
            print("No")
        elif check < 1:
            print("Yes")
        return check

    elif z == None:
        zmin = (2 * np.sqrt(2) * N * (dx**2)) / lam
        return zmin
    elif N == None:
        Nreq = (lam * z) / (2 * np.sqrt(2) * (dx**2))
        return Nreq
    elif dx == None:
        dxReq = np.sqrt((lam * z) / (2 * np.sqrt(2) * N))
        return dxReq


def angSpecSampling(lam, z=None, N=None, dx=None):
    if lam and z and N and dx != None:
        print("Are sampling requirements met for angular spectrum propagator?? ... ")
        check = (2 * np.sqrt(2) * lam * z) / (
            (N * (dx**2)) * np.sqrt(1 - ((lam**2) / (2 * (dx**2))))
        )
        if check >= 1:
            print("No")
        elif check < 1:
            print("Yes")
        return check

    elif z == None:
        zmax = (N * dx * np.sqrt(2 * (dx**2) - (lam**2))) / (4 * lam)
        return zmax
    elif N == None:
        Nreq = (4 * z * lam * np.sqrt(2 * (dx**2) - (lam**2))) / (
            2 * (dx**3) - dx * lam
        )
        return Nreq
    elif dx == None:
        print(
            "Finding sample pixel resolution not currently supported for angular spectrum propagator"
        )
        pass


def testSamplingFF():
    lam1 = 6.7e-9
    lam2 = 13.5e-9
    px = 11e-6
    N = 2048
    zMax = 1  # maximum allowable propagation distance
    zMin = 21e-3  # minimum allowable propagation distance

    Gx = 40e-6  # size of grating
    Mx = 120e-6  # size of four-grating mask
    Bx = 1e-3  # maximum extend of beam at mask plane

    deltaZ = np.linspace(zMin, zMax, 1000)
    deltaW = np.linspace(Gx, Mx * 4, 1000)

    fig, ax = plt.subplots(1, 3)
    print("FAR-FIELD SAMPLING REQUIREMENTS")
    print(" ")
    print(f"Detector resolution:                    {px*1e6} um")
    print(f"Number of pixels in detector:           {N}")
    print(f"Minimum allowable propagation distance: {zMin*1e3} mm")
    print(f"Maximum allowable propagation distance: {zMax} m")
    print(f"Size of grating:                        {Gx*1e6} um")
    print(f"Size of four grating mask:              {Mx*1e6} um")
    print(f"Size of beam at mask:                   {Bx*1e6} um")

    for l in (lam1, lam2):
        W_zmax = maxWidthOverSFF(
            zMax, l, px
        )  # maximum object width for maximum propagation distance
        W_zmin = maxWidthOverSFF(
            zMin, l, px
        )  # maximum object width for minimum propagation distance

        z_g = minDistOverSFF(
            Gx, px, l
        )  # minimum propagation distance to oversample grating
        z_m = minDistOverSFF(
            Mx, px, l
        )  # minimum propagation distance to oversample mask
        z_b = minDistOverSFF(
            Bx, px, l
        )  # minimum propagation distance to oversample beam

        dx_zmin = objectResFF(
            l, zMin, N, px
        )  # object resolution for minimum propagation distance
        dx_zmax = objectResFF(
            l, zMax, N, px
        )  # object resolution for maximum propagation distance

        print(
            "==========================================================================="
        )
        print(f"|| Beam wavelength:       {l*1e9:.3g} nm")
        print("||")
        print(
            f"|| Maximum object width for minimum propagation distance:    || {W_zmin*1e6:.3g} um"
        )
        print(
            f"|| Maximum object width for maximum propagation distance:    || {W_zmax*1e6:.3g} um"
        )
        print("|| -")
        print(
            f"|| Minumum propagation distance to oversample grating:       || {z_g*100:.3g} cm"
        )
        print(
            f"|| Minumum propagation distance to oversample mask:          || {z_m*100:.3g} cm"
        )
        print(
            f"|| Minumum propagation distance to oversample beam:          || {z_b*100:.3g} cm"
        )
        print("|| -")
        print(
            f"|| Object resolution for minimum propagation distance:       || {dx_zmin*1e9:.3g} nm"
        )
        print(
            f"|| Object resolution for maximum propagation distance:       || {dx_zmax*1e9:.3g}  nm"
        )

        print(
            "==========================================================================="
        )
        print(" ")

        oWidth = [maxWidthOverS(z, l, px) * 1e3 for z in deltaZ]
        propD = [minDistOverS(w, px, l) * 1e3 for w in deltaW]
        oRes = [objectResFF(l, z, N, px) * 1e9 for z in deltaZ]

        ax[0].plot(deltaZ, oWidth, label=f"$\lambda =${l*1e9:.3g} nm")
        ax[0].set_xlabel("Propagation Distance [m]")
        ax[0].set_ylabel("Maximum Object Width [mm]")
        ax[1].plot(deltaZ, oRes, label=f"$\lambda =${l*1e9:.3g} nm")
        ax[1].set_xlabel("Propagation Distance [m]")
        ax[1].set_ylabel("Object Resolution [nm]")
        ax[1].set_title("Far field")
        ax[2].plot(deltaW * 1e6, propD, label=f"$\lambda =${l*1e9:.3g} nm")
        ax[2].set_xlabel("Object Width [microns]")
        ax[2].set_ylabel("Minimum Propagation Distance [mm]")
    plt.legend()
    plt.tight_layout()
    plt.plot()


def testSamplingNF():
    lam1 = 6.7e-9
    lam2 = 13.5e-9
    px = 11e-6
    N = 2048
    zMax = 1  # maximum allowable propagation distance
    zMin = 21e-3  # minimum allowable propagation distance

    Gx = 40e-6  # size of grating
    Mx = 120e-6  # size of four-grating mask
    Bx = 2e-3  # maximum extend of beam at mask plane

    deltaZ = np.linspace(zMin, zMax, 1000)
    deltaW = np.linspace(Gx, Mx * 4, 1000)

    fig, ax = plt.subplots(1, 3)
    print("NEAR-FIELD SAMPLING REQUIREMENTS")
    print(" ")
    print(f"Detector resolution:                    {px*1e6} um")
    print(f"Number of pixels in detector:           {N}")
    print(f"Minimum allowable propagation distance: {zMin*1e3} mm")
    print(f"Maximum allowable propagation distance: {zMax} m")
    print(f"Size of grating:                        {Gx*1e6} um")
    print(f"Size of four grating mask:              {Mx*1e6} um")
    for l in (lam1, lam2):
        dx_zmin = objectResFF(
            l, zMin, N, px
        )  # object resolution for minimum propagation distance
        dx_zmax = objectResFF(
            l, zMax, N, px
        )  # object resolution for maximum propagation distance

        dX_zmin = testN(
            l, zMin, px, Bx, N
        )  # object resolution for minimum propagation distance
        dX_zmax = testN(
            l, zMin, px, Bx, N
        )  # object resolution for maximum propagation distance

        W_zmax = maxWidthOverSNF(
            zMax, l, px, dx_zmax, N
        )  # maximum object width for maximum propagation distance
        W_zmin = maxWidthOverSNF(
            zMin, l, px, dx_zmin, N
        )  # maximum object width for minimum propagation distance

        z_g = minDistOverSNF(
            Gx, px, dx_zmin, l, N
        )  # minimum propagation distance to oversample grating
        z_m = minDistOverSNF(
            Mx, px, dx_zmax, l, N
        )  # minimum propagation distance to oversample mask
        #        w,dXd,dXo,lam,N

        print(
            "==========================================================================="
        )
        print(f"|| Beam wavelength:       {l*1e9:.3g} nm")
        print("||")
        print(
            f"|| Maximum object width for minimum propagation distance:    || {W_zmin*1e6:.3g} um"
        )
        print(
            f"|| Maximum object width for maximum propagation distance:    || {W_zmax*1e6:.3g} um"
        )
        print("|| -")
        print(
            f"|| Minumum propagation distance to oversample grating:       || {z_g*100:.3g} cm"
        )
        print(
            f"|| Minumum propagation distance to oversample mask:          || {z_m*100:.3g} cm"
        )
        print("|| -")
        print(
            f"|| Object resolution for minimum propagation distance:       || {dx_zmin*1e9:.3g} nm"
        )
        print(
            f"|| Object resolution for maximum propagation distance:       || {dx_zmax*1e9:.3g}  nm"
        )

        print(
            "==========================================================================="
        )

        oRes = [objectResNF(l, z, N, px, Mx) * 1e9 for z in deltaZ]
        oRes1 = [objectResFF(l, z, N, px) * 1e9 for z in deltaZ]
        oRes2 = [testN(l, z, px, Mx, N) * 1e9 for z in deltaZ]

        oWidth = [maxWidthOverSNF(z, l, px, d, N) * 1e3 for z, d in zip(deltaZ, oRes2)]
        propD = [minDistOverSNF(w, px, d, l, N) * 1e3 for w, d in zip(deltaW, oRes2)]

        ax[0].plot(deltaZ, oWidth, label=f"$\lambda =${l*1e9:.3g} nm")
        ax[0].set_xlabel("Propagation Distance [m]")
        ax[0].set_ylabel("Maximum Object Width [mm]")
        #        ax[1].plot(deltaZ,oRes, label=f'$\lambda =${l*1e9:.3g} nm')
        ax[1].plot(deltaZ, oRes1, ":", label=f"$\lambda =${l*1e9:.3g} nm - FF")
        ax[1].plot(deltaZ, oRes2, label=f"$\lambda =${l*1e9:.3g} nm - NF")
        ax[1].set_xlabel("Propagation Distance [m]")
        ax[1].set_ylabel("Object Resolution [nm]")
        ax[1].set_title("Near field")
        ax[1].legend()
        ax[2].plot(deltaW * 1e6, propD, label=f"$\lambda =${l*1e9:.3g} nm")
        ax[2].set_xlabel("Object Width [microns]")
        ax[2].set_ylabel("Minimum Propagation Distance [mm]")
    plt.legend()
    plt.tight_layout()
    plt.plot()

    testN(lam2, zMin, px, Mx, N)


def testSampling():
    lam1 = 6.7e-9
    lam2 = 13.5e-9
    px = 11e-6
    N = 2048
    zMax = 1  # maximum allowable propagation distance
    zMin = 21e-3  # minimum allowable propagation distance
    Bx = 2e-3  # maximum extend of beam at mask plane

    Gx = 40e-6  # size of grating
    Mx = 120e-6  # size of four-grating mask

    deltaZ = np.linspace(zMin, zMax, 1000)
    deltaW = np.linspace(Gx, Mx, 1000)

    NearField = False
    FarField = True
    Conv = False
    FFT = False
    angSpec = False

    checkReq = False

    if checkReq:
        print(" ")
        print(" 6.7 nm, z = 21 mm")
        propReq(lam1, zMin, N, objectResFF(lam1, zMin, N, px))
        print(" ")
        print(" 6.7 nm, z = 1 m")
        propReq(lam1, zMax, N, objectResFF(lam1, zMax, N, px))
        print(" ")
        print(" 13.5 nm, z = 21 mm")
        propReq(lam2, zMin, N, objectResFF(lam2, zMin, N, px))
        print(" ")
        print(" 13.5 nm, z = 1 m")
        propReq(lam2, zMax, N, objectResFF(lam2, zMax, N, px))
        print(" ")
    else:
        pass

    if NearField:
        testSamplingNF()
    else:
        pass
    if FarField:
        testSamplingFF()
    else:
        pass
    if Conv:
        print(" ")
        print("Convolution Propagator")
        minS = convSampling(lam=lam1, z=zMin, N=N, dx=2.5e-9)
        print(minS)
        maxS = convSampling(lam=lam1, z=zMax, N=N, dx=2.5e-9)
        print(maxS)
        zMaxConv = convSampling(lam=lam1, z=None, N=N, dx=2.5e-9)
        print(f"Max propagation Distance: {zMaxConv:.3g} m")
        NconvMin = convSampling(lam=lam1, z=zMin, N=None, dx=2.5e-9)
        print(f"Min N: {int(NconvMin)}")
        NconvMax = convSampling(lam=lam1, z=zMax, N=None, dx=2.5e-9)
        print(f"Max N: {int(NconvMax)}")
        XconvMin = convSampling(lam=lam1, z=zMin, N=N, dx=None)
        print(f"Min dx: {XconvMin:.3g} m")
        XconvMax = convSampling(lam=lam1, z=zMax, N=N, dx=None)
        print(f"Max dx: {XconvMax:.3g} m")
    else:
        pass
    if FFT:
        print(" ")
        print("Single FFT Propagator")
        minS = fftSampling(lam=lam1, z=zMin, N=N, dx=2.5e-9)
        print(minS)
        maxS = fftSampling(lam=lam1, z=zMax, N=N, dx=2.5e-9)
        print(maxS)
        zMaxfft = fftSampling(lam=lam1, z=None, N=N, dx=2.5e-9)
        print(f"Max propagation Distance: {zMaxfft:.3g} m")
        NfftMin = fftSampling(lam=lam1, z=zMin, N=None, dx=2.5e-9)
        print(f"Min N: {int(NfftMin)}")
        NfftMax = fftSampling(lam=lam1, z=zMax, N=None, dx=2.5e-9)
        print(f"Max N: {int(NfftMax)}")
        XfftMin = fftSampling(lam=lam1, z=zMin, N=N, dx=None)
        print(f"Min dx: {XfftMin:.3g} m")
        XfftMax = fftSampling(lam=lam1, z=zMax, N=N, dx=None)
        print(f"Max dx: {XfftMax:.3g} m")
    else:
        pass
    if angSpec:
        print(" ")
        print("Angular Spectrum Propagator")
        minS = angSpecSampling(lam=lam1, z=zMin, N=N, dx=2.5e-9)
        print(minS)
        maxS = angSpecSampling(lam=lam1, z=zMax, N=N, dx=2.5e-9)
        print(maxS)
        zMaxangSpec = angSpecSampling(lam=lam1, z=None, N=N, dx=2.5e-9)
        print(f"Max propagation Distance: {zMaxangSpec:.3g} m")
        NangSpecMin = angSpecSampling(lam=lam1, z=zMin, N=None, dx=2.5e-9)
        print(f"Min N: {int(NangSpecMin)}")
        NangSpecMax = angSpecSampling(lam=lam1, z=zMax, N=None, dx=2.5e-9)
        print(f"Max N: {int(NangSpecMax)}")
        XangSpecMin = angSpecSampling(lam=lam1, z=zMin, N=N, dx=None)
        print(f"Min dx: {XangSpecMin:.3g} m")
        XangSpecMax = angSpecSampling(lam=lam1, z=zMax, N=N, dx=None)
        print(f"Max dx: {XangSpecMax:.3g} m")
    else:
        pass


#    n, w = targetFresnel(N,px,Gx,lam,zMin)


def testN(lam, z, dx, w, N):
    D = dx * N
    #    dxs_n = ((lam*z)*(1 - np.sqrt((1 + ((4*D*w)/(lam*z*N))))))/(2*D)
    dxs_p = ((lam * z) * (1 + np.sqrt((1 + ((4 * D * w) / (lam * z * N)))))) / (2 * D)

    #    print(dxs_n)
    #    print(dxs_p)
    return dxs_p


if __name__ == "__main__":
    #    testSamplingFF()
    testSampling()
#    testSamplingNF()
