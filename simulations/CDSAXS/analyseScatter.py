#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 29 14:26:17 2025

@author: -
"""

import numpy as np
import matplotlib.pyplot as plt

import matplotlib.ticker as ticker
import scipy
from scipy import signal
import FWarbValue

# maskFile = ''
intensityFile = '/user/home/opt/xl/xl/experiments/CDSAXS/data/test/circ_ap_larger/500um_5/IntensityDist.dat'
I_threshold = 1
G_size = 100
_e = 2.71828
frac = 1/_e
log = 1
fitGauss = 0
savgol = 80
suppress_peak = 165

nx = str(np.loadtxt(intensityFile, dtype=str, comments=None, skiprows=6, max_rows=1, usecols=(0)))[1:]#[1:3]
ny = str(np.loadtxt(intensityFile, dtype=str, comments=None, skiprows=9, max_rows=1, usecols=(0)))[1:]#[1:3]
xMin = str(np.loadtxt(intensityFile, dtype=str, comments=None, skiprows=4, max_rows=1, usecols=(0)))[1:]#[1:3]
xMax = str(np.loadtxt(intensityFile, dtype=str, comments=None, skiprows=5, max_rows=1, usecols=(0)))[1:]#[1:3]
rx = float(xMax)-float(xMin)
dx = np.divide(rx,float(nx))
yMin = str(np.loadtxt(intensityFile, dtype=str, comments=None, skiprows=7, max_rows=1, usecols=(0)))[1:]#[1:3]
yMax = str(np.loadtxt(intensityFile, dtype=str, comments=None, skiprows=8, max_rows=1, usecols=(0)))[1:]#[1:3]
ry = float(yMax)-float(yMin)
dy = np.divide(ry,float(ny))
numC = 1 #int(str(np.loadtxt(intensityFile, dtype=str, comments=None, skiprows=10, max_rows=1, usecols=(0)))[1:])#[1:3]
print("Resolution (x,y): {}".format((nx,ny)))
print("xRange: {}".format(rx))
print("xMax: {}".format(xMax))
print("xMin: {}".format(xMin))
print("yRange: {}".format(ry))
print("yMax: {}".format(yMax))
print("yMin: {}".format(yMin))
print("Dx, Dy : {}".format((dx,dy)))

I = np.reshape(np.loadtxt(intensityFile,skiprows=10), (numC,int(ny),int(nx)))
I = I[0,:,:]

# # converting from ph/s/mm^2 to ph/s
# I = (I / 1.0e-6) * (dx*dy)

I = np.where(I < I_threshold, 1, I)
# I = tifffile.imread(intensityFile)

# Getting PSD of far-field intesity distribution (along y direction)
P,F = [],[]
for n,y in enumerate(I.T):
    L = len(y)*dy
    fmin = 1 / (2*np.pi*L)
    smax =  1 / fmin
    
    X = np.linspace(-L/2,L/2,num=len(y),endpoint=True)
    
    if n == 0:
        print('\n')
        print('Shape of y:                   ', np.shape(y))
        print('Length of sampled area:       ', L*1e3, ' mm')
        print("minimum frequency sampled:    ", fmin/1e6, ' /um')
        print("maximum feature size sampled: ", smax*1e6, ' um')
        # plt.plot(X,y)
        # plt.show()
    
    f,p = signal.periodogram(y,1/dx)
    
    P.append(p)
    F.append(f)


# print(np.shape(F))
f=np.mean(F,axis=0)
p=np.mean(P,axis=0)
# print(np.shape(F))

plt.plot([_f/1.0e-9 for _f in f[1::]], p[1::],'.')#, label='biased',alpha=0.2)
ax = plt.gca()
ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%0.0e'))
plt.yscale('log')
plt.xscale('log')
plt.xlabel('Spatial frequency (nm$^{-1}$)')
plt.ylabel('Fourier power (au)')
plt.title('Fourier power spectrum')
plt.legend()
plt.show()

# Smoothing I with Gaussian the size of speckles
# I = gaussian_filter(I)
fig, ax = plt.subplots(1,2)
ax[0].imshow(np.log(I))
ax[0].set_title('raw (log)')

I = scipy.ndimage.gaussian_filter(I, sigma=G_size/6, mode='reflect')

ax[1].imshow(np.log(I))
ax[1].set_title('Gaussian filtered (log)')
plt.show()

# Getting average y-profile of smoothed I
Iy1_l = np.log(np.mean(I[:,0:1500],axis=1))
Iy2_l = np.log(np.mean(I[:,-1500::],axis=1))
Iy_l = (Iy1_l + Iy2_l) / 2

Iy1 = np.mean(I[:,0:1500],axis=1)
Iy2 = np.mean(I[:,-1500::],axis=1)
Iy = (Iy1 + Iy2) / 2
# removing central diffraction peak
ny = int(ny)
if suppress_peak:
    N = suppress_peak
    plt.plot(Iy_l,label='before peak suppression (log)')
    plt.plot(Iy/np.max(Iy) * np.max(Iy_l),label='before peak suppression')
    Iy_l[ny//2-N:ny//2+N] = Iy_l[ny//2-(N+1)]
    Iy[ny//2-N:ny//2+N] = Iy[ny//2-(N+1)]
    plt.plot(Iy_l,label='after peak suppression (log)')
    plt.plot(Iy/np.max(Iy) * np.max(Iy_l),label='after peak suppression')
    plt.legend()
    plt.show()


# Removing background
Iy_l = Iy_l - np.min(Iy_l)
Iy = Iy - np.min(Iy)

if fitGauss:
    from multiGaussFit import fitMultiGauss
    if log:
        amp = np.max(Iy)* 0.8
        mu = len(Iy)//2
        sigma = mu/3
    else:
        amp = np.max(Iy)
        mu = len(Iy)//6
        sigma = mu/3
    
    amp,mu,sigma = fitMultiGauss(Iy, dx=dy, N=1, iG=[amp,mu,sigma], known=[0,1,0])
    
    Iy = FWarbValue.gauss(X,amp,0,sigma*dy,plot=False)

if savgol:
    from scipy.signal import savgol_filter
    plt.plot(X,Iy_l,label='before savgol')
    Iy_l = savgol_filter(Iy_l,window_length=len(Iy)-1,polyorder=savgol)
    plt.plot(X,Iy_l,label='after savgol, order: ' + str(savgol))
    plt.legend()
    plt.show()

#Getting width of central intensity envelope at 1/e value
# IW = FWarbValue(Iy,1/e)
plt.plot(X,Iy_l, label='log')
plt.plot(X,Iy/np.max(Iy) * np.max(Iy_l), label='linear (normalised)')
# IW = FWarbValue.getFWatValue(I, dx, dy, averaging=5000, frac=1/_e, cuts='y')
IW = len(Iy_l[Iy_l>(Iy_l.max()*frac)])*dy
#Getting total flux in scattered envelope
Iys = Iy[Iy_l>(Iy_l.max()*frac)]
Iys = (Iys / 1.0e-6) * (dx*dy)
F = np.sum(Iys)

plt.text(0.0002, np.max(Iy_l), "FW@1/e : " + str(IW*1e3) + " mm")
plt.vlines([-IW/2,IW/2],ymin=np.min(Iy_l),ymax=np.max(Iy_l),colors='r',linestyles=':')
plt.legend()
plt.show()

print("Full width @ 1/e max:    ", IW*1e3, " mm")
print("Flux in full width @ 1/e max:    ", F)

