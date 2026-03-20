#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 16:32:37 2023

@author: -
"""

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from skimage import io,  exposure, img_as_uint, img_as_float
from tqdm import tqdm
import os
import matplotlib.patches as patches
from mpl_toolkits.axes_grid1.axes_divider import make_axes_locatable

from usefulWavefield import counts2photonsPsPcm2, intensity2power, findBeamCenter
from FWarbValue import getFWatValue

from image_processing import sumImages,cropImage,IoverGrating
from usefulGrating import lateralShift 
from usefulWavefield import EtoWL, round_sig
from fractions import Fraction
    
# Location of the images
imageFolder = '/user/home/data/offset_testing_91.84eV_2/'
darkFolder = '/user/home/data/darkfield_50ms_exposure/'
savePath_dark = darkFolder + 'averaged/'
savePath_images = '/user/home/data/DE_processed/offset_testing/'

energy_range = [91.84, 100, 110, 120, 130, 140, 150, 160, 170, 180, 185.05, 190, 200, 210, 220, 230, 240, 250, 260, 270, 3*91.84, 280, 290]
offset = [-1.6, -1.4, -1.0, -0.6, -0.2, 0.2, 0.6, 1.0] 

tl=0 
tr=1
ml=2
mr=3
bl=4
br=5

process = False
verbose = True
show = 120
gratings = [120] #[88,120,160,200]
positions = [ml] #[tl,ml,mr,bl]
save = True

if process:
    # print("Averaging Darkfield Images...")
    # sumImages(darkFolder,name='a_1_',sumNum=5000,imgType=".tif",average=True,
    #           darkfield=None,savePath=savePath_dark,show=True,verbose=True)
    print("Summing/Averaging Images...")
    ims,iTot,er = sumImages(imageFolder,name='a_1_',sumNum=2000,imgType=".tif",average=True,
                            darkfield=savePath_dark + str(4999) + '.tif',
                            savePath=savePath_images,hist=True,show=True,verbose=True)
    
    pEr = [e/i for e,i in zip(er,iTot)] # percentage error for summed intensities
    
    plt.errorbar(offset,iTot,yerr=er)
    plt.xlabel('Undulator Offset [%]')
    plt.ylabel('Total Intensity [counts]')
    plt.show()
    

inums = [2000,4000,6000,8000,10000,12000,14000,15999]
#[91999] #
inames = [savePath_images + str(i) + '.tif' for i in inums]

# print([savePath_images + str(i) + '.tif' for i in inames])
# ims = [io.imread(i for i in inames)]
# image = io.imread(path + str(name) + str(i) + str(imgType))

# defining coordinates for grating centers (same for every image) (y,x)
p88 = [(117,87),(118,117),(141,87),(141,116),(164,86),(164,115)]   # tl=0,tr=1,ml=2,mr=3,bl=4,br=5
p120 =  [(129,57),(129,79),(152,57),(152,79),(175,57),(175,78)]    # tl,tr,ml,mr,bl,br
p160 =  [(140,35),(140,51),(163,34),(163,50),(187,34),(187,50)]    # tl,tr,ml,mr,bl,br
p200 =  [(151,17),(151,30),(175,17),(174,30),(198,16),(199,29)]    # tl,tr,ml,mr,bl,br

T = (166,68)

# defining grating sizes in pixels (y,x)
s88 = (14,14) #
s120 = (14,14) # (12,10)
s160 = (14,14) # (12,8)
s200 = (14,14) # (12,8)
sT = (14,14)

try:
    x0_88,y0_88 = p88[positions[0]][1] - (s88[1]//2),  p88[positions[0]][0] - (s88[0]//2)
    x0_120,y0_120 = p120[positions[1]][1] - (s120[1]//2),  p120[positions[1]][0] - (s120[0]//2)
    x0_160,y0_160 = p160[positions[2]][1] - (s160[1]//2),  p160[positions[2]][0] - (s160[0]//2)
    x0_200,y0_200 = p200[positions[3]][1] - (s200[1]//2),  p200[positions[3]][0] - (s200[0]//2)
except:
    x0_88,y0_88 = p88[positions[0]][1] - (s88[1]//2),  p88[positions[0]][0] - (s88[0]//2)
    x0_120,y0_120 = p120[positions[0]][1] - (s120[1]//2),  p120[positions[0]][0] - (s120[0]//2)
    x0_160,y0_160 = p160[positions[0]][1] - (s160[1]//2),  p160[positions[0]][0] - (s160[0]//2)
    x0_200,y0_200 = p200[positions[0]][1] - (s200[1]//2),  p200[positions[0]][0] - (s200[0]//2)
    pass

x0_T,y0_T = T[1] - (sT[1]//2), T[0] - (sT[0]//2)

# parameters that work for 1st harmonic
z = 0.3366                   # propagation distance from grating in m
theta = 1.552                # correction factor for angle of grating
phi = 0.0000001

N = [1,2,3,4,5]
M = [1,2,3,4,5]

EffT88 = []
EffT120 = []
EffT160 = []
EffT200 = []

Eff88 = [ [] for _ in range(np.max(N)*np.max(M))]
Er88 = [ [] for _ in range(np.max(N)*np.max(M))]
Eff120 = [ [] for _ in range(np.max(N)*np.max(M))]
Er120 = [ [] for _ in range(np.max(N)*np.max(M))]
Eff160 = [ [] for _ in range(np.max(N)*np.max(M))]
Er160 = [ [] for _ in range(np.max(N)*np.max(M))]
Eff200 = [ [] for _ in range(np.max(N)*np.max(M))]
Er200 = [ [] for _ in range(np.max(N)*np.max(M))]

NM = [ [] for _ in range(np.max(N)*np.max(M))]

for e,i in enumerate(inames):
    im = io.imread(i)
    rx,ry = np.shape(im)[1],np.shape(im)[0]
    wl = EtoWL(91.84)
    print(" ")
    # print(f"Energy:      {energy_range[e]}")
    # print(f"Wavelength = {wl}")
    print(f"Undulator Offset: {offset[e]} %")
    
    
    # Defining area of 0 order beam
    # 88 nm pitch grating
    I0_88 = im[y0_88:y0_88 + s88[0],x0_88:x0_88 + s88[1]]
    rect88_0 = patches.Rectangle((x0_88,y0_88),s88[1],s88[0], edgecolor='r', facecolor="none")
    I0sum88 = np.sum(I0_88)
    er0_88 = np.sqrt(I0sum88)/I0sum88  #1/(np.sqrt(I0sum88)*I0sum88)  
    
    # 120 nm pitch grating
    I0_120 = im[y0_120:y0_120 + s120[0],x0_120:x0_120 + s120[1]]
    rect120_0 = patches.Rectangle((x0_120,y0_120),s120[1],s120[0], edgecolor='b', facecolor="none")
    I0sum120 = np.sum(I0_120)
    er0_120 = np.sqrt(I0sum120)/I0sum120  #1/(np.sqrt(I0sum88)*I0sum88)
    
    # 160 nm pitch grating
    I0_160 = im[y0_160:y0_160 + s160[0],x0_160:x0_160 + s160[1]]
    rect160_0 = patches.Rectangle((x0_160,y0_160),s160[1],s160[0], edgecolor='g', facecolor="none")
    I0sum160 = np.sum(I0_160)
    er0_160 = np.sqrt(I0sum160)/I0sum160  #1/(np.sqrt(I0sum88)*I0sum88)
    
    # 200 nm pitch grating
    I0_200 = im[y0_200:y0_200 + s200[0],x0_200:x0_200 + s200[1]]
    rect200_0 = patches.Rectangle((x0_200,y0_200),s200[1],s200[0], edgecolor='y', facecolor="none")
    I0sum200 = np.sum(I0_200)
    er0_200 = np.sqrt(I0sum200)/I0sum200  #1/(np.sqrt(I0sum88)*I0sum88)
    
    # transmission through photon block
    I0_T = im[y0_T:y0_T + sT[0],x0_T:x0_T + sT[1]]
    rectT_0 = patches.Rectangle((x0_T,y0_T),sT[1],sT[0], edgecolor='y', facecolor="none")
    I0sumT = np.sum(I0_T)
    er0_T = np.sqrt(I0sumT)/I0sumT  #1/(np.sqrt(I0sum88)*I0sum88)
    
    EffT88.append(I0sumT/I0sum88)
    EffT120.append(I0sumT/I0sum120)
    EffT160.append(I0sumT/I0sum160)
    EffT200.append(I0sumT/I0sum200)
    
    numXticks = 5
    numYticks = 5
    dx = 11.0e-6
    dy = 11.0e-6
    ny, nx = np.shape(im)[0], np.shape(im)[1]
    sF = 1e3
    
    if show:
        # Setting up plot
        fig, ax = plt.subplot_mosaic("ABCDE;FGHIJ;KLMNO;PQRST;UVWXY;ZZZZZ;ZZZZZ;ZZZZZ",figsize=(8,8))#STUVWX;YZabcd;eeeeee;eeeeee;eeeeee")
        axl = ["A","B","C","D","E",
               "F","G","H","I","J",
               "K","L","M","N","O",
               "P","Q","R","S","T",
               "U","V","W","X","Y"
               ]
               # "S","T","Z","V","W","X",
               # "Y","Z","a","b","c","d"]
        # i1 = ax["A"].imshow(I0_88)
        i4 = ax["Z"].imshow(im,vmin=0,vmax=np.max(im[:,250::]),aspect=2)
        # ax["Z"].set_xlim(250,rx)
        # ax["Z"].set_ylim(250,100)
        ax["Z"].set_title(f"Offset = {offset[e]} %")        
        ax["Z"].set_yticks([int((ny-1.0)*(b/(numYticks-1.0))) for b in range(0,numYticks)])
        ax["Z"].set_yticklabels([round_sig(ny*dy*(a/(numYticks-1.0))*sF) for a in range(-int((numYticks-1.0)/2.0),int((numYticks/2.0 + 1.0)))],fontsize=10)
        ax["Z"].set_xticks([int((nx-1.0)*(b/(numXticks-1.0))) for b in range(0,numXticks)])
        ax["Z"].set_xticklabels([round_sig(nx*dx*(a/(numXticks-1.0))*sF) for a in  range(-int((numXticks-1.0)/2.0),int((numXticks/2.0 + 1.0)))],fontsize=10)
        ax["Z"].set_xlabel("x [mm]")
        ax["Z"].set_ylabel("y [mm]")
        ax["Z"].add_patch(rect88_0)
        ax["Z"].add_patch(rect120_0)
        ax["Z"].add_patch(rect160_0)
        ax["Z"].add_patch(rect200_0)
    
    # Finding positions of diffracted orders
    nm = 0
    for n in N:
        for m in M:
            if e ==0:
                NM[nm].append([n,m])
            # 88 nm pitch grating
            x_88_m = lateralShift(wl/n,p=88e-9,m=m,z=z,theta_i=phi)
            x_88 = x_88_m/11.0e-6
            y_88 = x_88/np.tan(theta)
            
            # 120 nm pitch grating
            x_120_m = lateralShift(wl/n,p=120e-9,m=m,z=z,theta_i=phi)
            x_120 = x_120_m/11.0e-6
            y_120 = x_120/np.tan(theta)
            
            # 160 nm pitch grating
            x_160_m = lateralShift(wl/n,p=160e-9,m=m,z=z,theta_i=phi)
            x_160 = x_160_m/11.0e-6
            y_160 = x_160/np.tan(theta)
            
            # 200 nm pitch grating
            x_200_m = lateralShift(wl/n,p=200e-9,m=m,z=z,theta_i=phi)
            x_200 = x_200_m/11.0e-6
            y_200 = x_200/np.tan(theta)
            
            if int(x_88+x0_88) <= rx and int(x_88+x0_88) >= 235:
                good88 = True
            else:
                good88 = False
                
            if int(x_120+x0_120) <= rx and int(x_120+x0_120) >= 235:
                good120 = True
            else:
                good120 = False
                
            if int(x_160+x0_160) <= rx and int(x_160+x0_160) >= 235:
                good160 = True
            else:
                good160 = False
                
            if int(x_200+x0_200) <= rx and int(x_200+x0_200) >= 235:
                good200 = True
            else:
                good200 = False
            
            # Defining area of diffracted beam
            I_88 = im[int(y0_88 + y_88):int(y0_88 + y_88 + s88[0]),int(x0_88 + x_88):int(x0_88 + x_88 + s88[1])]
            I_120 = im[int(y0_120 + y_120):int(y0_120 + y_120 + s120[0]),int(x0_120 + x_120):int(x0_120 + x_120 + s120[1])]
            I_160 = im[int(y0_160 + y_160):int(y0_160 + y_160 + s160[0]),int(x0_160 + x_160):int(x0_160 + x_160 + s160[1])]
            I_200 = im[int(y0_200 + y_200):int(y0_200 + y_200 + s200[0]),int(x0_200 + x_200):int(x0_200 + x_200 + s200[1])]
            # Defining area for background intensity subtraction
            Ib_88 = im[325:int(325+s88[0]),int(x0_88 + x_88):int(x0_88 + x_88 + s88[1])]
            Ib_120 = im[325:int(325+s120[0]),int(x0_120 + x_120):int(x0_120 + x_120 + s120[1])]
            Ib_160 = im[325:int(325+s160[0]),int(x0_160 + x_160):int(x0_160 + x_160 + s160[1])]
            Ib_200 = im[325:int(325+s200[0]),int(x0_200 + x_200):int(x0_200 + x_200 + s200[1])]
            
            rect_88 = patches.Rectangle((int(x0_88+x_88),int(y0_88+y_88)),s88[1],s88[0], edgecolor='r', facecolor="none")
            rect_120 = patches.Rectangle((int(x0_120+x_120),int(y0_120+y_120)),s120[1],s120[0], edgecolor='b', facecolor="none")
            rect_160 = patches.Rectangle((int(x0_160+x_160),int(y0_160+y_160)),s160[1],s160[0], edgecolor='g', facecolor="none")
            rect_200 = patches.Rectangle((int(x0_200+x_200),int(y0_200+y_200)),s200[1],s200[0], edgecolor='y', facecolor="none")
            # print(" ")
            # print(f"\"{axl[nm]}\"")
            # print(nm)
            # print(" ")
            
            # divider = make_axes_locatable(ax[axl[nm]])
            # cax = divider.append_axes("right",size="3%",pad=0.05)
            # plt.colorbar(imI,cax=cax)
            if show:
                if 88 in gratings:
                    if good88 and n == Fraction(n,m).numerator:
                        ax["Z"].add_patch(rect_88)
                        ax["Z"].text(int(x_88+x0_88),int(y0_88+y_88),f'{(n,m)}',color='r',fontsize=8)
                if 120 in gratings:
                    if good120 and n == Fraction(n,m).numerator:
                        ax["Z"].add_patch(rect_120)
                        ax["Z"].text(int(x_120+x0_120),int(y0_120+y_120),f'{(n,m)}',color='b',fontsize=8)
                if 160 in gratings:
                    if good160 and n == Fraction(n,m).numerator:
                        ax["Z"].add_patch(rect_160)
                        ax["Z"].text(int(x_160+x0_160),int(y0_160+y_160),f'{(n,m)}',color='g',fontsize=8)
                if 200 in gratings:
                    if  good200 and n == Fraction(n,m).numerator:
                        ax["Z"].add_patch(rect_200)
                        ax["Z"].text(int(x_200+x0_200),int(y0_200+y_200),f'{(n,m)}',color='y',fontsize=8)
                    
                if show == 88:
                    if good88 == False or n != Fraction(n,m).numerator:
                        fig.delaxes(ax[axl[nm]])
                        ax[axl[nm]].set_axis_off()
                        ax[axl[nm]].set_visible(False)
                    else:
                        imI = ax[axl[nm]].imshow(I_88)
                        ax[axl[nm]].set_title(f"$I_{n,m}$",fontsize=8)
                        ax[axl[nm]].get_xaxis().set_visible(False)
                        ax[axl[nm]].get_yaxis().set_visible(False)
                elif show == 120:
                    if good120 == False or n != Fraction(n,m).numerator:
                        fig.delaxes(ax[axl[nm]])
                        ax[axl[nm]].set_axis_off()
                        ax[axl[nm]].set_visible(False)
                    else:
                        imI = ax[axl[nm]].imshow(I_120)
                        ax[axl[nm]].set_title(f"$I_{n,m}$",fontsize=8)
                        ax[axl[nm]].get_xaxis().set_visible(False)
                        ax[axl[nm]].get_yaxis().set_visible(False)
                elif show == 160:
                    if good160 == False or n != Fraction(n,m).numerator:
                        fig.delaxes(ax[axl[nm]])
                        ax[axl[nm]].set_axis_off()
                        ax[axl[nm]].set_visible(False)
                    else:
                        imI = ax[axl[nm]].imshow(I_160)
                        ax[axl[nm]].set_title(f"$I_{n,m}$",fontsize=8)
                        ax[axl[nm]].get_xaxis().set_visible(False)
                        ax[axl[nm]].get_yaxis().set_visible(False)
                elif show == 200:
                    if good200 == False or n != Fraction(n,m).numerator:
                        fig.delaxes(ax[axl[nm]])
                        ax[axl[nm]].set_axis_off()
                        ax[axl[nm]].set_visible(False)
                    else:
                        imI = ax[axl[nm]].imshow(I_200)
                        ax[axl[nm]].set_title(f"I_{n,m}",fontsize=8)
                        ax[axl[nm]].get_xaxis().set_visible(False)
                        ax[axl[nm]].get_yaxis().set_visible(False)
                
            
            Isum88 = (np.sum(I_88) - np.sum(Ib_88))
            Isum120 = (np.sum(I_120) - np.sum(Ib_120))
            Isum160 = (np.sum(I_160) - np.sum(Ib_160))
            Isum200 = (np.sum(I_200) - np.sum(Ib_200))
            
            E_88 = Isum88/I0sum88
            erI_88 = np.sqrt(Isum88)/Isum88
            erE_88 = np.sqrt((er0_88**2) + (erI_88**2)) * E_88
            E_120 = Isum120/I0sum120
            erI_120 = np.sqrt(Isum120)/Isum120
            erE_120 = np.sqrt((er0_120**2) + (erI_120**2)) * E_120
            E_160 = Isum160/I0sum160
            erI_160 = np.sqrt(Isum160)/Isum160
            erE_160 = np.sqrt((er0_160**2) + (erI_160**2)) * E_160
            E_200 = Isum200/I0sum200
            erI_200 = np.sqrt(Isum200)/Isum200
            erE_200 = np.sqrt((er0_200**2) + (erI_200**2)) * E_200
            
            if E_88 == 0:
                Eff88[nm].append(np.nan)
                Er88[nm].append(np.nan)
            elif E_88 >= 1:
                Eff88[nm].append(np.nan)
                Er88[nm].append(np.nan)
            elif good88:
                Eff88[nm].append(E_88)
                Er88[nm].append(erE_88)
            else:
                Eff88[nm].append(np.nan)
                Er88[nm].append(np.nan)
                
            if E_120 == 0:
                Eff120[nm].append(np.nan)
                Er120[nm].append(np.nan)
            elif E_120 >= 1:
                Eff120[nm].append(np.nan)
                Er120[nm].append(np.nan)
            elif good120:
                Eff120[nm].append(E_120)
                Er120[nm].append(erE_120)
            else:
                Eff120[nm].append(np.nan)
                Er120[nm].append(np.nan)
                
                
            if E_160 == 0:
                Eff160[nm].append(np.nan)
                Er160[nm].append(np.nan)
            elif E_160 >= 1:
                Eff160[nm].append(np.nan)
                Er160[nm].append(np.nan)
            elif good160:
                Eff160[nm].append(E_160)
                Er160[nm].append(erE_160)
            else:
                Eff160[nm].append(np.nan)
                Er160[nm].append(np.nan)
                
                
            if E_200 == 0:
                Eff200[nm].append(np.nan)
                Er200[nm].append(np.nan)
            elif E_200 >= 1:
                Eff200[nm].append(np.nan)
                Er200[nm].append(np.nan)
            elif good200:
                Eff200[nm].append(E_200)
                Er200[nm].append(erE_200)
            else:
                Eff200[nm].append(np.nan)
                Er200[nm].append(np.nan)
                
                
            # NM[nm].append((n,m))
            # print(nm)
            # print(n,m)
            nm+=1
    if show:
        fig.tight_layout()
        plt.show()
        
    
# Plotting efficiency for 88 nm pitch grating
for i88,e88,nm in zip(Eff88,Er88,NM):
    if np.isnan(i88).all():
        pass
    elif nm[0][0] != Fraction(nm[0][0],nm[0][1]).numerator:
        pass
    else:
        plt.errorbar(offset,[_i*100 for _i in i88],yerr=[_e*100 for _e in e88],fmt='.:', 
                     label="$\eta^{88}$" + str((nm[0][0],nm[0][1])))

plt.xlabel("Photon Energy [eV]")
plt.ylabel("$\eta_{n,m}$[%]")
plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.3),
           ncol=4, fancybox=True, shadow=True)
if save:
    plt.savefig('/user/home/data/DE_processed/plots/p88_' + str(positions[0]) + '.png')
plt.show()

# Plotting efficiency for 120 nm pitch grating
for i120,e120,nm in zip(Eff120,Er120,NM):
    if np.isnan(i120).all():
        pass
    elif nm[0][0] != Fraction(nm[0][0],nm[0][1]).numerator:
        pass
    else:
        plt.errorbar(offset,[_i*100 for _i in i120],yerr=[_e*100 for _e in e120],fmt='.:', 
                     label="$\eta^{120}$" + str((nm[0][0],nm[0][1])))

plt.xlabel("Photon Energy [eV]")
plt.ylabel("$\eta_{n,m}$[%]")
plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.3),
           ncol=4, fancybox=True, shadow=True)
if save:
    plt.savefig('/user/home/data/DE_processed/plots/p120_' + str(positions[0]) + '.png')
plt.show()


# Plotting efficiency for 160 nm pitch grating
for i160,e160,nm in zip(Eff160,Er160,NM):
    if np.isnan(i160).all():
        pass
    elif nm[0][0] != Fraction(nm[0][0],nm[0][1]).numerator:
        pass
    else:
        plt.errorbar(offset,[_i*100 for _i in i160],yerr=[_e*100 for _e in e160],fmt='.:', 
                     label="$\eta^{160}$" + str((nm[0][0],nm[0][1])))

plt.xlabel("Photon Energy [eV]")
plt.ylabel("$\eta_{n,m}$[%]")
plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.3),
           ncol=4, fancybox=True, shadow=True)
if save:
    plt.savefig('/user/home/data/DE_processed/plots/p160_' + str(positions[0]) + '.png')
plt.show()


# Plotting efficiency for 120 nm pitch grating
for i200,e200,nm in zip(Eff200,Er200,NM):
    if np.isnan(i200).all():
        pass
    elif nm[0][0] != Fraction(nm[0][0],nm[0][1]).numerator:
        pass
    else:
        plt.errorbar(offset,[_i*100 for _i in i200],yerr=[_e*100 for _e in e200],fmt='.:', 
                     label="$\eta^{200}$" + str((nm[0][0],nm[0][1])))

plt.xlabel("Photon Energy [eV]")
plt.ylabel("$\eta_{n,m}$[%]")
plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.3),
           ncol=4, fancybox=True, shadow=True)
if save:
    plt.savefig('/user/home/data/DE_processed/plots/p200_' + str(positions[0]) + '.png')
plt.show()


plt.plot(offset,EffT88,'.:',label='88 nm')
plt.plot(offset,EffT120,'.:',label='120 nm')
plt.plot(offset,EffT160,'.:',label='160 nm')
plt.plot(offset,EffT200,'.:',label='200 nm')
plt.xlabel('Undulator Offset [%]')
plt.ylabel('$I_0 / I_T $')
plt.legend()
plt.show()