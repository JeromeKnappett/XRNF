#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  8 12:24:41 2023

@author: -
"""

from image_processing import findCorrelation
import numpy as np
import matplotlib.pyplot as plt

def abs2(x):
    return x.real**2 + x.imag**2

imagePath = '/user/home/data/slsMask90to290ev_50msExpose/first10000/'
imagePath2 = '/user/home/data/slsMask90to290ev_50msExpose/'

# # first 1000 images
# C = findCorrelation(imagePath, imgType='.tif', name='a_1_',area=(100,100))
# print(C)
# fft = np.fft.rfft(C, norm="ortho")

# selfconvol=np.fft.irfft(abs2(fft), norm="ortho")

plt.plot(selfconvol[1::])
plt.show()


# rest of images
C2 = findCorrelation(imagePath2, imgType='.tif', name='a_1_',area=(100,100))
fft2 = np.fft.rfft(C2, norm="ortho")

selfconvol2=np.fft.irfft(abs2(fft2), norm="ortho")

plt.plot(selfconvol2[1:1010])
plt.show()