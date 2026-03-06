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

import pylab

# plt.style.use(['science','high-vis','no-latex']) # 'ieee', high-vis, high-contrast
pylab.rcParams['figure.figsize'] = (10.0, 8.0)

def round_sig(x, sig=2):
    if x != 0:
        return round(x, sig-int(floor(log10(abs(x))))-1)
    else:
            return x


def getPolarisationCharacteristics(S=None,Sparam=None, d=2):
    ''''
    Return the degree of polarization, 
            degree of polarization averaged over wavefront, 
            the eccentricity, 
            orientation,  and 
            chirality 
    of the polarization ellipse.
    Added ability to analyse 1D cuts.
    '''
    
    
    if S is not None:
        s0,s1,s2,s3 = getStokesParamFromStokes(S)
    else:
        if Sparam is not None:
            if d == 1:
                s0x, s1x, s2x, s3x, s0y, s1y, s2y, s3y = Sparam
            elif d == 2:
                s0, s1, s2, s3 = Sparam
        else:
            raise ValueError("S and Sparam both None")

    # degree of polarization.  Alternatively, we could use D = Ip/(Ip + Itot) where Ip is the polarised intensity and It is the total intensity.
    if d == 1:
        Dx = (np.sqrt((s1x**2 + s2x**2 + s3x**2)))/s0x
        Dy = (np.sqrt((s1y**2 + s2y**2 + s3y**2)))/s0y   

        DavgX = np.mean(Dx)
        DavgY = np.mean(Dy)        
        
        print("... eccentricity, inclination and chirality anslysis disabled for 1D cuts")
        
        return Dx, Dy, DavgX, DavgY
    
    elif d == 2:
        D = (np.sqrt((s1**2 + s2**2 + s3**2)))/s0
    
        Davg = np.mean(D)

        # eccentricity.  e = 1 => linear polarization (no chirality) 
        e = np.sqrt(s2*np.sqrt(s1**2 + s2**2)/(1+np.sqrt(s1**2 + s2**2))) # added sqrt - jerome
        
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
  
        #making sure eccentricity agrees with s3
        # e_3 = (2*(-1 + s3**2 + np.sqrt(-1*(1 - s3**2))))/(s3**2)
        # print('Eccentricity from s3 = {}'.format(e_3))
    
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
    """
    Parameters
    ----------
    stk: 
        SRWLStokes() stk object from getStokes().
    d : 
        Dimensions. Default is 2.
        Can be 1 for faster computation, 
        in this case 1D cuts are generated in x and y for each stoke parameter.

    Returns
    -------
    Separated stokes parameters
    
    """
    nTot = stk.mesh.nx*stk.mesh.ny*stk.mesh.ne
    # print('nTot before reshape: {}'.format(nTot))
    # print('arS shape : {}'.format(np.shape(stk.arS)))
    
    # plt.plot(stk.arS)
    # plt.title('arS')
    # plt.show()
    
    
    if stk.mutual > 0 :
        
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
        
        # print("Shape of 1st average of S0: {}".format(np.shape(_s0)))
        
        s0 = abs(_s0.mean(0))
        s1 = abs(_s1.mean(0))
        s2 = abs(_s2.mean(0))
        s3 = abs(_s3.mean(0))
        return s0, s1, s2, s3    
    
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
            
            return s0x, s1x, s2x, s3x, s0y, s1y, s2y, s3y


        if d == 2:
            s = np.reshape(stk.arS,(4,stk.mesh.nx,stk.mesh.ny))
            
            s0 = np.reshape(s[0],(stk.mesh.ny,stk.mesh.nx))
            s1 = np.reshape(s[1],(stk.mesh.ny,stk.mesh.nx))
            s2 = np.reshape(s[2],(stk.mesh.ny,stk.mesh.nx))
            s3 = np.reshape(s[3],(stk.mesh.ny,stk.mesh.nx))
#            s0 = np.reshape(s[0,:,:],(stk.mesh.nx,stk.mesh.ny))
#            s1 = np.reshape(s[1,:,:],(stk.mesh.nx,stk.mesh.ny))
#            s2 = np.reshape(s[2,:,:],(stk.mesh.nx,stk.mesh.ny))
#            s3 = np.reshape(s[3,:,:],(stk.mesh.nx,stk.mesh.ny))
            return s0, s1, s2, s3
        
    # print('S0 = {}'.format(np.shape(s0)))    
    # print('S1 = {}'.format(np.shape(s1)))    
    # print('S2 = {}'.format(np.shape(s2)))    
    # print('S3 = {}'.format(np.shape(s3)))
    

def getStokes(w, mutual=0, Fx = 1, Fy = 1):
    """
    Generates the Stokes parameters from a SRWLWfr() wavefront object.

    Parameters
    ----------
    w :
        SRWLWfr() wavefront.
    mutual :
        The default is 0.
        0 - Generate single-point stokes parameters
        1 - Generate two-point stokes parameters
    Fx :
        Fraction of wavefront array to sample in x. (0<Fx<1)
    Fy : 
        Fraction of wavefront array to sample in y. (0<Fy<1)

    Returns
    -------
    stk : TYPE
        SRWLStokes() array.
    Dx : 
        X-dimension of stokes array
    Dy :
        Y-dimension of stokes array

    """
    
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
    
    print(stk)
    
    w.calc_stokes(stk)
    
    plt.plot(stk.arS)
    plt.show()
    # print("mutual:")
    # print(stk.mutual)
    
    return stk, Dx ,Dy

def normaliseStoke(S, d=2):
    """
    Function to normalise an array of stokes parameters so that S0=1

    Parameters
    ----------
    S : 
        Array of stokes parameters
    d : 
        Dimensions of stokes array.
        1 - 1D cuts of each stokes parameter in x and y
        2 - 2D planes of each stokes parameter

    Returns
    -------
    Normalised stokes vector
    if d=1 - single stokes vector
    if d=2 - 2 stokes vectors, x-cut and y-cut

    """
    # print("STOKE SHAPE: {}".format(np.shape(S)))
    
    if d == 1:
        s0x,s1x,s2x,s3x,s0y,s1y,s2y,s3y = S[0], S[1], S[2], S[3], S[4], S[5], S[6], S[7] 
    
        _s0x = s0x/np.max(s0x)
        _s1x = s1x/np.max(s0x)
        _s2x = s2x/np.max(s0x)
        _s3x = s3x/np.max(s0x)
    
        _s0y = s0y/np.max(s0y)
        _s1y = s1y/np.max(s0y)
        _s2y = s2y/np.max(s0y)
        _s3y = s3y/np.max(s0y)  

        # _sX = np.array([[_s0x.mean(),_s1x.mean(),_s2x.mean(),_s3x.mean()]]).T
        # _sY = np.array([[_s0y.mean(),_s1y.mean(),_s2y.mean(),_s3y.mean()]]).T
            
        _sX = np.array([[np.max(_s0x),np.max(_s1x),np.max(_s2x),np.max(_s3x)]]).T
        _sY = np.array([[np.max(_s0y),np.max(_s1y),np.max(_s2y),np.max(_s3y)]]).T
        
        print("Normalised Stokes vector (x-cut):")
        print(_sX)
        print("Normalised Stokes vector (y-cut):")
        print(_sY)      
        
        return _sX, _sY
    
    elif d == 2:
        s0,s1,s2,s3 = S[0], S[1], S[2], S[3]
        
        _s0 = s0/np.max(s0)
        _s1 = s1/np.max(s0)
        _s2 = s2/np.max(s0)
        _s3 = s3/np.max(s0)
    
        _s = np.array([[_s0.mean(),_s1.mean(),_s2.mean(),_s3.mean()]]).T
#        _s = np.array([[np.max(_s0),np.max(_s1),np.max(_s2),np.max(_s3)]]).T
        
        print("Normalised Stokes vector:")
        print(_s)
        
        return _s0,_s1,s2,s3,_s
    
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
    

def plotStokes(s,dx=1,dy=1, extra=False, savePath=None):
               # fig1='S0',fig2='S1',fig3='S2',fig4='S3', Dx=50e-6, Dy=50e-6,
               # pathS0 = None, pathS1 = None, pathS2 = None, pathS3 = None,
               # pathD = None, pathE = None, pathIn = None):
    
    # print("Shape of S: {}".format(np.shape(S)))
    print("Shape of s: {}".format(np.shape(s)))
    
    Nx = np.shape(s[0])[1] 
    Ny = np.shape(s[0])[0]
    
    print("Nx={}".format(Nx))
    print("NY={}".format(Ny))
    
    """ Creating array of custom tick markers for plotting """
    tickAx = [round_sig(-dx*Nx/2),round_sig(-dx*Nx/4),0,round_sig(dx*Nx/4),round_sig(dx*Nx/2)]
    tickAy = [round_sig(dy*Ny/2),round_sig(dy*Ny/4),0,round_sig(-dy*Ny/4),round_sig(-dy*Ny/2)]
    
    
    print("plotting Stokes parameters (S0, S1, S2, S3)...")
    plt.clf()
    plt.close()
    smin = np.min([s[0],s[1],s[2],s[3]])
    smax = np.max([s[0],s[1],s[2],s[3]])
    fig, axs = plt.subplots(2, 2)
    im = axs[0, 0].imshow(s[0], aspect='auto', cmap='RdYlBu_r', vmin=smin, vmax=smax)
    axs[0, 0].set_title('S0')
    axs[0, 1].imshow(s[1], aspect='auto', cmap='RdYlBu_r', vmin=smin, vmax=smax)
    axs[0, 1].set_title('S1')
    axs[1, 0].imshow(s[2], aspect='auto', cmap='RdYlBu_r', vmin=smin, vmax=smax)
    axs[1, 0].set_title('S2')
    axs[1, 1].imshow(s[3], aspect='auto', cmap='RdYlBu_r', vmin=smin, vmax=smax)
    axs[1, 1].set_title('S3')

    for ax in axs.flat:
        ax.set(xlabel="x position [pixels]", ylabel="y position [pixels] ")
    # Hide x labels and tick labels for top plots and y ticks for right plots.
    for ax in axs.flat:
        ax.label_outer()
    fig.subplots_adjust(right=0.8)
    cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
    fig.colorbar(im, cax=cbar_ax)
    if savePath != None:
        print("Saving Stokes Plots to: {}".format(savePath  + 'stokesPlot.png'))
        plt.savefig(savePath + 'stokesPlot.png')
    plt.show()
    plt.clf()
    
    if extra:
        D, Davg, e, i, c = getPolarisationCharacteristics(S=None,Sparam=s)
        
        print('Average degree of polarisation = {}'.format(Davg))
        print('Average ellipticity = {}'.format(np.mean(e)))
        print('Average inclination = {}'.format(np.mean(i)))
        print ('Chirality: {}'.format(c))
        
    
        plt.imshow(D, aspect='auto',cmap='cividis')
        plt.title('Degree of polarization')
        plt.xticks(np.arange(0,Nx+1,Nx/4),tickAx)
        plt.yticks(np.arange(0,Ny+1,Ny/4),tickAy)
        plt.xlabel("Horizontal Position [m]") # [\u03bcm]")#"(\u03bcm)")
        plt.ylabel("Vertical Position [m]")#"(\u03bcm)")
        if savePath != None:
            print("Saving Deg of Pol figure to path: {}".format(savePath+'degPol.png'))
            plt.savefig(savePath + 'degPol.png')
        plt.colorbar()
        plt.show()
        plt.clf()    
    
        plt.imshow(e, aspect='auto')
        plt.title('Ellipticity')
        plt.xticks(np.arange(0,Nx+1,Nx/4),tickAx)
        plt.yticks(np.arange(0,Ny+1,Ny/4),tickAy)
        plt.xlabel("Horizontal Position [m]")#"(\u03bcm)")
        plt.ylabel("Vertical Position [m]")#"(\u03bcm)")
        if savePath != None:
            print("Saving ellipticity figure to path: {}".format(savePath + 'ellipticity.png'))
            plt.savefig(savePath + 'ellipticity.png')
        plt.colorbar()
        plt.show()
        plt.clf()
        
        plt.imshow(i, aspect='auto')
        plt.title('Inclination')
        plt.xticks(np.arange(0,Nx+1,Nx/4),tickAx)
        plt.yticks(np.arange(0,Ny+1,Ny/4),tickAy)
        plt.xlabel("Horizontal Position [m]")#"(\u03bcm)")
        plt.ylabel("Vertical Position [m]")#"(\u03bcm)")
        if savePath != None:
            print("Saving Inclination figure to path: {}".format(savePath + 'inclination.png'))
            plt.savefig(savePath + 'inclination.png')
        plt.colorbar()
        plt.show()
        plt.clf()

# def plotElipse(S):
    
#     from py_pol.stokes import Stokes
    
#     s0,s1,s2,s3 = S

def plotStokesCuts(s, savePath=None):
    
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
    if savePath != None:
        print("Saving Stokes Plots (x-cut) to: {}".format(savePath  + 'stokesXcut.png'))
        plt.savefig(savePath + 'stokesXcut.png')
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
    if savePath != None:
        print("Saving Stokes Plots (y-cut) to: {}".format(savePath  + 'stokesYcut.png'))
        plt.savefig(savePath + 'stokesYcut.png')
    plt.show()
    plt.clf()

def sumWaves(wavefronts, sampleFraction=1, stokes=None , norm=None, plots=None, savePath=None):
    """
    Parameters
    ----------
    wavefronts : 
        Array of paths to hdf5 wavefront files
    sampleFraction:
        Fraction of the wavefield to sample from centre. Between 0 and 1.
    stokes:
        Specify how to generate stokes parameters-
        None - Do not generate stokes parameters or polarisation characteristics
        0 - Generate 1D stokes horizontal and vertical cuts
        1 - Generate 2D stokes parameters
    norm:
        Normalisation of electric field -
        None - default, no normalisation
        E - Normalise by maximum e-field amplitude
        I - Normalise by maximum intensity
    plots :
        Path to save plots of each wavefront and resulting summed wavefront
    savePath:
        Path to save final wavefront hdf5 file
    Returns
    -------
    wfr:
        SRWLWfr() wavefront which is the sum of all wavefronts.

    """
    print("Wavefront files to be added:")
    print(wavefronts)
    #Setting up initial wavefield object to contain all summed wavefields
    wfr = SRWLWfr()
    
    stokeN = []
    stokeW = []
    stokeNx = []
    stokeNy = []
    stokeWx = []
    stokeWy = []
    degPolarisation = []
    degPolarisationN = []
    degPolarisationAv = []
    degPolarisationAvN = []
    degPolarisationX = []
    degPolarisationY = []
    degPolarisationXn = []
    degPolarisationYn = []
    degPolarisationAvX = []
    degPolarisationAvY = []
    degPolarisationAvXn = []
    degPolarisationAvYn = []
    
    maxI = []
    maxE = []
    
    for i, f in enumerate(wavefronts):
        print(" ")
        print('Loading wavefront #{} from file {}'.format(i+1, f) )
        w = Wavefront()
        w.load_hdf5(f)
        
        # Defining parameters
        nx = int(sampleFraction*w.params.Mesh.nx)
        ny = int(sampleFraction*w.params.Mesh.ny)
        nz = 1
        zMin = w.params.Mesh.zCoord
        eMin = w.params.photonEnergy #Initial Photon Energy [eV]
        xMin = sampleFraction*w.params.Mesh.xMin #Initial Horizontal Position [m]
        xMax = sampleFraction*w.params.Mesh.xMax #Final Horizontal Position [m]
        yMin = sampleFraction*w.params.Mesh.yMin #Initial Vertical Position [m]
        yMax = sampleFraction*w.params.Mesh.yMax #Final Vertical Position [m]
        Etot = w._srwl_wf.arEx + w._srwl_wf.arEy
        exMax = np.max(w._srwl_wf.arEx)
        eyMax = np.max(w._srwl_wf.arEy)
        eTotMax = np.max(abs(Etot))
        print("MAX E (x,y): {}".format((exMax,eyMax)))
        eMax = max(exMax,eyMax)
        print("MAXIMUM E: {}".format(eMax))
        print("MAX E-TOT: {}".format(eTotMax))
        Imax = np.max(w.get_intensity())
        print("MAX I: {}".format(Imax))
        # E = np.array(w._srwl_wf.arEx,w._srwl_wf.arEy)
        # normE = np.max(E)
        # print(w._srwl_wf.arEx)
        # print(np.max(w._srwl_wf.arEx))
        # print(w._srwl_wf.arEx/np.max(w._srwl_wf.arEx))
        
        _Ex = np.reshape(w._srwl_wf.arEx, (w.params.Mesh.nx, w.params.Mesh.ny, 2))
        _Ey = np.reshape(w._srwl_wf.arEy, (w.params.Mesh.nx, w.params.Mesh.ny, 2))
        
        midEhx = np.shape(_Ex)[0]/2
        midEhy = np.shape(_Ex)[1]/2
        midEvx = np.shape(_Ey)[0]/2
        midEvy = np.shape(_Ey)[1]/2
        
        Ex = _Ex[int(midEhx - midEhx*sampleFraction):int(midEhx + midEhx*sampleFraction),int(midEhy - midEhy*sampleFraction):int(midEhy + midEhy*sampleFraction), :].flatten()
        Ey = _Ey[int(midEvx - midEvx*sampleFraction):int(midEvx + midEvx*sampleFraction),int(midEvy - midEvy*sampleFraction):int(midEvy + midEvy*sampleFraction), :].flatten()
            
        if norm == None:
            Eh = Ex
            Ev = Ey
            # Eh = w._srwl_wf.arEx[int(midEh - midEh*sampleFraction): int(midEh + midEh*sampleFraction)]
            # Ev = w._srwl_wf.arEy[int(midEv - midEv*sampleFraction): int(midEv + midEv*sampleFraction)]
        elif norm == 'E':
            Eh = np.divide(Ex, eTotMax)
            Ev = np.divide(Ey, eTotMax)
            # Eh = np.divide(w._srwl_wf.arEx,eTotMax)[int(midEh - midEh*sampleFraction): int(midEh + midEh*sampleFraction)]
            # Ev = np.divide(w._srwl_wf.arEy,eTotMax)[int(midEv - midEv*sampleFraction): int(midEv + midEv*sampleFraction)]
        elif norm == 'I':
            Eh = np.divide(w._srwl_wf.arEx,Imax)
            Ev = np.divide(w._srwl_wf.arEy,Imax)
        else:
            print("Unrecognised normalisation parameter... choose E, I or None")
        
        print("SHAPE OF E ARRAYS: {}".format(np.shape(Eh)))
        print("LENGTH OF E ARRAYS: {}".format(len(Eh)))
        maxI.append(Imax)
        maxE.append(eMax)
        
        if plots != None:
            if stokes == 0:
                I = w.get_intensity()
                plt.clf()
                plt.close()
                plt.plot(I[int(ny/2),:], label="x-cut")
                plt.plot(I[:,int(nx/2)], label="y-cut")
                plt.title("Intensity - loaded from hdf5 #" + str(i+1))
                plt.legend()
                plt.savefig(plots + 'intensity_' + str(i+1) + '.png')
                print('Intensity of wavefield #' + str(i+1) + ' saved to: ' + plots + 'intensity_' + str(i+1) + '.png')
                plt.show()
                
                P = w.get_phase()
                plt.clf()
                plt.close()
                plt.plot(P[int(ny/2),:], label="x-cut")
                plt.plot(P[:,int(nx/2)], label="y-cut")
                plt.title("Phase - loaded from hdf5 #" + str(i+1))
                plt.legend()
                plt.savefig(plots + 'phase_' + str(i+1) + '.png')
                print('Phase of wavefield #' + str(i+1) + ' saved to: ' + plots + 'phase_' + str(i+1) + '.png')
                plt.show()                
                
            elif stokes == 1:    
                I = w.get_intensity()
                plt.clf()
                plt.close()
                plt.imshow(I, cmap='gray')
                plt.title("Intensity - loaded from hdf5 #" + str(i+1))
                plt.colorbar()
                plt.savefig(plots + 'intensity_' + str(i+1) + '.png')
                print('Intensity of wavefield #' + str(i+1) + ' saved to: ' + plots + 'intensity_' + str(i+1) + '.png')
                plt.show()
                
                P = w.get_phase()
                plt.clf()
                plt.close()
                plt.imshow(P, cmap='plasma')
                plt.title("Phase - loaded from hdf5 #" + str(i+1))
                plt.colorbar()
                plt.savefig(plots + 'phase_' + str(i+1) + '.png')
                print('Phase of wavefield #' + str(i+1) + ' saved to: ' + plots + 'phase_' + str(i+1) + '.png')
                plt.show()
            
            plt.clf()
            plt.close()
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
        
        if stokes != None:
            print ('-----Getting Stokes parameters-----')
            S, Dx, Dy = getStokes(wf, mutual=0, Fx = 1, Fy = 1)
            if stokes == 0:
                s = getStokesParamFromStokes(S,d=1)
                sn = normaliseStoke(s,d=1)
                if plots != None:
                    plotStokesCuts(s, savePath=plots + str(i+1))
            elif stokes == 1:
                s = getStokesParamFromStokes(S,d=2)
                sn = normaliseStoke(s,d=2)
                if plots != None:
                    plotStokes(s,dx=(xMax-xMin)/nx, dy=(yMax-yMin)/ny, savePath=plots + str(i+1))
                        
            print(" ")
            print("-----Getting stokes parameters of summed wavefield-----")
            Stot, Dxtot, Dytot = getStokes(wfr, mutual=0, Fx = 1, Fy = 1)
            if stokes == 0:
                stot = getStokesParamFromStokes(Stot,d=1)
                char = getPolarisationCharacteristics(Sparam=stot,d=1) # Dx, Dy, DavgX, DavgY
                snT = normaliseStoke(stot,d=1)
                normChar = getPolarisationCharacteristics(Sparam=stot/np.max(stot[0]),d=1) # Dx, Dy, DavgX, DavgY

                
                stokeNx.append(snT[0])
                stokeNy.append(snT[1])
                stokeWx.append(sn[0])
                stokeWy.append(sn[1])
                degPolarisationX.append(char[0])
                degPolarisationY.append(char[1])
                degPolarisationXn.append(normChar[0])
                degPolarisationYn.append(normChar[1])
                degPolarisationAvX.append(char[2])
                degPolarisationAvY.append(char[3])
                degPolarisationAvXn.append(normChar[2])
                degPolarisationAvYn.append(normChar[3])
            elif stokes == 1:
                stot = getStokesParamFromStokes(Stot,d=2)
                char = getPolarisationCharacteristics(Sparam=stot,d=2) # D, Davg, e, i, c
                snT = normaliseStoke(stot,d=2)
                normChar = getPolarisationCharacteristics(Sparam=stot/np.max(stot[0]),d=2) # D, Davg, e, i, c
                
                stokeN.append(snT)
                stokeW.append(sn)
                degPolarisation.append(char[0])
                degPolarisationN.append(normChar[0])
                degPolarisationAv.append(char[1])
                degPolarisationAvN.append(normChar[1])
        else:
            print("... Stokes parameters disabled")
        
    print(" ")
    print("---- Completed summing wavefield ----")
    
    if stokes != None:
        print(" ")
        print("-----Getting stokes parameters of FINAL wavefield-----")
        Sfin, Dxfin, Dyfin = getStokes(wfr, mutual=0, Fx = 1, Fy = 1)
        # s = getStokesParamFromStokes(S) # 2-dimensional stokes parameters
        if stokes == 0:
            sFin = getStokesParamFromStokes(Sfin, d=1)
            getPolarisationCharacteristics(Sparam=sFin, d=1) # D, Davg, e, i, c
            sNF = normaliseStoke(sFin, d=1)
            getPolarisationCharacteristics(Sparam=sFin/np.max(sFin[0]), d=1) # D, Davg, e, i, c
            if plots != None:
                plotStokesCuts(sFin, savePath=plots + 'final')
        elif stokes == 1:
            sFin = getStokesParamFromStokes(Sfin, d=2)
            getPolarisationCharacteristics(Sparam=sFin, d=2) # D, Davg, e, i, c
            sNF = normaliseStoke(sFin, d=2)
            if plots != None:
                    plotStokes(sFin,dx=(xMax-xMin)/nx, dy=(yMax-yMin)/ny, savePath=plots + 'final')
            getPolarisationCharacteristics(Sparam=sNF, d=2) # D, Davg, e, i, c
        
        if plots !=None:
            if stokes == 0:
                plt.clf()
                plt.close()
                fig, axs = plt.subplots(1,2)
                sPolx = np.sqrt(sFin[1]**2 + sFin[2]**2 + sFin[3]**2)
                sPoly = np.sqrt(sFin[5]**2 + sFin[6]**2 + sFin[7]**2)
                sUnPolx = sFin[0]-sPolx
                sUnPoly = sFin[4]-sPoly
                axs[0].plot(sPolx, label="x-cut")
                axs[0].plot(sPoly, label="y-cut")
                axs[0].set_title("Polarised component")
                axs[1].plot(sUnPolx, label="x-cut")
                axs[1].plot(sUnPoly, label="y-cut")
                axs[1].set_title("Unpolarised component")
                
                # for ax in axs.flat:
                #     ax.set(xlabel="x position [pixels]", ylabel="y position [pixels] ")
                # # Hide x labels and tick labels for top plots and y ticks for right plots.
                # for ax in axs.flat:
                #     ax.label_outer()
                axs[0].legend()
                axs[1].legend()
                
                plt.savefig(plots + 'degPol.png')
                print('Degree of Polarisation of final wavefield saved to: ' + plots + 'degPol.png')
                plt.show()
                
                stokeNx = np.array(stokeNx)
                stoke0x = stokeNx[:,0,0]
                stoke1x = stokeNx[:,1,0]
                stoke2x = stokeNx[:,2,0]
                stoke3x = stokeNx[:,3,0]
                
                stokeNy = np.array(stokeNy)
                stoke0y = stokeNy[:,0,0]
                stoke1y = stokeNy[:,1,0]
                stoke2y = stokeNy[:,2,0]
                stoke3y = stokeNy[:,3,0]
                
                stokeWx = np.array(stokeWx)
                stoke0wX = stokeWx[:,0,0]
                stoke1wX = stokeWx[:,1,0]
                stoke2wX = stokeWx[:,2,0]
                stoke3wX = stokeWx[:,3,0]
                
                stokeWy = np.array(stokeWy)
                stoke0wY = stokeWy[:,0,0]
                stoke1wY = stokeWy[:,1,0]
                stoke2wY = stokeWy[:,2,0]
                stoke3wY = stokeWy[:,3,0]
                
                plt.clf()
                plt.close()
                plt.plot(stoke0x, label = 's0 - sum')
                plt.plot(stoke1x, label = 's1 - sum')
                plt.plot(stoke2x, label = 's2 - sum')
                plt.plot(stoke3x, label = 's3 - sum')
                plt.plot(stoke0wX, ':', label = 's0 - in')
                plt.plot(stoke1wX, ':', label = 's1 - in')
                plt.plot(stoke2wX, ':', label = 's2 - in')
                plt.plot(stoke3wX, ':', label = 's3 - in')
                plt.title("Stokes parameters evolution (x-cut)")
                plt.legend()
                plt.savefig(plots + 'stokeEvolutionX.png')
                print('Stokes parameter variation (x-cut) of wavefield saved to: ' + plots + 'stokeEvolutionX.png')
                plt.show()
                                
                plt.clf()
                plt.close()
                plt.plot(stoke0y, label = 's0 - sum')
                plt.plot(stoke1y, label = 's1 - sum')
                plt.plot(stoke2y, label = 's2 - sum')
                plt.plot(stoke3y, label = 's3 - sum')
                plt.plot(stoke0wY, ':', label = 's0 - in')
                plt.plot(stoke1wY, ':', label = 's1 - in')
                plt.plot(stoke2wY, ':', label = 's2 - in')
                plt.plot(stoke3wY, ':', label = 's3 - in')
                plt.title("Stokes parameters evolution (y-cut)")
                plt.legend()
                plt.savefig(plots + 'stokeEvolutionY.png')
                print('Stokes parameter variation (y-cut) of wavefield saved to: ' + plots + 'stokeEvolutionY.png')
                plt.show()
                
                print("Evolution of degree of polarisation")
                print("x-cut: {}".format(degPolarisationAvX))
                print("y-cut: {}".format(degPolarisationAvY))
                print("x-cut: {}".format(degPolarisationAvXn))
                print("y-cut: {}".format(degPolarisationAvYn))
                
                dp2x = ((stoke1x**2 + stoke2x**2 + stoke3x**2)**(1/2))/(stoke0x)
                dp2y = ((stoke1y**2 + stoke2y**2 + stoke3y**2)**(1/2))/(stoke0y)
                
                plt.clf()
                plt.close()
                plt.plot(degPolarisationAvX, label='x-cut from function')
                plt.plot(degPolarisationAvXn, label='x-cut (norm)')
                plt.plot(dp2x, label='x-cut from normalised stokes')
                plt.plot(degPolarisationAvY, label='y-cut from function')
                plt.plot(degPolarisationAvYn, label='y-cut (norm)')
                plt.plot(dp2y, label='y-cut from normalised stokes')
                plt.title("Degree of Polarisation evolution")
                plt.legend()
                plt.savefig(plots + 'degPolEvolution.png')
                print('Degree of Polarisation variation of wavefield saved to: ' + plots + 'degPolEvolution.png')
                plt.show()               
                                
                plt.clf()
                plt.close()
                plt.plot(maxE)
                plt.title("Maximum E amplitude")
                plt.show()
                
                plt.clf()
                plt.close()
                plt.plot(maxI)
                plt.title("Maximum I amplitude")
                plt.show()
                
            elif stokes == 1:
                plt.clf()
                plt.close()
                fig, axs = plt.subplots(1,2)
                sPol = np.sqrt(sFin[1]**2 + sFin[2]**2 + sFin[3]**2)
                sUnPol = sFin[0]-sPol
                pMin = np.min([sPol,sUnPol])
                pMax = np.max([sPol,sUnPol])
                im1 = axs[0].imshow(sPol, cmap='cividis')#, vmin=pMin, vmax=pMax)
                axs[0].set_title("Polarised component")
                im2 = axs[1].imshow(sUnPol, cmap='cividis')#, vmin=pMin, vmax=pMax)
                axs[1].set_title("Unpolarised component")
                
                for ax in axs.flat:
                    ax.set(xlabel="x position [pixels]", ylabel="y position [pixels] ")
                # Hide x labels and tick labels for top plots and y ticks for right plots.
                for ax in axs.flat:
                    ax.label_outer() #(10,8)
                # fig.subplots_adjust(right=0.8)
                plt.subplots_adjust(bottom=0.1, right=1.8, top=0.9)
                cax2 = plt.axes([1.85, 0.1, 0.06, 0.8])
                cax1 = plt.axes([0.9, 0.1, 0.06, 0.8])
                # plt.colorbar(im1, cax=cax1)
                # cbar_ax1 = fig.add_axes([8.85, 9.15, 0.05, 8.7])
                plt.colorbar(im1, cax=cax1)
                plt.colorbar(im2, cax=cax2)
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
                print(degPolarisationAvN)
                
                dp2 = ((stoke1**2 + stoke2**2 + stoke3**2)**(1/2))/(stoke0)
                
                plt.clf()
                plt.close()
                plt.plot(degPolarisationAv, label='from function')
                plt.plot(degPolarisationAvN, label='from function - norm')
                plt.plot(dp2, label='from normalised stokes')
                plt.title("Degree of Polarisation evolution")
                plt.legend()
                plt.savefig(plots + 'degPolEvolution.png')
                print('Degree of Polarisation variation of wavefield saved to: ' + plots + 'degPolEvolution.png')
                plt.show()
                
                plt.clf()
                plt.close()
                plt.plot(maxE)
                plt.title("Maximum E amplitude")
                plt.show()
                
                plt.clf()
                plt.close()
                plt.plot(maxI)
                plt.title("Maximum I amplitude")
                plt.show()
                
    wfinal = Wavefront(srwl_wavefront=wfr)
    if plots != None:
        Ifinal = wfinal.get_intensity()
        IfinalH = wfinal.get_intensity(polarization='horizontal')
        IfinalV = wfinal.get_intensity(polarization='vertical')
        
        # plt.clf()
        # plt.close()
        # plt.imshow(Ifinal)
        # plt.title("Final wavefield Intensity")
  
        plt.clf()
        plt.close()
        fig, axs = plt.subplots(1,3)
        IMin = np.min(Ifinal)
        IMax = np.max(Ifinal)
        im = axs[0].imshow(IfinalH, cmap='gray', vmin=IMin, vmax=IMax)
        axs[0].set_title("Horizontally Polarised")
        axs[1].imshow(Ifinal, cmap='gray', vmin=IMin, vmax=IMax)
        axs[1].set_title("Final Wavefield Intensity")
        axs[2].imshow(IfinalV, cmap='gray', vmin=IMin, vmax=IMax)
        axs[2].set_title("Vertically Polarised")
                
        for ax in axs.flat:
            ax.set(xlabel="x position [pixels]", ylabel="y position [pixels] ")
        # Hide x labels and tick labels for top plots and y ticks for right plots.
        for ax in axs.flat:
            ax.label_outer()
        # fig.subplots_adjust(right=0.8)
        # cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
        # fig.colorbar(im, cax=cbar_ax)
        plt.subplots_adjust(bottom=0.1, right=1.8, top=0.7)
        cax1 = plt.axes([1.85, 0.1, 0.06, 0.6])
        plt.colorbar(im, cax=cax1)
                
        plt.savefig(plots + 'finalIntensity.png')
        print('Intensity of final wavefield saved to: ' + plots + 'finalIntensity.png')
        plt.show()    
  
    
    if savePath != None:
        wfinal.store_hdf5(savePath)
        print('Wrote final wavefront file to ' + savePath)
    elif savePath == None:
        print("... saving of final wavefront disabled")
    
    
    print("------ Done ------")
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
    
    eh = wfr.arEx 
    ev = wfr.arEy
    
    plt.plot(eh)
    plt.show()
    plt.plot(ev)
    plt.show()
    
    """ Converting Gaussian to Wavefront() structure"""
    wf = Wavefront(srwl_wavefront=w)
        
    intensity = np.squeeze(wf.get_intensity())           
    plt.imshow(intensity)
    plt.title("Intensity")
    plt.show()


    print ('-----Getting Stokes parameters-----')
    S, Dx, Dy = getStokes(wfr, mutual=mutual, Fx = Fx, Fy = Fy)
    s = getStokesParamFromStokes(S) # 2-dimensional stokes parameters
#    s = getStokesParamFromStokes(S,d=1)
    # _s = normaliseStoke(s)
    print(Dx)
    print("-----Plotting Stokes parameters-----")
    plotStokes(s,dx=Dx,dy=Dy)
#    plotStokesCuts(s)
    
    # print("-----Plotting normalised Stokes parameters-----")
    # plotStokes(_s,S,"_s0","_s1","_s2","_s3")
    
    
    print("-----Getting degree of coherence from Stokes parameters------")
    # start1 = time.time()
    # coherenceFromSTKS(S,Dx,Dy)
    # end1 = time.time()
    # print("Time taken to get degree of coherence from Stokes (s): {}".format(end1 - start1))
    
    print ('------Done------')


def testColorbar():
    # Fixing random state for reproducibility
    np.random.seed(19680801)
    
    fig, axs = plt.subplots(1,3)
    axs[0].imshow(np.random.random((100, 100)), cmap=plt.cm.BuPu_r)
    axs[1].imshow(np.random.random((100, 100)), cmap=plt.cm.BuPu_r)
    axs[2].imshow(np.random.random((100, 100)), cmap=plt.cm.BuPu_r)
    
    plt.subplots_adjust(bottom=0.01, right=0.8, top=0.9)
    cax = plt.axes([0.85, 0.1, 0.075, 0.8])
    plt.colorbar(cax=cax)
    plt.show()

def testMultiFunc():
    """ Loading hdf5 wavefields for testing """
    ran = range(0,60,10)
    
    dirPath = '/home/jerome/dev/experiments/beamPolarisation14/data/'
#    folders = ['t' + str(i) + '/' for i in ran]
    wfr_files = [dirPath + 'Clt/wf_tcl.hdf', dirPath + 'Crt/wf_tcr.hdf', dirPath + 'Ldt/wf_tld.hdf', dirPath + 'Et/wf_te.hdf'] #,'Lvt/wf_tlv.hdf', 'Lht/wf_tlh.hdf', 'wf_tclOP.hdf', 'wf_tcrOP.hdf','wf_tldOP.hdf','wf_teOP.hdf','wf_tlvOP.hdf', 'wf_tlhOP.hdf']
     #[dirPath + f + 'wf_final.hdf' for f in folders] #['wf_tcl.hdf', 'wf_tcr.hdf','wf_tld.hdf','wf_te.hdf'] #,'wf_tlv.hdf', 'wf_tlh.hdf', 'wf_tclOP.hdf', 'wf_tcrOP.hdf','wf_tldOP.hdf','wf_teOP.hdf','wf_tlvOP.hdf', 'wf_tlhOP.hdf']
    
    sumWaves(wavefronts=[dirPath +'Clt/wf_tcl.hdf', dirPath + 'Crt/wf_tcr.hdf'], sampleFraction=0.08, stokes=0, norm='E', plots=dirPath + 'plots/')#,savePath=dirPath + 'TESTwfSum.hdf')


def testSumStokes():
    dirPath = '/home/jerome/dev/experiments/beamPolarisation14/data/'
    wfr_files = [dirPath + 'Clt/wf_tcl.hdf', dirPath + 'Crt/wf_tcr.hdf']
    
    wavefronts= wfr_files
    print("Wavefront files to be added:")
    print(wavefronts)
    
    sampleFraction = 0.75

    for i, f in enumerate(wavefronts):
        print(" ")
        print('Loading wavefront #{} from file {}'.format(i+1, f) )
        w = Wavefront()
        w.load_hdf5(f)
        
        # Defining parameters
        nx = int(sampleFraction*w.params.Mesh.nx)
        ny = int(sampleFraction*w.params.Mesh.ny)
        nz = 1
        zMin = w.params.Mesh.zCoord
        eMin = w.params.photonEnergy #Initial Photon Energy [eV]
        xMin = sampleFraction*w.params.Mesh.xMin #Initial Horizontal Position [m]
        xMax = sampleFraction*w.params.Mesh.xMax #Final Horizontal Position [m]
        yMin = sampleFraction*w.params.Mesh.yMin #Initial Vertical Position [m]
        yMax = sampleFraction*w.params.Mesh.yMax #Final Vertical Position [m]
        Etot = w._srwl_wf.arEx + w._srwl_wf.arEy
        exMax = np.max(w._srwl_wf.arEx)
        eyMax = np.max(w._srwl_wf.arEy)
        eTotMax = np.max(abs(Etot))
        print("MAX E (x,y): {}".format((exMax,eyMax)))
        eMax = max(exMax,eyMax)
        print("MAXIMUM E: {}".format(eMax))
        print("MAX E-TOT: {}".format(eTotMax))
        Imax = np.max(w.get_intensity())
        print("MAX I: {}".format(Imax))
        # E = np.array(w._srwl_wf.arEx,w._srwl_wf.arEy)
        # normE = np.max(E)
        # print(w._srwl_wf.arEx)
        # print(np.max(w._srwl_wf.arEx))
        # print(w._srwl_wf.arEx/np.max(w._srwl_wf.arEx))
        
        _Ex = np.reshape(w._srwl_wf.arEx, (w.params.Mesh.nx, w.params.Mesh.ny, 2))
        _Ey = np.reshape(w._srwl_wf.arEy, (w.params.Mesh.nx, w.params.Mesh.ny, 2))
        
        midEhx = np.shape(_Ex)[0]/2
        midEhy = np.shape(_Ex)[1]/2
        midEvx = np.shape(_Ey)[0]/2
        midEvy = np.shape(_Ey)[1]/2
        
        Ex = _Ex[int(midEhx - midEhx*sampleFraction):int(midEhx + midEhx*sampleFraction),int(midEhy - midEhy*sampleFraction):int(midEhy + midEhy*sampleFraction), :].flatten()
        Ey = _Ey[int(midEvx - midEvx*sampleFraction):int(midEvx + midEvx*sampleFraction),int(midEvy - midEvy*sampleFraction):int(midEvy + midEvy*sampleFraction), :].flatten()
        
        Eh = Ex
        Ev = Ey
            
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
        
        print ('-----Getting Stokes parameters-----')
        S, Dx, Dy = getStokes(wf, mutual=0, Fx = 1, Fy = 1)
        s= getStokesParamFromStokes(S,d=2)
        sn = normaliseStoke(s,d=2)
        plotStokes(s,dx=(xMax-xMin)/nx, dy=(yMax-yMin)/ny, savePath=None)
        
        
if __name__ == '__main__':
    test()
    # testMulti()
#    testMultiFunc()
    # testColorbar()
#    testSumStokes()


# %%
