#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 16:02:19 2021

@author: jerome
"""
import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage

import time
import math

try:
    from wpg.srwlib import *
except ImportError:
    pass

from math import log10, floor, sqrt
try:
    import interferenceGratingModelsJK
except ImportError:
    pass

# from plotting import plotOneD, plotTwoD, plotMultiOneD, plotMultiTwoD
from useful import round_sig, sampleField, fromPickle, getLineProfile
    # import dev.scripts.interferenceGratingModelsJK as interferenceGratingModelsJK 
    # from dev.scripts.plotting import plotOneD, plotTwoD, plotMultiOneD, plotMultiTwoD
    # from dev.scripts.useful import round_sig, sampleField, fromPickle

colours = plt.rcParams["axes.prop_cycle"].by_key()["color"]

# %%
def getCoherenceFromProfile(p, verbose=False, show=False):
    '''
    Parameters
    ----------
    p : Line profile of complex electric field

    Returns
    -------
    C: Coherence profile

    '''
    if verbose:
        print(" ")
        print("-----Calculating coherence profile-----")
        start = time.time()
    else:
        pass
    
    n = len(p)       # number of pixels in profile
    mid = int(n/2)   # mid point of profile
    C = [abs(p[mid]*a) for a in p.conjugate()] # coherence of profile with respect to mid point
    nC = [c/np.max(C) for c in C]          # normalised coherence
    
    if verbose:
        end = time.time()
        print("Time taken to generate coherence profile (s): ", (end-start))
        # print(f"Shape of coherence profile {np.shape(np.squeeze(nC))}")
    else:
        pass
    
    if show:
        plt.plot(nC)
        plt.title('Normalised Coherence Profile')
        plt.xlabel('Position')
        plt.ylabel('Coherence')
        plt.show()
    else:
        pass
    
    return nC    

# %%
def profileMI(cpX, cpY, dx=1,dy=1, pathCP=None, verbose=False, show=False):
    """
    Calculates the Horizontal and Vertical Coherence profiles from line profiles through the complex wavefield.
    params:
    cpX: Horizontal profile of complex wavefield
    cpY: Vertical profile of complex wavefield
    # Ix: Horizontal Intensity profile
    # Iy: Vertical Intensity profile
    pathCP: Save path for coherence profile plot
    returns:
    cH: Horizontal coherence profile
    cV: Vertical coherence profile
    """

    if verbose:
        print(" ")
        print("-----Calculating Mutual Intensity profiles-----")
        start3 = time.time()
        print("Shape of line profiles:")
        print("Horizontal: {}".format(np.shape(cpX)))
        print("Vertical: {}".format(np.shape(cpY)))
    else:
        pass    

    """ Mutual Intensity Profiles """    
    ### CONVOLUTION DONE USING FOR LOOP ###
    J_H = np.array([cpX.conjugate()*a for a in cpX]) # Horizontal coherence profile - Eq. 2.3.1.3 
    J_V = np.array([cpY.conjugate()*a for a in cpY]) # Vertical coherence profile - Eq. 2.3.1.3
    
    if verbose:
        end3 = time.time()
        print("Time taken to calculate Mutual Intensity profiles: {} seconds".format(end3-start3))
        print(" ")
        print("Shape of each Mutual Intensity profile:")
        print("Horizontal profile: {}".format(np.shape(J_H)))
        print("Vertical profile: {}".format(np.shape(J_V)))
    else:
        pass

    j_H = abs(J_H) #np.sqrt(J_H**2)
    j_V = abs(J_V) #np.sqrt(J_V**2) 
    
    jHd = np.diagonal(np.squeeze(J_H))           # Diagonal of matrix J_H (horizontal intensity profile)
    jVd = np.diagonal(np.squeeze(J_V))           # Diagonal of matrix J_V (vertical intensity profile)
    jHh = np.squeeze(j_H)[int(np.shape(np.squeeze(J_H))[0]/2),:]  # Horizontal cut of horizontal coherence profile (horizontal coherence)
    jVh = np.squeeze(j_V)[int(np.shape(np.squeeze(J_V))[0]/2),:]  # Horizontal cut of vertical coherence profile (vertical coherence)
    
    nXh, nYh = np.shape(j_H)
    nXv, nYv = np.shape(j_V)
    
    cH, cV = jHh/np.max(jHh), jVh/np.max(jVh)
    
    if verbose:    
        print(" ")
        print("Shape of diagonalised arrays:")
        print("Horizontal: {}".format(np.shape(jHd)))
        print("Vertical: {}".format(np.shape(jVd)))
        # print(f'Horizontal range [m] (x,y): ({nXh*dx},{nYh*dx})')
        # print(f'Vertical range [m] (x,y):   ({nXv*dy},{nYv*dy})')
    else:
        pass

    if show:
        plotTwoD(j_H/np.max(j_H),
                 dx=dx,dy=dy,sF=1,describe=False,
                 title='J - Horizontal',
                 xLabel='($x_1 - x_2$) [mm]',
                 yLabel='($x_1 - x_2$) [mm]',
                 numXticks=9,numYticks=9)
        
        plotTwoD(j_V/np.max(j_V),
                 dx=dx,dy=dy,sF=1,describe=False,
                 title='J - Vertical',
                 xLabel='($y_1 - y_2$) [mm]',
                 yLabel='($y_1 - y_2$) [mm]',
                 numXticks=9,numYticks=9)
            
        plotOneD([jHh/np.max(jHh),jHd/np.max(jHd)],
                 d=np.full(2,dx),
                 title=['Horizontal Coherence'],
                 labels=['horizontal cut','intensity'],
                 xLabel=['Position'],
                 yLabel=['Normalized Coherence'])   
        
        plotOneD([jVh/np.max(jVh),jVd/np.max(jVd)],
                 d=np.full(2,dy),
                 title=['Vertical Coherence'],
                 labels=['horizontal cut','intensity'],
                 xLabel=['Position'],
                 yLabel=['Normalized Coherence'])
        
        plotOneD([jHh/np.max(jHh),jVh/np.max(jVh)],
                 d=[dx,dy],
                 title=['Vertical Coherence'],
                 labels=['Horizontal Coherence Profile','Vertical Coherence Profile'],
                 xLabel=["Point Separation [pixels]"],
                 yLabel=['Normalized Coherence'],
                 savePath=pathCP)
    else:
        pass
    
    fx = np.max(abs(j_H))
    fy = np.max(abs(j_V))
    
    return cH, cV, J_H, J_V, jHh, jVh, fx, fy
    
# %%
def getCoherenceLength(minC,dx=1,dy=1, cH=None, cV=None, pathCL=None,verbose=False,show=False):
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
    
    if verbose:
        print(" ")
        print("-----Finding Spatial Coherence Length-----")
    else:
        pass
    try:
        if cH.any()  != False:
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
            clX = len(cH[cH>minC])
            print("Horizontal Coherence Length [pixels]: {}".format(clX))
    except AttributeError:
        pass
    try:
        if cV.any() != False:
            clY = len(cV[cV>minC])
            print("Vertical Coherence Length [pixels]: {}".format(clY))
    except AttributeError:
        pass

    if show:
        plt.clf()
        plt.close()
        fig, axs = plt.subplots(1, 2)
        try:
            if cH.any() != False:
                axs[0].plot(x, cH, label="Horizontal")
                axs[0].axvline(x=len(cH)//2 - clX/2, linestyle = ':', color='red', label='C length')
                axs[0].axvline(x=len(cH)//2 + clX/2, linestyle = ':', color='red')
    #            for ax in fig.axes:
                axs[0].set_xticks([int(len(x)*(a/5)) for a in range(0,6)])
                axs[0].set_xticklabels([round_sig(int(len(x)*(a/5))*dx) for a in range(0,6)])
                axs[1].plot(x, cH, label="Horizontal")
                axs[1].axvline(x=len(cH)//2 - clX/2, linestyle = ':', color='red', label='C length')
                axs[1].axvline(x=len(cH)//2 + clX/2, linestyle = ':', color='red')
                axs[1].set_xticks([int(len(x)*(a/10)) for a in range(0,11)])
                axs[1].set_xticklabels([round_sig(int(len(x)*(a/10))*dx) for a in range(0,11)])
                axs[1].set_xlim([(len(x)/2)-np.max(clX), (len(x)/2)+np.max(clX)])
        except AttributeError:
            pass
        try:
            if cV.any() != False:
                axs[0].plot(x, cV, '-', label="Vertical")
                axs[0].axvline(x=len(cV)//2 - clY/2, linestyle = ':', color='red', label='C length')
                axs[0].axvline(x=len(cV)//2 + clY/2, linestyle = ':', color='red')
                axs[1].plot(x, cV, '-', label="Vertical")
    #            for ax in fig.axes:
                axs[0].set_xticks([int(len(x)*(a/5)) for a in range(0,6)])
                axs[0].set_xticklabels([round_sig(int(len(x)*(a/5))*dy) for a in range(0,6)])
                axs[1].axvline(x=len(cV)//2 - clY/2, linestyle = ':', color='red', label='C length')
                axs[1].axvline(x=len(cV)//2 + clY/2, linestyle = ':', color='red')
                axs[1].set_xlim([(len(x)/2)-np.max(clY), (len(x)/2)+np.max(clY)])
                axs[1].set_xticks([int(len(x)*(a/10)) for a in range(0,11)])
                axs[1].set_xticklabels([round_sig(int(len(x)*(a/10))*dy) for a in range(0,11)])
        except AttributeError:
            pass
        try:
            if cH.any() and cV.any() != False:
                axs[1].set_xlim([(len(x)/2)-np.max([clX,clY]), (len(x)/2)+np.max([clX,clY])])
        except AttributeError:
            pass
        plt.legend()
        if pathCL != None:
            print("Saving Coherence Profile plot to: {}".format(pathCL))
            plt.savefig(pathCL)
        plt.show()
        plt.clf()
        plt.close()
    else:
        pass
    
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
def mutualIntensity(cfrT,cfrH,cfrV, Fx, Fy, dx=1, dy=1, pathJP=None, pathJ=None, verbose=False, show=False):
    """
    NEEDS FURTHER CHECKING
    Parameters
    ----------
    cfrT : Complex wavefield array - total polarisation.
    cfrH : Complex wavefield array - horizontal polarisation.
    cfrV : Complex wavefield array - vertical polarisation.
    Fx : Fraction of wavefield to sample (horizontal).
    Fy : Fraction of wavefield to sample (vertical).
    dx : horizontal pixel size, optional
        The default is 1.
    dy : vertical pixel size, optional
        The default is 1.
    pathJP : Save path for Mutual Intensity plots. The default is None.
    pathJ : Save path for total Mutual Intensity plot. The default is None.
    Returns
    -------
    Total mutual intensity, MI components:
    j, jxx, jxy, jyx, jyy
    """
    
    if verbose:
        print(" ")
        print("----Starting Mutual Intensity Function---")
    else:
        pass
    
    """ Taking sample area at centre of each complex wavefield array """
    A_T = sampleField(cfrT, Fx=Fx, Fy=Fy, limit = 1000,verbose=verbose,show=show)
    A_H = sampleField(cfrH, Fx=Fx, Fy=Fy, limit = 1000)
    A_V = sampleField(cfrV, Fx=Fx, Fy=Fy, limit = 1000)
    
    I = abs(A_T.conjugate()*A_T)
    
    """ Mutual Intensity Functions (J, Jxx, Jxy, Jyx, Jyy) """
    ### Convolution using for loop ###
    if verbose:
        print(" ")
        print("-----Calculating Mutual Intensity arrays-----")
        start2 = time.time()
    else:
        pass
    
    
    
    # New method as per meeting with Chanh
    ATx = getLineProfile(A_T,axis=1)
    I = np.array(ATx).conjugate()*np.array(ATx)
    
    # Jx, X, dX = [], [], []
    J = []
    
    #1D approach
    for x, a in enumerate(ATx):
        for i, b in enumerate(ATx):
            # define new variables
            _x = (x+i)/2
            dx = (x-i)/2
            
            # get mutual intensity
            j = a.conjugate()*b
            
            J.append((j,_x,dx))
            # Jx.append(j)
            # X.append(_x)
            # dX.append(dx)
            
            # print(f'J(x,dx): {j}')
            # print(f'(x,dx): {(_x, dx)}')
       
    
    # print(J)
    Jsum = {}
    
    for j, x, dx in J:
        # print(j,x,dx)
        
        Jtot = Jsum.get(dx, 0) + j
        Jsum[dx] = Jtot
    
    # print(Jsum)
    
    DX = np.fromiter(Jsum.keys(), dtype=float)
    jX = np.fromiter(Jsum.values(), dtype=float)
    print(len(DX))
    
    plt.plot(DX,jX, 'x')
    plt.xlabel('dx')
    plt.ylabel('J')
    plt.show()
    
    # intensity
    I = np.array(ATx).conjugate()*np.array(ATx)
    print(np.max(I**2/2))
    
    xp = np.linspace(-12,12,len(I))
    
    plt.plot(DX,jX, 'x', label='J')
    plt.plot(xp,I**2/2, 'o', label='$I^2/2$')
    plt.xlabel('dx')
    plt.ylabel('J')
    plt.legend()
    plt.show()
    
    return J
        
    
    # J = np.array([A_T.conjugate()*a for a in A_T.flatten()])      # eq.2.3.1.3
    Jxx = np.array([A_H.conjugate()*a for a in A_H.flatten()])    # eq.2.3.1.5
    Jxy = np.array([A_H.conjugate()*a for a in A_V.flatten()])    # eq.2.3.1.5
    Jyx = np.array([A_V.conjugate()*a for a in A_H.flatten()])    # eq.2.3.1.5
    Jyy = np.array([A_V.conjugate()*a for a in A_V.flatten()])    # eq.2.3.1.5
    
    return J
    # # for a in A_T:
    # #     print(len(a))
    # #     for b in a:
    # #         print b
            
            
    # #     Ja = np.array(A_T.conjugate()*a)
        
        
    
    if verbose:
        end2 = time.time()
        print('Time taken to calculate Mutual Intensity Functions [J] (s): {}'.format(end2 - start2))
        
        print("Shape of each Mutual Intensity array:")
        print("J: {}".format(np.shape(J)))
        print("Jxx: {}".format(np.shape(Jxx)))
        print("Jxy: {}".format(np.shape(Jxy)))
        print("Jyx: {}".format(np.shape(Jyx)))
        print("Jyy: {}".format(np.shape(Jyy)))
        # print(f"Shape of Intensity array: {np.shape(I)}")
    
    """ Averaging each Mutual Intensity Array (& Normalising J)"""
    j = abs(J.mean(0))/(I[int(np.shape(I)[0]/2),int(np.shape(I)[1]/2)]) # This line needs fixing
    jxx = abs(Jxx.mean(0))
    jxy = abs(Jxy.mean(0))
    jyx = abs(Jyx.mean(0))
    jyy = abs(Jyy.mean(0))
    
    if show:
        plotMultiTwoD([abs(jxx), abs(jxy), abs(jyx), abs(jyy)], dims=[2,2],
                      dx=np.full(4,dx), dy=np.full(4,dy), 
                      #ran=[[jmin,jmax],[jmin,jmax],[jmin,jmax],[jmin,jmax]],
                      title=['$J_{xx}$','$J_{xy}$','$J_{yx}$','$J_{yy}$'],
                      xLabel='x-position',yLabel='y-position',
                      numXticks=3, numYticks=5,
                      onlyEdgeLabels=True,savePath=pathJP,multiCBar=True)
        
        plotTwoD(abs(j), dx=dx, dy=dy, title='Mutual Intensity - J',
                 xLabel="Point Separation x-x' [$\mu$m]",
                 yLabel="Point Separation y-y' [$\mu$m]",
                 savePath=pathJ)
    
    return j, jxx, jxy, jyx, jyy

# %%
def stokesFromJ(Jxx,Jxy,Jyx,Jyy, pathSJ=None, pathP=None, verbose=False, show=False):
    """ 
    Function to calculate and plot the 2 point Stokes parameters from the elements of the 2x2 J matrix.
    Also plots the degree of polarisation P for every point.
    Jxx, Jxy, Jyx, Jyy : elements of the Mutual Intensity matrix
    
    """
    J = np.array([[Jxx, Jxy], [Jyx, Jyy]])      # Eq. 2.3.1.4
    
    if verbose:
        print(" ")
        print("-----Getting Stokes from J-----")
        print("Shape of J: {}".format(np.shape(J)))
    else:
        pass
    
    import cmath
    i = cmath.sqrt(-1)
    
    """ Getting Stokes Parameters """
    S0 = abs(Jxx) + abs(Jyy)                               # Eq. 2.3.2.3.1
    S1 = abs(Jxx) - abs(Jyy)                               # Eq. 2.3.2.3.2
    S2 = abs(Jxy) + abs(Jyx)                               # Eq. 2.3.2.3.3
    S3 = i*(abs(Jxy)-abs(Jyx))                             # Eq. 2.3.2.3.4
    
    """ Normalising """
    s0 = S0/S0
    s1 = S1/S0
    s2 = S2/S0
    s3 = S3.real/S0
    
    """ Getting Degree of Polarisation """
    detJ = (Jxx*Jyy - Jxy*Jyx) #np.linalg.det(J)
    P = (1 - ((4*detJ)/((Jxx + Jyy)**2)))**(1/2)  # Eq. 2.3.2.3.5
    
    if show:
        """ Plotting Stokes Parameters """
        smin = np.min([S0,S1,S2,S3.real])
        smax = np.max([S0,S1,S2,S3.real])
        plotMultiTwoD([S0,S1,S2,S3.real], dims=[2,2],
                      ran=[[smin,smax],[smin,smax],[smin,smax],[smin,smax]],
                      title=['$S_0$','$S_1$','$S_2$','$S_3$'],
                      xLabel='x-position', yLabel='y-position',
                      onlyEdgeLabels=True)
        
        """ Plotting Normalised Stokes Parameters """
        smin = np.min([s0,s1,s2,s3])
        smax = np.max([s0,s1,s2,s3])
        plotMultiTwoD([s0,s1,s2,s3], dims=[2,2],
                      ran=[[smin,smax],[smin,smax],[smin,smax],[smin,smax]],
                      title=['$s_0$','$s_1$','$s_2$','$s_3$'],
                      xLabel='x-position', yLabel='y-position',
                      onlyEdgeLabels=True,savePath=pathSJ)
        
        """ Plotting Degree of Polarisation """
        plotTwoD(abs(P),title="Degree of Polarisation",savePath=pathP)
    else:
        pass
        
    return S0, S1, S2, S3



# %%
def test():
    from wpg.generators import build_gauss_wavefront
    from wpg.wavefront import Wavefront
    try:
        from wpg.srw import srwlpy as srwl
    except ImportError:
        import srwlpy as srwl
    from usefulWavefield import getComplex
    from useful import fromPickle
    
    eMin = 50e6
    Nx = 75
    Ny = 75
    Nz = 1
    xMin = -10e-6
    xMax = 10e-6
    yMin = -10e-6
    yMax = 10e-6
    zMin = 100
    Fx = 1/8
    Fy = 1/8
    print('Running Test:')
    print('building wavefront...')
    w = build_gauss_wavefront(Nx,Ny,Nz,eMin/1000,xMin,xMax,yMin,yMax,1,1e-6,1e-6,1) 
    
    wf0 = Wavefront(srwl_wavefront=w)
    
    # wf = wf0.toComplex()
    
    """From pickled wavefield """
    path = '/home/jerome/Documents/MASTERS/data/YDStest/13nm/' #wavefieldME_TEST_500um_.pkl' #'/home/jerome/dev/wavefieldME_TEST_500um_.pkl'
    waveName = path + 'wavefieldME_TEST_50um_.pkl'
    print("-----Loading Wavefield-----")
    wf = fromPickle(waveName)
    wf = Wavefront(srwl_wavefront=wf)
    extra = "_200nm"
    pathI = path + "Intensity" + extra + ".png" # Save path for horizontal coherence profile plot
    pathCpX = path + "CpX" + extra + ".png" # Save path for horizontal coherence profile plot
    pathCpY = path + "CpY" + extra + ".png" # Save path for vertical coherence profile plot
    pathWX = path + "WX" + extra + ".png" # Save path for horizontal complex wavefield plot
    pathWY = path + "WY" + extra + ".png" # Save path for vertical complex wavefield plot
    
    
    pathCP = path + "CoherenceProfile" + extra + ".png" # Save path for horizontal/vertical mutual intensity profiles
    pathJP = path + "MutualIntensityPlots" + extra + ".png" # Save path for Mutual Intensity plots
    pathJ = path + "MutualIntensity" + extra + ".png" # Save path for Mutual Intensity

    """Coherence from pyplot """
    #coherenceProfiles(wf,
    #                  pathI, pathCpX, pathCpY, pathWX, pathWY)

    cw = getComplex(wf)
    cwH = getComplex(wf,'horizontal')
    cwV = getComplex(wf,'vertical')
    I = wf.get_intensity()
    cX = cw[:,int(int(np.max(np.shape(cw[:,0,0])))/2)]
    cY = cw[int(int(np.max(np.shape(cw[0,:,0])))/2),:]
    Ix = I[:,int(int(np.max(np.shape(I[:,0,0])))/2)]
    Iy = I[int(int(np.max(np.shape(I[0,:,0])))/2),:]
    
    """Mutual Intensity """
    profileMI(np.squeeze(cX),np.squeeze(cY), verbose=True, show=True)
    mutualIntensity(cw,cwH,cwV, Fx=Fx, Fy=Fy, verbose=True, show=True)#, pathCP, pathJP, pathJ)
    
    
# %%
def testComplex():
    path = 'wavefield_1.pkl'
    
    import pickle
    with open(path, 'rb') as wav:
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
    path = '/home/jerome/dev/data/correctedCoherence/'
    #slit sizes]
    sX = [200,200]
    sY = [200,200]
    
    #resolution of each electric field
    cdx250, cdy250 = 2.0296997983770577e-06, 1.7427838524854241e-06
    
    dx = [cdx250,cdx250]
    dy = [cdy250,cdy250]
    
    if justHor:
        EhR = [imageio.imread(path + 'beforeBDA_efield_sx' + str(s) + 'ExReal.tif') for s in sX]
        EvR = [imageio.imread(path + 'beforeBDA_efield_sx' + str(s) + 'EyReal.tif') for s in sX]
        EhI = [imageio.imread(path + 'beforeBDA_efield_sx' + str(s) + 'ExIm.tif') for s in sX]
        EvI = [imageio.imread(path + 'beforeBDA_efield_sx' + str(s) + 'EyIm.tif') for s in sX]
    else:
        EhR = [imageio.imread(path + 'beforeBDA_efield_sx' + str(s) + 'sy' + str(y) + 'ExReal.tif') for s,y in zip(sX,sY)]
        EvR = [imageio.imread(path + 'beforeBDA_efield_sx' + str(s) + 'sy' + str(y) + 'EyReal.tif') for s,y in zip(sX,sY)]
        EhI = [imageio.imread(path + 'beforeBDA_efield_sx' + str(s) + 'sy' + str(y) + 'ExIm.tif') for s,y in zip(sX,sY)]
        EvI = [imageio.imread(path + 'beforeBDA_efield_sx' + str(s) + 'sy' + str(y) + 'EyIm.tif') for s,y in zip(sX,sY)]
    
    print(np.shape(EhR))
    print(np.shape(EvR))
    print(np.shape(EhI))
    print(np.shape(EvI))
    
    Eh = [ExR + ExI*1j for ExR,ExI in zip(EhR,EhI)]
    Ev = [EyR + EyI*1j for EyR,EyI in zip(EvR,EvI)]#EvR + EvI*1j
    cE = [Ex + Ey for Ex, Ey in zip(Eh,Ev)] #Eh + Ev
    
    # empty lists for coherence lengths
    cLx = []
    cLy = []
    cLx2 = []
    cLy2 = []
    mIx = []
    mIy = []
    totIx = []
    totIy = []
    ImTOT = []
    
    print("shape of cE: ", np.shape(cE))
    
    for ce, ch, cv, s, dX, dY in zip(cE,Eh,Ev,sX, dx, dy): 
        I = abs(ce.conjugate()*ce)
        ex = ce[int(np.shape(ce)[0]/2),:]
        ey = ce[:,int(np.shape(ce)[1]/2)]
        Ix = I[int(np.shape(I)[0]/2),:]
        Iy = I[:,int(np.shape(I)[1]/2)]
        
        J,Jxx,Jxy,Jyx,Jyy = mutualIntensity(ce,ch,cv,Fx=0.01,Fy=0.01,dx=dX,dy=dY,verbose=True,show=True)
        
        s1,s2,s3,s4 = stokesFromJ(Jxx, Jxy, Jyx, Jyy)#,verbose=True,show=True)
        
        p = int((gx*gy)/(dX*dY))
        px = int(gx/dX)
        py = int(gy/dY)
        print("resolution (x,y): ", (dX,dY))
        print("number of pixels for mask x profile: ", px)
        print("number of pixels for mask y profile: ", py)
        print("total number of pixels for mask area: ", p)
        
        _c = 299792458
        epsilon = 8.854187817e-12
        
        Imtot_w = I*(_c/2*epsilon) # W/m^2
        ITOT = Imtot_w*(1/1.602e-19)*(1/185)*0.0001
        
        Imtot = np.sum(ITOT*dX*dY)
        
        # print(np.shape(ex))
        cH, cV, jH, jV, jHh, jVh, fx, fy = profileMI(ex,ey,dx=dX,dy=dY)#,verbose=True,show=True)

        Cx = getCoherenceFromProfile(ex)#, verbose=True, show=True)
        Cy = getCoherenceFromProfile(ey)#, show=True)
        
        fig, axs = plt.subplots(2,1)
        axs[0].plot(Cx, label='horizontal coherence')
        axs[0].plot(Ix/np.max(Ix), label='normalised intensity (y=0)')
        axs[0].plot(cH, label='horizontal coherence')
        axs[1].plot(Cy, label='vertical coherence')
        axs[1].plot(Iy/np.max(Iy), label='normalised intensity (x=0)')
        axs[1].plot(cV, label='vertical coherence')
        axs[0].set_ylabel('Horiztonal Coherence')
        axs[0].legend()
        axs[1].set_ylabel('Vertical Coherence')
        axs[1].legend()
        axs[0].set_xticks([int(len(cH)*(a/4)) for a in range(0,5)])
        axs[0].set_xticklabels([round_sig(int((len(cH))*(a/4))*dX*1e3) for a in [-2,-1,0,1,2]])
        axs[1].set_xticks([int(len(cV)*(a/4)) for a in range(0,5)])
        axs[1].set_xticklabels([round_sig(int((len(cV))*(a/4))*dY*1e3) for a in [-2,-1,0,1,2]])
        axs[1].set_xlabel('Position [mm]')
        plt.show()
    
        
        # coherence length from profile
        clx_1 = getCoherenceLength(0.8,cH = np.array(Cx),dx=dX, verbose=True, show=True)*dX
        cly_1 = getCoherenceLength(0.8,cV = np.array(Cy),dy=dY)*dY
        
        # coherence length from MI function
        clx_2 = getCoherenceLength(0.8,cH = np.array(cH),dx=dX, verbose=True, show=True)*dX
        cly_2 = getCoherenceLength(0.8,cV = np.array(cV),dy=dY)*dY
        
        sumIx = abs(np.sum(Ix))
        print('I sum: ',sumIx)
        sumIy = abs(np.sum(Iy))
        print('I sum: ',sumIy)
        cLx.append(clx_1)
        cLy.append(cly_1)
        cLx2.append(clx_2)
        cLy2.append(cly_2)
        mIx.append(fx)
        mIy.append(fy)
        totIx.append(sumIx)
        totIy.append(sumIy)
        ImTOT.append(Imtot)
        
#        cL.append(get_coherence_len(ce,d,d))
        
        if save:
            imageio.imwrite(path + str(s) + 'coherenceHOR.tif',np.float32(jH))
            imageio.imwrite(path + str(s) + 'coherenceVER.tif',np.float32(jV))
#            imageio.imwrite(path + str(s) + 'mi.tif',np.float32(J))
#            imageio.imwrite(path + str(s) + 'miXX.tif',np.float32(Jxx))
#            imageio.imwrite(path + str(s) + 'miXY.tif',np.float32(Jxy))
#            imageio.imwrite(path + str(s) + 'miYX.tif',np.float32(Jyx))
#            imageio.imwrite(path + str(s) + 'miYY.tif',np.float32(Jyy))
#            imageio.imwrite(path + str(s) + 's0.tif',np.float32(S0))
#            imageio.imwrite(path + str(s) + 's1.tif',np.float32(S1))
#            imageio.imwrite(path + str(s) + 's2.tif',np.float32(S2))
#            imageio.imwrite(path + str(s) + 's3.tif',np.float32(S3))
    

    ImTOT = np.squeeze(ImTOT)
    
    plt.plot(sX,[c*1e6 for c in cLx2], 'x', label='horizontal - profile')
    plt.plot(sY,[c*1e6 for c in cLy2], 'x', label='vertical - profile')
# for coherence
    plt.ylabel('Coherence Length [\u03bcm]')
    plt.xlabel('SSA Width  [\u03bcm]')
    plt.legend()
    plt.show()
    
    #plotting separately
    fig, axs = plt.subplots(1,2)
    axs[0].plot(sX,[c*1e6 for c in cLx], 'x', label='profile')
    axs[1].plot(sY,[c*1e6 for c in cLy], 'x', label='profile') #[sY[0],sY[2],sY[4],sY[5]]
    # axs[0].plot(sX,[c*1e6 for c in cLx2], 'x', label='profile')
    # axs[1].plot(sY,[c*1e6 for c in cLy2], 'x', label='profile')
    axs[0].set_xlabel('Horiztonal SSA Width  [\u03bcm]')
    axs[0].set_ylabel('Horizontal Coherence Length  [\u03bcm]')
    axs[1].set_xlabel('Vertical SSA Width  [\u03bcm]')
    axs[1].set_ylabel('Vertical Coherence Length  [\u03bcm]')
    axs[1].legend()
    fig.tight_layout()
    plt.show()
    
    fig, ax1 = plt.subplots()
    ax0 = plt.subplot(121)
    ax1 = ax0.twinx()
    # for coherence
    ax0.plot(sX,[c*1e6 for c in cLx2], ':x')
    ax1.plot(sX, ImTOT,':x',color=colours[1], label='total I')
    ax0.set_ylabel('horizontal coherence length [\u03bcm]')
    ax1.set_ylabel('Total Intensity [ph/s/0.1%bw]')
    ax1.spines['left'].set_color(colours[0])
    ax1.spines['right'].set_color(colours[1])
    ax0.yaxis.label.set_color(colours[0])
    ax0.tick_params(axis='y', colors=colours[0])
    ax1.yaxis.label.set_color(colours[1])
    ax1.tick_params(axis='y', colors=colours[1])
    ax0.set_xlabel('Horiztonal SSA Width  [\u03bcm]')
    fig.tight_layout()
    plt.show()

# %%
if __name__ == '__main__':
    # test()
    testCoherenceProfile()