#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 10:28:39 2022

@author: -
"""

import cv2 #(OpenCV3)
from LER import edge_roughness
from scipy import integrate
from matplotlib import pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import tifffile
import pickle
from PSD import analyticalPSD_biased, analyticalPSD_unbiased
from resampleArray import resample_2d_array

from sklearn.metrics import auc

# plt.rcParams["figure.figsize"] = (6,4)

from scipy.optimize import curve_fit

def flatten(xss):
    return [x for xs in xss for x in xs]

def fit_psd(frequencies, psd_values, model_function, bounds=None, p0=None, plot_fit=False):
    """
    Fits a model line to the PSD (Power Spectral Density) data using the provided model function.
    
    Parameters:
    - frequencies: Array-like, the frequency values corresponding to the PSD.
    - psd_values: Array-like, the PSD values to fit the model to.
    - model_function: A function that defines the model line to be fitted to the PSD.
                      It should take frequency and model parameters as input.
    - p0: Initial guess for the parameters of the model function (optional).
    - plot_fit: Boolean, if True, plot the PSD and fitted line.
    
    Returns:
    - popt: Optimal parameters of the fitted model.
    - pcov: Covariance of the parameter estimates.
    """
    # Fit the model to the PSD data
    
    guess = model_function(frequencies,*p0)
    
    if bounds:
        popt, pcov = curve_fit(model_function, frequencies, psd_values, p0=p0,bounds=bounds)
    else:
        popt, pcov = curve_fit(model_function, frequencies, psd_values, p0=p0)
    
    # Plot the fit if requested
    if plot_fit:
        plt.figure(figsize=(8, 6))
        plt.plot(frequencies[1::], psd_values[1::], 'b.', label='PSD Data')
        plt.plot(frequencies[1::], guess[1::], ':', label='Initial Guess')
        plt.plot(frequencies[1::], model_function(frequencies, *popt)[1::], 'r--', label='Fitted Model')
        plt.xlabel('Frequency')
        plt.ylabel('Power Spectral Density')
        plt.yscale('log')
        plt.xscale('log')
        plt.legend()
        plt.title('PSD Fit')
        # plt.ylim(1e-30,1e-25)
        plt.show()
    
    return popt, pcov

# Example Model Function (You can define your own model function)
def model_PSD(frequency, psd0, corr, rmsH):
    """
    Model function representing a linear relationship: y = a * f + b
    where 'f' is frequency, and 'a', 'b' are parameters to be fitted.
    """
    psd_fit = psd0 / (1 + ((2 * np.pi * frequency * corr)**(2*rmsH + 1)))
    
    return psd_fit


maskFile =  '/user/home/opt_old/LineEdgeRoughness_old/masks/restest_20000020.00000_20.00000_200.00000_mask.tif'
maskImage = tifffile.imread(maskFile)
print(np.shape(maskImage))

# PARAMETERS OF MASK FILE
X = 5000-2                                  # size of grating in pixels
Y = 5000-2
res = 1.0e-9                                # resolution in m
midX, midY = np.shape(maskImage)[1]/2, 4030 # grating center position
pitch = 100.0e-9 / res #pixels              # grating pitch in pixels
hp = pitch/2                                # half pitch

numlines = 100#int(Y//hp-2)                 # number of grating lines to analyse
shiftY = 0                                  # shift starting y position for analysis (pixels)
extraY = 10                                 # add extra y range for analysis (pixels)

resample = True                             # resample grating lines at wavefront resolution
wavefront_res = (9.96e-10,1.17e-8)          # wavefront resolution at grating plane
# (1.273741166410393e-09,40.0e-09)

print(midX, midY)
view = 250                                  # size of grating view for plotting

gratingImage = maskImage[int(midY - (Y/2)):int(midY + (Y/2)), int(midX - (X/2)):int(midX + (X/2))]
#maskImage[1000:5000,6500:10500]
# gratingImage[1000:2000,1000:2000]
plt.imshow(gratingImage[1000:1000 + view,:],cmap='gray',aspect='auto')#,extent=[res*(-500)*1e6,res*500*1e6,res*(-500)*1e6,res*500*1e6])
plt.xlabel('$x$ [pix]')#'[\u03bcm]')
plt.ylabel('$y$ [pix]')#[\u03bcm]')
plt.title('Input grating')
# plt.colorbar()
plt.show()


# RESAMPLE GRATING AT WAVEFRONT RESOLUTION
if resample:
    gratingImage = resample_2d_array(gratingImage, (res,res), wavefront_res)
    #maskImage[1000:5000,6500:10500]
    # gratingImage[1000:2000,1000:2000]
    fy,fx = res/wavefront_res[0], res/wavefront_res[1]
    plt.imshow(gratingImage[int(fy*1000):int(fy*(1000 + view)),:],cmap='gray',aspect='auto')#,extent=[res*(-500)*1e6,res*500*1e6,res*(-500)*1e6,res*500*1e6])
    plt.xlabel('$x$ [pix]')#[\u03bcm]')
    plt.ylabel('$y$ [pix]')#[\u03bcm]')
    plt.title('Resampled grating')
    # plt.colorbar()
    plt.show()
   
    midX, midY = np.shape(gratingImage)[1]/2, np.shape(gratingImage)[0]/2 #5245#(3*np.shape(maskImage)[0])/17
    pitch = 200.0e-9 / wavefront_res[0] #pixels
    hp = pitch/2
    
    X = np.shape(gratingImage)[1]
    Y = np.shape(gratingImage)[0]
    
    numlines = int(Y//pitch-5) # 125

save2pick = False

# SAVE GRATING IMAGE
if save2pick:
    with open(maskFile[0:int(len(maskFile)-4)] + 'CLOSE.pkl', "wb") as f:
                pickle.dump(gratingImage, f, protocol=2)


# CALCULATE LER
f = []
p = []
LER = []
for n in range(0,numlines):
    
    lineImage = gratingImage[int(shiftY + n*hp):int(shiftY + hp//2 + extraY + n*hp),:]
    if lineImage[0,0] != 0:
        
        lineImage = abs(255 - lineImage)
    
    # print('Shape of gratingImage: ', np.shape(gratingImage))
    # print('Shaoe of lineImage:    ', np.shape(lineImage))
    if resample:
        Lbox = wavefront_res[1]*X
    else:
        Lbox = X*res
    fmin = 1 / (2*np.pi*Lbox)
    smax =  1 / fmin

    if n==0:
        print('Analysing ', numlines, ' lines ...')
        print("minimum frequency sampled: ", fmin, ' /m')
        print("maximum feature size sampled: ", smax, ' m')

    _LER = edge_roughness()
    # PLOT FIRST AND LAST LINE
    if n== 0 or n == numlines-1:
        if resample:
            plt.imshow(lineImage,aspect='auto',cmap='gray',extent=[wavefront_res[1]*(-midX)*1e6,
                                                                   wavefront_res[1]*midX*1e6,
                                                                   -wavefront_res[0]*((hp//2 + extraY)/2)*1e9,
                                                                   wavefront_res[0]*((hp//2 + extraY)/2)*1e9])
        else:
            plt.imshow(lineImage,aspect='auto',cmap='gray',extent=[wavefront_res[1]*(-midX)*1e6,
                                                                   wavefront_res[1]*midX*1e6,
                                                                   -wavefront_res[0]*((hp//2 + extraY)/2)*1e9,
                                                                   wavefront_res[0]*((hp//2 + extraY)/2)*1e9])
        plt.xlabel('$x$ [\u03bcm]')
        plt.ylabel('$y$ [nm]')
        plt.show()
        
        # print('Length of lineImage:   ', len(lineImage))
        if resample:
            (Xcln, Ycln, freq, FourierPow) = _LER.LER_analysis(lineImage, [wavefront_res[1],wavefront_res[0]], 10,show=True) #image, image width (m), threshold for outliers
        else:
            (Xcln, Ycln, freq, FourierPow) = _LER.LER_analysis(lineImage, [res,res], 10,show=True) #image, image width (m), threshold for outliers
        
        # print('Length of Ycln:         ', len(Ycln))
        # print('Length of Xcln:         ', len(Xcln))
        # print('Length of freq:         ', len(freq))
        # print('Length of FourierPow:   ', len(FourierPow))
    else:
        if resample:
            (Xcln, Ycln, freq, FourierPow) = _LER.LER_analysis(lineImage, [wavefront_res[1],wavefront_res[0]], 10,show=False) #image, image width (m), threshold for outliers
        else:
            (Xcln, Ycln, freq, FourierPow) = _LER.LER_analysis(lineImage, [res,res], 10,show=False) #image, image width (m), threshold for outliers
    
    L = 3*np.std(np.abs(Ycln))
    
    LER.append(L)
    f.append(freq)
    p.append(FourierPow)


# print(np.shape(f))
f=np.mean(f,axis=0)
p=np.mean(p,axis=0)
LER=np.mean(LER,axis=0)
# print(np.shape(f))

# plt.plot(Xcln, Ycln, '-')
# plt.plot(Xcln, Ycln, 'r.')
# plt.show()

# print(np.shape(freq))
        
# FITTING PSD
# - initial guess
import math
PSD0 = abs(np.mean(p[1:4]))# 1.429755368826315e-24 # PSD(0)
H = 0.5 #1.5                 # 
c = 75.0e-9    # correlation length
fan = np.linspace(np.min(f),np.max(f),5000) # Frequency range
if resample:
    dx = wavefront_res[1]    
else:
    dx = res
N = len(Ycln)
sigma= 2.5e-11              # bias 

B_b = None#((0.0, 0.2, 1e-10,0.0), (PSD0*2,1.0, 500.0e-9,15e-12))

print('-----GUESS-----')
print('PSD(0):    ', PSD0)
print('H:         ', H)
print('lc:        ', c)
# print('N:         ', N)
print('sigma:     ', sigma)

# FITTING BIASED PSD 
popt, pcov = fit_psd(f,p,analyticalPSD_biased,p0=[PSD0,H,c,sigma],bounds=B_b,plot_fit=True)#plot_fit=True)#,bounds=B_b,plot_fit=True)

PSD0, H, c, sigma = popt
PSD = analyticalPSD_biased(f, PSD0, H, c,sigma)


B = None #[(PSD0/2,0.25,c*0.5),(PSD0*1.1,1.0,c*1.5)]

print('-----UNBIASED FIT-----')
print('PSD(0):    ', PSD0)
print('H:         ', H)
print('lc:        ', c)
# print('N:         ', N)
print('sigma:     ', sigma)

# plt.plot(freq[2:100], FourierPow[2:100],'-')
plt.plot([_f/1.0e9 for _f in f[1::]], p[1::],'.', label='biased',alpha=0.2)
ax = plt.gca()
ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%0.0e'))
plt.yscale('log')
plt.xscale('log')
plt.xlabel('Spatial frequency (nm$^{-1}$)')
plt.ylabel('Fourier power (au)')
# plt.ylim([np.min(p),(np.max(p) + np.std(p))])
plt.title('Fourier power spectrum')

# REMOVING BIAS FROM PSD
p_ub = [P - (sigma**2)*(dx*N) for P in p]

plt.plot([_f/1.0e9 for _f in f[1::]], p_ub[1::],'.', label='unbiased',alpha=0.2)
plt.plot([_f/1e9 for _f in f[1:len(PSD)]],PSD[1::],'black', label='analytic')

plt.legend()
plt.show()
    
print('-----GUESS-----')
print('PSD(0):    ', PSD0)
print('H:         ', H)
print('lc:        ', c)

p_ub = np.array(p_ub)
popt, pcov = fit_psd(f,p_ub,analyticalPSD_unbiased,p0=[PSD0,1.0,c],bounds = B,plot_fit=True)
# set limits for fitted variables - H

PSD0, H, lc = popt
# if H>=1.0:
#     H = 1.0
print('-----FIT-----')
print('PSD(0):    ', popt[0])
print('H:         ', popt[1])
print('lc:        ', popt[2])
print('f(0)       ',f[0] )
print('1/f(0)       ',1/f[0] )
# print(popt)
# print(pcov)



# lc = 10.0e-9
if resample:
    per = 1 - ((2/np.pi) * np.arctan(lc/(X*wavefront_res[1])))
else:
    per = 1 - ((2/np.pi) * np.arctan(lc/(X*res)))

ler = np.sqrt(integrate.simpson(p, f))
print('LER from integration of PSD:                 ', 3*ler)
print('LER from standard deviation of line profile: ', LER)
print('LER error (PSD) [nm]:                        ', (1-per)*3*ler*1e9)
print('LER error (different methods) [nm]:          ', abs(3*ler - LER)*1e9)
# print(((LER + (3*ler))/2)*1e9)

