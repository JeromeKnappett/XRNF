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
import wfStokes
import scipy.ndimage

from wpg.wavefront import Wavefront

try:
    from wpg.srw import srwlpy as srwl
except ImportError:
    import srwlpy as srwl

import time
import math

from wpg.srwlib import *

from math import log10, floor

# %%
def round_sig(x, sig=2):
    if x != 0:
        return round(x, sig-int(floor(log10(abs(x))))-1)
    else:
            return x


# plt.style.use(['science','ieee'])

# %%    
def Coherence(wfr, Fx = 1/3, Fy = 1/3, pathX = None, pathY = None, pathC = None, pathCL = None, pathI = None):
    """
    Calculate the longitudinal correlation of a single slice of a wavefront
    of shape [nx, ny] 
    
    params:
    wfr: wavefield
    Fx: Fraction of wavefield to sample in Horizontal
    Fy: Fraction of wavefield to sample in Vertical
    path... : Path names to save plots
    
    returns: 
    B: mutual coherence function
    Dx: pixel dimension of wavefield (horizontal)
    Dy: pixel dimension of wavefield (vertical)
    """
    
    print("----Starting Coherence Function---")
    
    Sx = int(Fx*wfr.params.Mesh.nx)
    Sy = int(Fy*wfr.params.Mesh.ny)
    print("Sampled area (pixels): {}".format([Sx,Sy]))
        
    #if Sx > 120 or Sy > 120:
    #    print("Error: Sampled area of wavefront is too large. Change Fx/Fy to a smaller value")
    #    import sys
    #    sys.exit()
    
    start1 = time.time()
    cfr = getComplex(wfr)
    print("Shape of Complex Wavefield: {}".format(np.shape(cfr)))
    end1 = time.time()
    print('Time taken to convert to complex wavefield (s): {}'.format(end1 - start1))
    
    _x0 = 0 # These are in _pixel_ coordinates!!
    _y0 = 0
    _x1 = int(np.max(np.shape(cfr[:,0,0]))) # These are in _pixel_ coordinates!!
    _y1 = int(np.max(np.shape(cfr[0,:,0])))
    
    print("Nx (pixels): {}".format(_x1))
    print("Ny (pixels): {}".format(_y1))
    
    numx = _x1 - _x0 # number of points for line profile
    numy = _y1 - _y0
    midX = int(numx/2)
    midY = int(numy/2)
    
    print("mid x: {}".format(midX))
    print("mid y: {}".format(midY))

    # # Fraction of wavefront to calculate coherence over
    # Fx = 1/3
    # Fy = 1/3
    
    ROI = ((int(midX-((Fx)*midX)),int(midY-((Fy)*midY))),
           (int(midX+((Fx)*midX)),int(midY+((Fy)*midY)))) 
    
    lX = ROI[1][0]-ROI[0][0]
    lY = ROI[1][1]-ROI[0][1]
    
    print("Region of interest (pixels): {}".format((lX,lY)))
    
    x0,y0 = ROI[0][0], ROI[0][1]
    x1,y1 = ROI[1][0], ROI[1][1]
   
    A = cfr[y0:y1,x0:x1]
    
    A_x1 = int(np.max(np.shape(A[:,0,0]))) # These are in _pixel_ coordinates!!
    A_y1 = int(np.max(np.shape(A[0,:,0])))
    
    print("Nx (pixels): {}".format(_x1))
    print("Ny (pixels): {}".format(_y1))
    
    Anumx = A_x1 # number of points for line profile
    Anumy = A_y1
    AmidX = int(Anumx/2)
    AmidY = int(Anumy/2)
    
    
    """ Cross Spectral Density (W) & Mutual Intensity Functions (Jx,Jy) """
    start2 = time.time()
    B = np.array([A.conjugate() * a for a in A.flatten()])#[:,:,:,0] 
    Bx = np.array([A[:,AmidY].conjugate() * a for a in A[:,AmidY]])
    By = np.array([A[AmidX,:].conjugate() * a for a in A[AmidX,:]])
    end2 = time.time()
    print('Time taken to calculate Mutual Intensity [J] (s): {}'.format(end2 - start2))
    
    print("Shape of B: {}".format(np.shape(B)))
    print("Shape of Bx: {}".format(np.shape(Bx)))
    print("Shape of By: {}".format(np.shape(By)))
    
    C = abs(B.mean(0))
    # Cx = abs(Bx.mean(0))
    # Cy = abs(By.mean(0))
    
    print("Shape of C: {}".format(np.shape(C)))
    # print("Shape of Cx: {}".format(np.shape(Cx)))
    # print("Shape of Cy: {}".format(np.shape(Cy)))
    
    
    # if wfr is Wavefront():
    Dx = Fx*wfr.params.Mesh.xMax - Fx*wfr.params.Mesh.xMin
    Dy = Fy*wfr.params.Mesh.yMax - Fy*wfr.params.Mesh.yMin
    # # else:
    # #     Dx = Fx*wfr.mesh.xFin - Fx*wfr.mesh.xStart
    # #     Dy = Fy*wfr.mesh.yfin - Fy*wfr.mesh.yStart
    
    
    """ Creating array of custom tick markers for plotting """
    tickAx = [round_sig(-Dx*1e6/2),round_sig(-Dx*1e6/4),0,round_sig(Dx*1e6/4),round_sig(Dx*1e6/2)]
    tickAy = [round_sig(Dy*1e6/2),round_sig(Dy*1e6/4),0,round_sig(-Dy*1e6/4),round_sig(-Dy*1e6/2)]
    
    print("Array of horizontal markers: {}".format(tickAx))
    print("Array of vertical markers: {}".format(tickAy))
    
    plt.imshow(abs(Bx))#,vmin=np.min(C),vmax=np.max(C))
    plt.title("Mutual Intensity (x1-x0)")
    plt.colorbar()
    plt.xticks(np.arange(0,lX+1,lX/4),tickAx)
    plt.yticks(np.arange(0,lY+1,lY/4),tickAy)
    plt.xlabel("Horizontal Position [\u03bcm]")#"(\u03bcm)")
    plt.ylabel("Vertical Position [\u03bcm]")#"(\u03bcm)")
    if pathX != None:
        print("Saving (x1-x0) figure to path: {}".format(pathX))
        plt.savefig(pathX)
    plt.show()
    plt.clf()   
    
    plt.imshow(abs(By))#,vmin=np.min(C),vmax=np.max(C))
    plt.title("Mutual Intensity (y1-y0)")
    plt.colorbar()
    plt.xticks(np.arange(0,lX+1,lX/4),tickAx)
    plt.yticks(np.arange(0,lY+1,lY/4),tickAy)
    plt.xlabel("Horizontal Position [\u03bcm]")#" (\u03bcm)")
    plt.ylabel("Vertical Position [\u03bcm]")#"(\u03bcm)")
    if pathY != None:
        print("Saving (y1-y0) figure to path: {}".format(pathY))
        plt.savefig(pathY)
    plt.show()   
    plt.clf()    

    """ Normalised Degree of Coherence """
    U = (abs((C)/(A.conjugate()*A)))
    
    
    """ Taking line profiles through U """
    X = U[0:int(np.max(np.shape(U[:,0]))), int((y1-y0)/2)]
    Y = U[int((x1-x0)/2), 0:int(np.max(np.shape(U[0,:])))]
    
    # print(x0,x1)
    # print(y0,y1)
    
    
    print("Sampled area dimensions (m): {}".format([Dx,Dy]))
    
    pX = Dx/lX
    pY = Dy/lY
    
    print("Pixel size (m): {}".format([pX,pY]))
    print("Shape of U (pixels): {}".format(np.shape(U)))
    
    
    """Plotting"""
    plt.imshow(1/U) # ,vmin=0,vmax=1)
    plt.title("Degree of Coherence (1/\u03bc)")
    plt.colorbar()
    plt.xticks(np.arange(0,lX+1,lX/4),tickAx)
    plt.yticks(np.arange(0,lY+1,lY/4),tickAy)
    plt.xlabel("Horizontal Position [\u03bcm]")#"(\u03bcm)")
    plt.ylabel("Vertical Position [\u03bcm]")#"(\u03bcm)")
    if pathC != None:
        print("Saving Degree of Coherence figure to path: {}".format(pathC))
        plt.savefig(pathC)
    plt.show()
    plt.clf()   
    
    plt.plot(X, label="Horizontal Profile")
    plt.plot(Y, label="Vertical Profile")
    plt.xticks(np.arange(0,lX+1,lX/4),tickAx)
    plt.xlabel("Horizontal Position [\u03bcm]")#"(\u03bcm)")
    plt.ylim(0,1.1)
    if pathCL != None:
        print("Saving line profile figure to path: {}".format(pathCL))
        plt.savefig(pathCL)
    # locs, labels = plt.xticks()
    # labels = [round(float(item)*pX*1e7, 2 - int(math.floor(math.log10(abs(float(item)*pX*1e7)))) - 1) for item in locs]
    # plt.xticks(locs, labels)
    plt.legend()
    
    # round(float(item)*pX*1e7, 2 - int(math.floor(math.log10(abs(float(item)*pX*1e7)))) - 1)
    plt.show()
    plt.clf()    

    # print('coherence array shape: {}'.format(np.shape(B)))
    # plt.plot(B)
    # plt.show()
    
    # D = np.reshape(B,())
    
    plt.imshow(abs(A.conjugate()*A))
    plt.title("intensity")
    plt.xticks(np.arange(0,lX+1,lX/4),tickAx)
    plt.yticks(np.arange(0,lY+1,lY/4),tickAy)
    plt.xlabel("Horizontal Position [\u03bcm]")#"(\u03bcm)")
    plt.ylabel("Vertical Position [\u03bcm]")#"(\u03bcm)")
    plt.colorbar()
    if pathI != None:
        print("Saving intensity figure to path: {}".format(pathI))
        plt.savefig(pathI)
    plt.show()
    plt.clf()

    return B ,Dx, Dy

# %%
def coherenceProfiles(wfr, Fx = 1/3, Fy = 1/3):
    """
    Calculate the horizontal and vertical profiles of the spatial coherence 
    of a single slice of a wavefront of shape [nx, ny] 
    
    :param wfr:  wavefield
    :plots horizontal and vertical coherence profiles
    """
    
    print("----Starting coherenceProfiles Function---")
    
    Sx = int(Fx*wfr.params.Mesh.nx)
    Sy = int(Fy*wfr.params.Mesh.ny)
    print("Sampled area (pixels): {}".format([Sx,Sy]))
        
    #if Sx > 120 or Sy > 120:
    #    print("Error: Sampled area of wavefront is too large. Change Fx/Fy to a smaller value")
    #    import sys
    #    sys.exit()
    
    start1 = time.time()
    cfr = getComplex(wfr)
    end1 = time.time()
    print('Time taken to convert to complex wavefield (s): {}'.format(end1 - start1))
    
    _x0 = 0 # These are in _pixel_ coordinates!!
    _y0 = 0
    _x1 = int(np.max(np.shape(cfr[:,0,0]))) # These are in _pixel_ coordinates!!
    _y1 = int(np.max(np.shape(cfr[0,:,0])))
    
    print("Nx (pixels): {}".format(_x1))
    print("Ny (pixels): {}".format(_y1))
    
    numx = _x1 - _x0 # number of points for line profile
    numy = _y1 - _y0
    midX = int(numx/2)
    midY = int(numy/2)
    
    print("midX & midY : {}".format((midX,midY)))
    
    # # Fraction of wavefront to calculate coherence over
    # Fx = 1/3
    # Fy = 1/3
    
    ROI = ((int(midX-((Fx)*midX)),int(midY-((Fy)*midY))),
            (int(midX+((Fx)*midX)),int(midY+((Fy)*midY)))) 
    
    lX = ROI[1][0]-ROI[0][0]
    lY = ROI[1][1]-ROI[0][1]
    
    print("Region of interest (pixels): {}".format((lX,lY)))
    
    x0,y0 = ROI[0][0], ROI[0][1]
    x1,y1 = ROI[1][0], ROI[1][1]
    
    print("Region of interest again (x0,x1,y0,y1):{},{}".format((x0,x1),(y0,y1)))
   
    A = cfr[x0:x1,y0:y1]
    
    print("Shape of sampled array A: {}".format(np.shape(A)))
    
    """ Mutual Coherence Function """
    start2 = time.time()
    Bx = np.array([A[:,int(lY/2)].conjugate() * a for a in A[:,int(lY/2)]])
    By = np.array([A[int(lX/2),:].conjugate() * a for a in A[int(lX/2),:]])
    end2 = time.time()
    print('Time taken to calculate coherence (s): {}'.format(end2 - start2))
    
    print("Shape of Bx: {}".format(np.shape(Bx)))
    print("Shape of By: {}".format(np.shape(By)))
    
    
    Dx = Fx*wfr.params.Mesh.xMax - Fx*wfr.params.Mesh.xMin
    Dy = Fy*wfr.params.Mesh.yMax - Fy*wfr.params.Mesh.yMin
    
    """ Creating array of custom tick markers for plotting """
    tickAx = [round_sig(-Dx*1e6/2),round_sig(-Dx*1e6/4),0,round_sig(Dx*1e6/4),round_sig(Dx*1e6/2)]
    tickAy = [round_sig(Dy*1e6/2),round_sig(Dy*1e6/4),0,round_sig(-Dy*1e6/4),round_sig(-Dy*1e6/2)]
    
    # print("Array of horizontal markers: {}".format(tickAx))
    # print("Array of vertical markers: {}".format(tickAy))
    
    plt.imshow(abs(Bx))
    plt.title("(x0-x1)")
    plt.xticks(np.arange(0,lX+1,lX/4),tickAx)
    plt.xlabel("x1-x0 [\u03bcm]")#"(\u03bcm)")
    plt.yticks(np.arange(0,lY+1,lY/4),tickAy)
    plt.ylabel("x1-x0 [\u03bcm]")#"(\u03bcm)")
    plt.colorbar()
    plt.show() 
    
    plt.imshow(abs(By))
    plt.title("(y0-y1)")
    plt.xticks(np.arange(0,lX+1,lX/4),tickAx)
    plt.xlabel("y1-y0 [\u03bcm]")#"(\u03bcm)")
    plt.yticks(np.arange(0,lY+1,lY/4),tickAy)
    plt.ylabel("y1-y0 [\u03bcm]")#"(\u03bcm)")
    plt.colorbar()
    plt.show()

    
    # Cx = abs(Bx.mean(0))
    # Cy = abs(By.mean(0))
    
    # plt.imshow(Cx)#,vmin=np.min(C),vmax=np.max(C))
    # plt.title("Degree of Coherence (Horizontal) (mean)")
    # plt.colorbar()
    # plt.show()   
    
    # plt.imshow(Cy)#,vmin=np.min(C),vmax=np.max(C))
    # plt.title("Degree of Coherence (Horizontal) (mean)")
    # plt.colorbar()
    # plt.show()   
    
    # """ Normalised Degree of Coherence """
    # U = (abs(B.mean(0))/(abs(A.conjugate()*A)))
    
# %%    
def plotCoherence(B,Dx,Dy, pathCm = None, pathCmL = None):
    
    print("----Starting plotCoherence Function---")
    
    # print('Coherence shape (B): {}'.format(np.shape(B)))
    
    C = abs(B.mean(0))
    
    # print('Coherence shape (C): {}'.format(np.shape(C)))    
    
    
    ##-- Extract the line...
    ## Make a line with "num" points...
    
    x0 = 0 # These are in _pixel_ coordinates!!
    y0 = 0
    x1 = int(np.max(np.shape(C[:,0,0]))) # These are in _pixel_ coordinates!!
    y1 = int(np.max(np.shape(C[0,:,0])))
    
    z = np.max(np.shape(B[:,0,0,0]))
    
    numx = x1 - x0 # number of points for line profile
    numy = y1 - y0
    midX = int(numx/2)
    midY = int(numy/2)
    
    midZ = int(z/2)
    
    # print('midZ: {}'.format(midZ))
    
    # print("x0: {}".format(x0))
    # print("y0: {}".format(y0))
    # print("x1: {}".format(x1))
    # print("y1: {}".format(y1))
    
    # print('numx: {}'.format(numx))
    # print('numy: {}'.format(numy))
    # print('midX: {}'.format(midX))
    # print('midY: {}'.format(midY))
    
    
    X = C[x0:x1, midY]
    Y = C[midX, y0:y1]

    
    #-- Plot...
    """ Creating array of custom tick markers for plotting """
    tickAx = [round_sig(-Dx*1e6/2),round_sig(-Dx*1e6/4),0,round_sig(Dx*1e6/4),round_sig(Dx*1e6/2)]
    tickAy = [round_sig(Dy*1e6/2),round_sig(Dy*1e6/4),0,round_sig(-Dy*1e6/4),round_sig(-Dy*1e6/2)]
    
    
    plt.imshow(C)#,vmin=np.min(C),vmax=np.max(C))
    plt.title("Degree of Coherence (mean)")
    plt.colorbar()
    plt.xticks(np.arange(0,x1+1,x1/4),tickAx)
    plt.yticks(np.arange(0,y1+1,y1/4),tickAy)
    plt.xlabel("Horizontal Position [\u03bcm]")#"(\u03bcm)")
    plt.ylabel("Vertical Position [\u03bcm]")#"(\u03bcm)")
    if pathCm != None:
        print("Saving Coherence (mean) figure to path: {}".format(pathCm))
        plt.savefig(pathCm)
    plt.show()   
    plt.clf()
    
    # plt.imshow(abs(B.std(0)))#,vmin=np.min(C),vmax=np.max(C))
    # plt.title("STD - Degree of Coherence (Standard Deviation)")
    # plt.colorbar()
    # plt.show()   
    
    # plt.imshow(abs(B[midZ]))#,vmin=np.min(C),vmax=np.max(C))
    # plt.title("Degree of Coherence (middle slice)")
    # plt.colorbar()
    # plt.show()
    
    
    plt.plot(X, label="Horizontal Profile")
    plt.plot(Y, label="Vertical Profile")
    plt.xticks(np.arange(0,x1+1,x1/4),tickAx)
    plt.xlabel("Position [\u03bcm]")
    plt.legend()
    if pathCmL != None:
        print("Saving figure to path: {}".format(pathCmL))
        plt.savefig(pathCmL)
    plt.show()
    plt.clf()

# %%
def getComplex(w):
    """ 
    Give the complex representation of a wavefield
    w: scalar wavefield
    returns:
        cwf: complex wavefield
    """
    re = w.get_real_part()      # get real part of wavefield
    im = w.get_imag_part()      # get imaginary part of wavefield
    
    
    print("Shape of real part of wavefield: {}".format(np.shape(re)))
    print("Shape of imaginary part of wavefield: {}".format(np.shape(im)))
    
    # print("real part:")
    # print(re)
    # print("imaginary part:")
    # print(im)
    
    cwf = re + im*1j
    
    print("Shape of complex wavefield: {}".format(np.shape(cwf)))
    # print("Complex Wavefield:")
    # print(cwf)
    
    return cwf

# %%
def test():
    eMin = 10e6
    Nx = 150
    Ny = 150
    Nz = 1
    xMin = -10e-6
    xMax = 10e-6
    yMin = -10e-6
    yMax = 10e-6
    zMin = 100
    Fx = 1/2
    Fy = 1/2
    print('Running Test:')
    print('building wavefront...')
    w = build_gauss_wavefront(Nx,Ny,Nz,eMin/1000,xMin,xMax,yMin,yMax,1,1e-6,1e-6,1) 
    
    wf0 = Wavefront(srwl_wavefront=w)
    
    wf = wf0.toComplex()
    
    # g = build_gauss_wavefront(Nx,Ny,Nz, eMin/1000,xMin,xMax,yMin,yMax,1,2e-6,2e-6,1)
    
    # gf0 = Wavefront(srwl_wavefront=g)    
    # gf = gf0.toComplex()
    
    # COH = getCoherence(wf0)
    # C = abs(COH)
    
    # print(C)
    # plt.imshow(C)
    # plt.colorbar()
    # plt.show()
    
    B, Dx , Dy = Coherence(wf0,Fx,Fy)
    plotCoherence(B,Dx,Dy)
    coherenceProfiles(wf0,Fx,Fy)

# %%
def test_multi():
    
    """DEFINING ELECTRON BEAM"""
    elecBeam = SRWLPartBeam()
    elecBeam.Iavg = 0.2 #Average Current [A]
    elecBeam.partStatMom1.x = 0. #Initial Transverse Coordinates (initial Longitudinal Coordinate will be defined later on) [m]
    elecBeam.partStatMom1.y = 0.
    elecBeam.partStatMom1.z = 0. #-0.5*undPer*(numPer + 4) #Initial Longitudinal Coordinate (set before the ID)
    elecBeam.partStatMom1.xp = 0 #Initial Relative Transverse Velocities
    elecBeam.partStatMom1.yp = 0
    elecBeam.partStatMom1.gamma = 7./0.51099890221e-03 #Relative Energy
    #2nd order statistical moments
    elecBeam.arStatMom2[0] = (118.027e-06)**2 #<(x-x0)^2>
    elecBeam.arStatMom2[1] = 0
    elecBeam.arStatMom2[2] = (27.3666e-06)**2 #<(x'-x'0)^2>
    elecBeam.arStatMom2[3] = (15.4091e-06)**2 #<(y-y0)^2>
    elecBeam.arStatMom2[4] = 0
    elecBeam.arStatMom2[5] = (2.90738e-06)**2 #<(y'-y'0)^2>
    elecBeam.arStatMom2[10] = (1e-03)**2 #<(E-E0)^2>/E0^2
    
    """DEFINING UNDULATOR"""
    numPer = 72.5 #Number of ID Periods (without counting for terminations
    undPer = 0.033 #Period Length [m]
    Bx = 0 #Peak Horizontal field [T]
    By = 0.3545 #Peak Vertical field [T]
    phBx = 0 #Initial Phase of the Horizontal field component
    phBy = 0 #Initial Phase of the Vertical field component
    sBx = 1 #Symmetry of the Horizontal field component vs Longitudinal position
    sBy = -1 #Symmetry of the Vertical field component vs Longitudinal position
    xcID = 0 #Transverse Coordinates of Undulator Center [m]
    ycID = 0
    zcID = 1.25 #0 #Longitudinal Coordinate of Undulator Center wit hrespect to Straight Section Center [m]
        
    
    """DEFINING INITIAL WAVEFRONT"""
    wfr2 = SRWLWfr() #For intensity distribution at fixed photon energy
    wfr2.allocate(1, 101, 101) #Numbers of points vs Photon Energy, Horizontal and Vertical Positions
    wfr2.mesh.zStart = 36.25 + 1.25 #Longitudinal Position [m] from Center of Straight Section at which SR has to be calculated
    wfr2.mesh.eStart = 8830 #Initial Photon Energy [eV]
    wfr2.mesh.eFin = 8830 #Final Photon Energy [eV]
    wfr2.mesh.xStart = -0.0015 #Initial Horizontal Position [m]
    wfr2.mesh.xFin = 0.0015 #Final Horizontal Position [m]
    wfr2.mesh.yStart = -0.0006 #Initial Vertical Position [m]
    wfr2.mesh.yFin = 0.0006 #Final Vertical Position [m]
    meshInitPartCoh = deepcopy(wfr2.mesh)
    
    wfr2.partBeam = elecBeam
        
    
    und = SRWLMagFldU([SRWLMagFldH(1, 'v', By, phBy, sBy, 1), SRWLMagFldH(1, 'h', Bx, phBx, sBx, 1)], undPer, numPer) #Ellipsoidal Undulator
    magFldCnt = SRWLMagFldC([und], array('d', [xcID]), array('d', [ycID]), array('d', [zcID])) #Container of all Field Elements
    

    nMacroElec = 2 #total number of macro-electrons
    nMacroElecAvgPerProc = 1 #number of macro-electrons / wavefront to average on worker processes before sending data to master (for parallel calculation only)
    nMacroElecSavePer = 60 #intermediate data saving periodicity (in macro-electrons)
    srCalcMeth = 1 #SR calculation method
    srCalcPrec = 0.01 #SR calculation rel. accuracy



    #****************************Input Parameters:
    strExDataFolderName = 'coherence_test' #example data sub-folder name
    strIntOutFileNamePartCoh = 'part_coh1.dat' #file name for output SR intensity data


    #***********Precision Parameters for SR calculation
    sampFactNxNyForProp = 0.25 #sampling factor for adjusting nx, ny (effective if > 0)
    
    optDrift = SRWLOptD(1) #Drift space
    
    optBL = SRWLOptC([optDrift]) #"Beamline" - Container of Optical Elements (together with the corresponding wavefront propagation instructions)



    # multiEField = srwl_wfr_emit_prop_multi_e(_e_beam, _mag, _mesh, _sr_meth, _sr_rel_prec, _n_part_tot, _n_part_avg_proc=1, _n_save_per=100,
    #                                _file_path=None, _sr_samp_fact=-1, _opt_bl=None, _pres_ang=0, _char=0, _x0=0, _y0=0, _e_ph_integ=0,
    #                                _rand_meth=1, _tryToUseMPI=True, _wr=0., _wre=0., _det=None, _me_approx=0, _file_bkp=False)
    
    w = srwl_wfr_emit_prop_multi_e(elecBeam, magFldCnt,
                                    meshInitPartCoh, srCalcMeth,
                                    srCalcPrec, nMacroElec,
                                    nMacroElecAvgPerProc, nMacroElecSavePer,
                                    os.path.join(os.getcwd(), strExDataFolderName, strIntOutFileNamePartCoh),
                                    sampFactNxNyForProp, optBL,
                                    _pres_ang=0, _char=20)
    
    wf = SRWLWfr(w)
    
    s = np.reshape(w.arS,(4,w.mesh.nx,w.mesh.ny))
    
    s0 = np.reshape(s[0,:,:],(w.mesh.nx,w.mesh.ny))
    s1 = np.reshape(s[1,:,:],(w.mesh.nx,w.mesh.ny))
    s2 = np.reshape(s[2,:,:],(w.mesh.nx,w.mesh.ny))
    s3 = np.reshape(s[3,:,:],(w.mesh.nx,w.mesh.ny))
    
    S = s0, s1, s2, s3
    
    print("shape of s0: {}".format(np.shape(s0)))
    
    
    print("Shape of electric field data: {}".format(np.shape(w.arS)))
    plt.plot(np.array(w.arS))
    plt.show()
    
    plt.plot(s0)
    plt.show()
    plt.plot(s1)
    plt.show()
    plt.plot(s2)
    plt.show()
    plt.plot(s3)
    plt.show()
    
    # print ('-----Getting Stokes Parameters-----')
    # start1= time.time()
    # # S= Stokes.getStokes(wf,1, 1/18,1/3)
    # s = Stokes.getStokesParamFromStokes(w)
    # _s = Stokes.normaliseStoke(s)
    # end1 = time.time()
    # print('Time taken to get Stokes parameters (s): {}'.format(end1 - start1))
    
    # print("-----Plotting Stokes parameters-----")
    # Stokes.plotStokes(s,w)

    # print("-----Plotting normalised Stokes parameters-----")
    # Stokes.plotStokes(_s,w,'_s0','_s1','_s2','_s3')
    
    # print("-----Getting degree of coherence from Stokes-----")
    # start2 = time.time()
    # Stokes.coherenceFromSTKS(w)
    # end2 = time.time()
    # print('Time taken to get Coherence from Stokes parameters (s): {}'.format(end2 - start2))
    
    
    # plt.imshow(eField_pc)
    # plt.show()

# param _char: radiation characteristic to calculate:
#         0- Total Intensity, i.e. Flux per Unit Surface Area (s0);
#         1- Four Stokes components of Flux per Unit Surface Area;
#         2- Mutual Intensity Cut vs X;
#         3- Mutual Intensity Cut vs Y;
#         4- Mutual Intensity Cuts and Degree of Coherence vs X & Y;
#         10- Flux
#         20- Electric Field (sum of fields from all macro-electrons, assuming CSR)
#         40- Total Intensity, i.e. Flux per Unit Surface Area (s0), Mutual Intensity Cuts and Degree of Coherence vs X & Y;
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
    # test_multi()
