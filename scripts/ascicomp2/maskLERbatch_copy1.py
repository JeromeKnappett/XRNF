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

plt.rcParams["figure.figsize"] = (6,4)

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


def maskLER(maskFile,res,pitch,shift,extra,resample,wavefront_res):
    maskImage = tifffile.imread(maskFile)
    
    X = np.shape(maskImage)[1]-10
    Y = np.shape(maskImage)[0]-10
    print(np.shape(maskImage))
    midX, midY = np.shape(maskImage)[1]/2, np.shape(maskImage)[0]/2 
    
    # plt.imshow(maskImage)
    # plt.show()
    hp = pitch/2
    numlines = int(Y//(hp/res)-2)# 125
    
    print(midX, midY)
    
    view = 250
    
    gratingImage = maskImage[int(midY - (Y/2)):int(midY + (Y/2)), int(midX - (X/2)):int(midX + (X/2))]
    #maskImage[1000:5000,6500:10500]
    # gratingImage[1000:2000,1000:2000]
    plt.imshow(gratingImage[1000:1000 + view,:],cmap='gray',aspect='auto')#,extent=[res*(-500)*1e6,res*500*1e6,res*(-500)*1e6,res*500*1e6])
    plt.xlabel('$x$ [pix]')#'[\u03bcm]')
    plt.ylabel('$y$ [pix]')#[\u03bcm]')
    plt.title('Input grating')
    # plt.colorbar()
    plt.show()
    
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
        pitch = 50.0e-9 / wavefront_res[0] #pixels
        hp = pitch/2
        
        X = np.shape(gratingImage)[1]
        Y = np.shape(gratingImage)[0]
        
        numlines = int(Y//pitch-5) # 125
        # numlines = 100# int(Y//hp - 10)# 125
        # shift = 10
        # extra = 15
    
    save2pick = False
    
    if save2pick:
        with open(maskFile[0:int(len(maskFile)-4)] + 'CLOSE.pkl', "wb") as f:
                    pickle.dump(gratingImage, f, protocol=2)
    
    
    #offset = hp
    
    #lineImage = gratingImage[int(2000 - hp):int(2000),:]
    
    
    f = []
    p = []
    LER = []
    for n in range(0,numlines):
        
        # print('\n Analysing line ', n+1, ' of ', numlines)
        
        lineImage = gratingImage[int(shift + n*hp):int(shift + hp//2 + extra + n*hp),:]
        if lineImage[0,0] != 0:
            
            lineImage = abs(255 - lineImage)
        # if (n % 2) == 0:        
        #     lineImage = gratingImage[int(shift + n*hp):int(shift + hp//2 + n*hp),:]
        #     lineImage = abs(255 - lineImage)
        # else:
        #     lineImage = gratingImage[int(shift + n*hp):int(shift + hp//2 + n*hp),:]
        
        # lineImage = gratingImage[int(1980 - hp//2):int(1980 + hp//2),:]
    
        # plt.imshow(lineImage,aspect='auto')
        # plt.show()
        
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
        if n== 0 or n == numlines-1:
            if resample:
                plt.imshow(lineImage,aspect='auto',cmap='gray',extent=[wavefront_res[1]*(-midX)*1e6,
                                                                       wavefront_res[1]*midX*1e6,
                                                                       -wavefront_res[0]*((hp//2 + extra)/2)*1e9,
                                                                       wavefront_res[0]*((hp//2 + extra)/2)*1e9])
            else:
                plt.imshow(lineImage,aspect='auto',cmap='gray',extent=[wavefront_res[1]*(-midX)*1e6,
                                                                       wavefront_res[1]*midX*1e6,
                                                                       -wavefront_res[0]*((hp//2 + extra)/2)*1e9,
                                                                       wavefront_res[0]*((hp//2 + extra)/2)*1e9])
            plt.xlabel('$x$ [\u03bcm]')
            plt.ylabel('$y$ [nm]')
            plt.show()
            
            # print('Length of lineImage:   ', len(lineImage))
            if resample:
                (Xcln, Ycln, freq, FourierPow) = _LER.LER_analysis(lineImage, [wavefront_res[1],wavefront_res[0]], 10,show=True) #image, image width (m), threshold for outliers
            else:
                (Xcln, Ycln, freq, FourierPow) = _LER.LER_analysis(lineImage, [res,res], 10,show=True) #image, image width (m), threshold for outliers
            # plt.plot([x*1e6 for x in Xcln[4000:6000]], [y*1e9 for y in Ycln[4000:6000]],'black', label='rough edge')
            # plt.hlines(0, np.min(Xcln[4000:6000])*1e6, np.max(Xcln[4000:6000])*1e6,colors='gray',linestyles= '--', label='ideal edge')
            # plt.xlabel('x [\u03BCm]')
            # plt.ylabel('y [nm]')
            # plt.legend()
            # plt.show()
            
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
        
        
        # # Fit the model to the PSD data
        # popt, pcov = fit_psd(freq, FourierPow, model_PSD, p0=[1e-2, 1, 5e-9], plot_fit=True)
    
        # # Print the fitted parameters
        # print(f"Fitted parameters: PSD(0) = {popt[0]:.2f}, corr_len = {popt[1]:.2f}, rmsH = {popt[1]:.2f}")
        
        LER.append(L)
        f.append(freq)
        p.append(FourierPow)
    
        # plt.plot(freq,FourierPow)
        # plt.show()    
    
    
    print(np.shape(f))
    f=np.mean(f,axis=0)
    p=np.mean(p,axis=0)
    # f = np.squeeze(flatten(f))
    # p = np.squeeze(flatten(p))
    LER=np.mean(LER,axis=0)
    print(np.shape(f))
    
    # plt.plot(Xcln, Ycln, '-')
    # plt.plot(Xcln, Ycln, 'r.')
    # plt.show()
    
    # print(np.shape(freq))
            
    import math
    PSD0 = np.max(p[1::]) - (0.1 * 10**(math.floor(math.log(np.max(p[1::]), 10)))) #2.5e-25#4e-26
    H = 0.5#1.5
    c = 5.68e-8#4.0e-9 #3.5e-9
    fan = np.linspace(np.min(f),np.max(f),5000) #4e5,2e9,5000)
    if resample:
        dx = wavefront_res[1]    
    else:
        dx = res
    print(np.min(p[1:-1]))
    N = len(Ycln)
    sigma= np.sqrt((np.min(p[1:-1]) / (dx*N))) * 1.5 #3.0e-12#6.0e-12 #1.0e-12
    
    B = [(-np.inf,0,-np.inf),(np.inf,1,np.inf)]
    B_b = None#((-np.inf, 0, 1e-10,1e-14), (np.inf, 1, 5e-7,4e-12))
    
    print('-----GUESS-----')
    print('PSD(0):    ', PSD0)
    print('H:         ', H)
    print('lc:        ', c)
    # print('N:         ', N)
    print('sigma:     ', sigma)
    
    popt, pcov = fit_psd(f,p,analyticalPSD_biased,p0=[PSD0,H,c,sigma],bounds=B_b,plot_fit=True)#plot_fit=True)#,bounds=B_b,plot_fit=True)
    
    PSD0, H, c, sigma = popt
    PSD = analyticalPSD_biased(f, PSD0, H, c,sigma)
    
    print('-----UNBIASED FIT-----')
    print('PSD(0):    ', PSD0)
    print('H:         ', H)
    print('lc:        ', c)
    # print('N:         ', N)
    print('sigma:     ', sigma)
    
    # slopeX = np.logspace(2e-2,2e-1,500)
    # slopeY = np.logspace(2e-27,3e-29,500)
    # slope = [s * (2*H+1) for s in slopeX]
    
    # print([s/1e9 for s in slope])
    # print(f)
    # plt.plot(freq[2:100], FourierPow[2:100],'-')
    plt.plot([_f/1.0e9 for _f in f[1::]], p[1::],'.', label='biased',alpha=0.2)
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
    
    p_ub = [P - (sigma**2)*(dx*N) for P in p]
    
    plt.plot([_f/1.0e9 for _f in f[1::]], p_ub[1::],'.', label='unbiased',alpha=0.2)
    plt.plot([_f/1e9 for _f in f[1:len(PSD)]],PSD[1::],'black', label='analytic')
    
    #cv2.imshow('Origional Image',image)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    
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
    print('LER from integration of PSD: ', 3*ler)
    print('LER from standard deviation: ', LER)
    print('LER error (PSD) [nm]: ', (1-per)*3*ler*1e9)
    print('LER error (different methods) [nm]: ', abs(3*ler - LER)*1e9)
    print(((LER + (3*ler))/2)*1e9)

    return LER, popt[2]

def test():
    # C = [10,20,30,40,50]
    # R = [30,40,50,60,70,80,100,150,200,250,300,350,400,450,500]

    # order = []
    # clength = []
    # sigma = []
    # for r in R:
    #     for c in C:
    #         name = str(r) + 'um_' + str(c) + '/'
            
    #         if os.path.exists(os.path.join(os.getcwd(), dirPath + name, 'IntensityDist.dat')):
    #             order.append(name)
    #             clength.append(c)
    #             sigma.append(r)
    #         else:
    #             print(name + '... not found')
    C = [10, 20, 30, 40, 50, 10, 20, 30, 40, 50, 10, 20, 30, 40, 50, 10, 20, 30, 40, 50, 10, 20, 30, 40, 50, 10, 20, 30, 40, 50, 10, 20, 30, 40, 50, 10, 20, 30, 40, 50, 10, 20, 30, 40, 50, 20, 30, 40, 50, 20, 30, 40, 50, 30, 40, 50, 30, 40, 50, 40, 50, 40, 50]
    R = [30, 30, 30, 30, 30, 40, 40, 40, 40, 40, 50, 50, 50, 50, 50, 60, 60, 60, 60, 60, 70, 70, 70, 70, 70, 80, 80, 80, 80, 80, 100, 100, 100, 100, 100, 150, 150, 150, 150, 150, 200, 200, 200, 200, 200, 250, 250, 250, 250, 300, 300, 300, 300, 350, 350, 350, 400, 400, 400, 450, 450, 500, 500]
    maskFiles =  ['/user/home/opt_old/LineEdgeRoughness_old/masks/largeCsingle_20000000.00000_' + str(c) + '.00000_' + str(r) + '.00000_mask.tif' for c,r in zip(C,R)]

    # # PARAMETERS FORL LARGE CLENGTH MASKS
    res = 0.5e-9 #1.25e-9
    pitch = 50.0e-9 #/ res #pixels
    hp = pitch/2
    
    shift = 2
    extra = 8 #15
    
    resample = True
    wavefront_res = (2.556683508550129e-09, 4.903602170748339e-09)

    AMP, CL = [],[]    
    for m in maskFiles:
        amp, clen = maskLER(m,res,pitch,shift,extra,resample,wavefront_res)
    
        print('amp, clen:   ', amp, clen)
        AMP.append(amp)
        CL.append(clen)
    
    print('\n')
    print("AMP: ", AMP)
    print("CLEN: ", CL)
    
if __name__ == '__main__':
    test()
    
