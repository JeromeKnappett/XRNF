#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  8 16:31:00 2023

@author: -
"""

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from skimage import io,  exposure, img_as_uint, img_as_float
from tqdm import tqdm
import os

from usefulWavefield import counts2photonsPsPcm2, intensity2power, findBeamCenter
from FWarbValue import getFWatValue

from image_processing import sumImages,cropImage,IoverGrating
 
    
# Location of the images
imageFolder = '/user/home/data/slsMask91.84ev_no0order/'
darkFolder = '/user/home/data/slsMask91.84ev_no0order/'
savePath_dark = darkFolder + 'darkfield/'
savePath_images = '/user/home/data/DE_processed/91.84ev_no0order/'

# energy_range =  [91.84, 100, 110, 120, 130, 140, 150, 160, 170, 180, 185.05, 190, 200, 210, 220, 230, 240, 250, 260, 270, 3*91.84, 280, 290]

# print("Averaging Darkfield Images...")
# sumImages(darkFolder,name='DF_1_',sumNum=1000,imgType=".tif",average=True,
#           darkfield=None,savePath=savePath_dark,show=True,verbose=True)
print("Summing/Averaging Images...")
ims,iTot,er = sumImages(imageFolder,name='a_3_',sumNum=1000,imgType=".tif",average=True,
                        darkfield=savePath_dark + str(999) + '.tif',
                        savePath=savePath_images,hist=True,show=True,verbose=True)

pEr = [e/i for e,i in zip(er,iTot)] # percentage error for summed intensities
