#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 15:25:15 2023

@author: -
"""

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from skimage import io,  exposure, img_as_uint, img_as_float
from FWarbValue import getFWatValue

# Location of the images
imageFolder = Path('/user/home/data/19791/Spectra_2022_12_11_corse_changed_wbs_offset/normalised/')

saveImages = False ### CHANGE THIS TO AVOID SAVING NEW IMAGES - added by jk
show = False
gratingArea = True

x0,y0 = 0,0 #180,420
xL,yL = 800,600 #520, 380


img = []
FWHMx,FWHMy = [],[]
Itot=[]
count = 0
for i in imageFolder.glob("*.tif"):
    im = io.imread(i)
    # find central intensity peak
    centerIndex = np.unravel_index(im.argmax(), im.shape)
    x0 = centerIndex[1]
    y0 = centerIndex[0]
#    print(x0,y0)
#    im = im[y0:y0+yL,x0:x0+xL]
    im = im[y0-(yL//2):y0+(yL//2),x0-(xL//2):x0+(xL//2)]
#    img.append(im)

    if show:
        plt.plot(im[im.shape[0]//2,:])
#        if count % 10 == 0:
#            
#            print('number ', count)
#            print(im.shape)
#            fig, ax = plt.subplots(1,3)
#            ax[0].plot(im[im.shape[0]//2,:])
#            ax[1].imshow(im,aspect='auto')
#            ax[2].plot(im[:,im.shape[1]//2])
##            plt.colorbar()
#            plt.show()
    count +=1
    
    fwhmx,fwhmy = getFWatValue(im,frac=0.5,dx=11e-6,dy=11e-6,
                               centered=False,smoothing=True,sorder=17,
                               verbose=False,show=True)
    
    FWHMx.append(fwhmx)
    FWHMy.append(fwhmy)
    
    if gratingArea:
        from utilMask_n import defineOrderROI
        GA = 100.0e-6
        
        G, Isum = defineOrderROI(im,res=(11.0e-6,11.0e-6),
                                 m=1,dX=int(GA/11.0e-6),dY=int(GA/11.0e-6))
        Itot.append(Isum)
    
plt.show()

energy_range =  np.arange(90,900,10)

plt.plot(energy_range,[f*1e3 for f in FWHMx],'x:',label='x')
plt.plot(energy_range,[f*1e3 for f in FWHMy],'x:',label='y')
plt.xlabel('Energy [eV]')
plt.ylabel('FWHM [mm]')
plt.legend()
plt.show()



plt.plot(energy_range,[i for i in Itot[0]],'x:',label='0 order')
plt.plot(energy_range,[a + b for a,b in zip(Itot[1],Itot[2])],'x:',label='1st order')
plt.xlabel('Energy [eV]')
plt.ylabel('Intensity (total)')
plt.legend()
plt.show()


