#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 11:26:09 2023

@author: -
"""

import cv2
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import LogNorm

img = cv2.imread('/user/home/opt_old/xl/xl/experiments/masks3/single_vert_mask.tif',0)
old_size = np.shape(img)
# print(old_size)
top,bottom,left,right = [4000]*4
img_with_border = cv2.copyMakeBorder(img,top,bottom,left,right, cv2.BORDER_CONSTANT, value=0)


f = np.fft.fft2(img_with_border)
_f = np.abs(f)
fshift = np.fft.fftshift(f)
magnitude_spectrum = 20*np.log(np.abs(fshift))

plt.subplot(121),plt.imshow(img_with_border, cmap = 'gray')
plt.title('Input Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(magnitude_spectrum, cmap = 'gray')
# plt.subplot(122),plt.imshow(_f, cmap = 'gray', norm=LogNorm(vmin=np.min(_f), vmax=np.max(_f)))
plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
plt.show()