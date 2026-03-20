#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 13:40:30 2023

@author: -
"""

import numpy as np
import matplotlib.pyplot as plt
import pickle
from FWarbValue import getFWatValue, gauss2D, gauss
from multiGaussFit import fitMultiGauss, fitGauss

plt.rcParams["figure.figsize"] = (10,5)


def test():
    import numpy as np
    import tifffile
    from usefulWavefield import counts2photonsPsPcm2, counts2photonsPs
    path = '/user/home/data/HarmonicContam/Detector_Comission_August_2023/ProcessedImages/BeamProfile_90to350/averaged/'
    fileNums = range(0,21)
    files = [str(n) + '.tif' for n in fileNums]# [0,9]]#range(9,10)]
    exposure_time = 25e-3
    
    axis = 'y'
    N = 2
    pdev = 0.1
    averaging = 10
    saveToPickle = True
    guessFromPickle = False
    plotParams= True
    plotMetrics= True
    
    
    if axis == 'y':
        r = 0
        Ir =  [(0,0),(1,1),(2,3),(4,16),(17,17),(18,21)] 
        #       0,    1,    2,    3,     4,      5,
        _fa1 = [0.20, 0.50, 0.25, 0.35,  0.45,   0.50,2.1,2.1,1.4,1.8]
        _fa2 = [0.15, 0.40, 0.60, 0.60,  0.50,   0.45,1.8,1.7,2.7,2.2]
        _fm =  [-2.0, -1.0, -2.0, -1.0,  -1.0,   0.00,4,4,1,0]
        _fs1 = [0.75, 0.75, 0.90, 1.10,  1.0,    0.90,2.75, 2.5,2.4,1.9]
        _fs2 = [0.20, 0.30, 0.30, 0.35,  0.35,   0.35,1.4, 1.4,1.6,1.6]
        _pdev =[0.5, 0.5, 0.5, 0.5,      0.5,    0.50,0.15,0.15,0.15,0.15]
    
    elif axis == 'x':
        r = 0
        Ir = [(0,0),(1,1),(2,2),(3,5),(6,13),(14,16),(17,17),(18,19),(20,20),(21,22)]#,(5,5),(6,6),(7,7),(8,9),(10,13),(14,14),(15,15),(16,16),(17,17),(18,18),(19,22)]
        #      0,    1,    2,    3,    4,     5,      6,      7,      8,     9
        _fa1= [0.2,  0.45, 0.15, 0.25, 0.20,  0.30,   0.45,   0.55,  0.60,  0.65,  0.55,0.7,0.85,0.85,0.92] 
        _fa2= [0.3,  0.45, 0.75, 0.75, 0.73,  0.60,   0.55,   0.40,  0.40,  0.35,  0.4,0.3,0.1,0.1,0.08]
        _fm = [-1.0, -1.0, 2.00, 2.00, 2.00,  -1.0,   -1.0,   0.00,  0.00,  0.00,  0.00,0.00,0.00,-1.0,-1.0]
        _fs1= [0.90,  1.0,  1.30, 1.40, 1.90,  1.55,   1.25,   1.05,  0.95,  0.80,   1.0,0.6,0.525,0.475,0.45] 
        _fs2= [0.25, 0.35, 0.35, 0.35, 0.35,  0.35,   0.35,   0.25,  0.25,  0.20,  0.3,0.25,0.15,0.15,0.15]
        _pdev=[0.15, 0.15, 0.15, 0.15, 0.15,  0.15,   0.15,   0.15,  0.15,  0.50,  0.5,0.5,0.5,0.5,0.5]
    
    # if axis == 'y':
    #     r = 0
    #     Ir =  [(0,1),(2,2),(3,3),(4,8),(9,12),(13,14),(15,15),(16,21),(17,21)] 
    #     #       0,    1,    2,    3,     4,      5,      6,
    #     _fa1 = [0.55, 0.35, 0.40, 0.70, 0.70,  0.25,  0.57,   0.65,   0.55,   1.4,1.8]
    #     _fa2 = [0.40, 0.50, 0.40, 0.10, 0.20,  0.70,  0.40,   0.30,   0.60,   2.7,2.2]
    #     _fm =  [-1.0, -2.0, 5.00, 20.0, 10.0,  -2.0,  -5.00, -5.00, -5.00,   1,0]
    #     _fs1 = [0.90, 0.95, 1.05, 1.15, 1.15,  1.07,  0.89,   0.70,   0.90,   2.5,2.4,1.9]
    #     _fs2 = [0.30, 0.35, 0.47, 0.45, 0.40,  0.39,  0.35,   0.30,   0.40,   1.6,1.6]
    #     _pdev =[0.15, 0.15, 0.15, 0.5,  0.50,  0.5,   0.5,   0.5,   0.15,0.15,0.15]
    
    # elif axis == 'x':
    #     r = 0
    #     Ir = [(0,1),(2,2),(3,3),(4,4),(5,6),(7,8),(9,9),(10,13),(14,21),(18,18),(19,20),(21,21),(21,22)]#,(5,5),(6,6),(7,7),(8,9),(10,13),(14,14),(15,15),(16,16),(17,17),(18,18),(19,22)]
    #     #      0,    1,    2,    3,    4,    5,    6,    7,      8,     9
    #     _fa1= [0.85, 0.75, 0.60, 0.60, 0.60, 0.60, 0.70, 0.70,  0.10,   0.45,   0.60,  0.60,   0.65,  0.55,0.7,0.85,0.85,0.92] 
    #     _fa2= [1e-2, 0.20, 0.20, 0.25, 0.25, 0.20, 0.20, 0.20,  0.85,   0.40,  0.40,   0.35,  0.4,0.3,0.1,0.1,0.08]
    #     _fm = [0.00, 30.0, 30.0, 30.0, 40.0, 30.0, 30.0, 30.0,  2.00,   -1.0,   -5.0,  -5.0,   -5.0,  0.00,0.00,0.00,-1.0,-1.0]
    #     _fs1= [0.60, 0.75, 1.30, 1.30, 1.60, 1.10, 0.75, 0.60,  1.15,   1.25,   0.90,  0.83,   0.73,   1.0,0.6,0.525,0.475,0.45] 
    #     _fs2= [0.30, 0.30, 0.50, 0.60, 0.80, 0.80, 0.50, 0.40,  0.45,   0.35,   0.25,  0.20,   0.20,  0.3,0.25,0.15,0.15,0.15]
    #     _pdev=[0.15, 0.15, 0.15, 0.15, 0.15, 0.50, 0.50, 0.50,  0.15,   0.15,   0.15,  0.15,   0.50,  0.5,0.5,0.5,0.5,0.5]

    
    fa1 = 0.225
    fa2 = 0.17
    fm = -3
    fs1 = 0.12
    fs2 = 0.03
    # ignore_range = [0:150]
    
    energy_range =  [90,92] + [e for e in np.arange(100, 185,10)] + [185] + [e for e in np.arange(190, 205,10)] + [e for e in np.arange(290,355,10)]
    # print(len(energy_range))
    # print(len(fileNums))
    # energy_range = [energy_range[i] for i in fileNums]
    
    I = [tifffile.imread(path + f) for f in files]
    
    # converting cropped images from detector counts to ph/s/cm^2
    I = [counts2photonsPs(i, e, t=exposure_time, conversion=1.27) for i,e in zip(I,energy_range)]
    dx,dy = 11.0e-6, 11.0e-6 
    
    I = [(i/(dx*dy*10000)) for i in I]
    
    shiftX = 0
    shiftY = 0
    # print('Averaging 1')
    centerIndex = (np.shape(I[0])[0]//2 + shiftY,np.shape(I[0])[1]//2 + shiftX)
    midFracX = 5
    midFracY = 10
    if axis == 'x':
        center = [np.mean(i[centerIndex[0] - int(averaging/2):centerIndex[0] + int(averaging/2),:],axis=0) for i in I]
        #[np.mean(i[np.shape(i)[0]//2 - int(averaging/2):np.shape(i)[0]//2 + int(averaging/2),:],axis=0) for i in I]
        centerI = centerIndex[1]
    elif axis == 'y':
        center = [np.mean(i[:,centerIndex[1] - int(averaging/2):centerIndex[1] + int(averaging/2)],axis=1) for i in I]
        # [np.mean(i[:,np.shape(i)[1]//2 - int(averaging/2):np.shape(i)[1]//2 + int(averaging/2)],axis=1) for i in I]
        centerI = centerIndex[0]
    
    
    # Show images with lines for profile
    for i, _I in enumerate(I[0:5]):
        plt.imshow(_I)
        
        plt.hlines(centerIndex[0] - int(averaging/2),xmin=0,xmax=799,colors='r',linestyles=':')
        plt.hlines(centerIndex[0],xmin=0,xmax=799,colors='r')
        plt.hlines(centerIndex[0] + int(averaging/2),xmin=0,xmax=799,colors='r',linestyles=':')
        plt.vlines(centerIndex[1] - int(averaging/2),ymin=0,ymax=699,colors='b',linestyles=':')
        plt.vlines(centerIndex[1],ymin=0,ymax=699,colors='b')#,linestyles=':')
        plt.vlines(centerIndex[1] + int(averaging/2),ymin=0,ymax=699,colors='b',linestyles=':')
        plt.title('E = '+ str(energy_range[i]))
        plt.colorbar()
        plt.show()
    
    
    Amp, S, M = [],[],[]
    FWHM, TOTI, FRAC = [], [], []
    R = []
    
    for i,x_center in zip(fileNums,center): #enumerate(center):
        x_center = np.subtract(x_center,9)
        x_center[x_center < 1] = 0
        
        A1 = np.max(x_center)
        s1 = getFWatValue(x_center, dx=1, dy=1,frac=0.55,show=False)[0] 
        
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
        
        if N == 2:
            if guessFromPickle is False:
                if i == Ir[r][0]:
                    # print("here 1")
                    # print('\n GOOD')
                    pass
                elif i > Ir[r][0] and i <= Ir[r][1]: #i == Ir[r][1]:
                    # print("here 2")
                    # print('\n GOOD')
                    pass
                else:
                    # print('\n BAD \n')
                    # print(i)
                    # print(r)
                    # print(Ir[r][0])
                    # print(Ir[r][1])
                    r += 1
                    if i == Ir[r][0]:
                        # print("here 3")
                        # print('\n GOOD')
                        pass
                    elif i > Ir[r][0] and i <= Ir[r][1]: #i == Ir[r][1]:
                        # print("here 4")
                        # print('\n GOOD')
                        pass
                    else:
                        # print('\n BAD \n')
                        r += 1
                
                fa1,fa2,fm,fs1,fs2 = _fa1[r],_fa2[r],_fm[r],_fs1[r],_fs2[r]
                pdev = _pdev[r]
                
                if axis == 'x':
                    const1 = np.mean([x_center[0],x_center[-1]])
                elif axis == 'y':
                    const1 = np.mean([x_center[0],x_center[-1]])
                
                iG1 = [A1*fa1,centerI+fm,s1*fs1,const1]
                iG2 = [A1*fa2,centerI+fm,s1*fs2,const1]
                
                print('\n ' + str(fm) + ', ' + str(centerI))
                
                # print(np.shape(x_center))
                if axis == 'x':
                    ignorePix = np.shape(x_center)[0]//midFracX
                    ignore1 = np.ones_like(x_center)*pdev
                    ignore1[centerI-ignorePix:centerI+ignorePix] = 100
                    ignore2 = np.ones_like(x_center)*pdev
                    ignore2[0:centerI-ignorePix] = 100
                    ignore2[centerI+ignorePix:-1] = 100
                elif axis == 'y':
                    ignorePix = np.shape(x_center)[0]//midFracY
                    ignore1 = np.ones_like(x_center)*pdev
                    ignore1[0:np.shape(x_center)[0]//3 + 20] = 100
                    ignore1[(3*np.shape(x_center)[0])//4 - 20::] = 100
                    ignore2 = np.ones_like(x_center)*pdev
                    ignore2[0:centerI-ignorePix] = 100
                    ignore2[centerI+ignorePix:-1] = 100
                    ignore1[centerI-ignorePix:centerI+ignorePix] = 100
                    
                    
                
            else:
                pass
            known = [0,0,0,1]
            # print(ignore1)
            f1Params, f1cov = fitGauss(x_center,dx,ignore1,iG1,known,pdev=pdev,title="N = " + str(i) + ", E = " + str(energy_range[i]) + " eV , r =" + str(r),paramPlots=plotParams)
            iG2[0] = A1*fa2 + const1 + f1Params[0]
            print("IG1: ", iG1)
            print("IG2: ", iG2)
            f2Params, f2cov = fitGauss(x_center,dx,ignore2,iG2,known=[0,0,0,0],pdev=pdev,title="N = " + str(i) + ", E = " + str(energy_range[i]) + " eV , r =" + str(r),paramPlots=plotParams)

            iG = [f1Params[0],f2Params[0]-f2Params[3]-f1Params[0],f1Params[1],f1Params[2],f2Params[2]]
            fParams, fcov = fitMultiGauss(x_center,dx,N,iG=iG,known=[1,0,1,1,0],pdev=pdev,title="N = " + str(i) + ", E = " + str(energy_range[i]) + " eV , r =" + str(r),paramPlots=plotParams)
            
            A1,A2,mu,s1,s2,c = fParams[0],fParams[1],fParams[2],fParams[3],fParams[4],fParams[5]
            print(" ")
            print("----- Coefficients of fit -----")
            print("A1:                          {}".format(A1))
            print("A2:                          {}".format(A2))
            print("mu:                          {}".format(mu))
            print("sig1:                        {}".format(s1))
            print("sig2:                        {}".format(s2))
            A = [A1,A2]
            s = [s1,s2]
            RA1 = A1/np.max(x_center)
            RA2 = A2/np.max(x_center)
            RS1 = s1/getFWatValue(x_center, dx=1, dy=1,frac=0.55,show=False)[0] 
            RS2 = s2/getFWatValue(x_center, dx=1, dy=1,frac=0.55,show=False)[0] 
            Amp.append(A)
            S.append(s)
            M.append(mu)
            R.append([RA1,RA2,RS1,RS2])
            
            G1 = gauss(np.linspace(-100,800,600),A1,mu,s1,c,plot=False)
            G2 = gauss(np.linspace(-100,800,600),A2,mu,s2,c,plot=False)
            
            
            
            fwhm1 = 2.35482*s1*11.0e-3
            fwhm2 = 2.35482*s2*11.0e-3
            flux1 = np.sum(G1) #counts2photonsPsPcm2(1.064467*A1*fwhm1,energy_range[i],t=60.0e-3,res=(11.0e-6,11.0e-6),conversion=1.27)
            flux2 = np.sum(G2) #counts2photonsPsPcm2(1.064467*A2*fwhm1,energy_range[i],t=60.0e-3,res=(11.0e-6,11.0e-6),conversion=1.27)
            frac1 = flux1/(flux1+flux2)
            frac2 = flux2/(flux1+flux2)
            
            FWHM.append([fwhm1,fwhm2])
            TOTI.append([flux1,flux2])
            FRAC.append([frac1,frac2])
            
            print(np.shape(fcov))
            print(np.shape(f1cov))
            print(np.shape(f2cov))
            
            perr = np.sqrt(np.diag(fcov[0]))
            perr1 = np.sqrt(np.diag(f1cov[0]))
            perr2 = np.sqrt(np.diag(f2cov[0]))
            
            print('fParams: ',fParams)
            print('perr: ',perr)
            print('perr1: ',perr1)
            print('perr2: ',perr2)
            
        iG = fParams
        
    
    if saveToPickle:
        import pickle
        with open(path + 'G' + str(N) + axis + '_intensityFits.pkl', "wb") as f:
                    pickle.dump([Amp,S], f, protocol=2)
    if plotMetrics:
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
            
        ax[0].plot(energy_range[np.min(fileNums):np.max(fileNums)+1],[f[0] for f in FWHM],':x')
        ax[0].plot(energy_range[np.min(fileNums):np.max(fileNums)+1],[f[1] for f in FWHM],':x')
        ax[1].plot(energy_range[np.min(fileNums):np.max(fileNums)+1],[t[0] for t in TOTI],':x',label='H #1')
        ax[1].plot(energy_range[np.min(fileNums):np.max(fileNums)+1],[t[1] for t in TOTI],':x',label='H #2')
        ax[2].plot(energy_range[np.min(fileNums):np.max(fileNums)+1],[f[0] for f in FRAC],':x')
        ax[2].plot(energy_range[np.min(fileNums):np.max(fileNums)+1],[f[1] for f in FRAC],':x')
        ax[0].set_ylabel('FWHM (' + axis + ') [mm]')
        ax[1].set_ylabel("Total Intensity [$ph/s/.1\%bw$]")
        ax[2].set_ylabel("Fraction of Total Intensity")
        for a in ax:
            a.set_xlabel('Photon Energy [eV]')
        ax[1].legend()
        fig.tight_layout()
        plt.show()        
        
            
        fig, ax = plt.subplots(1,2)
        ax[0].plot(energy_range[np.min(fileNums):np.max(fileNums)+1],[r[0] for r in R],':x',label='a1')
        ax[0].plot(energy_range[np.min(fileNums):np.max(fileNums)+1],[r[1] for r in R],':x',label='a2')
        ax[1].plot(energy_range[np.min(fileNums):np.max(fileNums)+1],[r[2] for r in R],':x',label='s1')
        ax[1].plot(energy_range[np.min(fileNums):np.max(fileNums)+1],[r[3] for r in R],':x',label='s2')
        ax[0].legend()
        ax[1].legend()
        for a in ax:
            a.set_xlabel('Energy [eV]')
            a.set_ylabel('Scaling Factor')
        plt.show()
    
    
    if saveToPickle:
        import pickle
        with open(path + 'G' + str(N) + axis + '_analysis.pkl', "wb") as f:
                    pickle.dump([[f[0] for f in FWHM],[f[1] for f in FWHM],[t[0] for t in TOTI],[t[1] for t in TOTI]], f, protocol=2)
    
def testBuildGausses():
    import pickle
    import tifffile
    path = '/user/home/data/HarmonicContam/Detector_Comission_August_2023/ProcessedImages/BeamProfile_90to350/averaged/'
    savePath = '/user/home/data/HarmonicContam/Detector_Comission_August_2023/ProcessedImages/BeamProfile_90to350/fits/'
    
    Xparams = pickle.load(open(path + 'G2x_intensityFits.pkl', 'rb'))
    Yparams = pickle.load(open(path + 'G2y_intensityFits.pkl', 'rb'))
    
    Ax, Sx = Xparams[0], Xparams[1]
    Ay, Sy = Yparams[0], Yparams[1]    
    
    F1,F2 = [],[]
    for i,ax in enumerate(Ax):
        print('\n', i)
        print(ax[1])
        print(Ay[i][1])
        A0 = np.mean([ax[0],Ay[i][0]])
        A1 = np.mean([ax[1],Ay[i][1]])
        G1 = gauss2D(800,700,A0,sigma_x=Sx[i][0],sigma_y=Sy[i][0])
        G2 = gauss2D(800,700,A1,sigma_x=Sx[i][1],sigma_y=Sy[i][1])
        
        fig, ax = plt.subplots(1,2)
        ax[0].imshow(G1,vmax=np.max([G1,G2]),vmin=0)
        ax[1].imshow(G2,vmax=np.max([G1,G2]),vmin=0)
        # plt.colorbar()
        fig.tight_layout()
        plt.show()
        
        tifffile.imwrite(savePath + str(i) + '_1.tif', G1)
        tifffile.imwrite(savePath + str(i) + '_2.tif', G2)
        
        totI1 = np.sum(G1)
        totI2 = np.sum(G2)
        
        f1 = totI1 / (totI1 + totI2)
        f2 = totI2 / (totI1 + totI2)
        
        F1.append(f1)
        F2.append(f2)
        
        
    energy_range = [90,92] + [e for e in np.arange(100, 185,10)] + [185] + [e for e in np.arange(190, 205,10)] + [e for e in np.arange(290,355,10)]
        
    # plt.plot(energy_range,F1,label='fundamental')
    plt.plot(energy_range,[f*100 for f in F2],label='higher')
    plt.xlabel('Photon Energy')
    plt.ylabel('harmonic % of total intensity')
    plt.show()
    
if __name__ =='__main__':
    # test()
    testBuildGausses()