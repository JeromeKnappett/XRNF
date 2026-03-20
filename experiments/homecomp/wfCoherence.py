#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 16:02:19 2021

@author: jerome
"""
from wpg.generators import build_gauss_wavefront
from wpg.srwlib import SRWLStokes, SRWLWfr
import numpy as np
import matplotlib.pyplot as plt
#import wfStokes
import scipy.ndimage

from wpg.wavefront import Wavefront

try:
    from wpg.srw import srwlpy as srwl
except ImportError:
    import srwlpy as srwl

import time
import math

from wpg.srwlib import *

from math import log10, floor, sqrt

#import wfAnalyseWave as aw

#print(plt.style.available)
#plt.style.reload_library()
#plt.style.use('seaborn')#['science','ieee']) # 'no-latex'])#,'ieee'])

# %%
def round_sig(x, sig=2):
    if x != 0:
        return round(x, sig-int(floor(log10(abs(x))))-1)
    else:
            return x

# %%
def coherenceProfiles(wfr, pathI = None, CpX = None, CpY = None, WX = None, WY = None ):
    """
    Calculate the horizontal and vertical profiles of the spatial coherence 
    of a 2D wavefield
    
    :param wfr:  wavefield
    :plots horizontal and vertical coherence profiles
    """
    
    print("----Starting coherenceProfiles Function---")
    
    start1 = time.time()
    cfr = getComplex(wfr)
    end1 = time.time()
    print('Time taken to convert to complex wavefield (s): {}'.format(end1 - start1))
    
    A = cfr #sampleField(cfr, Fx=1, Fy=1, Limit = 750)
    
    print("Shape of sampled array A: {}".format(np.shape(A)))
    
    """ Finding number of points in each line profile """
    Anumx = int(np.max(np.shape(A[:,0,0]))) # These are in pixels
    Anumy = int(np.max(np.shape(A[0,:,0])))
    
    AmidX = int(Anumx/2)
    AmidY = int(Anumy/2)
    
#    """ Mutual Coherence Function """
#    start2 = time.time()
#    Bx = np.array([A[:,int(Anumy/2)].conjugate() * a for a in A[:,int(Anumy/2)]])
#    By = np.array([A[int(Anumx/2),:].conjugate() * a for a in A[int(Anumx/2),:]])
#    end2 = time.time()
#    print('Time taken to calculate coherence (s): {}'.format(end2 - start2))
#    
#    print("Shape of Bx: {}".format(np.shape(Bx)))
#    print("Shape of By: {}".format(np.shape(By)))
    
    """ Getting pixel dimensions """
    Dx = wfr.params.Mesh.xMax - wfr.params.Mesh.xMin
    Dy = wfr.params.Mesh.yMax - wfr.params.Mesh.yMin
    
    """ Creating array of custom tick markers for plotting """
    tickAx = [round_sig(-Dx*1e6/2),
               round_sig(-Dx*1e6/4),
              0,
               round_sig(Dx*1e6/4),
               round_sig(Dx*1e6/2)
              ]
    tickAy = [round_sig(Dy*1e6/2),
               round_sig(Dy*1e6/4),
              0,
               round_sig(-Dy*1e6/4),
              round_sig(-Dy*1e6/2)]

    NFFT = 128
    
    
    """ Plotting Intensity """
    plt.clf()
    plt.close()
    plt.imshow(abs(A.conjugate()*A))
    plt.title("Intensity")
    plt.xticks(np.arange(0,Anumx+1,Anumx/4),tickAx)
    plt.xticks(np.arange(0,Anumy+1,Anumy/4),tickAy)
    plt.xlabel("Horizontal Position [\u03bcm]")#"(\u03bcm)")
    plt.ylabel("Vertical Position [\u03bcm]")#"(\u03bcm)")
    plt.colorbar()
    if pathI != None:
        print("Saving intensity figure to path: {}".format(pathI))
        plt.savefig(pathI)
    plt.show()
    plt.clf()

    """ Plotting Complex Wavefield """
    plt.clf()
    plt.plot(A[:,AmidY])
    plt.title("Complex Wavefield - Horizontal Cut")
    plt.xticks(np.arange(0,Anumx+1,Anumx/4),tickAx)
    plt.xlabel("x [\u03bcm]")#"(\u03bcm)")
    if WX != None:
        print("Saving complex wavefield horizontal profile to: {}".format(WX))
        plt.savefig(WX)
    plt.show()
    plt.clf()    
    
    """ Getting Horizontal Coherence """
    corX = plt.cohere(np.squeeze(A[:,AmidY]), np.squeeze(A[:,AmidY].conjugate()),NFFT)    
      
#    print("min and max of corx (min,max): {}".format((np.min(corX[1]),np.max(corX[1]))))
    
    """ Plotting Coherence Profile """
    plt.title('Horizontal Coherence Profile')
    plt.xticks(np.arange(-1,1.00001,2/4),tickAx)#(np.arange(np.min(corX[1]) ,np.max(corX[1]),(np.max(corX[1])-np.min(corX[1]))/4),tickAx)
    plt.xlabel("x-x' [\u03bcm]")#"(\u03bcm)")
#    plt.ylim(0,1.1)
    if CpX != None:
        print("Saving horizontal coherence profile to: {}".format(CpX))
        plt.savefig(CpX)
    plt.show()
    plt.clf()
    
    """ Plotting Complex Wavefield """
    plt.plot(A[AmidX,:])
    plt.title("Complex Wavefield - Vertical Cut")
    plt.xticks(np.arange(0,Anumx+1,Anumx/4),tickAx)
    plt.xlabel("y [\u03bcm]")#"(\u03bcm)")
    if WY != None:
        print("Saving complex wavefield vertical profile to: {}".format(WY))
        plt.savefig(WY)
    plt.show()
    plt.clf()      
    
    """ Getting Vertical Coherence """
    corY = plt.cohere(np.squeeze(A[AmidX,:]), np.squeeze(A[AmidX,:].conjugate()),NFFT)    
    
    """ Plotting Coherence Profile """
    plt.title('Vertical Coherence Profile')
    plt.xticks(np.arange(-1,1.00001,2/4),tickAx)
    plt.xlabel("y-y' [\u03bcm]")#"(\u03bcm)")
#    plt.ylim(0,1.1)
    if CpY != None:
        print("Saving vertical coherence profile to: {}".format(CpY))
        plt.savefig(CpY)
    plt.show()
    plt.clf()

#    print("shape of y-coherence array: {}".format(np.shape(corY)))
#    print("shape of x-coherence array: {}".format(np.shape(corX)))
#    print("max,min values of y-coh array:{}".format((np.max(corY),np.min(corY))))

# %%
# %%
def mutualIntensity(wfr, Fx, Fy, pathCP=None, pathJP=None, pathJ=None):
    
    print("----Starting Mutual Intensity Function---")
    
    print("Converting to complex wavefields and extracting each polarisation component")
    start1 = time.time()
    cfrT = getComplex(wfr, polarization = "total")
    cfrH = getComplex(wfr, polarization = "horizontal")
    cfrV = getComplex(wfr, polarization = "vertical")
    end1 = time.time()
    print('Time taken to convert to complex wavefield (s): {}'.format(end1 - start1))
    
    """ Taking sample area at centre of each complex wavefield array """
    A_T = sampleField(cfrT, Fx=Fx, Fy=Fy, Limit = 200)
    A_H = sampleField(cfrH, Fx=Fx, Fy=Fy, Limit = 200)
    A_V = sampleField(cfrV, Fx=Fx, Fy=Fy, Limit = 200)
    
    """ Finding number of points in each line profile """
    Anumx = int(np.max(np.shape(A_T[:,0,0]))) # These are in pixels
    Anumy = int(np.max(np.shape(A_T[0,:,0])))
    
    AmidX = int(Anumx/2) # centre pixel in horizontal line profile
    AmidY = int(Anumy/2) # centre pixel in vertical line profile
    
    """ Taking line profiles through each array """
    A_Tx = A_T[:,AmidY]
    A_Ty = A_T[AmidX,:]
    A_Hx = A_H[:,AmidY]
    A_Hy = A_H[AmidX,:]
    A_Vx = A_V[:,AmidY]
    A_Vy = A_V[AmidX,:]
    
    """ Mutual Intensity Functions (J, Jxx, Jxy, Jyx, Jyy) """
    print(" ")
    print("-----Calculating Mutual Intensity arrays-----")
    start2 = time.time()
    J = np.array([A_T.conjugate()*a for a in A_T.flatten()])
    Jxx = np.array([A_H.conjugate()*a for a in A_H.flatten()])
    Jxy = np.array([A_H.conjugate()*a for a in A_V.flatten()])
    Jyx = np.array([A_V.conjugate()*a for a in A_H.flatten()])
    Jyy = np.array([A_V.conjugate()*a for a in A_V.flatten()])
    end2 = time.time()
    print('Time taken to calculate Mutual Intensity Functions [J] (s): {}'.format(end2 - start2))
    
    print("Shape of each Mutual Intensity array:")
    print("J: {}".format(np.shape(J)))
    print("Jxx: {}".format(np.shape(Jxx)))
    print("Jxy: {}".format(np.shape(Jxy)))
    print("Jyx: {}".format(np.shape(Jyx)))
    print("Jyy: {}".format(np.shape(Jyy)))
    
    """ Averaging each Mutual Intensity Array """
    j = abs(J.mean(0))
    jxx = abs(Jxx.mean(0))
    jxy = abs(Jxy.mean(0))
    jyx = abs(Jyx.mean(0))
    jyy = abs(Jyy.mean(0))



    """ Getting pixel dimensions """
    Dx = wfr.params.Mesh.xMax - wfr.params.Mesh.xMin
    Dy = wfr.params.Mesh.yMax - wfr.params.Mesh.yMin
    
    """ Creating array of custom tick markers for plotting """
    tickAx = [round_sig(-Dx*1e6/2),
               round_sig(-Dx*1e6/4),
              0,
               round_sig(Dx*1e6/4),
               round_sig(Dx*1e6/2)
              ]
    tickAy = [round_sig(Dy*1e6/2),
               round_sig(Dy*1e6/4),
              0,
               round_sig(-Dy*1e6/4),
              round_sig(-Dy*1e6/2)]




    """ Mutual Intensity Profiles """
    print(" ")
    print("-----Calculating Mutual Intensity profiles-----")
    start3 = time.time()
    print("Shape of line profiles:")
    print("Horizontal: {}".format(np.shape(A_Tx)))
    print("Vertical: {}".format(np.shape(A_Ty)))
    J_H = np.array([A_Tx.conjugate()*a for a in A_Tx]) # Horizontal coherence profile
    J_V = np.array([A_Ty.conjugate()*a for a in A_Ty]) # Vertical coherence profile
    end3 = time.time()
    print("time taken to calculate Mutual Intensity profiles: {}".format(end3-start3))
    
    print("Shape of each Mutual Intensity profile:")
    print("Horizontal profile: {}".format(np.shape(J_H)))
    print("Vertical profile: {}".format(np.shape(J_V)))

    j_H = abs(J_H) #(J_H[0]**2 + J_H[1]**2)**(1/2)
    j_V = abs(J_H) #(J_V[0]**2 + J_V[1]**2)**(1/2)
    
    jHd = np.diagonal(np.squeeze(J_H)) 
    jVd = np.diagonal(np.squeeze(J_V))
    print("Shape of diagonalised arrays:")
    print("Horizontal: {}".format(np.shape(jHd)))
    print("Vertical: {}".format(np.shape(jVd)))
    
    IH = np.diagonal(list(zip(np.squeeze(J_H)[::-1])))
    IV = np.diagonal(list(zip(np.squeeze(J_V)[::-1])))

    print("Shape of Intensity arrays:")
    print("Horizontal: {}".format(np.shape(IH)))
    print("Vertical: {}".format(np.shape(IV)))
    
    cH = abs(jHd/np.squeeze(IH))
    cV = abs(jVd/np.squeeze(IV))

    plt.close()
    #plt.plot(J_H[0], label = "Horizontal Coherence Profile - 1")
    #plt.plot(J_V[0], label = "Vertical Coherence Profile -1")
    #plt.plot(J_H[1], label = "Horizontal Coherence Profile - 2")
    #plt.plot(J_V[1], label = "Vertical Coherence Profile - 2")
    #plt.plot(j_H, label = "Horizontal Profile- Magnitude")
    #plt.plot(j_V, label = "Vertical Profile - Magnitude")
    #plt.plot(abs(J_H.mean(0)/(2*np.squeeze(IH))), label = 'Horizontal Profile - Mean (normalised)')
    #plt.plot(abs(J_V.mean(0)/(2*np.squeeze(IV))), label = 'Vertical Profile - Mean (normalised)')
    plt.plot(cH, label = 'Horizontal Profile - Diagonal (normalised)')
    plt.plot(cV, label = 'Vertical Profile - Diagonal (normalised)')
    #plt.plot(1/cH, label = 'Horizontal Profile - Opposite Diagonal (normalised)')
    #plt.plot(1/cV, label = 'Vertical Profile - Opposite Diagonal (normalised)')
    plt.xticks(np.arange(0,Anumx+1,Anumx/4),tickAx)
    plt.xlabel("Point Separation x-x'[\u03bcm]")
    plt.ylabel("Degree of Coherence")
    plt.legend()
    if pathCP != None:
        print("Saving Mutual Intensity profiles to: {}".format(pathCP))
        plt.savefig(pathCP)
    plt.show()
    plt.clf()
    
    plt.close()
    fig, axs = plt.subplots(2, 2)
    axs[0, 0].imshow(jxx)
    axs[0, 0].set_title('Jxx')
    axs[0, 1].imshow(jxy)
    axs[0, 1].set_title('Jxy')
    axs[1, 0].imshow(jyx)
    axs[1, 0].set_title('Jyx')
    axs[1, 1].imshow(jyy)
    axs[1, 1].set_title('Jyy')
    
    #from mpl_toolkits.axes_grid1 import make_axes_locatable
    #divider = make_axes_locatable(axs)
    #cax = divider.append_axes('right', size='5%', pad=0.05)
    #fig.colorbar(im, cax=cax, orientation='vertical')

    for ax in axs.flat:
        #ax.set(xticks(np.arange(0,Anumx+1,Anumx/4),tickAx), yticks(np.arange(0,Anumy+1,Anumy/4),tickAy))
        ax.set(xlabel="Point Separation x-x' [\u03bcm]", ylabel="Point Separation y-y'[\u03bcm] ")
    # Hide x labels and tick labels for top plots and y ticks for right plots.
    for ax in axs.flat:
        ax.label_outer()
    if pathJP != None:
        print("Saving Mutual Intensity Plots to: {}".format(pathJP))
        plt.savefig(pathJP)
    plt.show()
    plt.clf()
    
    plt.imshow(j)
    plt.title("Mututal Intensity - J")
    #plt.xticks(np.arange(0,Anumx+1,Anumx/4),tickAx)
    #plt.yticks(np.arange(0,Anumy+1,Anumy/4),tickAy)
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
    path ='/data/YDStest/13nm/' 
    extra = "_200nm"
    pathSJ = path + "Stokes" + extra + ".png" # Save path for Stokes plot
    pathP = path + "Polarisation" + extra + ".png" # Save path for degree of Polarisation plot

    stokesFromJ(jxx,jxy,jyx,jyy,pathSJ, pathP)

# %%
def stokesFromJ(Jxx,Jxy,Jyx,Jyy, pathSJ, pathP):
    """ 
    Function to calculate and plot the 2 point Stokes parameters from the elements of the 2x2 J matrix.
    Also plots the degree of polarisation P for every point.
    Jxx, Jxy, Jyx, Jyy : elements of the Mutual Intensity matrix
    
    """
    J = np.array([[Jxx, Jxy], [Jyx, Jyy]])
    print("Shape of J: {}".format(np.shape(J)))
    
    import cmath
    
    """ Getting Stokes Parameters """
    S0 = Jxx + Jyy
    S1 = Jxx - Jyy
    S2 = Jxy + Jyx
    S3 = cmath.sqrt(-1)*(Jxy - Jyx)
    
    """ Plotting Stokes Parameters """
    plt.close()
    fig, axs = plt.subplots(2, 2)
    axs[0, 0].imshow(S0)
    axs[0, 0].set_title('S0')
    axs[0, 1].imshow(S1)
    axs[0, 1].set_title('S1')
    axs[1, 0].imshow(S2)
    axs[1, 0].set_title('S2')
    axs[1, 1].imshow(abs(S3))
    axs[1, 1].set_title('S3')

    for ax in axs.flat:
        ax.set(xlabel='x', ylabel='y')
    # Hide x labels and tick labels for top plots and y ticks for right plots.
    for ax in axs.flat:
        ax.label_outer()
    if pathSJ != None:
        print("Saving Stokes Plots to: {}".format(pathSJ))
        plt.savefig(pathSJ)
    plt.show()
    plt.clf()
    
    """ Getting Degree of Polarisation """
    detJ = (Jxx*Jyy - Jxy*Jyx) #np.linalg.det(J)
    P = (1 - ((4*detJ)/((Jxx + Jyy)**2)))**(1/2)

    plt.imshow(P)
    plt.title("Degree of Polarisation")
    plt.colorbar()
    if pathP != None:
        print("Saving degree of polarisation plot to: {}".format(pathP))
        plt.savefig(pathP)
    plt.show()
    plt.clf()

# %%

def getComplex(w, polarization = None):
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
    
    re = w.get_real_part(polarization = polarization)      # get real part of wavefield
    im = w.get_imag_part(polarization = polarization)      # get imaginary part of wavefield
    
    
    print("Shape of real part of wavefield: {}".format(np.shape(re)))
    print("Shape of imaginary part of wavefield: {}".format(np.shape(im)))
    
    # print("real part:")
    # print(re)
    # print("imaginary part:")
    # print(im)
    
    cwf = re + im*1j
    
    print("Shape of complex wavefield: {}".format(np.shape(cwf)))
    print("Polarization of complex wavefield: {}".format(polarization))
    # print("Complex Wavefield:")
    # print(cwf)
    
    return cwf


# %%
def fromPickle(path, wavefront=False):
    import pickle
    
    with open(path, 'rb') as wav:
        w = pickle.load(wav)
    
    if wavefront != False:
        w = Wavefront(srwl_wavefront=w)
    
    return w
    

# %%
def sampleField(A,Fx,Fy,Limit = 75):
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
    print("Original size of wavefield [pixels]: {}".format((Ax,Ay)))
    
    Sx = Fx*Ax
    Sy = Fy*Ay
    print("Sampled area size (pixels): {}".format([Sx,Sy]))
        
    if Sx > Limit or Sy > Limit:
        print("Error: Sampled area of wavefront is too large. Change Fx/Fy to a smaller value")
        import sys
        sys.exit()
    
    
    _x0 = 0 # These are in _pixel_ coordinates!!
    _y0 = 0
    _x1 = int(np.max(np.shape(A[:,0,0]))) # These are in _pixel_ coordinates!!
    _y1 = int(np.max(np.shape(A[0,:,0])))
    
    print("Nx (pixels): {}".format(_x1))
    print("Ny (pixels): {}".format(_y1))
    
    numx = _x1 - _x0 # number of points for line profile
    numy = _y1 - _y0
    midX = int(numx/2)
    midY = int(numy/2)
    
    print("mid x: {}".format(midX))
    print("mid y: {}".format(midY))

    ROI = ((int(midX-((Fx)*midX)),int(midY-((Fy)*midY))),
           (int(midX+((Fx)*midX)),int(midY+((Fy)*midY)))) 
    
    print("Region of interest (pixels): {}".format(ROI))
    
    x0,y0 = ROI[0][0], ROI[0][1]
    x1,y1 = ROI[1][0], ROI[1][1]
    
    lX = ROI[1][0]-ROI[0][0]
    lY = ROI[1][1]-ROI[0][1]
    
    I = abs(A.conjugate()*A)
    figure, ax = plt.subplots(1) 
    rect = patches.Rectangle((x0,x0),lX,lY, edgecolor='r', facecolor="none")
    
    plt.imshow(I)
    ax.add_patch(rect)
    plt.title("Original Wavefield with Sampled Area")
    plt.show()
    plt.clf()
    plt.close()

    B = A[y0:y1,x0:x1]
    
    return B


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
    Fx = 2/8
    Fy = 2/8
    print('Running Test:')
    print('building wavefront...')
    w = build_gauss_wavefront(Nx,Ny,Nz,eMin/1000,xMin,xMax,yMin,yMax,1,1e-6,1e-6,1) 
    
    wf0 = Wavefront(srwl_wavefront=w)
    
    # wf = wf0.toComplex()
    
    """From pickled wavefield """
    path ='/data/YDStest/13nm/' # '/home/jerome/Documents/MASTERS/data/YDStest/13nm/wavefieldME_TEST_500um_.pkl' #'/home/jerome/dev/wavefieldME_TEST_500um_.pkl'
    waveName = path + 'wavefieldME_TEST_200um_.pkl'
    print("-----Loading Wavefield-----")
    wf = fromPickle(waveName,True)
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
    
    """Mutual Intensity """
    mutualIntensity(wf, Fx, Fy, pathCP, pathJP, pathJ)
    
    
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
if __name__ == '__main__':
    test()
