#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 17 10:34:21 2025

@author: jerome
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from matplotlib.pyplot import figure
from math import floor, log10

plt.rcParams["figure.figsize"] = (6,4)
# %%
def round_sig(x, sig=2):
    if x != 0:
        return round(x, sig - int(floor(log10(abs(x)))) - 1)
    else:
        return x
def maxFrequencyLER(NA,wl,gamma):
    f = (NA/wl)*(1+gamma)
    return f

def diffractionAngle(wl,p,m=1,theta_i = 0):
    theta = np.arcsin(((m*wl) / p) + np.sin(theta_i))
    return theta

# Set up parameters
wl = 13.5e-9
#13.5e-9
#6.7e-9        # wavelength (example, in same units as p)
NA_values = np.linspace(0.05, 0.95, 500)   # range of d
gamma_values = np.linspace(0.0, 1, 500)  # range of p (must be large enough so p^2 > m^2*wl^2)

pitches =[100e-9,50e-9,20e-9, 15.0e-9]

NA_IL = [np.sin(diffractionAngle(wl,p)) for p in pitches]

# Create meshgrids for plotting
NA, G = np.meshgrid(NA_values, gamma_values)

# Compute Z for each (d, p)
fmax = maxFrequencyLER(NA, wl, G)

C = [(1/f)*((4*1e9)) for f in fmax]

print(np.min(C))
print(np.max(C))
print(f"Diffraction angle:      {diffractionAngle(wl,pitches[0])} rad")
print(f"Diffraction angle:      {np.degrees(diffractionAngle(wl,pitches[0]))} degrees")
print(f"Numerical aperture:     {NA_IL[0]}")

print(NA_IL[len(NA_IL)//2])
# Plot using imshow
plt.figure()
# extent sets the axis ranges: (x_min, x_max, y_min, y_max)
im = plt.imshow(C, origin='lower',
                extent=(NA_values[0], NA_values[-1], gamma_values[0], gamma_values[-1]),
                aspect='auto',
                cmap='nipy_spectral_r',
                
                 norm=LogNorm(vmin=np.min(C),vmax=np.max(C))
                )
im.set_clim(14.0, 1080.0)
plt.vlines(NA_IL,0,1,colors='black',linestyles='--')
for i,p in enumerate(pitches):
    if i == 0:
        t = plt.text(NA_IL[i] + 0.01, 0.475,s = '$p_G$ = ' + str(p*1e9) + ' nm',color='black',rotation=-90)
#        t.set_bbox(dict(facecolor='white',alpha=0.2,linewidth=0))
    else:
        t = plt.text(NA_IL[i] + 0.01, 0.5,s = '$p_G$ = ' + str(np.round(p*1e9)) + ' nm',color='black',rotation=-90)
#        t.set_bbox(dict(facecolor='white',alpha=0.2,linewidth=0))
plt.text(0.75,0.93,'$\lambda = $' + str(round_sig(wl*1e9,3)) + ' nm',bbox=dict(facecolor='white',edgecolor='none'))
plt.colorbar(im,label='$c_{min}$ [nm]')
#plt.colorbar(label='$C_{min}$ [nm]')
plt.xlabel('NA$_{image}$',fontsize=12)
plt.ylabel('$\gamma$',fontsize=16)
#plt.savefig('/home/jerome/Documents/PhD/Figures/ModelApplication/minClength_EUV.pdf',format='pdf')
# plt.title('Aerial Image Distance as a Function of d and p')
plt.show()
