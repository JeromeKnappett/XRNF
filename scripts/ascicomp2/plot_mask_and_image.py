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
# 'surface'
# 'LER'

dirPath = '/home/jerome/dev/masks/forPlotting/'

if roughness == 'surface':
    dirPath = '/user/home/opt_old/xl/xl/experiments/'#'masks2/'
    savePath = dirPath + 'maskLinesSurfaceRoughness.eps'
    
    res_ae = (2.5011882651601634e-09, 2.426754806976689e-07)
    res_m = (2.5e-9,2.5e-9)
    # (196, 12188)
    aePaths = [dirPath + p for p in ['correctedAngle_roughness/data/20/20intensity.tif','correctedAngle_roughness/data/21/21intensity.tif','correctedAngle_roughness/data/22/22intensity.tif']]#
    maskPaths = [dirPath + p for p in ['masks2/T20nm_0.50000_10.00000_2.50000_mask.tif','masks2/T20nm_1.00000_10.00000_2.50000_mask.tif','masks2/T20nm_1.50000_10.00000_2.50000_mask.tif']]
    # maskPaths = [dirPath + p for p in ['T20nm_0.50000_10.00000_2.50000_mask.tif','T20nm_1.50000_10.00000_2.50000_mask.tif','T20nm_2.50000_10.00000_2.50000_mask.tif']]
    masks = [tifffile.imread(m) for m in maskPaths]
    aes = [tifffile.imread(m).T for m in aePaths]
    
    maskLines = [plotting.resample(m,fx=0.02375,fy=0.02,mid=[3001,8500],debug=False,show=False) for m in masks]
    aeLines = [plotting.resample(m,fx=0.0205,fy=0.005,mid=[12188,196],debug=False,show=False) for m in aes]
    
    plotting.plotMultiTwoD([a for a in [maskLines[0],aeLines[0],maskLines[1],aeLines[1],maskLines[2],aeLines[2]]],
                           dims=[1,6],
                           dx=[res_m[1],res_ae[1],res_m[1],res_ae[1],res_m[1],res_ae[1]],
                           dy=[res_m[0],res_ae[0],res_m[0],res_ae[0],res_m[0],res_ae[0]],
                           sF=1e6,
                           ran=[(np.min(maskLines),np.max(maskLines)),
                                (np.min(aeLines),np.max(aeLines)),
                                (np.min(maskLines),np.max(maskLines)),
                                (np.min(aeLines),np.max(aeLines)),
                                (np.min(maskLines),np.max(maskLines)),
                                (np.min(aeLines),np.max(aeLines))],
                           xLabel= 'x-position $[\mu m]$',
                           yLabel= 'y-position $[\mu m]$',
                           fSize=0.1,
                           numXticks= 3,
                           numYticks= 3,
                           onlyEdgeLabels= True,
                           aspct =[6.8,0.148,6.8,0.148,6.8,0.148],#['auto'],#[0.7],#'auto',
                           colour =['gray',None,'gray',None,'gray',None],
                           cBar = None,#'side',#'side',# 'bottom', # None,#'side', #'bottom',
                           cbarLabel= None,#'Intensity [ph/s/.1\%bw/mm²]', #'NILS', #'Intensity [ph/s/.1\%bw/mm²]',
                           multiCBar= False,
                           savePath = savePath)#'Intensity [ph/s/.1%bw/mm²]')
    

elif roughness == 'LER':
    dirPath = '/user/home/opt/xl/xl/experiments/maskLER_retry2/data/'
    savePath = dirPath + 'maskLinesLER_withCbar.eps'
    
    res_ae = (9.961053965443777e-10, 1.1737763772365647e-08)
    res_m = (1.0e-9,1.0e-9)#(9.961053965443777e-10, 1.1737763772365647e-08)
    
    aePaths = [dirPath + '0nm/0nmintensity.tif',dirPath + '3nm/3nmintensity.tif',dirPath + '6nm/6nmintensity.tif',]
    maskPaths = ['masks/restest_vert_mask.tif','masks/restest_20000020.00000_30.00000_150.00000_mask.tif','masks/restest_20000020.00000_60.00000_150.00000_mask.tif']
    #,'masks/restest_20000020.00000_30.00000_150.00000_mask.tif','masks/restest_20000020.00000_40.00000_150.00000_mask.tif',
                 # 'masks/restest_20000020.00000_50.00000_150.00000_mask.tif','masks/restest_20000020.00000_60.00000_150.00000_mask.tif']
    
    # maskPaths = [dirPath + p for p in ['20000020.00000_2.00000_10.00000_maskCLOSE.pkl','20000020.00000_3.00000_10.00000_maskCLOSE.pkl','20000020.00000_4.00000_10.00000_maskCLOSE.pkl']]
    masks = [tifffile.imread(m) for m in maskPaths]
    aes =  [tifffile.imread(m).T for m in aePaths]
    # [pickle.load(open(p, 'rb')) for p in maskPaths]
    
    maskLines = [plotting.resample(m,fx=0.12,fy=0.03,mid=[4990,9013],debug=False,show=False) for m in masks]
    aeLines = [plotting.resample(m,fx=0.2,fy=0.019,mid=[8001,460],debug=False,show=False) for m in aes]
    
    plotting.plotMultiTwoD([a for a in [maskLines[0],aeLines[0],maskLines[1],aeLines[1],maskLines[2],aeLines[2]]],
                           dims=[1,6],
                           dx=[res_m[1],res_ae[1],res_m[1],res_ae[1],res_m[1],res_ae[1]],
                           dy=[res_m[0],res_ae[0],res_m[0],res_ae[0],res_m[0],res_ae[0]],
                           sF=1e6,
                           ran=[(np.min(maskLines),np.max(maskLines)),
                                (np.min(aeLines),np.max(aeLines)),
                                (np.min(maskLines),np.max(maskLines)),
                                (np.min(aeLines),np.max(aeLines)),
                                (np.min(maskLines),np.max(maskLines)),
                                (np.min(aeLines),np.max(aeLines))],
                           xLabel= 'x-position $[\mu m]$',
                           yLabel= 'y-position $[\mu m]$',
                           fSize=0.1,#12,
                           numXticks= 3,
                           numYticks= 3,
                           onlyEdgeLabels= True,
                           aspct =[15,1.25,15,1.25,15,1.25], #[7,0.6,0,0.8,10,0.8],# ['auto'],#[7,0.55,7,0.6,7,0.6],#0.75,#7#'auto',
                           colour = ['gray',None,'gray',None,'gray',None],
                           cBar = 'side',#'side',#None,#'bottom', # None,#'side', #'bottom',
                           cbarLabel= None,#'Intensity [ph/s/.1\%bw/mm²]', #'NILS', #'Intensity [ph/s/.1\%bw/mm²]',
                           multiCBar= False,
                           savePath = savePath)#'Intensity [ph/s/.1%bw/mm²]')