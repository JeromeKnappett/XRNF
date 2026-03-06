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


def round_sig(x, sig=2):
    from math import log10, floor
    if x != 0:
        return round(x, sig-int(floor(log10(abs(x))))-1)
    else:
        return x

dirPath = '/user/home/opt/xl/xl/experiments/maskLER_retry2/data/'
savePath = None #'/home/jerome/Documents/MASTERS/Figures/plots/roughness/'
order = ['0nm','3nm','4nm','5nm', '6nm']#range(0,25)
cY = [2,2,2,2,2,4,4,4,4,4,6,6,6,6,6,8,8,8,8,8,10,10,10,10,10]
sigma = [0.0,3.0,4.0,5.0,6.0]
files = [str(o) + '/' + str(o) + '.pkl' for o in order]

print([i for i in order])
#    [dirPath + 'ideal27/ideal27intensity.tif',
#         '/user/home/opt/xl/xl/experiments/correctedWBS/data/ideal/idealintensity.tif']  #[str(o) + '/' + str(o) + 'intensity.tif' for o in order]

labels = ['\u03C3 = 0.0 nm ','\u03C3 = 3.0 nm ','\u03C3 = 4.0 nm ','\u03C3 = 5.0 nm','\u03C3 = 6.0 nm']#,'\u03C3 = 3.0 nm','\u03C3 = 3.5 nm','\u03C3 = 4.0 nm']

legendTitle = None #'$C_y =$ 2 nm' # None #'$C_y =$ 10 nm'

# Specify analysis - turn plotting on and off
show = True                          # show initial tiffs and entire profiles
plotTogether = True                   # plot aerial image profiles together
contrast = True                       # compute contrast metrics
efficiency = True
normalise = False                      # normalise profiles when plotting together
subtractAperture = False               # subtract intensity from aperture
plotFromEq = True                      # plot ideal intensity from equation
split = False                           # split into groups by correlation length (for ploting all aerial images together)
twoD = True                           # calculate two-dimensional contrast (still in development)
save = False                           # save plots to savePath
fromPickle = True
toPickle = True

N = 1500#2250 //2                         # number of pixels to take for line profile  - 1200 for roughness aerial images
n = 250  //2                            # number of pixels to average over for line profile - 15 for roughness aerial images
plotRange = 1000                       # range of aerial image plot in nm

#middle pixels of images
mid = np.full((np.shape(files)[0],2), (460, 8001))

pitch = 100e-9

# read from files - create profiles and images of sampled range
if fromPickle:
    picks = [pickle.load(open(dirPath + f, 'rb')) for f in files]
    tiffs = [p[0] for p in picks]
    res = [(p[1],p[2]) for p in picks]
#    print(res)
else:
    res = np.full((np.shape(files)[0],2), [2.5011882651601634e-09, 2.426754806976689e-07])
    try:
        tiffs = [tifffile.imread(dirPath + f) for f in files]
    except FileNotFoundError:
        tiffs = [tifffile.imread(f) for f in files]
    
images = [t[m[0]-n:m[0]+n,m[1]-N:m[1]+N] for t, m in zip(tiffs,mid)]
profiles = [i.mean(0) for i in images] #[t[m[0]-n:m[0]+n,m[1]-N:m[1]+N] for t, m in zip(tiffs,mid)]
xP = [np.linspace(-N*r[0], N*r[0],2*N) for r in res]
yP = [np.linspace(-n*r[1], n*r[1],2*n) for r in res]




if toPickle:
    for i, p in enumerate(images):
        with open(dirPath + str(order[i]) + 'AerialImage.pkl', "wb") as f:
            pickle.dump([p, res[i], mid[i]], f)


idealTif = tifffile.imread('/user/home/opt/xl/xl/experiments/correctedAngle_roughness/data/ideal/idealintensity.tif')
idealImage = idealTif[mid[0][0]-n:mid[0][0]+n,mid[0][1]-N:mid[0][1]+N]

''' define interference grating parameters'''
wl = 6.710553853647976e-9 # wavelength in m

# Amplitude of both beams (assumed equal)

A = 10*np.sqrt(np.max(profiles))/21
#A = 1.8e5 # 0.37e5 #0.3e5  # this may be scaled to  match simulated intensity
k = 2*np.pi/wl
m = 1 # order of diffracted beams from each grating
d = 100e-9 #24e-9 #100e-9 # grating spacing

# angle between the beams from each grating
theta = np.arcsin(m*wl/d)
IP = interferenceGratingModelsJK.interferenceIntensity(xP[0],k,theta,A=A)
I2d = np.tile(IP,(2*n,1))

fig, axs = plt.subplots(1,2)
axs[0].imshow(images[0],aspect='auto')
axs[1].imshow(I2d,aspect='auto')

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
            axs[i].imshow(images[i], aspect='auto')
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

plt.clf()
plt.close()

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

if efficiency:
    import efficiency
    inPick = pickle.load(open(dirPath + '/incident/incident.pkl','rb'))
    inTiff = inPick[0]
    inRes = (inPick[1],inPick[2])
   
    E0,E1 = efficiency.getAerialImageEfficiency(inTiff,tiffs,inRes,res,mid,G=4.0e-6,D=10.0e-6,
                                                extra=(1000,100),#(1300,100),
                                                verbose=True,show=True)

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
    # %%
    if twoD:
        nils2d = []
        nils2dRMS = []
        nils3s = []
        nilsrmsD = []
        nilsSTD = []
       
        fourierC2d = []
        M2D = []
        C2D= []
        print("getting line profiles down every pixel")
        for e, i in enumerate(images):
            iP = [i[:,a] for a in range(0,np.shape(i)[1])]
            print("shape:", np.shape(iP))
            plt.plot(xP[e]*1e9,[p for p in iP])
            plt.xlim(-plotRange,plotRange)
            plt.title(labels[e])
            plt.show()
           
            m2D = [interferenceGratingModels.gratingContrastMichelson(p) for p in iP]
            m2D = np.mean(m2D)
            M2D.append(m2D)
            
            c2D =  [interferenceGratingModels.meanDynamicRange(p) for p in iP]
            c2D = np.mean([c[0] for c in c2D])
            C2D.append(c2D)
            
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
           
    # return meanNILS,  meanLW, NILS, LW, rmsNILS, rmsLW, rmsdLW, p1, rmsdNILS, stdNILS
     
            stdNILS = np.std(NILS)#/np.mean(NILS)
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
            nilsSTD.append(stdNILS)
        LW = [interferenceGratingModelsJK.LWRChunkWise(i,xP[e], pitch/4, show =True, debug=False) for i in images]
        # LW = [(interferenceGratingModelsJK.LWR_JK(i,xP[e], pitch/4, debug=True)) for i in images]
        #disable LWR for speed - testing Fourier
        #LW = [[[0], 0, 0, 0] for i in images]
       
        michelsonC2d = [interferenceGratingModels.gratingContrastMichelson(i) for i in images]
        rmsC2d = [interferenceGratingModels.gratingContrastRMS(i) for i in images]
        compositeC2d = [interferenceGratingModels.meanDynamicRange(i) for i in images] #, mdrC, imbalanceC
#        nilsC2d = [interferenceGratingModels.NILS(i,x, pitch/4, show=False) for i, x in zip(images, xP)]
        #fourierC2d = [interferenceGratingModels.gratingContrastFourier(i,x*1e6, show=False) for i, x in zip(images,xP)] #Cf,  Am, Fr, peakFr - Still unsure but seems good
        fidel2d = [interferenceGratingModelsJK.fidelity(i,I2d) for i in images]   # fidelity based on comparison to model
        
        # NILS mean: 1.2224229538022116
        # NILS rms: 1.3071862846507827
        # LW mean: 2.505449312098684e-08
        # LW rms: 2.5600423059289736e-08
        # LW rmsd: 5.258710418442611e-09
        # NILS mean: 1.206876656717402
        # NILS rms: 1.296013808543514
        # LW mean: 2.505449312098684e-08
        # LW rms: 2.5608638698179333e-08
        # LW rmsd: 5.298561165477978e-09
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
        
        
        CDU = [f[4] for f in LW]
        plt.plot(CDU)
        plt.title('CDU')
        plt.show()
        
        CLR = [f[5] for f in LW]
        plt.plot(CLR)
        plt.title('CLR')
        plt.show()
        
        print(f"LWR: {LWR}")
        print(f"CDU: {CDU}")
        print(f"E0 = {E0}")
       


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

      # %%
        if split:
            sigma = np.reshape(sigma,(5,5))
            michelsonC2d = np.reshape(michelsonC2d,(5,5))
            rmsC2d = np.reshape(rmsC2d,(5,5))
            compositeC2d = np.reshape(compositeC2d,(5,5))
            nils2d = np.reshape(nils2d,(5,5))
            nils2dRMS = np.reshape(nils2dRMS,(5,5))
            fidel = np.reshape(fidel,(5,5))
            LWR = np.reshape(LWR,(5,5))
            E0 = np.reshape(E0,(5,5))
            E1 = np.reshape(E1,(5,5))
       
            print(np.shape(michelsonC2d))
            fig, axs = plt.subplots(3,3)
           
            for s,mic,rms,com,fid,nil,nilrms,lwr,e0,e1 in zip(sigma,michelsonC2d,rmsC2d,compositeC2d,fidel,nils2d,nils2dRMS,LWR,E0,E1):
                axs[0,0].plot(s,mic,'x:')
                axs[0,1].plot(s,rms,'x:')
                axs[0,2].plot(s,com[0],'x:')
                axs[1,0].plot(s,fid,'x:')
                axs[1,1].plot(s,nil,'x:')
                axs[1,2].plot(s,nilrms,'x:')
                axs[2,0].plot(s,lwr,'x:')
                axs[2,1].plot(s,e0,'x:')
                axs[2,2].plot(s,e1,'x:')
            axs[0,0].set_title("Michelson")
            axs[0,0].set_ylabel("Contrast")
            axs[0,1].set_title("RMS")
            axs[0,2].set_title("Composite")
            axs[1,0].set_title('Fidelity')
            axs[1,0].set_ylabel("Fidelity")
            axs[1,1].set_title("NILS - mean")
            axs[1,2].set_title("NILS - RMS")
            axs[1,1].set_ylabel("NILS")
            axs[2,0].set_title("LWR")
            axs[2,0].set_ylabel("LWR [m]")
            axs[2,1].set_title("0 order efficiency")
            axs[2,2].set_title("Aerial image efficiency")
            axs[2,1].set_ylabel("Efficiency")
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
           
            # %%
        else:
            fig, axs = plt.subplots(3,3)
            axs[0,0].plot(sigma, michelsonC2d, 'x:')
            axs[0,0].set_title("Michelson")
            axs[0,0].set_ylabel("Contrast")
            axs[0,1].plot(sigma, rmsC2d, 'x:')
            axs[0,1].set_title("RMS")
            axs[0,2].plot(sigma, [c[0] for c in compositeC2d], 'x:')
            axs[0,2].set_title("Composite")
            axs[1,0].plot(sigma, fidel2d, 'x:')
            axs[1,0].set_title("Fidelity")
            axs[1,0].set_ylabel("Contrast")
#            axs[1,1].plot(sigma[1::], fidel2d, 'x:')
#            axs[1,1].plot(sigma, fidel2d, 'x:')
#            axs[1,1].set_title("Fidelity")
            axs[1,1].plot(sigma, nils2d, 'x:')
            axs[1,1].set_title("NILS - mean")
            axs[1,1].set_ylabel("NILS")
            axs[1,2].plot(sigma, nils2dRMS, 'x:')
            axs[1,2].set_title("NILS - RMS")
            axs[1,2].set_ylabel("RMS")
            axs[2,0].plot(sigma, LWR, 'x:')
            axs[2,0].set_title("LWR")
            axs[2,1].plot(sigma, E0, 'x:')
            axs[2,1].set_title("0 order efficiency")
            axs[2,1].set_ylabel("Efficiency")
            axs[2,2].plot(sigma, E1, 'x:')
            axs[2,2].set_title("Aerial image efficiency")
#            axs[2,2].set_ylabel("")
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
            # 
    else:
        pass
   
    # 
if split:
    dataStructure = [sigma.flatten(), cY,
                     michelsonC2d.flatten(),rmsC2d.flatten(),[c[0] for c in compositeC2d.flatten()],
                      fidel2d.flatten(),
                      nils2d.flatten(),
                      nilsSTD.flatten(),
                      LWR.flatten(),
                      E1.flatten()]
else:
    dataStructure = [sigma, #cY,
                     michelsonC2d,M2D,
                     rmsC2d,
                     [c[0] for c in compositeC2d],C2D,
                     fidel2d,
                     nils2d,
                     nilsSTD,
                     nilsrmsD,
                     LW, # changed to LW from LWR - may cause issues with plotting
                     E1,
                     E0]

import pickle
with open(dirPath + 'LWR.pkl', "wb") as f:
    pickle.dump(LWR, f)
with open(dirPath + 'dataStructure.pkl', "wb") as g:
    pickle.dump(dataStructure, g)
    
# print(len(labels))
# print("Shape of data structure: ", np.shape(dataStructure))
import pandas as pd
# dF = pd.DataFrame(np.concatenate([labels,avPeaks,sumPeaks,rmsPeaks,
#                              michelsonC,rmsC,[c[0] for c in compositeC],
#                              [f[0] for f in fourierC],[n[0] for n in nilsC]]),
    
for d in dataStructure:
    print(np.shape(d))

dF = pd.DataFrame([np.array(dataStructure).T],
                  columns=['RMS roughness',#'Corr Length',
                           'Michelson C', 'rms C', 'composite C',
                           'fidelity',
                           'NILS','NILS-std','LWR','Efficiency'])
correlations = dF.corr()
import seaborn as sns

sns.heatmap(correlations,cmap='vlag',vmin=-1,vmax=1,annot=True)
plt.show()


print(LWR)

#import pickle
#
#with open(dirPath + 'LWR.pkl', "wb") as f:
#    pickle.dump(LWR, f)
#with open(dirPath + 'dataStructure.pkl', "wb") as g:
#    pickle.dump(dataStructure, g)