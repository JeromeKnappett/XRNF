#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 25 17:20:48 2021

@author: jerome
"""

import numpy as np
import matplotlib.pyplot as plt
import tifffile

colours = plt.rcParams["axes.prop_cycle"].by_key()["color"]
    
def round_sig(x, sig=2):
    from math import floor, log10
    if x != 0:
        return round(x, sig-int(floor(log10(abs(x))))-1)
    else:
        return x
    
dirPath = '/home/jerome/dev/data/sourceNdBeam/maskPlane/' #'/home/jerome/dev/experiments/beamPolarisation17/data/degrees/i' #'/home/jerome/dev/data/sourceNdBeam/maskPlane/' #experiments/beamPolarisation17/data/' #/data/beamCharacterisationVer/' #data/sourceNdBeam/maskPlane/' #beamCharacterisationVer/'

name = 'atMaskStokes' #'0'#'atMaskStokes' #'inCirR'

cfiles = ['coherencecoherenceHor.tif', 'coherencecoherenceVer.tif']
sfiles=  [name + 'stokes' + str(s) + '.tif' for s in [0,1,2,3]]
          # 'inLin45stokes0.tif',#'inLin45stokes0.tif', #'atMaskStokesstokes0.tif',
          # 'inLin45stokes1.tif',#'inLin45stokes1.tif', #'atMaskStokesstokes1.tif',
          # 'inLin45stokes2.tif',#'inLin45stokes2.tif', #'atMaskStokesstokes2.tif',
          # 'inLin45stokes3.tif']#'inLin45stokes3.tif'] #'atMaskStokesstokes3.tif']

plotType = 'stokes' #'intensity' #'stokes' #'coherence'
normalise = True
numPix = False #200 #False #1000

save = True
savePath = '/home/jerome/Documents/MASTERS/Figures/plots/'

if plotType == 'intensity':
    # dX, dY = 
    pass


if plotType == 'coherence':
    dXh, dYh = 6.68724364046726e-07, 1.330791653036487e-05
    dXv, dYv = 1.67444935861477e-05, 7.169247962486125e-07
    for i,f in enumerate(cfiles):
        c = tifffile.imread(dirPath + f)
        
        if i == 0:
            dX, dY = dXh, dXh
        elif i ==1:
            dX, dY = dYv, dYv
            
        nY, nX = np.shape(c)
        rY, rX = nY*dY, nX*dX
        print('Pixels (x,y):     {}'.format((nX,nY)))
        print('Range (x,y):      {}'.format((rX,rY)))
        print('Resolution (x,y): {}'.format((dX,dY)))
        
        plt.imshow(c, aspect='auto')
        plt.colorbar()
        plt.xticks()
        plt.yticks([int(nY*(b/8)) for b in range(0,9)],
                   [round_sig(nY*dY*(a/8)*1e6) for a in range(0,9)])
        plt.xticks([int(nX*(b/8)) for b in range(0,9)],
                   [round_sig(nX*dX*(a/8)*1e6) for a in range(-4,5)])
        plt.show()




if plotType == 'stokes':
    import jerome.dev.scripts.utilStokes as utilStokes
    dX, dY = 8.365500474037091e-06, 3.584623981243063e-07 #6.673209267855702e-06, 6.671991414331421e-06 #8.365500474037091e-06, 3.584623981243063e-07
    S0 = tifffile.imread(dirPath + sfiles[0])
    S1 = tifffile.imread(dirPath + sfiles[1])
    S2 = tifffile.imread(dirPath + sfiles[2])
    S3 = tifffile.imread(dirPath + sfiles[3])
    
    if normalise:
        S1 = S1/np.max(S0)
        S2 = S2/np.max(S0)
        S3 = S3/np.max(S0)
        S0 = S0/np.max(S0)
    
    if numPix:
        S = [S0[np.shape(S0)[0]//2-(numPix//2):np.shape(S0)[0]//2+(numPix//2),np.shape(S0)[1]//2-(numPix//2):np.shape(S0)[1]//2+(numPix//2)],
             S1[np.shape(S1)[0]//2-(numPix//2):np.shape(S1)[0]//2+(numPix//2),np.shape(S1)[1]//2-(numPix//2):np.shape(S1)[1]//2+(numPix//2)],
             S2[np.shape(S2)[0]//2-(numPix//2):np.shape(S2)[0]//2+(numPix//2),np.shape(S2)[1]//2-(numPix//2):np.shape(S2)[1]//2+(numPix//2)],
             S3[np.shape(S3)[0]//2-(numPix//2):np.shape(S3)[0]//2+(numPix//2),np.shape(S3)[1]//2-(numPix//2):np.shape(S3)[1]//2+(numPix//2)]]
    else:
        S = [S0,
             S1,
             S2,
             S3]
    
    # print(np.max(S0))
    # print(np.max(S1))
    # print(np.max(S2))
    # print(np.max(S3))
    
    unitConversion = 1e3
    dX, dY = unitConversion*dX, unitConversion*dY
    
    if save:
        utilStokes.plotStokes(S,dx=dX,dy=dY,savePath = savePath+name, compact=True)
    else:
        utilStokes.plotStokes(S,dx=dX,dy=dY, compact=True)
    pass
