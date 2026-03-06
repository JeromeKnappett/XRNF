#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 13 13:02:04 2025

@author: jerome
"""

import numpy as np
import matplotlib.pyplot as plt
import unicodedata as ud

def aerialImageDistance(d, p, m, wl):
    # Returns the image plane distance z
    z = (d * np.sqrt((p**2) - (m**2 * wl**2))) / (2 * m * wl)
    return z

# Set up parameters
m = 1.0         # magnification (example)
wl = 6.7e-9        # wavelength (example, in same units as p)
d_values = np.linspace(1e-6, 150e-6, 500)   # range of d
p_values = np.linspace(7e-9, 100e-9, 500)  # range of p (must be large enough so p^2 > m^2*wl^2)

# Create meshgrids for plotting
D, P = np.meshgrid(d_values, p_values)

# Compute Z for each (d, p)
Z = aerialImageDistance(D, P, m, wl)

print('\N{GREEK SMALL LETTER MU}')
print('µ')

colormap = [
#            'hsv_r',
#            'gist_stern_r',
#            'gnuplot',
#            'CMRmap',
#            'cubehelix',
#            'brg',
#            'gist_rainbow',
#            'rainbow',
#            'jet',
#            'turbo',
            'nipy_spectral_r',
#            'gist_ncar_r'
            ]
#mu = ud.lookup(mu)
# Plot using imshow
for c in colormap:
    plt.figure()
    # extent sets the axis ranges: (x_min, x_max, y_min, y_max)
    plt.imshow([z*1e3 for z in Z], origin='lower', cmap=c, extent=(d_values[0]*1e3, d_values[-1]*1e3, p_values[0]*1e9, p_values[-1]*1e9), aspect='auto')
    plt.colorbar(label='$z_1$ [mm]')
    plt.xlabel('$d$ [mm]')
    plt.ylabel('$p_G$ [nm]')
#    plt.title(c)
    plt.savefig('/home/jerome/Documents/PhD/Figures/LitReview/image_distance_BEUV.pdf', format='pdf')
    plt.show()
