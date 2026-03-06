#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 21:31:21 2021

@author: -
"""
import imageio
import matplotlib.pyplot as plt
import numpy as np
import interferenceGratingModelsJK

# Grating orientation
orientation = 'ver'

# Grating path
maskPath = '/user/home/opt/xl/xl/experiments/masks/T20nm_1.00000_1.00000_100.00000_mask.tif'

# Load mask tif file
maskTif = imageio.imread(maskPath)
# Define grating area
gratingTif = maskTif[1100:4000,7000:10000]
# Number of pixels and mid point
nX, nY = np.shape(gratingTif)
midX, midY = nX/2, nY/2

# Take line profile through grating
if orientation == 'ver':
    gratingProf = gratingTif[:,int(midX/2)]
elif orientation == 'hor':
    gratingProf = gratingTif[int(midY/2),:]

# Plot
fig, axs = plt.subplots(1,2)
axs[0].imshow(gratingTif, aspect='auto') #[0:5000,5000:10000])
axs[1].plot(gratingProf, label='profile: ' + orientation )
axs[1].legend()
fig.tight_layout()
plt.show()


mC = interferenceGratingModelsJK.gratingContrastMichelson(gratingProf)
rmsC = interferenceGratingModelsJK.gratingContrastRMS(gratingProf)
#fC = interferenceGratingModelsJK.gratingContrastFourier(gratingProf)[0]
#nC = interferenceGratingModelsJK.NILS(gratingProf)[0]
cC = interferenceGratingModelsJK.meanDynamicRange(gratingProf)[0]


print('Michelson Contrast:         {}'.format(mC))
print('RMS Contrast:               {}'.format(rmsC))
#print('Fourier Contrast:           {}'.format(fC))
print('Composite Contrast:         {}'.format(cC))
#print('NILS:                       {}'.format(nC))


