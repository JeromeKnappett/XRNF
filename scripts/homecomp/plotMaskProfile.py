#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 17 13:46:07 2021

@author: jerome
"""

import pickle
import matplotlib.pyplot as plt
import numpy as np

with open('/home/jerome/dev/data/profiles.pkl', 'rb') as p:
    profiles = pickle.load(p)
    
print(np.shape(profiles))

labels = ['\u03C3 = 2.5 nm, $C$ = 2 nm','\u03C3 = 0.5 nm, $C$ = 2 nm',
          '\u03C3 = 2.5 nm, $C$ = 10 nm','\u03C3 = 0.5 nm, $C$ = 10 nm']
x = np.linspace(-500*2.5e-3,500*2.5e-3,1000)
thickness = [3.740484237754313e-08,2.353025172753083e-08,5.955319433439844e-08,2.7597255910327376e-08]

for i,p in enumerate(profiles):
    plt.plot(x,p*thickness[i]*4e6, label=labels[i])
    plt.xlabel('Position [\u03bcm]')
    plt.ylabel('Mask Height [nm]')
    plt.legend()
plt.savefig('/home/jerome/Documents/MASTERS/Figures/plots/maskRoughnessProfiles.pdf')
plt.savefig('/home/jerome/Documents/MASTERS/Figures/plots/maskRoughnessProfiles.png', dpi=2000)
plt.show()
    