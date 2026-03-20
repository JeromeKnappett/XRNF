#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  2 11:29:21 2023

@author: jerome
"""

import numpy as np
import matplotlib.pyplot as plt
import imageio

def round_sig(x, sig=2):
    from math import floor, log10
    if x != 0:
        return round(x, sig-int(floor(log10(abs(x))))-1)
    else:
        return x
    
colours = plt.rcParams["axes.prop_cycle"].by_key()["color"]

dirPath = '/home/jerome/dev/data/spectralDetuning/' 
savePath = dirPath
M = [1,3,5,7,9]

save = True

E0 = 90.44
dE = 10

# save = True
# savePath = '/home/jerome/Documents/MASTERS/Figures/plots/'


# Div X plots
Dxfiles =  ['EUVxDiv_m' + str(m) + '.dat' for m in M] 
for i,f in enumerate(Dxfiles):
    D = np.loadtxt(dirPath+f, dtype=str, comments=None, skiprows=1)
    e = np.array(D[:,0],dtype='float')
    f = np.array(D[:,1],dtype='float')
    delta = E0*M[i] - e
    plt.plot(delta,f, label='m = ' + str(M[i]))

plt.ylabel('Horizontal Divergence [rad]')
plt.xlabel('Photon Energy [eV]')
plt.legend()
if save:
    plt.savefig(savePath + 'EUV_xDiv.png')
plt.show()   

# Div Y plots
Dyfiles =  ['EUVyDiv_m' + str(m) + '.dat' for m in M] 
for i,f in enumerate(Dyfiles):
    D = np.loadtxt(dirPath+f, dtype=str, comments=None, skiprows=1)
    e = np.array(D[:,0],dtype='float')
    f = np.array(D[:,1],dtype='float')
    delta = E0*M[i] - e
    plt.plot(delta,f, label='m = ' + str(M[i]))

plt.ylabel('Vertical Divergence [rad]')
plt.xlabel('Photon Energy [eV]')
plt.legend()
if save:
    plt.savefig(savePath + 'EUV_yDiv.png')
plt.show()   


# Beam Size X plots
Sxfiles =  ['EUVxSize_m' + str(m) + '.dat' for m in M] 
for i,f in enumerate(Sxfiles):
    D = np.loadtxt(dirPath+f, dtype=str, comments=None, skiprows=1)
    e = np.array(D[:,0],dtype='float')
    f = np.array(D[:,1],dtype='float')
    delta = E0*M[i] - e
    plt.plot(delta,f, label='m = ' + str(M[i]))

plt.ylabel('Horizontal Beam Size [m]')
plt.xlabel('Photon Energy [eV]')
plt.legend()
if save:
    plt.savefig(savePath + 'EUV_xSize.png')
plt.show()   

# Beam Size Y plots
Syfiles =  ['EUVySize_m' + str(m) + '.dat' for m in M] 
for i,f in enumerate(Syfiles):
    D = np.loadtxt(dirPath+f, dtype=str, comments=None, skiprows=1)
    e = np.array(D[:,0],dtype='float')
    f = np.array(D[:,1],dtype='float')
    delta = E0*M[i] - e
    plt.plot(delta,f, label='m = ' + str(M[i]))

plt.ylabel('Vertical Beam Size [m]')
plt.xlabel('Photon Energy [eV]')
plt.legend()
if save:
    plt.savefig(savePath + 'EUV_ySize.png')
plt.show()   




# dif = [b-B[0] for b in B[1::]]
# print(np.shape(dif))
# meanDif = np.mean(dif,axis=0)
# bestEnergy = DELTA[0][np.where(meanDif == meanDif.max())]
# for i,d in enumerate(dif):
#     plt.plot(DELTA[0],d,label='m = ' + str(2*i+3)) 
#     index = np.where(d == d.max())
#     print(DELTA[0][index])
# plt.plot(DELTA[0],meanDif, label='mean')
# plt.axvline(x=bestEnergy, linestyle=':',color='black')
# plt.text(x=1,y=0.2e13,s='E = ' + str(bestEnergy) + ' eV')
# plt.legend()
# plt.show()


# Flux plots
Ffiles =  ['EUVflux_m' + str(m) + '.dat' for m in M] 
for i,f in enumerate(Ffiles):
    D = np.loadtxt(dirPath+f, dtype=str, comments=None, skiprows=1)
    e = np.array(D[:,0],dtype='float')
    f = np.array(D[:,1],dtype='float')
    delta = E0*M[i] - e
    plt.plot(delta,f, label='m = ' + str(M[i]))

plt.ylabel('Flux [$Ph/s/.1\%$]')
plt.xlabel('Photon Energy [eV]')
plt.legend()
if save:
    plt.savefig(savePath + 'EUV_flux.png')
plt.show()        



B = []
DELTA = []

# Brilliance plots
Bfiles =  ['EUVbrilliance_m' + str(m) + '.dat' for m in M] 
for i,f in enumerate(Bfiles):
    D = np.loadtxt(dirPath+f, dtype=str, comments=None, skiprows=1)
    e = np.array(D[:,0],dtype='float')
    f = np.array(D[:,1],dtype='float')
    delta = E0*M[i] - e

    B.append(f)
    DELTA.append(delta)
    
    plt.plot(delta,f, label='m = ' + str(M[i]))

plt.ylabel('Brilliance [$Ph/s/.1/mr^2/mm^2$]')
plt.xlabel('Photon Energy [eV]')
plt.legend()
if save:
    plt.savefig(savePath + 'EUV_brilliance.png')
    
#Finding brilliance difference with no detuning
x0 = DELTA[0][np.where(abs(DELTA[0])==abs(DELTA[0]).min())]
B0 = B[0][np.where(abs(DELTA[0])==abs(DELTA[0]).min())]
Bdif_0 = [b[np.where(abs(DELTA[0])==abs(DELTA[0]).min())] / B0 for b in B[1::]]

plt.axvline(x=x0, linestyle=':',color='black')
plt.text(x=x0-2.0, y=-0.025e13, s='E=' + str(E0),fontsize=6)
for i,bd in enumerate(Bdif_0):
    plt.text(x=x0-12,y=(B0/4)*(i+12),s='$B_0 (m=$' + str(M[i+1]) + ') = ' + str(round_sig(bd)) + '$B_0 (m=1)$',fontsize=6)

#Finding brilliance difference at m=1 peak
xp = DELTA[0][np.where(B[0] == B[0].max())]
Bp = B[0][np.where(B[0] == B[0].max())]
Bdif_p = [b[np.where(B[0] == B[0].max())] / Bp for b in B[1::]]

plt.axvline(x=xp, linestyle=':',color='gray')
plt.text(x=x0+1.1, y=0.0, s='E=' + str(round_sig(E0 + xp,5)),fontsize=6,color='gray')
for i,bd in enumerate(Bdif_p):
    plt.text(x=x0-12,y=(B0/4)*(i+7),s='$B_p (m=$' + str(M[i+1]) + ') = ' + str(round_sig(bd)) + '$B_p (m=1)$',fontsize=6,color='gray')
    
#Finding optimal difference with B(m=1) >= B0(m=1)
Bdif = [b / B[0] for b in B[1::]]
Bdifmean = np.mean(Bdif,axis=0)
Bdif_acceptable = Bdifmean[np.where(B[0] >= B0)]
xbest = DELTA[0][np.where(Bdifmean == Bdif_acceptable.min())] #DELTA[0][np.where(B[0] >= B0)]
Bbest = B[0][np.where(DELTA[0] == xbest)]
Bdif_best = [b[np.where(B[0] == Bbest)] / Bbest for b in B[1::]]

plt.axvline(x=xbest, linestyle=':',color='blue')
plt.text(x=x0+xbest+0.1, y=0.1e13, s='E=' + str(round_sig(E0 + xbest,5)),fontsize=6,color='blue')
for i,bd in enumerate(Bdif_best):
    plt.text(x=x0-12,y=(B0/4)*(i+2),s='$B(m=$' + str(M[i+1]) + ') = ' + str(round_sig(bd)) + '$B(m=1)$',fontsize=6,color='blue')

# bestEnergy = DELTA[0][np.where(Bdifmean == Bdifmean.min())]
# plt.axvline(x=bestEnergy, linestyle=':',color='black')
# plt.text(x=1,y=0.2e13,s='E = ' + str(bestEnergy) + ' eV')
plt.show()            
