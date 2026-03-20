#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 22 10:18:15 2025

@author: -
"""

import numpy as np
import matplotlib.pyplot as plt

from xraydb import material_mu

energy = [91.8, 185.0, 293.0] #np.linspace(1000, 41000, 201)

T = np.linspace(50e-7,300e-7,1000)

for i,e in enumerate(energy):
    mu = material_mu('Au', e)
    print(mu)
    # mu is returned in 1/cm
    trans = np.exp(-0.1 * (mu*T))

    # print(trans)
    plt.plot([t*1e9 for t in T],trans, label=str(energy[i]) + ' eV')
    # plt.plot(energy, 1-trans, label='attenuated')
# plt.title('Transmisson of Au')
plt.xlabel('Thickness (nm)')
plt.ylabel('Transmitted fraction')
plt.legend()
plt.show()