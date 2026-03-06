#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 20 14:46:51 2025

@author: jerome
"""

import numpy as np
import matplotlib.pyplot as plt

wl = 6.7e-9
#13.5e-9
Gx = 50e-6
Gy = 100e-6
d = 2*Gx
pg = 100.0e-9
pr = np.linspace(0.0,500e-9,1000)

dy = (d/2)*np.sqrt(((pg**2) - (wl**2)) / ((pr**2) - (wl**2)))

plt.plot([p*1e9 for p in pr],[x*1e6 for x in dy])
plt.xlabel('LER period [nm]')
plt.ylabel('displacement [um]')

# interpreting x value based on y value
y_val = Gy
x_interp = np.interp(y_val, dy, pr)*1e9#round(np.interp(y_val, dy, pr), 4)  # x_interp = np.interp(y_vals, y, x)
print(x_interp)
# place a marker on point (x_interp, y_val)
plt.plot(x_interp, y_val*1e6, 'o', color='k')

# draw dash lines
plt.plot([x_interp, pr[0]*1e9], [y_val*1e6, y_val*1e6], '--', color='k')
plt.plot([x_interp, x_interp], [dy[0]*1e6, y_val*1e6], '--', color='k')

plt.yscale('log')
#plt.hlines(Gy*1e6,0,500,linestyles='--',label='Gy')
plt.legend()
plt.show()