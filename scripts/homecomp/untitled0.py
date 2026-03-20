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
M = [1,3,5,7,9]

save = False

E0 = 184.76
dE = 10

# save = True
# savePath = '/home/jerome/Documents/MASTERS/Figures/plots/'

# Brilliance plots
Bfiles =  ['BEUVbrilliance_m' + str(m) + '.dat' for m in M] 
for i,f in enumerate(Bfiles):
    D = np.loadtxt(dirPath+f, dtype=str, comments=None, skiprows=1)
    e = np.array(D[:,0],dtype='float')
    f = np.array(D[:,1],dtype='float')
    delta = E0*M[i] - e
    plt.plot(delta,f, label='m = ' + str(M[i]))

plt.ylabel('Brilliance [$Ph/s/.1/mr^2/mm^2$]')
plt.xlabel('Photon Energy [eV]')
plt.legend()
# if save:
#     plt.savefig(savePath + 'spectrum_{}.pdf'.format(str(f[7:len(str(f))-4])))
#     plt.savefig(savePath + 'spectrum_{}.png'.format(str(f[7:len(str(f))-4])), dpi=2000)
plt.show()            


# Flux plots
Ffiles =  ['BEUVflux_m' + str(m) + '.dat' for m in M] 
for i,f in enumerate(Ffiles):
    D = np.loadtxt(dirPath+f, dtype=str, comments=None, skiprows=1)
    e = np.array(D[:,0],dtype='float')
    f = np.array(D[:,1],dtype='float')
    delta = E0*M[i] - e
    plt.plot(delta,f, label='m = ' + str(M[i]))

plt.ylabel('Flux [$Ph/s/.1\%$]')
plt.xlabel('Photon Energy [eV]')
plt.legend()
# if save:
#     plt.savefig(savePath + 'spectrum_{}.pdf'.format(str(f[7:len(str(f))-4])))
#     plt.savefig(savePath + 'spectrum_{}.png'.format(str(f[7:len(str(f))-4])), dpi=2000)
plt.show()        


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
# if save:
#     plt.savefig(savePath + 'spectrum_{}.pdf'.format(str(f[7:len(str(f))-4])))
#     plt.savefig(savePath + 'spectrum_{}.png'.format(str(f[7:len(str(f))-4])), dpi=2000)
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
# if save:
#     plt.savefig(savePath + 'spectrum_{}.pdf'.format(str(f[7:len(str(f))-4])))
#     plt.savefig(savePath + 'spectrum_{}.png'.format(str(f[7:len(str(f))-4])), dpi=2000)
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
# if save:
#     plt.savefig(savePath + 'spectrum_{}.pdf'.format(str(f[7:len(str(f))-4])))
#     plt.savefig(savePath + 'spectrum_{}.png'.format(str(f[7:len(str(f))-4])), dpi=2000)
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
# if save:
#     plt.savefig(savePath + 'spectrum_{}.pdf'.format(str(f[7:len(str(f))-4])))
#     plt.savefig(savePath + 'spectrum_{}.png'.format(str(f[7:len(str(f))-4])), dpi=2000)
plt.show()   