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
    if isinstance(maskFile,str):
        print('\n ', maskFile)
        maskImage = tifffile.imread(maskFile)
    else:
        maskImage = maskFile
    
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
    # plt.imshow(gratingImage[1000:1000 + view,:],cmap='gray',aspect='auto')#,extent=[res*(-500)*1e6,res*500*1e6,res*(-500)*1e6,res*500*1e6])
    plt.imshow(gratingImage,cmap='gray',aspect='auto')#,extent=[res*(-500)*1e6,res*500*1e6,res*(-500)*1e6,res*500*1e6])
    plt.xlabel('$x$ [pix]')#'[\u03bcm]')
    plt.ylabel('$y$ [pix]')#[\u03bcm]')
    plt.title('Input grating')
    plt.colorbar()
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
        plt.colorbar()
        plt.show()
        
        midX, midY = np.shape(gratingImage)[1]/2, np.shape(gratingImage)[0]/2 #5245#(3*np.shape(maskImage)[0])/17
        pitch = 50.0e-9 / wavefront_res[0] #pixels
        hp = pitch/2
        
        X = np.shape(gratingImage)[1]
        Y = np.shape(gratingImage)[0]
        
        numlines = Y#int(Y//pitch-5) # 125
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
    for n in range(numlines):
        
        if resample:
            Xcln = np.linspace(0, X*wavefront_res[1], X) 
            Lbox = wavefront_res[1]*X
        else:
            Xcln = np.linspace(0, X*res, X) 
            Lbox = X*res
        fmin = 1 / (2*np.pi*Lbox)
        smax =  1 / fmin
    
        if n==0:
            print('Analysing ', numlines, ' lines ...')
            print("minimum frequency sampled: ", fmin, ' /m')
            print("maximum feature size sampled: ", smax, ' m')
        # print('\n Analysing line ', n+1, ' of ', numlines)
        
        lineImage = gratingImage[n,:]#int(shift + n*hp):int(shift + hp//2 + extra + n*hp),:]
        Ycln = lineImage
        if lineImage[len(lineImage)//2] == 0:
            print('\n skipping...')
            pass
        else:
            print('\n not skipping')
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
        
            _LER = edge_roughness()
            if n== 0 or n == numlines-1:
                if resample:
                    plt.plot([h*1e6 for h in Xcln],[h*1e9 for h in lineImage],':x')#,aspect='auto',cmap='gray',extent=[wavefront_res[1]*(-midX)*1e6,
                    # plt.show()                    #                                   wavefront_res[1]*midX*1e6,
                                         #                                  -wavefront_res[0]*((hp//2 + extra)/2)*1e9,
                                          #                                 wavefront_res[0]*((hp//2 + extra)/2)*1e9])
                else:
                    plt.plot([h*1e6 for h in Xcln],[h*1e9 for h in lineImage],':x')#,aspect='auto',cmap='gray',extent=[wavefront_res[1]*(-midX)*1e6,
                    # plt.show()                                                       # wavefront_res[1]*midX*1e6,
                                                                           # -wavefront_res[0]*((hp//2 + extra)/2)*1e9,
                                                                           # wavefront_res[0]*((hp//2 + extra)/2)*1e9])
                plt.xlabel('$x$ [\u03bcm]')
                plt.ylabel('$H$ [nm]')
                plt.show()
                
                # print('Length of lineImage:   ', len(lineImage))
                if resample:
                    # Xcln = np.linspace(0, X, X) 
                    # (Xcln,_Ycln) = _LER.extract_clean(Xcln, Ycln, 10)
                    # Ycln = [y*wavefront_res[0] for y in Ycln]
                    # Xcln = [x*res[0] for x in Xcln]
                    freq, FourierPow = _LER.fourier_power(Xcln, Ycln)
                    # (Xcln, Ycln, freq, FourierPow) = _LER.LER_analysis(lineImage, [wavefront_res[1],wavefront_res[0]], 10,show=True) #image, image width (m), threshold for outliers
                else:
                    # Xcln = np.linspace(0, X, X) 
                    # (Xcln,_Ycln) = _LER.extract_clean(Xcln, Ycln, 10)
                    # Ycln = [y*res for y in Ycln]
                    # Xcln = [x*res[0] for x in Xcln]
                    freq, FourierPow = _LER.fourier_power(Xcln, Ycln)
                    # (Xcln, Ycln, freq, FourierPow) = _LER.LER_analysis(lineImage, [res,res], 10,show=True) #image, image width (m), threshold for outliers
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
                    # (Xcln,_Ycln) = _LER.extract_clean(Xcln, Ycln, 10)
                    # Ycln = [y*wavefront_res[0] for y in Ycln]
                    # Xcln = [x*res[0] for x in Xcln]
                    freq, FourierPow = _LER.fourier_power(Xcln, Ycln)
                    # (Xcln, Ycln, freq, FourierPow) = _LER.LER_analysis(lineImage, [wavefront_res[1],wavefront_res[0]], 10,show=False) #image, image width (m), threshold for outliers
                else:
                    # (Xcln,_Ycln) = _LER.extract_clean(Xcln, Ycln, 10)
                    # Ycln = [y*res for y in Ycln]
                    # Xcln = [x*res[0] for x in Xcln]
                    freq, FourierPow = _LER.fourier_power(Xcln, Ycln)
                    # (Xcln, Ycln, freq, FourierPow) = _LER.LER_analysis(lineImage, [res,res], 10,show=False) #image, image width (m), threshold for outliers
            
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
    # [x for xs in f for x in xs] #np.mean(f,axis=0)
    p=np.mean(p,axis=0)
    # [x for xs in p for x in xs] #np.mean(p,axis=0)
    # f = np.squeeze(flatten(f))
    # p = np.squeeze(flatten(p))
    LER=np.mean(LER,axis=0)
    print(np.shape(f))
    
    # plt.plot(Xcln, Ycln, '-')
    # plt.plot(Xcln, Ycln, 'r.')
    # plt.show()
    
    # print(np.shape(freq))
            
    import math
    PSD0 = np.max(p[1::])# - (0.1 * 10**(math.floor(math.log(np.max(p[1::]), 10)))) #2.5e-25#4e-26
    H = 0.5#1.5
    c = 10.0e-9#4.0e-9 #3.5e-9
    fan = np.linspace(np.min(f),np.max(f),5000) #4e5,2e9,5000)
    if resample:
        dx = wavefront_res[1]    
    else:
        dx = res
    N = len(Ycln)
    sigma= np.min(p[1::]) #3.0e-12#6.0e-12 #1.0e-12
    
    B = None#[(-np.inf,0,-np.inf),(np.inf,1,np.inf)]
    B_b = None#((-np.inf, 0, 1e-10,1e-14), (np.inf, 1, 5e-7,4e-12))
    
    print('min f: ', np.min(f[1::]))
    print('max f: ', np.max(f[1::]))
    print('\n')
    
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
    elif H<=0.0:
        H = 1.0
        
    print('-----GUESS-----')
    print('PSD(0):    ', PSD0)
    print('H:         ', H)
    print('lc:        ', c)
    
    
    # B =[(PSD0 - PSD0*0.2, 0.1, c - c*0.4), (PSD0 + PSD0*0.2,1.0, c + c*0.4)] #None#[(PSD0*0.1, 0.1, c*0.1), (PSD0*2,1.0, c*10)]
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
    C = [2,2,2,2,2,4,4,4,4,4,6,6,6,6,6,8,8,8,8,8,10,10,10,10,10] # for D=27.5um
    # for D=50um # [10,10,10,10,10,2,2,2,2,2,4,4,4,4,4,6,6,6,6,6,8,8,8,8,8]#,2,4,6,8,10,2,4,6,8,10,2,4,6,8,10,2,4,6,8,10]
    R = [0.5,1.0,1.5,2.0,2.5,0.5,1.0,1.5,2.0,2.5,0.5,1.0,1.5,2.0,2.5,0.5,1.0,1.5,2.0,2.5,0.5,1.0,1.5,2.0,2.5]
    maskFiles =  ['/user/home/opt_old/xl/xl/experiments/masks2/T20nm_' + str(r) + '0000_' + str(c) + '.00000_2.50000_mask.tif' for r,c in zip(R,C)]
    # ['/user/home/opt_old/xl/xl/experiments/masks2/T20nm_' + str(r) + '0000_' + str(c) + '.00000_2.50000_mask.tif' for r,c in zip(R,C)]
    # ['/user/home/opt_old/xl/xl/experiments/masks3/T20nmD50um_' + str(r) + '0000_' + str(c) + '.00000_2.50000_mask.tif' for r,c in zip(R,C)]

    # print(maskFiles)
    # # PARAMETERS FOR surface roughness MASKS
    res = 2.5e-9 #1.25e-9
    pitch = 100.0e-9 #/ res #pixels
    hp = pitch/2
    
    shift = 2
    extra = 8 #15
    
    resample = True
    wavefront_res = (2.4986871083329154e-09, 2.1250955712885965e-07)

    # # D = 27.5um
    T = [2.353025172753083e-08,2.711203540498752e-08,3.143555894358832e-08,3.43265214949001e-08,3.740484237754313e-08,
          2.5165243262078253e-08,2.982752438924402e-08,3.461563925111531e-08,3.980449151532665e-08,4.477405736696371e-08,
          2.570380869572296e-08,3.214626222713788e-08,3.781150624199349e-08,4.580818777871269e-08,5.730477843158091e-08,
          2.6381095642257078e-08,3.372621369976859e-08,4.032381962768946e-08,4.640668525021293e-08,5.5695834865905164e-08,
          2.7597255910327376e-08,3.5203732338319117e-08,4.070122941780699e-08,5.0885101918369736e-08,5.955319433439844e-08,
        ]

    # D = 50um
    # T = [3.1624984448274474e-08,4.120929414659666e-08,5.495651140086134e-08,6.238086808841623e-08,7.549334307909943e-08,
    #       2.5158832253821112e-08,3.1185203993627854e-08,3.569295568488225e-08,4.093164752329961e-08,4.576600910009207e-08,
    #       2.778655875679539e-08,3.465840510240802e-08,4.161564046436785e-08,4.9866622351879454e-08,5.6149080393061895e-08,
    #       2.9096134271561907e-08,3.711672551791956e-08,4.536449188314153e-08,5.3873843163008244e-08,6.562202051827108e-08,
    #       3.0246431835542476e-08,4.02504706590283e-08,4.8512203510216304e-08,6.12897201488435e-08,6.923863685200453e-08]

    AMP, CL = [],[]    
    
    nx = 8000 # was 1500
    ny = 3000 # was 1500
    for i,m in enumerate(maskFiles):
        m = tifffile.imread(m) #np.rot90(tifffile.imread(m))
        plt.imshow(m)
        plt.show()
        print(np.shape(m))
        # m = m[np.shape(m)[0]//2 - 2000:np.shape(m)[0]//2 + 2000, np.shape(m)[1]//4 - 2000: np.shape(m)[1]//4 + 2000]
        m = m[np.shape(m)[0]//2 - ny:np.shape(m)[0]//2 + ny, np.shape(m)[1]//2 - nx: np.shape(m)[1]//2 + nx]#8000: np.shape(m)[1]//2 + 8000]
        # print(m)
        # plt.imshow(tifffile.imread(m))
        
        m = (m / np.max(m))*T[i]
        plt.imshow(m)
        plt.title('#' + str(i+1) + ': rms = ' + str(R[i]) + ' , clen = ' + str(C[i]))
        plt.colorbar()
        plt.show()
        
        
        amp, clen = maskLER(m,res,pitch,shift,extra,resample,wavefront_res)
    
        print('amp, clen:   ', amp, clen)
        AMP.append(amp)
        CL.append(clen)
    
    print('\n')
    print("AMP: ", AMP)
    print("CLEN: ", CL)
    
if __name__ == '__main__':
    test()
    # D = 27.5um
    AMP =  [
            # 2.035644886033035e-09, 4.0592196419614256e-09, 6.259875893638754e-09, 8.165842731590213e-09, 1.005550394063775e-08,
            # 2.895891162226716e-09, 5.847577561399199e-09, 8.778032847483112e-09, 1.1699667680053021e-08, 1.4636838480173525e-08, 
            # 3.4795549101231095e-09, 7.158433946055489e-09, 1.0902511792838049e-08, 1.4859620681935107e-08, 2.0972428694532717e-08, 
            4.122383897937525e-09, 8.117243390986007e-09, 1.2378726882139275e-08, 1.5545363813399494e-08, 2.140272219445471e-08, 
            4.53143622324516e-09, 9.473176992309738e-09, 1.3107525529334544e-08, 1.874120283733922e-08, 2.4337685465020497e-08]
    CLEN =  [
              # 1.9492903164991375e-10, 1.0533974279854767e-11, 6.765078485638228e-08, 6.7636342531154e-08, 6.772480934621956e-08, 
              # 6.76463212115712e-08, -2.479203455242585e-12, 6.765295512602593e-08, 6.764555177677725e-08, 6.76559165613844e-08,
              # 6.768035170486639e-08, 6.765474850579635e-08, 6.763807821930271e-08, 6.764496291159346e-08, 6.763945079407378e-08, 
              4.851911527058721e-08, 4.586465226159821e-08, 4.7413248203547776e-08, 4.809827540880266e-08, 4.5659646183619133e-08, 
              8.23561729162167e-08, 8.301111333484316e-08, 8.395692546022407e-08, 8.241197303928809e-08, 8.347488695429966e-08]
    
    #  D = 50um
    AMP =  [
                6.8889689179059445e-09, 1.3400953970250496e-08, 2.202831693380266e-08, 2.7644289763994316e-08, 3.6324436448930706e-08, 
              # 3.0073867697639402e-09, 6.296005890044727e-09, 8.982722729496e-09, 1.2004551131234126e-08, 1.6165342676274536e-08, 
              # 4.338956832803301e-09, 8.537279399440092e-09, 1.3083383697754931e-08, 1.7053875122472303e-08, 2.1122520493483343e-08, 
                5.400637841032609e-09, 1.0442686402609964e-08, 1.6816348605215538e-08, 2.1120604302173793e-08, 2.8427394626983363e-08, 
                5.9460811114356315e-09, 1.2464290221512782e-08, 1.8052265234725105e-08, 2.6852983029836686e-08, 2.9883960734215946e-08]
    CLEN =  [
                1.45e-07, 1.45e-07, 1.4113238388997165e-07, 1.458112315311206e-07, 1.45e-07, 
                # 2.418738811905356e-10, 2.450856499875283e-24, 3.700368381621219e-16, 6.764071171304971e-08, 6.76461436308354e-08, 
                # 6.765927212275439e-08, 6.762897914412015e-08, 6.763731551481169e-08, 6.763387112926504e-08, 6.761448124323488e-08, 
                6.237392279627136e-08, 6.229515239853539e-08, 6.577324420245618e-08, 6.552486666175774e-08, 6.308329380743707e-08, 
                1.0836686312746431e-07, 1.1323662320408521e-07, 1.100761427873787e-07, 1.1411125762677376e-07, 1.0981862221098018e-07]
    
