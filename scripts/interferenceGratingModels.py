#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 29 12:40:25 2020


This is intended to be a library of methods for analysing the properties 
of interference gratings and interference patterns.  It is under development and
mostly untested  — use with caution!

@author: gvanriessen
"""


import numpy as np
from numpy import sin, cos, exp, pi, sqrt, square
from scipy.signal import periodogram
from scipy.fftpack import fft, ifft, fftfreq
from scipy.signal import find_peaks, peak_widths
from findiff import FinDiff
from itertools import chain, zip_longest
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import argrelextrema

'''

    We are interested in MTF of the optical system, which may be calculated as 
    contrast as a function of frequency.
    
    Start here with methods to define contrast'
    
'''    



def getPhaseGradient(wf,polarization='horizontal'):
    ''' return phase gradient in x and y directions for wavefield wf
    **IGNORES slices
    '''
    
    phase = np.squeeze(wf.get_phase(polarization=polarization))
    gy,gx = np.gradient(phase)
            
    return gx, gy

    
#gx,gy=getPhaseGradient(wf)
#
#
#plt.figure()
#plt.suptitle("Phase and it gradient along each axis")
#ax = plt.subplot("131")
#ax.imshow(phase)
#ax.set_title("image")
#
#ax = plt.subplot("132")
#ax.imshow(gx,vmax=0.1, vmin=-0.1)
#ax.set_title("gx")
#
#ax = plt.subplot("133")
#ax.imshow(gy, vmax=0.1, vmin=-0.1)
#ax.set_title("gy")
#
#plt.colorbar()
#plt.show()


def lineProfile(A, ROI=None, AXIS = 0):
    '''
    make a line profile over a region of interest in a 2D array of values A 
    '''
    if ROI is None:
        a = A
    else:
         # get number of pixels in x and y
        Nx = np.shape(A)[1]
        Ny = np.shape(A)[0]
        
        x0,y0 = ROI[0][0], ROI[0][1]
        x1,y1 = ROI[1][0], ROI[1][1]
    
        a = A[y0:y1,x0:x1]
    
    profile = np.mean(a, axis=AXIS)

    return profile


def profilePeaks(A, ROI=None, AXIS = 0, H=[0.5], show=True):
    '''
    make a line profile over a region of interest in a 2D array of values A and
    find peaks and their width, where width is taken as the width at H*maximum peak height
    
    ROI specifies a region of interest in A. It should be a tuple of tuples 
    ((x0,y0),(x1,y1)),  where (x0,y0) is lower left corner, and (x1,y1) is upper right corner
    Height (width) of ROI may be 1 for a line profile over a single row (column) of pixels
    AXIS = 1  for profile along y direction, 0 for profile along x direction
    H or values h in H=[h1,h2,...] may be a list of values between 0 and 1.
    
    Displays array, ROI and peak finding results if show is True
    
    
    Returns:
        profile: the line profile over ROI for each value in H
        pos: peak positions for each value in H
        width: width of peaks for each value in H
        boundary: positions along profile where a peak rises and falls through a 
            line at a fraction each value in H of the peak height.
        avgWidth: average of peak widths for each value in H
    '''
    profile = lineProfile(A, ROI=ROI, AXIS = AXIS)

    pos, width, boundary = findPeaks(profile, H=[0.5,0.75])
    
    # find average widths
    avgWidth = np.mean(width,axis=1) 
    
    if show is True:
        plt.imshow(A)
        plt.show()
        plt.imshow(a)
        plt.show()
        
        plt.plot(profile, '-')
        plt.plot(pos, profile[pos], '*')
        plt.hlines(*boundary[0], color="C2")
        plt.hlines(*boundary[1], color="C3")
        plt.show()
    
    return profile, pos, width, boundary, avgWidth



def findPeaks(S,H=0.5):
    '''
    Find peaks return their position and width at some fraction H of their height.
    peak   in signal S that is defined over a range of values in P
    
    H or values h in H=[h1,h2,...] may be a list of values between 0 and 1.
    
    All in units of pixels, i.e. no scaling to pixel length here.
    '''
    if not isinstance(H, list):
        H = [H] # make it a list of length 1
    
    peaks, _ = find_peaks(S)   # peak indexes (see scipy.signal.find_peaks docs for more options)

    widths,boundaries=[],[]
    for h in H:
        w = peak_widths(S, peaks, rel_height=h)
        widths.append( w[0] )# widths of peaks at h * height
        boundaries.append(w[1:])
    return peaks, widths, boundaries


def getImageData(filename):
    import cv2
    im = cv2.imread(filename, cv2.IMREAD_ANYDEPTH )   # open any bit depth image (more readable than -1)    
    im = np.array(im)
    return im


def gratingContrastMichelson(A):
    '''
    Return Michelson contrast: $\frac{\max(I) - \min(I)}{\max(I) + \min(I)}$
    
    Michelson contrast is highly sensitive to noise. Since it is calculated only from extrema, i.e., at two pixels
    
    In the case where the optical fringe period is comparable to pixel size, Michelson contrast is also sensitive to the phase difference,between pixel grid and optical fringe signal. 
    '''
    maxA = np.max(A)
    minA = np.min(A)
    C = (maxA-minA) / (maxA+minA)
    return C


def gratingContrastRMS(A):
    '''
    Return root mean squared contrast. 
            
    RMS contrast does not depend on the angular frequency content or the spatial distribution of contrast in the image.
    '''    
    # normalise it first  ---  wrong to do this
    #A = (A-np.min(A))/(np.max(A)-np.min(A))    
    A = (A)/ np.max(A) 

    N = np.size(A)
    mean = np.mean(A)    
    C = sqrt( 1/N * np.sum(  square((A - mean)/mean)) )
    
    # fro comparison to Michelson Contrast:
    C = C * sqrt(2)
    
    return C


def NILS(I,x,w,show=True):
    '''
    Calculate Normalized Image Log-Slope (NILS) of a pattern
    
    pattern:  a 2d array that can be cast to float64 values, expected to contain 
              periodic patterns over axis 0 or 1.
              
    I: list of intensity values
    x: list of positions corresponding to the intensity values
    w: nominal linewidth
    '''
    
    lnI = np.log(I[:,0].astype('float64'))

    dx = (x[1] - x[0])/1000000
    d_dx = FinDiff(0, dx)
    gradAbs = np.abs(d_dx(lnI,acc=10))
    
    d = int(w/dx)
    
    p1, _ = find_peaks(lnI, distance=d)
    p2, _ = find_peaks(1-lnI, distance=d)
    p =  [x for x in chain.from_iterable(zip_longest(p1, p2)) if x is not None]
    sep = int(np.mean(np.diff(p))/2)
    p = [x+sep for x in p[:-1]]
    
    edgeSlope= np.mean(gradAbs[p])
    nils = w*edgeSlope
    
    
    if show == True:
        plt.plot(x[p], lnI[p],'x')
        plt.plot(x, lnI, label='ln(I)')
        plt.plot(x,np.max(lnI)*I[:,0]/np.max(I),label='I (norm.)')
        plt.xlim([0.2,0.8])
        plt.legend()
        plt.show()
        print('w: {}'.format(w))
        print('Slope: {}'.format(edgeSlope))
        print('NILS: {}'.format(nils))
        
    return nils



def gratingContrastFourier(A,x, show=True):
    '''
    Fourier contrast:  amplitude of the  fundamental  frequency
    
    The estimation of contrast, using the measured magnitudes of the fundamental frequency and the DC, is correct in an ideal case.
    However, it is subject to deviations due to discretization and 'spectral leakage '
    
    A: signal, i.e. intensity
    ** Here A is assumed to be 1D
    x: list of positions corresponding to A
    
    is scaling by sqrt(2) needed for comparison to Michelsen contrast?
    
    
    THIS STILL NEEDS TO BE CHECKED  USE WITH CAUTION
    '''
       
    N = np.size(A)
    xstep = x[1]-x[0]
    
    '''
    #get the FFT of I
    Af = fft(A)
    
    # Amplitudes
    amplitudes = 2/N * np.abs(Af)
   
    # The corresponding spatial frequencies
    frequencies = fftfreq(N, d=xstep)
    
    # Find the peak frequency
    posMask = np.where(frequencies > 0) # consider only +ve
    fr =  frequencies[posMask]
    peakFrequency = fr[amplitudes[posMask].argmax()]

    if show is True:
#        plt.plot(x, A)
#        plt.title('Intensity')
#        plt.show()
#        
        #plt.semilogx(frequencies[:len(frequencies) // 2], amplitudes[:len(Af) // 2])
        plt.plot(frequencies[:len(frequencies) // 2], amplitudes[:len(Af) // 2])
        plt.title('Fourier Amplitudes')
        plt.show()
        
        
        plt.plot(frequencies[len(frequencies) // 2:len(frequencies) // 2 + 500], amplitudes[len(frequencies) // 2:len(frequencies) // 2 + 500])
        plt.title('Fourier Amplitudes (partial)')
        plt.show()

    #C = amplitudes[0] 
    
    C =  (1/(4*pi)) * 1/(xstep/1e-9) * 2/xstep * np.sqrt(2)/sqrt(square(abs(Af[0]))-np.sum(square(abs(Af[3:])))) / abs(Af[0])
    '''
    
    fs = 1/xstep   # number of samples per m    
    sfft =  fft(A)
    freqs = fftfreq(len(A)) * fs
    
    print('DEBUG: freqs ', np.shape(freqs))
    
    
    plt.stem(freqs, np.abs(sfft))
    #plt.plot(freqs, np.abs(sfft))#,linefmt=next(cycol),label=label)

    
    s = np.abs(sfft)[len(sfft)//2+1:][:,0]
    f = freqs[len(sfft)//2+1:]
    print('DEBUG: s ', np.shape(s))
    print('DEBUG: f ', np.shape(f))
    
    m = argrelextrema(np.abs(s), np.greater, order=4) #array of indexes of the  maxima

    print('DEBUG: m ', np.shape(m))

    y = [s[i-1] for i in m]
    x = [f[i-1] for i in m]
    
    print('DEBUG: y ', np.shape(y))
    print('DEBUG: x ', np.shape(x))
    plt.plot(x, y, 'x')
    
    #print('length y ', np.shape(y), ' length m ', np.shape(m))
    index_max = np.argmax(y)
    
    print('DEBUG: index_max ', index_max)
    #print(m)
    #print(y)
    
    #print('m: ', m[0])
    #print(m[0][index_max])
    
    
    ymax = s[m[0][index_max]]
    xmax = f[m[0][index_max]]
    
    #print('ymax ', ymax)
    plt.plot(xmax, ymax, 'o')
    plt.show()
    
    C = ymax/(np.sum(s)-ymax)
    
    
    print('Fourier Contrast: ', C)
    #return C, amplitudes, frequencies, peakFrequency
    return C, sfft, freqs, xmax


def integralOpticalDensity(I,bins=256):
    '''
    calculate the integral optical density of an image from
    the histogram, which reflects the global performance of an image
    
    Set bins to a value appropriate to numerical type of I (could be done automatically)
    
    Returns:
        IOD
        IODM: maximum IOD for an image with the same number of grey levels and pixel count
        H: histogram of intensity over  a number of grey levels equal to bins
    '''
    I = bins* (I-np.min(I))/ (np.max(I)-np.min(I))
    #H, intensityBin =  np.histogram(I, bins=bins-1)
    
    H, binEdges = np.histogram(I, bins=bins)
    binCenters = binEdges[:-1] + np.diff(binEdges)/2
    
    IOD=0
    for i in range(np.shape(H)[0]):
        IOD += H[i]*binCenters[i]
        
    IODM =  np.size(I)*(bins-1)/2

    return  IOD, IODM, H, binEdges[:-1],binCenters
    

def meanDynamicRange(I):
    '''
    Calculate mean dynamic range of intensity values I using method of Lai and Von 
    Bally.
    This may be used to estimate fringe visibility in a way that is less sensitive
    to noise and more appropriate simply using V = (Imax-IMin)/(Imax-Imin)
    
    
    C compositely represents the mean dynamic range and greyscale imbalance of an
    image. Only when Cl and C2 reach the maximum values simultaneously,
    does C obtain the maximum value.The variation of C is related not only to the 
    variation of the greylevel of pixels, but also to the amount of pixels whose 
    greylevel varies.
    Thus noises with either a relative low number or relative small intensity do 
    not result in great variance of the contrast of the image itself.
    '''
    
    I1 = np.ravel(I)  # reduce 2D to 1D
    IOD,IODM,H,binEdges,binCenters = integralOpticalDensity(I1)
    
    # find mean of histogram and index (bin) of mean
    meanH = IOD/np.sum(H)
    #index = list(map(lambda k: k < meanH, H)).index(True)
    index=int(meanH)  # check this carefully
    
    N= np.size(H)
    Id = sum([x * y for x, y in zip(binCenters[:index],H[:index])]) / sum(H[:index]+1e-10)
    Ib = sum([x * y for x, y in zip(binCenters[index:N],H[index:N])]) / sum(H[index:N]+1e-10)
    
    C1 = (Ib-Id)/(Ib+Id) # mean dynamic range (definition 1)
    
    
    if IOD<=IODM:
        C2 = IOD/IODM    # mean dynamic range (definition 2)
    else:
        C2 = 2 - IOD/IODM
        
    # Unfortunately,neither C1 or C2 is suficient for estimating contrast in all cases
    # Lai and Von Bally suggest the composite:
    C = C1*C2
        
    return C, C1, C2


def correlationCoefficient(A, expected):
    return np.corrcoef(A,expected)[1,0]


def fidelity(A, reference):
    """
    Calculate fidelity as measure of similarity of A to reference
    """
    a = np.sqrt((reference-A)**2)
    b = abs(reference+A)
    c = 1/(np.size(A))
    fidelity = 1-(np.sum(a)/np.sum(b))*c
    return fidelity


def interferenceIntensityTMTM(x,k,theta,A = 1.0):
    '''
    Generate intensity profile for interfernce between TM polarised beams from
    a pair of diffraction gratings.  Based on 
    
    X Wang et al, Proceedings Volume 10809, International Conference on Extreme Ultraviolet 
    Lithography 2018; 108091Z (2018) https://doi.org/10.1117/12.2501949
    
    For two TM polarized beams, the electric field is parallel to the incident plane 
    and can be decomposed in the x and z directions regarding incident angle. In this 
    case, assuming 0 initial phases, equal amplitudes A, with the azimuthal angles 
    ϕ1 = 0°, ϕ2 = 180° and polarization angles ψ1 = 0°, ψ2 = 0°, the electric fields 
    are:
  
      E1 = A*exp(i*(k*x*np.sin(theta) - k*x*cos(theta )))
      E2 = A*exp(i*(-k*x*np.sin(theta) - k*x*cos(theta )))

    The polarisation vectors are :

      p1 = cos(theta)*y*iv+sin(tehta)*z*kv
      p2 = cos(theta)*y*iv-sin(tehta)*z*kv

    where iv, jv, kv is unit vector in x direction (i,j,k notation)
    '''
    I = 2.*square(A) + 2.*square(A) * cos(2.*k*x*sin(theta))*cos(2.*theta)
   
    return I


def interferenceIntensityTETE(x,k,theta,A = 1.0):
    '''
    Generate intensity profile for interfernce between TE polarised beams from
    a pair of diffraction gratings.  Based on 
    
    X Wang et al, Proceedings Volume 10809, International Conference on Extreme Ultraviolet 
    Lithography 2018; 108091Z (2018) https://doi.org/10.1117/12.2501949
    
    '''
    I = 2.*square(A) + 2.*square(A) * cos(2.*k*x*sin(theta))
    
    return I
    
    
def interferenceIntensityTMTE(x,k,theta,gamma, A = 1.0):
    '''
    Generate intensity profile for interfernce between a TE and TM polarised beam from
    a pair of diffraction gratings.  Based on 
    
    X Wang et al, Proceedings Volume 10809, International Conference on Extreme Ultraviolet 
    Lithography 2018; 108091Z (2018) https://doi.org/10.1117/12.2501949
    
    Polarization may by controlled by rotating the grating by certain angle gamma
    (e.g., 45°) In this case, for two-beam interference, the two diffracted beams 
    will carry both TE and TM polarizations. 
    
    '''
    I = 2.*square(A)+square(cos(gamma))* \
        (2. + cos(2.*k*x*cos(gamma)*sin(theta)) * cos(2.*theta) + \
        2.*cos(2.*k*cos(gamma)*x*sin(theta)))
    
    return I
    
    
    
def interferenceIntensity(x,k,theta, A = 1.0, gamma=0, polarisationModes=('TM','TM')):

    if (polarisationModes[0] == 'TE' and polarisationModes[1] == 'TE'):
        I = interferenceIntensityTETE(x,k,theta,A)
         
    if (polarisationModes[0] == 'TM' and polarisationModes[1] == 'TM'):
        I = interferenceIntensityTMTM(x,k,theta,A)
    
    if ((polarisationModes[0] == 'TE' and polarisationModes[1] == 'TM') \
       or (polarisationModes[0] == 'TM' and polarisationModes[1] == 'TE')):
        I = interferenceIntensityTMTE(x,k,theta,gamma,A)    
    return I



def whiteNoise(rho, sr, n, mu=0):
    '''
    parameters: 
    rho - spectral noise density unit/SQRT(Hz)
    sr  - sample rate
    n   - no of points
    mu  - mean value, optional
    
    returns:
    n points of noise signal with spectral noise density of rho
    '''
    sigma = rho * np.sqrt(sr/2)
    noise = np.random.normal(mu, sigma, n)
    return noise


def test_models():
    
   
    ''' define interference grating parameters'''
    wl = 13.5e-9 # wavelength in m
    #wl = 6.7e-9  # wavelength in m

    # Amplitude of both beams (assumed equal)
    A = 1.0  # this may be scaled to  match simulated intensity
    
    k = 2*np.pi/wl
    
    m = 1 # order of diffracted beams from each grating
    d = 20.e-9 # grating spacing
    
    # angle between the beams from each grating
    theta = np.arcsin( m *wl/d)
    
    #define x positions:
    dx=0.5e-9
    #number of points:
    n = 2000
    # grid:
    x =  np.linspace(-dx*int(n/2),dx*int(n/2),n) 
    
    cl=[]
    pl = np.linspace(20e-9, 200e-9, 10)
    plt.title('13.5 nm')
    for p in pl: 
        t=np.arcsin( m *wl/p)
        I = interferenceIntensity(x,k,t,A=A, polarisationModes=('TM','TM'))
        c = gratingContrastMichelson(I)
        cl.append(c)
        plt.plot(x*1e6, I, label='TM-TM, pitch = {:.0f} nm, contrast = {:.2f}'.format(p/1e-9, c))
        plt.legend()
    plt.show
    

    ''' plot dependence on grating pitch for TM-TM   (close-up)  '''
    
    plt.title('13.5 nm')
    for p in np.linspace(10e-9, 200e-9, 11):
        t=np.arcsin( m *wl/p)
        I = interferenceIntensity(x,k,t,A=A, polarisationModes=('TM','TM'))
        c = gratingContrastMichelson(I)
        plt.plot(x*1e6, I, label='TM-TM, pitch = {:.0f} nm, contrast = {:.2f}'.format(p/1e-9, c))
        plt.xlim(-0.05,0.05)
        plt.legend()
    plt.show
    
    
    ''' plot dependence on grating pitch for TM-TM   (close-up)  '''
    
    plt.title('13.5 nm RMS')
    for p in np.linspace(10e-9, 200e-9, 11):
        t=np.arcsin( m *wl/p)
        I = interferenceIntensity(x,k,t,A=A, polarisationModes=('TM','TM'))
        c = gratingContrastRMS(I)
        plt.plot(x*1e6, I, label='TM-TM, pitch = {:.0f} nm, contrast = {:.2f}'.format(p/1e-9, c))
        plt.xlim(-0.05,0.05)
        plt.legend()
    plt.show
    
    
    ''' plot dependence on grating pitch for TE-TE '''
    
    plt.title('13.5 nm')
    for p in np.linspace(20e-9, 200e-9, 10):
        t=np.arcsin( m *wl/p)
        I = interferenceIntensity(x,k,t,A=A, polarisationModes=('TE','TE'))
        c = gratingContrastMichelson(I)
        plt.plot(x*1e6, I, label='TE-TE, pitch = {:.0f} nm, contrast = {:.2f}'.format(p/1e-9, c))
        plt.xlim(-0.05,0.05)
        plt.legend()
    plt.show
    
    ''' plot dependence on grating pitch for TE-TE '''
    
    plt.title('13.5 nm RMS')
    for p in np.linspace(20e-9, 200e-9, 10):
        t=np.arcsin( m *wl/p)
        I = interferenceIntensity(x,k,t,A=A, polarisationModes=('TE','TE'))
        c = gratingContrastRMS(I)
        plt.plot(x*1e6, I, label='TE-TE, pitch = {:.0f} nm, contrast = {:.2f}'.format(p/1e-9, c))
        plt.xlim(-0.05,0.05)
        plt.legend()
    plt.show
    
    
    
    
    
    ''' Compare RMS and Fourier contrast vs grating pitch '''
    
    #define x positions:
    dx=1e-9
    #number of points:
    n = int(10e-6/dx)
    # grid:
    x =  np.linspace(-dx*int(n/2),dx*int(n/2),n) 
    
    fig, ax1 = plt.subplots()
    plt.title('TM-TM [10000 x 1 nm pixels]')
    ax2 = ax1.twinx()
  
    ax1.set_xlabel('Grating pitch (nm)')
    ax1.set_ylabel('RMS contrast, Michelson Contrast')
    ax2.set_ylabel('Fourier Contrast', color='b')

    cml=[]
    crl=[]
    fl = []
    pl = np.linspace(20e-9, 200e-9, 400)
    for p in pl: 
        t=np.arcsin( m *wl/p)
        I = interferenceIntensity(x,k,t,A=A, polarisationModes=('TM','TM'))
        
        ''' generate noise '''
        rho=1e-2
        sr = n  # (as period = n/sr)
        noise = whiteNoise(rho, sr, n, mu=0)
        I = I - noise
        
        
        cr = gratingContrastRMS(I)
        cm = gratingContrastMichelson(I)
        
        f, amplitudes, frequencies, peakFrequency = gratingContrastFourier(I,x, show=False)
        crl.append(cr)
        cml.append(cm)
        fl.append(f)
        
    ax1.plot(pl/1e-9, crl, 'g-', label='RMS')
    ax1.plot(pl/1e-9, cml, 'r-',  label='Michelson')
    ax2.plot(pl/1e-9, fl,  'b-', label='Fourier')
    ax1.set_ylim([0,1.2])
    ax1.set_ylim([0,1.2])
    plt.legend()

    plt.show()
    
    #########
    

    ''' Compare RMS and Fourier contrast vs noise '''
    
    #define x positions:
    dx=1e-9
    #number of points:
    n = int(10e-6/dx)
    # grid:
    x =  np.linspace(-dx*int(n/2),dx*int(n/2),n) 
    
    
    plt.title('TM-TM [10000 x 1 nm pixels]')
   
  
    plt.xlabel('rho (proportional to noise)')
    plt.ylabel('contrast')
    

    cml=[]
    crl=[]
    fl = []
    nl=[]
    Il=[]
    Imean = []
    p = 40e-9
    rho = np.linspace(0,4e-3,100)
    t=np.arcsin( m *wl/p)
    I0 = interferenceIntensity(x,k,t,A=A, polarisationModes=('TM','TM'))
    sr = n  # (as period = n/sr)


    for r in rho:
        noise = whiteNoise(r, sr, n, mu=0)
        nl.append(noise)
        I = I0 - np.mean(noise) + noise
        Imean.append(np.mean(I))
        Il.append(I)
        
        
        cr = gratingContrastRMS(I)
        cm = gratingContrastMichelson(I)
        
        f, amplitudes, frequencies, peakFrequency = gratingContrastFourier(I,x, show=False)
        crl.append(cr)
        cml.append(cm)
        fl.append(f)
        
    plt.plot(rho, crl, 'g-', label='RMS')
    plt.plot(rho, cml, 'r-',  label='Michelson')
    plt.plot(rho, fl,  'b-', label='Fourier')
    plt.legend()

    plt.show()
    
    
    #check that mean doesn't change
    plt.plot(rho, Imean)
    plt.show()
    
    
    # compare distributions:
    
    for noise in nl[::5][1:]:
        plt.hist(noise, bins=50, histtype='step')
    plt.gca().set(title='Noise Frequency Histogram', ylabel='Frequency');
    plt.show()
    
    for In in Il[::5][1:]:
        plt.hist(In, bins=50, histtype='step')
    plt.hist(I0, bins=50)    
    plt.gca().set(title='Intensity Frequency Histogram ', ylabel='Frequency');
    plt.show()
    
    
    #########
    
    
     #define x positions:
    dx=0.1e-9
    #number of points:
    n = 2000
    # grid:
    x =  np.linspace(-dx*int(n/2),dx*int(n/2),n) 
    
        # angle between the beams from each grating
    theta = np.arcsin( m *wl/d)
    
    
    ITMTM = interferenceIntensity(x,k,theta,A=A, polarisationModes=('TM','TM'))
    ITETE = interferenceIntensity(x,k,theta,A=A, polarisationModes=('TE','TE'))
   
    plt.title('13.5 nm, 40 nm pitch')
    plt.plot(x*1e6,ITETE, label='TE-TE, contrast = {:.2f}'.format(gratingContrastMichelson(ITETE)))
    plt.plot(x*1e6,ITMTM, label='TM-TM, contrast = {:.2f}'.format(gratingContrastMichelson(ITMTM)))

    for gamma in [np.pi/4]:  #np.linspace(0, np.pi/8, 2*np.pi):
        ''' generate interference intensity'''
        ITMTE = interferenceIntensity(x,k,theta, gamma=gamma, A=A, polarisationModes=('TM','TE'))

        
    #    ''' plot TM-TM intensity'''
    #    plt.plot(x*1e6,ITMTM, label='TM-TM')
    #    plt.xlabel('Position [um]')
    #    plt.ylabel('Intensity [a.u.]')
    #    plt.legend()
    #    plt.rcParams["figure.figsize"] = [7,4]
    #    plt.show()
    #    
    #    ''' plot TE-TE intensity'''
    #    plt.plot(x*1e6,ITETE, label='TE-TE')
    #    plt.xlabel('Position [um]')
    #    plt.ylabel('Intensity [a.u.]')
    #    plt.legend()
    #    plt.rcParams["figure.figsize"] = [7,4]
    #    plt.show()
    #
    #    ''' plot TM-TE intensity'''
    #    plt.plot(x*1e6,ITMTE, label='TM-TE')
    #    plt.xlabel('Position [um]')
    #    plt.ylabel('Intensity [a.u.]')
    #    plt.legend()
    #    plt.rcParams["figure.figsize"] = [7,4]
    #    plt.show()
        
        ''' plot all '''
        plt.plot(x*1e6,ITMTE, label='TM-TE, contrast = {:.2f}'.format(gratingContrastMichelson(ITMTE)))
        
    plt.xlabel('Position [um]')
    plt.ylabel('Intensity [a.u.]')
    plt.legend()
    plt.rcParams["figure.figsize"] = [7,4]
    plt.show()
    
    
    
    
    ''' Messing around with sums '''
    

    ## interpret with caution!! Summation should be done as coherent sum of E
    ITETE = interferenceIntensity(x,k,theta, A=A, polarisationModes=('TE','TE'))
    
    ITMTE = interferenceIntensity(x,k,theta, gamma=np.pi/8, A=A, polarisationModes=('TM','TE'))
    I = ITETE+ITMTE
    c=gratingContrastRMS(I)
    plt.plot(I,  label='TM-TE + TETE, gamma = pi/8, contrast = {:.2f}'.format(c))
    
    ITMTE = interferenceIntensity(x,k,theta, gamma=np.pi/6, A=A, polarisationModes=('TM','TE'))
    I = ITETE+ITMTE
    c=gratingContrastRMS(I)
    plt.plot(I, label='TM-TE + TETE, gamma = pi/6, contrast = {:.2f}'.format(c))
    
    ITMTE = interferenceIntensity(x,k,theta, gamma=np.pi/4, A=A, polarisationModes=('TM','TE'))
    I = ITETE+ITMTE
    c=gratingContrastRMS(I)
    plt.plot(I, label='TM-TE + TETE, gamma = pi/4, contrast = {:.2f}'.format(c))
    plt.legend()
    plt.show()
    
    

def test():
    
    ''' load a saved intensity profile. We will use some properties of this profile
    for simulations. '''
    profile = np.load('profile01.npy')
    profileN = np.size(profile)
    profileXs = 1.0e-8 # pixel scaling factor/
    profileX = np.linspace(-0.5*profileN*profileXs, 0.5*profileN*profileXs,profileN)
 
    ''' define interference grating parameters'''
    wl = 6.7e-9 # wavelength in m

    # Amplitude of both beams (assumed equal)
    A = 0.8e5  # this may be scaled to  match simulated intensity
    
    k = 2*np.pi/wl
    
    m = 1 # order of diffracted beams from each grating
    d = 200e-9 # grating spacing
    
    # angle between the beams from each grating
    theta = np.arcsin( m *wl/d)
    
    #define x positions:
    xstep=profileXs
    n = profileN
    x =  np.linspace(-xstep*int(n/2),xstep*int(n/2),n)  #np.linspace(-90e-9,90e-9,10000)
    
    # noise parameters
    rho=4*1/xstep
    ''' generate interference intensity'''
    I = interferenceIntensity(x,k,theta,A=A)
    
    ''' generate noise '''
    sr = n  # (as period = n/sr)
    noise = whiteNoise(rho, sr, n, mu=0)
    Inoisy = I + noise

    ''' plot intensity with and without noise, together with saved profile'''
    plt.plot(x*1e6,Inoisy,label='Model amplitude + noise')
    plt.plot(x*1e6,I, label='Model amplitude')
    plt.plot(profileX*1e6, profile,label='Simulated profile')
    plt.xlabel('Position [um]')
    plt.ylabel('Intensity [a.u.]')
    plt.legend()
    plt.rcParams["figure.figsize"] = [7,4]
    plt.show()

    f=[]      # initialise frequency list
    psd=[]    # initialise PSD list
    MSD = []  # initialise mean spectral density list
    signals = [I,Inoisy, profile]
    labels = ['Model TM-TM','Model + noise', 'Simulated']
    for s in signals:
        F, PSD = periodogram(s,sr)
        f.append(F)
        psd.append(PSD)
     
    from itertools import cycle
    cycol = cycle('bgrcmk')
    
    from scipy.signal import argrelextrema
    
    ''' plot frequency spectrum '''
    for signal,label in zip(signals,labels): 
        fs = 1/xstep   # number of samples per m    
        sfft =  fft(signal)
        freqs = fftfreq(len(signal)) * fs
        #plt.stem(freqs, np.abs(sfft),linefmt=next(cycol),label=label)
        plt.plot(freqs, np.abs(sfft))#,linefmt=next(cycol),label=label)

        
        s = np.abs(sfft)[len(sfft)//2+1:]
        f = freqs[len(sfft)//2+1:]
        m = argrelextrema(np.abs(s), np.greater, order=4) #array of indexes of the  maxima


        y = [s[i-1] for i in m]
        x = [f[i-1] for i in m]
        plt.plot(x, y, 'x')
        
        #print('length y ', np.shape(y), ' length m ', np.shape(m))
        index_max = np.argmax(y)
        
        #print('index_max ', index_max)
        #print(m)
        #print(y)
        
        #print('m: ', m[0])
        #print(m[0][index_max])
        
        
        ymax = s[m[0][index_max]]
        xmax = f[m[0][index_max]]
        
        #print('ymax ', ymax)
        plt.plot(xmax, ymax, 'o')
        
        R = ymax/(np.sum(s)-ymax)
        print('R: ', R)
        
    
    plt.xlabel('Spatial Frequency [1/m]')
    plt.ylabel('Frequency Domain (Spectrum) Magnitude')
    plt.legend()
    #plt.xlim(-1.2e7, 0.1e7)
    plt.xlim(-fs / 2, fs / 2)
    plt.show()
    
        
 
   

#    m = argrelextrema(np.abs(sfft), np.greater) #array of indexes of the  maxima
#    y = [freqs[i] for i in m]
#    plt.plot(m, y, 'rs')
#    plt.show()
#        
#        
    
    
    
        
    ''' plot PSD '''    
    cutoffIndex=1 #?????????
    for _psd, _f, _label in zip(psd,f,labels):
        #plt.semilogy(_f[1:], np.sqrt(_psd[1:]),label=_label)
        plt.semilogx(_f[1:], np.sqrt(_psd[1:]),label=_label,alpha=0.7)
    plt.xlabel("Spatial Frequency (1/nm)")
    plt.ylabel("PSD (arb.u./SQRT(nm))")
    plt.axhline(rho, ls="dashed", color="r",label='rho')
    plt.rcParams["figure.figsize"] = [4,2]
    plt.legend()
    plt.show()

    
    histogramI=[]
    histogramBins=[]
    for _psd, signal,label in zip(psd, signals,labels): 
        
        IOD, IODM, H, binEdges, binCenters = integralOpticalDensity(signal)
        histogramI.append(H)
        histogramBins.append(binEdges)
        C, C1, C2 = meanDynamicRange(signal)
        Cf,  Am, Fr, peakFr  = gratingContrastFourier(signal,x, show=False)
        Cm = gratingContrastMichelson(signal)
        fidel = fidelity(signal,signals[0])   # fidelity based on comparison to model
        

        print('**********',label,'***********')
        print('IOD: {}'.format(IOD))
        print('IOD max: {}'.format(IODM))
        print('Mean dynamic range (C): {}.  [C1 = {}, C2 = {}]'.format(C,C1,C2))
        print("Mean spectral noise density = ",np.sqrt(np.mean(_psd[cutoffIndex:])), "arb.u/SQRT(1/nm)")
        print('Michelson contrast: {}'.format(Cm))
        print ('Fourier contrast: {}'.format(Cf)) 
        print ('Fundamental frequency: {}'.format(peakFr))
        print('Period: {}- need to check)'.format(1/peakFr))
        print('Fidelity (1D): {}\n'.format(fidel))
        
       
    ''' plot histogram '''
    for h, e, label in zip(histogramI,histogramBins,labels):
        plt.bar(e,h,label=label)
        plt.ylabel('Frequency')
        plt.xlabel('Scaled Intensity')
        plt.legend()
        plt.show


if __name__ == "__main__":

    #test()
    test_models()