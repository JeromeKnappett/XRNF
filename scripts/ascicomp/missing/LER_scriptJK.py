#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 10:28:39 2022

@author: -
"""

import cv2 #(OpenCV3)
# from LER import edge_roughness
from matplotlib import pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
# import tifffile
import imageio
import pickle
from LER import edge_roughness

plt.rcParams["figure.figsize"] = (5,4)

maskFile = '/user/home/opt/xl/xl/experiments/maskLER_retry/masks/20000000.00000_4.00000_10.00000_mask.tif'
# '/user/home/opt/xl/xl/experiments/masks3/SLS_200p37.5r_Block.tif'#masks/200p37.5rMask.tif'
# '/user/home/opt/xl/xl/experiments/BEUVcoherenceLER1/masks_D50/20000020.00000_0.50000_10.00000_mask.tif'
#'/user/home/opt/xl/xl/experiments/BEUVcoherence/masks/200p50rBlock.tif'
#'/user/home/opt/xl/xl/experiments/BEUVcoherenceLER1/masks_D50/vert_block.tif'
#"/user/home/opt/xl/xl/experiments/maskLER1/masks/20000020.00000_1.00000_10.00000_mask.tif"

maskImage = imageio.imread(maskFile)
# tifffile.imread(maskFile)
print(np.shape(maskImage))

plt.imshow(maskImage,aspect='auto')
plt.title('Full Mask')
plt.colorbar()
plt.show()

X = 20
Y = 20 
midX, midY = np.shape(maskImage)[1]/2, 5000#(3*np.shape(maskImage)[0])/17
pitch = 200 #pixels
hp = pitch/2

print(midX, midY)

# gratingImage = maskImage[int(midY - (Y/2)):int(midY + (Y/2)), int(midX - (X/2)):int(midX + (X/2))]
# #maskImage[1000:5000,6500:10500]

# plt.imshow(gratingImage)
# plt.show()

# save2pick = False

# if save2pick:
#     with open(maskFile[0:int(len(maskFile)-4)] + 'CLOSE.pkl', "wb") as f:
#                 pickle.dump(gratingImage, f, protocol=2)


#offset = hp

#lineImage = gratingImage[int(2000 - hp):int(2000),:]
# lineImage = gratingImage[int(2000 - hp):int(2000 + hp),1000:2000]
lineImage = maskImage[1000:2000,int(2000 - hp):int(2000 + hp)]
# np.rot90(maskImage[1000:2000,int(2000 - hp):int(2000 + hp)])

plt.imshow(lineImage,aspect=5)
plt.show()


LER = edge_roughness()
(Xcln, Ycln, freq, FourierPow) = LER.LER_analysis(lineImage, 10e-6, 3) #image, image width (m), threshold for outliers


plt.plot(Xcln, Ycln, '-')
plt.plot(Xcln, Ycln, 'r.')
plt.show()

plt.plot(freq[2:100], FourierPow[2:100],'-')
ax = plt.gca()
ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%0.0e'))
plt.xlabel('cycles (m$^{-1}$)')
plt.ylabel('Fourier power (au)')
plt.title('Fourier power spectrum')
plt.show() 

#cv2.imshow('Origional Image',image)
#cv2.waitKey(0)
#cv2.destroyAllWindows()


