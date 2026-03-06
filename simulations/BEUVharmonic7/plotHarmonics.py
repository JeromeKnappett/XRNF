#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 12:06:36 2023

@author: -
"""

import numpy as np
import matplotlib.pyplot as plt
import pickle
# from wpg.useful_code.wfrutils import get_mesh
# from wpg.wavefront import Wavefront
from lineProfile import getLineProfile
from FWarbValue import getFWatValue
from math import floor, log10

def round_sig(x, sig=2):
    if x != 0:
        return round(x, sig-int(floor(log10(abs(x))))-1)
    else:
            return x

path = '/user/home/opt/xl/xl/experiments/BEUVbeamProfile/data/harmonics/'

M = [1,2,3,4,5,7]#,7,9]
numPoints = 1000

SE_ME = 'ME'

if SE_ME == 'SE':
#    I = [tifffile.imread(path + 'm' + str(m) + '_atMask_SE/intensity.tif')
    wPath = [path + 'm' + str(m) + '_atMask_SE_tuned/wf_final.hdf' for m in M]
    I = []
    dx,dy = [], []
    for p in wPath:
        wf = Wavefront()
        wf.load_hdf5(p)
        [nx, ny, xmin, xmax, ymin, ymax] = get_mesh(wf)
        dX, dY = (xmax-xmin)/nx, (ymax-ymin)/ny
#        print('Mesh grid period: {}x{}'.format(dX,dY))
        
        I.append(wf.get_intensity())
        dx.append(dX)
        dy.append(dY)

elif SE_ME == 'ME':
    # picks =  [pickle.load(open(path + 'm' + str(m) + '_atMask_ME/m' + str(m) + '_atMask_ME.pkl', 'rb')) for m in M]
    picks =  [pickle.load(open(path + 'm' + str(m) + '_atMask_ME.pkl', 'rb')) for m in M]
#m1 = pickle.load(open(path + 'm1_atMask_MEfixed/m1_atMask_MEfixed.pkl', 'rb'))
#m3 = pickle.load(open(path + 'm3_atMask_MEfixed/m3_atMask_MEfixed.pkl', 'rb'))
#m5 = pickle.load(open(path + 'm5_atMask_MEfixed/m5_atMask_MEfixed.pkl', 'rb'))

    I = [p[0] for p in picks]
    dx = [p[1]*1e3 for p in picks]
    dy = [p[2]*1e3 for p in picks]

xProfs = [getLineProfile(i,1) for i in I]
yProfs = [getLineProfile(i,0) for i in I]
Nx = [np.shape(p) for p in xProfs]
Ny = [np.shape(p) for p in yProfs]

print(Nx[0][0])
for i,p in enumerate(xProfs):
    plt.plot(p,label='m = '+str(M[i]))
    plt.xticks([int(Nx[0][0]*(a/8)) for a in range(0,9)],
                [round_sig(Nx[0][0]*dx[i]*(b/8)) for b in range(-4,5)])

#plt.xlim([1000,3800])
plt.title('horizontal profiles')
plt.xlabel('Position [mm]')
plt.ylabel('Intensity [$ph/s/cm^2$]')
plt.legend()
plt.show()


for i,p in enumerate(yProfs):
    plt.plot(p,label='m = '+str(i+1))
    plt.xticks([int(Ny[0][0]*(a/10)) for a in range(0,11)],
                [round_sig(Ny[0][0]*dy[i]*(b/10)) for b in range(-5,6)])

# plt.xlim([2000,2800])
plt.title('vertical profiles')
plt.xlabel('Position [mm]')
plt.ylabel('Intensity [$ph/s/cm^2$]')
plt.legend()
plt.show()


Isum = [np.sum(i) for i in I]
Imax = [np.max(i) for i in I]


fig, ax0 = plt.subplots()
ax1 = ax0.twinx()

ax0.plot(M,Isum,'x:',color='r')
ax1.plot(M,Imax,'x:',color='b')
ax0.set_ylabel('Total Intensity')
ax0.set_xlabel('Undulator Harmonic')
ax1.set_ylabel('Peak Intensity')
ax1.spines['left'].set_color('red')
ax1.spines['right'].set_color('blue')
ax0.yaxis.label.set_color('red')
ax0.tick_params(axis='y', colors='red')
ax1.yaxis.label.set_color('blue')
ax1.tick_params(axis='y', colors='blue')
plt.show()

FWHMx, FWHMy = [],[]

for i,p in enumerate(I):
    fwhmx,fwhmy = getFWatValue(p,dx[i]*1e-3,dy[i]*1e-3)
    FWHMx.append(fwhmx)
    FWHMy.append(fwhmy)

plt.plot(M,FWHMx, 'x:', label='x')
plt.plot(M,FWHMy, 'x:', label='y')
plt.xlabel('Undulator Harmonic')
plt.ylabel('FWHM [m]')
plt.legend()
plt.show()

#fig, ax0 = plt.subplots()
#ax1 = ax0.twinx()
#
#ax0.plot(M,FWHMx,'x:',color='r')
#ax1.plot(M,Imax,'x:',color='b')
#ax0.set_ylabel('Total Intensity')
#ax0.set_xlabel('Undulator Harmonic')
#ax1.set_ylabel('Peak Intensity')
#ax1.spines['left'].set_color('red')
#ax1.spines['right'].set_color('blue')
#ax0.yaxis.label.set_color('red')
#ax0.tick_params(axis='y', colors='red')
#ax1.yaxis.label.set_color('blue')
#ax1.tick_params(axis='y', colors='blue')
#plt.show()

#plt.plot(xProfs[0])
#plt.plot()
#print(dx[0]*1e-3*1300)