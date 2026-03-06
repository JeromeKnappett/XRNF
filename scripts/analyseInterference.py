#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 15 12:57:29 2021

@author: -
"""
import tifffile
import numpy as np
import matplotlib.pyplot as plt
import interferenceGratingModelsJK as interferenceGratingModelsJK
from math import log10, floor

colours = plt.rcParams["axes.prop_cycle"].by_key()["color"]

def round_sig(x, sig=2):
    if x != 0:
        return round(x, sig-int(floor(log10(abs(x))))-1)
    else:
        return x
    
Ipath = '/user/home/opt/xl/xl/experiments/fullBeamPolarisation3/data/'

ranV = ['ideal', 'test1', 'test2']

electrons = [100, 1000, 2000, 3000, 4000, 5000, 10000]

sepBy ='RMS'# # 'RMS' #'cLength' #
addBlock = True

if sepBy == 'RMS':
    order = [0,1,2,3,4,      # c = 1 nm
             5,9,        # c = 5 nm
             10,14,      # c = 10 nm 
             15,18,19,      # c = 15 nm
             20,21,22,23,24] # c = 25 nm
if sepBy == 'cLength':
    order = [0,5,10,15,20,   # r = 1 nm
             1,21,       # r = 2 nm
             2,22,       # r = 5 nm
             3,18,23,       # r = 10 nm
             4,9,14,19,24]  # r = 15 nm

filesH = [str(o) + 'intensity.tif' for o in order] #['fullRes_4000eintensity.tif'] #['TEintensity.tif', 'TMintensity.tif']  #['fullRes_' + str(n) + 'eintensity.tif' for n in electrons] #['fullRes_4000eintensity.tif']  # horizontally oriented
filesV = ['ideal_20nmintensity.tif','roughness1intensity.tif', 'roughness2intensity.tif', 'roughness3intensity.tif', 'roughness4intensity.tif']#['4000eintensity_vertical.tif'] #['ideal_20nmintensity.tif','roughness1intensity.tif', 'roughness2intensity.tif', 'roughness3intensity.tif', 'roughness4intensity.tif']#, '1stTestintensity.tif', '2ndTestintensity.tif'] # vertically oriented
# print(filesH[0:4])
# print(filesH[4:7])
pitch = 14
justBlockFile = str(pitch) + 'pBlockintensity.tif'

# filesH = filesH + justBlockFile
# filesV = filesV + justBlockFile

ver = False
hor = True

printContrast = False

save = False
savePath = '/home/jerome/Documents/MASTERS/Figures/plots/'

variable ='Polarisation' #  # #'Polarisation' #'\u03C3 [nm]' # '$N_e$'

labelsH = ['hor'] #['TE-TE', 'TM-TM'] #[str(n) for i,n in enumerate(electrons)]# if i!=1]
labelsV =[0, 1, 2, 5, 10] # ['ver'] #[0, 1, 2, 5, 10] # '\u03C3 = 2 nm', '\u03C3 = 5 nm', '\u03C3 = 10 nm'] #['ver: ' + str(r) for r in ranV]

# sigma - \u03C3
pitch = 14

plotRange = 2000 # in nm

justBlockRes = 2.501122539655539e-09, 2.658184225986154e-07

resH, resV, resH1000 =  1.9651759267701173e-09, 1.8194278317912603e-9, 2.1488320941276643e-09 # resolution of each tif along axis perpendicular to fringes


lowresH, lowresV = 2.658184225988639e-07, 3.314297299424348e-07

#defining middle points of each array
midH = 64, 16377   
midV = 112, 13477
midH1000 = 144, 21159

midB = 65, (12899) # + int((6.9375e-6/justBlockRes[0])))

print(midB)


# number of pixels to sample along each direction
N_par, N_per = 2000, 140
if variable == 'Polarisation':
    if pitch == 24:
        resH,resH1000 =  6.46327159071368e-10, 4.77529829067939e-10
        justBlockRes = 2.5011152174125335e-09, 2.6581841242337273e-07
        resTE, resTM = resH, resH1000
        midH = 190, 70348
        midH1000 = 80, 67045
    elif pitch == 14:
        resH,resH1000 = 3.231632826772039e-10, 2.387645475770844e-10
        justBlockRes = 2.5011141910134883e-09, 2.658184225986154e-07
        resTE, resTM = resH, resH1000
        midH = 350, 140696
        midH1000 = 158, 134089
    labelsH = ['TE', 'TM']
    filesH = ['TE/TEintensity.tif', 'TM/TMintensity.tif']
elif variable == '\u03C3 [nm]':
    if hor:
        resH = 2.501122539655539e-09
        midH = 65, 12899 #+ int((13.875e-6/justBlockRes[0])))
        # Input Values
        if sepBy == 'RMS':
            labelsH = [1, 2, 5, 10, 15,
                       1,15,
                       1,15,
                       1,10,15,
                       1, 2, 5, 10, 15] #['\u03C3:1nm,C:1nm','\u03C3:2nm,C:1nm','\u03C3:5nm,C:1nm', '\u03C3:15nm,C:1nm']#, 
                        # '\u03C3:1nm,C:15nm','\u03C3:15nm,C:5nm',
                        # '\u03C3:1nm,C:25nm','\u03C3:10nm,C:25nm', '\u03C3:15nm,C:25nm']
        else:
            labelsH = [1,5,10,15,25,
                       1,25,
                       1,25,
                       1,15,25,
                       1,5,10,15,25]
        # Output Values
        # labelsH = ['\u03C3:0.66nm,C:1nm','\u03C3:1.2nm,C:1nm','\u03C3:2.7nm,C:1nm', '\u03C3:7.6nm,C:1nm']#, 
                   # '\u03C3:1nm,C:15nm','\u03C3:15nm,C:5nm',
                   # '\u03C3:1nm,C:25nm','\u03C3:10nm,C:25nm', '\u03C3:15nm,C:25nm']
        
    
# redefining number of pixels for vertical array to match the range sampled in horizontal
nV = round((resH*N_par)/resV)
rangeV = resV*nV
rangeH = resH*N_par
M = round((resH*N_par)/resH1000)
B = round((rangeH)/justBlockRes[0])
rangeH1000 = resH1000*M
print("Range Hor: {} m".format(rangeH))
print("Range Hor - 2: {} m".format(rangeH1000))
print("Range B: {} m".format(justBlockRes[0]*B))
print("Range Ver: {} m".format(rangeV))
print("nH, nV, M, B :", N_par, nV, M, B)

    
    
    
# read tiff files
if hor:
    tiffsH = [tifffile.imread(Ipath + f) for f in filesH]
    tiffBlock = tifffile.imread('/user/home/opt/xl/xl/experiments/blockDiffraction/data/' + str(pitch) + 'pBlock/' +  str(justBlockFile))
    print(np.shape(tiffsH[1]))
    plt.imshow(tiffsH[0], aspect='auto')
    plt.title("intensity tif - TE")
    plt.show()
    plt.imshow(tiffsH[1], aspect='auto')
    plt.title("intensity tif - TM")
    plt.show()
    imageH = [t[midH[0]-N_per:midH[0]+N_per, midH[1]-N_par:midH[1]+N_par] for t in tiffsH]
    print("shape of tiffs: ", np.shape(tiffsH))
    print("shape of images: ", np.shape(imageH))
    print("shape of blockImage: ", np.shape(tiffBlock))
    if variable == 'Polarisation':
        try:
            imageH = tiffsH[0][midH[0]-N_per:midH[0]+N_per, midH[1]-N_par:midH[1]+N_par]
            imageH1000 = tiffsH[1][midH1000[0]-N_per:midH1000[0]+N_per, midH1000[1]-M:midH1000[1]+M]
            plt.imshow(imageH1000, aspect='auto')
            plt.title("aerial image - TM")
            plt.show()
            plt.imshow(imageH, aspect='auto')
            plt.title("aerial image - TE")
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
    plt.plot(aerialImageBlock)
    plt.show()
#    aerialImagesH = [a-aerialImageBlock for a in aerialImagesH]
    # aerialImagesH = aerialImagesH + aerialImageBlock
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
xB = np.linspace(-B*justBlockRes[0],B*justBlockRes[0],2*B)

''' define interference grating parameters'''
wl = 6.710553853647976e-9 # wavelength in m

# Amplitude of both beams (assumed equal)
A = 0.25e5 # 0.37e5 #0.3e5  # this may be scaled to  match simulated intensity
k = 2*np.pi/wl
m = 1 # order of diffracted beams from each grating
d = 24e-9 #24e-9 #100e-9 # grating spacing
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
    # plt.plot(xH*1e9,IH, ':', label='Model amplitude')
    # for i, a in enumerate(I):
    #     plt.plot(xH*1e9, a, linewidth=1, color=colours[i], label=str(round_sig(1/sigma[i])))
    if variable == 'Polarisation':
        for i, a in enumerate(aerialImagesH[0:2]): #[0:4]
            print("# ", i)
        #     plt.plot(xH*1e9, a, linewidth=1, color=colours[i], label=str(labelsH[i])) #'\u03C3 [nm]: ' + str(labelsH[i]) + ',C [nm]: 1')
        # for i, a in enumerate(aerialImagesH[4::]):
        #     plt.plot(xH*1e9, a, linewidth=1, color=colours[i+4], label='\u03C3 [nm]: ' + str(labelsH[i]) + ',C [nm]: 25')
            if i==0:
                plt.plot(xH*1e9, a, linewidth=1, color=colours[i], label=str(labelsH[i])) #'$N_e$ = '
            if i==1:
                plt.plot(xH1000*1e9, a, label=str(labelsH[i]), linewidth=1, color=colours[i])
        plt.plot(xB*1e9,(aerialImageBlock/np.max(aerialImageBlock)),color='red',label='Block')
        plt.xlim(-plotRange/2,plotRange/2)
        plt.legend()
    else:
        fig,axs = plt.subplots(5,1)
        fig.set_size_inches(6.0, 12.0)
        for i, a in enumerate(aerialImagesH[0:5]): #[0:4]
            if sepBy == 'RMS':
                axs[0].plot(xH*1e9, a, linewidth=1, color=colours[i])#, label='\u03C3 [nm]: ' + str(labelsH[i]))# + ',C [nm]: 1')
            else:
                axs[0].plot(xH*1e9, a, linewidth=1, color=colours[i])#, label='$C_y$ [nm]: ' + str(labelsH[i]))# + ',\u03C3 [nm]: 1')
        for i, a in enumerate(aerialImagesH[5:7]):
            if sepBy == 'RMS':
                axs[1].plot(xH*1e9, a, linewidth=1, color=colours[i])#, label='\u03C3 [nm]: ' + str(labelsH[i]) + ',C [nm]: 5')
            else:
                axs[1].plot(xH*1e9, a, linewidth=1, color=colours[i])#, label='$C_y$ [nm]: ' + str(labelsH[i]) + ',\u03C3 [nm]: 2')
        for i, a in enumerate(aerialImagesH[7:9]):
            if sepBy == 'RMS':
                axs[2].plot(xH*1e9, a, linewidth=1, color=colours[i])#, label='\u03C3 [nm]: ' + str(labelsH[i]) + ',C [nm]: 10')
            else:
                axs[2].plot(xH*1e9, a, linewidth=1, color=colours[i])#, label='$C_y$ [nm]: ' + str(labelsH[i]) + ',\u03C3 [nm]: 5')
        for i, a in enumerate(aerialImagesH[9:12]):
            if sepBy == 'RMS':
                axs[3].plot(xH*1e9, a, linewidth=1, color=colours[i])#, label='\u03C3 [nm]: ' + str(labelsH[i]) + ',C [nm]: 15')
            else:
                axs[3].plot(xH*1e9, a, linewidth=1, color=colours[i])#, label='$C_y$ [nm]: ' + str(labelsH[i]) + ',\u03C3 [nm]: 10')
        for i, a in enumerate(aerialImagesH[12::]):
            if sepBy == 'RMS':
                axs[4].plot(xH*1e9, a, linewidth=1, color=colours[i])#, label='\u03C3 [nm]: ' + str(labelsH[i]))# + ',C [nm]: 25')
            else:
                axs[4].plot(xH*1e9, a, linewidth=1, color=colours[i])#, label='$C_y$ [nm]: ' + str(labelsH[i]))# + ',\u03C3 [nm]: 15')
        for ax in fig.axes:
            if addBlock:
                ax.plot(xH*1e9, (aerialImageBlock), linewidth=1, color='red', label='Block')
                ax.legend()
            ax.set_xlim(-plotRange/2,plotRange/2)
            ax.set_ylabel('Intensity [ph/s/.1%bw/mm$^2$]')
        # axs[4].legend(loc='lower center', fontsize='small', #title='Simulated Electrons ($N_e$)', 
        #     bbox_to_anchor=(0.5, -3.3),fancybox=True, shadow=True,ncol=5)
        # axs[2].set_ylabel('Intensity [ph/s/.1%bw/mm$^2$]')
        axs[4].set_xlabel('Position [nm]')
        if sepBy == 'RMS':
            axs[0].text(plotRange*(-1/2 - 1/10) , -200000000, '$C_y = 1 nm$', {'color': 'red', 'fontsize': 6})
            axs[1].text(-540, -200000000, '$C_y = 5 nm$', {'color': 'red', 'fontsize': 6})
            axs[2].text(-540, -200000000, '$C_y = 10 nm$', {'color': 'red', 'fontsize': 6})
            axs[3].text(-540, -200000000, '$C_y = 15 nm$', {'color': 'red', 'fontsize': 6})
            axs[4].text(-540, -200000000, '$C_y = 25 nm$', {'color': 'red', 'fontsize': 6})
        else:
            axs[0].text(plotRange*(-1/2 - 1/10), -30000000, '\u03C3 = 1 nm', {'color': 'red', 'fontsize': 9})
            axs[1].text(plotRange*(-1/2 - 1/10), -30000000, '\u03C3 = 2 nm', {'color': 'red', 'fontsize': 9})
            axs[2].text(plotRange*(-1/2 - 1/10), -30000000, '\u03C3 = 5 nm', {'color': 'red', 'fontsize': 9})
            axs[3].text(plotRange*(-1/2 - 1/10), -30000000, '\u03C3 = 10 nm', {'color': 'red', 'fontsize': 9})
            axs[4].text(plotRange*(-1/2 - 1/10), -30000000, '\u03C3 = 15 nm', {'color': 'red', 'fontsize': 9})
            
            
        fig.tight_layout()
        
        fig.subplots_adjust(bottom=0.06)   ##  Need to play with this number.
        if sepBy == 'RMS':
            fig.legend(labels=['\u03C3 [nm]: ' + str(l) for l in labelsH[0:5]], loc="lower center", ncol=5)
        else:
            fig.legend(labels=['$C_y$ [nm]: ' + str(l) for l in labelsH[0:5]], loc="lower center", ncol=5)
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
print("here")
#print(nilsC[6])
print(nilsC[0][7])
print(np.shape(nilsC[0]))


plt.plot(xH*1e9,aerialImagesH[0])
plt.plot(xH[nilsC[0][7]]*1e9,aerialImagesH[0][nilsC[0][7]], 'x')
plt.xlim(-100,100)
plt.show()

sumPeaks = []
avPeaks = []
rmsPeaks = []

for a in aerialImagesH:
    peaks = [a[n] for n in nilsC[0][7]]
    sumPeak = np.sum(peaks)
    avPeak = np.mean(peaks)
    rmsPeak = np.sqrt(np.mean([p**2 for p in peaks]))
    
    sumPeaks.append(sumPeak)
    avPeaks.append(avPeak)
    rmsPeaks.append(rmsPeak)
    
fig, axs = plt.subplots(1,4)
axs[0].plot(sumPeaks[0:5], 'x:')
axs[0].plot(sumPeaks[5:7], 'x:')
axs[0].plot(sumPeaks[7:9], 'x:')
axs[0].plot(sumPeaks[9:12], 'x:')
axs[0].plot(sumPeaks[12::], 'x:')
axs[1].plot(avPeaks[0:5], 'x:')
axs[1].plot(avPeaks[5:7], 'x:')
axs[1].plot(avPeaks[7:9], 'x:')
axs[1].plot(avPeaks[9:12], 'x:')
axs[1].plot(avPeaks[12::], 'x:')
axs[2].plot(rmsPeaks[0:5], 'x:')
axs[2].plot(rmsPeaks[5:7], 'x:')
axs[2].plot(rmsPeaks[7:9], 'x:')
axs[2].plot(rmsPeaks[9:12], 'x:')
axs[2].plot(rmsPeaks[12::], 'x:')
axs[3].plot([c[0] for c in compositeC[0:5]], 'x:')
axs[3].plot([c[0] for c in compositeC[5:7]], 'x:')
axs[3].plot([c[0] for c in compositeC[7:9]], 'x:')
axs[3].plot([c[0] for c in compositeC[9:12]], 'x:')
axs[3].plot([c[0] for c in compositeC[12::]], 'x:')
axs[0].set_ylabel('Sum of peak heights')
axs[1].set_ylabel('Average peak height')
axs[2].set_ylabel('RMS peak height')
axs[3].set_ylabel('Composite Contrast')
fig.tight_layout()
fig.subplots_adjust(bottom=0.2)   ##  Need to play with this number.
if sepBy == 'RMS':
    fig.legend(labels=['\u03C3 [nm]: ' + str(l) for l in labelsH[0:5]], loc="lower center", ncol=5)
else:
    fig.legend(labels=['$C_y$ [nm]: ' + str(l) for l in labelsH[0:5]], loc="lower center", ncol=5)
plt.show()

# Plotting all contrast metrics together
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
    axs[0,0].plot(labels[5:7], michelsonC[5:7], 'x:')#, label='C=5nm')
    axs[0,0].plot(labels[7:9], michelsonC[7:9], 'x:')#, label='C=10nm')
    axs[0,0].plot(labels[9:12], michelsonC[9:12], 'x:')#, label='C=15nm')
    axs[0,0].plot(labels[12::], michelsonC[12::], 'x:')#, label='C=25nm')
    axs[0,0].set_title("Michelson")
    axs[0,0].set_ylabel("Contrast")
    axs[0,1].plot(labels[0:5], rmsC[0:5], 'x:')#, label='C=1nm')
    axs[0,1].plot(labels[5:7], rmsC[5:7], 'x:')#, label='C=25nm')
    axs[0,1].plot(labels[7:9], rmsC[7:9], 'x:')#, label='C=1nm')
    axs[0,1].plot(labels[9:12], rmsC[9:12], 'x:')#, label='C=1nm')
    axs[0,1].plot(labels[12::], rmsC[12::], 'x:')#, label='C=1nm')
    axs[0,1].set_title("RMS")
    axs[0,2].plot(labels[0:5], [c[0] for c in compositeC[0:5]], 'x:')#, label='C=1nm')
    axs[0,2].plot(labels[5:7], [c[0] for c in compositeC[5:7]], 'x:')#, label='C=1nm')
    axs[0,2].plot(labels[7:9], [c[0] for c in compositeC[7:9]], 'x:')#, label='C=1nm')
    axs[0,2].plot(labels[9:12], [c[0] for c in compositeC[9:12]], 'x:')#, label='C=1nm')
    axs[0,2].plot(labels[12::], [c[0] for c in compositeC[12::]], 'x:')#, label='C=1nm')
    axs[0,2].set_title("Composite")
    axs[1,0].plot(labels[0:5], [f[0] for f in  fourierC[0:5]], 'x:')#, label='C=1nm')
    axs[1,0].plot(labels[5:7], [f[0] for f in  fourierC[5:7]], 'x:')#, label='C=1nm')
    axs[1,0].plot(labels[7:9], [f[0] for f in  fourierC[7:9]], 'x:')#, label='C=1nm')
    axs[1,0].plot(labels[9:12], [f[0] for f in  fourierC[9:12]], 'x:')#, label='C=1nm')
    axs[1,0].plot(labels[12::], [f[0] for f in  fourierC[12::]], 'x:')#, label='C=1nm')
    axs[1,0].set_title("Fourier")
    axs[1,0].set_ylabel("Contrast")
    axs[1,1].set_title("NILS")
    axs[1,1].plot(labels[0:5], fidel[0:5], 'x:')#, label='C=1nm')
    axs[1,1].plot(labels[5:7], fidel[5:7], 'x:')#, label='C=1nm')
    axs[1,1].plot(labels[7:9], fidel[7:9], 'x:')#, label='C=1nm')
    axs[1,1].plot(labels[9:12], fidel[9:12], 'x:')#, label='C=1nm')
    axs[1,1].plot(labels[12::], fidel[12::], 'x:')#, label='C=1nm')
    axs[1,1].set_title("Fidelity")
    # axs[1,1].set_ylim(0.9997,0.99975)
    axs[1,2].plot(labels[0:5], [n[0] for n in nilsC[0:5]], 'x:')#, label='C=1nm')
    # if variable == '\u03C3 [nm]':
    axs[1,2].plot(labels[5:7], [n[0] for n in nilsC[5:7]], 'x:')#, label='C=1nm')
    axs[1,2].plot(labels[7:9], [n[0] for n in nilsC[7:9]], 'x:')#, label='C=1nm')
    axs[1,2].plot(labels[9:12], [n[0] for n in nilsC[9:12]], 'x:')#, label='C=1nm')
    axs[1,2].plot(labels[12::], [n[0] for n in nilsC[12::]], 'x:')#, label='C=1nm')
    axs[1,2].set_title("NILS - mean")
    axs[1,2].set_ylabel("NILS")
    if sepBy == 'RMS':
        axs[1,0].set_xlabel('$C_y [nm]$')
        axs[1,1].set_xlabel('$C_y [nm]$')
        axs[1,2].set_xlabel('$C_y [nm]$')
    else:
        axs[1,0].set_xlabel('\u03C3 [nm]')
        axs[1,1].set_xlabel('\u03C3 [nm]')
        axs[1,2].set_xlabel('\u03C3 [nm]')
    fig.tight_layout()
    fig.subplots_adjust(bottom=0.2)   ##  Need to play with this number.
    if sepBy == 'RMS':
        fig.legend(labels=['\u03C3 [nm]: ' + str(l) for l in labelsH[0:5]], loc="lower center", ncol=5)
    else:
        fig.legend(labels=['$C_y$ [nm]: ' + str(l) for l in labelsH[0:5]], loc="lower center", ncol=5)
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
    
else:
    fig, axs = plt.subplots(2,3)
    
    axs[0,0].plot(labels, michelsonC)
    axs[0,0].set_title("Michelson")
    axs[0,1].plot(labels, rmsC)
    axs[0,1].set_title("RMS")
    axs[0,2].plot(labels, [c[0] for c in compositeC])
    axs[0,2].set_title("Composite")
    axs[1,0].plot(labels, [f[0] for f in  fourierC])
    axs[1,0].set_title("Fourier")
    axs[1,1].plot(labels, [n[0] for n in nilsC])
    axs[1,1].set_title("NILS")
    axs[1,2].plot(labels, fidel)
    axs[1,2].set_title("Fidelity")
    fig.tight_layout()
    plt.show()
print(np.shape(fidel))
print(michelsonC[4::])


# Testing out combinations of metrics
fig, axs = plt.subplots(2,3)

if variable == '\u03C3 [nm]':
    # if sepBy == 'RMS':
    axs[0,0].plot(labels[0:5], [n[0]*aI*tI for n, aI, tI in zip(nilsC[0:5],avPeaks[0:5],sumPeaks[0:5])], 'x:')#, label='C=1nm')
    axs[0,0].plot(labels[5:7], [n[0]*aI*tI for n, aI, tI in zip(nilsC[5:7],avPeaks[5:7],sumPeaks[5:7])], 'x:')#, label='C=5nm')
    axs[0,0].plot(labels[7:9], [n[0]*aI*tI for n, aI, tI in zip(nilsC[7:9],avPeaks[7:9],sumPeaks[7:9])], 'x:')#, label='C=10nm')
    axs[0,0].plot(labels[9:12], [n[0]*aI*tI for n, aI, tI in zip(nilsC[9:12],avPeaks[9:12],sumPeaks[9:12])], 'x:')#, label='C=15nm')
    axs[0,0].plot(labels[12::], [n[0]*aI*tI for n, aI, tI in zip(nilsC[12::],avPeaks[12::],sumPeaks[12::])], 'x:')#, label='C=25nm')
    axs[0,0].set_title("NILS x Average I x Total I")
    axs[0,0].set_ylabel("Contrast")
    axs[0,1].plot(labels[0:5], [r*aI*tI for r, aI, tI in zip(rmsC[0:5],avPeaks[0:5],sumPeaks[0:5])], 'x:')#, label='C=1nm')
    axs[0,1].plot(labels[5:7], [r*aI*tI for r, aI, tI in zip(rmsC[5:7],avPeaks[5:7],sumPeaks[5:7])], 'x:')#, label='C=25nm')
    axs[0,1].plot(labels[7:9], [r*aI*tI for r, aI, tI in zip(rmsC[7:9],avPeaks[7:9],sumPeaks[7:9])], 'x:')#, label='C=1nm')
    axs[0,1].plot(labels[9:12], [r*aI*tI for r, aI, tI in zip(rmsC[9:12],avPeaks[9:12],sumPeaks[9:12])], 'x:')#, label='C=1nm')
    axs[0,1].plot(labels[12::], [r*aI*tI for r, aI, tI in zip(rmsC[12::],avPeaks[12::],sumPeaks[12::])], 'x:')#, label='C=1nm')
    axs[0,1].set_title("RMS x Average I x Total I")
    axs[0,2].plot(labels[0:5], [c[0]*n[0]*aI for c, n, aI in zip(compositeC[0:5],nilsC[0:5],avPeaks[0:5])], 'x:')#, label='C=1nm')
    axs[0,2].plot(labels[5:7], [c[0]*n[0]*aI for c, n, aI in zip(compositeC[5:7],nilsC[5:7],avPeaks[5:7])], 'x:')#, label='C=1nm')
    axs[0,2].plot(labels[7:9], [c[0]*n[0]*aI for c, n, aI in zip(compositeC[7:9],nilsC[7:9],avPeaks[7:9])], 'x:')#, label='C=1nm')
    axs[0,2].plot(labels[9:12], [c[0]*n[0]*aI for c, n, aI in zip(compositeC[9:12],nilsC[9:12],avPeaks[9:12])], 'x:')#, label='C=1nm')
    axs[0,2].plot(labels[12::], [c[0]*n[0]*aI for c, n, aI in zip(compositeC[12::],nilsC[12::],avPeaks[12::])], 'x:')#, label='C=1nm')
    axs[0,2].set_title("Composite x NILS x Average I")
    axs[1,0].plot(labels[0:5], [c[0]*n[0]*r for c, n, r in zip(compositeC[0:5],nilsC[0:5],rmsC[0:5])], 'x:')#, label='C=1nm')
    axs[1,0].plot(labels[5:7], [c[0]*n[0]*r for c, n, r in zip(compositeC[5:7],nilsC[5:7],rmsC[5:7])], 'x:')#, label='C=1nm')
    axs[1,0].plot(labels[7:9], [c[0]*n[0]*r for c, n, r in zip(compositeC[7:9],nilsC[7:9],rmsC[7:9])], 'x:')#, label='C=1nm')
    axs[1,0].plot(labels[9:12], [c[0]*n[0]*r for c, n, r in zip(compositeC[9:12],nilsC[9:12],rmsC[9:12])], 'x:')#, label='C=1nm')
    axs[1,0].plot(labels[12::], [c[0]*n[0]*r for c, n, r in zip(compositeC[12::],nilsC[12::],rmsC[12::])], 'x:')#, label='C=1nm')
    axs[1,0].set_title("Composite x NILS x RMS")
    axs[1,0].set_ylabel("Contrast")
    axs[1,1].plot(labels[0:5], [rI*n[0]*aI for rI, n, aI in zip(rmsPeaks[0:5],nilsC[0:5],avPeaks[0:5])], 'x:')#, label='C=1nm')
    axs[1,1].plot(labels[5:7], [rI*n[0]*aI for rI, n, aI in zip(rmsPeaks[5:7],nilsC[5:7],avPeaks[5:7])], 'x:')#, label='C=1nm')
    axs[1,1].plot(labels[7:9], [rI*n[0]*aI for rI, n, aI in zip(rmsPeaks[7:9],nilsC[7:9],avPeaks[7:9])], 'x:')#, label='C=1nm')
    axs[1,1].plot(labels[9:12], [rI*n[0]*aI for rI, n, aI in zip(rmsPeaks[9:12],nilsC[9:12],avPeaks[9:12])], 'x:')#, label='C=1nm')
    axs[1,1].plot(labels[12::], [rI*n[0]*aI for rI, n, aI in zip(rmsPeaks[12::],nilsC[12::],avPeaks[12::])], 'x:')#, label='C=1nm')
    axs[1,1].set_title("rms I x NILS x Average I")
    # axs[1,1].set_ylim(0.9997,0.99975)
    axs[1,2].plot(labels[0:5], [r*c[0] for r, c in zip(rmsC[0:5],compositeC[0:5])], 'x:')#, label='C=1nm')
    axs[1,2].plot(labels[5:7], [r*c[0] for r, c in zip(rmsC[5:7],compositeC[5:7])], 'x:')#, label='C=1nm')
    axs[1,2].plot(labels[7:9], [r*c[0] for r, c in zip(rmsC[7:9],compositeC[7:9])], 'x:')#, label='C=1nm')
    axs[1,2].plot(labels[9:12], [r*c[0] for r, c in zip(rmsC[9:12],compositeC[9:12])], 'x:')#, label='C=1nm')
    axs[1,2].plot(labels[12::], [r*c[0] for r, c in zip(rmsC[12::],compositeC[12::])], 'x:')#, label='C=1nm')
    axs[1,2].set_title("RMS x Composite")
    # axs[1,2].set_ylabel("NILS")
    if sepBy == 'RMS':
        axs[0,0].set_xlabel('$C_y [nm]$')
        axs[0,1].set_xlabel('$C_y [nm]$')
        axs[0,2].set_xlabel('$C_y [nm]$')
    else:
        axs[0,0].set_xlabel('\u03C3 [nm]')
        axs[0,1].set_xlabel('\u03C3 [nm]')
        axs[0,2].set_xlabel('\u03C3 [nm]')
    fig.tight_layout()
    fig.subplots_adjust(bottom=0.2)   ##  Need to play with this number.
    if sepBy == 'RMS':
        fig.legend(labels=['\u03C3 [nm]: ' + str(l) for l in labelsH[0:5]], loc="lower center", ncol=5)
    else:
        fig.legend(labels=['$C_y$ [nm]: ' + str(l) for l in labelsH[0:5]], loc="lower center", ncol=5)
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
else:
    fig, axs = plt.subplots(2,3)
    
    axs[0,0].plot(labels, [n[0]*aI*tI for n, aI, tI in zip(nilsC,avPeaks,sumPeaks)])
    axs[0,0].set_title("NILS*avI*totI")
    axs[0,1].plot(labels, [r*aI*tI for r, aI, tI in zip(rmsC, avPeaks, sumPeaks)])
    axs[0,1].set_title("RMS*avI*totI")
    axs[0,2].plot(labels, [c[0]*n[0]*aI for c,n,aI in zip(compositeC,nilsC,avPeaks)])
    axs[0,2].set_title("Composite*NILS*avI")
    axs[1,0].plot(labels, [c[0]*n[0]*r for c,n,r in zip(compositeC,nilsC,rmsC)])
    axs[1,0].set_title("Composite*NILS*RMS")
    axs[1,1].plot(labels, [rI*n[0]*avI for rI,n,avI in zip(rmsPeaks,nilsC,avPeaks)])
    axs[1,1].set_title("rmsI*NILS*avI")
    axs[1,2].plot(labels, [r*c[0] for r,c in zip(rmsC,compositeC)])
    axs[1,2].set_title("RMS*Composite")
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
    
