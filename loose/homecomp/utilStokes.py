# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 12:32:22 2021

@author: jerome
"""

# %%
#from wpg.wavefront import Wavefront
from wpg.generators import build_gauss_wavefront
from wpg.srwlib import SRWLStokes, SRWLWfr
import numpy as np
import matplotlib.pyplot as plt
import time
from wpg.wavefront import Wavefront

from math import log10, floor

def round_sig(x, sig=2):
    if x != 0:
        return round(x, sig-int(floor(log10(abs(x))))-1)
    else:
            return x


def getPolarisationCharacteristics(S=None,Sparam=None):
    ''''
    Return the degree of polarization, 
            degree of polarization averaged over wavefront, 
            the eccentricity, 
            orientation,  and 
            chirality 
    of the polarization ellipse.
    '''
    
    
    if S is not None:
        s0,s1,s2,s3 = getStokesParamFromStokes(S)
    else:
        if Sparam is not None:
            s0, s1, s2, s3 = Sparam
        else:
            raise ValueError("S and Sparam both None")

    # degree of polarization.  Alternatively, we could use D = Ip/(Ip + Itot) where Ip is the polarised intensity and It is the total intensity.
    D = (np.sqrt((s1**2 + s2**2 + s3**2)))/s0
    
    Davg = np.mean(D)

    # eccentricity.  e = 1 => linear polarization (no chirality) 
    e = np.sqrt(s2*np.sqrt(s1**2 + s2**2)/(1+np.sqrt(s1**2 + s2**2))) # added sqrt - jerome
    
    #making sure eccentricity agrees with s3
    # e_3 = (2*(-1 + s3**2 + np.sqrt(-1*(1 - s3**2))))/(s3**2)
    # print('Eccentricity from s3 = {}'.format(e_3))
    
    # inclination of polarization ellipse (radians)
    i = 0.5*np.arctan(s2/s1)

    # chirality, c, defined for convenience 
    s3m = np.mean(s3)
    if s3m < 0:
        c = 'ccw'
    if s3m >0:
        c = 'cw'
    if s3m ==0:
        c = None


    
    return D, Davg, e, i, c


def deg_pol(S):
    ''''
    Return the degree of polarization,  
            the eccentricity, 
            orientation, and 
            chirality 
    of the polarization ellipse.
    '''
    
    
    s0,s1,s2,s3 = S

    if type is 'linear':
        D = (np.sqrt((s1**2 + s2**2 + s3**2)))/s0
    
    return D


def getStokesParamFromStokes(stk, d=2):
    
    nTot = stk.mesh.nx*stk.mesh.ny*stk.mesh.ne
    # print('nTot before reshape: {}'.format(nTot))
    # print('arS shape : {}'.format(np.shape(stk.arS)))
    
    # plt.plot(stk.arS)
    # plt.title('arS')
    # plt.show()
    
    
    if stk.mutual > 0 :
        
        # print("TESTING IF ARRAY IS REPEATED (1-3)...")
        # s = np.reshape(stk.arS,(2,int(np.size(stk.arS)/2)))
        # print(np.nonzero(s[0]-s[1]))
        # plt.plot(s[0],label="1st")
        # plt.plot(s[1],label="2nd")
        # plt.legend()
        # plt.show()
        
        # print("TESTING IF ARRAY IS REPEATED AGAIN (neighbours)...")
        # s = np.reshape(stk.arS,(int(np.size(stk.arS)/2),2))
        # print(np.nonzero(s[:,0]-s[:,1]))
        # plt.plot(s[:,0],label="1st")
        # plt.plot(s[:,1],label="2nd")
        # plt.legend()
        # plt.show()
        
        
        # # s = np.reshape(stk.arS,(4,nTot,stk.mesh.nx,stk.mesh.ny,1))
        # s = np.reshape(stk.arS,(4,int(np.size(stk.arS)/4)))
        # print('stk.arS shape after reshape: {}'.format(np.shape(s)))
        # print("TESTING IF ARRAY IS REPEATED AGAIN (1-2)...")
        # print(np.nonzero(s[0]-s[1]))
        # plt.plot(s[0],label="1st")
        # plt.plot(s[1],label="2nd")
        # plt.legend()
        # plt.show()
        # plt.plot(s[0,:])
        # plt.title('S0')
        # plt.show()
        
        s = np.reshape(stk.arS,(4,int(np.size(stk.arS)/4)))
        # s0 = np.reshape(s[0,:,:],(stk.mesh.nx,stk.mesh.ny))
        
        S0 = np.reshape(s[0,:],(nTot,stk.mesh.nx,stk.mesh.ny,2))
        S1 = np.reshape(s[1,:],(nTot,stk.mesh.nx,stk.mesh.ny,2))
        S2 = np.reshape(s[2,:],(nTot,stk.mesh.nx,stk.mesh.ny,2))
        S3 = np.reshape(s[3,:],(nTot,stk.mesh.nx,stk.mesh.ny,2))

        
        _s0 = S0.mean(3)
        _s1 = S1.mean(3)
        _s2 = S2.mean(3)
        _s3 = S3.mean(3)
        
        # plt.imshow(_s0[int(stk.mesh.nx/2),:,:])
        # plt.title("TEST")
        # plt.show()
                
        # print("Shape of 1st average of S0: {}".format(np.shape(_s0)))
        
        s0 = abs(_s0.mean(0))
        s1 = abs(_s1.mean(0))
        s2 = abs(_s2.mean(0))
        s3 = abs(_s3.mean(0))
        return s0, s1, s2, s3
        # print("shape of 2nd averag of S0: {}".format(np.shape(s0)))
        
        # s0 = np.reshape(s[0,:,:],(stk.mesh.nx**2,stk.mesh.ny**2))

        
    
    else:
        if d == 1:
            s = np.reshape(stk.arS,(4,stk.mesh.ny,stk.mesh.nx))
        
            s0x = np.reshape(s[0,:,:],(stk.mesh.ny,stk.mesh.nx))[int(stk.mesh.ny/2),:]
            s1x = np.reshape(s[1,:,:],(stk.mesh.ny,stk.mesh.nx))[int(stk.mesh.ny/2),:]
            s2x = np.reshape(s[2,:,:],(stk.mesh.ny,stk.mesh.nx))[int(stk.mesh.ny/2),:]
            s3x = np.reshape(s[3,:,:],(stk.mesh.ny,stk.mesh.nx))[int(stk.mesh.ny/2),:]
        
            s0y = np.reshape(s[0,:,:],(stk.mesh.ny,stk.mesh.nx))[:,int(stk.mesh.nx/2)]
            s1y = np.reshape(s[1,:,:],(stk.mesh.ny,stk.mesh.nx))[:,int(stk.mesh.nx/2)]
            s2y = np.reshape(s[2,:,:],(stk.mesh.ny,stk.mesh.nx))[:,int(stk.mesh.nx/2)]
            s3y = np.reshape(s[3,:,:],(stk.mesh.ny,stk.mesh.nx))[:,int(stk.mesh.nx/2)]
            
            print("Shape of s0x:{}".format(np.shape(s0x)))
            print("Shape of s1x:{}".format(np.shape(s1x)))
            print("Shape of s2x:{}".format(np.shape(s2x)))
            print("Shape of s3x:{}".format(np.shape(s3x)))
            print("Shape of s0y:{}".format(np.shape(s0y)))
            print("Shape of s1y:{}".format(np.shape(s1y)))
            print("Shape of s2y:{}".format(np.shape(s2y)))
            print("Shape of s3y:{}".format(np.shape(s3y)))
            return s0x, s1x, s2x, s3x, s0y, s1y, s2y, s3y


        if d == 2:
            s = np.reshape(stk.arS,(4,stk.mesh.nx,stk.mesh.ny))
        
            s0 = np.reshape(s[0,:,:],(stk.mesh.nx,stk.mesh.ny))
            s1 = np.reshape(s[1,:,:],(stk.mesh.nx,stk.mesh.ny))
            s2 = np.reshape(s[2,:,:],(stk.mesh.nx,stk.mesh.ny))
            s3 = np.reshape(s[3,:,:],(stk.mesh.nx,stk.mesh.ny))
            return s0, s1, s2, s3
        
    # print('S0 = {}'.format(np.shape(s0)))    
    # print('S1 = {}'.format(np.shape(s1)))    
    # print('S2 = {}'.format(np.shape(s2)))    
    # print('S3 = {}'.format(np.shape(s3)))
    

def getStokes(w, mutual=0, Fx = 1, Fy = 1):
        
    #if(isinstance(w, SRWLWfr) == False):
    #    w = SRWLWfr(w)
    stk = SRWLStokes()
    
    if mutual==0:
        stk.allocate(w.mesh.ne, w.mesh.nx, w.mesh.ny, _mutual = mutual) #numbers of points vs photon energy, horizontal and vertical positions
        stk.mesh.zStart = w.mesh.zStart #30. #longitudinal position [m] at which UR has to be calculated
        stk.mesh.eStart = w.mesh.eStart #initial photon energy [eV]
        stk.mesh.eFin = w.mesh.eFin #20000. #final photon energy [eV]
        stk.mesh.xStart = w.mesh.xStart #initial horizontal position of the collection aperture [m]
        stk.mesh.xFin = w.mesh.xFin #final horizontal position of the collection aperture [m]
        stk.mesh.yStart = w.mesh.yStart #initial vertical position of the collection aperture [m]
        stk.mesh.yFin = w.mesh.yFin #final vertical position of the collection aperture [m]  
        
    elif mutual > 0:
        
        # # Mid-point of wavefield mesh (assuming centered on 0)
        # midX = 0#(w.mesh.xFin + w.mesh.xStart)/2
        # midY = 0#(w.mesh.yFin + w.mesh.yStart)/2
        
        Sx = int(Fx*w.mesh.nx)
        Sy = int(Fy*w.mesh.ny)
        print("Sampled area (pixels): {}".format([Sx,Sy]))
        
        #if Sx > 76 or Sy > 76:
        #    print("Error: Sampled area of wavefront is too large. Change Fx/Fy to a smaller value")
        #    import sys
        #    sys.exit()
            
        stk.allocate(w.mesh.ne, int(Fx*(w.mesh.nx)), int(Fy*(w.mesh.ny)), _mutual = mutual) #numbers of points vs photon energy, horizontal and vertical positions
        stk.mesh.zStart = w.mesh.zStart #30. #longitudinal position [m] at which UR has to be calculated
        stk.mesh.eStart = w.mesh.eStart #initial photon energy [eV]
        stk.mesh.eFin = w.mesh.eFin #20000. #final photon energy [eV]
        stk.mesh.xStart = Fx*w.mesh.xStart   #initial horizontal position of the collection aperture [m]
        stk.mesh.xFin = Fx*w.mesh.xFin #final horizontal position of the collection aperture [m]
        stk.mesh.yStart = Fy*w.mesh.yStart #initial vertical position of the collection aperture [m]
        stk.mesh.yFin = Fy*w.mesh.yFin #final vertical position of the collection aperture [m]  
        
        # print("Stokes Dimensions (xStart,xFin,yStart,yFin):")
        # print(stk.mesh.xStart)
        # print(stk.mesh.xFin)
        # print(stk.mesh.yStart)
        # print(stk.mesh.yFin)
        
        # print("Wavefield Dimensions (xStart,xFin,yStart,yFin):")
        # print(w.mesh.xStart)
        # print(w.mesh.xFin)
        # print(w.mesh.yStart)
        # print(w.mesh.yFin)
        
    """ Getting sampled area [m]"""
    Dx = Fx*w.mesh.xFin - Fx*w.mesh.xStart
    Dy = Fx*w.mesh.yFin - Fx*w.mesh.yStart
    print("Sampled range (x,y) [m]:{}".format((Dx,Dy)))
    
    w.calc_stokes(stk)
    
    # print("mutual:")
    # print(stk.mutual)
    
    return stk, Dx ,Dy

def normaliseStoke(S):
    # print("STOKE SHAPE: {}".format(np.shape(S)))
    
    s0,s1,s2,s3 = S[0], S[1], S[2], S[3]
    
    _s0 = s0/s0
    _s1 = s1/s0
    _s2 = s2/s0
    _s3 = s3/s0

    _s = np.array([[_s0.mean(),_s1.mean(),_s2.mean(),_s3.mean()]]).T
    print("Normalised Stokes vector:")
    print(_s)
    
    return _s
    
def coherenceFromSTKS(S, Dx, Dy, pathCS = None, pathCSL = None):
    
    nTot = S.mesh.nx*S.mesh.ny*S.mesh.ne
    
    C = S.to_deg_coh()
    print("shape of coherence array: {}".format(np.shape(C)))
    
    # plt.plot(C)
    # plt.title('C')
    # plt.show()
    
    d = np.reshape(C,(nTot,S.mesh.nx,S.mesh.ny))
    print("shape of new coherence array: {}".format(np.shape(d)))
    
    dC = abs(d.mean(0))
    
    print("Shape of even newer Coherence array: {}:".format(np.shape(dC)))
    
    # print(np.nonzero(C))
    # plt.plot(C)
    # plt.show()
    
    
    Nx = int(np.squeeze(np.shape(dC[:][0])))
    Ny = int(np.squeeze(np.shape(dC[0][:])))
    
    """ Creating array of custom tick markers for plotting """
    tickAx = [round_sig(-Dx*1e6/2),round_sig(-Dx*1e6/4),0,round_sig(Dx*1e6/4),round_sig(Dx*1e6/2)]
    tickAy = [round_sig(Dy*1e6/2),round_sig(Dy*1e6/4),0,round_sig(-Dy*1e6/4),round_sig(-Dy*1e6/2)]
    
    
    plt.imshow(dC)
    plt.title("Degree of Coherence (from Stokes)")
    plt.xticks(np.arange(0,Nx+1,Nx/4),tickAx)
    plt.yticks(np.arange(0,Ny+1,Ny/4),tickAy)
    plt.xlabel("Horizontal Position [\u03bcm]")#"(\u03bcm)")
    plt.ylabel("Vertical Position [\u03bcm]")#"(\u03bcm)")
    plt.colorbar()
    if pathCS != None:
        print("Saving figure to path: {}".format(pathCS))
        plt.savefig(pathCS)
    plt.show()
    plt.clf()
    
    x0 = 0 # These are in _pixel_ coordinates!!
    y0 = 0
    x1 = int(np.max(np.shape(dC[:,0]))) # These are in _pixel_ coordinates!!
    y1 = int(np.max(np.shape(dC[0,:])))
    
    
    numx = x1 - x0 # number of points for line profile
    numy = y1 - y0
    midX = int(numx/2)
    midY = int(numy/2)
    
    X = dC[x0:x1, midY]
    Y = dC[midX, y0:y1]
    
    plt.plot(X, label="Horizontal Profile")
    plt.plot(Y, label="Vertical Profile")
    plt.legend()
    if pathCSL != None:
        print("Saving figure to path: {}".format(pathCSL))
        plt.savefig(pathCSL)
    plt.show()
    plt.clf()

    # cfr = w.toComplex()
    # A = cfr[x0:x1,y0:y1]
    # I = np.squeeze((abs(A.conjugate()*A)))
    
    # print("Shape of Intensity array: {}".format(np.shape(I)))
    
    # U = dC/I
    
    
    # print("Shape of U array: {}".format(np.shape(U)))
    
    # plt.imshow(U)
    # plt.title("Degree of Coherence (maybe)")
    # plt.colorbar()
    # plt.show()
    

def plotStokes(s,S,fig1='S0',fig2='S1',fig3='S2',fig4='S3', Dx=50e-6, Dy=50e-6,
               pathS0 = None, pathS1 = None, pathS2 = None, pathS3 = None,
               pathD = None, pathE = None, pathIn = None):
    
    print("Shape of S: {}".format(np.shape(S)))
    print("Shape of s: {}".format(np.shape(s)))
    
    Nx = int(np.squeeze(np.shape(s[0][:][0])))
    Ny = int(np.squeeze(np.shape(s[0][0][:])))
    
    print("Nx={}".format(Nx))
    print("Nx={}".format(Ny))
    
    """ Creating array of custom tick markers for plotting """
    tickAx = [round_sig(-Dx*1e6/2),round_sig(-Dx*1e6/4),0,round_sig(Dx*1e6/4),round_sig(Dx*1e6/2)]
    tickAy = [round_sig(Dy*1e6/2),round_sig(Dy*1e6/4),0,round_sig(-Dy*1e6/4),round_sig(-Dy*1e6/2)]
    
    
    print("plotting Stokes parameters (S0, S1, S2, S3)...")
    plt.imshow(s[0],vmin=np.min(s),vmax=np.max(s))
    plt.title(fig1)
    plt.xticks(np.arange(0,Nx+1,Nx/4),tickAx)
    plt.yticks(np.arange(0,Ny+1,Ny/4),tickAy)
    plt.xlabel("Horizontal Position [\u03bcm]")#"(\u03bcm)")
    plt.ylabel("Vertical Position [\u03bcm]")#"(\u03bcm)")
    if pathS0 != None:
        print("Saving S0 figure to path: {}".format(pathS0))
        plt.savefig(pathS0)
    plt.colorbar()
    plt.show()
    plt.clf()

    plt.imshow(s[1],vmin=np.min(s),vmax=np.max(s))
    plt.title(fig2)
    plt.xticks(np.arange(0,Nx+1,Nx/4),tickAx)
    plt.yticks(np.arange(0,Ny+1,Ny/4),tickAy)
    plt.xlabel("Horizontal Position [\u03bcm]")#"(\u03bcm)")
    plt.ylabel("Vertical Position [\u03bcm]")#"(\u03bcm)")
    if pathS1 != None:
        print("Saving S1 figure to path: {}".format(pathS1))
        plt.savefig(pathS1)
    plt.colorbar()
    plt.show()
    plt.clf()

    plt.imshow(s[2],vmin=np.min(s),vmax=np.max(s))
    plt.title(fig3)
    plt.xticks(np.arange(0,Nx+1,Nx/4),tickAx)
    plt.yticks(np.arange(0,Ny+1,Ny/4),tickAy)
    plt.xlabel("Horizontal Position [\u03bcm]")#"(\u03bcm)")
    plt.ylabel("Vertical Position [\u03bcm]")#"(\u03bcm)")   
    if pathS2 != None:
        print("Saving S2 figure to path: {}".format(pathS2))
        plt.savefig(pathS2)
    plt.colorbar()
    plt.show()
    plt.clf()

    plt.imshow(s[3],vmin=np.min(s),vmax=np.max(s))
    plt.title(fig4)
    plt.xticks(np.arange(0,Nx+1,Nx/4),tickAx)
    plt.yticks(np.arange(0,Ny+1,Ny/4),tickAy)
    plt.xlabel("Horizontal Position [\u03bcm]")#"(\u03bcm)")
    plt.ylabel("Vertical Position [\u03bcm]")#"(\u03bcm)")
    if pathS3 != None:
        print("Saving S3 figure to path: {}".format(pathS3))
        plt.savefig(pathS3)
    plt.colorbar()
    plt.show()
    plt.clf()
    
    D, Davg, e, i, c = getPolarisationCharacteristics(S=None,Sparam=s)
    
    print('Average degree of polarisation = {}'.format(Davg))
    print('Average ellipticity = {}'.format(np.mean(e)))
    print('Average inclination = {}'.format(np.mean(i)))
    print ('Chirality: {}'.format(c))
    

    plt.imshow(D)
    plt.title('Degree of polarization')
    plt.xticks(np.arange(0,Nx+1,Nx/4),tickAx)
    plt.yticks(np.arange(0,Ny+1,Ny/4),tickAy)
    plt.xlabel("Horizontal Position [\u03bcm]")#"(\u03bcm)")
    plt.ylabel("Vertical Position [\u03bcm]")#"(\u03bcm)")
    if pathD != None:
        print("Saving Deg of Pol figure to path: {}".format(pathD))
        plt.savefig(pathD)
    plt.colorbar()
    plt.show()
    plt.clf()    

    plt.imshow(e)
    plt.title('Ellipticity')
    plt.xticks(np.arange(0,Nx+1,Nx/4),tickAx)
    plt.yticks(np.arange(0,Ny+1,Ny/4),tickAy)
    plt.xlabel("Horizontal Position [\u03bcm]")#"(\u03bcm)")
    plt.ylabel("Vertical Position [\u03bcm]")#"(\u03bcm)")
    if pathE != None:
        print("Saving ellipticity figure to path: {}".format(pathE))
        plt.savefig(pathE)
    plt.colorbar()
    plt.show()
    plt.clf()
    
    plt.imshow(i)
    plt.title('Inclination')
    plt.xticks(np.arange(0,Nx+1,Nx/4),tickAx)
    plt.yticks(np.arange(0,Ny+1,Ny/4),tickAy)
    plt.xlabel("Horizontal Position [\u03bcm]")#"(\u03bcm)")
    plt.ylabel("Vertical Position [\u03bcm]")#"(\u03bcm)")
    if pathIn != None:
        print("Saving Inclination figure to path: {}".format(pathIn))
        plt.savefig(pathIn)
    plt.colorbar()
    plt.show()
    plt.clf()

# def plotElipse(S):
    
#     from py_pol.stokes import Stokes
    
#     s0,s1,s2,s3 = S

def plotStokesCuts(s):
    
    S0x = s[0]
    S1x = s[1]
    S2x = s[2]
    S3x = s[3]
    S0y = s[4]
    S1y = s[5]
    S2y = s[6]
    S3y = s[7]
    
    
    
    fig, axs = plt.subplots(2, 2)
    axs[0, 0].plot(S0y)
    axs[0, 0].set_title('S0: y-cut')
    axs[0, 1].plot(S1y)
    axs[0, 1].set_title('S1: y-cut')
    axs[1, 0].plot(S2y)
    axs[1, 0].set_title('S2: y-cut')
    axs[1, 1].plot(S3y)
    axs[1, 1].set_title('S3: y-cut')

    for ax in axs.flat:
        ax.set(xlabel="y position [pixels]", ylabel=" ")
    plt.show()
    plt.clf()
    
    fig, axs = plt.subplots(2, 2)
    axs[0, 0].plot(S0x)
    axs[0, 0].set_title('S0: x-cut')
    axs[0, 1].plot(S1x)
    axs[0, 1].set_title('S1: x-cut')
    axs[1, 0].plot(S2x)
    axs[1, 0].set_title('S2: x-cut')
    axs[1, 1].plot(S3x)
    axs[1, 1].set_title('S3: x-cut')

    for ax in axs.flat:
        ax.set(xlabel="x position [pixels]", ylabel=" ")
    plt.show()
    plt.clf()

def sumWaves(wavefronts, path=None, plots=None):
    """
    Parameters
    ----------
    wavefronts : 
        Array of hdf5 wavefront files

    path :
        Path to folder containing wavefront files.
        The default is None.
    
    plots :
        Path to save plots of each wavefront and resulting summed wavefront
    Returns
    -------
    wfr:
        SRWLWfr() wavefront which is the sum of all wavefronts.

    """
    #Setting up initial wavefield object to contain all summed wavefields
    wfr = SRWLWfr()
    
    stokeN = []
    stokeW = []
    degPolarisation = []
    degPolarisationAv = []
    
    for i, f in enumerate(wavefronts):
        print(" ")
        print('Loading wavefront #{} from file {}'.format(i+1, path+f) )
        w = Wavefront()
        w.load_hdf5(path+f)
        
        # Defining parameters
        nx = w.params.Mesh.nx
        ny = w.params.Mesh.ny
        nz = 1
        zMin = w.params.Mesh.zCoord
        eMin = w.params.photonEnergy #Initial Photon Energy [eV]
        xMin = w.params.Mesh.xMin #Initial Horizontal Position [m]
        xMax = w.params.Mesh.xMax #Final Horizontal Position [m]
        yMin = w.params.Mesh.yMin #Initial Vertical Position [m]
        yMax = w.params.Mesh.yMax #Final Vertical Position [m]
        Eh = w._srwl_wf.arEx
        Ev = w._srwl_wf.arEy
        
        if plots != None:
            I = w.get_intensity()
            plt.clf()
            plt.close()
            plt.imshow(I)
            plt.title("Intensity - loaded from hdf5 #" + str(i+1))
            plt.savefig(plots + 'intensity_' + str(i+1) + '.png')
            print('Intensity of wavefield #' + str(i+1) + ' saved to: ' + plots + 'intensity_' + str(i+1) + '.png')
            plt.colorbar()
            plt.show()
            
            P = w.get_phase()
            plt.clf()
            plt.close()
            plt.imshow(P)
            plt.title("Phase - loaded from hdf5 #" + str(i+1))
            plt.savefig(plots + 'phase_' + str(i+1) + '.png')
            print('Phase of wavefield #' + str(i+1) + ' saved to: ' + plots + 'phase_' + str(i+1) + '.png')
            plt.colorbar()
            plt.show()
            
            fig, axs = plt.subplots(2,1)
            axs[0].plot(Eh)
            axs[0].set_title("Horizontal e-field #" + str(i+1))
            axs[1].plot(Ev)
            axs[1].set_title("Vertical e-field #" + str(i+1))
            plt.show()        
            for ax in axs.flat:
                ax.set(xlabel="x position [pixels]", ylabel="amplitude")
                # Hide x labels and tick labels for top plots and y ticks for right plots.
            for ax in axs.flat:
                ax.label_outer()
            plt.savefig(plots + 'eField_' + str(i+1) + '.png')
            print('Electric field of wavefield #' + str(i+1) + ' saved to: ' + plots + 'eField_' + str(i+1) + '.png')
        else:
            print("... Plotting disabled")
        
        wf = SRWLWfr() #Initial Electric Field Wavefront    
        
        wf.allocate(1, nx, ny) #Numbers of points vs Photon Energy (1), Horizontal and Vertical Positions (dummy)
        wf.mesh.zStart = zMin #Longitudinal Position [m] at which Electric Field has to be calculated, i.e. the position of the first optical element
        wf.mesh.eStart = eMin #Initial Photon Energy [eV]
        wf.mesh.eFin = eMin #Final Photon Energy [eV]
        wf.mesh.xStart = xMin #Initial Horizontal Position [m]
        wf.mesh.xFin = xMax #Final Horizontal Position [m]
        wf.mesh.yStart = yMin #Initial Vertical Position [m]
        wf.mesh.yFin = yMax #Final Vertical Position [m]
        wf.arEx = Eh
        wf.arEy = Ev
        wf.mesh.ne = nz
        
        if i == 0:
            print("-----Setting up initial wavefield parameters-----")
            # Setting initial parameters for summed wavefield
            wfr.allocate(1, nx, ny) #Numbers of points vs Photon Energy (1), Horizontal and Vertical Positions (dummy)
            wfr.mesh.zStart = zMin #Longitudinal Position [m] at which Electric Field has to be calculated, i.e. the position of the first optical element
            wfr.mesh.eStart = eMin #Initial Photon Energy [eV]
            wfr.mesh.eFin = eMin #Final Photon Energy [eV]
            wfr.mesh.xStart = xMin #Initial Horizontal Position [m]
            wfr.mesh.xFin = xMax #Final Horizontal Position [m]
            wfr.mesh.yStart = yMin #Initial Vertical Position [m]
            wfr.mesh.yFin = yMax #Final Vertical Position [m]
            wfr.mesh.ne = nz
        
        print(" ")
        print("Adding electric field #{} to wavefield".format(i+1))
        wfr.addE(wf)
            
        print ('-----Getting Stokes parameters-----')
        S, Dx, Dy = getStokes(wf, mutual=0, Fx = 1, Fy = 1)
        s = getStokesParamFromStokes(S)
        sn = normaliseStoke(s)
        
        print(" ")
        print("-----Getting stokes parameters of summed wavefield-----")
        Stot, Dxtot, Dytot = getStokes(wfr, mutual=0, Fx = 1, Fy = 1)
        stot = getStokesParamFromStokes(Stot)
        char = getPolarisationCharacteristics(Sparam=stot) # D, Davg, e, i, c
        snT = normaliseStoke(stot)
        
        
        stokeN.append(snT)
        stokeW.append(sn)
        degPolarisation.append(char[0])
        degPolarisationAv.append(char[1])
        
    print(" ")
    print("-----Getting stokes parameters of FINAL wavefield-----")
    Sfin, Dxfin, Dyfin = getStokes(wfr, mutual=0, Fx = 1, Fy = 1)
    # s = getStokesParamFromStokes(S) # 2-dimensional stokes parameters
    sFin = getStokesParamFromStokes(Sfin)
    getPolarisationCharacteristics(Sparam=sFin) # D, Davg, e, i, c
    normaliseStoke(sFin)
    plotStokes(sFin,Sfin)
    
    if plots !=None:
        plt.clf()
        plt.close()
        fig, axs = plt.subplots(1,2)
        sPol = np.sqrt(sFin[1]**2 + sFin[2]**2 + sFin[3]**2)
        sUnPol = sFin[0]-sPol
        pMin = np.min([sPol,sUnPol])
        pMax = np.max([sPol,sUnPol])
        im = axs[0].imshow(sPol, vmin=pMin, vmax=pMax)
        axs[0].set_title("Polarised component")
        axs[1].imshow(sUnPol, vmin=pMin, vmax=pMax)
        axs[1].set_title("Unpolarised component")
        
        for ax in axs.flat:
            ax.set(xlabel="x position [pixels]", ylabel="y position [pixels] ")
        # Hide x labels and tick labels for top plots and y ticks for right plots.
        for ax in axs.flat:
            ax.label_outer()
        fig.subplots_adjust(right=0.8)
        cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
        fig.colorbar(im, cax=cbar_ax)
        plt.savefig(plots + 'degPol.png')
        print('Degree of Polarisation of final wavefield saved to: ' + plots + 'degPol.png')
        plt.show()
        
        stokeN = np.array(stokeN)
        stoke0 = stokeN[:,0,0]
        stoke1 = stokeN[:,1,0]
        stoke2 = stokeN[:,2,0]
        stoke3 = stokeN[:,3,0]
        
        stokeW = np.array(stokeW)
        stoke0w = stokeW[:,0,0]
        stoke1w = stokeW[:,1,0]
        stoke2w = stokeW[:,2,0]
        stoke3w = stokeW[:,3,0]
        
        plt.clf()
        plt.close()
        plt.plot(stoke0, label = 's0 - sum')
        plt.plot(stoke1, label = 's1 - sum')
        plt.plot(stoke2, label = 's2 - sum')
        plt.plot(stoke3, label = 's3 - sum')
        plt.plot(stoke0w, ':', label = 's0 - in')
        plt.plot(stoke1w, ':', label = 's1 - in')
        plt.plot(stoke2w, ':', label = 's2 - in')
        plt.plot(stoke3w, ':', label = 's3 - in')
        plt.title("Stokes parameters evolution")
        plt.legend()
        plt.savefig(plots + 'stokeEvolution.png')
        print('Stokes parameter variation of wavefield saved to: ' + plots + 'stokeEvolution.png')
        plt.show()
        
        print("Evolution of degree of polarisation")
        print(degPolarisationAv)
        
        dp2 = ((stoke1**2 + stoke2**2 + stoke3**2)**(1/2))/(stoke0)
        
        plt.clf()
        plt.close()
        plt.plot(degPolarisationAv, label='from function')
        plt.plot(dp2, label='from normalised stokes')
        plt.title("Degree of Polarisation evolution")
        plt.legend()
        plt.savefig(plots + 'degPolEvolution.png')
        print('Degree of Polarisation variation of wavefield saved to: ' + plots + 'degPolEvolution.png')
        plt.show()
    
    return wfr

def test():
    eMin = 10e6
    Nx = 100
    Ny = 200
    Nz = 1
    xMin = -10e-6
    xMax = 10e-6
    yMin = -10e-6
    yMax = 10e-6
    zMin = 1
    mutual = 0
    Fx = 1
    Fy = 1
    print('-----Running Test-----')
    print('-----building wavefront-----')
    w = build_gauss_wavefront(Nx,Ny,Nz,eMin/1000,xMin,xMax,yMin,yMax,1,1e-6,1e-6,1) 
    #build_gauss_wavefront()
    
    # print(w)
    
    """ Converting Gaussian to SRWLWfr() structure"""
    wfr = SRWLWfr() #Initial Electric Field Wavefront
    wfr.allocate(1, Nx, Ny) #Numbers of points vs Photon Energy (1), Horizontal and Vertical Positions (dummy)
    wfr.mesh.zStart = zMin #Longitudinal Position [m] at which Electric Field has to be calculated, i.e. the position of the first optical element
    wfr.mesh.eStart = eMin #Initial Photon Energy [eV]
    wfr.mesh.eFin = eMin #Final Photon Energy [eV]
    wfr.mesh.xStart = xMin #Initial Horizontal Position [m]
    wfr.mesh.xFin = xMax #Final Horizontal Position [m]
    wfr.mesh.yStart = yMin #Initial Vertical Position [m]
    wfr.mesh.yFin = yMax #Final Vertical Position [m]
    # wfr.delE()
    wfr.addE(w)
    
    
    
    """ Converting Gaussian to Wavefront() structure"""
    wf = Wavefront(srwl_wavefront=w)
        
    intensity = wf.get_intensity()           
    plt.imshow(intensity)
    plt.title("Intensity")
    plt.show()


    print ('-----Getting Stokes parameters-----')
    S, Dx, Dy = getStokes(wfr, mutual=mutual, Fx = Fx, Fy = Fy)
    # s = getStokesParamFromStokes(S) # 2-dimensional stokes parameters
    s = getStokesParamFromStokes(S,d=1)
    # _s = normaliseStoke(s)
    
    print("-----Plotting Stokes parameters-----")
    # plotStokes(s,S, Dx=Dx, Dy=Dy)
    plotStokesCuts(s)
    
    # print("-----Plotting normalised Stokes parameters-----")
    # plotStokes(_s,S,"_s0","_s1","_s2","_s3")
    
    
    print("-----Getting degree of coherence from Stokes parameters------")
    # start1 = time.time()
    # coherenceFromSTKS(S,Dx,Dy)
    # end1 = time.time()
    # print("Time taken to get degree of coherence from Stokes (s): {}".format(end1 - start1))
    
    print ('------Done------')

def testMulti():
    """ Loading Gaussian hdf5 wavefields for testing """
    dirPath = '/home/jerome/dev/experiments/beamPolarisation14/data/'
    wfr_files = ['wf_tcl.hdf', 'wf_tcr.hdf'] #,'wf_tld.hdf','wf_te.hdf','wf_tlv.hdf', 'wf_tlh.hdf', 'wf_tclOP.hdf', 'wf_tcrOP.hdf','wf_tldOP.hdf','wf_teOP.hdf','wf_tlvOP.hdf', 'wf_tlhOP.hdf']
    #'/home/jerome/dev/data/testGaussian.hdf'   #'/home/jerome/dev/data/testGaussian.hdf'#'/home/jerome/dev/experiments/beamPolarisation9/wf_final.hdf'    
    
    #Setting up initial wavefield object to contain all summed wavefields
    wfr = SRWLWfr()
    
    stokeN = []
    degPolarisation = []
    degPolarisationAv = []
    degPolarisation3 = []
    
    for i, f in enumerate(wfr_files):
        print(" ")
        print('Loading wavefront #{} from file {}'.format(i+1, dirPath+f) )
        w = Wavefront()
        w.load_hdf5(dirPath+f)
    
        I = w.get_intensity()
        plt.imshow(I)
        plt.title("Intensity - loaded from hdf5 #" + str(i+1))
        plt.colorbar()
        plt.show()
        
        P = w.get_phase()
        plt.imshow(P)
        plt.title("Phase - loaded from hdf5 #" + str(i+1))
        plt.colorbar()
        plt.show()
        
        nx = w.params.Mesh.nx
        ny = w.params.Mesh.ny
        nz = 1
        zMin = w.params.Mesh.zCoord
        eMin = w.params.photonEnergy #Initial Photon Energy [eV]
        xMin = w.params.Mesh.xMin #Initial Horizontal Position [m]
        xMax = w.params.Mesh.xMax #Final Horizontal Position [m]
        yMin = w.params.Mesh.yMin #Initial Vertical Position [m]
        yMax = w.params.Mesh.yMax #Final Vertical Position [m]
        Eh = w._srwl_wf.arEx
        Ev = w._srwl_wf.arEy
        
        fig, axs = plt.subplots(2,1)
        axs[0].plot(Eh)
        axs[0].set_title("Horizontal e-field #" + str(i+1))
        axs[1].plot(Ev)
        axs[1].set_title("Vertical e-field #" + str(i+1))
        plt.show()
        # plt.plot(Eh)
        # plt.title("E-field (horizontal) #" + str(i+1))
        # plt.show()
        # plt.plot(Ev)
        # plt.title("E-field (vertical) #" + str(i+1))
        # plt.show()
        
        # print("Eh shape: {}".format(np.shape(Eh1)))
        # print("Ev shape: {}".format(np.shape(Ev1)))
        
        wf = SRWLWfr() #Initial Electric Field Wavefront    
        
        wf.allocate(1, nx, ny) #Numbers of points vs Photon Energy (1), Horizontal and Vertical Positions (dummy)
        wf.mesh.zStart = zMin #Longitudinal Position [m] at which Electric Field has to be calculated, i.e. the position of the first optical element
        wf.mesh.eStart = eMin #Initial Photon Energy [eV]
        wf.mesh.eFin = eMin #Final Photon Energy [eV]
        wf.mesh.xStart = xMin #Initial Horizontal Position [m]
        wf.mesh.xFin = xMax #Final Horizontal Position [m]
        wf.mesh.yStart = yMin #Initial Vertical Position [m]
        wf.mesh.yFin = yMax #Final Vertical Position [m]
        wf.arEx = Eh
        wf.arEy = Ev
        wf.mesh.ne = nz
        
        if i == 0:
            print("-----Setting up initial wavefield parameters-----")
            # Setting initial parameters for summed wavefield
            wfr.allocate(1, nx, ny) #Numbers of points vs Photon Energy (1), Horizontal and Vertical Positions (dummy)
            wfr.mesh.zStart = zMin #Longitudinal Position [m] at which Electric Field has to be calculated, i.e. the position of the first optical element
            wfr.mesh.eStart = eMin #Initial Photon Energy [eV]
            wfr.mesh.eFin = eMin #Final Photon Energy [eV]
            wfr.mesh.xStart = xMin #Initial Horizontal Position [m]
            wfr.mesh.xFin = xMax #Final Horizontal Position [m]
            wfr.mesh.yStart = yMin #Initial Vertical Position [m]
            wfr.mesh.yFin = yMax #Final Vertical Position [m]
            wfr.mesh.ne = nz
        
        print(" ")
        print("Adding electric field #{} to wavefield".format(i+1))
        wfr.addE(wf)
        
        fig, axs = plt.subplots(2,1)
        axs[0].plot(wfr.arEx)
        axs[0].set_title("Horizontal e-field - summed")
        axs[1].plot(wfr.arEy)
        axs[1].set_title("Vertical e-field - summed")
        plt.show()
        
        
            
        print ('-----Getting Stokes parameters-----')
        S, Dx, Dy = getStokes(wf, mutual=0, Fx = 1, Fy = 1)
        # s = getStokesParamFromStokes(S) # 2-dimensional stokes parameters
        s = getStokesParamFromStokes(S)
        sn = normaliseStoke(s)
        plotStokes(s,S)
        
        print(" ")
        print("-----Getting stokes parameters of summed wavefield-----")
        Stot, Dxtot, Dytot = getStokes(wfr, mutual=0, Fx = 1, Fy = 1)
        # s = getStokesParamFromStokes(S) # 2-dimensional stokes parameters
        stot = getStokesParamFromStokes(Stot)
        char = getPolarisationCharacteristics(Sparam=stot) # D, Davg, e, i, c
        snT = normaliseStoke(stot)
        plotStokes(stot,Stot)
        
        
        fig, axs = plt.subplots(1,2)
        sPol = np.sqrt(stot[1]**2 + stot[2]**2 + stot[3]**2)
        sUnPol = stot[0]-sPol
        pMin = np.min([sPol,sUnPol])
        pMax = np.max([sPol,sUnPol])
        im = axs[0].imshow(sPol)#, vmin=pMin, vmax=pMax)
        axs[0].set_title("Polarised component")
        axs[0].colorbar()
        axs[1].imshow(sUnPol)#, vmin=pMin, vmax=pMax)
        axs[1].set_title("Unpolarised component")
        axs[1].colorbar()
        
        for ax in axs.flat:
            ax.set(xlabel="x position [pixels]", ylabel="y position [pixels] ")
        # Hide x labels and tick labels for top plots and y ticks for right plots.
        for ax in axs.flat:
            ax.label_outer()
        # fig.subplots_adjust(right=0.8)
        # cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
        # fig.colorbar(im, cax=cbar_ax)
        plt.show()
        
        degpol3 = sPol/stot[0]
        
        plt.imshow(degpol3)
        plt.title("degree of pol")
        plt.colorbar()
        plt.show()
        
        stokeN.append(snT)
        degPolarisation.append(char[0])
        degPolarisationAv.append(char[1])
        degPolarisation3.append(np.mean(degpol3))
    
    print("Evolution of stokes parameters")
    stokeN = np.array(stokeN)
    print(stokeN)
    print("Shape of stokeN: {}".format(np.shape(stokeN)))
    
    stoke0 = stokeN[:,0,0]
    stoke1 = stokeN[:,1,0]
    stoke2 = stokeN[:,2,0]
    stoke3 = stokeN[:,3,0]
    
    plt.plot(stoke0, label = 's0')
    plt.plot(stoke1, label = 's1')
    plt.plot(stoke2, label = 's2')
    plt.plot(stoke3, label = 's3')
    plt.title("Stokes parameters evolution")
    plt.legend()
    plt.show()
    
    print("Evolution of degree of polarisation")
    print(degPolarisationAv)
    
    print("Average deg of pol from loop: {}".format(np.mean(degPolarisation3)))
    
    dp2 = ((stoke1**2 + stoke2**2 + stoke3**2)**(1/2))/(stoke0)
    
    plt.plot(degPolarisationAv, label='from function')
    # plt.plot(dp2, label='from stokeN')
    plt.plot(degPolarisation3, label='from loop')
    plt.title("Degree of Polarisation evolution")
    plt.legend()
    plt.show()

def testMultiFunc():
    """ Loading Gaussian hdf5 wavefields for testing """
    dirPath = '/home/jerome/dev/experiments/beamPolarisation14/data/'
    wfr_files = ['wf_tcl.hdf', 'wf_tcr.hdf','wf_tld.hdf','wf_te.hdf','wf_tlv.hdf', 'wf_tlh.hdf', 'wf_tclOP.hdf', 'wf_tcrOP.hdf','wf_tldOP.hdf','wf_teOP.hdf','wf_tlvOP.hdf', 'wf_tlhOP.hdf']
    
    sumWaves(wfr_files,dirPath,dirPath + 'plots/')


if __name__ == '__main__':
   # test()
    # testMulti()
    testMultiFunc()


# %%
