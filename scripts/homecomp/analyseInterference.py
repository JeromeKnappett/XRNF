#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 15 12:57:29 2021

@author: -
"""
import tifffile
import numpy as np
import matplotlib.pyplot as plt
import jerome.dev.scripts.interferenceGratingModelsJK as interferenceGratingModelsJK
from math import log10, floor

colours = plt.rcParams["axes.prop_cycle"].by_key()["color"]

def round_sig(x, sig=2):
    if x != 0:
        return round(x, sig-int(floor(log10(abs(x))))-1)
    else:
        return x
    
Ipath = '/home/jerome/dev/data/aerialImages/'

ranV = ['ideal', 'test1', 'test2']

electrons = [100, 1000, 2000, 3000, 4000, 5000, 10000]

sepBy = 'RMS' # # 'RMS' #'cLength' #
addBlock = True

if sepBy == 'RMS': # constant C length
    order = [0, 1, 2, 3, 4,  # c = 1 nm
             5, 6, 7, 8, 9,   # c = 5 nm
             10,11,12,13,14,  # c = 10 nm 
             15,16,17,18,19,  # c = 15 nm
             20,21,22,23,24] # c = 25 nm
if sepBy == 'cLength': # constant RMS
    order = [0,5,10,15,20,   # r = 1 nm
             1,6,11,16,21,   # r = 2 nm
             2,7,12,17,22,   # r = 5 nm
             3,8,13,18,23,   # r = 10 nm
             4,9,14,19,24]   # r = 15 nm

filesH = [str(o) + 'intensity.tif' for o in order] #['fullRes_4000eintensity.tif'] #['TEintensity.tif', 'TMintensity.tif']  #['fullRes_' + str(n) + 'eintensity.tif' for n in electrons] #['fullRes_4000eintensity.tif']  # horizontally oriented
filesV = ['ideal_20nmintensity.tif','roughness1intensity.tif', 'roughness2intensity.tif', 'roughness3intensity.tif', 'roughness4intensity.tif']#['4000eintensity_vertical.tif'] #['ideal_20nmintensity.tif','roughness1intensity.tif', 'roughness2intensity.tif', 'roughness3intensity.tif', 'roughness4intensity.tif']#, '1stTestintensity.tif', '2ndTestintensity.tif'] # vertically oriented
# print(filesH[0:4])
# print(filesH[4:7])
justBlockFile = 'idealintensity.tif' #'10umBlockintensity.tif'

# filesH = filesH + justBlockFile
# filesV = filesV + justBlockFile

ver = False
hor = True

printContrast = False

save = False
savePath = '/home/jerome/Documents/MASTERS/Figures/plots/'

variable = 'block'  #'exitSlit'  # #'Polarisation' #'\u03C3 [nm]' # '$N_e$'

labelsH = ['hor'] #['TE-TE', 'TM-TM'] #[str(n) for i,n in enumerate(electrons)]# if i!=1]
labelsV =[0, 1, 2, 5, 10] # ['ver'] #[0, 1, 2, 5, 10] # '\u03C3 = 2 nm', '\u03C3 = 5 nm', '\u03C3 = 10 nm'] #['ver: ' + str(r) for r in ranV]

# sigma - \u03C3
pitch = 24

plotRange = 1000 # in nm

justBlockRes = 2.501122539655539e-09, 2.658184225986154e-07

resH, resV, resH1000 =  1.9651759267701173e-09, 1.8194278317912603e-9, 2.1488320941276643e-09 # resolution of each tif along axis perpendicular to fringes


lowresH, lowresV = 2.658184225988639e-07, 3.314297299424348e-07

#defining middle points of each array
midH = 64, 16377   
midV = 112, 13477
midH1000 = 144, 21159

midB = 64, (16377) # + int((6.9375e-6/justBlockRes[0])))

print(midB)


# number of pixels to sample along each direction
N_par, N_per = 1000, 1

if variable == 'exitSlit':
    resH = 2.4549295628988656e-09 #, 2.6639171024459003e-07
    # resH1000 = 1.9651759267701173e-09 #, 2.658184225988639e-07
    resH1000 = 2.501122539655539e-09
    res500 = 2.5431737001664825e-09 #2.6946186789244103e-09
    midH = 60, 12920
    midH1000 = 60, 12899
    midH500 = 60, 12881
    labelsH = ['100um Slit', '200um Slit', '300um Slit']
    filesH = ['100umSlitintensity.tif', '200umSlitintensity.tif', '300umSlitintensity.tif']

elif variable == 'Polarisation':
    if pitch == 24:
        resH,resH1000 = 4.77529829067939e-10, 6.46327159071368e-10
        resTM, resTE = resH, resH1000
        midH = 80, 67045
        midH1000 = 190, 70348
    if pitch == 14:
        resH,resH1000 = 3.231632826772039e-10, 2.387645475770844e-10
        resTE, resTM = resH, resH1000
        midH = 350, 140696
        midH1000 = 158, 134089
        labelsH = ['TE', 'TM']
        filesH = ['TEintensity_14p.tif', 'TMintensity_14p.tif']
elif variable == '\u03C3 [nm]':
    if hor:
        resH = 2.501122539655539e-09
        midH = 65, 12899
        midB = 65, (12899) #+ int((13.875e-6/justBlockRes[0])))
        # Input Values
        if sepBy == 'RMS':
            labelsH = [1, 2, 5, 10, 15,
                       1, 2, 5, 10, 15,
                       1, 2, 5, 10, 15,
                       1, 2, 5, 10, 15,
                       1, 2, 5, 10, 15] 
            secondLabels = [1,1,1,1,1,
                            5,5,5,5,5,
                            10,10,10,10,10,
                            15,15,15,15,15,
                            25,25,25,25,25]
            
            labelsRMS = labelsH
            labelsClength = secondLabels
            #['\u03C3:1nm,C:1nm','\u03C3:2nm,C:1nm','\u03C3:5nm,C:1nm', '\u03C3:15nm,C:1nm']#, 
                        # '\u03C3:1nm,C:15nm','\u03C3:15nm,C:5nm',
                        # '\u03C3:1nm,C:25nm','\u03C3:10nm,C:25nm', '\u03C3:15nm,C:25nm']
        elif sepBy == 'cLength':
            labelsH = [1,5,10,15,25,
                       1,5,10,15,25,
                       1,5,10,15,25,
                       1,5,10,15,25,
                       1,5,10,15,25]
            secondLabels = [1,1,1,1,1,
                            2,2,2,2,2,
                            5,5,5,5,5,
                            10,10,10,10,10,
                            15,15,15,15,15]
            labelsRMS = secondLabels
            labelsClength = labelsH
        # Output Values
        # labelsH = ['\u03C3:0.66nm,C:1nm','\u03C3:1.2nm,C:1nm','\u03C3:2.7nm,C:1nm', '\u03C3:7.6nm,C:1nm']#, 
                   # '\u03C3:1nm,C:15nm','\u03C3:15nm,C:5nm',
                   # '\u03C3:1nm,C:25nm','\u03C3:10nm,C:25nm', '\u03C3:15nm,C:25nm']
        
    
# redefining number of pixels for vertical array to match the range sampled in horizontal
nV = round((resH*N_par)/resV)
rangeV = resV*nV
rangeH = resH*N_par
rangeH1000 = resH1000*N_par
M = round((rangeH1000)/resH1000)
B = round((rangeH)/justBlockRes[0])
if variable == 'exitSlit':
    range500 = res500*N_par
    N500 = round((range500)/res500)
    print("Range500 :", range500)
    print("N500 :", N500)
else:
    pass
print("Range Hor: {} m".format(rangeH))
print("Range Hor - 2: {} m".format(rangeH1000))
print("Range Ver: {} m".format(rangeV))
print("nH, nV, M :", N_par, nV, M)

    
    
    
# read tiff files
if hor:
    tiffsH = [tifffile.imread(Ipath + f) for f in filesH]
    tiffBlock = tifffile.imread(Ipath + str(justBlockFile))
    # print(np.shape(tiffsH[1]))
    plt.imshow(tiffsH[1], aspect='auto')
    plt.title("intensity tif")
    plt.show()
    imageH = [t[midH[0]-N_per:midH[0]+N_per, midH[1]-N_par:midH[1]+N_par] for t in tiffsH]
    print("shape of tiffs: ", np.shape(tiffsH))
    print("shape of images: ", np.shape(imageH))
    print("shape of blockImage: ", np.shape(tiffBlock))
    if variable == 'block':
        try:
            fig, axs = plt.subplots(3,1)
            imageH100 = tiffsH[0][midH[0]-N_per:midH[0]+N_per, midH[1]-N_par:midH[1]+N_par]
            imageH1000 = tiffsH[1][midH1000[0]-N_per:midH1000[0]+N_per, midH1000[1]-M:midH1000[1]+M]
            iMin, iMax = np.min(imageH), np.max(imageH)
            axs[0].imshow(imageH100, aspect='auto', vmin=iMin,vmax=iMax)
            axs[0].set_title("aerial image # 100 um")
            axs[1].imshow(imageH1000, aspect='auto', vmin=iMin,vmax=iMax)
            axs[1].set_title("aerial image # 200 um")
            # plt.show()
            imageH500 = tiffsH[2][midH500[0]-N_per:midH500[0]+N_per, midH500[1]-N500:midH500[1]+N500]
            axs[2].imshow(imageH500, aspect='auto', vmin=iMin,vmax=iMax)
            axs[2].set_title("aerial image # 500 um")
            plt.show()
            ROI500 = [midH500[1]-N500, midH500[0]-N_per], [midH500[1]+N500,  midH500[0]+N_per]
            
        except IndexError:
            pass
    if variable == 'exitSlit':
        try:
            fig, axs = plt.subplots(3,1)
            imageH100 = tiffsH[0][midH[0]-N_per:midH[0]+N_per, midH[1]-N_par:midH[1]+N_par]
            imageH1000 = tiffsH[1][midH1000[0]-N_per:midH1000[0]+N_per, midH1000[1]-M:midH1000[1]+M]
            iMin, iMax = np.min(imageH), np.max(imageH)
            axs[0].imshow(imageH100, aspect='auto', vmin=iMin,vmax=iMax)
            axs[0].set_title("aerial image # 100 um")
            axs[1].imshow(imageH1000, aspect='auto', vmin=iMin,vmax=iMax)
            axs[1].set_title("aerial image # 200 um")
            # plt.show()
            imageH500 = tiffsH[2][midH500[0]-N_per:midH500[0]+N_per, midH500[1]-N500:midH500[1]+N500]
            axs[2].imshow(imageH500, aspect='auto', vmin=iMin,vmax=iMax)
            axs[2].set_title("aerial image # 500 um")
            plt.show()
            ROI500 = [midH500[1]-N500, midH500[0]-N_per], [midH500[1]+N500,  midH500[0]+N_per]
            
        except IndexError:
            pass
    if variable == 'Polarisation':
        try:
            imageH1000 = tiffsH[1][midH1000[0]-N_per:midH1000[0]+N_per, midH1000[1]-M:midH1000[1]+M]
            plt.imshow(imageH1000, aspect='auto')
            plt.title("aerial image")
            plt.show()
        except IndexError:
            pass
if ver:
    tiffsV = [tifffile.imread(Ipath + f) for f in filesV]
    imageV = tiffsV[0][midV[1]-nV:midV[1]+nV, midV[0]-N_per:midV[0]+N_per]



ROIH = [midH[1]-N_par, midH[0]-N_per], [midH[1]+N_par,  midH[0]+N_per]
ROIV = [midV[0]-N_per, midV[1]-nV], [midV[0]+N_per, midV[1]+nV]
ROIH1000 = [midH1000[1]-M, midH1000[0]-N_per], [midH1000[1]+M,  midH1000[0]+N_per]
ROIB = [midB[1]-B, midB[0]-N_per], [midB[1]+B,  midB[0]+N_per]


if hor and ver:
    fig, axs = plt.subplots(1,2)
    axs[0].imshow(imageH, aspect='auto')
    axs[0].set_title("Horizontal Orientation")
    axs[0].set_yticks([0, N_per, 2*N_per-1]) #int(len(imageH[0])/2), len(imageH[0])-1])
    axs[0].set_yticklabels([round_sig(-1e6*N_per*lowresH),0,round_sig(1e6*N_per*lowresH)])
    axs[0].set_xticks([0, N_par/2, N_par, int((3/2)*N_par), 2*N_par])
    axs[0].set_xticklabels([round_sig(-1e6*N_par*resH),round_sig(-1e6*(N_par/2)*resH),0,round_sig(1e6*(N_par/2)*resH),round_sig(1e6*N_par*resH)])
    axs[0].set_xlabel("x-position [\u03bcm]")
    axs[0].set_ylabel("y-position [\u03bcm]")
    axs[1].imshow(imageV, aspect='auto')
    axs[1].set_title("Vertical Orientation")
    axs[1].set_xticks([0, N_per, 2*N_per-1])  #int(len(imageV[1])/2), len(imageV[1])-1])
    axs[1].set_xticklabels([round_sig(-1e6*N_per*lowresV),0,round_sig(1e6*N_per*lowresV)])
    axs[1].set_yticks([0, nV/2, nV, int((3/2)*nV), 2*nV])
    axs[1].set_yticklabels([round_sig(-1e6*nV*resV),round_sig(-1e6*(nV/2)*resV),0,round_sig(1e6*(nV/2)*resV),round_sig(1e6*nV*resV)])
    axs[1].set_xlabel("x-position [\u03bcm]")
    if save:
        plt.savefig(savePath + 'horVver.pdf')
        plt.savefig(savePath + 'horVver.png', dpi=2000)
    plt.show()

if ver:
    image = tiffsV[0][midV[1]-nV:midV[1]+nV, midV[0]-N_per:midV[0]+N_per]
    plt.imshow(imageV, aspect=0.25)
    plt.xlabel("x-position [\u03bcm]")
    plt.ylabel("y-position [\u03bcm]")
    plt.xticks([0,int(len(imageV[1])/2), len(imageV[1])-1], [round_sig(-1e6*N_per*lowresV),0,round_sig(1e6*N_per*lowresV)])
    plt.yticks([0, nV/2, nV, int((3/2)*nV), 2*nV], [round_sig(-1e6*nV*resV),round_sig(-1e6*(nV/2)*resV),0,round_sig(1e6*(nV/2)*resV),round_sig(1e6*nV*resV)])
    plt.colorbar(label="Intensity [ph/s/.1%bw/mm$^2$]")#[a.u]")
    if save:
        plt.savefig(savePath + 'aerialImage.pdf')
        plt.savefig(savePath + 'aerialImage.png', dpi=2000)
    plt.show()

if hor:
    aerialImagesH = [interferenceGratingModelsJK.lineProfile(t, ROI=ROIH, AXIS=0) for i,t in enumerate(tiffsH)]# if i!=1]
    aerialImageBlock = tiffBlock[midB[0],midB[1]-B:midB[1]+B]
    # aerialImagesH = [a-aerialImageBlock for a in aerialImagesH]
    # aerialImagesH = aerialImagesH + aerialImageBlock
    if variable == 'exitSlit':
        aerialImageH100 = interferenceGratingModelsJK.lineProfile(tiffsH[0], ROI=ROIH, AXIS=0)
        aerialImageH200 = interferenceGratingModelsJK.lineProfile(tiffsH[1], ROI=ROIH1000, AXIS=0)
        aerialImageH500 = interferenceGratingModelsJK.lineProfile(tiffsH[2], ROI=ROI500, AXIS=0)
        xH500 = np.linspace(-N500*res500, N500*res500,2*N500)
        # try:
        #     aerialImagesH.insert(1,aerialImagesH1000[0])
        #     aerialImagesH.insert(2,aerialImagesH500[0])
        # except IndexError:
        #     pass
    if variable == 'Polarisation':
        aerialImagesH1000 = [interferenceGratingModelsJK.lineProfile(t, ROI=ROIH1000, AXIS=0) for i,t in enumerate(tiffsH) if i==1]
        try:
            aerialImagesH.insert(1,aerialImagesH1000[0])
        except IndexError:
            pass
        
    print(np.shape(aerialImagesH))    
    print(np.shape(aerialImageBlock))
    fig, axs = plt.subplots(2,1)
    axs[0].imshow(imageH[0], aspect='auto')
    axs[0].set_title("Sampled Aerial Image")    
    axs[0].set_yticks([0, N_per, 2*N_per-1]) #int(len(imageH[0])/2), len(imageH[0])-1])
    axs[0].set_yticklabels([round_sig(-1e6*N_per*lowresH),0,round_sig(1e6*N_per*lowresH)])
    axs[0].set_xticks([0, N_par/2, N_par, int((3/2)*N_par), 2*N_par])
    axs[0].set_xticklabels([round_sig(-1e6*N_par*resH),round_sig(-1e6*(N_par/2)*resH),0,round_sig(1e6*(N_par/2)*resH),round_sig(1e6*N_par*resH)])
    axs[0].set_ylabel("y-position [\u03bcm]")
    axs[1].plot(aerialImagesH[0])
    axs[1].set_title("Averaged Intensity Profile")    
    axs[1].set_xticks([0, N_par/2, N_par, int((3/2)*N_par), 2*N_par])
    axs[1].set_xticklabels([round_sig(-1e6*N_par*resH),round_sig(-1e6*(N_par/2)*resH),0,round_sig(1e6*(N_par/2)*resH),round_sig(1e6*N_par*resH)])
    axs[1].set_xlabel("x-position [\u03bcm]")
    axs[1].set_ylabel("Intensity [ph/s/.1%bw/mm$^2$]")
    fig.tight_layout()
    plt.show()
    # aerialImagesH = aerialImagesH[0] + aerialImagesH1000 + aerialImagesH[1::]
if ver:
    aerialImagesV = [interferenceGratingModelsJK.lineProfile(t, ROI=ROIV, AXIS=1) for t in tiffsV]
    print(np.shape(aerialImagesV))
#
#fig, axs = plt.subplots(1,2)
#axs[0].imshow(aerialImagesH, aspect='auto')
#axs[0].set_title("Horizontal")
#axs[1].imshow(aerialImagesV, aspect='auto')
#axs[1].set_title("Vertical")
#plt.show()

avIN = [np.mean(np.mean(a)) for a in aerialImagesH]
totIN = [np.sum(a) for a in aerialImagesH]

xH = np.linspace(-N_par*resH, N_par*resH,2*N_par)
xH1000 = np.linspace(-M*resH1000, M*resH1000,2*M)
xV = np.linspace(-nV*resV, nV*resV,2*nV)
xB = np.linspace(-B*justBlockRes[0], B*justBlockRes[0],2*B)

''' define interference grating parameters'''
wl = 6.710553853647976e-9 # wavelength in m

# Amplitude of both beams (assumed equal)
A = 0.07e5 # 0.37e5 #0.3e5  # this may be scaled to  match simulated intensity
k = 2*np.pi/wl
m = 1 # order of diffracted beams from each grating
d = 100e-9 #24e-9 #100e-9 # grating spacing
# angle between the beams from each grating
theta = np.arcsin( m *wl/d)

''' generate interference intensity'''
IH = interferenceGratingModelsJK.interferenceIntensity(xH,k,theta,A=A)
IV = interferenceGratingModelsJK.interferenceIntensity(xV,k,theta,A=A)
IH1000 = interferenceGratingModelsJK.interferenceIntensity(xH1000,k,theta,A=A)

    
''' convolve intensity with gaussian '''
sigma = [1, 1.5, 2, 5] #2.7
if hor:
    I = [interferenceGratingModelsJK.gaussian_filter(IH, sigma=s) for s in sigma]

''' plot intensity with and without noise, together with saved profile'''
# plt.figure(figsize=(10,6))
# colours = colours[0:5] + colours[8::]
if hor:
    # for i, a in enumerate(I):
    #     plt.plot(xH*1e9, a, linewidth=1, color=colours[i], label=str(round_sig(1/sigma[i])))
    if variable == 'exitSlit':
        # for i,a in enumerate(aerialImagesH[0:1]):
        plt.plot(xH*1e9, aerialImageH100, linewidth=1, color=colours[0], label=str(labelsH[0])) #'\u03C3 [nm]: ' + str(labelsH[i]) + ',C [nm]: 1')
        plt.plot(xH1000*1e9, aerialImageH200, linewidth=1, color=colours[1], label=str(labelsH[1])) 
        plt.plot(xH500*1e9, aerialImageH500, linewidth=1, color=colours[2], label=str(labelsH[2])) 
        plt.xlim(-plotRange/2,plotRange/2)
        # if addBlock:
        #     plt.plot(xB*1e9, (aerialImageBlock), linewidth=1, color='red', label='Block')
        # plt.plot(xH*1e9,IH, ':', label='Model amplitude')
        plt.legend()
        # for i, a in enumerate(aerialImagesH[4::]):
        #     plt.plot(xH*1e9, a, linewidth=1, color=colours[i+4], label='\u03C3 [nm]: ' + str(labelsH[i]) + ',C [nm]: 25')
    elif variable == 'Polarisation':
        for i, a in enumerate(aerialImagesH[0:2]): #[0:4]
            print("# ", i)
        #     plt.plot(xH*1e9, a, linewidth=1, color=colours[i], label=str(labelsH[i])) #'\u03C3 [nm]: ' + str(labelsH[i]) + ',C [nm]: 1')
        # for i, a in enumerate(aerialImagesH[4::]):
        #     plt.plot(xH*1e9, a, linewidth=1, color=colours[i+4], label='\u03C3 [nm]: ' + str(labelsH[i]) + ',C [nm]: 25')
            if i==0:
                plt.plot(xH*1e9, a, linewidth=1, color=colours[i], label=str(labelsH[i])) #'$N_e$ = '
            if i==1:
                plt.plot(xH1000*1e9, a, label=str(labelsH[i]), linewidth=1, color=colours[i])
    else:
        fig,axs = plt.subplots(5,1)
        fig.set_size_inches(6.0, 12.0)
        for i, a in enumerate(aerialImagesH[0:5]): #[0:4]
            if sepBy == 'RMS':
                axs[0].plot(xH*1e9, a, linewidth=1, color=colours[i])#, label='\u03C3 [nm]: ' + str(labelsH[i]))# + ',C [nm]: 1')
            else:
                axs[0].plot(xH*1e9, a, linewidth=1, color=colours[i])#, label='$C_y$ [nm]: ' + str(labelsH[i]))# + ',\u03C3 [nm]: 1')
        for i, a in enumerate(aerialImagesH[5:10]):
            if sepBy == 'RMS':
                axs[1].plot(xH*1e9, a, linewidth=1, color=colours[i])#, label='\u03C3 [nm]: ' + str(labelsH[i]) + ',C [nm]: 5')
            else:
                axs[1].plot(xH*1e9, a, linewidth=1, color=colours[i])#, label='$C_y$ [nm]: ' + str(labelsH[i]) + ',\u03C3 [nm]: 2')
        for i, a in enumerate(aerialImagesH[10:15]):
            if sepBy == 'RMS':
                axs[2].plot(xH*1e9, a, linewidth=1, color=colours[i])#, label='\u03C3 [nm]: ' + str(labelsH[i]) + ',C [nm]: 10')
            else:
                axs[2].plot(xH*1e9, a, linewidth=1, color=colours[i])#, label='$C_y$ [nm]: ' + str(labelsH[i]) + ',\u03C3 [nm]: 5')
        for i, a in enumerate(aerialImagesH[15:20]):
            if sepBy == 'RMS':
                axs[3].plot(xH*1e9, a, linewidth=1, color=colours[i])#, label='\u03C3 [nm]: ' + str(labelsH[i]) + ',C [nm]: 15')
            else:
                axs[3].plot(xH*1e9, a, linewidth=1, color=colours[i])#, label='$C_y$ [nm]: ' + str(labelsH[i]) + ',\u03C3 [nm]: 10')
        for i, a in enumerate(aerialImagesH[20::]):
            if sepBy == 'RMS':
                axs[4].plot(xH*1e9, a, linewidth=1, color=colours[i])#, label='\u03C3 [nm]: ' + str(labelsH[i]))# + ',C [nm]: 25')
            else:
                axs[4].plot(xH*1e9, a, linewidth=1, color=colours[i])#, label='$C_y$ [nm]: ' + str(labelsH[i]))# + ',\u03C3 [nm]: 15')
        for ax in fig.axes:
            if addBlock:
                ax.plot(xH*1e9, (aerialImageBlock), linewidth=1, linestyle=':', color='red', label='Non-Rough Mask')
                ax.legend()
            ax.set_xlim(-plotRange/2,plotRange/2)
            ax.set_ylabel('Intensity [ph/s/.1%bw/mm$^2$]')
        # axs[4].legend(loc='lower center', fontsize='small', #title='Simulated Electrons ($N_e$)', 
        #     bbox_to_anchor=(0.5, -3.3),fancybox=True, shadow=True,ncol=5)
        # axs[2].set_ylabel('Intensity [ph/s/.1%bw/mm$^2$]')
        axs[4].set_xlabel('Position [nm]')
        if sepBy == 'RMS':
            axs[0].text(plotRange*(-1/2 - 1/10), -60000000, '$C_y = 1 nm$', {'color': 'red', 'fontsize': 6})
            axs[1].text(plotRange*(-1/2 - 1/10), -60000000, '$C_y = 5 nm$', {'color': 'red', 'fontsize': 6})
            axs[2].text(plotRange*(-1/2 - 1/10), -60000000, '$C_y = 10 nm$', {'color': 'red', 'fontsize': 6})
            axs[3].text(plotRange*(-1/2 - 1/10), -60000000, '$C_y = 15 nm$', {'color': 'red', 'fontsize': 6})
            axs[4].text(plotRange*(-1/2 - 1/10), -60000000, '$C_y = 25 nm$', {'color': 'red', 'fontsize': 6})
        else:
            axs[0].text(plotRange*(-1/2 - 1/10), -60000000, '\u03C3 = 1 nm', {'color': 'red', 'fontsize': 9})
            axs[1].text(plotRange*(-1/2 - 1/10), -60000000, '\u03C3 = 2 nm', {'color': 'red', 'fontsize': 9})
            axs[2].text(plotRange*(-1/2 - 1/10), -60000000, '\u03C3 = 5 nm', {'color': 'red', 'fontsize': 9})
            axs[3].text(plotRange*(-1/2 - 1/10), -60000000, '\u03C3 = 10 nm', {'color': 'red', 'fontsize': 9})
            axs[4].text(plotRange*(-1/2 - 1/10), -60000000, '\u03C3 = 15 nm', {'color': 'red', 'fontsize': 9})
            
            
        fig.tight_layout()
        
        fig.subplots_adjust(bottom=0.06)   ##  Need to play with this number.
        if sepBy == 'RMS':
            fig.legend(labels=['\u03C3 [nm]: ' + str(l) for l in np.array(labelsH).T[0:5]], loc="lower center", ncol=5)
        elif sepBy == 'cLength':
            fig.legend(labels=['$C_y$ [nm]: ' + str(l) for l in np.array(labelsH).T[0:5]], loc="lower center", ncol=5)
if ver:
    # if hor != True:
    #     plt.plot(xV*1e9,IV, ':', label='Model amplitude')
    for i, b in enumerate(aerialImagesV):
        plt.plot(xV*1e9, b, label=variable + ' = ' + str(labelsV[i]), color=colours[i])
    plt.xlabel('Position [nm]')
    plt.ylabel('Intensity [ph/s/.1%bw/mm$^2$]') #[ph/s/.1 $\%% bw/mm^2]')
    plt.ylim(bottom=0)#, top=0.5e9)
    plt.xlim(-500,500)
        # plt.legend()
    plt.legend(loc='lower center', fontsize='medium', #title='Simulated Electrons ($N_e$)', 
            bbox_to_anchor=(0.5, -0.23),fancybox=True, shadow=True,ncol=5)
# fig.tight_layout()
if save:
    plt.savefig(savePath + 'aerialImage_horOrientation_electrons.pdf')
    plt.savefig(savePath + 'aerialImage_horOrientation_electrons.png', dpi=2000)
plt.show()


# Working contrast metrics
if hor:
    # aerialImagesH = I
    # labels = sigma
    if variable == 'Polarisation':
        michelsonH = [interferenceGratingModelsJK.gratingContrastMichelson(a) for a in aerialImagesH[0:2]]
        rmsH = [interferenceGratingModelsJK.gratingContrastRMS(a) for a in aerialImagesH[0:2]]
        compositeH = [interferenceGratingModelsJK.meanDynamicRange(a) for a in aerialImagesH[0:2]] #, mdrC, imbalanceC 
        nilsH = [interferenceGratingModelsJK.NILS(aerialImagesH[0],xH, d/4, show=False)]
        fourierH = [interferenceGratingModelsJK.gratingContrastFourier(aerialImagesH[0],xH*1e6, show=False)] #Cf,  Am, Fr, peakFr - Still unsure but seems good
        fidelH = [interferenceGratingModelsJK.fidelity(aerialImagesH[0],IH)]   # fidelity based on comparison to model
        try:
            nilsH1000 = interferenceGratingModelsJK.NILS(aerialImagesH1000[0], xH1000, d/4, show=False)
            nilsH.insert(1,nilsH1000)
            fourierH1000 = interferenceGratingModelsJK.gratingContrastFourier(aerialImagesH1000[0],xH1000*1e6, show=False)
            fourierH.insert(1,fourierH1000)
            fidelH1000 = interferenceGratingModelsJK.fidelity(aerialImagesH1000[0],IH1000)
            fidelH.insert(1,fidelH1000)
        except IndexError:
            pass
    elif variable =='exitSlit':
        michelsonH = [interferenceGratingModelsJK.gratingContrastMichelson(a) for a in [aerialImageH100,aerialImageH200,aerialImageH500]]
        rmsH = [interferenceGratingModelsJK.gratingContrastRMS(a) for a in [aerialImageH100,aerialImageH200,aerialImageH500]]
        compositeH = [interferenceGratingModelsJK.meanDynamicRange(a) for a in [aerialImageH100,aerialImageH200,aerialImageH500]]
        nilsH = [interferenceGratingModelsJK.NILS(aerialImageH100,xH, d/4, show=True), interferenceGratingModelsJK.NILS(aerialImageH200,xH1000, d/4, show=True),interferenceGratingModelsJK.NILS(aerialImageH500,xH500, d/4, show=True)]
        fourierH = [interferenceGratingModelsJK.gratingContrastFourier(aerialImageH100,xH*1e6, show=False), interferenceGratingModelsJK.gratingContrastFourier(aerialImageH200,xH1000*1e6, show=False), interferenceGratingModelsJK.gratingContrastFourier(aerialImageH500,xH500*1e6, show=False)]
        fidelH = [interferenceGratingModelsJK.fidelity(a,IH) for i,a in enumerate(aerialImagesH)]# if i!=1]   # fidelity based on comparison to model
        
    else:
        michelsonH = [interferenceGratingModelsJK.gratingContrastMichelson(a) for a in aerialImagesH]
        rmsH = [interferenceGratingModelsJK.gratingContrastRMS(a) for a in aerialImagesH]
        compositeH = [interferenceGratingModelsJK.meanDynamicRange(a) for a in aerialImagesH]
        nilsH = [interferenceGratingModelsJK.NILS(a,xH, d/4, show=False) for i,a in enumerate(aerialImagesH)]# if i!=1]
        fourierH = [interferenceGratingModelsJK.gratingContrastFourier(a,xH*1e6, show=False) for i,a in enumerate(aerialImagesH)]# if i!=1] #Cf,  Am, Fr, peakFr - Still unsure but seems good
        fidelH = [interferenceGratingModelsJK.fidelity(a,IH) for i,a in enumerate(aerialImagesH)]# if i!=1]   # fidelity based on comparison to model
 
    if ver != True:
        michelsonC = michelsonH
        rmsC = rmsH
        compositeC = compositeH
        nilsC = nilsH
        fourierC = fourierH
        fidel = fidelH  
        labels = labelsH
if ver:
    michelsonV = [interferenceGratingModelsJK.gratingContrastMichelson(a) for a in aerialImagesV]
    rmsV = [interferenceGratingModelsJK.gratingContrastRMS(a) for a in aerialImagesV]
    compositeV = [interferenceGratingModelsJK.meanDynamicRange(a) for a in aerialImagesV] #, mdrC, imbalanceC 
    nilsV = [interferenceGratingModelsJK.NILS(a,xV, d/4, show=False) for a in aerialImagesV] 
    fourierV = [interferenceGratingModelsJK.gratingContrastFourier(a,xV*1e6, show=False) for a in aerialImagesV] #Cf,  Am, Fr, peakFr - Still unsure but seems good
    fidelV = [interferenceGratingModelsJK.fidelity(a,IV) for a in aerialImagesV]   # fidelity based on comparison to model
    if hor != True:
        michelsonC = michelsonV
        rmsC = rmsV
        compositeC = compositeV
        nilsC = nilsV
        fourierC = fourierV
        fidel = fidelV    
        labels = labelsV
        
if hor and ver:
    michelsonC = michelsonH + michelsonV
    rmsC = rmsH + rmsV
    compositeC = compositeH + compositeV
    nilsC = nilsH + nilsV
    fourierC = fourierH + fourierV
    fidel = fidelH + fidelV
    labels = labelsH + labelsV

# print(michelsonC)
# print(np.shape(michelsonC))
# print(nilsC[0][6])
# print(nilsC[0][7])
# print(np.shape(nilsC[0]))


# plt.plot(xH*1e9,aerialImagesH[0])
# plt.plot(xH[nilsC[0][7]]*1e9,aerialImagesH[0][nilsC[0][7]], 'x')
# plt.xlim(-100,100)
# plt.show()

sumPeaks = []
avPeaks = []
rmsPeaks = []

for a in aerialImagesH:
    try:
        peaks = [a[n[7]] for n in nilsC]
        sumPeak = np.sum(peaks)
        avPeak = np.mean(peaks)
        rmsPeak = np.sqrt(np.mean([p**2 for p in peaks]))
        
        sumPeaks.append(sumPeak)
        avPeaks.append(avPeak)
        rmsPeaks.append(rmsPeak)
    except ValueError:
        pass
    
if variable == 'exitSlit':
    for a in [aerialImageH100,aerialImageH200,aerialImageH500]:
        peaks = np.array([a[n[7]] for n in nilsC])
        print(np.shape(peaks[0]))
        print(np.shape(np.squeeze(peaks).flatten()))
        sumPeak = np.sum(peaks[0])
        avPeak = np.mean(peaks[0])
        rmsPeak = np.sqrt(np.mean([p**2 for p in peaks[0]]))
        
        sumPeaks.append(sumPeak)
        avPeaks.append(avPeak)
        rmsPeaks.append(rmsPeak)
else:
    pass
    
# fig, axs = plt.subplots(1,4)
# axs[0].plot(sumPeaks, 'x:')
# # axs[0].plot(sumPeaks[5:10], 'x:')
# # axs[0].plot(sumPeaks[10:15], 'x:')
# # axs[0].plot(sumPeaks[15:20], 'x:')
# # axs[0].plot(sumPeaks[20::], 'x:')
# axs[1].plot(avPeaks, 'x:')
# # axs[1].plot(avPeaks[5:10], 'x:')
# # axs[1].plot(avPeaks[10:15], 'x:')
# # axs[1].plot(avPeaks[15:20], 'x:')
# # axs[1].plot(avPeaks[20::], 'x:')
# axs[2].plot(rmsPeaks, 'x:')
# # axs[2].plot(rmsPeaks[5:10], 'x:')
# # axs[2].plot(rmsPeaks[10:15], 'x:')
# # axs[2].plot(rmsPeaks[15:20], 'x:')
# # axs[2].plot(rmsPeaks[20::], 'x:')
# axs[3].plot([c[0] for c in compositeC], 'x:')
# # axs[3].plot([c[0] for c in compositeC[5:10]], 'x:')
# # axs[3].plot([c[0] for c in compositeC[10:15]], 'x:')
# # axs[3].plot([c[0] for c in compositeC[15:20]], 'x:')
# # axs[3].plot([c[0] for c in compositeC[20::]], 'x:')
# axs[0].set_ylabel('Sum of peak heights')
# axs[1].set_ylabel('Average peak height')
# axs[2].set_ylabel('RMS peak height')
# axs[3].set_ylabel('Composite Contrast')
# fig.tight_layout()
# # fig.subplots_adjust(bottom=0.2)   ##  Need to play with this number.
# # if sepBy == 'RMS':
# #     fig.legend(labels=['\u03C3 [nm]: ' + str(l) for l in labelsH[0:5]], loc="lower center", ncol=5)
# # else:
# #     fig.legend(labels=['$C_y$ [nm]: ' + str(l) for l in labelsH[0:5]], loc="lower center", ncol=5)
# # plt.show()

# # Plotting all contrast metrics together
# # labels = sigma
# fig, ax1 = plt.subplots()
# ax2 = ax1.twinx()
    
# ax1.plot(labels, michelsonC, 'x:', label='Michelson')
# ax1.plot(labels, rmsC, 'x:', label='RMS')
# ax1.plot(labels, [c[0] for c in compositeC], 'x:', label='Composite')
# ax1.plot(labels, [c[1] for c in compositeC], 'x:', label='MDR')
# ax1.plot(labels, [c[2] for c in compositeC], 'x:', label='Imbalance')
# ax1.plot(labels, [f[0] for f in fourierC], 'x:', label='Fourier')
# ax2.plot(labels, [n[0] for n in nilsC], 'o:', label='NILS - mean')
# ax2.plot(labels, [n[4] for n in nilsC], 'o:', label='NILS - rms')
# ax1.plot(labels, fidel, ':', label='Fidelity')
# ax1.legend(fontsize='x-small')
# ax2.legend(loc='center right', fontsize='x-small')
#     # ax2.set_ylabel("Fidelity")
# ax2.set_ylabel("NILS")
# ax1.set_ylabel("Aerial Image Contrast")
# ax1.set_xlabel(variable)
# if save:
#     plt.savefig(savePath + 'contrastAll_horOrientation_electrons.pdf')
#     plt.savefig(savePath + 'contrastAll_horOrientation_electrons.png', dpi=2000)
# plt.show()
# plt.show()
    
# Plotting contrast metrics seperately
fig, axs = plt.subplots(2,3)

if variable == '\u03C3 [nm]':
    # if sepBy == 'RMS':
    axs[0,0].plot(labels[0:5], michelsonC[0:5], 'x:')#, label='C=1nm')
    axs[0,0].plot(labels[5:10], michelsonC[5:10], 'x:')#, label='C=5nm')
    axs[0,0].plot(labels[10:15], michelsonC[10:15], 'x:')#, label='C=10nm')
    axs[0,0].plot(labels[15:20], michelsonC[15:20], 'x:')#, label='C=15nm')
    axs[0,0].plot(labels[20::], michelsonC[20::], 'x:')#, label='C=25nm')
    axs[0,0].set_title("Michelson")
    axs[0,0].set_ylabel("Contrast")
    axs[0,1].plot(labels[0:5], rmsC[0:5], 'x:')#, label='C=1nm')
    axs[0,1].plot(labels[5:10], rmsC[5:10], 'x:')#, label='C=25nm')
    axs[0,1].plot(labels[10:15], rmsC[10:15], 'x:')#, label='C=1nm')
    axs[0,1].plot(labels[15:20], rmsC[15:20], 'x:')#, label='C=1nm')
    axs[0,1].plot(labels[20::], rmsC[20::], 'x:')#, label='C=1nm')
    axs[0,1].set_title("RMS")
    axs[0,2].plot(labels[0:5], [c[0] for c in compositeC[0:5]], 'x:')#, label='C=1nm')
    axs[0,2].plot(labels[5:10], [c[0] for c in compositeC[5:10]], 'x:')#, label='C=1nm')
    axs[0,2].plot(labels[10:15], [c[0] for c in compositeC[10:15]], 'x:')#, label='C=1nm')
    axs[0,2].plot(labels[15:20], [c[0] for c in compositeC[15:20]], 'x:')#, label='C=1nm')
    axs[0,2].plot(labels[20::], [c[0] for c in compositeC[20::]], 'x:')#, label='C=1nm')
    axs[0,2].set_title("Composite")
    axs[1,0].plot(labels[0:5], [f[0] for f in  fourierC[0:5]], 'x:')#, label='C=1nm')
    axs[1,0].plot(labels[5:10], [f[0] for f in  fourierC[5:10]], 'x:')#, label='C=1nm')
    axs[1,0].plot(labels[10:15], [f[0] for f in  fourierC[10:15]], 'x:')#, label='C=1nm')
    axs[1,0].plot(labels[15:20], [f[0] for f in  fourierC[15:20]], 'x:')#, label='C=1nm')
    axs[1,0].plot(labels[20::], [f[0] for f in  fourierC[20::]], 'x:')#, label='C=1nm')
    axs[1,0].set_title("Fourier")
    axs[1,0].set_ylabel("Contrast")
    axs[1,1].set_title("NILS")
    axs[1,1].plot(labels[0:5], fidel[0:5], 'x:')#, label='C=1nm')
    axs[1,1].plot(labels[5:10], fidel[5:10], 'x:')#, label='C=1nm')
    axs[1,1].plot(labels[10:15], fidel[10:15], 'x:')#, label='C=1nm')
    axs[1,1].plot(labels[15:20], fidel[15:20], 'x:')#, label='C=1nm')
    axs[1,1].plot(labels[20::], fidel[20::], 'x:')#, label='C=1nm')
    axs[1,1].set_title("Fidelity")
    # axs[1,1].set_ylim(0.9997,0.99975)
    axs[1,2].plot(labels[0:5], [n[0] for n in nilsC[0:5]], 'x:')#, label='C=1nm')
    # if variable == '\u03C3 [nm]':
    axs[1,2].plot(labels[5:10], [n[0] for n in nilsC[5:10]], 'x:')#, label='C=1nm')
    axs[1,2].plot(labels[10:15], [n[0] for n in nilsC[10:15]], 'x:')#, label='C=1nm')
    axs[1,2].plot(labels[15:20], [n[0] for n in nilsC[15:20]], 'x:')#, label='C=1nm')
    axs[1,2].plot(labels[20::], [n[0] for n in nilsC[20::]], 'x:')#, label='C=1nm')
    axs[1,2].set_title("NILS - mean")
    axs[1,2].set_ylabel("NILS")
    if sepBy == 'cLength':
        axs[1,0].set_xlabel('$C_y [nm]$')
        axs[1,1].set_xlabel('$C_y [nm]$')
        axs[1,2].set_xlabel('$C_y [nm]$')
    elif sepBy == 'RMS':
        axs[1,0].set_xlabel('\u03C3 [nm]')
        axs[1,1].set_xlabel('\u03C3 [nm]')
        axs[1,2].set_xlabel('\u03C3 [nm]')
    fig.tight_layout()
    # fig.subplots_adjust(bottom=0.2)   ##  Need to play with this number.
    # if sepBy == 'RMS':
    #     plt.legend(labels=['$C_y$ [nm]: ' + str(l) for l in [1,5,10,15,25]], loc="lower center", ncol=5)
    # elif sepBy == 'cLength':
    #     plt.legend(labels=['\u03C3 [nm]: ' + str(l) for l in [1,2,5,10,15]], loc="lower center", ncol=5)
    if save:
        plt.savefig(savePath + 'contrastAllSep_horOrientation_electrons.pdf')
        plt.savefig(savePath + 'contrastAllSep_horOrientation_electrons.png', dpi=2000)
    else:
        pass
    plt.show()
    
    for ax in fig.axes:
        ax.legend()
        if variable == '\u03C3 [nm]':
                ax.set_xticklabels(labels, rotation=45, ha='right')
    fig.tight_layout()
    if save:
        plt.savefig(savePath + 'contrastAllSep_horOrientation_electrons.pdf')
        plt.savefig(savePath + 'contrastAllSep_horOrientation_electrons.png', dpi=2000)
    plt.show()
elif variable == 'exitSlit':
    # if sepBy == 'RMS':
    axs[0,0].plot(labels, michelsonC, 'x:')
    axs[0,0].set_title("Michelson")
    axs[0,0].set_ylabel("Contrast")
    axs[0,1].plot(labels, rmsC, 'x:')
    axs[0,1].set_title("RMS")
    axs[0,2].plot(labels, [c[0] for c in compositeC], 'x:')
    axs[0,2].set_title("Composite")
    axs[1,0].plot(labels, [f[0] for f in  fourierC], 'x:')
    axs[1,0].set_title("Fourier")
    axs[1,0].set_ylabel("Contrast")
    axs[1,1].set_title("NILS")
    axs[1,1].plot(labels, fidel, 'x:')
    axs[1,1].set_title("Fidelity")
    axs[1,2].plot(labels, [n[0] for n in nilsC], 'x:')
    axs[1,2].set_title("NILS - mean")
    axs[1,2].set_ylabel("NILS")
    axs[1,0].set_xlabel('Slit Width')
    axs[1,1].set_xlabel('Slit Width')
    axs[1,2].set_xlabel('Slit Width')
    fig.tight_layout()
    plt.show()
print(np.shape(fidel))
print(michelsonC[4::])


# Testing out combinations of metrics
fig, axs = plt.subplots(2,3)

if variable == '\u03C3 [nm]':
    # if sepBy == 'RMS':
    axs[0,0].plot(labels[0:5], [n[0]*aI*tI for n, aI, tI in zip(nilsC[0:5],avPeaks[0:5],sumPeaks[0:5])], 'x:')#, label='C=1nm')
    axs[0,0].plot(labels[5:10], [n[0]*aI*tI for n, aI, tI in zip(nilsC[5:10],avPeaks[5:10],sumPeaks[5:10])], 'x:')#, label='C=5nm')
    axs[0,0].plot(labels[10:15], [n[0]*aI*tI for n, aI, tI in zip(nilsC[10:15],avPeaks[10:15],sumPeaks[10:15])], 'x:')#, label='C=10nm')
    axs[0,0].plot(labels[15:20], [n[0]*aI*tI for n, aI, tI in zip(nilsC[15:20],avPeaks[15:20],sumPeaks[15:20])], 'x:')#, label='C=15nm')
    axs[0,0].plot(labels[20::], [n[0]*aI*tI for n, aI, tI in zip(nilsC[20::],avPeaks[20::],sumPeaks[20::])], 'x:')#, label='C=25nm')
    axs[0,0].set_title("NILS x Average I x Total I")
    axs[0,0].set_ylabel("Contrast")
    axs[0,1].plot(labels[0:5], [r*aI*tI for r, aI, tI in zip(rmsC[0:5],avPeaks[0:5],sumPeaks[0:5])], 'x:')#, label='C=1nm')
    axs[0,1].plot(labels[5:10], [r*aI*tI for r, aI, tI in zip(rmsC[5:10],avPeaks[5:10],sumPeaks[5:10])], 'x:')#, label='C=25nm')
    axs[0,1].plot(labels[10:15], [r*aI*tI for r, aI, tI in zip(rmsC[10:15],avPeaks[10:15],sumPeaks[10:15])], 'x:')#, label='C=1nm')
    axs[0,1].plot(labels[15:20], [r*aI*tI for r, aI, tI in zip(rmsC[15:20],avPeaks[15:20],sumPeaks[15:20])], 'x:')#, label='C=1nm')
    axs[0,1].plot(labels[20::], [r*aI*tI for r, aI, tI in zip(rmsC[20::],avPeaks[20::],sumPeaks[20::])], 'x:')#, label='C=1nm')
    axs[0,1].set_title("RMS x Average I x Total I")
    axs[0,2].plot(labels[0:5], [c[0]*n[0]*aI for c, n, aI in zip(compositeC[0:5],nilsC[0:5],avPeaks[0:5])], 'x:')#, label='C=1nm')
    axs[0,2].plot(labels[5:10], [c[0]*n[0]*aI for c, n, aI in zip(compositeC[5:10],nilsC[5:10],avPeaks[5:10])], 'x:')#, label='C=1nm')
    axs[0,2].plot(labels[10:15], [c[0]*n[0]*aI for c, n, aI in zip(compositeC[10:15],nilsC[10:15],avPeaks[10:15])], 'x:')#, label='C=1nm')
    axs[0,2].plot(labels[15:20], [c[0]*n[0]*aI for c, n, aI in zip(compositeC[15:20],nilsC[15:20],avPeaks[15:20])], 'x:')#, label='C=1nm')
    axs[0,2].plot(labels[20::], [c[0]*n[0]*aI for c, n, aI in zip(compositeC[20::],nilsC[20::],avPeaks[20::])], 'x:')#, label='C=1nm')
    axs[0,2].set_title("Composite x NILS x Average I")
    axs[1,0].plot(labels[0:5], [c[0]*n[0]*r for c, n, r in zip(compositeC[0:5],nilsC[0:5],rmsC[0:5])], 'x:')#, label='C=1nm')
    axs[1,0].plot(labels[5:10], [c[0]*n[0]*r for c, n, r in zip(compositeC[5:10],nilsC[5:10],rmsC[5:10])], 'x:')#, label='C=1nm')
    axs[1,0].plot(labels[10:15], [c[0]*n[0]*r for c, n, r in zip(compositeC[10:15],nilsC[10:15],rmsC[10:15])], 'x:')#, label='C=1nm')
    axs[1,0].plot(labels[15:20], [c[0]*n[0]*r for c, n, r in zip(compositeC[15:20],nilsC[15:20],rmsC[15:20])], 'x:')#, label='C=1nm')
    axs[1,0].plot(labels[20::], [c[0]*n[0]*r for c, n, r in zip(compositeC[20::],nilsC[20::],rmsC[20::])], 'x:')#, label='C=1nm')
    axs[1,0].set_title("Composite x NILS x RMS")
    axs[1,0].set_ylabel("Contrast")
    axs[1,1].plot(labels[0:5], [rI*n[0]*aI for rI, n, aI in zip(rmsPeaks[0:5],nilsC[0:5],avPeaks[0:5])], 'x:')#, label='C=1nm')
    axs[1,1].plot(labels[5:10], [rI*n[0]*aI for rI, n, aI in zip(rmsPeaks[5:10],nilsC[5:10],avPeaks[5:10])], 'x:')#, label='C=1nm')
    axs[1,1].plot(labels[10:15], [rI*n[0]*aI for rI, n, aI in zip(rmsPeaks[10:15],nilsC[10:15],avPeaks[10:15])], 'x:')#, label='C=1nm')
    axs[1,1].plot(labels[15:20], [rI*n[0]*aI for rI, n, aI in zip(rmsPeaks[15:20],nilsC[15:20],avPeaks[15:20])], 'x:')#, label='C=1nm')
    axs[1,1].plot(labels[20::], [rI*n[0]*aI for rI, n, aI in zip(rmsPeaks[20::],nilsC[20::],avPeaks[20::])], 'x:')#, label='C=1nm')
    axs[1,1].set_title("rms I x NILS x Average I")
    # axs[1,1].set_ylim(0.9997,0.99975)
    axs[1,2].plot(labels[0:5], [r*c[0] for r, c in zip(rmsC[0:5],compositeC[0:5])], 'x:')#, label='C=1nm')
    axs[1,2].plot(labels[5:10], [r*c[0] for r, c in zip(rmsC[5:10],compositeC[5:10])], 'x:')#, label='C=1nm')
    axs[1,2].plot(labels[10:15], [r*c[0] for r, c in zip(rmsC[10:15],compositeC[10:15])], 'x:')#, label='C=1nm')
    axs[1,2].plot(labels[15:20], [r*c[0] for r, c in zip(rmsC[15:20],compositeC[15:20])], 'x:')#, label='C=1nm')
    axs[1,2].plot(labels[20::], [r*c[0] for r, c in zip(rmsC[20::],compositeC[20::])], 'x:')#, label='C=1nm')
    axs[1,2].set_title("RMS x Composite")
    # axs[1,2].set_ylabel("NILS")
    if sepBy == 'cLength':
        axs[1,0].set_xlabel('$C_y [nm]$')
        axs[1,1].set_xlabel('$C_y [nm]$')
        axs[1,2].set_xlabel('$C_y [nm]$')
    elif sepBy == 'RMS':
        axs[1,0].set_xlabel('\u03C3 [nm]')
        axs[1,1].set_xlabel('\u03C3 [nm]')
        axs[1,2].set_xlabel('\u03C3 [nm]')
    fig.tight_layout()
    # fig.subplots_adjust(bottom=0.2)   ##  Need to play with this number.
    # if sepBy == 'RMS':
    #     plt.legend(labels=['$C_y$ [nm]: ' + str(l) for l in [1,5,10,15,25]], loc="lower center", ncol=5)
    # elif sepBy == 'cLength':
    #     plt.legend(labels=['\u03C3 [nm]: ' + str(l) for l in [1,2,5,10,15]], loc="lower center", ncol=5)
    if save:
        plt.savefig(savePath + 'contrastAllSep_horOrientation_electrons.pdf')
        plt.savefig(savePath + 'contrastAllSep_horOrientation_electrons.png', dpi=2000)
    else:
        pass
    plt.show()
    
    for ax in fig.axes:
        ax.legend()
        if variable == '\u03C3 [nm]':
                ax.set_xticklabels(labels, rotation=45, ha='right')
    fig.tight_layout()
    if save:
        plt.savefig(savePath + 'contrastAllSep_horOrientation_electrons.pdf')
        plt.savefig(savePath + 'contrastAllSep_horOrientation_electrons.png', dpi=2000)
    plt.show()
elif variable == 'exitSlit':
    # if sepBy == 'RMS':
    axs[0,0].plot(labels, [n[0]*aI*tI for n, aI, tI in zip(nilsC,avPeaks,sumPeaks)], 'x:')#, label='C=1nm')
    axs[0,0].set_title("NILS x Average I x Total I")
    axs[0,0].set_ylabel("Contrast")
    axs[0,1].plot(labels, [r*aI*tI for r, aI, tI in zip(rmsC,avPeaks,sumPeaks)], 'x:')#, label='C=1nm')
    axs[0,1].set_title("RMS x Average I x Total I")
    axs[0,2].plot(labels, [c[0]*n[0]*aI for c, n, aI in zip(compositeC,nilsC,avPeaks)], 'x:')#, label='C=1nm')
    axs[0,2].set_title("Composite x NILS x Average I")
    axs[1,0].plot(labels, [c[0]*n[0]*r for c, n, r in zip(compositeC,nilsC,rmsC)], 'x:')#, label='C=1nm')
    axs[1,0].set_title("Composite x NILS x RMS")
    axs[1,0].set_ylabel("Contrast")
    axs[1,1].plot(labels, [rI*n[0]*aI for rI, n, aI in zip(rmsPeaks,nilsC,avPeaks)], 'x:')#, label='C=1nm')
    axs[1,1].set_title("rms I x NILS x Average I")
    # axs[1,1].set_ylim(0.9997,0.99975)
    axs[1,2].plot(labels, [r*c[0] for r, c in zip(rmsC,compositeC)], 'x:')#, label='C=1nm')
    axs[1,2].set_title("RMS x Composite")
    # axs[1,2].set_ylabel("NILS")
    axs[1,0].set_xlabel('Slit Width')
    axs[1,1].set_xlabel('Slit Width')
    axs[1,2].set_xlabel('Slit Width')
    fig.tight_layout()
    plt.show()

if printContrast:
    for i in range(0,len(labels)):
        print(" ")
        print("profile #{} ----------------------------------------".format(i+1))
        print(labels[i])
        print("Michelson Contrast:              {}".format(michelsonC[i]))
        print("RMS Contrast:                    {}".format(rmsC[i]))
        print("Fourier Contrast:                {}".format(fourierC[i][0]))
        print("Composite Contrast:              {}".format(compositeC[i][0]))
        print("Imbalance Contrast:              {}".format(compositeC[i][2]))
        print("MDR Contrast:                    {}".format(compositeC[i][1]))
        print("NILS:                            {}".format(nilsC[i][0]))
        print("Fidelity:                        {}".format(fidel[i]))
        print("RMS x COMPOSITE                  {}".format(rmsC[i]*compositeC[i][0]))
    print("")
    print("Difference in Contrast -----------------------------")
    print("Michelson Contrast:              {}".format(michelsonC[0]-michelsonC[1]))
    print("RMS Contrast:                    {}".format(rmsC[0]-rmsC[1]))
    print("Fourier Contrast:                {}".format(fourierC[0][0]-fourierC[1][0]))
    print("Composite Contrast:              {}".format(compositeC[0][0]-compositeC[1][0]))
    print("Imbalance Contrast:              {}".format(compositeC[0][2]-compositeC[1][2]))
    print("MDR Contrast:                    {}".format(compositeC[0][1]-compositeC[1][1]))
    print("NILS:                            {}".format(nilsC[0][0]-nilsC[1][0]))
    print("Fidelity:                        {}".format(fidel[0]-fidel[1]))
    
# PLOT RMS C x COMPOSITE C
if variable == '\u03C3 [nm]':
    plt.plot(labelsH[0:5], [r*c[0] for r, c in zip(rmsC[0:5],compositeC[0:5])], 'x:')#, label='C=1nm')
    plt.plot(labelsH[5:10], [r*c[0] for r, c in zip(rmsC[5:10],compositeC[5:10])], 'x:')#, label='C=1nm')
    plt.plot(labelsH[10:15], [r*c[0] for r, c in zip(rmsC[10:15],compositeC[10:15])], 'x:')#, label='C=1nm')
    plt.plot(labelsH[15:20], [r*c[0] for r, c in zip(rmsC[15:20],compositeC[15:20])], 'x:')#, label='C=1nm')
    plt.plot(labelsH[20::], [r*c[0] for r, c in zip(rmsC[20::],compositeC[20::])], 'x:')#, label='C=1nm')
    plt.title("RMS x Composite")    
    if sepBy == 'RMS':
        plt.xlabel('\u03C3 [nm]')
    elif sepBy == 'cLength':
        plt.xlabel('$C_y [nm]$')
    # fig.tight_layout()
    # fig.subplots_adjust(bottom=0.5)   ##  Need to play with this number.
    # if sepBy == 'RMS':
    #     plt.legend(['$C_y$ [nm]: ' + str(l) for l in [1,5,10,15,25]], loc="lower center", ncol=5)
    # elif sepBy == 'cLength':
    #     plt.legend(['\u03C3 [nm]: ' + str(l) for l in [1,2,5,10,15]], loc="lower center", ncol=5)
    if save:
        plt.savefig(savePath + 'contrastAllSep_horOrientation_electrons.pdf')
        plt.savefig(savePath + 'contrastAllSep_horOrientation_electrons.png', dpi=2000)
    else:
        pass
    plt.show()
    
    
dataStructure = [labelsRMS, labelsClength,avPeaks,totIN,rmsPeaks,
                  michelsonC,rmsC,[c[0] for c in compositeC],
                  [f[0] for f in fourierC],[n[0] for n in nilsC],
                  fidel,
                  [n[0]*aI*tI for n, aI, tI in zip(nilsC,avPeaks,sumPeaks)],
                  [r*aI*tI for r, aI, tI in zip(rmsC,avPeaks,sumPeaks)],
                  [c[0]*n[0]*aI for c, n, aI in zip(compositeC,nilsC,avPeaks)],
                  [c[0]*n[0]*r for c, n, r in zip(compositeC,nilsC,rmsC)],
                  [rI*n[0]*aI for rI, n, aI in zip(rmsPeaks,nilsC,avPeaks)],
                  [r*c[0] for r,c in zip(rmsC,compositeC)]]

# print(len(labels))
# print("Shape of data structure: ", np.shape(dataStructure))
import pandas as pd
# dF = pd.DataFrame(np.concatenate([labels,avPeaks,sumPeaks,rmsPeaks,
#                              michelsonC,rmsC,[c[0] for c in compositeC],
#                              [f[0] for f in fourierC],[n[0] for n in nilsC]]),
dF = pd.DataFrame(np.array(dataStructure).T,
                  columns=['RMS roughness','Corr Length','Average I Peak', 'Sum I', 'rms I Peaks',
                           'Michelson C', 'rms C', 'composite C',
                           'fourier C', 'NILS', 'Fidelity',
                           "NILS x Average I x Total I","rms C x Average I x Total I","Composite C x NILS x Average I",
                           "Composite C x NILS x rms C","rms I x NILS x Average I",'rms C x composite C'])
correlations = dF.corr() 
import seaborn as sns

sns.heatmap(correlations,cmap='vlag',vmin=-1,vmax=1)
plt.show()

    
