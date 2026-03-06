#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 29 14:26:17 2025

@author: -
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.special import factorial

import matplotlib.ticker as ticker
import scipy
from scipy import signal
import FWarbValue
from math import log10, floor

def round_sig(x, sig=2):
    from math import log10, floor
    if x != 0:
        return round(x, sig-int(floor(log10(abs(x))))-1)
    else:
        return x

# Gaussian function
def gaussian(x, A, x0, sigma, offset):
    return A * np.exp(-((x - x0) ** 2) / (2 * sigma ** 2)) + offset

# Lorentzian (Cauchy) function
def lorentzian(x, A, x0, gamma, offset):
    return A * (gamma**2 / ((x - x0)**2 + gamma**2)) + offset

# Poisson-like continuous approximation
def poisson_cont(x, A, mu, offset):
    # Poisson PMF over continuous x, using interpolation trick
    return A * (mu**x * np.exp(-mu) / factorial(x)) + offset

# General fitting function
def fit_profile_sides(x, y, exclude_width=0, fit_type='gaussian'):
    """
    Fit a 1D profile to Gaussian, Lorentzian, or Poisson distribution, excluding a center region.

    Parameters:
        x (np.ndarray): x-data
        y (np.ndarray): y-data
        exclude_width (float): width of central region to exclude (centered at peak)
        fit_type (str): 'gaussian', 'lorentzian', or 'poisson'

    Returns:
        popt (tuple): best-fit parameters
        pcov (2D array): covariance matrix
    """
    peak_idx = len(y)//2 #np.argmax(y)
    x0_est = x[peak_idx]

    mask = (x < x0_est - exclude_width / 2) | (x > x0_est + exclude_width / 2)
    x_fit = x[mask]
    y_fit = y[mask]

    A_guess = np.max(y)*1.4# np.max(y_fit) - np.min(y_fit)
    offset_guess = np.min(y_fit)
    print('Guess for ', fit_type, ' fit')
    print("Amp:     ", A_guess)
    print("Offset:  ", offset_guess)

    if fit_type == 'gaussian':
        sigma_guess = (np.max(x_fit) - np.min(x_fit)) / 6
        print("sigma:  ", sigma_guess)
        p0 = [A_guess, x0_est, sigma_guess, offset_guess]
        func = gaussian
    elif fit_type == 'lorentzian':
        gamma_guess = (np.max(x_fit) - np.min(x_fit)) * 0.027
        print("Gamma:  ", gamma_guess)
        p0 = [A_guess, x0_est, gamma_guess, offset_guess]
        func = lorentzian
    elif fit_type == 'poisson':
        mu_guess = x0_est
        print("Mu:  ", mu_guess)
        p0 = [A_guess, mu_guess, offset_guess]
        func = poisson_cont
        # Avoid negative x values for Poisson
        mask &= x >= 0
        x_fit = x[mask]
        y_fit = y[mask]
    else:
        raise ValueError("fit_type must be 'gaussian', 'lorentzian', or 'poisson'")

    try:
        print('p0: ', p0)
        B = [[A_guess*0.5, x0_est*1.5, gamma_guess*0.5, offset_guess - 1e-6],[A_guess*1.5, x0_est*0.5, gamma_guess*1.5, offset_guess + 1e-6]]
        print(B)
        popt, pcov = curve_fit(
            func, x_fit, y_fit, p0=p0, bounds=B
            # sigma=None, absolute_sigma=False,# if y_err_fit is not None else False,
            # maxfev=10000
        )
        A, x0, gamma, offset = popt
        perr = np.sqrt(np.diag(pcov))
        A_err, x0_err, gamma_err, offset_err = perr

        # Full width at 1/10 maximum: FW10M = 2 * gamma * sqrt(9) = 6 * gamma
        fw10m = 6 * gamma
        fw10m_err = 6 * gamma_err

        # Area under Lorentzian (infinite) = A * À
        # Area under FW10M range (between x0 - 3³ and x0 + 3³):
        # A_FW10M = +_{x0-3³}^{x0+3³} A * (³² / ((x - x0)² + ³²)) dx = A * ³ * arctangent term
        area_fw10m = A * gamma * (2 * np.arctan(3))
        # Partial derivatives for error propagation
        dA = gamma * (2 * np.arctan(3))
        dG = A * (2 * np.arctan(3))
        area_err = np.sqrt((dA * A_err)**2 + (dG * gamma_err)**2)

        plt.plot(x, lorentzian(x, *p0), label='Initial guess', linestyle='--')
        return {
            "params": {"A": A, "x0": x0, "gamma": gamma, "offset": offset},
            "errors": {"A": A_err, "x0": x0_err, "gamma": gamma_err, "offset": offset_err},
            "FW10M": fw10m,
            "FW10M_err": fw10m_err,
            "area_FW10M": area_fw10m,
            "area_FW10M_err": area_err,
            "popt": popt,
            "pcov": pcov
        }
    except RuntimeError as e:
        print("Fit failed:", e)
        return None, None

    
def analyse_scatter(intensityFile,I_threshold,G_size,frac,det_distance,wl,log=1,fitGauss=0,savgol=80,suppress_peak=165,sumtype='edges',getPSD=False,show=False):
    
    
    nx = str(np.loadtxt(intensityFile, dtype=str, comments=None, skiprows=6, max_rows=1, usecols=(0)))[1:]#[1:3]
    ny = str(np.loadtxt(intensityFile, dtype=str, comments=None, skiprows=9, max_rows=1, usecols=(0)))[1:]#[1:3]
    xMin = str(np.loadtxt(intensityFile, dtype=str, comments=None, skiprows=4, max_rows=1, usecols=(0)))[1:]#[1:3]
    xMax = str(np.loadtxt(intensityFile, dtype=str, comments=None, skiprows=5, max_rows=1, usecols=(0)))[1:]#[1:3]
    rx = float(xMax)-float(xMin)
    dx = np.divide(rx,float(nx))
    yMin = str(np.loadtxt(intensityFile, dtype=str, comments=None, skiprows=7, max_rows=1, usecols=(0)))[1:]#[1:3]
    yMax = str(np.loadtxt(intensityFile, dtype=str, comments=None, skiprows=8, max_rows=1, usecols=(0)))[1:]#[1:3]
    ry = float(yMax)-float(yMin)
    dy = np.divide(ry,float(ny))
    numC = 1 #int(str(np.loadtxt(intensityFile, dtype=str, comments=None, skiprows=10, max_rows=1, usecols=(0)))[1:])#[1:3]
    print("Resolution (x,y): {}".format((nx,ny)))
    print("xRange: {}".format(rx))
    print("xMax: {}".format(xMax))
    print("xMin: {}".format(xMin))
    print("yRange: {}".format(ry))
    print("yMax: {}".format(yMax))
    print("yMin: {}".format(yMin))
    print("Dx, Dy : {}".format((dx,dy)))
    ny = int(ny)

    I = np.reshape(np.loadtxt(intensityFile,skiprows=10), (numC,int(ny),int(nx)))
    I = I[0,:,:]
    
    # # converting from ph/s/mm^2 to ph/s
    # I = (I / 1.0e-6) * (dx*dy)
    
    I = np.where(I < I_threshold, 1, I)
    # I = tifffile.imread(intensityFile)
    
    if getPSD:
        # Getting PSD of far-field intesity distribution (along y direction)
        P,F = [],[]
        for n,y in enumerate(I.T):
            L = len(y)*dy
            fmin = 1 / (2*np.pi*L)
            smax =  1 / fmin
            
            X = np.linspace(-L/2,L/2,num=len(y),endpoint=True)
            
            if n == 0:
                print('\n')
                print('Shape of y:                   ', np.shape(y))
                print('Length of sampled area:       ', L*1e3, ' mm')
                print("minimum frequency sampled:    ", fmin/1e6, ' /um')
                print("maximum feature size sampled: ", smax*1e6, ' um')
                # plt.plot(X,y)
                # plt.show()
            
            f,p = signal.periodogram(y,1/dx)
            
            P.append(p)
            F.append(f)
        
        
        # print(np.shape(F))
        f=np.mean(F,axis=0)
        p=np.mean(P,axis=0)
        # print(np.shape(F))
        
        if show:
            plt.plot([_f/1.0e-9 for _f in f[1::]], p[1::],'.')#, label='biased',alpha=0.2)
            ax = plt.gca()
            ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%0.0e'))
            plt.yscale('log')
            plt.xscale('log')
            plt.xlabel('Spatial frequency (nm$^{-1}$)')
            plt.ylabel('Fourier power (au)')
            plt.title('Fourier power spectrum')
            plt.legend()
            plt.show()
            
        Iy0 = I[:,int(nx)//2]
        ky = pixel_to_reciprocal(int(ny), dy, wl, det_distance)
        ky = ky[Iy0 >= 10]
        Iy0 = Iy0[Iy0 >= 10]
            
        if show:
                plt.plot([k/1e-9 for k in ky],Iy0,'x')
                plt.title('PSD of grating LWR')
                plt.xlabel('spatial frequency [/m]')
                plt.ylabel('power')
                plt.xscale('log')
                plt.yscale('log')
                plt.show()
        
        if suppress_peak:
            N = suppress_peak//2
            plt.plot(Iy0, label='x=0 (before peak suppression)')
            Iy0[ny//2-N:ny//2+N] = 0 #Iy0[ny//2-(N+1)]
            plt.plot(Iy0, label='x=0 (after peak suppression)')
            plt.legend()
            plt.show()

    
    # # Smoothing I with Gaussian the size of speckles
    # # I = gaussian_filter(I)
    if G_size:
        if show:
            fig, ax = plt.subplots(1,2)
            ax[0].imshow(np.log(I))
            ax[0].set_title('raw (log)')
            
            I = scipy.ndimage.gaussian_filter(I, sigma=G_size/6, mode='reflect')
            
            ax[1].imshow(np.log(I))
            ax[1].set_title('Gaussian filtered (log)')
            plt.show()
        else:
            I = scipy.ndimage.gaussian_filter(I, sigma=G_size/6, mode='reflect')
        
    
    # Getting average y-profile of smoothed I
    if sumtype == 'edge':
        Iy1_l = np.log(np.mean(I[:,0:1500],axis=1))
        Iy2_l = np.log(np.mean(I[:,-1500::],axis=1))
        Iy_l = (Iy1_l + Iy2_l) / 2
        Iy1 = np.mean(I[:,0:1000],axis=1)
        Iy2 = np.mean(I[:,-1000::],axis=1)
        Iy = (Iy1 + Iy2) / 2
    elif sumtype == 'all':
        Iy_l = np.log(np.mean(I,axis=1))
        Iy = np.mean(I,axis=1)
        Iys = np.sum(I,axis=1)
        
        
    # removing central diffraction peak
    if suppress_peak:
        N = suppress_peak
        if show:
            plt.plot(Iy_l,label='before peak suppression (log)')
            plt.plot(Iy/np.max(Iy) * np.max(Iy_l),label='before peak suppression')
            Iy_l[ny//2-N:ny//2+N] = Iy_l[ny//2-(N+1)]
            Iy[ny//2-N:ny//2+N] = Iy[ny//2-(N+1)]
            Iys[ny//2-N:ny//2+N] = Iys[ny//2-(N+1)]
            plt.plot(Iy_l,label='after peak suppression (log)')
            plt.plot(Iy/np.max(Iy) * np.max(Iy_l),label='after peak suppression')
            plt.legend()
            plt.show()
        else:
            Iy_l[ny//2-N:ny//2+N] = Iy_l[ny//2-(N+1)]
            Iy[ny//2-N:ny//2+N] = Iy[ny//2-(N+1)]
            Iys[ny//2-N:ny//2+N] = Iys[ny//2-(N+1)]
        
        # if PSD:
        #     Iy0 = I[:,int(nx)//2]
        #     ky = pixel_to_reciprocal(int(ny), dy, wl, det_distance)
        #     ky = ky[Iy0 >= 10]
        #     Iy0 = Iy0[Iy0 >= 10]
        #     if show:
        #         plt.plot([k/1e-9 for k in ky],Iy0,'x')
        #         plt.title('PSD of grating LWR')
        #         plt.xlabel('spatial frequency [/m]')
        #         plt.ylabel('power')
        #         plt.xscale('log')
        #         plt.yscale('log')
        #         plt.show()
            
    
    # Removing background
    Iy_l = Iy_l - np.min(Iy_l)
    Iy_l = Iy_l - Iy_l[400]
    Iy_l= np.where(Iy_l < 0, 0, Iy_l)
    
    Iy = Iy - np.min(Iy)
    Iy = Iy - Iy[400]
    Iy= np.where(Iy < 0, 0, Iy)
    
    Iys = Iys - np.min(Iys)
    Iys = Iys - Iys[400]
    Iys= np.where(Iys < 0, 0, Iys)
    
    
    if fitGauss:
        # from multiGaussFit import fitMultiGauss
        # if log:
        #     amp = np.max(Iy)* 0.8
        #     mu = len(Iy)//2
        #     sigma = mu/3
        # else:
        #     amp = 1.5*np.max(Iy)
        #     mu = len(Iy)//2 - 100
        #     sigma = mu/14
        
        # amp,mu,sigma = fitMultiGauss(Iy, dx=dy, N=1, iG=[amp,mu,sigma], known=[0,0,0], no_center=suppress_peak)
        
        # Iy = FWarbValue.gauss(X,amp,0,sigma*dy,plot=False)
        
        x = np.linspace(float(yMin),float(yMax),int(ny))
        # Fit using different models
        # popt_g, _ = fit_profile_sides(x, Iys, exclude_width=suppress_peak*dy, fit_type='gaussian')
        popt_l = fit_profile_sides(x, Iys, exclude_width=suppress_peak*dy, fit_type='lorentzian')
        # popt_p, _ = fit_profile_sides(x, Iys, exclude_width=suppress_peak*dy, fit_type='poisson')
        
        print(popt_l)
        
        _IW = popt_l['FW10M']#['FW10M']
        _F = popt_l['area_FW10M']
        _IW_e = popt_l['FW10M_err']
        _F_e = popt_l['area_FW10M_err']
        popt_l = popt_l['popt']
        
        # Plotting
        plt.plot(x, Iys, label='Data', color='black')
        # if popt_g is not None:
        #     plt.plot(x, gaussian(x, *popt_g), label='Gaussian Fit', linestyle='--')
        if popt_l is not None:
            plt.plot(x, lorentzian(x, *popt_l), label='Lorentzian Fit', linestyle='--')
        # if popt_p is not None:
        #     plt.plot(x, poisson_cont(x, *popt_p), label='Poisson Fit', linestyle='--')
        plt.legend()
        plt.show()
        Iys = lorentzian(x, *popt_l)
        Iy_l = np.log(Iys)
    
    if savgol:
        from scipy.signal import savgol_filter
        if show:
            plt.plot(X,Iy_l,label='before savgol')
            Iy_l = savgol_filter(Iy_l,window_length=len(Iy)-1,polyorder=savgol)
            plt.plot(X,Iy_l,label='after savgol, order: ' + str(savgol))
            plt.legend()
            plt.show()
        else:
            Iy_l = savgol_filter(Iy_l,window_length=len(Iy)-1,polyorder=savgol)
            
    # #Getting width of central intensity envelope at 1/e value
    # # IW = FWarbValue(Iy,1/e)
    if show:
        X = x
        print('Iy_l max:', np.max(Iy_l))
        plt.plot(X,Iy_l, label='log')
        plt.plot(X,Iys/np.max(Iys) * np.max(Iy_l), label='linear (normalised)')
        # # IW = FWarbValue.getFWatValue(I, dx, dy, averaging=5000, frac=1/_e, cuts='y')
        # IW = len(Iy_l[Iy_l>(Iy_l.max()*frac)])*dy
        IW = len(Iys[Iys>(Iys.max()*frac)])*dy
        #Getting total flux in scattered envelope
        # Iys = Iys[Iy_l>(Iy_l.max()*frac)]
        Iys = Iys[Iys>(Iys.max()*frac)]
        Iys = (Iys / 1.0e-6) * (dx*dy)
        F = np.sum(Iys)
        
        plt.text(0.0002, np.max(Iy_l), "FW@1/e : " + str(IW*1e3) + " mm")
        plt.vlines([-IW/2,IW/2],ymin=np.min(Iy_l),ymax=np.max(Iy_l),colors='r',linestyles=':')
        plt.legend()
        plt.show()
    else:
        IW = len(Iy_l[Iy_l>(Iy_l.max()*frac)])*dy
        #Getting total flux in scattered envelope
        Iys = Iys[Iy_l>(Iy_l.max()*frac)]
        Iys = (Iys / 1.0e-6) * (dx*dy)
        F = np.sum(Iys)
        
    
    print("Full width @ 1/e max:    ", IW*1e3, " mm")
    print("Flux in full width @ 1/e max:    ", F)
    
    return _IW, _F, _IW_e, _F_e

def pixel_to_reciprocal(n_pixels, pixel_size, wavelength, detector_distance):
    """
    Convert pixel positions to reciprocal space coordinates.

    Parameters:
        n_pixels (int): Number of pixels along one dimension.
        pixel_size (float): Physical size of one pixel (e.g., in meters).
        wavelength (float): Wavelength of the incident light (in meters).
        detector_distance (float): Distance from the sample to the detector (in meters).

    Returns:
        k (1D np.ndarray): Reciprocal space coordinate array (in rad/m).
    """
    # Determine the pixel indices relative to the center of the detector.
    indices = np.arange(n_pixels)
    center = n_pixels // 2
    x_det = (indices - center) * pixel_size  # physical displacement
    # Use small-angle approximation to convert to angle theta and then to reciprocal space k.
    theta = x_det / detector_distance
    # k = (2 * np.pi / wavelength) * theta
    k = (theta / wavelength)
    # print('k:', k)
    return k

def testSingle():
    import os
    # maskFile = ''
    dirPath ='/user/home/opt/xl/xl/experiments/CDSAXS2/data/'  #'/user/home/opt/xl/xl/experiments/fullbeamPolarisation/'#'/user/home/opt/xl/xl/experiments/beamCoherence2/data/' 
    
    Ifile = 'res_int_pr_me.dat'
    # 'IntensityDist.dat'

    Z = 8.0e-3
    WL = 6.7e-9

    c = [50]
    r = [300]
    C = [1.0359985777488058e-07]    
    R = [3.748497232782469e-09]
    name = [str(_r) + 'um_' + str(_c) + '/' for _r,_c in zip(r,c)]
    order = name
    intensityFiles = [dirPath + o + Ifile for o in order]
    
    I_threshold = 1
    G_size = 0
    _e = 2.71828
    frac = 1/10 #1/_e
    log = 0
    fitGauss = 1
    savgol = 0
    suppress_peak = 165 # 500#165
    
    FW,FLUX = [],[]
    FWe,FLUXe = [],[]
    
    
    for e,i in enumerate(intensityFiles):
        print('\n Analysing file ', str(e+1), ' out of ', str(len(intensityFiles)))
        w, f, we, fe = analyse_scatter(i, I_threshold, G_size, frac, det_distance=Z, wl=WL,
                                       log=log,fitGauss=fitGauss,savgol=savgol,suppress_peak=suppress_peak,
                                       getPSD=False, show=True, sumtype='all')
        
        FW.append(w)
        FLUX.append(f)
        FWe.append(we)
        FLUXe.append(fe)

    plt.errorbar(c,FW,yerr=FWe,fmt=':x')
    plt.xlabel('amp')
    plt.ylabel('FW')
    plt.show()
    
    plt.errorbar(r,FLUX,yerr=FLUXe,fmt=':x')
    plt.xlabel('clen')
    plt.ylabel('FLUX')
    plt.show()
    
def test():
    import os
    # maskFile = ''
    dirPath ='/user/home/opt/xl/xl/experiments/CDSAXS2/data/'  #'/user/home/opt/xl/xl/experiments/fullbeamPolarisation/'#'/user/home/opt/xl/xl/experiments/beamCoherence2/data/' 

    C = [10,30,40,50]#[10,20,30,40,50]
    R = [30,300,500]#[30,40,50,60,70,80,100,150,200,250,300,350,400,450,500]
    
    Z = 8.0e-3
    WL = 6.7e-9
    
    Ifile = 'res_int_pr_me.dat'
    # 'IntensityDist.dat'

    order = []
    clength = []
    sigma = []
    for r in R:
        for c in C:
            name = str(r) + 'um_' + str(c) + '/'
            
            if os.path.exists(os.path.join(os.getcwd(), dirPath + name, Ifile)):
                order.append(name)
                clength.append(c)
                sigma.append(r)
            else:
                print(name + '... not found')
    c = [
          0,
          10,30,40,50,
          10,
          30,40,50,
          30,40,50,
         10,20,30,40,50,
         10,20,30,40,50,
         20,30,40,50,
         20,30,40,50,
         30,40,50,
         30,40,50,
         40,50,
         40,50]
    r = [
          0,
          30,30,30,30,
          40,
          50,50,50,
          100,100,100,
         150,150,150,150,150,
         200,200,200,200,200,
         250,250,250,250,
         300,300,300,300,
         350,350,350,
         400,400,400,
         450,450,
         500,500]
    
    name = [str(_r) + 'um_' + str(_c) + '/' for _r,_c in zip(r,c)]
    order = name
    intensityFiles = [dirPath + o + Ifile for o in order]
    
    I_threshold = 1
    G_size = 0
    _e = 2.71828
    frac = 1/10 # 1/_e
    log = 0
    fitGauss = 1
    savgol = 0
    suppress_peak = 165 # 500#165
    

    AMP = [
            0.0,
            3.016387765071197e-09,6.102360188008288e-09, 8.031055574152644e-09,1.0385776162389328e-08, #30
            2.7095382849836953e-09, #40
            5.008100110915626e-09, 6.1101121461293464e-09, 7.603621216312748e-09,  #50
            3.975809860701153e-09, 4.7189583854131024e-09, 5.482511253759968e-09, #100
           1.056081068512468e-09, 2.6811681727968483e-09, 3.4921718096454575e-09, 4.1491834179568365e-09, 4.703568547831566e-09, #150
           7.66341586056225e-10, 2.304362327616702e-09, 3.209913420232057e-09, 3.763157204877446e-09, 4.300232009226104e-09, #200
           1.957442049194117e-09, 2.9658910922182028e-09, 3.5071212684151764e-09, 3.977052595673463e-09, #250
           1.7094107295934241e-09, 2.7164183088529227e-09, 3.3234557931908824e-09, 3.748497232782469e-09, #300
           2.43635600518475e-09, 3.1662308723429888e-09, 3.5833760161372036e-09, #350
           2.2640573815065912e-09, 3.0047414176195986e-09, 3.4186001710150556e-09, #400
           2.849456899424863e-09, 3.2867417571126873e-09, #450
           2.699828279211232e-09, 3.1460558288819256e-09] #500
    #[3.016387765071197e-09, 4.58346054359592e-09, 6.102360188008288e-09, 8.031055574152644e-09, 1.0385776162389328e-08, #30
    # 2.7095382849836953e-09, 4.18703535978458e-09, 5.429089596045713e-09, 6.88764401490643e-09, 8.780550178302147e-09, #40
    # 2.4545895441573195e-09, 3.908461350505914e-09, 5.008100110915626e-09, 6.1101121461293464e-09, 7.603621216312748e-09,#50
    # 2.242784670053878e-09, 3.6953668953260938e-09, 4.678455324109337e-09, 5.679515333180197e-09, 6.828877559008521e-09, #60
    # 2.0399929294964275e-09, 3.518200700150911e-09, 4.462053893757656e-09, 5.378424447834905e-09, 6.319916457500549e-09, #70
    # 1.8710971902786945e-09, 3.3791602898360313e-09, 4.252526296458387e-09, 5.111232242202665e-09, 5.991173767741781e-09, #80
    # 1.5909127583925899e-09, 3.135425649823205e-09, 3.975809860701153e-09, 4.7189583854131024e-09, 5.482511253759968e-09, #100
    # 1.056081068512468e-09, 2.6811681727968483e-09, 3.4921718096454575e-09, 4.1491834179568365e-09, 4.703568547831566e-09, #150
    # 7.66341586056225e-10, 2.304362327616702e-09, 3.209913420232057e-09, 3.763157204877446e-09, 4.300232009226104e-09, #200
    # 1.957442049194117e-09, 2.9658910922182028e-09, 3.5071212684151764e-09, 3.977052595673463e-09, #250
    # 1.7094107295934241e-09, 2.7164183088529227e-09, 3.3234557931908824e-09, 3.748497232782469e-09, #300
    # 2.43635600518475e-09, 3.1662308723429888e-09, 3.5833760161372036e-09, #350
    # 2.2640573815065912e-09, 3.0047414176195986e-09, 3.4186001710150556e-09, #400
    # 2.849456899424863e-09, 3.2867417571126873e-09, #450
    # 2.699828279211232e-09, 3.1460558288819256e-09] #500
    
    # CLEN =  [1.4727555395929846e-08,1.6135569917510868e-08, 1.5590501944447553e-08, 
    #          2.646283837477489e-08, 2.6705723972929028e-08, 2.6599043845058543e-08, 
    #  3.786620033714236e-08, 3.725429087519083e-08, 3.70937326551284e-08,
    #  7.24957709697544e-08, 7.136193874808976e-08, 7.056320881975831e-08, 
    #  1.0269506739247003e-07, 1.0161040689736109e-07, 1.0359985777488058e-07, 
    #  1.3709364899090413e-07, 1.4859113529527584e-07, 1.6230885942593075e-07, 
    #  1.5753368275352675e-07, 1.5751544987504004e-07
    #  ]
    # [1.3928556735451649e-08,1.2183545884634037e-08,1.1905288939928361e-08,
             # 3.786620033714236e-08,3.725429087519083e-08,3.70937326551284e-08,
             # 7.24957709697544e-08, 7.136193874808976e-08, 7.056320881975831e-08,
             # 1.0269506739247003e-07,1.0161040689736109e-07,1.0359985777488058e-07,
             # 1.5753368275352675e-07,1.5751544987504004e-07]
    CLEN = [
            0.0,
            1.3928556735451649e-08,1.2183545884634037e-08, 1.1905288939928361e-08,1.1752924545289062e-08,  #30
            1.8505147815803875e-08, #40
            2.0050374577727624e-08, 1.978386467744462e-08, 1.8983958830280756e-08, #50
            3.786620033714236e-08, 3.725429087519083e-08, 3.70937326551284e-08, #100
            5.421859492741135e-08, 5.705283784278363e-08, 5.592505779446223e-08, 5.43727038010882e-08, 5.415636217533553e-08, #150
            6.49968692852524e-08, 7.060555097896247e-08, 7.24957709697544e-08, 7.136193874808976e-08, 7.056320881975831e-08, #200
            8.246661402257836e-08, 8.783681941115278e-08, 8.823807986129125e-08, 8.803228431283725e-08,  #250
            9.708711126580204e-08, 1.0269506739247003e-07, 1.0161040689736109e-07, 1.0359985777488058e-07,  #300
            1.221843701257718e-07, 1.1814628461038706e-07, 1.18111238680232e-07,  #350
            1.3669036637595525e-07, 1.3315690217564072e-07, 1.33924190655721e-07, #400
            1.4586131357045706e-07, 1.4425042518054088e-07, #450
            1.5753368275352675e-07, 1.5751544987504004e-07] #500
    #[1.3928556735451649e-08, 1.255587727725058e-08, 1.2183545884634037e-08, 1.1905288939928361e-08, 1.1752924545289062e-08, 
    # 1.8505147815803875e-08, 1.6990649935393598e-08, 1.595860219101251e-08, 1.5612374902459373e-08, 1.5168973911505048e-08, 
    # 2.274084297147959e-08, 2.1690932983026807e-08, 2.0050374577727624e-08, 1.978386467744462e-08, 1.8983958830280756e-08,
    # 2.6742059984484254e-08, 2.5722657090844682e-08, 2.4040514497872457e-08, 2.389306966230613e-08, 2.3105848686231706e-08, 
    # 2.971863334810301e-08, 2.9569312823911468e-08, 2.7727847172878385e-08, 2.7460953023302613e-08, 2.7168315269960114e-08, 
    # 3.302891799188977e-08, 3.3328291410818976e-08, 3.0926426516914295e-08, 3.0915512475726705e-08, 3.030839511021523e-08, 
    # 3.973527082993862e-08, 4.081215059598284e-08, 3.786620033714236e-08, 3.725429087519083e-08, 3.70937326551284e-08,
    # 5.421859492741135e-08, 5.705283784278363e-08, 5.592505779446223e-08, 5.43727038010882e-08, 5.415636217533553e-08, 
    # 6.49968692852524e-08, 7.060555097896247e-08, 7.24957709697544e-08, 7.136193874808976e-08, 7.056320881975831e-08, 
    # 8.246661402257836e-08, 8.783681941115278e-08, 8.823807986129125e-08, 8.803228431283725e-08, 
    # 9.708711126580204e-08, 1.0269506739247003e-07, 1.0161040689736109e-07, 1.0359985777488058e-07, 
    # 1.221843701257718e-07, 1.1814628461038706e-07, 1.18111238680232e-07, 
    # 1.3669036637595525e-07, 1.3315690217564072e-07, 1.33924190655721e-07, 
    # 1.4586131357045706e-07, 1.4425042518054088e-07, 
    # 1.5753368275352675e-07, 1.5751544987504004e-07]
    

    #[1.4727556148635645e-08, 1.5937364883331687e-08, 1.6135569774892195e-08, 1.559049909660557e-08, 1.4073201054400636e-08, #30
    # 1.922095792336182e-08, 2.121354962770152e-08, 2.1390675743984456e-08, 2.1482415650742637e-08, 2.0458923430833793e-08, #40
    # 2.3224239844132928e-08, 2.5914383338918227e-08, 2.6462838150932005e-08, 2.6705714589027955e-08, 2.65990966563463e-08, #50
    # 2.6889536202885506e-08, 2.998578711477559e-08, 3.1681923494854016e-08, 3.1691104398558346e-08, 3.181392521710338e-08, #60
    # 2.9948536477623856e-08, 3.387888763359171e-08, 3.628205210099372e-08, 3.6876966517870725e-08, 3.6921688348685974e-08, #70
    # 3.3123946674996e-08, 3.754501464067993e-08, 4.068831922121904e-08, 4.1863885251528277e-08, 4.2011151481684215e-08, #80
    # 3.998276981853463e-08, 4.438196493258947e-08, 4.8837945586600984e-08, 5.064744262802844e-08, 5.139876981083624e-08, #100
    # 5.352330062857801e-08, 5.889428028973509e-08, 6.687791056819281e-08, 7.268951176967429e-08, 7.444772752525978e-08, #150
    # 6.297328333668129e-08, 7.182415548067742e-08, 8.258028153239154e-08, 9.22633517889298e-08, 9.765197870472679e-08, #200
    # 8.306755350840893e-08, 9.748706097790091e-08, 1.0779178748532417e-07, 1.1524349891104237e-07, #250
    # 9.769255908095117e-08, 1.101632022596104e-07, 1.2392560109796275e-07, 1.313855443085085e-07, #300
    # 1.2517828781201882e-07, 1.375377107765822e-07, 1.4852806006472062e-07, #350
    # 1.3709288415461228e-07, 1.4859262186510616e-07, 1.6230465713163418e-07,#400
    # 1.5929766833490644e-07, 1.708391357486508e-07,#450
    # 1.6848753537133408e-07, 1.7989298720022828e-07]#500

    FW,FLUX = [],[]
    FWe, FLUXe = [],[]
    
    
    for e,i in enumerate(intensityFiles):
        print('\n Analysing file ', str(e+1), ' out of ', str(len(intensityFiles)))
        w, f, we, fe = analyse_scatter(i, I_threshold, G_size, frac, det_distance=Z, wl=WL,
                               log=log,fitGauss=fitGauss,savgol=savgol,suppress_peak=suppress_peak,
                               getPSD=True, show=True, sumtype='all')
        
        FW.append(w)
        FLUX.append(f)
        FWe.append(we)
        FLUXe.append(fe)
        
        fig, ax = plt.subplots(2,1)
        ax[0].errorbar(CLEN[0:len(FW)],FW,yerr=FWe,fmt='x')
        ax[1].errorbar(AMP[0:len(FLUX)],FLUX,yerr=FLUXe,fmt='x')
        ax[0].set_xlabel('LER correlation length [nm]')
        ax[0].set_ylabel('Intensity Full Width [mm]')
        ax[1].set_xlabel('LER amplitude [nm]')
        ax[1].set_ylabel('Flux in FW [ph/s]')
        # ax[0].plot([c*1e9 for c in CLEN[0:e+1]],[fw*1e3 for fw in FW] ,'x',color=colour[e])
        # ax[1].plot([a*1e9 for a in AMP[0:e+1]],FLUX,'x',color=colour[e])
        fig.tight_layout()
        plt.show()
    # plt.show()
    
    import pickle
    with open(dirPath + 'results_pc_err.pkl', "wb") as f:
        pickle.dump([AMP,CLEN,FW,FLUX,FWe,FLUXe], f)


    plt.errorbar([c*1e9 for c in CLEN],[F*1e3 for F in FW],yerr=[FE*1e3 for FE in FWe],fmt='x')
    plt.ylabel('Intensity Full Width [mm]')
    plt.xlabel('LER correlation length [nm]')
    plt.show()
    
    plt.errorbar([a*1e9 for a in AMP],FLUX,yerr=FLUXe,fmt='x')
    plt.ylabel('Flux in FW [ph/s]')
    plt.xlabel('LER amplitude [nm]')
    plt.show()

def replot():
    import pickle
    
    wl = 6.7e-9
    D = 4.5e-9
    z=8.0e-3
    
    fit = False
    
    dirPath ='/user/home/opt/xl/xl/experiments/CDSAXS2/data/'
    
    # amp, clen, fw, flux = pickle.load(open(dirPath + 'results_pc.pkl', 'rb'))
    amp, clen, fw, flux, fwe, fluxe = pickle.load(open(dirPath + 'results_pc_err.pkl', 'rb'))
    # colour = ['b','b','b','b','b',
    #           'r','r','r','r','r',
    #           'g','g','g','g','g',
    #           'y','y','y','y','y',
    #           'm','m','m','m','m',
    #           'c','c','c','c','c',
    #           'black','black','black','black','black',
    #           'brown','brown','brown','brown','brown',
    #           'pink','pink','pink','pink','pink',
    #           'orange','orange','orange','orange',
    #           'gray','gray','gray','gray',
    #           'lime','lime','lime',
    #           'tan','tan','tan',
    #           'deepskyblue','deepskyblue',
    #           'salmon','salmon']

    # amp = [3.016387765071197e-09,6.102360188008288e-09, 8.031055574152644e-09,
    #        5.008100110915626e-09, 6.1101121461293464e-09, 7.603621216312748e-09, 
    #        3.975809860701153e-09, 4.7189583854131024e-09, 5.482511253759968e-09, 
    #        3.209913420232057e-09, 3.763157204877446e-09, 4.300232009226104e-09, 
    #        2.7164183088529227e-09, 3.3234557931908824e-09, 3.748497232782469e-09, 
    #        2.2640573815065912e-09, 3.0047414176195986e-09, 3.4186001710150556e-09, 
    #        2.699828279211232e-09, 3.1460558288819256e-09]
    # clen = [1.3928556735451649e-08,1.2183545884634037e-08, 1.1905288939928361e-08,
    #         2.0050374577727624e-08, 1.978386467744462e-08, 1.8983958830280756e-08,
    #         3.786620033714236e-08, 3.725429087519083e-08, 3.70937326551284e-08,
    #         7.24957709697544e-08, 7.136193874808976e-08, 7.056320881975831e-08, 
    #         1.0269506739247003e-07, 1.0161040689736109e-07, 1.0359985777488058e-07,
    #         1.3669036637595525e-07, 1.3315690217564072e-07, 1.33924190655721e-07, 
    #         1.5753368275352675e-07, 1.5751544987504004e-07]
    colour = ['b','b','b',#'b','b',
              'c','c','c','c','c',
              'm','m','m','m',
              # 'lime','lime','lime',
              'r','r','r',#'r','r',
              'g','g','g',#'g','g',
              # 'black','black','black',
              'y','y',#'y','y','y',
               # 'm','m','m','m','m',
              # 'c','c','c','c','c',
              # 'black','black','black','black','black',
              # 'brown','brown','brown','brown','brown',
              # 'pink','pink','pink','pink','pink',
              # 'orange','orange','orange','orange',
              # 'gray','gray','gray','gray',
              # 'lime','lime','lime',
              # 'tan','tan','tan',
              # 'deepskyblue','deepskyblue',
              # 'salmon','salmon'
              ]
    
    c_min = 40.0e-9
    a_min = 0.5e-9
    a_max = 8.0e-9
    _amp, _clen, _flux, _fw = [],[],[],[]
    _fluxe, _fwe = [],[]
    for i,c in enumerate(clen):
        if c > c_min:
            if amp[i] > a_min and amp[i] < a_max:
                _amp.append(amp[i])
                _clen.append(clen[i])
                _flux.append(flux[i])
                _fw.append(fw[i])
                try:
                    _fluxe.append(fluxe[i])
                    _fwe.append(fwe[i])
                except:
                    pass
    amp = _amp
    clen=_clen
    flux=_flux
    fw=_fw
    fluxe = _fluxe
    fwe = _fwe

    # amp = [amp[i] for i,c in enumerate(clen) if c > c_min]
    # clen = [c for c in clen if c > c_min]
    # fw = [fw[i] for i,c in enumerate(clen) if c > c_min]
    # flux = [flux[i] for i,c in enumerate(clen) if c > c_min]
    # amp = [a for a in amp[10::]]#[0:7]]#3::]]
    # clen = [a for a in clen[10::]]#[0:7]]#3::]]
    # fw = [a for a in fw[10::]]#[0:7]]#3::]]
    # flux = [a for a in flux[10::]]#[0:7]]#3::]]
    
    # print(amp)
    # print(clen)
    # print(flux)
    # print(fw)
    for n in [amp,clen,flux,fw,fluxe,fwe]:
        print(np.shape(n))

    if fit:
        # Fit linear function to amp vs flux: y = a*x + b
        a, b = np.polyfit([_a**2 for _a in amp], flux, 1)
        
        print(f"Fitted line: $\Phi$ = {a:.5f}$\sigma^{2}$ + {b:.5f}")
    
        # Transform x to 1/x^2 for clen vs fw fit
        c_t = [1 / (_c*1e9)**2 for _c in clen]
    
        # Fit linear model to clen vs fw: y = a * (1/x^2)
        d, e = np.polyfit(c_t, fw, 1)
        # d, e = np.polyfit(clen, fw, 1)
    
        print(f"Fitted function: fw = {d:.5f} / $c^2$ + {e:.5f}")
    
        x_c = np.linspace(np.min(clen)*1e9 - 10,np.max(clen)*1e9 + 10,400)
        fw_fit = [((d/ (_c)**2) + e)*1e3 for _c in x_c]
        # [(d*(s) + e)*1e-9 for s in x_c]
        # [((d/ (_c)**2) + e)*1e3 for _c in x_c]
        
        x_a = np.linspace(np.min(amp)*1e9 - 0.25,np.max(amp)*1e9 + 0.25,400)
        flux_fit = [a*((s*1e-9)**2) + b for s in x_a]
    
    fig, ax = plt.subplots(2,1)
    ax[0].set_xlabel('LER correlation length [nm]')
    ax[0].set_ylabel('Intensity Full Width [mm]')
    ax[1].set_xlabel('LER amplitude [nm]')
    ax[1].set_ylabel('Flux in FW [ph/s]')
    
    for i,x in enumerate(clen):
        if x < 60.0e-9:
            c = 'b'
        elif x > 60.0e-9 and x < 75.0e-9:
            c = 'm'
        elif x > 75.0e-9 and x < 90.0e-9:
            c = 'brown'
        elif x > 90.0e-9 and x < 110.0e-9:
            c = 'c'
        elif x > 110.0e-9 and x < 130.0e-9:
            c = 'r'
        elif x > 130.0e-9 and x < 140.0e-9:
            c = 'g'
        elif x > 140.0e-9 and x < 150.0e-9:
            c = 'black'
        elif x > 150.0e-9:# and x < 80.0e-9:
            c = 'y'
            
    # for i,x in enumerate(amp):
    #     if x < 1.50e-9:
    #         c = 'b'
    #     elif x > 1.5e-9 and x < 2.0e-9:
    #         c = 'm'
    #     elif x > 2.0e-9 and x < 2.5e-9:
    #         c = 'brown'
    #     elif x > 2.5e-9 and x < 3.0e-9:
    #         c = 'c'
    #     elif x > 3.0e-9 and x < 3.5e-9:
    #         c = 'r'
    #     elif x > 3.5e-9 and x < 4.0e-9:
    #         c = 'g'
    #     elif x > 4.0e-9 and x < 5.0e-9:
    #         c = 'black'
    #     elif x > 5.0e-9:# and x < 80.0e-9:
    #         c = 'y'
            
        
        # ax[0].plot(clen[i]*1e9,fw[i]*1e3,'x',color=c)
        # ax[1].plot(amp[i]*1e9,flux[i],'x',color=c)
        print('fwe: ', fwe[i])
        print('fluxe: ', flux[i])
        print(np.shape(fwe))
        ax[0].errorbar(clen[i]*1e9,fw[i]*1e3,yerr=fwe[i]*1e3,fmt='x',color=c)
        ax[1].errorbar(amp[i]*1e9,flux[i],yerr=fluxe[i],fmt='x',color=c)
    if fit:
        ax[0].plot(x_c,fw_fit, '--',color='black',label="$FW$ = " + str(round_sig(d,3)) + " / $c^2$  + " + str(round_sig(e,3)) )
        ax[1].plot(x_a,flux_fit, '--',color='black',label="$\Phi$ = " + str(round_sig(a,3)) + " $\sigma^{2}$ + " + str(round_sig(b,3)) )
    # ax[0].plot(x_c,[((wl*z / (_c*1e-9))/1)*1e3 for _c in x_c],':')
        ax[0].legend()
        ax[1].legend()
    fig.tight_layout()
    plt.show()
    
    fig, ax = plt.subplots(2,2)
    ax[0,0].set_xlabel('LER correlation length [nm]')
    ax[0,0].set_ylabel('$\sqrt{1 / FW}$ [m$^{-1}$]')
    ax[0,1].set_xlabel('LER amplitude [nm]')
    ax[0,1].set_ylabel('1/$\sqrt{\Phi}$ [s/ph]')
    ax[1,0].set_xlabel('LER correlation length [nm]')
    ax[1,0].set_ylabel('$\Phi$ [ph/s]')
    ax[1,1].set_xlabel('LER amplitude [nm]')
    ax[1,1].set_ylabel('FW [mm]')#'/ $\sigma$')
    
    for i,x in enumerate(clen):
        if x < 60.0e-9:
            c = 'b'
        elif x > 60.0e-9 and x < 75.0e-9:
            c = 'm'
        elif x > 75.0e-9 and x < 90.0e-9:
            c = 'brown'
        elif x > 90.0e-9 and x < 110.0e-9:
            c = 'c'
        elif x > 110.0e-9 and x < 130.0e-9:
            c = 'r'
        elif x > 130.0e-9 and x < 140.0e-9:
            c = 'g'
        elif x > 140.0e-9 and x < 150.0e-9:
            c = 'black'
        elif x > 150.0e-9:# and x < 80.0e-9:
            c = 'y'
            
    # for i,x in enumerate(amp):
    #     if x < 1.50e-9:
    #         c = 'b'
    #     elif x > 1.5e-9 and x < 2.0e-9:
    #         c = 'm'
    #     elif x > 2.0e-9 and x < 2.5e-9:
    #         c = 'brown'
    #     elif x > 2.5e-9 and x < 3.0e-9:
    #         c = 'c'
    #     elif x > 3.0e-9 and x < 3.5e-9:
    #         c = 'r'
    #     elif x > 3.5e-9 and x < 4.0e-9:
    #         c = 'g'
    #     elif x > 4.0e-9 and x < 5.0e-9:
    #         c = 'black'
    #     elif x > 5.0e-9:# and x < 80.0e-9:
    #         c = 'y'
        
        ax[0,0].plot(clen[i],1/fw[i],'x',color=c) #clen[i]*1e9,fw[i]*1e3 / clen[i]*1e9,'x',color=c)
        ax[0,1].plot(amp[i],1/flux[i],'x',color=c) #amp[i]*1e9,flux[i] / amp[i]*1e9,'x',color=c)
        ax[1,0].plot(clen[i]*1e9,flux[i],'x',color=c)
        ax[1,1].plot(amp[i]*1e9,fw[i]*1e3,'x',color=c)
    fig.tight_layout()
    plt.show()
    
    # for i,x in enumerate(clen):
    #     if x < 60.0e-9:
    #         c = 'b'
    #     elif x > 60.0e-9 and x < 75.0e-9:
    #         c = 'm'
    #     elif x > 75.0e-9 and x < 90.0e-9:
    #         c = 'brown'
    #     elif x > 90.0e-9 and x < 110.0e-9:
    #         c = 'c'
    #     elif x > 110.0e-9 and x < 130.0e-9:
    #         c = 'r'
    #     elif x > 130.0e-9 and x < 140.0e-9:
    #         c = 'g'
    #     elif x > 140.0e-9 and x < 150.0e-9:
    #         c = 'black'
    #     elif x > 150.0e-9:# and x < 80.0e-9:
    #         c = 'y'
        
    #     plt.plot(clen[i],amp[i],'x',color=c)
    # plt.xlabel('LER correlation length [nm]')
    # plt.ylabel('LER amplitude [nm]')
    # plt.show()

    # fig, ax = plt.subplots(1,1)
    # ax.set_xlabel('$c$ / FW')#'LER correlation length [nm]')
    # ax.set_ylabel('$\sigma / \Phi $ [nm/ph/s]')
    # # ax[1].set_xlabel('LER amplitude [nm]')
    # # ax[1].set_ylabel('Flux in FW [ph/s]')
    
    # for i,x in enumerate(clen):
    #     if x < 60.0e-9:
    #         c = 'b'
    #     elif x > 60.0e-9 and x < 75.0e-9:
    #         c = 'm'
    #     elif x > 75.0e-9 and x < 90.0e-9:
    #         c = 'brown'
    #     elif x > 90.0e-9 and x < 110.0e-9:
    #         c = 'c'
    #     elif x > 110.0e-9 and x < 130.0e-9:
    #         c = 'r'
    #     elif x > 130.0e-9 and x < 140.0e-9:
    #         c = 'g'
    #     elif x > 140.0e-9 and x < 150.0e-9:
    #         c = 'black'
    #     elif x > 150.0e-9:# and x < 80.0e-9:
    #         c = 'y'
        
    #     X = (clen[i] / fw[i])#amp[i])
    #     Y = 1/(flux[i] / amp[i])#fw[i])
    #     # ax.plot(clen[i]*1e9,1/(amp[i]*1e9 / flux[i]),'x',color=c)
    #     ax.plot(X,Y,'x',color=c)
    #     # ax[1].plot(amp[i]*1e9,flux[i],'x',color=c)
    # fig.tight_layout()
    # plt.show()

    # from mpl_toolkits.mplot3d import Axes3D
    
    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    
    # # x = np.random.standard_normal(100)
    # # y = np.random.standard_normal(100)
    # # z = np.random.standard_normal(100)
    # # c = np.random.standard_normal(100)
    
    # x = [C*1e9 for C in clen]
    # y = [A*1e9 for A in amp]
    # z = flux#[F*1e3 for F in fw]
    # c =[F*1e3 for F in fw]# flux
    # index_x = 0; index_y = 1; index_z = 2; index_c = 3;
    # list_name_variables = ['$c$ [nm]','$\sigma$ [nm]', '$\Phi$ [ph/s]', 'FW [mm]'];
    # img = ax.scatter(x, y, z)#, c=c, cmap=plt.hot())
    # ax.set_xlabel(list_name_variables[index_x]); ax.set_ylabel(list_name_variables[index_y]);
    # ax.set_zlabel(list_name_variables[index_z]);
    # # fig.colorbar(img,label=list_name_variables[index_c])
    # fig.tight_layout()
    # plt.show()
    
    # import matplotlib.tri as mtri

    # index_x = 0; index_y = 1; index_z = 2; index_c = 3;
    # list_name_variables = ['$c$ [nm]','$\sigma$ [nm]', 'FW [mm]', '$\Phi$ [ph/s]'];
    # name_color_map = 'seismic';
    
    # x = [C*1e9 for C in clen]
    # y = [A*1e9 for A in amp]
    # z = [F*1e3 for F in fw]
    # c = flux
    # #end
    # #-----
    
    # # # We create triangles that join 3 pt at a time and where their colors will be
    # # # determined by the values ​​of their 4th dimension. Each triangle contains 3
    # # # indexes corresponding to the line number of the points to be grouped. 
    # # # Therefore, different methods can be used to define the value that 
    # # # will represent the 3 grouped points and I put some examples.
    # # triangles = mtri.Triangulation(x, y).triangles;
    
    
    
    # # choice_calcuation_colors = 1;
    
    # # print(triangles[:,0])
    # # if choice_calcuation_colors == 1: # Mean of the "c" values of the 3 pt of the triangle
    # #     colors = np.mean( [[c[i] for i in triangles[:,0]], [c[i] for i in triangles[:,1]], [c[i] for i in triangles[:,2]]], axis = 0);
    # # elif choice_calcuation_colors == 2: # Mediane of the "c" values of the 3 pt of the triangle
    # #     colors = np.median( [c[triangles[:,0]], c[triangles[:,1]], c[triangles[:,2]]], axis = 0);
    # # elif choice_calcuation_colors == 3: # Max of the "c" values of the 3 pt of the triangle
    # #     colors = np.max( [c[triangles[:,0]], c[triangles[:,1]], c[triangles[:,2]]], axis = 0);
    # # #end
    # # #----------
    # # # Displays the 4D graphic.
    # # fig = plt.figure();
    # # ax = fig.gca(projection='3d');
    # # triang = mtri.Triangulation(x, y, triangles);
    # # surf = ax.plot_trisurf(triang, z, cmap = name_color_map, shade=False, linewidth=0.2);
    # # surf.set_array(colors); surf.autoscale();
    
    # # #Add a color bar with a title to explain which variable is represented by the color.
    # # cbar = fig.colorbar(surf, shrink=0.5, aspect=5);
    # # cbar.ax.get_yaxis().labelpad = 15; cbar.ax.set_ylabel(list_name_variables[index_c], rotation = 270);
    
    # # # Add titles to the axes and a title in the figure.
    # # ax.set_xlabel(list_name_variables[index_x]); ax.set_ylabel(list_name_variables[index_y]);
    # # ax.set_zlabel(list_name_variables[index_z]);
    # # plt.title('%s in function of %s, %s and %s' % (list_name_variables[index_c], list_name_variables[index_x], list_name_variables[index_y], list_name_variables[index_z]) );
    
    # # plt.show()
    # name_color_map_surface = 'Greens';  # Colormap for the 3D surface only.

    # fig = plt.figure(); 
    # ax = fig.add_subplot(111, projection='3d');
    # ax.set_xlabel(list_name_variables[index_x]); ax.set_ylabel(list_name_variables[index_y]);
    # ax.set_zlabel(list_name_variables[index_z]);
    # plt.title('%s in fcn of %s, %s and %s' % (list_name_variables[index_c], list_name_variables[index_x], list_name_variables[index_y], list_name_variables[index_z]) );
    
    # # In this case, we will have 2 color bars: one for the surface and another for 
    # # the "scatter plot".
    # # For example, we can place the second color bar under or to the left of the figure.
    # choice_pos_colorbar = 2;
    
    # #The scatter plot.
    # img = ax.scatter(x, y, z, c = c, cmap = name_color_map);
    # cbar = fig.colorbar(img, shrink=0.5, aspect=5); # Default location is at the 'right' of the figure.
    # cbar.ax.get_yaxis().labelpad = 15; cbar.ax.set_ylabel(list_name_variables[index_c], rotation = 270);
    
    # # The 3D surface that serves only to connect the points to help visualize 
    # # the distances that separates them.
    # # The "alpha" is used to have some transparency in the surface.
    # surf = ax.plot_trisurf(x, y, z, cmap = name_color_map_surface, linewidth = 0.2, alpha = 0.25);
    
    # # The second color bar will be placed at the left of the figure.
    # if choice_pos_colorbar == 1: 
    #     #I am trying here to have the two color bars with the same size even if it 
    #     #is currently set manually.
    #     cbaxes = fig.add_axes([1-0.78375-0.1, 0.3025, 0.0393823, 0.385]);  # Case without tigh layout.
    #     #cbaxes = fig.add_axes([1-0.844805-0.1, 0.25942, 0.0492187, 0.481161]); # Case with tigh layout.
    
    #     cbar = plt.colorbar(surf, cax = cbaxes, shrink=0.5, aspect=5);
    #     cbar.ax.get_yaxis().labelpad = 15; cbar.ax.set_ylabel(list_name_variables[index_z], rotation = 90);
    
    # # The second color bar will be placed under the figure.
    # elif choice_pos_colorbar == 2: 
    #     cbar = fig.colorbar(surf, shrink=0.75, aspect=20,pad = 0.05, orientation = 'horizontal');
    #     cbar.ax.get_yaxis().labelpad = 15; cbar.ax.set_xlabel(list_name_variables[index_z], rotation = 0);
    # #end
    # plt.show();
        
    # import pandas as pd
    
    # x = [C*1e9 for C in clen]
    # y = [A*1e9 for A in amp]
    # z = [F*1e3 for F in fw]
    # c = flux
    # dataStructure = [amp,clen,fw,flux]
    # for d in dataStructure:
    #     print(np.shape(d))

    # dF = pd.DataFrame(np.array(dataStructure).T,
    #                   columns=['$\sigma$','$c$','FW','$\Phi$'])
    # correlations = dF.corr()
    # import seaborn as sns

    # sns.heatmap(np.abs(correlations),cmap='gray',vmin=0,vmax=1,annot=True) #'vlag',vmin=-1,vmax=1,annot=True)
    # plt.show()

    # sns.heatmap(correlations,cmap='vlag',vmin=-1,vmax=1,annot=True)
    # plt.show()

if __name__ == '__main__':
    # test()
    replot()
    # testSingle()