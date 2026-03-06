#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 23:02:45 2021

@author: gvanriessen


Draft code to produce a non-redundant array (Like a Golomb ruler) in which values of 1 are separated
by unique intervals, and to produce an NRA grating representation suitable for
use in simulating methods of spatial coherence determination.

This code has not been fully tested.  Use with caution!



Added: utility functions for analysing intensity of far-field diffraction from NRA

"""

from itertools import combinations
from random import randrange
from scipy import ndimage
import scipy.fft as scifft
from scipy.optimize import curve_fit
from scipy.signal import find_peaks


import numpy as np
import matplotlib.pyplot as plt
import imageio


def triangle(x,c,a,s):
    #  return triangle with amplitude hc, width c, and slope a/2c, and shift s for list of x values
    return np.array([triangleAmp(t-s,c,a) for t in x])


def triangleAmp(x,c,a):
     #  return amplitude of triangle at point x with amplitude a, width c, and slope a/2c
     if x>=c/2:
          r = 0.0
     elif x<=-c/2:
          r = 0.0
     elif x > -c/2 and x<0:
          r=2*x/c*a+a
     else:
          r=-2*x/c*a+a
     return r


def Gamma(xi, xj, Gamma0,sigma, C):
    
    
    ''' defines model for the Fourier amplitude  of the diffraction pattern from the NRA of slits, i.e. 
        a set of trianglular peaks centred at the possible values of xi-xj, whose intensity is modulated by the 
        mutual coherence function, Gamma(xi,xj) = gamma(xi-xj)[I(xi)I(xj)]^(1/2)
        
        In the Gaussian Schell Model, this is given as:
                                    
        
            Gamma(xi,xj) = Gamma0 exp(-(xi-xj)^2 / (2*C))) * exp(-(xi^2 + xj^2)/(4*Sigma^2))
        
        where C is the coherence length and Sigma is the beam size.
        
        
        X is a list of each value of xi,xj for a NRA of slits
        
    '''
    
    return  Gamma0 * np.exp(-(xi-xj)**2 / (2*C**2)   )  *  np.exp(-(xi**2 + xj**2)/(4*sigma**2))



def modelNRAFT(xixj,Gamma0, sigma, C, sort=True):
    ''' generates model for the expected FFT of the diffraction intensity from NRA
    
        A is the list of slit positions (xi, xj) in units of m 
    '''
    
    x = []
    G = []
    for xi, xj in xixj:
        dx = xi-xj
        x.append(np.abs(dx))
        g = Gamma(xi, xj, Gamma0, sigma, C)
        G.append(g)
        print('(xi,xy) = ', xi, ',', xj, ', dx = ',dx,'. Gamma = ', g)

    if sort == True:
        G = [g for _, g in sorted(zip(x, G))]
        x = sorted(x)

    return x,G

def getFTAmpFromFile(path):
    
    xy = np.genfromtxt(path, delimiter=',')
    x = xy[1:,0]
    y = xy[1:,1]
    
    return getFTAmp(x,y)


def getFTAmp(x, I, plot=True):
    
    # Sample points
    N = len(x)
    # Sampling period, m
    T = np.abs(x[1]-x[0])
    
    yf = scifft.fft(I)
    yf = 2.0/N * np.abs(yf[0:N//2])
    xf = scifft.fftfreq(N, T)[:N//2]
    
    if plot == True:
        plt.plot(xf, yf,'.')
        plt.ylabel('FFT')
        plt.xlabel('Spatial frequency [1/m]')
        plt.grid()
        plt.show()

    return xf,yf


def fitTriangles(x,y,N):
    ''' unfinished/untested '''
    def func(x, *params):
        y = np.zeros_like(x)
        for p in range(0, len(params),3):
            width, amp, pos = p[i], p[i+1], p[i+2]
            y =np.add(y, triangle(x,width,amp,pos))
        return y
    
    
    for i in range(N):
        guess += [60+80*i, 46000, 25]   
    
    popt, pcov = curve_fit(func, x, y, p0=guess)
    print (popt)
    fit = func(x, *popt)
    
    plt.plot(x, y)
    plt.plot(x, fit , 'r-')
    plt.show()


def pairs(A):
    # return list of indices, one for each a pair of elements with value == 1
    return [(a,b) for a, b in combinations(indices(A), 2)]


def indices(A):
    # return list of indices of elements with value == 1
    return [i for i, x in enumerate(A) if x==1]


def pairIntervals(A):
    # return Intervals between indices 
    return [abs(a -b) for a, b in combinations(indices(A), 2)]
 
    
def pointIntervals(n,A):
    # return the distance of a point n from all indices in ind 
    return [np.abs(n-a) for a in indices(A)]


def matchingIntervals(n, d, A):
    return [i for i in pointIntervals(n,A) if i == d and i > 0]


def nonredundantIntervals(intervals, maxLength, start=0, strict=False, trim=False, maxTrials=None):
    
    '''
    Find non-redundant intervals listed in S within a list of maximum length
    maxLength.
    
    e.g.:
        nrI = nonredundantIntervals([10,12,14,16], 70, start=35, strict=False)
        
        
    Approach is to 'throw darts', i.e. randomly choose a position and check if it satisfies
    condition that the point is separated from another point by a distance listed in 'intervals' 
    and not by any distance not listed in 'intervals'.  This is terribly inefficient! Rationale for
    taking this approach was that sequential 
    
    '''
    ''' TODO: 1. implement smarter way to choose maxLength or extend if intervals can not be satisfied
              2. strict option does not prevent intervals larger than those in list (fix
                                                                                     
    '''
    
    S = intervals
    A = np.zeros(maxLength)
    
    A[start] = 1
    if strict==True:
        nonS = np.setdiff1d(range(maxLength),S)
    else:
        nonS = np.setdiff1d(range(max(S)),S)
    SMatched = np.zeros_like(S)
    seeking=True
    
    print('Disallowed intervals: ', nonS)
    
    iteration = 0
    while seeking == True:
        i = randrange(maxLength)
        matches = [matchingIntervals(i,s,A) for s in S]
        matches = [item for sublist in matches for item in sublist]
        if matches:
            # find which intervals would be created if point i is set to 1.
            newMatches = np.setdiff1d(matches,SMatched)
            if np.size(newMatches) > 0:
                # check for undesirable intervals created if point i is set to 1
                badMatches = [matchingIntervals(i,s,A) for s in nonS]
                badMatches = [item for sublist in badMatches for item in sublist] 
                
                print ('%d: %d matches %s, conflicts %s' % (iteration,i,newMatches,badMatches))
                
                #if np.size(newMatches) > 0 and np.size(badMatches) == 0:
                if np.size(badMatches) == 0:
                    
                    A[i] = 1 
                        
                    # update list of matched intervals
                    SMatched = np.concatenate((SMatched,newMatches))
                    
                    # remove zeros (not sure why they are appearing in list - needs better fix)
                    SMatched = [s for s in SMatched if s != 0]
                    print ('Matched: ', SMatched)
                    
                if all(elem in SMatched  for elem in S):
                    seeking = False
                    print('Done... all intervals found')
        
        iteration += 1
        if maxTrials is not None:
            if iteration > maxTrials:
                seeking = False
                print('Failed to find solution after %d trials' % iteration)

    if trim == True:
        A = A[np.min(indices(A)):np.max(indices(A))]
            
    intervals = pairIntervals(A)
    
    print('Intervals sought: ', np.sort(S) )
    print('Intervals satisfied: ', np.sort(intervals))
    print('Length: ', np.size(A))
    
    return A


def NRA(intervals, maxLength, h, width, start=0, strict=False, maxTrials=None):
    
    A = nonredundantIntervals(intervals, maxLength, start=start, strict=strict, trim=False,maxTrials=maxTrials)
    A2D = np.tile(A,[h,1])
    
    #struct1 = ndimage.generate_binary_structure(2, int(width/2))
    #struct1 = ndimage.iterate_structure(struct1, int(width/8)).astype(int)
    struct1 = np.zeros((width*2,width*2))
    struct1[:,width-int(width/2):width+int(width/2)] = 1
    A2D = ndimage.binary_dilation(A2D, structure=struct1).astype(A2D.dtype)
    
    return A2D, A


def test():
    ''' test creation of 1D NRA and export as 2D image '''
    
    # resolution
    pixRes = 1e7 # pixels / m
    
    # intervals (spacing) required for the NRA
    intervals_m = [8e-6,11e-6,12e-6,15e-6,16e-6,17e-6] # um
    
    intervals_px = np.array(np.multiply(intervals_m, pixRes), dtype=int)
    
    # conservative estimate of required array length
    maxLength = int(np.sum(intervals_m) * pixRes)
    
    height = int(10e-6 * pixRes)
    slitWidth = int(1e-6 * pixRes)
    startIndex = slitWidth*2  # better strategy?
    filename = 'nra.tif'
    
    NRA_arr, A =  NRA(intervals_px,maxLength, height, slitWidth, start=startIndex, strict=False, maxTrials = 10000)
    
    # display it
    plt.imshow(NRA_arr)
    plt.show()
    
    # display profile
    fig = plt.figure(figsize=(7,1))
    ax = fig.add_subplot(111)
    #x = np.linspace(0,np.size(NRA_arr[:,0]),int(np.size(NRA_arr)*pixRes))
    ax.plot(NRA_arr[0,:],'.')
    plt.show()
    
    # write to file
    scaled =  255*NRA_arr/np.max(NRA_arr)
    imageio.imwrite(filename, scaled.astype('int8'))
    
    print('Wrote ', filename)
    
    pairs_px = pairs(A)
    pairs_m = np.divide(pairs_px,pixRes)
    print('Pairs (pixel): ', pairs_px)
    print('Pairs (m): ', pairs_m)
    
    
    Gamma0=1.0
    Sigma = 160.e-6
    C = 17.e-6
    
    # model 
    X = np.linspace(0,np.max(np.divide(pairIntervals(A),pixRes))/2,400)
    Y = np.multiply(-1,X)
    XY = list(zip(Y, X))
    xm,Gm=modelNRAFT(XY,Gamma0, Sigma, C)
    
    
    # model values at each slit pair
    x,G=modelNRAFT(pairs_m,Gamma0, Sigma, C, sort=True)
    plt.xlabel('Slits separation [m]')
    plt.ylabel('Gamma')
    plt.plot(x,G,'o')
    plt.plot(xm,Gm)
    plt.show()
    

def testAnalysis():
    
   
    # Load experimental / simulated data, i.e. a line profile through the intensity of a diffraction 
    # pattern due to a NRA.
    xf,yf=getFTAmpFromFile('Intensity-Diffraction-WP-86-5m-Horizontal-Position.csv')
    
    
    # Try to find the peaks, ignoring anything with prominence of less than 5% of max. value
    # Note that this is a very approximate method - better to fit an ensemble of peaks.
    peaks, properties = find_peaks(yf,  prominence=(0.05*np.max(yf),None),width=1)
    
    Nf=np.size(peaks)
    pm = np.max(yf[peaks])
    print ('{:d} peaks found:'.format(Nf))
    for p in zip( properties["prominences"], properties["widths"]):
        print('Peak prominence: {0:.2f}%, width: {1} 1/um[CHECK UNITS!]'.format(p[0]/pm,p[1]))
    plt.plot(xf,yf)
    plt.plot(xf[peaks], yf[peaks], "x")
    plt.plot(np.zeros_like(xf), "--", color="gray")
    #plt.xlim([2800,3800])
    plt.show()
    
    # try dropping first three found prominences...  not generally necessary, but above peak
    # fitting  will tend to identify a prominence associated with the DC component.
    peaks = np.sort(peaks)
    peaksMod= peaks[2:]

    
    Xe = 2/(xf[peaksMod])
    XYe = list(zip(-Xe/2, Xe/2))
    
    # Initial guesses:
    Gamma0=1.0  # ???
    Sigma = 50.e-6
    C = 200.e-6
    
    
    ''' Your job is to fit the values of (XYe,yf[peaks]) to the model defined by modelNRAFT(X,Gamma0,Sigma,C) 
     to find the values of Sigma (beamsize) and C (coherence length).  '''
     
     
     '''''''