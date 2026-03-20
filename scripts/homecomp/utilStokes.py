# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 12:32:22 2021

@author: jerome
"""

# %%
#from wpg.wavefront import Wavefront
import numpy as np
import matplotlib.pyplot as plt
import time
# from wpg.wavefront import Wavefront
# from wpg.generators import build_gauss_wavefront
# from wpg.srwlib import SRWLStokes, SRWLWfr

from math import log10, floor

import pylab

#plt.style.use(['science','high-vis','no-latex']) # 'ieee', high-vis, high-contrast
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
    from wpg.srwlib import SRWLStokes, SRWLWfr
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
    
    w.calc_stokes(stk)
    
    # print("mutual:")
    # print(stk.mutual)
    
    return stk, Dx ,Dy

def normaliseStoke(S, d=2, outputArray=False):
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
    outputArray:
        Enable/Disable returning a normalised array of equal size as input array

    Returns
    -------
    Normalised stokes vector
    if d=1 - 2 stokes vectors, x-cut and y-cut
    if d=2 - single stokes vector
    
    Array of normalised stokes parameters - only if outputArray=True

    """
    print("STOKE SHAPE: {}".format(np.shape(S)))
    
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
        
        if outputArray == True:    
            Sn = _s0x,_s1x,_s2x,_s3x,_s0y,_s1y,_s2y,_s3y
            return _sX, _sY, Sn
        else:
            return _sX, _sY
    
    elif d == 2:
        s0,s1,s2,s3 = S[0], S[1], S[2], S[3]
        
        _s0 = s0/np.max(s0)
        _s1 = s1/np.max(s0)
        _s2 = s2/np.max(s0)
        _s3 = s3/np.max(s0)
    
        # _s = np.array([[_s0.mean(),_s1.mean(),_s2.mean(),_s3.mean()]]).T
        _s = np.array([[np.max(_s0),np.max(_s1),np.max(_s2),np.max(_s3)]]).T
        
        print("Normalised Stokes vector:")
        print(_s)
        if outputArray == True:
            Sn = _s0,_s1,_s2,_s3
            return _s, Sn
        else:
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
    

def plotStokes(s,dx=1,dy=1, savePath=None, compact=False):
               # fig1='S0',fig2='S1',fig3='S2',fig4='S3', Dx=50e-6, Dy=50e-6,
               # pathS0 = None, pathS1 = None, pathS2 = None, pathS3 = None,
               # pathD = None, pathE = None, pathIn = None):
    
    # print("Shape of S: {}".format(np.shape(S)))
    print("Shape of s: {}".format(np.shape(s)))
    
    try:
        Nx = int(np.squeeze(np.shape(s[0][:][0])))
        Ny = int(np.squeeze(np.shape(s[0][0][:])))
    except TypeError:
        Nx = int(np.squeeze(np.shape(s[:][0])))
        Ny = int(np.squeeze(np.shape(s[0][:])))
        
    if Nx == Ny:
        Nx = np.shape(s)[2]
        Ny = np.shape(s)[1]
        
    # print("Nx={}".format(Nx))
    # print("Ny={}".format(Ny))
    
    """ Creating array of custom tick markers for plotting """
    tickX = [0, Nx/4, Nx/2, 3*Nx/4, Nx-1]
    tickY = [0, Ny/4, Ny/2, 3*Ny/4, Ny-1]
    labX = [round_sig(-dx*Nx/2),round_sig(-dx*Nx/4),0,round_sig(dx*Nx/4),round_sig(dx*Nx/2)]
    labY = [round_sig(dy*Ny/2),round_sig(dy*Ny/4),0,round_sig(-dy*Ny/4),round_sig(-dy*Ny/2)]
    
    
    D, Davg, e, i, c = getPolarisationCharacteristics(S=None,Sparam=s)
    
    if compact:
        print("plotting Stokes parameters (S0, S1, S2, S3) (compact)...")
        plt.clf()
        plt.close()
        smin = np.min([s[0],s[1],s[2],s[3]])
        smax = np.max([s[0],s[1],s[2],s[3]])
        fig, axs = plt.subplots(1, 4)
        plt.setp(axs, 
                 xticks=tickX,
                 xticklabels=labX,
                 yticks=tickY,
                 yticklabels=labY)
        im = axs[0].imshow(s[0], cmap='RdYlBu_r', vmin=smin, vmax=smax, aspect=1)#)#, aspect=0.045)#1)#0.045)#'auto')#1)#
        axs[0].set_title('$S_0$')
        axs[1].imshow(s[1], cmap='RdYlBu_r', vmin=smin, vmax=smax, aspect=1)#)#, aspect=0.045)#1)#0.045)#'auto')#1)
        axs[1].set_title('$S_1$')
        axs[2].imshow(s[2], cmap='RdYlBu_r', vmin=smin, vmax=smax, aspect=1)#)#, aspect=0.045)#1)#0.045)#'auto')#1)
        axs[2].set_title('$S_2$')
        axs[3].imshow(s[3], cmap='RdYlBu_r', vmin=smin, vmax=smax, aspect=1)#)#, aspect=0.045)#1)#0.045)#'auto')#1)
        axs[3].set_title('$S_3$')
    
        for ax in axs.flat:
            ax.set(xlabel="x position [mm]", ylabel="y position [mm] ")
        # Hide x labels and tick labels for top plots and y ticks for right plots.
        for ax in axs.flat:
            ax.label_outer()
        fig.subplots_adjust(right=0.8)
        cbar_ax = fig.add_axes([0.82, 0.4, 0.025, 0.2])
        fig.colorbar(im,cax=cbar_ax)#fraction=0.05, pad=0.04) #cax=cbar_ax)
        if savePath != None:
            print("Saving Stokes Plots to: {}".format(savePath  + 'stokesPlot.png'))
            plt.savefig(savePath + 'stokesPlot.png')
            plt.savefig(savePath + 'stokesPlot.png', dpi=2000)
        plt.show()
        plt.clf()
    
    else:
        print("plotting Stokes parameters (S0, S1, S2, S3)...")
        plt.clf()
        plt.close()
        smin = np.min([s[0],s[1],s[2],s[3]])
        smax = np.max([s[0],s[1],s[2],s[3]])
        fig, axs = plt.subplots(2, 2)
        plt.setp(axs, 
                 xticks=tickX,
                 xticklabels=labX,
                 yticks=tickY,
                 yticklabels=labY)
        im = axs[0, 0].imshow(s[0], cmap='RdYlBu_r', vmin=smin, vmax=smax, aspect='auto')
        axs[0, 0].set_title('$S_0$')
        axs[0, 1].imshow(s[1], cmap='RdYlBu_r', vmin=smin, vmax=smax, aspect='auto')
        axs[0, 1].set_title('$S_1$')
        axs[1, 0].imshow(s[2], cmap='RdYlBu_r', vmin=smin, vmax=smax, aspect='auto')
        axs[1, 0].set_title('$S_2$')
        axs[1, 1].imshow(s[3], cmap='RdYlBu_r', vmin=smin, vmax=smax, aspect='auto')
        axs[1, 1].set_title('$S_3$')
    
        for ax in axs.flat:
            ax.set(xlabel="x position [m]", ylabel="y position [m] ")
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

    
    print('Average degree of polarisation = {}'.format(Davg))
    print('Average ellipticity = {}'.format(np.mean(e)))
    print('Average inclination = {}'.format(np.mean(i)))
    print ('Chirality: {}'.format(c))
    
    
    sPol = np.sqrt(s[1]**2 + s[2]**2 + s[3]**2)
    sUnPol = s[0]-sPol
    
    fig, axs = plt.subplots(1,3)
    plt.setp(axs, 
             xticks=tickX,
             xticklabels=labX,
             yticks=tickY,
             yticklabels=labY)
    im1 = axs[0].imshow(sPol, cmap='cividis', aspect=1)#)#, aspect=0.045)#)#, vmin=pMin, vmax=pMax)
    axs[0].set_title("Polarised component", fontsize=20)
    im2 = axs[1].imshow(sUnPol, cmap='cividis', aspect=1,vmin=0,vmax=0.000001)#)#, aspect=0.045)#)#, vmin=pMin, vmax=pMax)
    axs[1].set_title("Unpolarised component", fontsize=20)
    im3 = axs[2].imshow(D,cmap='cividis', aspect=1, vmin=0, vmax=1)#)#, aspect=0.045)#, aspect='auto')
    axs[2].set_title('Degree of polarization', fontsize=20)#)
    axs[1].set_xlabel("x position [mm]", fontsize=20) # [\u03bcm]")#"(\u03bcm)")
    axs[2].set_xlabel("x position [mm]", fontsize=20)
    axs[0].set_xlabel("x position [mm]", fontsize=20)
    axs[0].set_ylabel("y position [mm]", fontsize=20)
    axs[1].set_xticklabels(labels=labX,fontsize=20) 
    axs[2].set_xticklabels(labels=labX,fontsize=20)
    axs[0].set_xticklabels(labels=labX,fontsize=20)
    axs[0].set_yticklabels(labels=labY,fontsize=20)
    # axs[0].tick_params(axis='x',labelsize=10)
    # axs[1].tick_params(axis='x',labelsize=10)
    axs[2].tick_params(axis='x',labelsize=20)
    fig.tight_layout()
    # axs[2].set_ylabel("Vertical Position [m]", fontsize=20)#"(\u03bcm)")
    # for ax in axs.flat:
    #     ax.set(xlabel="x position [mm]", ylabel="y position [mm] ")#, fontsize=20)
    # Hide x labels and tick labels for top plots and y ticks for right plots.
    for ax in axs.flat:
        ax.label_outer() #(10,8)
    # fig.subplots_adjust(right=0.8)
    plt.subplots_adjust(bottom=0.1, right=1.8, top=0.9)
    cax3 = plt.axes([1.835, 0.2, 0.04, 0.6])
    cax2 = plt.axes([1.215, 0.2, 0.04, 0.6])
    cax1 = plt.axes([0.625, 0.2, 0.04, 0.6])
    # plt.colorbar(im1, cax=cax1)
    # cbar_ax1 = fig.add_axes([8.85, 9.15, 0.05, 8.7])
    plt.colorbar(im1, cax=cax1).ax.tick_params(labelsize=20)
    plt.colorbar(im2, cax=cax2).ax.tick_params(labelsize=20)
    plt.colorbar(im3, cax=cax3),ax.tick_params(labelsize=20)
    # plt.savefig(plots + 'degPol.png')
    # print('Degree of Polarisation of final wavefield saved to: ' + plots + 'degPol.png')
    # fig.tight_layout()
    if savePath != None:
        print("Saving Deg of Pol figure to path: {}".format(savePath+'degPol.png'))
        plt.savefig(savePath + 'degPol.png') 
    plt.show()

    # plt.imshow(D,cmap='cividis', aspect='auto')
    # plt.title('Degree of polarization')
    # # plt.xticks(np.arange(0,Nx+1,Nx/4),tickX)
    # # plt.yticks(np.arange(0,Ny+1,Ny/4),tickY)
    # plt.xticks(tickX,labX)
    # plt.yticks(tickY,labY)
    # plt.xlabel("Horizontal Position [m]") # [\u03bcm]")#"(\u03bcm)")
    # plt.ylabel("Vertical Position [m]")#"(\u03bcm)")
    # if savePath != None:
    #     print("Saving Deg of Pol figure to path: {}".format(savePath+'degPol.png'))
    #     plt.savefig(savePath + 'degPol.png')
    # plt.colorbar()
    # plt.show()
    # plt.clf()    

    plt.imshow(e, aspect='auto')
    plt.title('Ellipticity')
    # plt.xticks(np.arange(0,Nx+1,Nx/4),tickAx)
    # plt.yticks(np.arange(0,Ny+1,Ny/4),tickAy)
    plt.xticks(tickX,labX)
    plt.yticks(tickY,labY)
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
    # plt.xticks(np.arange(0,Nx+1,Nx/4),tickAx)
    # plt.yticks(np.arange(0,Ny+1,Ny/4),tickAy)
    plt.xticks(tickX,labX)
    plt.yticks(tickY,labY)
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
    from wpg.wavefront import Wavefront
    from wpg.srwlib import SRWLStokes, SRWLWfr
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

def sumStokes(wavefronts, sampleFraction=1, dimensions=2, display=True , plotsPath=None, savePath=None):
    from wpg.wavefront import Wavefront
    from wpg.srwlib import SRWLStokes, SRWLWfr
    """
    Parameters
    ----------
    wavefronts : 
        Array of paths to hdf5 wavefront files
    sampleFraction:
        Fraction of the wavefield to sample from centre. Between 0 and 1.
    dimensions:
        Specify whether output is 2-dimensional arrays or 1-dimensional cuts in x & y
    display:
        enable/disable plots (True/False)
    plotsPath :
        Path to save plots of each wavefront and resulting summed wavefront
    savePath:
        Path to save final stokes
    Returns
    -------
    array of stokes parameters, dimensions depending on specicifications
        
        """

    print("----- Summing Stokes parameters of each wavefield -----")
    print(" ")
    print("Wavefront files to be added:")
    print(wavefronts)
    
    if dimensions==2:
        stokes = []
        stokesN = []
        P2 = []
    elif dimensions==1:
        stokesCut = []
        stokesCutN = []
        P1 = []
    
    Nx = []
    Ny = []
    Dx = []
    Dy = []
    mx = []
    Mx = []
    my = []
    My = []
    
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
        
        print ("-----Getting Stokes parameters of wavefront #{}-----".format(i+1))
        S, dX, dY = getStokes(wf, mutual=0, Fx = 1, Fy = 1)
        
        if dimensions==2:
            s= getStokesParamFromStokes(S,d=2)
            sn = normaliseStoke(s,d=2,outputArray=True)
            if display==True:
                try:
                    plotStokes(s,dx=(xMax-xMin)/nx, dy=(yMax-yMin)/ny, savePath=plotsPath + str(i+1))
                except TypeError:
                    plotStokes(s,dx=(xMax-xMin)/nx, dy=(yMax-yMin)/ny)
        elif dimensions==1:
            sCut = getStokesParamFromStokes(S,d=1)
            snCut = normaliseStoke(sCut,d=1,outputArray=True)
            if display==True:
                try:
                    plotStokesCuts(sCut, savePath=plotsPath + str(i+1))
                except TypeError:
                    plotStokesCuts(sCut)
                    
        
        if i == 0:
            if dimensions==2:    
                stokes.append(s)
                stokesN.append(sn[1])                
                Pchars = getPolarisationCharacteristics(Sparam=np.squeeze(stokes), d=2) #D, Davg, e, i, c
                P2.append(Pchars[1])
            elif dimensions==1:
                stokesCut.append(sCut)
                stokesCutN.append(snCut[2])
                Pchars = getPolarisationCharacteristics(Sparam=np.squeeze(stokesCut), d=1) #Dx, Dy, DavgX, DavgY
                P1.append([Pchars[2],Pchars[3]])
            
            Nx.append(nx)
            Ny.append(ny)
            Dx.append((xMax-xMin)/nx)
            Dy.append((yMax-yMin)/ny)
            mx.append(xMin)
            Mx.append(xMax)
            my.append(yMin)
            My.append(yMax)
        
        else:    
            if dimensions==2:
                # print("Dims:")
                # print("stokes: {}".format(np.shape(stokes)))
                # print("stokesN: {}".format(np.shape(stokesN)))
                # print("s: {}".format(np.shape(s)))
                # print("sn: {}".format(np.shape(sn)))
                stokes = np.squeeze(stokes)
                stokesN = np.squeeze(stokesN)
                stokes = [x + y for x,y in zip(s, stokes)]
                stokesN = [x + y for x,y in zip(sn[1], stokesN)]
                
                Pchars = getPolarisationCharacteristics(Sparam=stokes, d=2) #D, Davg, e, i, c
                P2.append(Pchars[1])
                
            elif dimensions==1:
                # stokesCut = [x + y for x,y in zip(sCut, stokesCut)]
                print("Dims:")
                print("stokesCut: {}".format(np.shape(stokesCut)))
                print("sCut: {}".format(np.shape(sCut)))
                print("stokesCutN: {}".format(np.shape(stokesCutN)))
                print("snCut: {}".format(np.shape(sCut)))
                stokesCut = np.squeeze(stokesCut)
                stokesCutN = np.squeeze(stokesCutN)
                print("stokesCut: {}".format(np.shape(stokesCut)))
                
                
                # stokesCut[0] = [x + y for x,y in zip(sCut[0],stokesCut[0])]
                # stokesCutN[0] = [x + y for x,y in zip(snCut, stokesCutN[0])]
                
                stokesCut = [x + y for x,y in zip(sCut,stokesCut)]
                stokesCutN = [x + y for x,y in zip(snCut, stokesCutN)]
                
                
                # stokesCut = [x + y for x,y in zip(sCut,stokesCut)]
                # stokesCut[0][:] = [x + y for x,y in zip(sCut[0][:],stokesCut[0][:])]
                # stokesCut[1][:] = [x + y for x,y in zip(sCut[1][:],stokesCut[1][:])]
                # stokesCut[2][:] = [x + y for x,y in zip(sCut[2][:],stokesCut[2][:])]
                # stokesCut[3][:] = [x + y for x,y in zip(sCut[3][:],stokesCut[3][:])]
                # stokesCut[4][:] = [x + y for x,y in zip(sCut[4][:],stokesCut[4][:])]
                # stokesCut[5][:] = [x + y for x,y in zip(sCut[5][:],stokesCut[5][:])]
                # stokesCut[6][:] = [x + y for x,y in zip(sCut[6][:],stokesCut[6][:])]
                # stokesCut[7][:] = [x + y for x,y in zip(sCut[7][:],stokesCut[7][:])]
                
                # stokesCutN[0][:] = [x + y for x,y in zip(snCut[0][:],stokesCutN[0][:])]
                # stokesCutN[1][:] = [x + y for x,y in zip(snCut[1][:],stokesCutN[1][:])]
                # stokesCutN[2][:] = [x + y for x,y in zip(snCut[2][:],stokesCutN[2][:])]
                # stokesCutN[3][:] = [x + y for x,y in zip(snCut[3][:],stokesCutN[3][:])]
                # stokesCutN[4][:] = [x + y for x,y in zip(snCut[4][:],stokesCutN[4][:])]
                # stokesCutN[5][:] = [x + y for x,y in zip(snCut[5][:],stokesCutN[5][:])]
                # stokesCutN[6][:] = [x + y for x,y in zip(snCut[6][:],stokesCutN[6][:])]
                # stokesCutN[7][:] = [x + y for x,y in zip(snCut[7][:],stokesCutN[7][:])]
                
                # plt.plot(stokesCut[0])
                # plt.show()
                # plt.plot(stokesCut[5])
                # plt.show()
                # stokesCut[0] = [x + y for x,y in zip(sCut[0],stokesCut[0])]
                # stokesCutN[0] = [x + y for x,y in zip(snCut, stokesCutN[0])]
                
                Pchars = getPolarisationCharacteristics(Sparam=stokesCut, d=1) #Dx, Dy, DavgX, DavgY
                P1.append([Pchars[2],Pchars[3]])
                

    print(" ")
    print("----- Finished summing stokes -----")
    print(" ")

    print(mx)
    print(Mx)
    print(my)
    print(My)
    


    Dx = Dx[0]
    Dy = Dy[0]
    Nx = Nx[0]
    Ny = Ny[0]
    mx = mx[0]
    Mx = Mx[0]
    my = my[0]
    My = My[0]

    # Defining ticks and labels for plotting
    Xtix = [0,     int(Nx)/4, int(Nx)/2, 3*int(Nx)/4, int(Nx)]
    Xlab = [mx,    mx/2,      0,         Mx/2,        Mx]
    Ytix = [0,     int(Ny)/4, int(Ny)/2, 3*int(Ny)/4, int(Ny)]
    Ylab = [my,    my/2,      0,         My/2,        My]
    
    if dimensions==2:
        totNS = normaliseStoke(stokes, d=2, outputArray=True)
        totNN = normaliseStoke(stokesN, d=2, outputArray=True)
        print("Shape of total stokes array: {}".format(np.shape(stokes[0])))
        
        D_pol = (np.sqrt(stokes[1]**2 + stokes[2]**2 + stokes[3]**2))/(stokes[0])
        D_polN = (np.sqrt(totNS[1][1]**2 + totNS[1][2]**2 + totNS[1][3]**2))/(totNS[1][0])
        
        if display == True:
            try:
                plotStokes(stokes,dx=(xMax-xMin)/nx, dy=(yMax-yMin)/ny, savePath=plotsPath+'finalStokes')
                plotStokes(totNS[1],dx=(xMax-xMin)/nx, dy=(yMax-yMin)/ny, savePath=plotsPath+'finalStokesNorm')
                plotStokes(totNN[1],dx=(xMax-xMin)/nx, dy=(yMax-yMin)/ny, savePath=plotsPath+'finalStokesTwiceNorm')
            except TypeError:
                plotStokes(stokes,dx=(xMax-xMin)/nx, dy=(yMax-yMin)/ny)
                plotStokes(totNS[1],dx=(xMax-xMin)/nx, dy=(yMax-yMin)/ny)
                plotStokes(totNN[1],dx=(xMax-xMin)/nx, dy=(yMax-yMin)/ny)
                
            plt.clf()
            plt.close()
            fig, axs = plt.subplots(1,2)
            plt.setp(axs, 
                     xticks=Xtix,
                     xticklabels=Xlab,
                     yticks=Ytix,
                     yticklabels=Ylab)
            sPol = np.sqrt(stokes[1]**2 + stokes[2]**2 + stokes[3]**2)
            sUnPol = stokes[0]-sPol
            sPolN = np.sqrt(totNS[1][1]**2 + totNS[1][2]**2 + totNS[1][3]**2)
            sUnPolN = totNS[1][0]-sPolN
            pMin = np.min([sPolN,sUnPolN])
            pMax = np.max([sPolN,sUnPolN])
            # im1 = axs[0,0].imshow(sPol, cmap='cividis')#, vmin=pMin, vmax=pMax)
            # axs[0,0].set_title("Polarised component")
            # im2 = axs[0,1].imshow(sUnPol, cmap='cividis')#, vmin=pMin, vmax=pMax)
            # axs[0,1].set_title("Unpolarised component")
            im1 = axs[0].imshow(sPolN, cmap='cividis', vmin=pMin, vmax=pMax)
            axs[0].set_title("Polarised component (Normalised)")
            im2 = axs[1].imshow(sUnPolN, cmap='cividis', vmin=pMin, vmax=pMax)
            axs[1].set_title("Unpolarised component (Normalised)")
            
            for ax in axs.flat:
                ax.set(xlabel="x position [pixels]", ylabel="y position [pixels] ")
            # Hide x labels and tick labels for top plots and y ticks for right plots.
            for ax in axs.flat:
                ax.label_outer() #(10,8)
            fig.subplots_adjust(right=0.8)
            plt.subplots_adjust(bottom=0.1, right=1.8, top=0.9)
            cax2 = plt.axes([1.85, 0.1, 0.06, 0.8])
            cax1 = plt.axes([0.9, 0.1, 0.06, 0.8])
            plt.colorbar(im1, cax=cax1)
            plt.colorbar(im2, cax=cax2)
            if plotsPath!=None:
                plt.savefig(plotsPath + 'PolComponents.png')
                print('Polarisation Components of final wavefield saved to: ' + plotsPath + 'PolComponents.png')
            plt.show()
            plt.clf()
            plt.close()
            
            # fig, axs = plt.subplots(1,2)
            plt.imshow(D_pol, cmap='cividis')
            plt.title("Final Degree of Polarisation")    
            plt.xticks(Xtix, Xlab)
            plt.yticks(Ytix, Ylab)
            plt.xlabel("x-position [m]")
            plt.ylabel("y-position [m]")
            plt.colorbar()
            if plotsPath!=None:
                plt.savefig(plotsPath + 'degPol.png')
                print('Degree of Polarisation of final wavefield saved to: ' + plotsPath + 'degPol.png')
                
            plt.show()
            plt.clf()
            plt.close()
            
            
            fig, axs = plt.subplots(1,3)
                                    # figsize(15,8))
            plt.setp(axs[0:2], 
                     xticks=Xtix,
                     xticklabels=Xlab)
            plt.setp(axs[1], 
                     yticks=Ytix,
                     yticklabels=Ylab)
            axs[0].plot(D_polN[:,int(np.shape(D_polN)[0]/2)])
            axs[0].set_title("x-cut")
            axs[1].imshow(D_polN, cmap='cividis')
            axs[1].set_title("Final Degree of Polarisation (Normalised)")
            axs[2].plot(D_polN[int(np.shape(D_polN)[1]/2),:])
            axs[2].set_title("y-cut")
            # plt.colorbar()
            if plotsPath!=None:
                plt.savefig(plotsPath + 'degPolNorm.png')
                print('Normalised Degree of Polarisation of final wavefield saved to: ' + plotsPath + 'degPolNorm.png')
            plt.show()
            plt.clf()
            plt.close()
            
            plt.plot(P2)
            # plt.plot([D[0] for D in P2], label='x-cut')
            plt.xticks(range(0,np.shape(P2)[0]),range(0,np.shape(P2)[0]))
            plt.title("Degree of Polarisation evolution")
            plt.xlabel("Number of summed wavefields")
            plt.ylabel("Average Degree of Polarisation")
            if plotsPath!=None:
                plt.savefig(plotsPath + 'degPolEvolution.png')
                print('Degree of Polarisation evolution saved to: ' + plotsPath + 'degPolEvolution.png')
            plt.show()
            plt.clf()
            plt.close()
    
    elif dimensions==1:
        totScuts = stokesCut #stokesX + stokesY
        totNcuts = normaliseStoke(stokesCut, d=1, outputArray=True)
        # totNcutsN = normaliseStoke(stokesCutN[0], d=1, outputArray=True)
        print("Shape of total stokes cuts array: {}".format(np.shape(totScuts))) 
    
        D_polx = (np.sqrt(totScuts[1]**2 + totScuts[2]**2 + totScuts[3]**2))/(totScuts[0])
        D_poly = (np.sqrt(totScuts[5]**2 + totScuts[6]**2 + totScuts[7]**2))/(totScuts[4])
        D_polxN = (np.sqrt(totNcuts[2][1]**2 + totNcuts[2][2]**2 + totNcuts[2][3]**2))/(totNcuts[2][0])
        D_polyN = (np.sqrt(totNcuts[2][5]**2 + totNcuts[2][6]**2 + totNcuts[2][7]**2))/(totNcuts[2][4])
        
        if display == True:
            try:
                print("Shape of stokes cuts array: {}".format(np.shape(stokesCut)))
                print("Shape of stokes cuts array: {}".format(np.shape(stokesCut)))
                plotStokesCuts(stokesCut, savePath=plotsPath+'finalStokes') 
                plotStokesCuts(totNcuts[2], savePath=plotsPath+'finalStokesNorm')  
                # plotStokesCuts(totNcutsN[2], savePath=plotsPath+'finalStokesTwiceNorm')
            except TypeError:
                plotStokesCuts(totScuts)
                plotStokesCuts(totNcuts[2])
                # plotStokesCuts(totNcutsN[2])
    
            plt.clf()
            plt.close()
            fig, axs = plt.subplots(2,2)           
            plt.setp(axs, 
                     xticks=Xtix,
                     xticklabels=Xlab)
            sPolx = np.sqrt(totScuts[1]**2 + totScuts[2]**2 + totScuts[3]**2)
            sPoly = np.sqrt(totScuts[5]**2 + totScuts[6]**2 + totScuts[7]**2)
            sUnPolx = totScuts[0]-sPolx
            sUnPoly = totScuts[4]-sPoly
            sPolxN = np.sqrt(totNcuts[2][1]**2 + totNcuts[2][2]**2 + totNcuts[2][3]**2)
            sPolyN = np.sqrt(totNcuts[2][5]**2 + totNcuts[2][6]**2 + totNcuts[2][7]**2)
            sUnPolxN = totNcuts[2][0]-sPolxN
            sUnPolyN = totNcuts[2][4]-sPolyN
            axs[0,0].plot(sPolx, label="x-cut")
            axs[0,0].plot(sPoly, label="y-cut")
            axs[0,0].set_title("Polarised component")
            axs[0,1].plot(sUnPolx, label="x-cut")
            axs[0,1].plot(sUnPoly, label="y-cut")
            axs[0,1].set_title("Unpolarised component")
            axs[1,0].plot(sPolxN, label="x-cut")
            axs[1,0].plot(sPolyN, label="y-cut")
            axs[1,0].set_title("Polarised component (Normalised)")
            axs[1,1].plot(sUnPolxN, label="x-cut")
            axs[1,1].plot(sUnPolyN, label="y-cut")
            axs[1,1].set_title("Unpolarised component (Normalised)")
            # for ax in axs.flat:
            #     ax.set(xlabel="x position [pixels]", ylabel="y position [pixels] ")
            # # Hide x labels and tick labels for top plots and y ticks for right plots.
            # for ax in axs.flat:
            #     ax.label_outer()
            axs[0,0].legend()
            axs[0,1].legend()
            axs[1,0].legend()
            axs[1,1].legend()
            if plotsPath!=None:
                plt.savefig(plotsPath + 'PolComponents.png')
                print('Polarisation Components of final wavefield saved to: ' + plotsPath + 'PolComponents.png')
            plt.show()
            plt.clf()
            plt.close()
            
            fig, axs = plt.subplots(1,3)
            plt.setp(axs, 
                     xticks=Xtix,
                     xticklabels=Xlab)
            axs[0].plot(D_polx)
            axs[0].set_title("D.pol x-cut")
            axs[1].plot(D_polx, label="x-cut")
            axs[1].plot(D_poly, label="y-cut")
            axs[1].legend()
            axs[2].plot(D_poly)
            axs[2].set_title("D.pol y-cut")
            if plotsPath!=None:
                plt.savefig(plotsPath + 'degPolCuts.png')
                print('Degree of Polarisation cuts of final wavefield saved to: ' + plotsPath + 'degPolCuts.png')
            plt.show()
            plt.clf()
            plt.close()
        
            fig, axs = plt.subplots(1,3)
            plt.setp(axs, 
                     xticks=Xtix,
                     xticklabels=Xlab)
            axs[0].plot(D_polxN)
            axs[0].set_title("D.pol x-cut (Normalised)")
            axs[1].plot(D_polxN, label="x-cut")
            axs[1].plot(D_polyN, label="y-cut")
            axs[1].legend()
            axs[2].plot(D_polyN)
            axs[2].set_title("D.pol y-cut (Normalised)")
            if plotsPath!=None:
                plt.savefig(plotsPath + 'degPolCutsNorm.png')
                print('Normalised Degree of Polarisation cuts of final wavefield saved to: ' + plotsPath + 'degPolCutsNorm.png')
            plt.show()
            plt.clf()
            plt.close()
            
            plt.plot([D[0] for D in P1], label='x-cut')
            plt.plot([D[1] for D in P1], label='y-cut') #Dx, Dy, DavgX, DavgY
            plt.xticks(range(0,np.shape(P1)[0]),range(0,np.shape(P1)[0]))
            plt.title("Degree of Polarisation evolution")
            plt.xlabel("Number of summed wavefields")
            plt.ylabel("Average Degree of Polarisation")
            plt.legend()
            if plotsPath!=None:
                plt.savefig(plotsPath + 'degPolCutsEvolution.png')
                print('Degree of Polarisation evolution saved to: ' + plotsPath + 'degPolCutsEvolution.png')
            plt.show()
            plt.clf()
            plt.close()
            
    
    if dimensions == 2:
        if savePath != None:
            import pickle
            with open(savePath, "wb") as g:
                pickle.dump(stokes[0], g)
                print("Final stokes parameters written to: {}".format(savePath))      
        else:
            print("... saving disabled")
        print(" ")
        print("===== DONE =====")
        return stokes[0]
    elif dimensions == 1:
        if savePath != None:
            import pickle
            with open(savePath, "wb") as g:
                pickle.dump(stokesCut, g)
                print("Final stokes parameters written to: {}".format(savePath))   
        else:
            print("... saving disabled")
        print(" ")
        print("===== DONE =====")   
        return stokesCut


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
    from wpg.wavefront import Wavefront
    from wpg.generators import build_gauss_wavefront
    from wpg.srwlib import SRWLStokes, SRWLWfr
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
    folders = ['t' + str(i) + '/' for i in ran]
    wfr_files = [dirPath + f + 'wf_final.hdf' for f in folders] #['wf_tcl.hdf', 'wf_tcr.hdf','wf_tld.hdf','wf_te.hdf'] #,'wf_tlv.hdf', 'wf_tlh.hdf', 'wf_tclOP.hdf', 'wf_tcrOP.hdf','wf_tldOP.hdf','wf_teOP.hdf','wf_tlvOP.hdf', 'wf_tlhOP.hdf']
    
    sumWaves(wavefronts=wfr_files, sampleFraction=0.08, stokes=0, norm='E', plots=dirPath + 'plots/')#,savePath=dirPath + 'TESTwfSum.hdf')


def testSumStokes():
    """ Loading hdf5 wavefields for testing """
    ran = range(0,100,10)
    
    dirPath = '/home/jerome/dev/experiments/beamPolarisation14/data/'
    folders = ['t' + str(i) + '/' for i in ran]
    wfr_files = [dirPath + f + 'wf_final.hdf' for f in folders] #['wf_tcl.hdf', 'wf_tcr.hdf','wf_tld.hdf','wf_te.hdf'] #,'wf_tlv.hdf', 'wf_tlh.hdf', 'wf_tclOP.hdf', 'wf_tcrOP.hdf','wf_tldOP.hdf','wf_teOP.hdf','wf_tlvOP.hdf', 'wf_tlhOP.hdf']
    
    save = False
    
    stokes = sumStokes(wavefronts=wfr_files, 
                       sampleFraction=0.2, 
                       dimensions=2,
                       display=True, 
                       plotsPath=None)
    if save:
        import pickle
        with open(dirPath + 'finalStokes.pkl', 'wb') as p:
            pickle.dump(stokes, p)

def sumStokesFromTif():
    ran = range(0,100,90)
    import tifffile
    dirPath = '/home/jerome/dev/experiments/beamPolarisation17/data/degrees/'
    savePath = '/home/jerome/Documents/MASTERS/Figures/plots/'
    numPix = 200
    
    interval = 90
    name = str(interval)
    
    ran = range(0,interval+10,interval)
    save = True
    
    dX, dY = 6.673209267855702e-06, 6.671991414331421e-06
    unitConversion = 1e3
    dX, dY = unitConversion*dX, unitConversion*dY
    
    print(" ")
    print("--- Reading tiff files ---")
    stokesTifs = [[tifffile.imread(dirPath + 'i'+ str(r) + 'stokes0.tif'),
                    tifffile.imread(dirPath + 'i'+ str(r) + 'stokes1.tif'),
                    tifffile.imread(dirPath + 'i'+ str(r) + 'stokes2.tif'),
                    tifffile.imread(dirPath + 'i'+ str(r) + 'stokes3.tif')] for r in ran]
    
    # print(np.shape(stokesTifs))
    # print(stokesTifs)
    print("")
    print("... reshaping")
    resampleStokes = [[s[0][np.shape(s[0])[0]//2-(numPix//2):np.shape(s[0])[0]//2+(numPix//2),np.shape(s[0])[1]//2-(numPix//2):np.shape(s[0])[1]//2+(numPix//2)] for s in stokesTifs],
                      [s[1][np.shape(s[0])[0]//2-(numPix//2):np.shape(s[0])[0]//2+(numPix//2),np.shape(s[0])[1]//2-(numPix//2):np.shape(s[0])[1]//2+(numPix//2)] for s in stokesTifs],
                      [s[2][np.shape(s[0])[0]//2-(numPix//2):np.shape(s[0])[0]//2+(numPix//2),np.shape(s[0])[1]//2-(numPix//2):np.shape(s[0])[1]//2+(numPix//2)] for s in stokesTifs],
                      [s[3][np.shape(s[0])[0]//2-(numPix//2):np.shape(s[0])[0]//2+(numPix//2),np.shape(s[0])[1]//2-(numPix//2):np.shape(s[0])[1]//2+(numPix//2)] for s in stokesTifs]]
    # print(np.shape(resampleStokes))
    
    print("")
    print("... ... summing")
    finalStokes = [np.sum(resampleStokes[0],axis=0),
                   np.sum(resampleStokes[1],axis=0),
                   np.sum(resampleStokes[2],axis=0),
                   np.sum(resampleStokes[3],axis=0)]
    
    print("")
    print("... ... ... normalising")
    finalStokes[1] = finalStokes[1]/np.max(finalStokes[0])
    finalStokes[2] = finalStokes[2]/np.max(finalStokes[0])
    finalStokes[3] = finalStokes[3]/np.max(finalStokes[0])
    finalStokes[0] = finalStokes[0]/np.max(finalStokes[0])
    
    print("")
    print("... ... ... ... plotting")
    if save:
        plotStokes(finalStokes,dx=dX,dy=dY, savePath=savePath+name, compact=True)
    else:
        plotStokes(finalStokes,dx=dX,dy=dY,compact=True)

if __name__ == '__main__':
   # test()
    # testMulti()
#    testMultiFunc()
    # testColorbar()
    # testSumStokes()
    # sumStokesFromTif()

    import tifffile
    stokesTifs = [tifffile.imread('/home/jerome/dev/data/sourceNdBeam/maskPlane/100s0.tif'),
                    tifffile.imread('/home/jerome/dev/data/sourceNdBeam/maskPlane/100s1.tif'),
                    tifffile.imread('/home/jerome/dev/data/sourceNdBeam/maskPlane/100s2.tif'),
                    tifffile.imread('/home/jerome/dev/data/sourceNdBeam/maskPlane/100s3.tif')]
    
    stokesTifs = [s/np.max(stokesTifs[0]) for s in stokesTifs]
    dX, dY = 2.4633703639094306e-06, 2.406360648168151e-06
    plotStokes(stokesTifs,dx=dX*1e3,dy=dY*1e3,compact=True, savePath = '/home/jerome/Documents/MASTERS/Figures/plots/')
# %%
