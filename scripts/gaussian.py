#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 18 10:43:23 2025

@author: jerome
"""

import numpy as np
import matplotlib.pyplot as plt

def difAngle(wl,p,m=1):
    theta = np.arcsin((m*wl)/p)
    return theta


E10 = 0.5
E20 = 0.5
E30 = 0.02
E1p = 0.0#np.pi
E2p = 0.0
E3p = 0*np.pi
wl = 6.7e-9
k = (2*np.pi)/wl
p= 100.0e-9
theta = difAngle(wl,p)
w=1/wl
t = 0.0

ratio_sum = E10 + E20
E1a = E10 / ratio_sum * (1 - E30)
E2a = E20 / ratio_sum * (1 - E30)
E3a = E30*np.sqrt(2)

# Grid size
Nx, Ny = 300, 300

# Physical extent of the grid
x_min, x_max = -200.0e-9, 200.0e-9
y_min, y_max = -200.0e-9, 200.0e-9

# Generate coordinates and meshgrid
x = np.linspace(x_min, x_max, Nx)
y = np.linspace(y_min, y_max, Ny)
xx, yy = np.meshgrid(x, y)

# Beam waist parameter
w0 = 1.0e-3

# Wave number (arbitrary example)
wl = 6.7e-9
k = (2*np.pi)/wl
z = 100e3
R = 10.0

# Complex Gaussian beam electric field:
#   E(x,y) = exp[-(x^2 + y^2)/w0^2] * exp[i * phase_term * (x^2 + y^2)]
# Here we use a simplified quadratic phase. In reality, you'd have
# more terms for curvature, Gouy phase, etc., at different propagation distances.
amplitude_factor = E3a*np.exp(- (xx**2 + yy**2) / w0**2)
phase_factor = np.exp(-1j * k * ((z +((xx**2 + yy**2) / (2.0 * R)))) + E3p)
#np.exp(1j * k * (xx**2 + yy**2) / (2.0 * 5.0))  # e.g. focusing at z=5.0
E_T = amplitude_factor * phase_factor

# Extract amplitude and phase
amplitude = np.abs(E_T)
phase = np.angle(E_T)

# --- Plot amplitude ---
plt.figure()
plt.imshow(amplitude, extent=[x_min, x_max, y_min, y_max],
           origin='lower', aspect='auto')
plt.colorbar(label='Amplitude')
plt.title("Gaussian Beam (Amplitude)")
plt.xlabel("x")
plt.ylabel("y")
plt.show()

# --- Plot phase ---
plt.figure()
plt.imshow(phase, extent=[x_min, x_max, y_min, y_max],
           origin='lower', aspect='auto', cmap='twilight')
plt.colorbar(label='Phase [radians]')
plt.title("Gaussian Beam (Phase)")
plt.xlabel("x")
plt.ylabel("y")
plt.show()

print(np.shape(E_T))

E_T = E_T[np.shape(E_T)[0]//2,:]


E1 = E1a * np.exp((1j * k * x * np.sin(theta)) - (w*t) - E1p)
E2 = E2a * np.exp((-1j * k * x * np.sin(theta)) - (w*t) - E2p)

E = E1 + E2 + E_T

I1 = np.sum(abs(E1**2))
I2 = np.sum(abs(E2**2))
I3 = np.sum(abs(E_T**2))

print('Total I1:   ', I1)
print('Total I2:   ', I2)
print('Total IT:   ', I3)

print("% contamination: ", 100*(I3/(I1 + I2 + I3)))



I = abs(E**2)


plt.plot([a*1e9 for a in x],I)
plt.show()