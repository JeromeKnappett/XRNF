#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 16:02:19 2021

@author: jerome
"""
# from wpg.generators import build_gauss_wavefront
# from wpg.srwlib import SRWLStokes, SRWLWfr
import numpy as np
import matplotlib.pyplot as plt

# import wfStokes
import scipy.ndimage

# from wpg.wavefront import Wavefront

# try:
#     from wpg.srw import srwlpy as srwl
# except ImportError:
#     import srwlpy as srwl

import time
import math

# from wpg.srwlib import *

from math import log10, floor, sqrt

# import wfAnalyseWave as aw

# print(plt.style.available)
# plt.style.reload_library()
# plt.style.use('seaborn')#['science','ieee']) # 'no-latex'])#,'ieee'])

colours = plt.rcParams["axes.prop_cycle"].by_key()["color"]


# %%
def round_sig(x, sig=2):
    if x != 0:
        return round(x, sig - int(floor(log10(abs(x)))) - 1)
    else:
        return x


def getCoherenceFromProfile(p):
    """
    Parameters
    ----------
    p : Line profile of complex electric field

    Returns
    -------
    C: Coherence profile

    """
    start = time.time()

    n = len(p)
    mid = int(n / 2)

    C = [abs(p[mid] * a) for a in p.conjugate()]

    nC = [c / np.max(C) for c in C]

    end = time.time()
    print("Time taken to generate coherence profile (s): ", (end - start))

    return nC


# %%
def profileMI(cpX, cpY, Ix, Iy, dx=1, dy=1, pathCP=None):
    """
    Calculates the Horizontal and Vertical Coherence profiles from line profiles through the complex wavefield.
    params:
    cpX: Horizontal profile of complex wavefield
    cpY: Vertical profile of complex wavefield
    Ix: Horizontal Intensity profile
    Iy: Vertical Intensity profile
    pathCP: Save path for coherence profile plot
    returns:
    cH: Horizontal coherence profile
    cV: Vertical coherence profile
    """

    """ Mutual Intensity Profiles """
    print(" ")
    print("-----Calculating Mutual Intensity profiles-----")
    ### CONVOLUTION DONE USING FOR LOOP ###
    start3 = time.time()
    print("Shape of line profiles:")
    print("Horizontal: {}".format(np.shape(cpX)))
    print("Vertical: {}".format(np.shape(cpY)))
    J_H = np.array(
        [cpX.conjugate() * a for a in cpX]
    )  # Horizontal coherence profile - Eq. 2.3.1.3
    J_V = np.array(
        [cpY.conjugate() * a for a in cpY]
    )  # Vertical coherence profile - Eq. 2.3.1.3
    end3 = time.time()
    print("time taken to calculate Mutual Intensity profiles: {}".format(end3 - start3))

    print("Shape of each Mutual Intensity profile:")
    print("Horizontal profile: {}".format(np.shape(J_H)))
    print("Vertical profile: {}".format(np.shape(J_V)))

    j_H = np.sqrt(J_H**2)  # abs(J_H) #(J_H[0]**2 + J_H[1]**2)**(1/2)
    j_V = np.sqrt(J_V**2)  # abs(J_V) #(J_V[0]**2 + J_V[1]**2)**(1/2)

    jHd = np.diagonal(np.squeeze(J_H))  # Diagonal of matrix J_H
    jVd = np.diagonal(np.squeeze(J_V))  # Diagonal of matrix J_V
    jHd2 = np.diagonal(np.squeeze(J_H).T)  # Diagonal of matrix J_H
    jVd2 = np.diagonal(np.squeeze(J_V).T)  # Diagonal of matrix J_V
    jHh = np.squeeze(j_H)[int(np.shape(np.squeeze(J_H))[0] / 2), :]
    jHv = np.squeeze(j_H)[:, int(np.shape(np.squeeze(J_H))[1] / 2)]
    jVh = np.squeeze(j_V)[int(np.shape(np.squeeze(J_V))[0] / 2), :]
    jVv = np.squeeze(j_V)[:, int(np.shape(np.squeeze(J_V))[1] / 2)]
    print("Shape of diagonalised arrays:")
    print("Horizontal: {}".format(np.shape(jHd)))
    print("Vertical: {}".format(np.shape(jVd)))

    ### CONVOLUTION DONE USING SCIPY.SIGNAL.FFTCONVOLVE ###
    from scipy import signal

    # jH = signal.convolve(cpX, cpX[::-1], mode='same')
    # jV = signal.convolve(cpY, cpY[::-1], mode='same')

    # print("Shape of each Mutual Intensity profile:")
    # print("Horizontal profile: {}".format(np.shape(jH)))
    # print("Vertical profile: {}".format(np.shape(jV)))

    # jHd = (abs(jH)**(1/2))
    # jVd = (abs(jV)**(1/2))

    # IH = signal.convolve(cpX, cpX, mode='same')
    IH = Ix  # abs(cpX.conjugate()*cpX)
    ## np.diagonal(list(zip(np.squeeze(J_H)[::-1])))
    # IV = signal.convolve(cpY, cpY, mode='same')
    IV = Iy  # abs(cpY.conjugate()*cpY)
    ## np.diagonal(list(zip(np.squeeze(J_V)[::-1])))

    # print("Shape of Intensity arrays:")
    # print("Horizontal: {}".format(np.shape(IH)))
    # print("Vertical: {}".format(np.shape(IV)))

    cH = 1 / (abs(np.squeeze(jHh) / np.squeeze(jHd)))  # Eq. 2.3.1.4
    cV = 1 / (abs(np.squeeze(jVh) / np.squeeze(jVd)))  # Eq. 2.3.1.4

    nXh, nYh = np.shape(j_H)
    nXv, nYv = np.shape(j_V)

    print(nXh, nXv)
    print("Range: ", nXh * dx)

    plt.clf()
    plt.close()
    plt.imshow(abs(j_H) / np.max(abs(j_H)))
    plt.title("J - Horizontal")
    plt.yticks(
        [int(nYh * (b / 8)) for b in range(0, 9)],
        [round_sig(nYh * dx * (a / 8) * 1e3) for a in range(-4, 5)],
    )
    plt.xticks(
        [int(nXh * (b / 8)) for b in range(0, 9)],
        [round_sig(nXh * dx * (a / 8) * 1e3) for a in range(-4, 5)],
    )
    plt.xlabel("($x_1 - x_2$) [mm]")
    plt.ylabel("($x_1 - x_2$) [mm]")
    plt.colorbar()
    plt.show()
    plt.imshow(abs(j_V) / np.max(abs(j_V)))
    plt.title("J - Vertical")
    plt.yticks(
        [int(nYv * (b / 8)) for b in range(0, 9)],
        [round_sig(nYv * dy * (a / 8) * 1e3) for a in range(-4, 5)],
    )
    plt.xticks(
        [int(nXv * (b / 8)) for b in range(0, 9)],
        [round_sig(nXv * dy * (a / 8) * 1e3) for a in range(-4, 5)],
    )
    plt.xlabel("($y_1 - y_2$) [mm]")
    plt.ylabel("($y_1 - y_2$) [mm]")
    plt.colorbar()
    plt.show()

    plt.clf()
    plt.close()
    #    plt.plot(IH/np.max(IH), label="Horizontal cut Intensity")
    #    plt.plot(IV/np.max(IV), label="Vertical cut Intensity")
    plt.plot(jHh / np.max(jHh), label="horizontal cut")
    plt.plot(jHv / np.max(jHv), label="vertical cut")
    plt.plot(
        jHd / np.max(jHd), label="diagonal cut"
    )  # label="Horizontal Mutual Intensity")
    plt.title("horizontal coherence")
    plt.legend()
    plt.show()

    plt.clf()
    plt.close()
    plt.plot(jVh / np.max(jVh), label="horizontal cut")
    plt.plot(jVv / np.max(jVv), label="vertical cut")
    plt.plot(
        jVd / np.max(jVd), label="diagonal cut"
    )  # label="Vertical Mutual Intensity")
    plt.title("vertical coherence")
    plt.legend()
    plt.show()

    plt.clf()
    plt.close()
    plt.plot(cH / np.max(cH), label="Horizontal Coherence Profile")
    plt.plot(cV / np.max(cV), label="Vertical Coherence Profile")
    plt.xlabel("Point Separation x-x' [pixels]")  # [\u03bcm]")
    plt.ylabel("Degree of Coherence")
    plt.legend()
    if pathCP != None:
        print("Saving Coherence profiles to: {}".format(pathCP))
        plt.savefig(pathCP)
    plt.show()
    plt.clf()

    fx = np.max(abs(j_H))
    fy = np.max(abs(j_V))

    return cH, cV, J_H, J_V, jHh, jVh, jHd2, jVd2, fx, fy


# %%
def getCoherenceLength(minC, dx=1, dy=1, cH=None, cV=None, pathCL=None):
    """
    Calculates the horizontal and vertical coherence length from coherence profiles
    params:
    minC: Minimum coherence value to define coherence length
    cH: Horizontal coherence profile
    cV: Vertical coherence profile
    pathCL: Save path for coherence plot

    returns:
    clX: Horizontal coherence length
    clY: Vertical coherence length
    """

    print(" ")
    print("-----Finding Spatial Coherence Length-----")
    try:
        if cH.any() != False:
            x = np.arange(0, (np.shape(cH)[0]))
    except AttributeError:
        pass
    try:
        if cV.any() != False:
            x = np.arange(0, (np.shape(cV)[0]))
    except AttributeError:
        pass

    # print('x: ', x)
    try:
        if cH.any() != False:
            clX = len(cH[cH > minC])
            print("Horizontal Coherence Length [pixels]: {}".format(clX))
    except AttributeError:
        pass
    try:
        if cV.any() != False:
            clY = len(cV[cV > minC])
            print("Vertical Coherence Length [pixels]: {}".format(clY))
    except AttributeError:
        pass

    plt.clf()
    plt.close()
    fig, axs = plt.subplots(1, 2)
    try:
        if cH.any() != False:
            axs[0].plot(x, cH, label="Horizontal")
            axs[0].axvline(
                x=len(cH) // 2 - clX / 2, linestyle=":", color="red", label="C length"
            )
            axs[0].axvline(x=len(cH) // 2 + clX / 2, linestyle=":", color="red")
            #            for ax in fig.axes:
            axs[0].set_xticks([int(len(x) * (a / 5)) for a in range(0, 6)])
            axs[0].set_xticklabels(
                [round_sig(int(len(x) * (a / 5)) * dx) for a in range(0, 6)]
            )
            axs[1].plot(x, cH, label="Horizontal")
            axs[1].axvline(
                x=len(cH) // 2 - clX / 2, linestyle=":", color="red", label="C length"
            )
            axs[1].axvline(x=len(cH) // 2 + clX / 2, linestyle=":", color="red")
            axs[1].set_xticks([int(len(x) * (a / 10)) for a in range(0, 11)])
            axs[1].set_xticklabels(
                [round_sig(int(len(x) * (a / 10)) * dx) for a in range(0, 11)]
            )
            axs[1].set_xlim([(len(x) / 2) - np.max(clX), (len(x) / 2) + np.max(clX)])
    except AttributeError:
        pass
    try:
        if cV.any() != False:
            axs[0].plot(x, cV, "-", label="Vertical")
            axs[0].axvline(
                x=len(cV) // 2 - clY / 2, linestyle=":", color="red", label="C length"
            )
            axs[0].axvline(x=len(cV) // 2 + clY / 2, linestyle=":", color="red")
            axs[1].plot(x, cV, "-", label="Vertical")
            #            for ax in fig.axes:
            axs[0].set_xticks([int(len(x) * (a / 5)) for a in range(0, 6)])
            axs[0].set_xticklabels(
                [round_sig(int(len(x) * (a / 5)) * dy) for a in range(0, 6)]
            )
            axs[1].axvline(
                x=len(cV) // 2 - clY / 2, linestyle=":", color="red", label="C length"
            )
            axs[1].axvline(x=len(cV) // 2 + clY / 2, linestyle=":", color="red")
            axs[1].set_xlim([(len(x) / 2) - np.max(clY), (len(x) / 2) + np.max(clY)])
            axs[1].set_xticks([int(len(x) * (a / 10)) for a in range(0, 11)])
            axs[1].set_xticklabels(
                [round_sig(int(len(x) * (a / 10)) * dy) for a in range(0, 11)]
            )
    except AttributeError:
        pass
    try:
        if cH.any() and cV.any() != False:
            axs[1].set_xlim(
                [(len(x) / 2) - np.max([clX, clY]), (len(x) / 2) + np.max([clX, clY])]
            )
    except AttributeError:
        pass
    plt.legend()
    if pathCL != None:
        print("Saving Coherence Profile plot to: {}".format(pathCL))
        plt.savefig(pathCL)
    plt.show()
    plt.clf()
    plt.close()

    try:
        return clX, clY
    except UnboundLocalError:
        try:
            return clX
        except UnboundLocalError:
            try:
                return clY
            except UnboundLocalError:
                pass


# %%
def mutualIntensity(
    cfrT, cfrH, cfrV, Fx, Fy, dx=None, dy=None, pathJP=None, pathJ=None
):
    print("----Starting Mutual Intensity Function---")

    #    print("Converting to complex wavefields and extracting each polarisation component")
    #    start1 = time.time()
    #    cfrT = getComplex(cfr, polarization = "total")
    #    cfrH = getComplex(cfr, polarization = "horizontal")
    #    cfrV = getComplex(cfr, polarization = "vertical")
    #    end1 = time.time()
    #    print('Time taken to convert to complex wavefield (s): {}'.format(end1 - start1))

    """ Taking sample area at centre of each complex wavefield array """
    A_T = sampleField(cfrT, Fx=Fx, Fy=Fy, Limit=1000)
    A_H = sampleField(cfrH, Fx=Fx, Fy=Fy, Limit=1000)
    A_V = sampleField(cfrV, Fx=Fx, Fy=Fy, Limit=1000)

    I = sampleField(
        cfrT.conjugate() * cfrT, Fx=Fx, Fy=Fy, Limit=1000
    )  # sampleField(cfr.get_intensity(), Fx=Fx, Fy=Fy, Limit=200)

    """ Finding number of points in each line profile """
    try:
        Anumx = int(np.max(np.shape(A_T[:, 0, 0])))  # These are in pixels
        Anumy = int(np.max(np.shape(A_T[0, :, 0])))
    except IndexError:
        Anumx = int(np.max(np.shape(A_T[:, 0])))  # These are in pixels
        Anumy = int(np.max(np.shape(A_T[0, :])))

    AmidX = int(Anumx / 2)  # centre pixel in horizontal line profile
    AmidY = int(Anumy / 2)  # centre pixel in vertical line profile

    """ Taking line profiles through each array """
    A_Tx = A_T[:, AmidY]
    A_Ty = A_T[AmidX, :]
    A_Hx = A_H[:, AmidY]
    A_Hy = A_H[AmidX, :]
    A_Vx = A_V[:, AmidY]
    A_Vy = A_V[AmidX, :]

    """ Mutual Intensity Functions (J, Jxx, Jxy, Jyx, Jyy) """
    ### Convolution using for loop ###
    print(" ")
    print("-----Calculating Mutual Intensity arrays-----")
    start2 = time.time()
    J = np.array([A_T.conjugate() * a for a in A_T.flatten()])  # eq.2.3.1.3
    Jxx = np.array([A_H.conjugate() * a for a in A_H.flatten()])  # eq.2.3.1.5
    Jxy = np.array([A_H.conjugate() * a for a in A_V.flatten()])  # eq.2.3.1.5
    Jyx = np.array([A_V.conjugate() * a for a in A_H.flatten()])  # eq.2.3.1.5
    Jyy = np.array([A_V.conjugate() * a for a in A_V.flatten()])  # eq.2.3.1.5
    end2 = time.time()
    print(
        "Time taken to calculate Mutual Intensity Functions [J] (s): {}".format(
            end2 - start2
        )
    )

    print("Shape of each Mutual Intensity array:")
    print("J: {}".format(np.shape(J)))
    print("Jxx: {}".format(np.shape(Jxx)))
    print("Jxy: {}".format(np.shape(Jxy)))
    print("Jyx: {}".format(np.shape(Jyx)))
    print("Jyy: {}".format(np.shape(Jyy)))

    """ Averaging each Mutual Intensity Array (& Normalising J)"""
    j = abs(J.mean(0)) / I
    jxx = abs(Jxx.mean(0))
    jxy = abs(Jxy.mean(0))
    jyx = abs(Jyx.mean(0))
    jyy = abs(Jyy.mean(0))

    # print("Shape of each Mutual Intensity array:")
    # print("A_T: {}".format(np.shape(A_T)))
    # print("A_H: {}".format(np.shape(A_H)))
    # print("A_V: {}".format(np.shape(A_V)))
    # print("I: {}".format(np.shape(I)))
    A_Ts = np.squeeze(A_T)
    A_Hs = np.squeeze(A_H)
    A_Vs = np.squeeze(A_V)

    ### Convolution using scipy.signal.convolve2d ###
    from scipy import signal

    # print(" ")
    # print("-----Calculating Mutual Intensity arrays-----")
    # J = signal.convolve2d(A_Ts, A_Ts, boundary='symm', mode='same')
    # Jxx = signal.convolve2d(A_Hs, A_Hs, boundary='symm', mode='same')
    # Jxy = signal.convolve2d(A_Hs, A_Vs, boundary='symm', mode='same')
    # Jyx = signal.convolve2d(A_Vs, A_Hs, boundary='symm', mode='same')
    # Jyy = signal.convolve2d(A_Vs, A_Vs, boundary='symm', mode='same')

    # j = J/np.squeeze(I)#abs(J)/np.squeeze(I)            # Eq. 2.3.1.4
    # jxx = Jxx/np.squeeze(I) #abs(Jxx)/np.squeeze(I)     # Eq. 2.3.1.4
    # jxy = Jxy/np.squeeze(I) #abs(Jxy)/np.squeeze(I)     # Eq. 2.3.1.4
    # jyx = Jyx/np.squeeze(I) #abs(Jyx)/np.squeeze(I)     # Eq. 2.3.1.4
    # jyy = Jyy/np.squeeze(I) #abs(Jyy)/np.squeeze(I)     # Eq. 2.3.1.4

    """ Getting pixel dimensions """
    if dx != None:
        Dx = dx
    else:
        Dx = cfr.params.Mesh.xMax - cfr.params.Mesh.xMin
    if dy != None:
        Dy = dy
    else:
        Dy = cfr.params.Mesh.yMax - cfr.params.Mesh.yMin

    """ Creating array of custom tick markers for plotting """
    tickAx = [
        round_sig(-Dx * 1e6 / 2),
        round_sig(-Dx * 1e6 / 4),
        0,
        round_sig(Dx * 1e6 / 4),
        round_sig(Dx * 1e6 / 2),
    ]
    tickAy = [
        round_sig(Dy * 1e6 / 2),
        round_sig(Dy * 1e6 / 4),
        0,
        round_sig(-Dy * 1e6 / 4),
        round_sig(-Dy * 1e6 / 2),
    ]

    plt.close()
    jmin = np.min([abs(jxx), abs(jxy), abs(jyx), abs(jyy)])
    jmax = np.max([abs(jxx), abs(jxy), abs(jyx), abs(jyy)])
    fig, axs = plt.subplots(2, 2)
    im = axs[0, 0].imshow(abs(jxx), vmin=jmin, vmax=jmax)
    axs[0, 0].set_title("Jxx")
    axs[0, 1].imshow(abs(jxy), vmin=jmin, vmax=jmax)
    axs[0, 1].set_title("Jxy")
    axs[1, 0].imshow(abs(jyx), vmin=jmin, vmax=jmax)
    axs[1, 0].set_title("Jyx")
    axs[1, 1].imshow(abs(jyy), vmin=jmin, vmax=jmax)
    axs[1, 1].set_title("Jyy")

    # from mpl_toolkits.axes_grid1 import make_axes_locatable
    # divider = make_axes_locatable(axs)
    # cax = divider.append_axes('right', size='5%', pad=0.05)
    # fig.colorbar(im, cax=cax, orientation='vertical')

    for ax in axs.flat:
        # ax.set(xticks(np.arange(0,Anumx+1,Anumx/4),tickAx), yticks(np.arange(0,Anumy+1,Anumy/4),tickAy))
        ax.set(
            xlabel="x - position [pixels]", ylabel="y - position [pixels] "
        )  # [\u03bcm]
    # Hide x labels and tick labels for top plots and y ticks for right plots.
    for ax in axs.flat:
        ax.label_outer()
    fig.subplots_adjust(right=0.8)
    cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
    fig.colorbar(im, cax=cbar_ax)
    if pathJP != None:
        print("Saving Mutual Intensity Plots to: {}".format(pathJP))
        plt.savefig(pathJP)
    plt.show()
    plt.clf()

    plt.imshow(abs(j))
    plt.title("Mututal Intensity - J")
    plt.xticks(np.arange(0, Anumx + 1, Anumx / 4), tickAx)
    plt.yticks(np.arange(0, Anumy + 1, Anumy / 4), tickAy)
    plt.xlabel("Point Separation x-x'[\u03bcm]")
    plt.ylabel("Point Separation y-y'[\u03bcm]")
    plt.colorbar()
    if pathJ != None:
        print("Saving Mutual Intensity to: {}".format(pathJ))
        plt.savefig(pathJ)
    plt.show()
    plt.clf()

    print(" ")
    print("-----Getting Stokes Parameters and Degree of Polarisation from J-----")
    #    path ='/data/YDStest/13nm/'
    #    extra = "_200nm"
    #    pathSJ = path + "Stokes" + extra + ".png" # Save path for Stokes plot
    #    pathP = path + "Polarisation" + extra + ".png" # Save path for degree of Polarisation plot

    s0, s1, s2, s3 = stokesFromJ(jxx, jxy, jyx, jyy)  # ,pathSJ, pathP)

    return j, jxx, jxy, jyx, jyy, s0, s1, s2, s3


# %%
def stokesFromJ(Jxx, Jxy, Jyx, Jyy, pathSJ=None, pathP=None):
    """
    Function to calculate and plot the 2 point Stokes parameters from the elements of the 2x2 J matrix.
    Also plots the degree of polarisation P for every point.
    Jxx, Jxy, Jyx, Jyy : elements of the Mutual Intensity matrix

    """
    J = np.array([[Jxx, Jxy], [Jyx, Jyy]])  # Eq. 2.3.1.4
    print("Shape of J: {}".format(np.shape(J)))

    import cmath

    """ Getting Stokes Parameters """
    S0 = abs(Jxx) + abs(Jyy)  # Eq. 2.3.2.3.1
    S1 = abs(Jxx) - abs(Jyy)  # Eq. 2.3.2.3.2
    S2 = abs(Jxy) + abs(Jyx)  # Eq. 2.3.2.3.3
    S3 = abs(cmath.sqrt(-1) * (Jxy)) - abs(cmath.sqrt(-1) * (Jyx))  # Eq. 2.3.2.3.4
    # cmath.sqrt(-1)*(Jxy - Jyx)

    """ Normalising """
    s0 = S0 / S0
    s1 = S1 / S0
    s2 = S2 / S0
    s3 = S3 / S0

    """ Plotting Stokes Parameters """
    plt.close()
    smin = np.min([S0, S1, S2, S3])
    smax = np.max([S0, S1, S2, S3])
    fig, axs = plt.subplots(2, 2)
    plt.title("Stokes Parameters")
    im = axs[0, 0].imshow(S0, vmin=smin, vmax=smax)
    axs[0, 0].set_title("S0")
    axs[0, 1].imshow(S1, vmin=smin, vmax=smax)
    axs[0, 1].set_title("S1")
    axs[1, 0].imshow(S2, vmin=smin, vmax=smax)
    axs[1, 0].set_title("S2")
    axs[1, 1].imshow(S3, vmin=smin, vmax=smax)
    axs[1, 1].set_title("S3")

    for ax in axs.flat:
        ax.set(xlabel="x", ylabel="y")
    # Hide x labels and tick labels for top plots and y ticks for right plots.
    for ax in axs.flat:
        ax.label_outer()
    fig.subplots_adjust(right=0.8)
    cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
    fig.colorbar(im, cax=cbar_ax)
    if pathSJ != None:
        print("Saving Stokes Plots to: {}".format(pathSJ))
        plt.savefig(pathSJ)
    plt.show()
    plt.clf()

    """ Plotting Normalised Stokes Parameters """
    plt.close()
    smin = np.min([s0, s1, s2, s3])
    smax = np.max([s0, s1, s2, s3])
    fig, axs = plt.subplots(2, 2)

    plt.title("Normalised Stokes Parameters")
    im = axs[0, 0].imshow(s0, vmin=smin, vmax=smax)
    axs[0, 0].set_title("s0")
    axs[0, 1].imshow(s1, vmin=smin, vmax=smax)
    axs[0, 1].set_title("s1")
    axs[1, 0].imshow(s2, vmin=smin, vmax=smax)
    axs[1, 0].set_title("s2")
    axs[1, 1].imshow(s3, vmin=smin, vmax=smax)
    axs[1, 1].set_title("s3")
    for ax in axs.flat:
        ax.set(xlabel="x", ylabel="y")
    # Hide x labels and tick labels for top plots and y ticks for right plots.
    for ax in axs.flat:
        ax.label_outer()
    fig.subplots_adjust(right=0.8)
    cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
    fig.colorbar(im, cax=cbar_ax)
    plt.show()
    plt.clf()

    """ Getting Degree of Polarisation """
    detJ = Jxx * Jyy - Jxy * Jyx  # np.linalg.det(J)
    P = (1 - ((4 * detJ) / ((Jxx + Jyy) ** 2))) ** (1 / 2)  # Eq. 2.3.2.3.5

    plt.imshow(abs(P))
    plt.title("Degree of Polarisation")
    plt.colorbar()
    if pathP != None:
        print("Saving degree of polarisation plot to: {}".format(pathP))
        plt.savefig(pathP)
    plt.show()
    plt.clf()

    return S0, S1, S2, S3


# %%


def getComplex(w, polarization=None):
    """
    Give the complex representation of a wavefield
    Parameters
    ----------
    w:
        scalar wavefield
    polarization:
        polarization component of wavefield to extract. Can be "total", "horizontal" or "vertical".
    returns:
        cwf: complex wavefield
    """

    re = w.get_real_part(polarization=polarization)  # get real part of wavefield
    im = w.get_imag_part(polarization=polarization)  # get imaginary part of wavefield

    print("Shape of real part of wavefield: {}".format(np.shape(re)))
    print("Shape of imaginary part of wavefield: {}".format(np.shape(im)))

    # print("real part:")
    # print(re)
    # print("imaginary part:")
    # print(im)

    cwf = re + im * 1j

    print("Shape of complex wavefield: {}".format(np.shape(cwf)))
    print("Polarization of complex wavefield: {}".format(polarization))
    # print("Complex Wavefield:")
    # print(cwf)

    return cwf


# %%
def fromPickle(path, wavefront=False):
    import pickle

    with open(path, "rb") as wav:
        w = pickle.load(wav)

    if wavefront != False:
        w = Wavefront(srwl_wavefront=w)

    return w


# %%
def sampleField(A, Fx, Fy, Limit=75):
    """
    Parameters
    ----------
    A : 2D array
        Wavefield to be sampled.
    Fx :
        Fraction of array to be sampled in horizontal.
    Fy :
        Fraction of array to be sampled in vertical.
    Limit:
        Maximum number of pixels allowed in any dimension
    Returns
    -------
    B:
        2D array sampled from centre of A.

    """

    import matplotlib.patches as patches

    print("-----Sampling middle part of wavefield-----")
    Ax = np.shape(A)[0]
    Ay = np.shape(A)[1]
    print("Original size of wavefield [pixels]: {}".format((Ax, Ay)))

    Sx = Fx * Ax
    Sy = Fy * Ay
    print("Sampled area size (pixels): {}".format([Sx, Sy]))

    if Sx > Limit or Sy > Limit:
        print(
            "Error: Sampled area of wavefront is too large. Change Fx/Fy to a smaller value"
        )
        import sys

        sys.exit()

    _x0 = 0  # These are in _pixel_ coordinates!!
    _y0 = 0
    try:
        _x1 = int(np.max(np.shape(A[:, 0, 0])))  # These are in _pixel_ coordinates!!
        _y1 = int(np.max(np.shape(A[0, :, 0])))
    except IndexError:
        _x1 = int(np.max(np.shape(A[:, 0])))  # These are in _pixel_ coordinates!!
        _y1 = int(np.max(np.shape(A[0, :])))

    print("Nx (pixels): {}".format(_x1))
    print("Ny (pixels): {}".format(_y1))

    numx = _x1 - _x0  # number of points for line profile
    numy = _y1 - _y0
    midX = int(numx / 2)
    midY = int(numy / 2)

    print("mid x: {}".format(midX))
    print("mid y: {}".format(midY))

    ROI = (
        (int(midX - ((Fx) * midX)), int(midY - ((Fy) * midY))),
        (int(midX + ((Fx) * midX)), int(midY + ((Fy) * midY))),
    )

    print("Region of interest (pixels): {}".format(ROI))

    x0, y0 = ROI[0][0], ROI[0][1]
    x1, y1 = ROI[1][0], ROI[1][1]

    lX = ROI[1][0] - ROI[0][0]
    lY = ROI[1][1] - ROI[0][1]

    I = abs(A.conjugate() * A)
    figure, ax = plt.subplots(1)
    rect = patches.Rectangle((x0, x0), lX, lY, edgecolor="r", facecolor="none")

    plt.imshow(I)
    ax.add_patch(rect)
    plt.title("Original Wavefield with Sampled Area")
    plt.show()
    plt.clf()
    plt.close()

    B = A[y0:y1, x0:x1]

    return B


def get_coherence_len(wfr, dx, dy, VERBOSE=True):
    """
    Calculate coherence length of a complex wavefield of shape
    [nx, ny. nz]

    :param wfr: complex wavefield
    :param dx: horizontal pixel size
    :param dy: vertical pixel size

    :returns Jd: complex degree of coherence
    :returns clen: coherence length [m]
    """

    profile = wfr  # [int(np.shape(wfr)[0]/2),:]
    nt = wfr.shape[0]  # [-1]

    J = np.dot(profile, profile.T.conjugate()) / nt
    II = np.abs(np.diag(J))  # intensity as the main diagonal

    #    J /= II**0.5 * II[:, np.newaxis]**0.5
    Jd = np.abs(np.diag(np.fliplr(J)))  # DoC as the cross-diagonal

    lm = np.arange(Jd.shape[0])

    lm = lm[(lm >= Jd.shape[0] // 2) & (Jd[lm] < 0.5)]

    rstep = np.sqrt((dx) ** 2 + (dy) ** 2)

    plt.imshow(abs(J))
    plt.title("from trey script")
    plt.colorbar()
    plt.show()

    plt.plot(Jd, label="DoC")
    plt.plot(II, label="I")
    plt.legend()
    plt.show()

    try:
        lm = lm[0] - Jd.shape[0] // 2
    except IndexError:
        lm = np.inf

    clen = lm * rstep

    if VERBOSE:
        print("Radial Coherence Length: {:.2f} um".format(clen * 1e6))
    return clen


# %%
def test():
    eMin = 50e6
    Nx = 75
    Ny = 75
    Nz = 1
    xMin = -10e-6
    xMax = 10e-6
    yMin = -10e-6
    yMax = 10e-6
    zMin = 100
    Fx = 1 / 8
    Fy = 1 / 8
    print("Running Test:")
    print("building wavefront...")
    w = build_gauss_wavefront(
        Nx, Ny, Nz, eMin / 1000, xMin, xMax, yMin, yMax, 1, 1e-6, 1e-6, 1
    )

    wf0 = Wavefront(srwl_wavefront=w)

    # wf = wf0.toComplex()

    """From pickled wavefield """
    path = "/home/jerome/Documents/MASTERS/data/YDStest/13nm/"  # wavefieldME_TEST_500um_.pkl' #'/home/jerome/dev/wavefieldME_TEST_500um_.pkl'
    waveName = path + "wavefieldME_TEST_50um_.pkl"
    print("-----Loading Wavefield-----")
    wf = fromPickle(waveName, True)
    extra = "_200nm"
    pathI = (
        path + "Intensity" + extra + ".png"
    )  # Save path for horizontal coherence profile plot
    pathCpX = (
        path + "CpX" + extra + ".png"
    )  # Save path for horizontal coherence profile plot
    pathCpY = (
        path + "CpY" + extra + ".png"
    )  # Save path for vertical coherence profile plot
    pathWX = (
        path + "WX" + extra + ".png"
    )  # Save path for horizontal complex wavefield plot
    pathWY = (
        path + "WY" + extra + ".png"
    )  # Save path for vertical complex wavefield plot

    pathCP = (
        path + "CoherenceProfile" + extra + ".png"
    )  # Save path for horizontal/vertical mutual intensity profiles
    pathJP = (
        path + "MutualIntensityPlots" + extra + ".png"
    )  # Save path for Mutual Intensity plots
    pathJ = path + "MutualIntensity" + extra + ".png"  # Save path for Mutual Intensity

    """Coherence from pyplot """
    # coherenceProfiles(wf,
    #                  pathI, pathCpX, pathCpY, pathWX, pathWY)

    cw = getComplex(wf)
    I = wf.get_intensity()
    cX = cw[:, int(int(np.max(np.shape(cw[:, 0, 0]))) / 2)]
    cY = cw[int(int(np.max(np.shape(cw[0, :, 0]))) / 2), :]
    Ix = I[:, int(int(np.max(np.shape(I[:, 0, 0]))) / 2)]
    Iy = I[int(int(np.max(np.shape(I[0, :, 0]))) / 2), :]

    """Mutual Intensity """
    profileMI(cX, cY, Ix, Iy)
    mutualIntensity(wf, Fx, Fy)  # , pathCP, pathJP, pathJ)


# %%
def testComplex():
    path = "wavefield_1.pkl"

    import pickle

    with open(path, "rb") as wav:
        w = pickle.load(wav)

    wc = Wavefront(srwl_wavefront=w)
    getComplex(wc)
    print(" ")


# %%
def testCoherenceProfile():
    import imageio

    save = False

    justHor = False
    gx = 40e-6
    gy = 10e-6
    # path = 'wavefield_1.pkl'
    path = "/home/jerome/dev/data/correctedCoherence/"
    # slit sizes]
    sX = [
        100,
        200,
        300,
    ]  # ,350,400,500]#,750,1000] #[100,200,300,350,300,500,750,1000] #,400,500,750,1000]
    sY = [
        250,
        250,
        250,
    ]  # ,125,125,125]#,150,250,200,250,350,500] #[125,125,125,125,250,125,350,500]#,125,125,350,500]

    cdx100, cdy100 = 1.9145603288612563e-06, 1.744394036324584e-06
    cdx150, cdy150 = 1.9487510862889527e-06, 1.74502888218383e-06
    cdx200, cdy200 = 1.9944689868343538e-06, 1.742897255839409e-06
    cdx250, cdy250 = 2.0296997983770577e-06, 1.7427838524854241e-06
    cdx300, cdy300 = 3.37365690229677e-07, 2.787347002816151e-06

    # resolution of each electric field
    # dx125,dy100 = 2.4689055387588117e-06, 5.310613400205268e-07# good
    # dx150, dy150 = 2.478226023383787e-06, 1.1160332083797564e-06# good
    # dx250, dy200 = 2.5342967535507866e-06, 1.8061040812635488e-06# good
    # dx200, dy250 = 2.509446544260192e-06, 2.3886004028860022e-06# good
    # dx325, dy325 = 2.56251722643114e-06, 2.880625541834018e-06# good
    dx100, dyX100 = 2.4633703639094306e-06, 2.406360648168151e-06  # good
    dx200, dyX200 = 2.509768682470555e-06, 2.3936707460080324e-06
    dx500, dyX500 = 2.704305789676536e-06, 2.39402783274347e-06
    dx300, dy125 = 2.5520841887378355e-06, 2.3949861313413743e-06
    # dx300_, dy250_ = 2.551639150787167e-06, 7.167414781137508e-06 # good
    dx350, dy125__ = 2.5780978476807674e-06, 2.394476584601917e-06
    dx400, dy125_ = 2.6154271212479892e-06, 2.3941822674748382e-06
    # dx750, dy350 = 2.8223103191715313e-06, 8.711028596736527e-06# good
    # dx1000, dy500 = 2.8472368922886252e-06, 8.798292839349388e-06# good

    dx = [cdx100, cdx200, cdx300]
    # [dx100,dx200,dx300]#,dx350,dx400,dx500]
    # [dx100,dx125,dx150,dx200,dx250,dx300_,dx750,dx1000] #dx100,dx200,dx300,dx350,dx300_,dx500,dx750,dx1000 #,dx400,dx500,dx750.dx1000
    # 2.4633703639094306e-06, 2.509768682470555e-06, 2.551639150787167e-06, 2.6154271212479892e-06, 2.704305789676536e-06, 2.8223103191715313e-06, 2.8472368922886252e-06
    dy = [cdy100, cdy200, cdy300]
    # [dyX100,dyX200,dy125]#,dy125__,dy125_,dyX500]
    # [dyX100,dy100,dy150,dy250,dy200,dy250_,dy350,dy500] #dyX100,dyX200,dy125,dy125__,dy250,dy125_,dy350,dy500
    # 2.406360648168151e-06, 2.3936707460080324e-06, 7.167414781137508e-06, 2.3941822674748382e-06, 2.39402783274347e-06, 8.711028596736527e-06,  8.798292839349388e-06

    if justHor:
        EhR = [
            imageio.imread(path + "beforeBDA_efield_sx" + str(s) + "ExReal.tif")
            for s in sX
        ]
        EvR = [
            imageio.imread(path + "beforeBDA_efield_sx" + str(s) + "EyReal.tif")
            for s in sX
        ]
        EhI = [
            imageio.imread(path + "beforeBDA_efield_sx" + str(s) + "ExIm.tif")
            for s in sX
        ]
        EvI = [
            imageio.imread(path + "beforeBDA_efield_sx" + str(s) + "EyIm.tif")
            for s in sX
        ]
    else:
        EhR = [
            imageio.imread(
                path + "beforeBDA_efield_sx" + str(s) + "sy" + str(y) + "ExReal.tif"
            )
            for s, y in zip(sX, sY)
        ]
        EvR = [
            imageio.imread(
                path + "beforeBDA_efield_sx" + str(s) + "sy" + str(y) + "EyReal.tif"
            )
            for s, y in zip(sX, sY)
        ]
        EhI = [
            imageio.imread(
                path + "beforeBDA_efield_sx" + str(s) + "sy" + str(y) + "ExIm.tif"
            )
            for s, y in zip(sX, sY)
        ]
        EvI = [
            imageio.imread(
                path + "beforeBDA_efield_sx" + str(s) + "sy" + str(y) + "EyIm.tif"
            )
            for s, y in zip(sX, sY)
        ]

    print(np.shape(EhR))
    print(np.shape(EvR))
    print(np.shape(EhI))
    print(np.shape(EvI))

    # method 3
    Eh = [ExR + ExI * 1j for ExR, ExI in zip(EhR, EhI)]
    Ev = [EyR + EyI * 1j for EyR, EyI in zip(EvR, EvI)]  # EvR + EvI*1j
    cE = [Ex + Ey for Ex, Ey in zip(Eh, Ev)]  # Eh + Ev

    # empty lists for coherence lengths
    cLx = []
    cLy = []
    cLx2 = []
    cLy2 = []
    cLx3 = []
    cLy3 = []
    cLx4 = []
    cLy4 = []
    cL = []
    mIx = []
    mIy = []
    totIx = []
    totIy = []
    ImTOT = []

    print("shape of cE: ", np.shape(cE))

    for ce, ch, cv, s, dX, dY in zip(cE, Eh, Ev, sX, dx, dy):
        I = abs(ce.conjugate() * ce)
        ex = ce[int(np.shape(ce)[0] / 2), :]
        ey = ce[:, int(np.shape(ce)[1] / 2)]
        Ix = I[int(np.shape(I)[0] / 2), :]
        Iy = I[:, int(np.shape(I)[1] / 2)]

        #        J,Jxx,Jxy,Jyx,Jyy,S0,S1,S2,S3 = mutualIntensity(ce,ch,cv,Fx=0.1,Fy=0.1,dx=dx300,dy=dy250)

        p = int((gx * gy) / (dX * dY))
        px = int(gx / dX)
        py = int(gy / dY)
        print("resolution (x,y): ", (dX, dY))
        print("number of pixels for mask x profile: ", px)
        print("number of pixels for mask y profile: ", py)
        print("total number of pixels for mask area: ", p)

        # Im = I[int(np.shape(I)[0]/2)-int(px/2):int(np.shape(I)[0]/2)+int(px/2),int(np.shape(I)[1]/2)-int(py/2):int(np.shape(I)[1]/2)+int(py/2)]

        # print("shape of Im: ", np.shape(Im))
        # plt.imshow(Im, aspect ='auto')
        # plt.title('intensity over mask')
        # plt.show()

        _c = 299792458
        epsilon = 8.854187817e-12

        Imtot_w = I * (_c / 2 * epsilon)  # W/m^2
        ITOT = Imtot_w * (1 / 1.602e-19) * (1 / 185) * 0.0001

        Imtot = np.sum(ITOT * dX * dY)

        # print(np.shape(ex))
        cH, cV, jH, jV, jHh, jVh, jHd, jVd, fx, fy = profileMI(
            ex, ey, Ix, Iy, dx=dX, dy=dY
        )

        # Cx = getCoherenceFromProfile(ex)
        # Cy = getCoherenceFromProfile(ey)

        # plt.plot(ex, label='horizontal cut (y=0)')
        # plt.plot(ey, label='vertical cut (x=0)')
        # plt.ylabel('e-field amplitude')
        # plt.legend()
        # plt.show()

        fig, axs = plt.subplots(2, 1)
        # axs[0].plot(Cx, label='horizontal coherence')
        axs[0].plot(Ix / np.max(Ix), label="normalised intensity (y=0)")
        axs[0].plot(cH, label="horizontal coherence")
        # # axs[0].plot(jHd/np.max(jHd), label='normalised intensity (y=0) - from MI')
        # # axs[1].plot(Cy, label='vertical coherence')
        # axs[1].plot(Iy/np.max(Iy), label='normalised intensity (x=0)')
        # axs[1].plot(cV, label='vertical coherence')
        # # axs[1].plot(jVd/np.max(jVd), label='normalised intensity (x=0) - from MI')
        axs[0].set_ylabel("Horiztonal Coherence")
        axs[0].legend()
        axs[1].set_ylabel("Vertical Coherence")
        axs[1].legend()
        # for ax in fig.axes:
        axs[0].set_xticks([int(len(cH) * (a / 4)) for a in range(0, 5)])
        axs[0].set_xticklabels(
            [round_sig(int((len(cH)) * (a / 4)) * dX * 1e3) for a in [-2, -1, 0, 1, 2]]
        )
        axs[1].set_xticks([int(len(cV) * (a / 4)) for a in range(0, 5)])
        axs[1].set_xticklabels(
            [round_sig(int((len(cV)) * (a / 4)) * dY * 1e3) for a in [-2, -1, 0, 1, 2]]
        )
        # plt.yticks([int(nYh*(b/8)) for b in range(0,9)],
        #            [round_sig(nYh*dx*(a/8)*1e3) for a in range(-4,5)])
        # plt.xticks([int(nXh*(b/8)) for b in range(0,9)],
        #            [round_sig(nXh*dx*(a/8)*1e3) for a in range(-4,5)])
        axs[1].set_xlabel("Position [mm]")
        plt.show()

        #    ix, iy = -0.0028130414104853107, -0.002501515125127075 #Initial Horizontal Position [m]
        #    fx, fy = 0.002811914632041884, 0.002478062766979343 #Final Horizontal Position [m]
        #

        # print(np.shape(Cx))

        # coherence length from profile
        # clx_1 = getCoherenceLength(0.8,cH = np.array(Cx),dx=dx300)*dX
        # cly_1 = getCoherenceLength(0.8,cV = np.array(Cy),dy=dy250)*dY

        # coherence length from MI function
        clx_2 = getCoherenceLength(0.8, cH=np.array(cH), dx=dX) * dX
        # cly_2 = getCoherenceLength(0.8,cV = np.array(cV),dy=dY)*dY
        # clx_3 = getCoherenceLength(0.8,cH = np.array(jHh/np.max(jHh)),dx=dx300)*dX
        # cly_3 = getCoherenceLength(0.8,cV = np.array(jVh/np.max(jVh)),dy=dy250)*dY
        # clx_4 = getCoherenceLength(0.8,cH = np.array(jHd/np.max(jHd)),dx=dx300)*dX
        # cly_4 = getCoherenceLength(0.8,cV = np.array(jVd/np.max(jVd)),dy=dy250)*dY

        sumIx = abs(np.sum(Ix))
        print("I sum: ", sumIx)
        sumIy = abs(np.sum(Iy))
        print("I sum: ", sumIy)
        # cLx.append(clx_1)
        # cLy.append(cly_1)
        cLx2.append(clx_2)
        # cLy2.append(cly_2)
        # cLx3.append(clx_3)
        # cLy3.append(cly_3)
        # cLx4.append(clx_4)
        # cLy4.append(cly_4)
        mIx.append(fx)
        mIy.append(fy)
        totIx.append(sumIx)
        totIy.append(sumIy)
        ImTOT.append(Imtot)

        #        cL.append(get_coherence_len(ce,d,d))

        if save:
            imageio.imwrite(path + str(s) + "coherenceHOR.tif", np.float32(jH))
            imageio.imwrite(path + str(s) + "coherenceVER.tif", np.float32(jV))
            #            imageio.imwrite(path + str(s) + 'mi.tif',np.float32(J))
            #            imageio.imwrite(path + str(s) + 'miXX.tif',np.float32(Jxx))
            #            imageio.imwrite(path + str(s) + 'miXY.tif',np.float32(Jxy))
            #            imageio.imwrite(path + str(s) + 'miYX.tif',np.float32(Jyx))
            #            imageio.imwrite(path + str(s) + 'miYY.tif',np.float32(Jyy))2.8223103191715313e-06, 8.711028596736527e-06
            #            imageio.imwrite(path + str(s) + 's0.tif',np.float32(S0))
            #            imageio.imwrite(path + str(s) + 's1.tif',np.float32(S1))
            #            imageio.imwrite(path + str(s) + 's2.tif',np.float32(S2))
            #            imageio.imwrite(path + str(s) + 's3.tif',np.float32(S3))
            [125, 100, 150, 250, 200, 125, 325, 350]
    print(np.shape(ImTOT))
    print(cLx)
    # print(cLy)
    # plotting all on the same plot
    ImTOT = np.squeeze(ImTOT)
    print(ImTOT)

    # fig, ax1 = plt.subplots()
    # ax2 = ax1.twinx()
    plt.plot(sX, [c * 1e6 for c in cLx2], "x", label="horizontal - profile")
    # plt.plot(sY,[c*1e6 for c in cLy2], 'x', label='vertical - profile') #[cLy[0],cLy[2],cLy[5],cLy[6]]
    # for coherence
    # plt.plot(sX[0:6],[c*1e6 for c in cLx2[0:6]], 'x', label='horizontal')#' - MI #1')
    # plt.plot([sY[0],sY[5],sY[6],sY[7]],[c*1e6 for c in [cLy2[0],cLy2[5],cLy2[6],cLy2[7]]], 'x', label='vertical')#' - MI #1') #[cLy2[0],cLy2[2],cLy2[5],cLy2[6]]

    # plt.plot(sX,[c*1e6 for c in cLx3], 'x', label='horizontal - MI #2')
    # plt.plot(sY,[c*1e6 for c in cLy3], 'x', label='vertical - MI #2') #[cLy3[0],cLy3[2],cLy3[5],cLy3[6]]
    # plt.plot(sX,[c*1e6 for c in cLx4], 'x', label='horizontal - MI #3')
    # plt.plot(sY,[c*1e6 for c in cLy4], 'x', label='vertical - MI #3') #[cLy4[0],cLy4[2],cLy4[5],cLy4[6]]
    # plt.xlabel('Slit Width [microns]')
    plt.ylabel("Coherence Length [\u03bcm]")
    plt.xlabel("SSA Width  [\u03bcm]")
    plt.legend()
    plt.show()

    # plotting separately
    # axs[0].plot(sX,[c*1e6 for c in cLx], 'x', label='profile')
    # axs[1].plot(sY,[c*1e6 for c in cLy], 'x', label='profile') #[sY[0],sY[2],sY[4],sY[5]]
    # for coherence
    # axs[0].plot(sX[0:6],[c*1e6 for c in cLx2[0:6]], 'x', label='MI #1')
    # axs[1].plot([sY[0],sY[5],sY[6],sY[7]],[c*1e6 for c in [cLy2[0],cLy2[5],cLy2[6],cLy2[7]]], 'x', label='MI #1')
    # axs[0].plot(sX,[c*1e6 for c in cLx3], 'x', label='MI #2')
    # axs[1].plot(sY,[c*1e6 for c in cLy3], 'x', label='MI #2')
    # axs[0].plot(sX,[c*1e6 for c in cLx4], 'x', label='MI #3')
    # axs[1].plot(sY,[c*1e6 for c in cLy4], 'x', label='MI #3')
    axs[0].set_xlabel("Horiztonal SSA Width  [\u03bcm]")
    axs[0].set_ylabel("Horizontal Coherence Length  [\u03bcm]")
    axs[1].set_xlabel("Vertical SSA Width  [\u03bcm]")
    axs[1].set_ylabel("Vertical Coherence Length  [\u03bcm]")
    # axs[1].legend()
    # for ax in fig.axes:
    #     ax.set_ylim(100,900)
    #     ax.set_xlim(100,751)
    fig.tight_layout()
    plt.show()


#     fig, ax1 = plt.subplots()
#     ax2 = ax1.twinx()
#     # fig, axs = plt.subplots(1,2)
#     ax0 = plt.subplot(121)
#     ax1 = ax0.twinx()
#     # ax2 = plt.subplot(122)
#     # ax3 = ax2.twinx()
#     # for coherence
#     ax0.plot(sX[0:3],[c*1e6 for c in cLx2[0:3]], ':x')
#     # ax1.plot(sX[0:6], mIx[0:6],':x',color=colours[1], label='peak I')
#     ax1.plot(sX[0:3], ImTOT[0:3],':x',color=colours[1], label='total I')
#     # for coherence
#     # ax2.plot([sY[0],sY[5],sY[6],sY[7]],[c*1e6 for c in [cLy2[0],cLy2[5],cLy2[6],cLy2[7]]], ':x', label='MI #1')
#     # ax3.plot([sY[0],sY[5],sY[6],sY[7]],[c for c in [ImTOT[0],ImTOT[5],ImTOT[6],ImTOT[7]]], ':x',color=colours[1], label='peak I')
#     # ax3.plot([sY[0],sY[5],sY[6],sY[7]],[c for c in [totIy[0],totIy[5],totIy[6],totIy[7]]], ':x',color=colours[2], label='total I')
#     ax0.set_ylabel('horizontal coherence length [\u03bcm]')
#     # ax2.set_ylabel('coherence length (ver)')
#     ax1.set_ylabel('Total Intensity [ph/s/0.1%bw]')
#     # ax3.set_ylabel('Intensity')
#     ax1.spines['left'].set_color(colours[0])
#     ax1.spines['right'].set_color(colours[1])
#     ax0.yaxis.label.set_color(colours[0])
#     ax0.tick_params(axis='y', colors=colours[0])
#     ax1.yaxis.label.set_color(colours[1])
#     ax1.tick_params(axis='y', colors=colours[1])
#     # ax2.spines['left'].set_color(colours[0])
#     # ax3.spines['right'].set_color(colours[1])
#     # ax2.yaxis.label.set_color(colours[0])
#     # ax2.tick_params(axis='y', colors=colours[0])
#     # ax3.yaxis.label.set_color(colours[1])
#     # ax3.tick_params(axis='y', colors=colours[1])
#     # ax1.legend()
#     # ax3.legend()
#     ax0.set_xlabel('Horiztonal SSA Width  [\u03bcm]')
#     fig.tight_layout()
#     plt.show()
# #    plt.plot(cL)
# #    plt.title("from trey script")
# #    plt.show()

# %%
if __name__ == "__main__":
    # test()
    testCoherenceProfile()
    # sX = [100,125,150,200,250,300] #[100,200,300,350,300,500,750,1000] #,400,500,750,1000]
    # sY = [125,100,150,250,200,125,325,350]
    # plt.plot(sX,[0.0004581868876871541, 0.00036786692527506295, 0.0003073000268995896, 0.00023337852861619784, 0.00020020944353051214, 0.00018630214577786198])
    # plt.plot(sY,[0.00036336045787339086, 0.0006287766265843037, 0.00045645758222732035, 0.0005422122914551225, 0.0006104631794670795, 0.0003376930445191338, 0.0005588413551157995, 0.00010453234316083832], 'o')
    # plt.show()
