#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 11:50:06 2020

@author: gvanriessen


Draft code - under development

Intended purpose of this code is to support the generation of randomly
rough surfaces, with and wihout correlation, for SRW masks
"""


import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
#import statsmodels
from statsmodels.tsa.stattools import acovf

def generateGrid(Nx,Ny,Rx,Ry):
    '''
    Generate a grid of Nx*Ny points with length scale Rx*Ry
    Returns x and y values in units of Rx and Ry
    '''
    x = np.linspace(-Rx/2,Rx/2,Nx) 
    y = np.linspace(-Ry/2,Ry/2,Ny)
    xv, yv = np.meshgrid(x, y, sparse=False, indexing='xy')
    
    return xv, yv

def getHDF(z,bins=None):
    '''
    (using numpy)
    Calculate  Height Density Function (distribution) for the height values
    in z.  The number of bins will be automatically determined unless
    specified.
    Returns the frequency values in n and bin index in bins (bin widths are not 
     scaled]  to length units))
    
    '''

    if bins is None:
        hist, bin_edges =  np.histogram(z, bins='auto')
    else:
        hist, bin_edges =  np.histogram(z, bins=bins)
   
    
    return hist, bins


def plotHDF(z,bins='auto', outFileName=None):
    '''
    (using pyplot, which uses numpy's histogram)
    Calculate and plot the Height Density Function (distribution) for the height values
    in z.  The number of bins will be automatically determined unless
    specified.
    Returns the frequency values in n and bin index in bins (bin widths are not 
     scaled]  to length units))
    Will save plot if valid filepath supplied via outFileName
    Note: it would be better to separate the determination of HDF from plotting/saving features
    '''
    
    if bins is None:
        n, bins, _ = plt.hist(z.ravel(), bins=bins,  density=True, color="lightblue")
    else:
        n, bins, _ = plt.hist(z.ravel(), bins=bins,  density=True, color="lightblue")
   
    
    plt.ylim(0.0,max(n)+0.05)
    plt.title('Height Distribution')
    plt.grid()
    plt.show()
        
    if outFileName is not None:
        plt.savefig(outFileName, bbox_inches='tight')

    return n, bins


def generateRandomRoughness2D(Nx, Ny, Rx, Ry, h=100e-9, sigma=50e-9, clx=0, cly=0):
    '''
    Generates randomly rough surface with Gaussian distribution of heights, with 
    width given by sigma and height h. 
    Correlation is (optionally) introduced along x and y by
    convolution with a gaussian of width equal to the correlation length in x and y.
    
    ** TODO: check/understand relationship between correlation length input parameters
    and resulting correlation length as measured by conventional approaches.
    
    Parameters:
    
    Nx, Ny: number of points along x and y
    Lx, Ly: length of sides along x and y direction
    clx, cly: correlation length along x and y
    h: rms height
    
    Returns:
        z: heights
        x, y: positions in length units of input parameters
    '''

    x, y = generateGrid(Nx,Ny,Rx,Ry)
    
    # generare uncorrlated Gaussian random height distribution with mean 0 and std deviation h
    z = h + sigma * np.random.randn(Nx*Ny)
    z = np.reshape(z, (Ny, Nx))
    
    if clx != 0 or cly != 0:
        
        # Gaussian kernel
        F = np.exp(-(np.square(x)/(np.square(clx)/2)+np.square(y)/(np.square(cly)/2)))
    
        # correlated surface generation
        #f = 2/np.sqrt(pi)*  Rx/N/sqrt(clx)/sqrt(cly)*    ifft2(fft2(z).*fft2(F))
        z = signal.fftconvolve(z, F, mode='same')
    
    return z, x, y


def getCorrelationLength(ACF,lags):
    '''
    Compute the length of correlation along x (and y if 2D) in roughness values z

    '''
    
    # find index of first value below 1/e
    index = list(map(lambda k: k < 1/np.e, ACF)).index(True)
  
    return lags[index]
    
    
    
    
    
def getACF(z,x,y=None,lags=None):
    '''
    Compute the autocovariation  averaged over x and y
   '''    
    if y is not None:
        try:
            Nx, Ny = np.shape(z)
        except ValueError:
            print('Could not get 2 dimensions of z') 
        #ylags = np.linspace(0,x(Ny-1)-x(0),Ny)    
    else:
        Nx, _ = np.shape(z)
        Ny = 1
    #xlags = np.linspace(0,x(Nx-1)-x(0),Nx)         

    # should the mean be removed first?

    # a guess that the number of lags should be 1/10
    if lags is None:
        nxlags, nylags = int(Nx/10), int(Ny/10)
    else:
        nxlags, nylags = int(lags), int(lags)
        
    xv = np.linspace(0,np.max(x)-np.min(x),nxlags)
    yv = np.linspace(0,np.max(y)-np.min(y),nylags)

    # autocovariance function calculation
    acfx = np.zeros(nxlags)
    acfy = np.zeros(nylags)
     
    for i in range(Nx):
       #cx = statsmodels.tsa.stattools.acf(z[i,:], unbiased=False, fft=True, nlags=nxlags)
       cx = acovf(z[i,:], unbiased=False, demean=True, 
                                            fft=True, missing='none', nlag=nxlags)
       acfx = acfx + cx[1:] #  cumulative sum
    acfx = acfx/Nx   # average
    acfx = acfx / np.max(acfx) # normalise
    
    for i in range(Ny):
       #cy = statsmodels.tsa.stattools.acf(z[:,i], unbiased=False, fft=True, nlags=nylags)
       cy = acovf(z[:,i], unbiased=False, demean=True, 
                                            fft=True, missing='none', nlag=nylags)
       acfy = acfy + cy[1:]   #  cumulative sum
    acfy = acfy/Ny   # average
    acfy = acfy / np.max(acfy)
    
    return acfx, xv,  acfy, yv
    
def plotACF(acf,x, outFileName=None):
    plt.plot(x*1e9,acf,label="ACF x")
    plt.xlabel("Distance [nm]")
    plt.ylabel("Autocovariance value")
    plt.legend()
    plt.show()

    if outFileName is not None:
        plt.savefig(outFileName, bbox_inches='tight')

def test():
    # uncorrelated example
    z,x,y = generateRandomRoughness2D(500, 500, 10e-6, 10e-6, h=100e-9, sigma=20e-9)
    plt.imshow(z)
    plt.show()
    i,d = getHDF(z)
    plt.plot(i)
    plt.show()

    #correlated example
    z,x,y = generateRandomRoughness2D(500, 500, 10e-6, 10e-6, h=100e-9, sigma=20e-9, clx = 40e-9, cly=100e-9)
    plt.imshow(z)
    plt.show()
    i,d = getHDF(z)
    plt.plot(i)
    plt.show()
   
    z = np.csvread('filename.csv')
    x = np.linspace(0,1e-3,np.shape(z)[0])

    acfx, xv, acfy, yv = getACF(z,x[0,:],y[:,0])
    xl = getCorrelationLength(acfx,xv)
    yl = getCorrelationLength(acfy,yv)
    plt.plot(xv*1e9,acfx,label="ACF x, correlation length={} nm".format(xl))
    plt.xlabel("Distance [nm]")
    plt.ylabel("Autocovariance value")
    plt.legend()
    plt.show()
    plt.plot(yv*1e9,acfy,label="ACF y, correlation length={} nm".format(yl))
    plt.xlabel("Distance [nm]")
    plt.ylabel("Autocovariance value")
    plt.legend()
    plt.show()
    
if __name__ == '__main__':
    test()
    