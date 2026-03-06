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


def round_sig(x, sig=2):
    from math import log10, floor
    if x != 0:
        return round(x, sig-int(floor(log10(abs(x))))-1)
    else:
        return x

dirPath = '/user/home/opt/xl/xl/experiments/maskRoughnessRedo/data/'
savePath = './x/'
order = range(0,25)
cY = [2,2,2,2,2,4,4,4,4,4,6,6,6,6,6,8,8,8,8,8,10,10,10,10,10]
sigma = [0.5,1.0,1.5,2.0,2.5,0.5,1.0,1.5,2.0,2.5,0.5,1.0,1.5,2.0,2.5,0.5,1.0,1.5,2.0,2.5,0.5,1.0,1.5,2.0,2.5]
files = [str(o) + '/' + str(o) + 'intensity.tif' for o in order]

labels =  ['\u03C3 = 0.5 nm ','\u03C3 = 1.0 nm ','\u03C3 = 1.5 nm ','\u03C3 = 2.0 nm','\u03C3 = 2.5 nm',
           '\u03C3 = 0.5 nm ','\u03C3 = 1.0 nm ','\u03C3 = 1.5 nm ','\u03C3 = 2.0 nm','\u03C3 = 2.5 nm',
           '\u03C3 = 0.5 nm ','\u03C3 = 1.0 nm ','\u03C3 = 1.5 nm ','\u03C3 = 2.0 nm','\u03C3 = 2.5 nm',
           '\u03C3 = 0.5 nm ','\u03C3 = 1.0 nm ','\u03C3 = 1.5 nm ','\u03C3 = 2.0 nm','\u03C3 = 2.5 nm',
           '\u03C3 = 0.5 nm ','\u03C3 = 1.0 nm ','\u03C3 = 1.5 nm ','\u03C3 = 2.0 nm','\u03C3 = 2.5 nm']
#['\u03C3 = 0.5 nm ','\u03C3 = 1.0 nm ','\u03C3 = 1.5 nm ','\u03C3 = 2.0 nm','\u03C3 = 2.5 nm']
# ['\u03C3 = 0.5 nm ','\u03C3 = 1.0 nm ','\u03C3 = 1.5 nm ','\u03C3 = 2.0 nm','\u03C3 = 2.5 nm',
#           '\u03C3 = 0.5 nm ','\u03C3 = 1.0 nm ','\u03C3 = 1.5 nm ','\u03C3 = 2.0 nm','\u03C3 = 2.5 nm',
#           '\u03C3 = 0.5 nm ','\u03C3 = 1.0 nm ','\u03C3 = 1.5 nm ','\u03C3 = 2.0 nm','\u03C3 = 2.5 nm',
#           '\u03C3 = 0.5 nm ','\u03C3 = 1.0 nm ','\u03C3 = 1.5 nm ','\u03C3 = 2.0 nm','\u03C3 = 2.5 nm',
#           '\u03C3 = 0.5 nm ','\u03C3 = 1.0 nm ','\u03C3 = 1.5 nm ','\u03C3 = 2.0 nm','\u03C3 = 2.5 nm']
legendTitle ='$C_y =$ 2 nm' # None #'$C_y =$ 10 nm'

# Specify analysis - turn plotting on and off
show = False                          # show initial tiffs and entire profiles
plotTogether = False                   # plot aerial image profiles together
contrast = True                        # compute contrast metrics
normalise = False                      # normalise profiles when plotting together
subtractAperture = False               # subtract intensity from aperture
plotFromEq = False                      # plot ideal intensity from equation
split = True                           # split into groups by correlation length (for ploting all aerial images together)
twoD = True                           # calculate two-dimensional contrast (still in development)
save = False                           # save plots to savePath




N = 1000                            # number of pixels to take for line profile  - 1200 for roughness aerial images
n = 15                             # number of pixels to average over for line profile - 15 for roughness aerial images
plotRange = 100                       # range of aerial image plot in nm


# res and middle pixels of images
res =   [(2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07),
         (2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07),
         (2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07),
         (2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07),
         (2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07)]

#[(2.5011240434424064e-09, 2.658184246883298e-07),
#         (2.501124043067869e-09, 2.658184246878093e-07),
#         (2.501124043067869e-09, 2.658184246878093e-07),
#         (2.501124043067869e-09, 2.658184246878093e-07),
#         (2.501124043067869e-09, 2.658184246878093e-07),
#         (2.501124043067869e-09, 2.658184246878093e-07)]

# [(2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07),
#         (2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07),
#         (2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07),
#         (2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07),
#         (2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07)]

mid =   [(64, 12899),(64, 12899),(64, 12899),(64, 12899),(64, 12899),
         (64, 12899),(64, 12899),(64, 12899),(64, 12899),(64, 12899),
         (64, 12899),(64, 12899),(64, 12899),(64, 12899),(64, 12899),
         (64, 12899),(64, 12899),(64, 12899),(64, 12899),(64, 12899),
         (64, 12899),(64, 12899),(64, 12899),(64, 12899),(64, 12899)]
#[(65, 12899), 
#         (65, 12899),
#         (65, 12899),
#         (65, 12899),
#         (65, 12899),
#         (65, 12899)]
# [(64, 12899),(64, 12899),(64, 12899),(64, 12899),(64, 12899),
#         (64, 12899),(64, 12899),(64, 12899),(64, 12899),(64, 12899),
#         (64, 12899),(64, 12899),(64, 12899),(64, 12899),(64, 12899),
#         (64, 12899),(64, 12899),(64, 12899),(64, 12899),(64, 12899),
#         (64, 12899),(64, 12899),(64, 12899),(64, 12899),(64, 12899)]

pitch = 100e-9

# read from files - create profiles and images of sampled range
tiffs = [tifffile.imread(dirPath + f) for f in files]
images = [t[m[0]-n:m[0]+n,m[1]-N:m[1]+N] for t, m in zip(tiffs,mid)]
profiles = [i.mean(0) for i in images] #[t[m[0]-n:m[0]+n,m[1]-N:m[1]+N] for t, m in zip(tiffs,mid)]
xP = [np.linspace(-N*r[0], N*r[0],2*N) for r in res]
yP = [np.linspace(-n*r[1], n*r[1],2*n) for r in res]

idealTif = tifffile.imread(dirPath + 'ideal27/ideal27intensity.tif')
idealImage = idealTif[mid[0][0]-n:mid[0][0]+n,mid[0][1]-N:mid[0][1]+N]

''' define interference grating parameters'''
wl = 6.710553853647976e-9 # wavelength in m

# Amplitude of both beams (assumed equal)
A = 0.12e5 # 0.37e5 #0.3e5  # this may be scaled to  match simulated intensity
k = 2*np.pi/wl
m = 1 # order of diffracted beams from each grating
d = 100e-9 #24e-9 #100e-9 # grating spacing
# angle between the beams from each grating
theta = np.arcsin( m *wl/d)
IP = interferenceGratingModelsJK.interferenceIntensity(xP[0],k,theta,A=A)

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
            axs[i].imshow(tiffs[i], aspect=5)
            axs[i].set_title(labels[i])
        axs[int(len(tiffs)/2)].set_ylabel('y-position [pixels]')
        axs[len(tiffs)-1].set_xlabel('x-position [pixels]')
        fig.tight_layout()
        plt.show()
        
        fig, axs = plt.subplots(int(len(tiffs)),1)
        for i in range(len(tiffs)):
            axs[i].imshow(images[i], aspect=15)
            # axs[i].set_title(labels[i])
            axs[i].set_xticklabels([round_sig(np.max(xP[i])*x*1e9) for x in [0,-1, -3/5,-1/5,1/5,3/5,1]])
            axs[i].set_yticklabels([round_sig(np.max(yP[i])*y*1e9) for y in [0,-1, -2/5,2/5,1]])
        axs[int(len(tiffs)/2)].set_ylabel('y-position [nm]')
        axs[len(tiffs)-1].set_xlabel('x-position [nm]')
        fig.tight_layout()
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

if plotTogether:
    if normalise:
        for i,p in enumerate(profiles):
            plt.plot(xP[i]*1e9,p/np.max(p), label=labels[i])
        plt.ylabel('Intensity [a.u]')
    else:
        for i,p in enumerate(profiles):
            plt.plot(xP[i]*1e9,p, label=labels[i])
        plt.ylabel('Intensity [ph/s/.1%bw/mm$^2$]')
    if plotFromEq:
        if subtractAperture:
            profileSubtract = profiles[2]*2/np.max(profiles[2]) - profiles[1]/np.max(profiles[1])  - profiles[0]/4*np.max(profiles[0])
            EQplus = IP/np.max(IP) + profiles[1]/np.max(profiles[1]) + profiles[0]/np.max(profiles[0])
            plt.plot(xP[0]*1e9,profileSubtract/np.max(profileSubtract), label = 'aerial image - subtacted envelope')
            plt.plot(xP[0]*1e9,EQplus/np.max(EQplus), label = 'Eq.2.3.45 - added envelope')
        else:
            plt.plot(xP[0]*1e9,IP, ':', label='Eq.2.3.45')
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
    nilsC = [interferenceGratingModelsJK.NILS(p,x, pitch/4, show=False) for p, x in zip(profiles, xP)]
    fourierC = [interferenceGratingModelsJK.gratingContrastFourier(p,x*1e6, show=False) for p, x in zip(profiles,xP)] #Cf,  Am, Fr, peakFr - Still unsure but seems good
    fidel = [interferenceGratingModelsJK.fidelity(p,IP) for p in profiles]   # fidelity based on comparison to model
    
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
        axs[0,0].plot(labels, michelsonC, 'x:')
        axs[0,0].set_title("Michelson")
        axs[0,0].set_ylabel("Contrast")
        axs[0,1].plot(labels, rmsC, 'x:')
        axs[0,1].set_title("RMS")
        axs[0,2].plot(labels, [c[0] for c in compositeC], 'x:')
        axs[0,2].set_title("Composite")
        axs[1,0].plot(labels, [n[5] for n in  nilsC], 'x:')
        axs[1,0].set_title("NILS - rms")
        axs[1,0].set_ylabel("Contrast")
        axs[1,1].set_title("NILS")
        axs[1,1].plot(labels, fidel, 'x:')
        axs[1,1].set_title("Fidelity")
        axs[1,2].plot(labels, [n[0] for n in nilsC], 'x:')
        axs[1,2].set_title("NILS - mean")
        axs[1,2].set_ylabel("NILS")
        for ax in fig.axes:
            ax.set_xticklabels(labels, rotation=45, ha='right')
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
        lwRMS = []
        dlwRMS = []
        fourierC2d = []
        print("getting line profiles down every pixel")
        for e, i in enumerate(images):
            iP = [i[:,a] for a in range(0,np.shape(i)[1])]
            print("shape:", np.shape(iP))
            plt.plot(xP[e]*1e9,[p for p in iP])
            plt.xlim(-plotRange,plotRange)
            plt.title(labels[e])
            plt.show()
           
           #LWRe, edges = interferenceGratingModelsJK.LWR(iP,xP[e][1]-xP[e][0], dim=0)
#            print('LWR: ', LWRe)
#            plt.imshow(edges, aspect = 0.1)
#            plt.colorbar()
#            plt.title('Edges detected')
#            plt.show()
            
            plt.imshow(iP, aspect = 0.1)
            plt.colorbar()
            plt.title('Lines')
            plt.show()
            
            #print('e: ', e)
            NILS2D = np.array([interferenceGratingModelsJK.NILS(ip,xP[e], pitch/4, show=False) for ip in np.transpose(np.array(iP))])
            

                
            
            #FOURIERC2D  = [interferenceGratingModelsJK.gratingContrastFourier(ip,x*1e6, show=False) for ip, x in zip(iP,xP)]
            #FOURIERC2D = [[0,1] for ip, x in zip(iP,xP)]
            #fC = np.mean([f[0] for f in FOURIERC2D])
            
            NNILS = [len(a) for a in NILS2D[:,2]]
            NILS   = [a[0:np.min(NNILS)-1] for a in NILS2D[:,2]]
            #LW     = [a[0:np.min(NNILS)-1] for a in NILS2D[:,3]]
            #plt.hist(np.array(LW).flatten(),bins=7)
            #plt.title('LW histogram')
            #plt.show()
            
            NILS = np.stack(NILS2D[:,2])
            #LW  =  np.stack(NILS2D[:,3])
            #rmsLW   = np.sqrt(np.mean(np.square(LW)))

            #LWd = np.subtract(pitch/4,LW)
            #rmsdLW =  np.sqrt(np.mean(np.square(LWd)))
            
            
            
                        # This is is line width error
            #plt.imshow(abs(LWd))
            #plt.title('LW - error')
            #plt.colorbar()
            #plt.show()
            
            #plt.plot(np.mean(LW,axis=0))
            #plt.title('LW - 1D dist')
            #plt.show()
            
            
            
            #rmsNILS = np.sqrt(np.mean(np.square(NILS)))
          
            
            
            ## THis is the 2D NILS distribution
            #plt.imshow(NILS)
            #plt.title('NILS - 2D dist')
            #plt.colorbar()
            #plt.show()
            
            #plt.plot(np.mean(NILS,axis=0))
            #plt.title('NILS - 1D dist')
            #plt.show()
            
            # This is the 2D linewidth distribution.
            #plt.imshow(LW)
            #plt.title('LW - 2D dist')
            #plt.colorbar()
            #plt.show()
            

      
            #added excep
#            try:
            #avNILS = np.mean(NILS)
#            except ValueError:
#                avNILS = 0

               
           

            
            #fourierC2d.append(fC)
            #nils2d.append(avNILS)
            #nils2dRMS.append(rmsNILS)
            #lwRMS.append(rmsLW)
            #dlwRMS.append(rmsdLW)
            
        
        michelsonC2d = [interferenceGratingModels.gratingContrastMichelson(i) for i in images]
        rmsC2d = [interferenceGratingModels.gratingContrastRMS(i) for i in images]
        compositeC2d = [interferenceGratingModels.meanDynamicRange(i) for i in images] #, mdrC, imbalanceC 
#        nilsC2d = [interferenceGratingModels.NILS(i,x, pitch/4, show=False) for i, x in zip(images, xP)]
#        fourierC2d = [interferenceGratingModels.gratingContrastFourier(i,x*1e6, show=False) for i, x in zip(images,xP)] #Cf,  Am, Fr, peakFr - Still unsure but seems good
        fidel2d = [interferenceGratingModelsJK.fidelity(i,idealImage) for i in images]   # fidelity based on comparison to model
        
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
             axs[2,2].plot(sigma[0:5], dlwRMS[0:5], 'x:')
             axs[2,2].plot(sigma[5:10], dlwRMS[5:10], 'x:')
             axs[2,2].plot(sigma[10:15], dlwRMS[10:15], 'x:')
             axs[2,2].plot(sigma[15:20],dlwRMS[15:20], 'x:')
             axs[2,2].plot(sigma[20:25],dlwRMS[20:25], 'x:')
             axs[2,2].set_title("dLW - RMS")
             axs[2,1].set_ylabel("Line Width")
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
             axs[2,2].set_title("dLW - RMS")
             axs[2,2].set_ylabel("Line Width")
             
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
    
dataStructure = [sigma, cY,
                   michelsonC2d,rmsC2d,[c[0] for c in compositeC2d],
                   fidel2d,
                   nils2d,
                   nils2dRMS,
                   lwRMS,
                   dlwRMS]
 
# print(len(labels))
# print("Shape of data structure: ", np.shape(dataStructure))
import pandas as pd
#dF = pd.DataFrame(np.concatenate([labels,avPeaks,sumPeaks,rmsPeaks,
#                              michelsonC,rmsC,[c[0] for c in compositeC],
#                              [f[0] for f in fourierC],[n[0] for n in nilsC]]),
dF = pd.DataFrame(np.array(dataStructure).T,
                   columns=['RMS roughness','Corr Length',
                            'Michelson C', 'rms C', 'composite C',
                            'fidelity',
                            'NILS','NILS-rms','LW','dLW'])
correlations = dF.corr() 
import seaborn as sns
 
sns.heatmap(correlations,cmap='vlag',vmin=-1,vmax=1)
plt.show()


import pickle
LW = pickle.load( open("LW.pickle","rb") )

sigma3 = []
LWRx = []
means =[]
for l in LW:
    stdDev3 = 3 * np.std( l[0] )
    sigma3.append(stdDev3)
    LWRx.append(l[3])
    varianceFromMean = np.var(l[0])
    variance = sum((xi-m)**2 for xi in l[0]) / len(l[0])
    mean = np.mean(l[0])
    means.append(mean)
    print('3sigma = {}, variance (f. mean) = {}, variance = {}, mean = {}'.format(stdDev3, varianceFromMean, variance, mean))
    plt.plot(l[0])
    plt.show()
    
plt.plot(LW[3][:])
plt.plot(LWR[5:])



