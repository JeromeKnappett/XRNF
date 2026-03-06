#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 16 17:07:48 2021

@author: jerome
"""

import tifffile
import numpy as np
import matplotlib.pyplot as plt
import interferenceGratingModelsJK as interferenceGratingModelsJK
import interferenceGratingModels as interferenceGratingModels
import pickle

plt.rcParams["figure.figsize"] = (12,10)

def round_sig(x, sig=2):
    from math import log10, floor
    if x != 0:
        return round(x, sig-int(floor(log10(abs(x))))-1)
    else:
        return x

dirPath = '/user/home/opt/xl/xl/experiments/lowEnergyBeam/data/electrons/'
savePath = '/home/jerome/Documents/MASTERS/Figures/plots/roughness/'
order = [100,1000,2000,3000,4000]
mag = [1,1,1,1,1]

files = [str(o) + '/' + str(o) + '.pkl' for o in order]

labels =  [str(o) + ' electrons' for o in order]

legendTitle = None #'Propagation Distance'

# Specify analysis - turn plotting on and off
show = True                          # show initial tiffs and entire profiles
plotTogether = True                   # plot aerial image profiles together
contrast = True                       # compute contrast metrics
normalise = False                      # normalise profiles when plotting together
subtractAperture = False               # subtract intensity from aperture
plotFromEq = True                      # plot ideal intensity from equation
split = False                           # split into groups by correlation length (for ploting all aerial images together)
twoD = False                           # calculate two-dimensional contrast (still in development)
save = False                           # save plots to savePath
fromPickle = True

_N = range(30,2001,10)  #range(1200,1201) #                            # number of pixels to take for line profile  - 1200 for roughness aerial images
n = 1                                 # number of pixels to average over for line profile - 15 for roughness aerial images
plotRange = 500                       # range of aerial image plot in nm

# middle pixels of images
mid = np.full((np.shape(files)[0],2), (196, 12544-258))  #1250 for original

pitch = 100e-9

# read from files - create profiles and images of sampled range
if fromPickle:
    print([dirPath + f for f in files])
    picks = [pickle.load(open(dirPath + f, 'rb')) for f in files]
    tiffs = [p[0] for p in picks]
    res = [(p[1],p[2]) for p in picks]
#    print(res)
else:
    try:
        tiffs = [tifffile.imread(dirPath + f) for f in files]
    except FileNotFoundError:
        tiffs = [tifffile.imread(f) for f in files]
    
mC, rC, cC, Nrms, F, NI = [],[],[],[],[],[]
        
for N in _N:
    images = [t[m[0]-n:m[0]+n,m[1]-N:m[1]+N] for t, m in zip(tiffs,mid)]
    profiles = [i.mean(0) for i in images] #[t[m[0]-n:m[0]+n,m[1]-N:m[1]+N] for t, m in zip(tiffs,mid)]
    xP = [np.linspace(-N*r[0], N*r[0],2*N) for r in res]
    yP = [np.linspace(-n*r[1], n*r[1],2*n) for r in res]
    
    idealPickle = pickle.load(open('/user/home/opt/xl/xl/experiments/propDisTolerance/data/200um/200um.pkl', 'rb'))
    idealTif = idealPickle[0]
    idealRes = (idealPickle[1],idealPickle[2])
    idealMid = (196, 12188)
    idealImage = idealTif[idealMid[0]-n:idealMid[0]+n,idealMid[1]-N:idealMid[1]+N]
    idealProfile = idealImage.mean(0)
    idealXP = np.linspace(-N*idealRes[0], N*idealRes[0],2*N)
    
    ''' define interference grating parameters'''
    wl = 6.710553853647976e-9 # wavelength in m
    
    # Amplitude of both beams (assumed equal)
    A = np.max(profiles[0])*1e-6 #45.0e5 # 0.37e5 #0.3e5  # this may be scaled to  match simulated intensity
    A2 = 18.0e5
    k = 2*np.pi/wl
    m = 1 # order of diffracted beams from each grating
    d = [m*pitch for m in mag] #24e-9 #100e-9 # grating spacing
    d2 = round_sig(0.955*pitch,5)
    # angle between the beams from each grating
    theta = [np.arcsin(m *wl/_d) for _d in d]
    thetaF = np.arcsin(m *wl/(d2))
#    IPuf = interferenceGratingModelsJK.interferenceIntensity(xP[0],k,thetaUF,A=A,polarisationModes=('TE','TE'))
#    IPf = interferenceGratingModelsJK.interferenceIntensity(xP[0],k,thetaF,A=A2,polarisationModes=('TE','TE'))
    IPte = [interferenceGratingModelsJK.interferenceIntensity(xP[0],k,t,A=A,polarisationModes=('TE','TE')) for t in theta]
    IPtm = [interferenceGratingModelsJK.interferenceIntensity(xP[0],k,t,A=A,polarisationModes=('TM','TM')) for t in theta]
    I2d = [np.tile(te,(2*n,1)) for te in IPte]
    
    fig, axs = plt.subplots(1,2)
    axs[0].imshow(images[0],aspect='auto')
    axs[1].imshow(I2d[0],aspect='auto')
    
    print("Range of aerial image profile (h) [m]: ", np.max(xP[0])-np.min(xP[0]))
    print("Range of aerial image profile (v) [m]: ", np.max(yP[0])-np.min(yP[0]))
    # print(len(tiffs))
    # print(len(profiles))
    # print(len(labels))
    
    if show:
        if len(tiffs) == 1:
            plt.imshow(tiffs[0], aspect ='auto')
            plt.show()
            
            plt.imshow(images[0], aspect = 'auto')
            plt.show()
            
            plt.plot(profiles[0], label=labels[0])
            plt.legend()
            plt.ylabel('Intensity [ph/s/.1%bw/mm$^2$]')
            plt.xlabel('Position [nm]')
            plt.show
        else:
            fig, axs = plt.subplots(int(len(tiffs)),1)
            for i in range(len(tiffs)):
                axs[i].imshow(tiffs[i], aspect='auto')#5)
                axs[i].set_title(labels[i])
            axs[int(len(tiffs)/2)].set_ylabel('y-position [pixels]')
            axs[len(tiffs)-1].set_xlabel('x-position [pixels]')
            fig.tight_layout()
            plt.show()
            
            fig, axs = plt.subplots(int(len(tiffs)),1)
            for i in range(len(tiffs)):
                axs[i].imshow(images[i], aspect='auto')#15)
                # axs[i].set_title(labels[i])
                axs[i].set_xticks([int(((2*N)-1)*(b/(8))) for b in range(0,9)])   
                axs[i].set_yticks([int(((2*n)-1)*(b/(1))) for b in range(0,2)])   
                axs[i].set_yticklabels([round_sig(2*n*res[i][1]*(a/(2))*1e9) for a in range(-int((2)/2),int((3/2 + 1)))])
                axs[i].set_xticklabels([])
                fig.tight_layout()
                    
                
    #            axs[i].set_xticklabels([round_sig(np.max(xP[i])*x*1e9) for x in [0,-1, -3/5,-1/5,1/5,3/5,1]])
    #            axs[i].set_yticklabels([round_sig(np.max(yP[i])*y*1e9) for y in [0,-1, -2/5,2/5,1]])
                
        
            axs[len(tiffs)-1].set_xticklabels([round_sig(2*N*res[i][0]*(a/(8))*1e9) for a in range(-int((8)/2),int((9/2 + 1)))])
            axs[len(tiffs)-1].set_xlabel('x-position [nm]')
            axs[int(len(tiffs)/2)].set_ylabel('y-position [nm]')
            if save:
                plt.savefig(savePath + '2daerialImageAperture.pdf')
                plt.savefig(savePath + '2daerialImageAperture.png', dpi=2000)
            else:
                pass
            plt.show()
            
            fig, axs = plt.subplots(int(len(tiffs)),1)
            for i in range(len(tiffs)):
                axs[i].plot(xP[i]*1e9,profiles[i], label=labels[i])
            axs[int(len(tiffs)/2)].set_ylabel('Intensity [ph/s/.1%bw/mm$^2$]')
            axs[len(tiffs)-1].set_xlabel('Position [nm]')
            fig.tight_layout()
            plt.show()
    if subtractAperture:
        # profileSubtract = [a/np.max(a) - b/np.max(b) - c/np.max(c) for a,b,c in zip(profiles[2],profiles[1],profiles[0])]
        profileSubtract = profiles[2] - profiles[1] # - profiles[0]/np.max(profiles[1])
        plt.plot(xP[0]*1e9,profileSubtract)
        plt.xlim(-int(plotRange/2),int(plotRange/2))
        plt.show()
    
    plt.clf()
    plt.close()
    if plotTogether:
        if normalise:
            print("Normalising...")
            for i,p in enumerate(profiles):
                plt.plot(xP[i]*1e9,p/np.max(p), label=labels[i])
            plt.ylabel('Intensity [a.u]')
        else:
            print("Plotting...")
            for i,p in enumerate(profiles):
                print("Profile #", str(i))
                plt.plot(xP[i]*1e9,p, label=labels[i])
            plt.ylabel('Intensity [ph/s/.1%bw/mm$^2$]')
        if plotFromEq:
            if normalise:
                plt.plot(idealXP*1e9,idealProfile/np.max(idealProfile), '-', label='non-focused beam')
                plt.plot(xP[0]*1e9,IPte/np.max(IPte), ':', label='Eq.2.3.45 - TE')
            elif subtractAperture:
                profileSubtract = profiles[2]*2/np.max(profiles[2]) - profiles[1]/np.max(profiles[1])  - profiles[0]/4*np.max(profiles[0])
                EQplus = IPte/np.max(IPte) + profiles[1]/np.max(profiles[1]) + profiles[0]/np.max(profiles[0])
                plt.plot(xP[0]*1e9,profileSubtract/np.max(profileSubtract), label = 'aerial image - subtacted envelope')
                plt.plot(xP[0]*1e9,EQplus/np.max(EQplus), label = 'Eq.2.3.45 - added envelope')
            else:
                for i,t in enumerate(IPte):
                    plt.plot(xP[0]*1e9,t, ':', label='Eq.2.3.45 - pitch = {}nm'.format(d[i]*1e9))
                    
    #            plt.plot(idealXP*1e9,idealProfile, '-', label='non-focused beam')
#                plt.plot(xP[0]*1e9,IPuf, ':', label='Eq.2.3.45 - pitch = 100.0nm')
    #            plt.plot(xP[0]*1e9,IPf, ':', label='Eq.2.3.45 - pitch = {}nm'.format(d2*1e9))
    #            plt.plot(xP[0]*1e9,IPte, ':', label='Eq.2.3.45 - TE')
    #            plt.plot(xP[0]*1e9,IPtm, ':', label='Eq.2.3.45 - TM')
        else:
            pass
        plt.xlim(-int(plotRange/2), int(plotRange/2))
        plt.ylim(bottom=0)
        plt.xlabel('Position [nm]')
        plt.legend(title=legendTitle, loc='upper left')
        if save:
            plt.savefig(savePath + 'aerialImageAperture.pdf')
            plt.savefig(savePath + 'aerialImageAperture.png', dpi=2000)
        else:
            pass
        plt.show()
    else:
        pass
    
    
    if contrast:
        michelsonC = [interferenceGratingModelsJK.gratingContrastMichelson(p) for p in profiles]
        rmsC = [interferenceGratingModelsJK.gratingContrastRMS(p) for p in profiles]
        compositeC = [interferenceGratingModelsJK.meanDynamicRange(p) for p in profiles] #, mdrC, imbalanceC 
        nilsC = [interferenceGratingModelsJK.NILS(p,x, _d/4, show=False) for p, x, _d in zip(profiles, xP, d)]
    #    fourierC = [interferenceGratingModelsJK.gratingContrastFourier(p,x*1e6, show=False) for p, x in zip(profiles,xP)] #Cf,  Am, Fr, peakFr - Still unsure but seems good
        fidel = [interferenceGratingModelsJK.fidelity(p,ite) for p, ite in zip(profiles,IPte)]   # fidelity based on comparison to model
        
        
        print(f'Michelson Contrast: {michelsonC}')
        print(f'RMS Contrast:       {rmsC}')
        print(f'Composite Contrast: {[c[0] for c in compositeC]}')
        print(f'NILS (mean):        {[n[0] for n in nilsC]}')
        print(f'NILS (rms):         {[n[5] for n in nilsC]}')
        print(f'Fidelity:           {fidel}')
    
        mC.append(michelsonC)
        rC.append(rmsC)
        cC.append([c[0] for c in compositeC])
        Nrms.append([n[5] for n in nilsC])
        F.append(fidel)
        NI.append([n[0] for n in nilsC])
        
conM = np.array(mC).mean(0)
conRMS = np.array(rC).mean(0)
conC = np.array(cC).mean(0)
conNRMS = np.array(Nrms).mean(0)
FID = np.array(F).mean(0)
conN = np.array(NI).mean(0)

eM = [np.std(a) for a in np.transpose(mC)]/np.sqrt(len(_N))
eRMS = [np.std(a) for a in np.transpose(rC)]/np.sqrt(len(_N))
eC = [np.std(a) for a in np.transpose(cC)]/np.sqrt(len(_N))
eNrms = [np.std(a) for a in np.transpose(Nrms)]/np.sqrt(len(_N))
eF = [np.std(a) for a in np.transpose(F)]/np.sqrt(len(_N))
eN = [np.std(a) for a in np.transpose(NI)]/np.sqrt(len(_N))

#print(conM, conRMS, conC, conNRMS, FID, conN)
print(eM, eRMS, eC, eNrms, eF, eN)
#print(mC,rC,cC,Nrms,F,NI)#, eRMS, eC, eNrms, eF, eN)


if split:
    print(np.shape(michelsonC))
    fig, axs = plt.subplots(2,3)
    axs[0,0].plot(sigma[0:5], michelsonC[0:5], 'x:')
    axs[0,0].plot(sigma[5:10], michelsonC[5:10], 'x:')
    axs[0,0].plot(sigma[10:15], michelsonC[10:15], 'x:')
    axs[0,0].plot(sigma[15:20], michelsonC[15:20], 'x:')
    axs[0,0].plot(sigma[20:25], michelsonC[20:25], 'x:')
    axs[0,0].set_title("Michelson")
    axs[0,0].set_ylabel("Contrast")
    # axs[0,0].legend(loc='lower left')
    axs[0,1].plot(sigma[0:5], rmsC[0:5], 'x:')
    axs[0,1].plot(sigma[5:10], rmsC[5:10], 'x:')
    axs[0,1].plot(sigma[10:15], rmsC[10:15], 'x:')
    axs[0,1].plot(sigma[15:20], rmsC[15:20], 'x:')
    axs[0,1].plot(sigma[20:25], rmsC[20:25], 'x:')
    axs[0,1].set_title("RMS")
    axs[0,2].plot(sigma[0:5], [c[0] for c in compositeC[0:5]], 'x:')
    axs[0,2].plot(sigma[5:10], [c[0] for c in compositeC[5:10]], 'x:')
    axs[0,2].plot(sigma[10:15], [c[0] for c in compositeC[10:15]], 'x:')
    axs[0,2].plot(sigma[15:20], [c[0] for c in compositeC[15:20]], 'x:')
    axs[0,2].plot(sigma[20:25], [c[0] for c in compositeC[20:25]], 'x:')
    axs[0,2].set_title("Composite")
    axs[1,0].plot(sigma[0:5], [n[0] for n in  fourierC[0:5]], 'x:')
    axs[1,0].plot(sigma[5:10], [n[0] for n in  fourierC[5:10]], 'x:')
    axs[1,0].plot(sigma[10:15], [n[0] for n in  fourierC[10:15]], 'x:')
    axs[1,0].plot(sigma[15:20], [n[0] for n in  fourierC[15:20]], 'x:')
    axs[1,0].plot(sigma[20:25], [n[0] for n in  fourierC[20:25]], 'x:')
    axs[1,0].set_title("Fourier")
    axs[1,0].set_ylabel("Contrast")
    axs[1,1].set_title("NILS")
    axs[1,1].plot(sigma[0:5], fidel[0:5], 'x:')
    axs[1,1].plot(sigma[5:10], fidel[5:10], 'x:')
    axs[1,1].plot(sigma[10:15], fidel[10:15], 'x:')
    axs[1,1].plot(sigma[15:20], fidel[15:20], 'x:')
    axs[1,1].plot(sigma[20:25], fidel[20:25], 'x:')
    axs[1,1].set_title("Fidelity")
    axs[1,2].plot(sigma[0:5], [n[0] for n in nilsC[0:5]], 'x:')
    axs[1,2].plot(sigma[5:10], [n[0] for n in nilsC[5:10]], 'x:')
    axs[1,2].plot(sigma[10:15], [n[0] for n in nilsC[10:15]], 'x:')
    axs[1,2].plot(sigma[15:20], [n[0] for n in nilsC[15:20]], 'x:')
    axs[1,2].plot(sigma[20:25], [n[0] for n in nilsC[20:25]], 'x:')
    axs[1,2].set_title("NILS - mean")
    axs[1,2].set_ylabel("NILS")
    # for ax in fig.axes:
        # ax.set_xticklabels(labels, rotation=45, ha='right')
    axs[1,0].set_xlabel('\u03C3 [nm]')
    axs[1,1].set_xlabel('\u03C3 [nm]')
    axs[1,2].set_xlabel('\u03C3 [nm]')
    fig.tight_layout()
    # fig.subplots_adjust(bottom=0.5,hspace=5.33)   ##  Need to play with this number.
    axs[1,1].legend(labels=['$C_y$ = ' + str(c) for c in [2,4,6,8,10]], bbox_to_anchor=(2.3,-0.35), ncol=5) #loc="lower center"
    if save:
        plt.savefig(savePath + 'contrastAll.pdf')
        plt.savefig(savePath + 'contrastAll.png', dpi=2000)
    plt.show()
    
else:
    fig, axs = plt.subplots(2,3)
    axs[0,0].errorbar(order, conM, yerr=eM, fmt='x:', capsize=2.0)
    axs[0,0].set_title("Michelson")
    axs[0,0].set_ylabel("Contrast")
    axs[0,1].errorbar(order, conRMS, yerr=eRMS, fmt='x:', capsize=2.0)
    axs[0,1].set_title("RMS")
    axs[0,2].errorbar(order, conC, yerr=eC, fmt='x:', capsize=2.0)
    axs[0,2].set_title("Composite")
    axs[1,0].errorbar(order, conNRMS, yerr=eNrms, fmt='x:', capsize=2.0)
    axs[1,0].set_title("NILS - rms")
    axs[1,0].set_ylabel("Contrast")
    axs[1,1].set_title("NILS")
    axs[1,1].errorbar(order, FID, yerr=eF, fmt='x:', capsize=2.0)
    axs[1,1].set_title("Fidelity")
    axs[1,2].errorbar(order, conN, yerr=eN, fmt='x:', capsize=2.0)
    axs[1,2].set_title("NILS - mean")
    axs[1,2].set_ylabel("NILS")
#        for ax in fig.axes:
#            ax.set_xticklabels(order, rotation=45, ha='right')
    # axs[1,0].set_xlabel('Slit Width')
    # axs[1,1].set_xlabel('Slit Width')
    # axs[1,2].set_xlabel('Slit Width')
    fig.tight_layout()
    if save:
        plt.savefig(savePath + 'contrastAllCy4.pdf')
        plt.savefig(savePath + 'contrastAllCy4.png', dpi=2000)
    plt.show()
    
    if twoD:
        nils2d = []
        nils2dRMS = []
        nils3s = []
        nilsrmsD = []
        
        fourierC2d = []
        print("getting line profiles down every pixel")
        for e, i in enumerate(images):
            iP = [i[:,a] for a in range(0,np.shape(i)[1])]
            print("shape:", np.shape(iP))
            plt.plot(xP[e]*1e9,[p for p in iP])
            plt.xlim(-plotRange,plotRange)
            plt.title(labels[e])
            plt.show()
           
             
            print('e: ', e)
            NILS2D = np.array([interferenceGratingModelsJK.NILS(ip,xP[e], pitch/4, show=False) for ip in np.transpose(np.array(iP))])
          
            FOURIERC2D  = [interferenceGratingModelsJK.gratingContrastFourier(ip,x*1e6, show=False) for ip, x in zip(iP,xP)]
            #FOURIERC2D = [[0,1] for ip, x in zip(iP,xP)]
            fC = np.mean([f[0] for f in FOURIERC2D])
            
            NNILS = [len(a) for a in NILS2D[:,2]]
            print(NILS2D[:,9][0:np.min(NNILS)-1])
            NILS   = [a[0:np.min(NNILS)-1] for a in NILS2D[:,2]]
            NILS3s = NILS2D[:,9][0:np.min(NNILS)-1] #[a[0:np.min(NNILS)-1] for a in NILS2D[:,9]]
            NILSrmsd = NILS2D[:,8][0:np.min(NNILS)-1] #[a[0:np.min(NNILS)-1] for a in NILS2D[:][8]]
            #LW     = [a[0:np.min(NNILS)-1] for a in NILS2D[:,3]]
            
            #NILS = np.stack(NILS2D[:,2])
            
     
            
            
            rmsNILS = np.sqrt(np.mean(np.square(NILS)))
            #rmsdNILS = 
            
            
            # THis is the 2D NILS distribution
            plt.imshow(NILS)
            plt.title('NILS - 2D dist')
            plt.colorbar()
            plt.show()
            
            plt.plot(np.mean(NILS,axis=0))
            plt.title('NILS - 1D dist')
            plt.show()
     
            avNILS = np.mean(NILS)

            nils3s.append(NILS3s)
            nilsrmsD.append(NILSrmsd)
            fourierC2d.append(fC)
            nils2d.append(avNILS)
            nils2dRMS.append(rmsNILS)

        LW = [interferenceGratingModelsJK.LWR(i,xP[e], pitch/4, debug=False) for i in images]
        #disable LWR for speed - testing Fourier
        #LW = [[[0], 0, 0, 0] for i in images]
        
        michelsonC2d = [interferenceGratingModels.gratingContrastMichelson(i) for i in images]
        rmsC2d = [interferenceGratingModels.gratingContrastRMS(i) for i in images]
        compositeC2d = [interferenceGratingModels.meanDynamicRange(i) for i in images] #, mdrC, imbalanceC 
#        nilsC2d = [interferenceGratingModels.NILS(i,x, pitch/4, show=False) for i, x in zip(images, xP)]
        #fourierC2d = [interferenceGratingModels.gratingContrastFourier(i,x*1e6, show=False) for i, x in zip(images,xP)] #Cf,  Am, Fr, peakFr - Still unsure but seems good
        fidel2d = [interferenceGratingModelsJK.fidelity(i,I2d) for i in images]   # fidelity based on comparison to model


        # This is is line width error
        
#        LWlist = [np.array(f[0]).flatten() for f in LW]
#        plt.imshow(LW)
#        plt.colorbar()
#        plt.title('LW')
#        plt.show()
        
        lwRMS = [f[1] for f in LW]
        plt.plot(lwRMS)
        plt.title('LW rms')
        plt.show()
        
        LWmean = [np.mean(f[0]) for f in LW]
        plt.plot(LWmean)
        plt.title('LW mean')
        plt.show()
            
     
        dlwRMS = [f[2] for f in LW]
        plt.plot(dlwRMS)
        plt.title('LW rmsd')
        plt.show()

        LWR = [f[3] for f in LW]
        plt.plot(LWR)
        plt.title('LWR')
        plt.show()
        
        


        minLen = np.min([len(a[0]) for a in LW])
        LW2d = np.stack([f[0][0:minLen] for f in LW])
        plt.imshow(LW2d,aspect=11)
        plt.show()
        stepy = 2.658184246878093e-07
#        
#        xvals = [np.mean(LW2d)*x for x in range(minLen)]
#        ypos = np.arange(0, n, stepy)
#        ylabels = ypos[::5]
#        nlabels=5
#        stepx = int(minLen / (nlabels-1))
#        xpos = np.arange(0,minLen,stepx)
#        xlabels = xvals[::stepx]
#        plt.xticks(xpos,xlabels)
#        plt.yticks(ypos  ,ylabels)
#        plt.title('LW 2d')
#
#        plt.show()

      
        if split:
            fig, axs = plt.subplots(3,3)
            axs[0,0].plot(sigma[0:5], michelsonC2d[0:5], 'x:')
            axs[0,0].plot(sigma[5:10], michelsonC2d[5:10], 'x:')
            axs[0,0].plot(sigma[10:15], michelsonC2d[10:15], 'x:')
            axs[0,0].plot(sigma[20:25], michelsonC2d[20:25], 'x:')
            axs[0,0].plot(sigma[15:20], michelsonC2d[15:20], 'x:')
            axs[0,0].set_title("Michelson")
            axs[0,0].set_ylabel("Contrast")
            # axs[0,0].legend(loc='lower left')
            axs[0,1].plot(sigma[0:5], rmsC2d[0:5], 'x:')
            axs[0,1].plot(sigma[5:10], rmsC2d[5:10], 'x:')
            axs[0,1].plot(sigma[10:15], rmsC2d[10:15], 'x:')
            axs[0,1].plot(sigma[20:25], rmsC2d[20:25], 'x:')
            axs[0,1].set_title("RMS")
            axs[0,2].plot(sigma[0:5], [c[0] for c in compositeC2d[0:5]], 'x:')
            axs[0,2].plot(sigma[5:10], [c[0] for c in compositeC2d[5:10]], 'x:')
            axs[0,2].plot(sigma[10:15], [c[0] for c in compositeC2d[10:15]], 'x:')
            axs[0,2].plot(sigma[15:20], [c[0] for c in compositeC2d[15:20]], 'x:')
            axs[0,2].plot(sigma[20:25], [c[0] for c in compositeC2d[20:25]], 'x:')
            axs[0,2].set_title("Composite")
            # axs[1,0].plot(sigma[0:5], fourierC2d[0:5], 'x:')
            # axs[1,0].plot(sigma[5:10], fourierC2d[5:10], 'x:')
            # axs[1,0].plot(sigma[10:15], fourierC2d[10:15], 'x:')
            # axs[1,0].plot(sigma[15:20], fourierC2d[15:20], 'x:')
            # axs[1,0].set_title("Fourier")
            axs[1,0].set_ylabel("Contrast")
            axs[1,1].set_title("NILS")
            axs[1,1].plot(sigma[0:5], fidel[0:5], 'x:')
            axs[1,1].plot(sigma[5:10], fidel[5:10], 'x:')
            axs[1,1].plot(sigma[10:15], fidel[10:15], 'x:')
            axs[1,1].plot(sigma[15:20], fidel[15:20], 'x:')
            axs[1,1].plot(sigma[20:25], fidel[20:25], 'x:')
            axs[1,1].set_title("Fidelity")
            axs[1,2].plot(sigma[0:5], nils2d[0:5], 'x:')
            axs[1,2].plot(sigma[5:10], nils2d[5:10], 'x:')
            axs[1,2].plot(sigma[10:15], nils2d[10:15], 'x:')
            axs[1,2].plot(sigma[15:20],nils2d[15:20], 'x:')
            axs[1,2].plot(sigma[20:25],nils2d[20:25], 'x:')
            axs[1,2].set_title("NILS - mean")
            axs[1,2].set_ylabel("NILS")
            axs[2,0].plot(sigma[0:5], nils2dRMS[0:5], 'x:')
            axs[2,0].plot(sigma[5:10], nils2dRMS[5:10], 'x:')
            axs[2,0].plot(sigma[10:15], nils2dRMS[10:15], 'x:')
            axs[2,0].plot(sigma[15:20], nils2dRMS[15:20], 'x:')
            axs[2,0].plot(sigma[20:25], nils2dRMS[20:25], 'x:')
            axs[2,0].set_title("NILS - RMS")
            axs[2,0].set_ylabel("RMS")
            axs[2,1].set_title("Line Width - RMS")
            axs[2,1].plot(sigma[0:5], lwRMS[0:5], 'x:')
            axs[2,1].plot(sigma[5:10], lwRMS[5:10], 'x:')
            axs[2,1].plot(sigma[10:15], lwRMS[10:15], 'x:')
            axs[2,1].plot(sigma[15:20], lwRMS[15:20], 'x:')
            axs[2,1].plot(sigma[20:25], lwRMS[20:25], 'x:')
            axs[2,2].plot(sigma[0:5], LWR[0:5], 'x:')
            axs[2,2].plot(sigma[5:10], LWR[5:10], 'x:')
            axs[2,2].plot(sigma[10:15], LWR[10:15], 'x:')
            axs[2,2].plot(sigma[15:20],LWR[15:20], 'x:')
            axs[2,2].plot(sigma[20:25],LWR[20:25], 'x:')
            axs[2,2].set_title("LWR")
            axs[2,1].set_ylabel("LWR")
            # for ax in fig.axes:
                # ax.set_xticklabels(labels, rotation=45, ha='right')
            axs[1,0].set_xlabel('\u03C3 [nm]')
            axs[1,1].set_xlabel('\u03C3 [nm]')
            axs[1,2].set_xlabel('\u03C3 [nm]')
            fig.tight_layout()
            # fig.subplots_adjust(bottom=0.5,hspace=5.33)   ##  Need to play with this number.
            axs[1,1].legend(labels=['$C_y$ = ' + str(c) for c in [2,4,6,8,10]], bbox_to_anchor=(1.75,-0.35), ncol=5) #loc="lower center"
            # if save:
                # plt.savefig(savePath + 'contrastAll.pdf')
                # plt.savefig(savePath + 'contrastAll.png', dpi=2000)
            plt.show()
            
            
            # big plot of LWR
            
            plt.plot(sigma[0:5], LWR[0:5], 'o-')
            plt.plot(sigma[5:10], LWR[5:10], 'o-')
            plt.plot(sigma[10:15], LWR[10:15], 'o-')
            plt.plot(sigma[15:20],LWR[15:20], 'o-')
            plt.plot(sigma[20:25],LWR[20:25], 'o-')
            #plt.ylim([1e-10,8e-9])
            plt.title("LWR")
            plt.ylabel("LWR")
            plt.xlabel("RMS")
            
            
            
            
            
            
        else:
            fig, axs = plt.subplots(3,3)
            axs[0,0].plot(sigma, michelsonC2d, 'x:')
            axs[0,0].set_title("Michelson")
            axs[0,0].set_ylabel("Contrast")
            axs[0,1].plot(sigma, rmsC2d, 'x:')
            axs[0,1].set_title("RMS")
            axs[0,2].plot(sigma, [c[0] for c in compositeC2d], 'x:')
            axs[0,2].set_title("Composite")
            axs[1,0].plot(sigma, fourierC2d, 'x:')
            axs[1,0].set_title("Fourier")
            axs[1,0].set_ylabel("Contrast")
            axs[1,1].plot(sigma[1::], fidel2d, 'x:')
            axs[1,1].set_title("Fidelity")
            axs[1,2].plot(sigma, nils2d, 'x:')
            axs[1,2].set_title("NILS - mean")
            axs[1,2].set_ylabel("NILS")
            axs[2,0].plot(sigma, nils2dRMS, 'x:')
            axs[2,0].set_title("NILS - RMS")
            axs[2,0].set_ylabel("RMS")
            axs[2,1].plot(sigma, lwRMS, 'x:')
            axs[2,1].set_title("Line Width - RMS")
            axs[2,2].plot(sigma, dlwRMS, 'x:')
            axs[2,2].set_title("LWR")
            axs[2,2].set_ylabel("LWR")
            
            # for ax in fig.axes:
            #     ax.set_xticklabels(labels, rotation=45, ha='right')
            # axs[1,0].set_xlabel('Slit Width')
            # axs[1,1].set_xlabel('Slit Width')
            # axs[1,2].set_xlabel('Slit Width')
            fig.tight_layout()
            # if save:
            #     plt.savefig(savePath + 'contrastAllCy10.pdf')
            #     plt.savefig(savePath + 'contrastAllCy10.png', dpi=2000)
            plt.show()
    else:
        pass
    
#    
#dataStructure = [sigma, cY,
#                  michelsonC2d,rmsC2d,[c[0] for c in compositeC2d],
#                  fidel2d,
#                  nils2d,
#                  nils2dRMS,
#                  lwRMS,
#                  LWR]
#
## print(len(labels))
## print("Shape of data structure: ", np.shape(dataStructure))
#import pandas as pd
## dF = pd.DataFrame(np.concatenate([labels,avPeaks,sumPeaks,rmsPeaks,
##                              michelsonC,rmsC,[c[0] for c in compositeC],
##                              [f[0] for f in fourierC],[n[0] for n in nilsC]]),
#dF = pd.DataFrame(np.array(dataStructure).T,
#                  columns=['RMS roughness','Corr Length',
#                           'Michelson C', 'rms C', 'composite C',
#                           'fidelity',
#                           'NILS','NILS-rms','LW','LWR'])
#correlations = dF.corr() 
#import seaborn as sns
#
#sns.heatmap(correlations,cmap='vlag',vmin=-1,vmax=1)
#plt.show()
#
#
