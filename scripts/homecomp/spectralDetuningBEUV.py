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

E0 = 184.76
dE = 10

# save = True
# savePath = '/home/jerome/Documents/MASTERS/Figures/plots/'


# Div X plots
Dxfiles =  ['BEUVxDiv_m' + str(m) + '.dat' for m in M] 
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
    plt.savefig(savePath + 'BEUV_xDiv.png')
plt.show()   

# Div Y plots
Dyfiles =  ['BEUVyDiv_m' + str(m) + '.dat' for m in M] 
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
    plt.savefig(savePath + 'BEUV_yDiv.png')
plt.show()   


# Beam Size X plots
Sxfiles =  ['BEUVxSize_m' + str(m) + '.dat' for m in M] 
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
    plt.savefig(savePath + 'BEUV_xSize.png')
plt.show()   

# Beam Size Y plots
Syfiles =  ['BEUVySize_m' + str(m) + '.dat' for m in M] 
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
    plt.savefig(savePath + 'BEUV_ySize.png')
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

Ffiles =  ['BEUVflux_m' + str(m) + '.dat' for m in M] 
F, _DELTA = [],[]
for i,f in enumerate(Ffiles):
    D = np.loadtxt(dirPath+f, dtype=str, comments=None, skiprows=1)
    e = np.array(D[:,0],dtype='float')
    f = np.array(D[:,1],dtype='float')
    delta = E0*M[i] - e
    plt.plot(delta,f, label='m = ' + str(M[i]))
    
    F.append(f)
    _DELTA.append(delta)

plt.ylabel('Flux [$Ph/s/.1\%$]')
plt.xlabel('Photon Energy [eV]')
plt.legend()
if save:
    plt.savefig(savePath + 'BEUV_flux.png')
# plt.show()        


#Finding flux difference with no detuning
_x0 = _DELTA[0][np.where(abs(_DELTA[0])==abs(_DELTA[0]).min())]
F0 = F[0][np.where(abs(_DELTA[0])==abs(_DELTA[0]).min())]
Fdif_0 = [b[np.where(abs(_DELTA[0])==abs(_DELTA[0]).min())] / F0 for b in F[1::]]

plt.axvline(x=_x0, linestyle=':',color='black')
plt.text(x=_x0-2.5, y=0.0, s='E=' + str(E0),fontsize=6)
for i,bd in enumerate(Fdif_0):
    plt.text(x=_x0-10,y=(F0/10)*(i+9),s='$F_0 (m= $' + str(M[i+1]) + ') = ' + str(round_sig(bd)) + '$F_0 (m=1)$',fontsize=6)

#Finding flux difference at m=1 peak
xp = _DELTA[0][np.where(F[0] == F[0].max())]
Fp = F[0][np.where(F[0] == F[0].max())]
Fdif_p = [b[np.where(F[0] == F[0].max())] / Fp for b in F[1::]]

plt.axvline(x=xp, linestyle=':',color='gray')
plt.text(x=xp-2.5, y=0.0, s='E=' + str(round_sig(E0 + xp,5)),fontsize=6,color='gray')
for i,bd in enumerate(Fdif_p):
    plt.text(x=_x0-10,y=(F0/10)*(i+4),s='$F_p (m= $' + str(M[i+1]) + ') = ' + str(round_sig(bd)) + '$F_p (m=1)$',fontsize=6,color='gray')
    
#Finding optimal difference with F(m=1) >= F0(m=1)
Fdif = [b / F[0] for b in F[1::]]
Fdifmean = np.mean(Fdif,axis=0)
Fdif_acceptable = Fdifmean[np.where(F[0] >= F0)]
xbest = _DELTA[0][np.where(Fdifmean == Fdif_acceptable.min())] #_DELTA[0][np.where(F[0] >= F0)]
Fbest = F[0][np.where(_DELTA[0] == xbest)]
Fdif_best = [b[np.where(F[0] == Fbest)] / Fbest for b in F[1::]]

plt.axvline(x=xbest, linestyle=':',color='blue')
plt.text(x=_x0+xbest+0.1, y=0.5e9, s='E=' + str(round_sig(E0 + xbest,5)),fontsize=6,color='blue')
for i,bd in enumerate(Fdif_best):
    plt.text(x=xp+1,y=(F0/10)*(i+8),s='$F(m= $' + str(M[i+1]) + ') = ' + str(round_sig(bd)) + '$F(m=1)$',fontsize=6,color='blue')

# bestEnergy = DELTA[0][np.where(Bdifmean == Bdifmean.min())]
# plt.axvline(x=bestEnergy, linestyle=':',color='black')
# plt.text(x=1,y=0.2e13,s='E = ' + str(bestEnergy) + ' eV')
plt.show()            


B = []
DELTA = []

# Brilliance plots
Bfiles =  ['BEUVbrilliance_m' + str(m) + '.dat' for m in M] 
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
    plt.savefig(savePath + 'BEUV_brilliance.png')
    
#Finding brilliance difference with no detuning
x0 = DELTA[0][np.where(abs(DELTA[0])==abs(DELTA[0]).min())]
B0 = B[0][np.where(abs(DELTA[0])==abs(DELTA[0]).min())]
Bdif_0 = [b[np.where(abs(DELTA[0])==abs(DELTA[0]).min())] / B0 for b in B[1::]]

plt.axvline(x=x0, linestyle=':',color='black')
plt.text(x=x0-2.5, y=0.0, s='E=' + str(E0),fontsize=6)
for i,bd in enumerate(Bdif_0):
    plt.text(x=x0-10,y=(B0/6)*(i+15),s='$B_0 (m= $' + str(M[i+1]) + ') = ' + str(round_sig(bd)) + '$B_0 (m=1)$',fontsize=6)

#Finding brilliance difference at m=1 peak
xp = DELTA[0][np.where(B[0] == B[0].max())]
Bp = B[0][np.where(B[0] == B[0].max())]
Bdif_p = [b[np.where(B[0] == B[0].max())] / Bp for b in B[1::]]

plt.axvline(x=xp, linestyle=':',color='gray')
plt.text(x=x0+0.1, y=0.25e13, s='E=' + str(round_sig(E0 + xp,5)),fontsize=6,color='gray')
for i,bd in enumerate(Bdif_p):
    plt.text(x=x0-10,y=(B0/6)*(i+10),s='$B_p (m= $' + str(M[i+1]) + ') = ' + str(round_sig(bd)) + '$B_p (m=1)$',fontsize=6,color='gray')
    
#Finding optimal difference with B(m=1) >= B0(m=1)
Bdif = [b / B[0] for b in B[1::]]
Bdifmean = np.mean(Bdif,axis=0)
Bdif_acceptable = Bdifmean[np.where(B[0] >= B0)]
xbest = DELTA[0][np.where(Bdifmean == Bdif_acceptable.min())] #DELTA[0][np.where(B[0] >= B0)]
Bbest = B[0][np.where(DELTA[0] == xbest)]
Bdif_best = [b[np.where(B[0] == Bbest)] / Bbest for b in B[1::]]

plt.axvline(x=xbest, linestyle=':',color='blue')
plt.text(x=x0+xbest+0.1, y=0.5e13, s='E=' + str(round_sig(E0 + xbest,5)),fontsize=6,color='blue')
for i,bd in enumerate(Bdif_best):
    plt.text(x=x0-10,y=(B0/6)*(i+5),s='$B(m= $' + str(M[i+1]) + ') = ' + str(round_sig(bd)) + '$B(m=1)$',fontsize=6,color='blue')

# bestEnergy = DELTA[0][np.where(Bdifmean == Bdifmean.min())]
# plt.axvline(x=bestEnergy, linestyle=':',color='black')
# plt.text(x=1,y=0.2e13,s='E = ' + str(bestEnergy) + ' eV')
plt.show()            