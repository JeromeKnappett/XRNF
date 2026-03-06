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

# from PSD import analyticalPSD_biased, analyticalPSD_unbiased
from sklearn.metrics import auc

# plt.rcParams["figure.figsize"] = (2,3)

from scipy.optimize import curve_fit

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
    popt, pcov = curve_fit(model_function, frequencies, psd_values, p0=p0,bounds=bounds)
    
    # Plot the fit if requested
    if plot_fit:
        plt.figure(figsize=(8, 6))
        plt.plot(frequencies[1::], psd_values[1::], 'b.', label='PSD Data')
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


dirPath =  '/user/home/opt/xl/xl/experiments/maskLER2/data/'
order = ['rms05','rms10','rms15','rms20','rms25','rms30','rms35','rms40']#range(0,25)
sigma = [0.5,1.0,1.5,2.0,2.5,3.0,3.5,4.0]
files = [str(o) + '/' + str(o) + '.pkl' for o in order]


N = 2000                            # number of pixels to take for line profile  - 1200 for roughness aerial images
n = 15                             # number of pixels to average over for line profile - 15 for roughness aerial images
plotRange = 1000                       # range of aerial image plot in nm

#middle pixels of images
mid = np.full((np.shape(files)[0],2), (398, 25025))

pitch = 50e-9
picks = [pickle.load(open(dirPath + f, 'rb')) for f in files]
tiffs = [p[0] for p in picks]
res = [(p[1],p[2]) for p in picks]

# midx, midy = np.shape(tiffs[0])[1]//2, np.shape(tiffs[0])[0]//2
# mid = np.full((np.shape(files)[0],2), (midy,midx-3530))

# print(np.shape(tiffs))
# print(mid)
# plt.imshow(tiffs[0],aspect='auto')
# plt.show()


images = [np.rot90(t[m[0]-n:m[0]+n,m[1]-N:m[1]+N]) for t, m in zip(tiffs,mid)]
profiles = [i.mean(0) for i in images] #[t[m[0]-n:m[0]+n,m[1]-N:m[1]+N] for t, m in zip(tiffs,mid)]
xP = [np.linspace(-N*r[0], N*r[0],2*N) for r in res]
yP = [np.linspace(-n*r[1], n*r[1],2*n) for r in res]

# maskImage = tifffile.imread(maskFile)
# print(np.shape(maskImage))

print(np.shape(images))
plt.imshow(images[0],aspect='auto')
plt.show()
plt.plot(images[0][:,n])
plt.vlines(np.shape(images[0])[0]//2,0,1.3e11)
plt.show()
# plt.imshow(maskImage)
# plt.show()

image = images[0]
res = res[0]
print(res)

# # PARAMETERS FORL LARGE CLENGTH MASKS
X = np.shape(image)[1]# for i in images]
Y = np.shape(image)[0]# for i in images]
# res = 1.25e-9
# midX, midY = np.shape(maskImage)[1]/2, np.shape(maskImage)[0]/2 
pitch = pitch / res[0] #pixels
hp = pitch/2
print(hp)

numlines = int(Y/hp) - 2  #99 #int(Y//hp-2)# 125
shiftY = 0
extraY = 10

# print(midX, midY)

gratingImage = images[0] #[int(mid[ - (Y/2)):int(midY + (Y/2)), int(midX - (X/2)):int(midX + (X/2))]
#maskImage[1000:5000,6500:10500]

plt.imshow(gratingImage,cmap='gray',aspect='auto')#,extent=[res*(Y[0]//2)*1e6,res*(Y[0]//2)*1e6,res*(X[0]//2)*1e6,res*(X[0]//2)*1e6])
plt.xlabel('$x$ [\u03bcm]')
plt.ylabel('$y$ [\u03bcm]')
# plt.colorbar()
plt.show()

save2pick = True

FR = []
FP = []
LER = []
for i,a in enumerate(images):
    print('#', i+1)
    p, f = [],[]
    ler = []
    # print(np.shape(a))
    # print(np.shape(images))
    for n in range(numlines):
        
        # print('\n Analysing line ', n+1, ' of ', numlines)
        
        lineImage = a[int(shiftY + n*hp):int(shiftY + hp//2 + extraY + n*hp),:]
        if lineImage[0,0] != 0:
            lineImage = abs(255 - lineImage)
        # if (n % 2) == 0:        
        #     lineImage = gratingImage[int(shiftY + n*hp):int(shiftY + hp//2 + n*hp),:]
        #     lineImage = abs(255 - lineImage)
        # else:
        #     lineImage = gratingImage[int(shiftY + n*hp):int(shiftY + hp//2 + n*hp),:]
        
        # lineImage = gratingImage[int(1980 - hp//2):int(1980 + hp//2),:]
    
        # plt.imshow(lineImage,aspect='auto')
        # plt.show()
    
        Lbox = X*res[1]
        # print(Lbox)
        fmin = 1 / (2*np.pi*Lbox)
        smax =  1 / fmin
    
        # print("minimum frequency sampled: ", fmin/1e6, ' /um')
        # print("maximum feature size sampled: ", smax*1e6, ' um')
    
        _LER = edge_roughness()
        if n == 0 or n == numlines-1:
            plt.imshow(lineImage,aspect='auto',cmap='gray')#,extent=[res*((-hp//2 + extraY)/2)*1e9,res*((hp//2 + extraY)/2)*1e9,res*(-midX)*1e6,res*midX*1e6])
            plt.xlabel('$x$ [\u03bcm]')
            plt.ylabel('$y$ [nm]')
            plt.show()
            
            (Xcln, Ycln, freq, FourierPow) = _LER.LER_analysis(lineImage, [res[1],res[0]], 10,show=True) #image, image width (m), threshold for outliers
            # plt.plot([x*1e6 for x in Xcln[4000:6000]], [y*1e9 for y in Ycln[4000:6000]],'black', label='rough edge')
            # plt.hlines(0, np.min(Xcln[4000:6000])*1e6, np.max(Xcln[4000:6000])*1e6,colors='gray',linestyles= '--', label='ideal edge')
            # plt.xlabel('x [\u03BCm]')
            # plt.ylabel('y [nm]')
            # plt.legend()
            # plt.show()
        else:
            (Xcln, Ycln, freq, FourierPow) = _LER.LER_analysis(lineImage, [res[1],res[0]], 10,show=False) #image, image width (m), threshold for outliers
        
        L = 3*np.std(np.abs(Ycln))
        
        
        # # Fit the model to the PSD data
        # popt, pcov = fit_psd(freq, FourierPow, model_PSD, p0=[1e-2, 1, 5e-9], plot_fit=True)
    
        # # Print the fitted parameters
        # print(f"Fitted parameters: PSD(0) = {popt[0]:.2f}, corr_len = {popt[1]:.2f}, rmsH = {popt[1]:.2f}")
        
        print("L    :", L)
        ler.append(L)
        f.append(freq)
        p.append(FourierPow)
    
        # plt.plot(freq,FourierPow)
        # plt.show()    


    print('Done aerial image #', i+1)
    print(np.shape(f))
    print(ler)
    f=np.mean(f,axis=0)
    p=np.mean(p,axis=0)
    ler=np.mean(ler,axis=0)
    print(np.shape(f))
    FR.append(f)
    FP.append(p)
    LER.append(ler)
    print("ler:   ", ler)

print("LER:   ", LER)
# plt.plot(Xcln, Ycln, '-')
# plt.plot(Xcln, Ycln, 'r.')
# plt.show()

# print(np.shape(freq))

if save2pick:
    with open(dirPath + 'LER__maskLER2.pkl', "wb") as f:
        pickle.dump([order,LER], f)
        


# PSD0 = np.max(p)#2.5e-25#4e-26
# H = 0.85#1.5
# c = 1000e-9#4.0e-9 #3.5e-9
# fan = np.linspace(np.min(f),np.max(f),5000) #4e5,2e9,5000)
# dx = res[1]#1.25e-9 
# N = 1000
# sigma= 1.0e-13#6.0e-12 #1.0e-12

# B = [(-np.inf,0,-np.inf),(np.inf,1,np.inf)]

# PSD = analyticalPSD_biased(f, PSD0, H, c,dx,N,sigma)

# slopeX = np.logspace(2e-2,2e-1,500)
# slopeY = np.logspace(2e-27,3e-29,500)
# slope = [s * (2*H+1) for s in slopeX]

# print([s/1e9 for s in slope])
# print(f)
# plt.plot(freq[2:100], FourierPow[2:100],'-')
LWR = []
for i,f in enumerate(FR):
    plt.plot([_f/1.0e-9 for _f in f], FP[i],'.')#, label='biased',alpha=0.2)
    ax = plt.gca()
    ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%0.0e'))
    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel('Spatial frequency (nm$^{-1}$)')
    # plt.xlabel('Feature size (nm)')
    plt.ylabel('Fourier power (au)')
    plt.ylim([2e-31,(np.max(FP[i]) + 5*np.std(FP[i]))])
    plt.title('Fourier power spectrum')
    plt.legend()
    plt.show()
    
    lwr = np.sqrt(integrate.simpson(FP[i], f))
    print('LWR from integration of PSD: ', 3*lwr)
    # print('LER error (different methods) [nm]: ', abs(3*ler - LER[i])*1e9)
    # print(((LER[i] + (3*ler))/2)*1e9)
    LWR.append(3*lwr)
    

plt.plot(order,[l*1e9 for l in LER],label='LER')
plt.plot(order,[l*1e9 for l in LWR],label='LWR')
plt.xlabel('batch number')
plt.ylabel('[nm]')
plt.legend()
plt.show()
# plt.plot([_f/1.0e9 for _f in f[1:1000]], p[1:1000],'.')
# plt.plot([1/f for f in freq[0:100]], FourierPow[0:100],'-')
ax = plt.gca()
ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%0.0e'))
plt.yscale('log')
plt.xscale('log')
# plt.xaxis.set_minor_formatter(ticker.ScalarFormatter())
# plt.ticklabel_format(style='plain', axis='x')
plt.xlabel('Spatial frequency (nm$^{-1}$)')
# plt.xlabel('Feature size (nm)')
plt.ylabel('Fourier power (au)')
# plt.ylim([np.min(p),(np.max(p) + np.std(p))])
plt.title('Fourier power spectrum')
# plt.show() 

# p_ub = [P - (sigma**2)*(dx*N) for P in p]

# plt.plot([_f/1.0e9 for _f in f], p_ub,'.', label='unbiased',alpha=0.2)
# plt.plot([_f/1e9 for _f in fan[0:len(PSD)]],PSD,'black', label='analytic')

# #cv2.imshow('Origional Image',image)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

plt.legend()
plt.show()


popt, pcov = fit_psd(f,p_ub,analyticalPSD_unbiased,p0=[PSD0,H,c],bounds = B,plot_fit=True)
# set limits for fitted variables - H

PSD0, H, lc = popt
print('PSD(0):    ', popt[0])
print('H:         ', popt[1])
print('lc:        ', popt[2])
print('f(0)       ',f[0] )
print('1/f(0)       ',1/f[0] )
# print(popt)
# print(pcov)



# lc = 10.0e-9

per = 1 - ((2/np.pi) * np.arctan(lc/(X*res)))

ler = np.sqrt(integrate.simpson(p, f))
print('LER from integration of PSD: ', 3*ler)
print('LER from standard deviation: ', LER)
print('LER error (PSD) [nm]: ', (1-per)*3*ler*1e9)
print('LER error (different methods) [nm]: ', abs(3*ler - LER)*1e9)
print(((LER + (3*ler))/2)*1e9)
# print('computed AUC using sklearn.metrics.auc: {}'.format(3*np.sqrt(auc(f,p))))



# [3.0,6.6,10.4,14.3,18.2,22.0,25.7,29.0]
# 20000020.00000_0.50000_10.00000_mask = 3.00 +/- 0.005 nm LER
# 20000020.00000_1.00000_10.00000_mask = 6.60 +/- 0.004 nm LER
# 20000020.00000_1.50000_10.00000_mask = 10.4 +/- 0.007 nm LER
# 20000020.00000_2.00000_10.00000_mask = 14.3 +/- 0.009 nm LER
# 20000020.00000_2.50000_10.00000_mask = 18.2 +/- 0.01 nm LER
# 20000020.00000_3.00000_10.00000_mask = 22.0 +/- 0.01 nm LER
# 20000020.00000_3.50000_10.00000_mask = 25.7 +/- 0.02 nm LER
# 20000020.00000_4.00000_10.00000_mask = 29.0 +/- 0.1 nm LER
