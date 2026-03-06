#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 14 11:23:10 2021

@author: -
"""

import imageio
import numpy as np
import matplotlib.pyplot as plt
import pickle

masks = ['/user/home/opt/xl/xl/experiments/masks2/' + t for t in ['T20nm_2.50000_2.00000_2.50000_mask.tif',
                                                                  'T20nm_0.50000_2.00000_2.50000_mask.tif',
                                                                  'T20nm_2.50000_10.00000_2.50000_mask.tif',
                                                                  'T20nm_0.50000_10.00000_2.50000_mask.tif']]
cLengths = [2,2,10,10]
rmsR = [2.5,0.5,2.5,0.5]
thickness = [3.740484237754313e-08,2.353025172753083e-08,5.955319433439844e-08,2.7597255910327376e-08]

i, f = 3000,4000

maskTiffs = [imageio.imread(m) for m in masks]
maskProfiles = [t[4000,i:f] for t in maskTiffs]

x = np.linspace(-((f-i)/2)*2.5,((f-i)/2)*2.5,(f-i))

with open('/user/home/opt/xl/xl/experiments/masks2/profiles.pkl','wb') as f:
    g = pickle.dump(maskProfiles,f)

for i,p in enumerate(maskProfiles):
    plt.plot(x*1e-3, (p/np.max(p))*thickness[i]*1e9, label = '\u03C3 = ' + str(rmsR[i]) + ', $C_y = $' + str(cLengths[i])) 
plt.xlabel('Position [um]')
plt.ylabel('Mask Thickness [nm]')
plt.legend()
plt.show()
