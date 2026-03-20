#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  8 16:31:00 2023

@author: -
"""
from image_processing import sumImages

dirPath = '/user/home/data/DetectorCom/slsMask91.84ev_no0order/'

# df, Idf, edf = sumImages(dirPath + 'darkfield/', 'DF_1_',sumNum=1000, average=True,show=True,verbose=True,savePath=dirPath + 'processed/DF_')
im, I, e = sumImages(dirPath,'a_3_',sumNum=1000,darkfield=dirPath + 'processed/DF_999.tif',average=True,show=True,hist=True,verbose=True,savePath=dirPath + 'summed/')

