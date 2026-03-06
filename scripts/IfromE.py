#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 15:18:49 2022

@author: jerome
"""
import numpy as np
import matplotlib.pyplot as plt
import imageio
import tifffile
import pickle


def IfromEtiffs(files, mid=None, N=1000, n=1, res=(1,1), includeSum=False):
    if mid == None:
        mid = [(int(np.shape(f)[0] / 2), int(np.shape(f)[1] / 2)) for f in files]

    EhR = [tifffile.imread(f + "ExReal.tif") for f in files]
    EvR = [tifffile.imread(f + "EyReal.tif") for f in files]
    EhI = [tifffile.imread(f + "ExIm.tif") for f in files]
    EvI = [tifffile.imread(f + "EyIm.tif") for f in files]

    imagesEhR = [t[m[0] - n : m[0] + n, m[1] - N : m[1] + N] for t, m in zip(EhR, mid)]
    imagesEvR = [t[m[0] - n : m[0] + n, m[1] - N : m[1] + N] for t, m in zip(EvR, mid)]
    imagesEhI = [t[m[0] - n : m[0] + n, m[1] - N : m[1] + N] for t, m in zip(EhI, mid)]
    imagesEvI = [t[m[0] - n : m[0] + n, m[1] - N : m[1] + N] for t, m in zip(EvI, mid)]

    # method
    Eh = [ExR + ExI * 1j for ExR, ExI in zip(imagesEhR, imagesEhI)]
    Ev = [EyR + EyI * 1j for EyR, EyI in zip(imagesEvR, imagesEvI)]  # EvR + EvI*1j
    cE = [Ex + Ey for Ex, Ey in zip(Eh, Ev)]  # Eh + Ev

    I = [abs(e.conjugate() * e) for e in cE]
    
    if includeSum:
        E3a = 0.18 #0.83 #75/100 # value of transmission through mask in Masters thesis
        E3p = 0*np.pi
        wl = 6.7e-9 # 13.5e-9 #6.7e-9
        k = (2*np.pi)/wl
        xR = N*res[0][0]
    
        x = np.linspace(-xR/2,xR/2,2*N)
    
        # Wo = 10.0e-6
        Wz = 1000.0e-6   #beam size at z (1/e^2)
        R = 15.0         #radius of curvature
        Z = 9.5          #propagation distance from waist
        ET = E3a * np.exp((-(x**2))/((Wz**2))) * np.exp(-1j * ((k*Z) + (k * ((x**2)/(2*R))) - E3p))        
        E2d = np.tile(ET,(2*n,1))
        E = cE[0] + 0.1*cE[1] + 10e4*E2d
        Isum = abs(E**2)
        plt.imshow(Isum,aspect='auto')
        plt.colorbar()
        plt.show()
        return I, Isum
    else:
        return I


def testIfromE():
    path = "/home/jerome/dev/data/correctedBlockDiffraction/"

    # res and middle pixels of images
    res = [
        (4.832552851219838e-09, 3.853038352405723e-07),
        (4.832457034313024e-09, 3.8431154968763494e-07),
    ]
    mid = [(196, 19887), (96, 7405)]

    N = 1000  # number of pixels to take for line profile  - 1200 for roughness aerial images
    n = 1  # number of pixels to average over for line profile - 15 for roughness aerial images
    plotRange = 10000  # range of aerial image plot in nm

    files = ["apertureDiffraction", "blockDiffraction"]

    fileNames = [path + f for f in files]

    I = IfromEtiffs(fileNames, mid, N, n)

    plt.imshow(I[0], aspect="auto")
    plt.show()


def testBlockApDiff():
    import plotting

    path = "/home/jerome/dev/data/correctedBlockDiffraction/"
    savePath = None #path + "allClose.png"
    titles = [
        "Single Aperture",
        "Two-Grating Mask Model",
        "Photon Block Mask Layer",
        "Summed",
    ]

    # res and middle pixels of images
    res = [
        (4.832552851219838e-09, 3.853038352405723e-07),
        (4.832457034313024e-09, 3.8431154968763494e-07),
    ]
    mid = [(196, 19887), (96, 7405)]

    N = 800  # number of pixels to take for line profile  - 1200 for roughness aerial images
    n = 1  # number of pixels to average over for line profile - 15 for roughness aerial images
    plotRange = 2000  # range of aerial image plot in nm

    files = ["apertureDiffraction", "blockDiffraction"]

    fileNames = [path + f for f in files]

    I, Isum = IfromEtiffs(fileNames, mid, N, n,res,includeSum=True)

    resAE = (2.5011882651601634e-09, 2.426754806976689e-07)
    midAE = (196, 12188)

    tiffAE = tifffile.imread(path + "imagePlaneintensity.tif")
    imageAE = tiffAE[midAE[0] - n : midAE[0] + n, midAE[1] - 2 * N : midAE[1] + 2 * N]
    profileAE = imageAE.mean(0)
    xAE = np.linspace(-2 * N * resAE[0], 2 * N * resAE[0], 4 * N)
    xP = [np.linspace(-N * r[0], N * r[0], 2 * N) for r in res]
    yP = [np.linspace(-n * r[1], n * r[1], 2 * n) for r in res]

#    Isum = I[0] + I[1]

    Itot = [I[0], imageAE, I[1], Isum]
    resTOT = [
        (4.832552851219838e-09, 3.853038352405723e-07),
        (4.832457034313024e-09, 3.8431154968763494e-07),
        (2.5011882651601634e-09, 2.426754806976689e-07),
        (4.832552851219838e-09, 3.853038352405723e-07),
    ]
    midTOT = [(196, 19887), (96, 7405), (196, 12188)]

    # 2D PLOT
    #    for i,t in enumerate(Itot):
    #        plt.imshow(t, aspect='auto')
    #        plt.show()
    #        print(resTOT[i][1])
    #        print(np.shape(t))
    #    print([r[0] for r in resTOT])
    #
    #    plotting.plotMultiTwoD(I,
    #                           dims=[3,1],
    #                           dx = [r[0] for r in resTOT],
    #                           dy = [r[1] for r in resTOT],
    #                           sF = 1e6,
    ##                            mid = midTOT,
    #                           describe = True,
    #                           title= titles, #labels[i],
    #                           xLabel= 'x-position $[\mu m]$',
    #                           yLabel= 'y-position $[\mu m]$',
    #                           aspct = 'auto',
    ##                           colour = 'gray',
    #                           cbarLabel= 'Intensity [ph/s/.1\%bw/mm²]',
    #                           savePath = savePath)#'Intensity [ph/s/.1%bw/mm²]')

    # 1D PLOT
    profs = [i.mean(0) / np.max(i) for i in Itot]

    plotting.plotOneD(
        profs,
        d=[r[0] for r in resTOT],
        sF=1e6,
        xlim=[-plotRange/2, plotRange/2],
        ylim=None,
        describe=False,
        split=None,
        customX=[x * 1e9 for x in [xP[0], xAE, xP[0], xP[0]]],
        title=None,
        labels=titles,
        xLabel=["Position [nm]"],
        yLabel=["Intensity [a.u]"],  # [ph/s/.1\%bw/mm²]'],
        aspct="auto",
        lStyle="-",
        lWidth=1,
        pStyle="",
        fSize=10,
        figSize=(10,6),
        dpi=100,
        color=[0, 1, 3, 4],
        savePath=savePath,
    )


if __name__ == "__main__":
    #    testIfromE()
    testBlockApDiff()
