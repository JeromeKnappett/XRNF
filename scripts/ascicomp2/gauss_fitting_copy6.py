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

plt.rcParams["figure.figsize"] = (8,4)


def test():
    import numpy as np
    import tifffile
    from usefulWavefield import counts2photonsPsPcm2
    path = '/user/home/data/HarmonicContam/Detector_Comission_August_2023/ProcessedImages/BeamProfile_120to350_CircPol_fixedslits/averaged/'
    fileNums = range(2,4)
    files = [str(n) + '.tif' for n in fileNums]# [0,9]]#range(9,10)]
    exposure_time = 50e-3
    
    axis = 'x'
    N = 2
    pdev = 0.1
    averaging = 10
    saveToPickle = False
    guessFromPickle = False
    plotParams= True
    plotMetrics= True
    
    if axis == 'y':
        r = 0
        Ir = [(0,24)] 
        _fa1 = [4.0,1.7,1.2,1.1,1.0,1.9,2.1,2.1,1.4,1.8]
        _fa2 = [0.01,1.5,1.7,2.0,3.0,3.2,1.8,1.7,2.7,2.2]
        _fm =  [2,2,2,6,10,5,4,4,1,0]
        _fs1 = [1.3,1.6,3.2,3.2,2.5,2.4,2.75, 2.5,2.4,1.9]
        _fs2 = [1.0,1.0,1.2,1.2,1.9,2.0,1.4, 1.4,1.6,1.6]
        _pdev = [0.15,0.15,0.15,0.15,0.35,0.35,0.15,0.15,0.15,0.15]
    
    elif axis == 'x':
        r = 0
        Ir = [(0,22)] #[(0,0),(1,1),(2,4),(5,5),(6,6),(7,7),(8,9),(10,13),(14,14),(15,15),(16,16),(17,17),(18,18),(19,22)]
    
        _fa1 = [0.75] #[0.75,0.75,0.35,0.4,0.325,0.45,0.5,0.5,0.55,0.55,0.7,0.85,0.85,0.92] 
        _fa2 = [1.0e-10] #[0.01,0.01,0.45,0.5,0.30,0.45,0.45,0.5,0.5,0.4,0.3,0.1,0.1,0.08]
        _fm =  [-4] #[-4,-1,0,0,-1,0,0,0,0,0,0,0,-1,-1]
        _fs1 = [0.4] #[0.4,0.4,1.3,1.5,1.5,1.8,1.65,1.45,1.0,1.0,0.6,0.525,0.475,0.45] 
        _fs2 = [0.1] #[0.2,0.15,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.25,0.15,0.15,0.15]
        _pdev = [0.5] #[0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5]

    
    fa1 = 0.225
    fa2 = 0.17
    fm = -3
    fs1 = 0.12
    fs2 = 0.03
    # ignore_range = [0:150]
    
    energy_range = [90,92] + [e for e in np.arange(100, 180,10)] + [185] + [e for e in np.arange(190, 285,10)] #np.arange(90,355,10)
    # print(len(energy_range))
    # print(len(fileNums))
    # energy_range = [energy_range[i] for i in fileNums]
    
    I = [tifffile.imread(path + f) for f in files]
    
    # converting cropped images from detector counts to ph/s/cm^2
    I = [counts2photonsPsPcm2(i, e, t=exposure_time, res=(11.0e-6,11.0e-6), conversion=1.27) for i,e in zip(I,energy_range)]
    
    dx,dy = 11.0e-6, 11.0e-6 
    
    # print('Averaging 1')
    centerIndex = (np.shape(I[0])[0]//2,np.shape(I[0])[1]//2)
    if axis == 'x':
        center = [np.mean(i[np.shape(i)[1]//2 - int(averaging/2):np.shape(i)[1]//2 + int(averaging/2),:],axis=0) for i in I]
        centerI = centerIndex[1]
    elif axis == 'y':
        center = [np.mean(i[:,np.shape(i)[0]//2 - int(averaging/2):np.shape(i)[0]//2 + int(averaging/2)],axis=1) for i in I]
        centerI = centerIndex[0]
    
    # for i, _I in enumerate(I):
    #     plt.imshow(_I)
    #     plt.vlines(centerIndex[0], ymin=0,ymax=600)
    #     plt.colorbar()
    #     plt.show()
    
    
    Amp, S, M = [],[],[]
    FWHM, TOTI, FRAC = [], [], []
    
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
                    print("here 1")
                    print('\n GOOD')
                    pass
                elif i > Ir[r][0] and i <= Ir[r][1]: #i == Ir[r][1]:
                    print("here 2")
                    print('\n GOOD')
                    pass
                else:
                    print('\n BAD \n')
                    print(i)
                    print(r)
                    print(Ir[r][0])
                    print(Ir[r][1])
                    r += 1
                    if i == Ir[r][0]:
                        print("here 3")
                        print('\n GOOD')
                        pass
                    elif i > Ir[r][0] and i <= Ir[r][1]: #i == Ir[r][1]:
                        print("here 4")
                        print('\n GOOD')
                        pass
                    else:
                        print('\n BAD \n')
                        r += 1
                
                fa1,fa2,fm,fs1,fs2 = _fa1[r],_fa2[r],_fm[r],_fs1[r],_fs2[r]
                pdev = 0.35 #_pdev[r]
                
                const1 = np.mean([x_center[0],x_center[-1]])
                
                iG1 = [A1*fa1,centerI+fm,s1*fs1,const1]
                iG2 = [A1*fa2,centerI+fm,s1*fs2,const1]
                
                # print(np.shape(x_center))
                ignorePix = np.shape(x_center)[0]//5
                ignore1 = np.ones_like(x_center)*pdev
                ignore1[centerI-ignorePix:centerI+ignorePix] = 100
                ignore2 = np.ones_like(x_center)*pdev
                ignore2[0:centerI-ignorePix] = 100
                ignore2[centerI+ignorePix:-1] = 100
                
            else:
                pass
            known = [0,0,0,1]
            # print(ignore1)
            f1Params = fitGauss(x_center,dx,ignore1,iG1,known,pdev=pdev,title="E = " + str(energy_range[i]) + " eV , r =" + str(r),paramPlots=plotParams)
            iG2[0] = A1*fa2 + const1
            print("IG1: ", iG1)
            print("IG2: ", iG2)
            f2Params = fitGauss(x_center,dx,ignore2,iG2,known=[0,0,0,0],pdev=pdev,title="E = " + str(energy_range[i]) + " eV , r =" + str(r),paramPlots=plotParams)

            iG = [f1Params[0],f2Params[0]-f2Params[3],f1Params[1],f1Params[2],f2Params[2]]
            fParams = fitMultiGauss(x_center,dx,N,iG=iG,known=[1,0,1,1,0],pdev=pdev,title="E = " + str(energy_range[i]) + " eV , r =" + str(r),paramPlots=plotParams)
            
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
            Amp.append(A)
            S.append(s)
            M.append(mu)
            
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