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
from sklearn.metrics import auc

# plt.rcParams["figure.figsize"] = (2,3)

from scipy.optimize import curve_fit
from scipy.signal import find_peaks

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
    # if model_function == analyticalPSD_biased:
    #     PSD0,H,c,sigma = p0
    #     guess = model_function(frequencies,PSD0,H,c,sigma)
    # elif model_function == analyticalPSD_unbiased:
    #     PSD0,H,c = p0
    #     guess = model_function(frequencies,PSD0,H,c)
    
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


dirPath =  '/user/home/opt/xl/xl/experiments/maskLER_retry2/data/'
cY = [1000,1000,1000,1000,900,900,900,700,700,700,600,600,600]
sigma = [140,120,100,80,70,60,40,70,60,40,70,60,40]
order = ['c' + str(c) + 'a' + str(s) for c,s in zip(cY,sigma)]
files = [str(o) + '/' + str(o) + '.pkl' for o in order]
# labels =  ['1000 nm'
# ['\u03C3 = 0.0 nm ','\u03C3 = 3.0 nm ','\u03C3 = 4.0 nm ','\u03C3 = 5.0 nm','\u03C3 = 6.0 nm']#,'\u03C3 = 3.0 nm','\u03C3 = 3.5 nm','\u03C3 = 4.0 nm']
# ['\u03C3 = 6.0 nm']#['\u03C3 = 0.0 nm ','\u03C3 = 3.0 nm ','\u03C3 = 4.0 nm ','\u03C3 = 5.0 nm','\u03C3 = 6.0 nm']#,'\u03C3 = 3.0 nm','\u03C3 = 3.5 nm','\u03C3 = 4.0 nm']

C = 60.0e-9
save2pick = True

N = 2250 //2                         # number of pixels to take for line profile  - 1200 for roughness aerial images
n = 250  //2                            # number of pixels to average over for line profile - 15 for roughness aerial images
plotRange = 1000                       # range of aerial image plot in nm

#middle pixels of images
mid = np.full((np.shape(files)[0],2), (460, 8000))

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
profiles = [i.mean(1) for i in images] #[t[m[0]-n:m[0]+n,m[1]-N:m[1]+N] for t, m in zip(tiffs,mid)]
xP = [np.linspace(-N*r[0], N*r[0],2*N) for r in res]
yP = [np.linspace(-n*r[1], n*r[1],2*n) for r in res]

# maskImage = tifffile.imread(maskFile)
# print(np.shape(maskImage))

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

numlines = (int(Y/hp) - 1) // 2  #99 #int(Y//hp-2)# 125
shiftY = 10
extraY = hp / 3

peaks, properties = find_peaks(profiles[0],distance=pitch-5)
troughs, properties = find_peaks(1 - profiles[0]/np.max(profiles[0]),distance=pitch-18)

if troughs[0] <= peaks[0]:
    troughs=troughs[1::]

print(np.shape(images))
plt.imshow(images[0],aspect='auto')
plt.show()
# plt.plot(profiles[0])
# plt.plot(peaks,profiles[0][peaks], 'x')
# plt.plot(troughs,profiles[0][troughs], 'x')
# plt.vlines(np.shape(images[0])[0]//2,0,np.max(images[0])*0.75,colors='r')
# plt.show()
# plt.imshow(maskImage)
# plt.show()

# print(midX, midY)

gratingImage = images[0] #[int(mid[ - (Y/2)):int(midY + (Y/2)), int(midX - (X/2)):int(midX + (X/2))]
#maskImage[1000:5000,6500:10500]
# [0:500,:]
# plt.imshow(gratingImage,cmap='gray',aspect='auto')#,extent=[res*(Y[0]//2)*1e6,res*(Y[0]//2)*1e6,res*(X[0]//2)*1e6,res*(X[0]//2)*1e6])
# for n in range(numlines):
#     plt.hlines(int(shiftY + n*hp),xmin=0,xmax=X,linestyles='--',colors='r')
#     plt.hlines(int(shiftY + hp//2 + extraY + n*hp),xmin=0,xmax=X,linestyles='--',colors='g')
#     if n %11 == 0:
#         print('\n here')
#         print(n)
#         shiftY += 1
#         print(shiftY)
# plt.xlabel('$x$ [\u03bcm]')
# plt.ylabel('$y$ [\u03bcm]')
# plt.xlim([100,150])
# plt.ylim([1000,1250])
# # plt.colorbar()
# plt.show()

FR = []
FP = []
LER = []
LERe = []
C = []
pLER = []
aLER = []
for i,a in enumerate(images):
    print('#', i+1)
    print(np.max(a))
    p, f = [],[]
    ler = []
    # print(np.shape(a))
    # print(np.shape(images))
    
    peaks, properties = find_peaks(profiles[i],distance=pitch-18)
    troughs, properties = find_peaks(1 - profiles[i]/np.max(profiles[i]),distance=pitch-18)
    
    if troughs[0] <= peaks[0]:
        troughs=troughs[1::]
        
        
    plt.plot(profiles[i])
    plt.plot(peaks,profiles[i][peaks], 'x')
    plt.plot(troughs,profiles[i][troughs], 'x')
    plt.show()

    for n in range(numlines):
        
        print('\n Analysing line ', n+1, ' of ', numlines)
        
        
        
        # if n+1 < numlines:
        lineImage1 = a[int(peaks[n]-extraY):int(troughs[n]+extraY),:].copy()
        lineImage2 = np.flipud(a[int(troughs[n]-extraY):int(peaks[n+1]+extraY),:].copy())
        # else:
        #     lineImage1 = a[peaks[n]:troughs[n],:]
        #     lineImage2 = a[troughs[n]::,:]
        
        # lineImage1[-1,:] = 0
        # lineImage2[-1,:] = 0 #np.max(lineImage2)
        
        
        # lineImage = a[int(shiftY + n*hp):int(shiftY + hp//2 + extraY + n*hp),:]
        # if lineImage[0,0] != np.min(lineImage) or lineImage[0,1] != np.min(lineImage) or lineImage[0,2] != np.min(lineImage):
        #     # print('inverting line # ', n)
        #     lineImage = abs(255 - lineImage)
        # if (n % 2) == 0:        
        #     lineImage = gratingImage[int(shiftY + n*hp):int(shiftY + hp//2 + n*hp),:]
        #     lineImage = abs(255 - lineImage)
        # else:
        #     lineImage = gratingImage[int(shiftY + n*hp):int(shiftY + hp//2 + n*hp),:]
        
        # lineImage = gratingImage[int(1980 - hp//2):int(1980 + hp//2),:]
    
        # plt.imshow(lineImage1,aspect='auto')
        # plt.show()
        # plt.imshow(lineImage2,aspect='auto')
        # plt.show()
    
        Lbox = X*res[1]
        # print(Lbox)
        fmin = 1 / (2*np.pi*Lbox)
        smax =  1 / fmin
    
        # print("minimum frequency sampled: ", fmin/1e6, ' /um')
        # print("maximum feature size sampled: ", smax*1e6, ' um')
    
        _LER = edge_roughness()
        if n == 0 or n == numlines-1:
            plt.imshow(lineImage1,aspect='auto',cmap='gray')#,extent=[res*((-hp//2 + extraY)/2)*1e9,res*((hp//2 + extraY)/2)*1e9,res*(-midX)*1e6,res*midX*1e6])
            plt.xlabel('$x$ [\u03bcm]')
            plt.ylabel('$y$ [nm]')
            plt.show()
            
            plt.imshow(lineImage2,aspect='auto',cmap='gray')#,extent=[res*((-hp//2 + extraY)/2)*1e9,res*((hp//2 + extraY)/2)*1e9,res*(-midX)*1e6,res*midX*1e6])
            plt.xlabel('$x$ [\u03bcm]')
            plt.ylabel('$y$ [nm]')
            plt.show()
            
            (Xcln1, Ycln1, freq1, FourierPow1) = _LER.LER_analysis(lineImage1, [res[1],res[0]], 10,show=True, extra=extraY) #image, image width (m), threshold for outliers
            
            (Xcln2, Ycln2, freq2, FourierPow2) = _LER.LER_analysis(lineImage2, [res[1],res[0]], 10,show=True, extra=extraY)
            # plt.plot([x*1e6 for x in Xcln[4000:6000]], [y*1e9 for y in Ycln[4000:6000]],'black', label='rough edge')
            # plt.hlines(0, np.min(Xcln[4000:6000])*1e6, np.max(Xcln[4000:6000])*1e6,colors='gray',linestyles= '--', label='ideal edge')
            # plt.xlabel('x [\u03BCm]')
            # plt.ylabel('y [nm]')
            # plt.legend()
            # plt.show()
        else:
            (Xcln1, Ycln1, freq1, FourierPow1) = _LER.LER_analysis(lineImage1, [res[1],res[0]], 10,show=False, extra=extraY)
            (Xcln2, Ycln2, freq2, FourierPow2) = _LER.LER_analysis(lineImage2, [res[1],res[0]], 10,show=False, extra=extraY) #image, image width (m), threshold for outliers
        
        L1 = 3*np.std(np.abs(Ycln1))
        L2 = 3*np.std(np.abs(Ycln2))
        
        
        # # Fit the model to the PSD data
        # popt, pcov = fit_psd(freq, FourierPow, model_PSD, p0=[1e-2, 1, 5e-9], plot_fit=True)
    
        # # Print the fitted parameters
        # print(f"Fitted parameters: PSD(0) = {popt[0]:.2f}, corr_len = {popt[1]:.2f}, rmsH = {popt[1]:.2f}")
        
        print("L    :", L1)
        ler.append(L1)
        f.append(freq1)
        p.append(FourierPow1)
        ler.append(L2)
        f.append(freq2)
        p.append(FourierPow2)
    
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

    import math
    PSD0 = np.max(p[1::]) - (0.1 * 10**(math.floor(math.log(np.max(p[1::]), 10)))) #2.5e-25#4e-26
    H = 0.6 #1.5
    c = 40.0e-9 #C #102.0e-9#5.68e-8#4.0e-9 #3.5e-9
    fan = np.linspace(np.min(f),np.max(f),5000) #4e5,2e9,5000)
    N = len(Ycln1)
    sigma= 2e-11#(np.max(p[1::]) - np.min(p)) #6.0e-12 #1.0e-12
    
    B_b = None#((PSD0*0.2, 0.3, c*0.4 ,0.0), (PSD0*2,0.8, c*4,sigma*5))
    
    
    print('-----GUESS-----')
    print('PSD(0):    ', PSD0)
    print('H:         ', H)
    print('lc:        ', c)
    # print('N:         ', N)
    print('sigma:     ', sigma)
    
    popt, pcov = fit_psd(f,p,analyticalPSD_biased,p0=[PSD0,H,c,sigma],bounds=B_b,plot_fit=True)#plot_fit=True)#,bounds=B_b,plot_fit=True)
    
    PSD0, H, c, sigma = popt
    PSD = analyticalPSD_biased(f, PSD0, H, c,sigma)
    
    B =None #[(-np.inf,0,-np.inf),(np.inf,1,np.inf)] #None#[(PSD0*0.1, 0.1, c*0.1), (PSD0*2,1.0, c*10)]
    
    print('-----BIASED FIT-----')
    print('PSD(0):    ', PSD0)
    print('H:         ', H)
    print('lc:        ', c)
    # print('N:         ', N)
    print('sigma:     ', sigma)
    
    plt.plot([_f/1.0e9 for _f in f[1::]], p[1::],'.', label='biased',alpha=0.2)
    ax = plt.gca()
    ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%0.0e'))
    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel('Spatial frequency (nm$^{-1}$)')
    plt.ylabel('Fourier power (au)')
    plt.title('Fourier power spectrum')
    
    print(sigma)
    print(res)
    print(N)
    dx = res[1]
    p_ub = [P - (sigma**2)*(dx*N) for P in p]
    
    plt.plot([_f/1.0e9 for _f in f[1::]], p_ub[1::],'.', label='unbiased',alpha=0.2)
    plt.plot([_f/1e9 for _f in f[1:len(PSD)]],PSD[1::],'black', label='analytic')
    plt.legend()
    plt.show()
    
    if H>=1.0:
        H = 1.0

    print('-----GUESS-----')
    print('PSD(0):    ', PSD0)
    print('H:         ', H)
    print('lc:        ', c)
    
    B =[(PSD0 - PSD0*0.2, 0.1, c - c*0.4), (PSD0 + PSD0*0.2,1.0, c + c*0.4)] #None#[(PSD0*0.1, 0.1, c*0.1), (PSD0*2,1.0, c*10)]
    p_ub = np.array(p_ub)
    popt, pcov = fit_psd(f,p_ub,analyticalPSD_unbiased,p0=[PSD0,H,c],bounds = B,plot_fit=True)
    # set limits for fitted variables - H
    
    PSD0, H, lc = popt
    print('-----UNBIASED FIT-----')
    print('PSD(0):    ', popt[0])
    print('H:         ', popt[1])
    print('lc:        ', popt[2])
    print('f(0)       ',f[0] )
    print('1/f(0)       ',1/f[0] )
    # print(popt)
    # print(pcov)
    
    
    per = 1 - ((2/np.pi) * np.arctan(lc/(X*dx)))
    
    ler = np.sqrt(integrate.simpson(p, f))
    lere =  abs(3*ler - LER[i])# #abs(3*ler - LER[i])#(1-per)*3*ler
    print('LER from integration of PSD: ', 3*ler)
    print('LER from standard deviation: ', LER[i])
    print('LER error (PSD) [nm]: ', (1-per)*3*ler*1e9)
    print('LER error (different methods) [nm]: ', abs(3*ler - LER[i])*1e9)
    print(((LER[i] + (3*ler))/2)*1e9)
    C.append(popt[2])
    LERe.append(lere)
    pLER.append(ler*3)
    aLER.append((LER[i] + (3*ler))/2)
    # print('computed AUC using sklearn.metrics.auc: {}'.format(3*np.sqrt(auc(f,p))))

print("LER:   ", LER)
print("Clen:  ", C)



plt.errorbar(order,aLER,[l/2 for l in LERe],fmt='x')
# plt.plot(order,LER,'x')
# plt.plot(order,pLER,'x')
plt.xlabel('sigma [nm]')
plt.ylabel('Aerial image LER amplitude')
plt.show()
plt.plot(order,C,'x')
plt.xlabel('sigma [nm]')
plt.ylabel('Aerial image LER C length')
plt.show()
# plt.plot(Xcln, Ycln, '-')
# plt.plot(Xcln, Ycln, 'r.')
# plt.show()

# print(np.shape(freq))

if save2pick:
    with open(dirPath + 'LER__maskLER_retry_largeClen.pkl', "wb") as f:
        pickle.dump([order,LER,aLER,LERe,C], f)
