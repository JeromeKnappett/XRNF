#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 14:47:09 2022

@author: jerome
"""

import numpy as np
import matplotlib.pyplot as plt
import pickle
import tifffile
import plotting

roughness = 'surface'

dirPath = '/home/jerome/dev/masks/forPlotting/'

if roughness == 'surface':
    savePath = dirPath + 'maskLinesSurfaceRoughnessWithCbar.eps'
    
    maskPaths = [dirPath + p for p in ['T20nm_0.50000_10.00000_2.50000_mask.tif','T20nm_1.50000_10.00000_2.50000_mask.tif','T20nm_2.50000_10.00000_2.50000_mask.tif']]
    masks = [tifffile.imread(m) for m in maskPaths]
    maskLines = [plotting.resample(m,fx=0.19,fy=0.0175,midX=8500,midY=3001,debug=False,show=False) for m in masks]
    
    plotting.plotMultiTwoD(maskLines,
                           dims=[1,3],
                           dx=[2.5e-9,2.5e-9,2.5e-9],
                           dy=[2.5e-9,2.5e-9,2.5e-9],
                           sF=1e6,
                           ran=[(np.min(maskLines),np.max(maskLines))],
                           xLabel= 'x-position $[\mu m]$',
                           yLabel= 'y-position $[\mu m]$',
                           fSize=2,
                           numXticks= 3,
                           numYticks= 5,
                           onlyEdgeLabels= True,
                           aspct ='auto',
                           colour = 'gray',
                           cBar = 'bottom', # None,#'side', #'bottom',
                           cbarLabel= None,#'Intensity [ph/s/.1\%bw/mm²]', #'NILS', #'Intensity [ph/s/.1\%bw/mm²]',
                           multiCBar= False,
                           savePath = savePath)#'Intensity [ph/s/.1%bw/mm²]')
    

elif roughness == 'LER':
    savePath = dirPath + 'maskLinesLER.eps'
    
    maskPaths = [dirPath + p for p in ['20000020.00000_2.00000_10.00000_maskCLOSE.pkl','20000020.00000_3.00000_10.00000_maskCLOSE.pkl','20000020.00000_4.00000_10.00000_maskCLOSE.pkl']]
    masks = [pickle.load(open(p, 'rb')) for p in maskPaths]
    
    maskLines = [plotting.resample(m,fx=0.63,fy=0.04,debug=False,show=False) for m in masks]
    
    plotting.plotMultiTwoD(maskLines,
                           dims=[1,3],
                           dx=[1.25e-9,1.25e-9,1.25e-9],
                           dy=[1.25e-9,1.25e-9,1.25e-9],
                           sF=1e6,
                           ran=[(np.min(maskLines),np.max(maskLines))],
                           xLabel= 'x-position $[\mu m]$',
                           yLabel= 'y-position $[\mu m]$',
                           fSize=15,
                           numXticks= 3,
                           numYticks= 5,
                           onlyEdgeLabels= True,
                           aspct ='auto',
                           colour = 'gray',
                           cBar = None,#'bottom', # None,#'side', #'bottom',
                           cbarLabel= None,#'Intensity [ph/s/.1\%bw/mm²]', #'NILS', #'Intensity [ph/s/.1\%bw/mm²]',
                           multiCBar= False,
                           savePath = savePath)#'Intensity [ph/s/.1%bw/mm²]')