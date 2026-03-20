#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 11:12:40 2023

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
from tqdm import tqdm

from sklearn.metrics import auc

from collections import defaultdict

plt.rcParams["figure.figsize"] = (10,8)

file = '/user/home/opt_old/xl/xl/experiments/masks3/50.0rBlock.tif'

image = tifffile.imread(file)
dx = 10.0e-9
dy = 10.0e-9
print(np.shape(image))


plt.imshow(image,aspect='auto')
plt.colorbar()
plt.show()

imagefft = abs(np.fft.fft2(image))**2

freqx = np.fft.fftfreq(np.shape(image)[1],dx)
freqy = np.fft.fftfreq(np.shape(image)[0],dy)

F = np.zeros_like(imagefft)
for i,y in enumerate(imagefft):
    for j,x in enumerate(y):
        F[i,j] = np.sqrt(freqx[j]**2 + freqy[i]**2)

plt.imshow(F)
plt.colorbar()
plt.show()

plt.imshow(imagefft)
plt.colorbar()
plt.show()


data = [(f,A) for f,A in zip(F.ravel(),imagefft.ravel())]

plt.plot(data[0],data[1],'.')
plt.xscale('log')
plt.yscale('log')
plt.show()

dic = defaultdict(int)
for j, f in tqdm(enumerate(F.ravel())):
    dic[f] += imagefft.ravel()[j]

freq_counts = np.array([dic[f] for f in F.ravel()])

# print(np.shape(b))

plt.plot(freq_counts)
plt.show()


# sx = [1/f for f in freqx]
# sy = [1/f for f in freqy]

# sx = sx[0:len(sx)//2]
# sy = sy[0:len(sy)//2]
# freqx = freqx[0:len(freqx)//2]
# freqy = freqy[0:len(freqy)//2]

# print(np.min(imagefft))
# print(np.max(imagefft))
        
# yf = np.sum(imagefft,axis=0)
# xf = np.sum(imagefft,axis=1)

# xf = xf[0:len(xf)//2]
# yf = yf[0:len(yf)//2]


# print(np.min(xf))
# print(np.max(xf))
# print(np.min(yf))
# print(np.max(yf))

# plt.plot([s*1e6 for s in sx[0:10]],xf[0:10],'-',label='x')
# plt.plot([s*1e6 for s in sy[0:10]],yf[0:10],'-',label='y')
# # plt.xscale('log')
# plt.yscale('log')
# plt.xlabel('Feature size [um]')
# plt.ylabel('Power')
# plt.legend()
# plt.show()
        
# print(sx)

# plt.plot(freqx,xf,'.')
# # plt.xscale('log')
# plt.yscale('log')
# plt.show()

# domx = sx[xf==np.max(xf)]

# print(domx)

# print('Dominant x ', (sx[xf==np.max(xf)]), ' m')
# print('Dominant y ', (sy[yf==np.max(yf)]), ' m')

# # print(np.shape(freqy))

# # plt.plot(freqx.ravel(),imagefft.ravel(),'.',label='x')
# # plt.plot(freqy.ravel(),imagefft.ravel(),'.',label='y')
# # plt.show()


# # fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(14, 6))
# # ax[0,0].hist(imagefft.ravel())
# # ax[0,0].set_title('hist(freqx)')
# # ax[0,1].hist(np.log(imagefft).ravel())
# # ax[0,1].set_title('hist(log(freqx))')
# # ax[1,0].imshow(np.log(imagefft), interpolation="none")
# # ax[1,0].set_title('log(freqx)')
# # ax[1,1].imshow(image, interpolation="none")
# # plt.show()