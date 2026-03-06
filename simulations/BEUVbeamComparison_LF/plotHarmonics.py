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

def transmission(wl,T,beta):
    k = (2*np.pi) / wl
    trans = np.exp((-2*k * beta * T)) # np.exp(((-k) / (beta * T))) # changed to -2k from -1k by JK - 29/10/24
    return trans

path = '/user/home/opt/xl/xl/experiments/BEUVbeamComparison_LF/data/'

filePaths = ['atMask_cff2offset0_m1','atMask_cff2offset0_m2']
# ['atMask_cff1.4offset0_m1_roughM','atMask_cff1.4offset0_m2_roughM','atMask_cff1.4offset0_m3_roughM']
# ['atMask_cff2offset0_m1','atMask_cff2offset0_m2']

M = [1,2,3] #3,5]#,7,9]
numPoints = 1000

SE_ME = 'ME'

# if SE_ME == 'SE':
# #    I = [tifffile.imread(path + 'm' + str(m) + '_atMask_SE/intensity.tif')
#     wPath = [path + 'm' + str(m) + '_atMask_SE_tuned/wf_final.hdf' for m in M]
#     I = []
#     dx,dy = [], []
#     for p in wPath:
#         wf = Wavefront()
#         wf.load_hdf5(p)
#         [nx, ny, xmin, xmax, ymin, ymax] = get_mesh(wf)
#         dX, dY = (xmax-xmin)/nx, (ymax-ymin)/ny
# #        print('Mesh grid period: {}x{}'.format(dX,dY))
        
#         I.append(wf.get_intensity())
#         dx.append(dX)
#         dy.append(dY)

if SE_ME == 'ME':
    picks = [pickle.load(open(path + f + '/' + f + '.pkl', 'rb')) for f in filePaths] 
    #[pickle.load(open(path + 'm' + str(m) + '_atMask_ME/m' + str(m) + '_atMask_ME.pkl', 'rb')) for m in M]
#m1 = pickle.load(open(path + 'm1_atMask_MEfixed/m1_atMask_MEfixed.pkl', 'rb'))
#m3 = pickle.load(open(path + 'm3_atMask_MEfixed/m3_atMask_MEfixed.pkl', 'rb'))
#m5 = pickle.load(open(path + 'm5_atMask_MEfixed/m5_atMask_MEfixed.pkl', 'rb'))

    I = [p[0] for p in picks]
    dx = [p[1]*1e3 for p in picks]
    dy = [p[2]*1e3 for p in picks]
    
    print(dx)
    print(dy)

import xraydb

hN = 3
CF = 'C3H6' # chemical formula for ultralene
beta1,beta2 = [],[]
T1,T2 = [],[]

CF2 = 'C2H4'
R = 4/4
T = 4.064e-6
DPE = 0.96
TPP = R*T
TPE = T - TPP#(1-R)*T
        
        
(d1,b1,atlen1) = xraydb.xray_delta_beta(CF, 0.855, 184.75) # density obtained from .... add ref
(d1,b2,atlen1) = xraydb.xray_delta_beta(CF, 0.855, 184.75*3) # density obtained from .... add ref
# beta1.append(b1)
# (d1,bw1,atlen1) = xraydb.xray_delta_beta(CF2, DPE, 184.76)
# beta1.append(bw1)
        
tran1 = transmission((4.135667696e-15 * 299792458) / 184.76,TPP,b1)
tran2 = transmission((4.135667696e-15 * 299792458) / (3*184.76),TPP,b2)


    
            # (d2,b2,atlen2) = xraydb.xray_delta_beta(CF,0.855,int(e)*hN)
            # beta2.append(b2)
            # (d2,bw2,atlen2) = xraydb.xray_delta_beta(CF2,DPE,int(e)*hN)
            # beta2.append(bw2)
            # # (d3,b3,atlen3) = xraydb.xray_delta_beta(CF,0.855,int(e)*3)
            # # beta2.append(b2)
            
            # wl1 = (4.135667696e-15 * 299792458) / e
            # wl2 = (4.135667696e-15 * 299792458) / (hN*e)
            # # wl3 = (4.135667696e-15 * 299792458) / (3*e)
            
            # # print('\n')
            # # print(wl1, wl2)
            # tran1 = transmission(wl1,TPP+extraCT,b1)
            # tran2 = transmission(wl2,TPP+extraCT,b2)
            # tranW1 = transmission(wl1,TPE,bw1)
            # tranW2 = transmission(wl2,TPE,bw2)
            
            
                    
            # # converting from ph/s/cm^2 (at fundamental energy) to ph/s
            # i1 = io.imread(fitFolder + sortedH1[i])*10000*(11.0e-6 * 11.0e-6)
            # i3 = io.imread(fitFolder + sortedH3[i])*10000*(11.0e-6 * 11.0e-6)
            # # converting from ph/s (at fundamental energy) to counts at detector
            # i1 = photonsPs2counts(i1, energy_range[i], t=exposure_time, conversion=1.27)
            # i3 = photonsPs2counts(i3, energy_range[i], t=exposure_time, conversion=1.27)
            # # converting from counts to ph/s and accounting for transmission through ultralene filter
            # i1 = counts2photonsPs(i1,energy_range[i],t=exposure_time,conversion=1.27) / T1[i]
            # i3 = counts2photonsPs(i3,energy_range[i]*hN,t=exposure_time,conversion=1.27) / T2[i]
            
            

xProfs = [getLineProfile(i*tran1,1) for i in I]
yProfs = [getLineProfile(i*tran2,0) for i in I]

Nx = [np.shape(p) for p in xProfs]
Ny = [np.shape(p) for p in yProfs]

print(Nx)

Rx = [d*n[0] for d,n in zip(dx,Nx)]
Ry = [d*n[0] for d,n in zip(dy,Ny)]

X = [np.linspace(-r/2,r/2,n[0]) for r,n in zip(Rx,Nx)]
Y = [np.linspace(-r/2,r/2,n[0]) for r,n in zip(Ry,Ny)]

print(Nx[0][0])
for i,p in enumerate(xProfs):
    plt.plot(X[i],p,label='m = '+str(i+1))
    # plt.xticks([int(Nx[0][0]*(a/8)) for a in range(0,9)],
    #             [round_sig(Nx[0][0]*dx[i]*(b/8)) for b in range(-4,5)])
plt.plot(X[0],[x1+x2 for x1,x2 in zip(xProfs[0],xProfs[1])],label='sum')
plt.xlim([-10,10])
plt.title('horizontal profiles')
plt.xlabel('Position [mm]')
plt.ylabel('Intensity [$ph/s/cm^2$]')
plt.legend()
plt.show()


for i,p in enumerate(yProfs):
    plt.plot(Y[i],p,label='m = '+str(i+1))
    # plt.xticks([int(Ny[0][0]*(a/30)) for a in range(0,31)],
    #             [round_sig(Ny[0][0]*dy[i]*(b/30)) for b in range(-15,16)])

# plt.xlim([2000,2800])
plt.plot(Y[0],[x1+x2 for x1,x2 in zip(yProfs[0],yProfs[1])],label='sum')
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