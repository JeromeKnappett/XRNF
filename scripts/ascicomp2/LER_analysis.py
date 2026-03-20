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

from sklearn.metrics import auc

plt.rcParams["figure.figsize"] = (10,8)

dirPath = '/user/home/opt_old/xl/xl/experiments/BEUVcoherenceLER1/data/d27um/'
ids = ['05','10','15','20','25','30','35','40']
files = [dirPath + 'rms' + i + '/rms' + i + '.pkl' for i in ids]
# '/user/home/opt_old/xl/xl/experiments/BEUVcoherenceLER1/masks_D50/20000020.00000_4.00000_10.00000_mask.tif'
# '/user/home/opt/xl/xl/experiments/maskLER1/masks/vert_block.tif'
# '/user/home/opt/xl/xl/experiments/BEUVcoherenceLER1/masks_D50/20000020.00000_0.50000_10.00000_mask.tif'
#'/user/home/opt/xl/xl/experiments/BEUVcoherence/masks/200p50rBlock.tif'
#'/user/home/opt/xl/xl/experiments/BEUVcoherenceLER1/masks_D50/vert_block.tif'
#"/user/home/opt/xl/xl/experiments/maskLER1/masks/20000020.00000_1.00000_10.00000_mask.tif"

fromPickle = True


Nx = 2000
Ny = 20
G = 10.0e-6
pitch = 50.0e-9
shiftX,shiftY = -4,7
extraX,extraY = 14,10
line_orientation = 'vert'

aeLER = []
aeLERe = []

LERpsd = []
LERrms = []

for f in files:
    
    if fromPickle:
        pick = pickle.load(open(f, 'rb'))
        tiff = pick[0]
        res = (pick[1],pick[2])
        print(res)
    # maskImage = tifffile.imread(f)
    print(np.shape(tiff))

    # plt.imshow(tiff,aspect='auto')
    # plt.colorbar()
    # plt.show()
    
    midX,midY = np.shape(tiff)[1]//2, np.shape(tiff)[0]//2
    print(midX,midY)
    # print(np.shape(tiff))
    hppix = pitch/(2*res[0])
    print(hppix)
    numlines =  int(Nx//hppix - 2) # 5 # int(Nx//hppix - 2)
    
    aerialimage = tiff[int(midY + shiftY - (Ny/2)):int(midY + shiftY + (Ny/2)), int(midX + shiftX - (Nx/2)):int(midX + shiftX + (Nx/2))]
    
    plt.imshow(aerialimage,aspect='auto')
    plt.title('aerial image')
    plt.colorbar()
    plt.show()
    
    
    f = []
    p = []
    LER = []
    for n in range(0,numlines):
        
        print('\n Analysing line ', n+1, ' of ', numlines)
        
        if line_orientation == 'hor':
            move = hppix//2 + extraY
            lineImage = aerialimage[int(shiftY + n*hppix):int(shiftY + hppix//2 + extraY + n*hppix),:]
        elif line_orientation == 'vert':            
            move = hppix//2 + extraX
            lineImage = aerialimage[:,round(n*hppix):round(n*hppix + move)]
            lineImage = np.rot90(lineImage,k=-1)#,axes=(0,1))
            if n==0:
                res = res[1],res[0]
            else:
                pass
        # if lineImage[0,0] > lineImage[-1:0]:
            # lineImage = abs(255 - lineImage)
        # if (n % 2) == 0:        
        #     lineImage = gratingImage[int(shiftY + n*hp):int(shiftY + hp//2 + n*hp),:]
        #     lineImage = abs(255 - lineImage)
        # else:
        #     lineImage = gratingImage[int(shiftY + n*hp):int(shiftY + hp//2 + n*hp),:]
        
        # lineImage = gratingImage[int(1980 - hp//2):int(1980 + hp//2),:]
    
        # plt.imshow(lineImage,aspect='auto')
        # plt.title('line image')#' #', str(n+1))
        # plt.colorbar()
        # plt.show()
    
        Lbox = Ny*res[1]
        fmin = 1 / (2*np.pi*Lbox)
        smax =  1 / fmin
    
        # print("minimum frequency sampled: ", fmin/1e6, ' /um')
        # print("maximum feature size sampled: ", smax*1e6, ' um')
    
        _LER = edge_roughness()
        (Xcln, Ycln, freq, FourierPow) = _LER.LER_analysis(lineImage, res, 10, maxI = np.max(aerialimage),show=False) #image, image width (m), threshold for outliers
        
        L = 3*np.std(Ycln)
        
        LER.append(L)
        f.append(freq)
        p.append(FourierPow)
    

    print(np.shape(f))
    f=np.mean(f,axis=0)
    p=np.mean(p,axis=0)
    LER=np.mean(LER,axis=0)
    print(np.shape(f))
    
    # plt.plot(Xcln, Ycln, '-')
    # plt.plot(Xcln, Ycln, 'r.')
    # plt.show()
    
    # print(np.shape(freq))
    
    # plt.plot(freq[2:100], FourierPow[2:100],'-')
    plt.plot([_f/1.0e9 for _f in f[1:100]], p[1:100],'.')
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
    plt.show() 
    
    #cv2.imshow('Origional Image',image)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    
    lc = 10.0e-9
    
    per = 1 - ((2/np.pi) * np.arctan(lc/(Ny*res[0])))
    
    ler = np.sqrt(integrate.simpson(p, f))
    print('LER from integration of PSD: ', 3*ler)
    print('LER from standard deviation: ', LER)
    print('LER error (PSD) [nm]: ', (1-per)*3*ler*1e9)
    print('LER error (different methods) [nm]: ', abs(3*ler - LER)*1e9)
    
    print(((LER + (3*ler))/2)*1e9)
    
    aeLER.append(((LER + (3*ler))/2)*1e9)
    aeLERe.append(np.max([(1-per)*3*ler*1e9, abs(3*ler - LER)*1e9]))
    
    LERpsd.append(3*ler*1e9)
    LERrms.append(LER*1e9)
    # print('computed AUC using sklearn.metrics.auc: {}'.format(3*np.sqrt(auc(f,p))))
        
            # plt.plot(freq,FourierPow)
            # plt.show()    


maskLER = [3.0,6.6,10.4,14.3,18.2,22.0,25.7,29.0]

# plt.errorbar(maskLER,aeLER,yerr=aeLERe,fmt='o',markerfacecolor='none')
plt.plot(maskLER,LERpsd,'o',markerfacecolor='none',label='PSD')
plt.plot(maskLER,LERrms,'o',markerfacecolor='none',label='STD')
plt.xlabel('Mask LER [nm]')
plt.ylabel('Aerial Image LER [nm]')
plt.legend()
plt.show()

# X = 8000
# Y = 7000 
# res = 1.25e-9
# midX, midY = np.shape(maskImage)[1]/2, 5235 #5245#(3*np.shape(maskImage)[0])/17
# pitch = 100.0e-9 / res #pixels
# hp = pitch/2

# numlines = int(Y//hp-2)# 125
# shiftY = 2
# extraY = 20

# print(midX, midY)

# gratingImage = maskImage[int(midY - (Y/2)):int(midY + (Y/2)), int(midX - (X/2)):int(midX + (X/2))]
# #maskImage[1000:5000,6500:10500]

# plt.imshow(gratingImage)
# plt.colorbar()
# plt.show()

# save2pick = False

# if save2pick:
#     with open(maskFile[0:int(len(maskFile)-4)] + 'CLOSE.pkl', "wb") as f:
#                 pickle.dump(gratingImage, f, protocol=2)


# #offset = hp

# #lineImage = gratingImage[int(2000 - hp):int(2000),:]


# f = []
# p = []
# LER = []
# for n in range(0,numlines):
    
#     print('\n Analysing line ', n+1, ' of ', numlines)
    
#     lineImage = gratingImage[int(shiftY + n*hp):int(shiftY + hp//2 + extraY + n*hp),:]
#     if lineImage[0,0] != 0:
#         lineImage = abs(255 - lineImage)
#     # if (n % 2) == 0:        
#     #     lineImage = gratingImage[int(shiftY + n*hp):int(shiftY + hp//2 + n*hp),:]
#     #     lineImage = abs(255 - lineImage)
#     # else:
#     #     lineImage = gratingImage[int(shiftY + n*hp):int(shiftY + hp//2 + n*hp),:]
    
#     # lineImage = gratingImage[int(1980 - hp//2):int(1980 + hp//2),:]

#     # plt.imshow(lineImage,aspect='auto')
#     # plt.show()

#     Lbox = X*res
#     fmin = 1 / (2*np.pi*Lbox)
#     smax =  1 / fmin

#     # print("minimum frequency sampled: ", fmin/1e6, ' /um')
#     # print("maximum feature size sampled: ", smax*1e6, ' um')

#     _LER = edge_roughness()
#     (Xcln, Ycln, freq, FourierPow) = _LER.LER_analysis(lineImage, X * 1.25e-9, 10,show=False) #image, image width (m), threshold for outliers
    
#     L = 3*np.std(Ycln)
    
#     LER.append(L)
#     f.append(freq)
#     p.append(FourierPow)

#     # plt.plot(freq,FourierPow)
#     # plt.show()    


# print(np.shape(f))
# f=np.mean(f,axis=0)
# p=np.mean(p,axis=0)
# LER=np.mean(LER,axis=0)
# print(np.shape(f))

# # plt.plot(Xcln, Ycln, '-')
# # plt.plot(Xcln, Ycln, 'r.')
# # plt.show()

# # print(np.shape(freq))

# # plt.plot(freq[2:100], FourierPow[2:100],'-')
# plt.plot([_f/1.0e9 for _f in f[1:100]], p[1:100],'.')
# # plt.plot([1/f for f in freq[0:100]], FourierPow[0:100],'-')
# ax = plt.gca()
# ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%0.0e'))
# plt.yscale('log')
# plt.xscale('log')
# # plt.xaxis.set_minor_formatter(ticker.ScalarFormatter())
# # plt.ticklabel_format(style='plain', axis='x')
# plt.xlabel('Spatial frequency (nm$^{-1}$)')
# # plt.xlabel('Feature size (nm)')
# plt.ylabel('Fourier power (au)')
# # plt.ylim([np.min(p),(np.max(p) + np.std(p))])
# plt.title('Fourier power spectrum')
# plt.show() 

# #cv2.imshow('Origional Image',image)
# #cv2.waitKey(0)
# #cv2.destroyAllWindows()

# lc = 10.0e-9

# per = 1 - ((2/np.pi) * np.arctan(lc/(X*1.25e-9)))

# ler = np.sqrt(integrate.simpson(p, f))
# print('LER from integration of PSD: ', 3*ler)
# print('LER from standard deviation: ', LER)
# print('LER error (PSD) [nm]: ', (1-per)*3*ler*1e9)
# print('LER error (different methods) [nm]: ', abs(3*ler - LER)*1e9)
# print(((LER + (3*ler))/2)*1e9)
# # print('computed AUC using sklearn.metrics.auc: {}'.format(3*np.sqrt(auc(f,p))))



# # [3.0,6.6,10.4,14.3,18.2,22.0,25.7,29.0]
# # 20000020.00000_0.50000_10.00000_mask = 3.00 +/- 0.005 nm LER
# # 20000020.00000_1.00000_10.00000_mask = 6.60 +/- 0.004 nm LER
# # 20000020.00000_1.50000_10.00000_mask = 10.4 +/- 0.007 nm LER
# # 20000020.00000_2.00000_10.00000_mask = 14.3 +/- 0.009 nm LER
# # 20000020.00000_2.50000_10.00000_mask = 18.2 +/- 0.01 nm LER
# # 20000020.00000_3.00000_10.00000_mask = 22.0 +/- 0.01 nm LER
# # 20000020.00000_3.50000_10.00000_mask = 25.7 +/- 0.02 nm LER
# # 20000020.00000_4.00000_10.00000_mask = 29.0 +/- 0.1 nm LER
