#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 15:05:32 2023

@author: -
"""
import io
import numpy as np
import matplotlib.pyplot as plt
import pickle
# from FWarbValue import twoGauss, threeGauss, fourGauss, fiveGauss, getFWatValue, gauss2D, gauss
from scipy.optimize import curve_fit
from math import log10, floor

def round_sig(x, sig=2):
    if x != 0:
        return round(x, sig-int(floor(log10(abs(x))))-1)
    else:
        return x
    
def fitMultiGauss(Iprof,dx,N,iG,known,pdev=0.2,title=None,savePath=None,no_center=False):
    """
    Parameters
    ----------
    Iprofiles :
        Array of intensity profiles (generated from prepYDSTiffs()).
    detRange : 
        Detector range [m], along axis of interference.
    iG : 
        Array of initial guess values for fit.
    known : 
        Boolean array specifying which values are known
        0=unknown
        1=known
    savePath:
        Path to save intensity plots with fits

    Returns
    -------
    vis :
        Visibility of central interference fringe.
    coherence : 
        Degree of coherence from final fit.

    """
    
    FWHMs = []
    Isums = []
    
    finalParams = []
    if N == 1:
        from FWarbValue import gauss
        paramNames = ['Amplitude', 'Central Position', 'Sigma']
        fit = gauss
    elif N == 2:
        from FWarbValue import twoGauss
        paramNames = ['Amplitude 1', 'Amplitude 2', 'Central Position', 'Sigma 1', 'Sigma 2']
        fit = twoGauss
    elif N == 3:
        from FWarbValue import threeGauss
        paramNames = ['Amplitude 1','Amplitude 2', 'Amplitude 3', 'Central Position', 'Sigma 1', 'Sigma 2', 'Sigma 3']
        fit = threeGauss
    elif N == 4:
        from FWarbValue import fourGauss
        paramNames = ['Amplitude1', 'Amplitude 2', 'Amplitude 3', 'Amplitude 4', 'Central Position', 'Sigma 1', 'Sigma 2', 'Sigma 3', 'Sigma 4']
        fit = fourGauss
    elif N == 5:
        from FWarbValue import fiveGauss
        paramNames = ['Amplitude 1', 'Amplitude 2', 'Amplitude 3', 'Amplitude 4', 'Amplitude 5', 'Central Position', 'Sigma 1', 'Sigma 2', 'Sigma 3', 'Sigma 4', 'Sigma 5']
        fit = fiveGauss
    
    # FW = getFWatValue(Iprof,dx=1,dy=1,frac=0.25,show=False)[0]
    
    # print("Full Width: ", FW)
    
    # SET BOUNDS FOR VARIABLES
    param_bounds = (
                    #-------------------- MINIMUM VALUES:
                    [iG[n]*(1-pdev) for n in range(0,(2*N)+1)],
                    #-------------------- MAXIMUM VALUES:
                    [iG[n]*(1+pdev) for n in range(0,(2*N)+1)]
                    )
            
    x = np.linspace(0,len(Iprof),len(Iprof))
    
    for i, k in enumerate(known):
        if k == 1:
            param_bounds[0][i] = iG[i]-iG[i]*1e-6
            param_bounds[1][i] = iG[i]+iG[i]*1e-6
            print("Value of {} is known... restricting fit".format(paramNames[i]))
        if iG[i] < param_bounds[0][i]:
            print(" ")
            print("Initial guess for {} less than lower bounds... adjusting bounds".format(paramNames[i]))
            p_old = param_bounds[0][i]
            param_bounds[0][i] = iG[i]-iG[i]*1e-6
            print("Guess Value: {},  Initial Lower Bound Value: {},  New Lower Bound: {}".format((iG[i]),(p_old),(param_bounds[0][i])))
        elif iG[i] > param_bounds[1][i]:
            print(" ")
            print("Initial guess for {} greater than upper bounds... adjusting bounds".format(paramNames[i]))
            p_old = param_bounds[1][i]
            param_bounds[1][i] = iG[i]+iG[i]*1e-6                
            print("Guess Value: {},  Initial Upper Bound Value: {},  New Upper Bound: {}".format((iG[i]),(p_old),(param_bounds[1][i])))
    
    
    if no_center:
        # Estimate peak position for central exclusion
        peak_idx = len(Iprof)//2 #np.argmax(Iprof)
        x0_est = x[peak_idx]

        # Create mask to exclude center
        mask = (x < x0_est - no_center / 2) | (x > x0_est + no_center / 2)
    
        x = x[mask]
        Iprof = Iprof[mask]
    
        # # Initial guesses for parameters
        # A_guess = np.max(y_fit) - np.min(y_fit)
        # sigma_guess = (np.max(x_fit) - np.min(x_fit)) / 6
        # offset_guess = np.min(y_fit)
    
        # try:
        #     popt, pcov = curve_fit(gaussian, x_fit, y_fit, p0=[A_guess, x0_est, sigma_guess, offset_guess])
        #     return popt, pcov
        # except RuntimeError as e:
        #     print("Fit failed:", e)
        #     return None, None
    
    p0 = iG
    
    # Arrays for plotting evolution of parameters
    A1,A2,A3,A4,A5 = [],[],[],[],[]
    mu = []
    sig1,sig2,sig3,sig4,sig5 = [],[],[],[],[]
    
    guess = fit(x, *p0) #[p for p in p0])
    
    
    A1.append(p0[0])
    mu.append(p0[N])
    sig1.append(p0[N+1])
    if N >= 2:
        A2.append(p0[1])
        sig2.append(p0[N+2])
    if N >= 3:
        # print('here')
        A3.append(p0[2])
        sig3.append(p0[N+3])
    if N >= 4:
        # print('here')
        A4.append(p0[3])
        sig4.append(p0[N+4])
    if N == 5:
        # print('here')
        A5.append(p0[4])
        sig5.append(p0[N+5])
    
    # curve_fit() function takes the f-function
    # x-data and y-data as argument and returns
    # the coefficient u in param and
    # the estimated covariance of param in param_cov
    #range(len(Iprof)),
    try:
        print("Fitting.....")
        param, param_cov = curve_fit(fit, Iprof, x, p0=p0, bounds=param_bounds)
    except RuntimeError:
        print("Optimal fit not found! ...returning guess and skipping.")
        return iG
    # ans stores the new y-data according to
    # the coefficient given by curve-fit() function
    y_fit = fit(x,*param)
    
    # elif N == 5:
    #     y_fit = fiveGauss(x,param[0],param[1],param[2],param[3],param[4],param[5],param[6],param[7],param[8],param[9],param[10])
    
    A1.append(param[0])
    mu.append(param[N])
    sig1.append(param[N+1])
    if N >= 2:
        A2.append(param[1])
        sig2.append(param[N+2])
    if N >= 3:
        A3.append(param[2])
        sig3.append(param[N+3])
    if N >= 4:
        A4.append(param[3])
        sig4.append(param[N+4])
    if N == 5:
        A5.append(param[4])
        sig5.append(param[N+5])
    
    iterations = 50 # number of iterations of the curve_fit() function in while loop below
    i=1
    
    numXticks = 7
    sF = 1e3
    nx = len(Iprof)
    
    # plt.clf()
    # plt.close()        
    plt.plot(Iprof, '.', color ='red', label ="data")
    # plt.plot(guess, ':', color = 'black', label="Initial Guess")
    # plt.plot(y_fit, ':', color = 'green', label="Model Fit")
    plt.title(str(title))
    plt.xlabel('Position [mm]')#[pixels]')
    plt.ylabel('Intensity [ph/s/cm$^2$]')#[counts]')        
    plt.xticks([int((nx-1.0)*(b/(numXticks-1.0))) for b in range(0,numXticks)],
               [round_sig(nx*dx*(a/(numXticks-1.0))*sF,1) for a in  range(-int((numXticks-1.0)/2.0),int((numXticks/2.0 + 1.0)))],fontsize=10)
    # plt.ticklabel_format(axis='x', style='sci', scilimits=(-4,4))
    
    # while i < iterations:
    #     print("Refining fitting... attempt #{}".format(i))
    #     param1, param_cov1 = curve_fit(fit, Iprof, x, p0=param, bounds=param_bounds)
        
    #     y_fit1 = fit(x,*param1)
        
    #     plt.plot(y_fit1, '--', label ="Model Fit - #" + str(i))
        
    #     A1.append(param1[0])
    #     A2.append(param1[1])
    #     mu.append(param1[N])
    #     sig1.append(param1[N+1])
    #     sig2.append(param1[N+2])
    #     if N >= 3:
    #         A3.append(param1[2])
    #         sig3.append(param1[N+3])
    #     if N >= 4:
    #         A4.append(param1[3])
    #         sig4.append(param1[N+4])
    #     if N == 5:
    #         A5.append(param1[4])
    #         sig5.append(param1[N+5])
        
    #     p1 = [round(p,5) for p in param]
    #     p2 = [round(p,5) for p in param1]
        
        
    #     if np.array(p1).all()==np.array(p2).all(): 
    #     # np.array(round(param1,3)) == np.array(round(param,3)): 
    #         #(param==param1).all(): 
    #         #param.all() == param1.all(): 
    #         #np.all(param) == np.all(param1):
    #         print(" ")
    #         print("----- Fitting parameters have reached equilibrium after {} iterations -----".format(i))
    #         finalParams.append(param1)
    #         # print([_p0-_p1 for _p0,_p1 in zip(param,param1)])
            
    #         fit(x,*param1,plot=True)
    #         break
        
    #     else:
    #         # print([_p0-_p1 for _p0,_p1 in zip(param,param1)])
    #         param = param1
    #         i += 1
    # else:
    finalParams.append(param)
    fit(x,*param,plot=True)
        
        # if N == 2:
        #     twoGauss(x,param1[0],param1[1],param1[2],param1[3],param1[4],plot=False)
        # elif N == 3:
        #     fiveGauss(x,param1[0],param1[1],param1[2],param1[3],param1[4],param1[5],param1[6], plot=False)
        # elif N == 5:
        #     fiveGauss(x,param1[0],param1[1],param1[2],param1[3],param1[4],param1[5],param1[6],param1[7],param1[8],param1[9],param1[10], plot=True)
        # print(" ")
        # print("----- Completed {} iterations without stagnation -----".format(iterations))
        
    
    plt.legend()
    # if savePath !=None:
    #     plt.savefig(savePath + str(pNum) + 'fittingPlot.png')
    plt.show()

    # # plt.clf()
    # # plt.close()
    # plt.plot(Iprof, '.', color ='red', label ="data")
    # plt.plot(y_fit1, '--', color ='blue', label ="Final Fit")
    # plt.plot(guess, ':', color = 'green', label="Initial Guess")
    # plt.ticklabel_format(axis='x', style='sci', scilimits=(-4,4))
    # plt.legend()
    # # if savePath !=None:
    # #     plt.savefig(savePath + str(pNum) + 'finalPlot.png')
    # plt.show()
    
    fig, axs = plt.subplots(2,N)
    if N ==1:
    
        axs[0].plot(A1)
        axs[0].set_title("A1")
        axs[0].set_ylim(param_bounds[0][0],param_bounds[1][0])
        axs[1].plot(sig1)
        axs[1].set_title("sig 1")
        axs[1].set_ylim(param_bounds[0][N+1],param_bounds[1][N+1])
    
    else:
        axs[0,0].plot(A1)
        axs[0,0].set_title("A1")
        axs[0,0].set_ylim(param_bounds[0][0],param_bounds[1][0])
        axs[0,1].plot(A2)
        axs[0,1].set_title("A2")
        axs[0,1].set_ylim(param_bounds[0][1],param_bounds[1][1])
        axs[1,0].plot(sig1)
        axs[1,0].set_title("sig 1")
        axs[1,0].set_ylim(param_bounds[0][N+1],param_bounds[1][N+1])
        axs[1,1].plot(sig2)
        axs[1,1].set_title("sig 2")
        axs[1,1].set_ylim(param_bounds[0][N+2],param_bounds[1][N+2])
        if N >= 3:
            axs[0,2].plot(A3)
            axs[0,2].set_title("A3")
            # axs[0,2].set_ylim(param_bounds[0][2],param_bounds[1][2])
            axs[1,2].plot(sig3)
            axs[1,2].set_title("sig 3")
            axs[1,2].set_ylim(param_bounds[0][N+3],param_bounds[1][N+3])
        if N >= 4:
            axs[0,3].plot(A4)
            axs[0,3].set_title("A4")
            axs[0,3].set_ylim(param_bounds[0][3],param_bounds[1][3])
            axs[1,3].plot(sig4)
            axs[1,3].set_title("sig 4")
            axs[1,3].set_ylim(param_bounds[0][N+4],param_bounds[1][N+4])
        if N == 5:
            axs[0,4].plot(A5)
            axs[0,4].set_title("A5")
            axs[0,4].set_ylim(param_bounds[0][4],param_bounds[1][4])
            # axs[1,2].plot(mu)
            # axs[1,2].set_title("mu")
            # axs[1,2].set_ylim(param_bounds[0][5],param_bounds[1][5])
            axs[1,4].plot(sig5)
            axs[1,4].set_title("sig 5")
            axs[1,4].set_ylim(param_bounds[0][10],param_bounds[1][10])
    # for ax in axs.reshape(-1): 
    #     ax.set_yscale('log')
    fig.tight_layout()
    # if savePath !=None:
    #     plt.savefig(savePath + str(pNum) + 'parametersPlot.png')        
    plt.show()
    
    
    return finalParams[0]
    
    # # return vis, coherence
    # if N == 2:
    #     return A1,A2,mu,sig1,sig2
    # elif N == 3:
    #     return A1,A2,A3,mu,sig1,sig2,sig3
    # elif N == 4:
    #     return A1,A2,A3,A4,mu,sig1,sig2,sig3,sig4
    # elif N == 5:
    #     return A1,A2,A3,A4,A5,mu,sig1,sig2,sig3,sig4,sig5


def test():
    import numpy as np
    import tifffile
    from usefulWavefield import counts2photonsPsPcm2
    path = '/user/home/data/BeamProfile_processed/averaged/'
    fileNums = range(0,41)
    files = [str(n) + '.tif' for n in fileNums]# [0,9]]#range(9,10)]
    
    axis = 'y'
    N = 2
    pdev = 0.15
    averaging = 10
    iterations = 1
    saveToPickle = True
    guessFromPickle = False
    
    if axis == 'y':
        r = 0
        Ir = [(0,0),(0,3),(4,4),(4,8),(8,11),(11,16),(17,19),(19,24),(24,31),(31,41)]

        _fa1 = [4.0,1.7,1.2,1.1,1.0,1.9,2.1,2.1,1.4,1.8]
        _fa2 = [0.01,1.5,1.7,2.0,3.0,3.2,1.8,1.7,2.7,2.2]
        _fm =  [2,2,2,6,10,5,4,4,1,0]
        _fs1 = [1.3,1.6,3.2,3.2,2.5,2.4,2.75, 2.5,2.4,1.9]
        _fs2 = [1.0,1.0,1.2,1.2,1.9,2.0,1.4, 1.4,1.6,1.6]
        _pdev = [0.15,0.15,0.15,0.15,0.35,0.35,0.15,0.15,0.15,0.15]
    
    elif axis == 'x':
        r = 0
        Ir = [(0,0),
              (0,3),
              (3,6),
              (6,21),
              (21,23),
              (24,24),
              (24,41)]
    
        _fa1 = [3.8,
                0.8,
                1.2,
                1.7,
                1.8,
                1.5,
                1.6]
        _fa2 = [0.01,
                2.1,
                1.5,
                1.6,
                1.3,
                1.4,
                1.8]
        _fm =  [2, 2, 10, 9, 9, 7,8]
        _fs1 = [1.35,
                2.1,
                2.5,
                2.5,
                1.8,
                1.8,
                1.8]
        _fs2 = [1.0,
                1.3,
                1.1,
                1.1,
                1.0,
                1.1,
                1.2]
        _pdev = [0.15,
                 0.20,
                 0.15,
                 0.05,
                 0.15,
                 0.15,0.05]
    
    
    fa1 = 1.1#*(1-pdev)*(1+pdev)
    fa2 = 2.0#*(1-pdev)
    fm = 6#*(1-pdev)
    fs1 = 3.2#*(1-pdev)
    fs2 = 1.2#*(1-pdev)
    
    energy_range =  np.arange(90,910,10)
    energy_range = [energy_range[i] for i in fileNums]
    
    I = [tifffile.imread(path + f) for f in files]
    
    # # converting cropped images from detector counts to ph/s/cm^2
    # I = [counts2photonsPsPcm2(i, e, t=60.0e-3, res=(11.0e-6,11.0e-6), conversion=1.27) for i,e in zip(I,energy_range)]
    
    dx,dy = 11.0e-6, 11.0e-6 #9.57713358e-7, 7.253495748e-7
    # x_center = [i[np.shape(i)[1]//2,:] for i in I]# I[0][I[0].shape[0]//2,:]
    # y_center = I[0][:,I[0].shape[1]//2]
    
    # plt.imshow(I[0])
    # plt.show()
    
    # print('Averaging 1')
    if axis == 'x':
        center = [np.mean(i[np.shape(i)[1]//2 - int(averaging/2):np.shape(i)[1]//2 + int(averaging/2),:],axis=0) for i in I]
    elif axis == 'y':
        center = [np.mean(i[:,np.shape(i)[0]//2 - int(averaging/2):np.shape(i)[0]//2 + int(averaging/2)],axis=1) for i in I]
    # y_center = np.mean(I[:,I.shape[1]//2 - int(averaging/2):I.shape[1]//2 + int(averaging/2)],axis=1)
    # x,y = np.linspace(0,len(x_center),len(x_center)), np.linspace(0,len(y_center),len(y_center))
    centerIndex = (np.shape(I[0])[0]//2,np.shape(I[0])[1]//2)
    if axis == 'x':
        centerI = centerIndex[1]
    elif axis == 'y':
        centerI = centerIndex[0]
    
    # for i, _I in enumerate(I):
    #     plt.imshow(_I)
    #     plt.vlines(centerIndex[0], ymin=0,ymax=600)
    #     plt.colorbar()
    #     plt.show()
    
    print(' ')
    print(centerIndex)
    print(' ')
    
    transportEUV = [0.2*3.370622228559459e+00,# 0.02912449075001519, 
                    50*0.0007733456105504161,# 9.988727217880288e-05, 
                    80*1.0275986398716954e-05,# 1.1207129598100509e-06,
                    1.0628327603986831e-07,# 9.395146279594812e-09, 
                    7.028188266094643e-10]
    transportBEUV = [0.200777800669182,# 0.010118098188164832, 
                     70*0.0012707964425810554,# 0.00013500761409059693, 
                     100*1.3210249918570955e-05,# 1.0912870506333387e-06, 
                     3.75954413824336e-08,# 5.339077267518293e-08, 
                     4.020904647940034e-09]
    T = [transportEUV,transportBEUV]    
    
    IsimEUV = [0.01,0.04,1.5,1.75,2.75]
    IsimBEUV = [0.025,0.5,1.2,1.4,1.75] # last 2 are made up
    Isim = [IsimEUV,IsimBEUV]
    
    spreadEUV = [70*m for m in [0.013,0.008,0.005,0.002,0.00175]] #[0.013,0.004,0.003,0.002,0.00175]
    spreadBEUV = [70*m for m in [0.005,0.003,0.002,0.0005,0.00035]] #[0.005,0.002,0.001,0.0005,0.00035] # last 2 are made up
    spreads = [spreadEUV,spreadBEUV]
    
    # if len(T) != len(fileNums):
    I = [(a+b)/2 for a,b in zip(Isim[0],Isim[1])]
    T = [(a+b)/2 for a,b in zip(T[0],T[1])]
    spreads = [(a+b) for a,b in zip(spreads[0],spreads[1])]
    spreads = np.tile(spreads,(len(fileNums),1))
    weights = [t*_I for t,_I in zip(T,I)]#[0.65,0.4]#,1.4,0.7,1.4]
        # print(weights)
        # print('here')
        # print(spreads)
    # else:
    #     pass
    
    Amp, S, M = [],[],[]
    FWHM, TOTI, FRAC = [], [], []
    
    for i,x_center in enumerate(center):
        # if len(T) == len(fileNums):
        #     weights = [t*I for t,I in zip(T[i],Isim[i])]#[0.65,0.4]#,1.4,0.7,1.4]
        # else:
        #     pass
        x_center = np.subtract(x_center,9)
        x_center[x_center < 1] = 0
        
        A1 = np.max(x_center)
        s1 = getFWatValue(x_center, dx=1, dy=1,frac=0.55,show=False)[0] # np.std(x_center)/5
        # print(spreads[0]/np.sum(spreads[i]))
        # print(spreads[1]/np.sum(spreads[i]))
        if guessFromPickle:
            import pickle
            print('hello')
            pG = pickle.load(open(path + 'G' + str(N) + axis + '_intensityFits.pkl', 'rb'))
            aG, sG = pG[0], pG[1]
            iG = [*aG[i],
                  centerI, 
                  *sG[i]]
            # print(iG)
            # print(np.shape(pG))
            # print(pG[0])
        
        it = 1
        while it <= iterations:
            if N == 2:
                if guessFromPickle is False:
                    # if i == 0:
                    #     fa1,fa2,fm,fs1,fs2 = _fa1[0],_fa2[0],_fm[0],_fs1[0],_fs2[0] 
                    #     pdev = _pdev[0]
                    # elif i > 0 and i <= 3:
                    #     fa1,fa2,fm,fs1,fs2 = _fa1[1],_fa2[1],_fm[1],_fs1[1],_fs2[1] 
                    #     pdev = _pdev[1]
                    # elif i == 4:
                    #     fa1,fa2,fm,fs1,fs2 = _fa1[2],_fa2[2],_fm[2],_fs1[2],_fs2[2] 
                    #     pdev = _pdev[2]
                    # elif i > 4 and i <= 8:
                    #     fa1,fa2,fm,fs1,fs2 = _fa1[3],_fa2[3],_fm[3],_fs1[3],_fs2[3] 
                    #     pdev = _pdev[3]
                    # elif i > 8 and i <= 11:
                    #     fa1,fa2,fm,fs1,fs2 = _fa1[4],_fa2[4],_fm[4],_fs1[4],_fs2[4] 
                    #     pdev = _pdev[4]
                    # elif i > 11 and i <= 17:
                    #     fa1,fa2,fm,fs1,fs2 = _fa1[5],_fa2[5],_fm[5],_fs1[5],_fs2[5] 
                    #     pdev = _pdev[5]
                    # elif i > 17 and i <= 24:
                    #     fa1,fa2,fm,fs1,fs2 = _fa1[6],_fa2[6],_fm[6],_fs1[6],_fs2[6] 
                    #     pdev = _pdev[6]
                    # elif i > 24 and i <= 31:
                    #     fa1,fa2,fm,fs1,fs2 = _fa1[7],_fa2[7],_fm[7],_fs1[7],_fs2[7] 
                    #     pdev = _pdev[7]
                    # elif i > 31 and i <= 41:
                    #     fa1,fa2,fm,fs1,fs2 = _fa1[8],_fa2[8],_fm[8],_fs1[8],_fs2[8] 
                    #     pdev = _pdev[8]
                    
                    if i == Ir[r][0] and i == Ir[r][1] or i > Ir[r][0] and i <= Ir[r][1]:
                        pass
                    else:
                        r += 1
                    fa1,fa2,fm,fs1,fs2 = _fa1[r],_fa2[r],_fm[r],_fs1[r],_fs2[r]
                    pdev = _pdev[r]
                        
                    print('here')
                    print(fa1,fa2,fm,fs1,fs2)
                    
                    iG = [A1*(weights[0]/np.sum(weights))*fa1,
                          A1*(weights[0]/np.sum(weights))*fa2,
                          centerI+fm,
                          s1*(spreads[i][0]/np.sum(spreads[i]))*fs1,
                          s1*(spreads[i][1]/np.sum(spreads[i]))*fs2]
                    print('iG: ', iG)
                else:
                    pass
                known = [0,0,1,0,0]
                fParams = fitMultiGauss(x_center,dx,N,iG,known,pdev=pdev,title=energy_range[i])
                A1,A2,mu,s1,s2 = fParams[0],fParams[1],fParams[2],fParams[3],fParams[4]
                print(" ")
                print("----- Coefficients of fit -----")
                print("A1:                          {}".format(A1))
                print("A2:                          {}".format(A2))
                print("mu:                          {}".format(mu))
                print("sig1:                        {}".format(s1))
                print("sig2:                        {}".format(s2))
                A = [A1,A2]
                s = [s1,s2]
                Amp.append(A)
                S.append(s)
                M.append(mu)
                
                G1 = gauss(np.linspace(-100,800,600),A1,mu,s1,plot=False)
                G2 = gauss(np.linspace(-100,800,600),A2,mu,s2,plot=False)
                
                
                
                fwhm1 = 2.35482*s1*11.0e-3
                fwhm2 = 2.35482*s2*11.0e-3
                flux1 = np.sum(G1) #counts2photonsPsPcm2(1.064467*A1*fwhm1,energy_range[i],t=60.0e-3,res=(11.0e-6,11.0e-6),conversion=1.27)
                flux2 = np.sum(G2) #counts2photonsPsPcm2(1.064467*A2*fwhm1,energy_range[i],t=60.0e-3,res=(11.0e-6,11.0e-6),conversion=1.27)
                frac1 = flux1/(flux1+flux2)
                frac2 = flux2/(flux1+flux2)
                
                FWHM.append([fwhm1,fwhm2])
                TOTI.append([flux1,flux2])
                FRAC.append([frac1,frac2])
                
                print('fParams: ',fParams)
            
            elif N == 3:
                if guessFromPickle is False:
                    iG = [A1*(weights[0]/np.sum(weights)),
                          A1*(weights[1]/np.sum(weights))*2,
                          A1*(weights[2]/np.sum(weights)),
                          centerI+10,
                          s1*(spreads[i][0]/np.sum(spreads[i]))*2.5,
                          s1*(spreads[i][1]/np.sum(spreads[i]))*1.9,
                          s1*(spreads[i][2]/np.sum(spreads[i]))]
                    print('iG: ', iG)
                else:
                    pass
                known = [0,0,0,1,0,0,0]
                fParams = fitMultiGauss(x_center,dx,N,iG,known,pdev=pdev)
                A1,A2,A3,mu,s1,s2,s3 = fParams[0],fParams[1],fParams[2],fParams[3],fParams[4],fParams[5],fParams[6]
                print(" ")
                print("----- Coefficients of fit -----")
                print("A1:                          {}".format(A1))
                print("A2:                          {}".format(A2))
                print("A3:                          {}".format(A3))
                print("mu:                          {}".format(mu))
                print("sig1:                        {}".format(s1))
                print("sig2:                        {}".format(s2))
                print("sig3:                        {}".format(s3))
                A = [A1,A2,A3]
                s = [s1,s2,s3]
                Amp.append(A)
                S.append(s)
                print('fParams: ',fParams)
                
            elif N == 4:
                if guessFromPickle is False:
                    iG = [A1*(weights[0]/np.sum(weights)),
                          A1*(weights[1]/np.sum(weights)),
                          A1*(weights[2]/np.sum(weights)),
                          A1*(weights[3]/np.sum(weights)),
                          centerI,
                          s1*(spreads[i][0]/np.sum(spreads[i])),
                          s1*(spreads[i][1]/np.sum(spreads[i])),
                          s1*(spreads[i][2]/np.sum(spreads[i])),
                          s1*(spreads[i][3]/np.sum(spreads[i]))] 
                    print('iG: ', iG)
                else:
                    pass
                known = [0,0,0,0,1,0,0,0,0]
                fParams = fitMultiGauss(x_center,dx,N,iG,known,pdev=pdev)
                A1,A2,A3,A4,mu,s1,s2,s3,s4 = fParams[0],fParams[1],fParams[2],fParams[3],fParams[4],fParams[5],fParams[6],fParams[7],fParams[8]
                print(" ")
                print("----- Coefficients of fit -----")
                print("A1:                          {}".format(A1))
                print("A2:                          {}".format(A2))
                print("A3:                          {}".format(A3))
                print("A4:                          {}".format(A4))
                print("mu:                          {}".format(mu))
                print("sig1:                        {}".format(s1))
                print("sig2:                        {}".format(s2))
                print("sig3:                        {}".format(s3))
                print("sig4:                        {}".format(s4))
                A = [A1,A2,A3,A4]
                s = [s1,s2,s3,s4]
                Amp.append(A)
                S.append(s)
                print('fParams: ',fParams)
                
            elif N == 5:
                if guessFromPickle is False:
                    iG = [A1*(weights[0]/np.sum(weights)),
                          A1*(weights[1]/np.sum(weights)),
                          A1*(weights[2]/np.sum(weights)),
                          A1*(weights[3]/np.sum(weights)),
                          A1*(weights[4]/np.sum(weights)),
                          centerI,
                          s1*(spreads[i][0]/np.sum(spreads[i])),
                          s1*(spreads[i][1]/np.sum(spreads[i])),
                          s1*(spreads[i][2]/np.sum(spreads[i])),
                          s1*(spreads[i][3]/np.sum(spreads[i])),
                          s1*(spreads[i][4]/np.sum(spreads[i]))] 
                    print('iG: ', iG)
                else:
                    pass
                known = [0,0,0,0,0,1,0,0,0,0,0]
                fParams = fitMultiGauss(x_center,dx,N,iG,known,pdev=pdev)
                A1,A2,A3,A4,A5,mu,s1,s2,s3,s4,s5 = fParams[0],fParams[1],fParams[2],fParams[3],fParams[4],fParams[5],fParams[6],fParams[7],fParams[8],fParams[9],fParams[10]
                print(" ")
                print("----- Coefficients of fit -----")
                print("A1:                          {}".format(A1))
                print("A2:                          {}".format(A2))
                print("A3:                          {}".format(A3))
                print("A4:                          {}".format(A4))
                print("A5:                          {}".format(A5))
                print("mu:                          {}".format(mu))
                print("sig1:                        {}".format(s1))
                print("sig2:                        {}".format(s2))
                print("sig3:                        {}".format(s3))
                print("sig4:                        {}".format(s4))
                print("sig5:                        {}".format(s5))
                A = [A1,A2,A3,A4,A5]
                s = [s1,s2,s3,s4,s5]
                Amp.append(A)
                S.append(s)
                print('fParams: ',np.array(fParams))
            
            iG = fParams
            it += 1
        
    
    if saveToPickle:
        import pickle
        with open(path + 'G' + str(N) + axis + '_intensityFits.pkl', "wb") as f:
                    pickle.dump([Amp,S], f, protocol=2)
    
    fig, ax = plt.subplots(1,3)
    # for i,_A in enumerate(np.array(Amp).T):
    #     FWHM = [2.35482*_s*11e-3 for _s in np.array(S).T[i]]
    #     area = [counts2photonsPsPcm2(1.064467*a*f,energy_range[i],t=60.0e-3,res=(11.0e-6,11.0e-6),conversion=1.27) for a,f in zip(_A,FWHM)]
    #     F = [a/np.sum(area) for a in area]
    
    #     # FWHM = [2.35482*_s*11e-3 for _s in s] 
    #     # area = [1.064467*a*f for a,f in zip(A,FWHM)]
    #     # F = [a/np.sum(area) for a in area]
    #     # print("FWHM of each Gaussian:                     ", FWHM)
    #     # print("Area of each Gaussian:                     ", area)
    #     # print("Fraction of total area of each Gaussian:   ", F)
            
    #     ax[0].plot(energy_range,FWHM,':x')
    #     ax[0].set_ylabel('FWHM (' + axis + ') [mm]')
    #     ax[1].plot(energy_range,area,':x', label=f"#{1+i}")
    #     ax[1].set_ylabel("Area [a.u]")
    #     ax[2].plot(energy_range,F,':x')
    #     ax[2].set_ylabel("Fraction")
    # for a in ax:
    #     a.set_xlabel('Photon Energy [eV]')
    #     # a.set_yscale('log')
        
    ax[0].plot(energy_range,[f[0] for f in FWHM],':x')
    ax[0].plot(energy_range,[f[1] for f in FWHM],':x')
    ax[1].plot(energy_range,[t[0] for t in TOTI],':x',label='H #1')
    ax[1].plot(energy_range,[t[1] for t in TOTI],':x',label='H #2')
    ax[2].plot(energy_range,[f[0] for f in FRAC],':x')
    ax[2].plot(energy_range,[f[1] for f in FRAC],':x')
    ax[0].set_ylabel('FWHM (' + axis + ') [mm]')
    ax[1].set_ylabel("Total Intensity [$ph/s/.1\%bw$]")
    ax[2].set_ylabel("Fraction of Total Intensity")
    for a in ax:
        a.set_xlabel('Photon Energy [eV]')
    ax[1].legend()
    fig.tight_layout()
    plt.show()        
    
    
    if saveToPickle:
        import pickle
        with open(path + 'G' + str(N) + axis + '_analysis.pkl', "wb") as f:
                    pickle.dump([[f[0] for f in FWHM],[f[1] for f in FWHM],[t[0] for t in TOTI],[t[1] for t in TOTI]], f, protocol=2)
    
def testBuildGausses():
    import pickle
    import tifffile
    path = '/user/home/data/BeamProfile_processed/averaged/'
    savePath = '/user/home/data/BeamProfile_processed/fits/'
    
    Xparams = pickle.load(open(path + 'G2x_intensityFits.pkl', 'rb'))
    Yparams = pickle.load(open(path + 'G2y_intensityFits.pkl', 'rb'))
    
    Ax, Sx = Xparams[0], Xparams[1]
    Ay, Sy = Yparams[0], Yparams[1]    
    
    for i,ax in enumerate(Ax):
        # print(ax[1])
        # print(Ay[i][1])
        A0 = np.mean([ax[0],Ay[i][0]])
        A1 = np.mean([ax[1],Ay[i][1]])
        G1 = gauss2D(624,624,A0,sigma_x=Sx[i][0],sigma_y=Sy[i][0])
        G2 = gauss2D(624,624,A1,sigma_x=Sx[i][1],sigma_y=Sy[i][1])
        
        fig, ax = plt.subplots(1,2)
        ax[0].imshow(G1,vmax=np.max([G1,G2]),vmin=0)
        ax[1].imshow(G2,vmax=np.max([G1,G2]),vmin=0)
        # plt.colorbar()
        fig.tight_layout()
        plt.show()
        
        tifffile.imwrite(savePath + str(i) + '_1.tif', G1)
        tifffile.imwrite(savePath + str(i) + '_2.tif', G2)
    
if __name__ =='__main__':
    test()
    # testBuildGausses()