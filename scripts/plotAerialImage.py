#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 11:48:36 2022

@author: jerome
"""

import numpy as np
from numpy import sin, cos, exp, pi, sqrt, square
import matplotlib.pyplot as plt
import tifffile


def interferenceIntensityTMTM(x, k, theta, A=1.0):
    """
    Generate intensity profile for interfernce between TM polarised beams from
    a pair of diffraction gratings.  Based on

    X Wang et al, Proceedings Volume 10809, International Conference on Extreme Ultraviolet
    Lithography 2018; 108091Z (2018) https://doi.org/10.1117/12.2501949

    For two TM polarized beams, the electric field is parallel to the incident plane
    and can be decomposed in the x and z directions regarding incident angle. In this
    case, assuming 0 initial phases, equal amplitudes A, with the azimuthal angles
    ?1 = 0°, ?2 = 180° and polarization angles ?1 = 0°, ?2 = 0°, the electric fields
    are:

      E1 = A*exp(i*(k*x*np.sin(theta) - k*x*cos(theta )))
      E2 = A*exp(i*(-k*x*np.sin(theta) - k*x*cos(theta )))

    The polarisation vectors are :

      p1 = cos(theta)*y*iv+sin(tehta)*z*kv
      p2 = cos(theta)*y*iv-sin(tehta)*z*kv

    where iv, jv, kv is unit vector in x direction (i,j,k notation)
    """
    I = 2.0 * square(A) + 2.0 * square(A) * cos(2.0 * k * x * sin(theta)) * cos(
        2.0 * theta
    )

    return I


def interferenceIntensityTETE(x, k, theta, A=1.0):
    """
    Generate intensity profile for interfernce between TE polarised beams from
    a pair of diffraction gratings.  Based on

    X Wang et al, Proceedings Volume 10809, International Conference on Extreme Ultraviolet
    Lithography 2018; 108091Z (2018) https://doi.org/10.1117/12.2501949

    """
    I = 2.0 * square(A) + 2.0 * square(A) * cos(2.0 * k * x * sin(theta))

    return I


def interferenceIntensityTMTE(x, k, theta, gamma, A=1.0):
    """
    Generate intensity profile for interfernce between a TE and TM polarised beam from
    a pair of diffraction gratings.  Based on

    X Wang et al, Proceedings Volume 10809, International Conference on Extreme Ultraviolet
    Lithography 2018; 108091Z (2018) https://doi.org/10.1117/12.2501949

    Polarization may by controlled by rotating the grating by certain angle gamma
    (e.g., 45°) In this case, for two-beam interference, the two diffracted beams
    will carry both TE and TM polarizations.

    """
    I = 2.0 * square(A) + square(cos(gamma)) * (
        2.0
        + cos(2.0 * k * x * cos(gamma) * sin(theta)) * cos(2.0 * theta)
        + 2.0 * cos(2.0 * k * cos(gamma) * x * sin(theta))
    )

    return I


def interferenceIntensity(x, k, theta, A=1.0, gamma=0, polarisationModes=("TM", "TM")):
    if polarisationModes[0] == "TE" and polarisationModes[1] == "TE":
        I = interferenceIntensityTETE(x, k, theta, A)

    if polarisationModes[0] == "TM" and polarisationModes[1] == "TM":
        I = interferenceIntensityTMTM(x, k, theta, A)

    if (polarisationModes[0] == "TE" and polarisationModes[1] == "TM") or (
        polarisationModes[0] == "TM" and polarisationModes[1] == "TE"
    ):
        I = interferenceIntensityTMTE(x, k, theta, gamma, A)
    return I


def test():
    """load a saved intensity profile. We will use some properties of this profile
    for simulations."""

    # profile = np.load('profile01.npy')
    Ipath = "/home/jerome/dev/data/aerialimages/"
    files = ["ideal27intensity.tif", "aerialImageintensity.tif"]

    tiffs = [tifffile.imread(Ipath + f) for f in files]  # read tiff files

    res = [
        (2.5182637683019347e-09, 1.113721350329607e-07),
        (2.5011240434424064e-09, 2.658184246883298e-07),
    ]

    res1 = 2.5182637683019347e-09  # 4.77529829067939e-10 #2.1488261831535813e-9
    res2 = 2.5011240434424064e-09  # 6.46327159071368e-10 #1.9651701737063605e-9 # (3.924772866734718e-05 + 4.546782781154186e-05)/39424

    ny = 1
    nx = 500

    midX = [12544 + 355, 12544 - 287]  # [int(np.shape(t)[1]/2) for t in tiffs]
    midY = [60, 196]  # [int(np.shape(t)[0]/2) for t in tiffs]

    print("MidX: ", midX)
    print("MidY: ", midY)

    Ry = [res1 * ny, res2 * ny]
    # M = round((res1*N)/res2)
    # R2 = res2*M
    # print("Range 1: {} m".format(R1))
    # print("Range 2: {} m".format(R2))
    # print("M: {}".format(M))

    Iprofiles = [
        t[y - ny : y + ny, :].mean(0) for t, y in zip(tiffs, midY)
    ]  # take averaged line profile through interference fringes

    # plt.imshow(tiffs[0], aspect='auto')
    # plt.colorbar()
    # plt.show()

    # plt.plot(Iprofiles[0])
    # plt.plot(Iprofiles[1])
    # plt.show()

    aerialImages = [
        i[x - nx : x + nx] for i, x in zip(Iprofiles, midX)
    ]  # take centre of line profile

    print("shape of profiles: ", np.shape(aerialImages))

    labels = ["Original beamline", "Corrected beamline"]

    # profile = I5000[m1-N:m1+N]# I5000[m1-N:m1+N] #I1000TM[m2-N:m2+N]
    # profile2 = I100[m1-N:m1+N] #I1000[m2-N:m2+N]
    profileN = [np.size(a) for a in aerialImages]
    profileXs = [
        res1,
        res2,
    ]  # 1.9651759267701173e-09 #1.9651759267701173e-09 #1.0e-8 # pixel scaling factor/
    profileX = [
        np.linspace(-0.5 * pn * px, 0.5 * pn * px, pn)
        for pn, px in zip(profileN, profileXs)
    ]

    print("range of profiles: ", [np.max(X) - np.min(X) for X in profileX])
    # -0.5*profileN*profileXs, 0.5*profileN*profileXs,profileN) for
    # -4.546782781154186e-05 #Initial Horizontal Position [m]
    # 3.924772866734718e-05 #Final Horizontal Position [m]
    #    #39424 #Number of points vs Horizontal Position
    #
    #    profileV = np.size(aerialImagesV[0])
    #    profileVs = resV
    #    profileV1 = np.linspace(-0.5*profileV*profileVs, 0.5*profileV*profileVs,profileV)

    # print(profileX1s)

    """ define interference grating parameters"""
    wl = 6.710553853647976e-9  # wavelength in m

    # Amplitude of both beams (assumed equal)
    A = 0.25e5  # 0.37e5 #0.3e5  # this may be scaled to  match simulated intensity

    k = 2 * np.pi / wl

    m = 1  # order of diffracted beams from each grating
    d = 14e-9  # 24e-9 #100e-9 # grating spacing

    # angle between the beams from each grating
    theta = np.arcsin(m * wl / d)

    # define x positions:
    xstep = profileXs[0]
    n = profileN[0]
    x = np.linspace(
        -xstep * int(n / 2), xstep * int(n / 2), n
    )  # np.linspace(-90e-9,90e-9,10000)
    ##    xV =  np.linspace(-profileVs*int(profileV/2),profileVs*int(profileV/2),profileV)

    # noise parameters
    rho = 4 * 1 / xstep
    """ generate interference intensity"""
    I = interferenceIntensity(x, k, theta, A=A, polarisationModes=("TE", "TE"))
    ##    IV = interferenceIntensity(xV,k,theta,A=A)

    # ''' generate noise '''
    # sr = n  # (as period = n/sr)
    # noise = whiteNoise(rho, sr, n, mu=0)
    # # Inoisy = I + noise

    """ convolve intensity with gaussian """
    #    sigma = 1.5 #2.7
    #    I = gaussian_filter(I, sigma=sigma)

    #     plt.plot(profileX,aerialImages[0], label=labels[0])
    #     plt.legend()
    # #    plt.plot(profileV1,aerialImagesV[0])
    #     plt.show()

    #     ''' plot intensity with and without noise, together with saved profile'''
    #     # plt.plot(x*1e6,Inoisy,label='Model amplitude + noise')
    # #    plt.plot(x*1e6,I, ':', label='Model - TM')
    # #    plt.plot(x1*1e6,I1, ':', label='Model - TE')
    for i, a in enumerate(aerialImages):  # [1::]
        MAX = np.max(a)
        print("Shape of profile: {}".format(np.shape(a)))
        print("Plotting profile number {}".format(i + 1))
        plt.plot(profileX[i] * 1e6, a / MAX, label=labels[i])
    # #    for i, b in enumerate(aerialImagesV):
    # #        plt.plot(profileV1*1e6, b, label=labelsV[i])
    #     # plt.plot(profileX*1e6, profile,label='Simulated profile 1')
    #     # plt.plot(profileX*1e6, profile2,label='Simulated profile 2')
    #     plt.xlabel('Position [um]')
    #     plt.ylabel('Intensity [a.u.]')
    #     plt.ylim(bottom=0)#, top=0.5e9)
    plt.legend()
    #     plt.rcParams["figure.figsize"] = [7,4]
    plt.show()


if __name__ == "__main__":
    test()
    # test_multi()
