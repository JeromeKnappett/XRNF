#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 13:53:37 2022

@author: jerome
"""

import numpy as np
import matplotlib.pyplot as plt
import pickle
import tifffile
import plotting

dirPath = '/home/jerome/Downloads/' 

savePath = dirPath + 'intensityPlots.eps'

wavePaths = [dirPath + p for p in ['atExitAp.pkl','atExitSlits.pkl','atBDA_200y.pkl','aerialImageLarge.pkl']]
picks = [pickle.load(open(p, 'rb')) for p in wavePaths]
waves = [p[0] for p in picks]
DX,DY = [p[1] for p in picks],[p[2] for p in picks]

titles=['Exit Aperture','SSA','Mask','Aerial Image']

print(np.max(waves[0]))
print(np.max(waves[1]))
print(np.max(waves[2]))
print(np.max(waves[3]))

plotting.plotMultiTwoD(waves,
                       dims=[2,2],
                       dx=DX,
                       dy=DY,
                       sF=1e3,
                       title=titles,
#                       ran=[(np.min(waves[1]),np.max(waves[1]))],
                       xLabel= 'x-position [mm]', #'x-position $[\mu m]$',
                       yLabel= 'y-position [mm]',#'y-position $[\mu m]$',
                       fSize=10,
                       numXticks= 5,
                       numYticks= 5,
                       onlyEdgeLabels= False,
                       aspct ='auto',
#                       colour = 'gray',
                       cBar = 'side', # None,#'side', #'bottom',
                       cbarLabel= None,#'Intensity [ph/s/.1\%bw/mm²]', #'NILS', #'Intensity [ph/s/.1\%bw/mm²]',
                       multiCBar= True,
                       savePath = savePath)#'Intensity [ph/s/.1%bw/mm²]')


