#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 10 14:13:37 2025

@author: -
"""
import numpy as np
import matplotlib.pyplot as plt

import interferenceGratingModelsJK as interferenceGratingModelsJK

def aerialImageDistance(d,p,m,wl):
    z = (d*np.sqrt((p**2) - ((m**2)*(wl**2))))/(2*m*wl)
    return z

def diffractionAngle(wl, p, phi=0, m = 1):
    # Use grating equation to determine diffraction angle  
    # (m = order; l = lambda, wavelength; d = spacing)
    theta = np.arcsin(np.sin(phi) + m*wl/p)
    return theta

def aerialImageITE(E1a,E2a,E3,E1p,E2p,k,theta,x,z,show=True):
    
    E1 = E1a * np.exp(1j * ((k * x * np.sin(theta)) - (k * z * np.cos(theta))) - E1p)
    E2 = E2a * np.exp(1j * ((-k * x * np.sin(theta)) - (k * z * np.cos(theta))) - E2p)
    
    
    E = E1 + E2 + E3
    
    I = abs(E)**2
    
    if show:
        plt.plot([a*1e9 for a in x],I)
        # plt.plot([a*1e9 for a in x],abs(E3)**2)
        # plt.plot([a*1e9 for a in x],np.angle(E3)/np.pi)
        plt.xlabel('x [nm]')
        plt.ylabel('I [a.u]')
        # plt.ylim(0,1)
        plt.show()
    
    return I


c = 299792458
E10 = 0.50    # E10 + E20 = 1.0
E20 = 0.50 
E30 = 0.2#np.linspace(0.01,0.03,500)#0.05 #0.83 #75/100 # value of transmission through mask in Masters thesis
E1p = 0 * 1/2 * np.pi
E2p = 0*np.pi
E3p = 0.8*np.pi
wl = 6.7e-9 # 13.5e-9 #6.7e-9
k = (2*np.pi)/wl
p = 100.0e-9
theta = diffractionAngle(wl,p)
w=c*k#1/wl

Show = True

xR = 0.5e-6
xN = 5000

x = np.linspace(-xR/2,xR/2,xN)

z = aerialImageDistance(100e-6, p=p, m=1, wl=wl)
t =  0*z/c
# Wo = 10.0e-6
Wz = 10.0e-3   #beam size at z (1/e^2)
R = 25.0         #radius of curvature
Z = 9.5          #propagation distance from waist

ratio_sum = E10 + E20
E1a = E10 / ratio_sum * (1 - E30)
E2a = E20 / ratio_sum * (1 - E30)
E3a = E30

E3 = E3a * np.exp((-(x**2))/((Wz**2))) * np.exp(-1j * ((k*Z) + (k * ((x**2)/(2*R))) - E3p))

Ib1d = aerialImageITE(E1a, E2a, E3, E1p, E2p, k, theta, x, z,show=Show)
Ib = np.tile(Ib1d,(4,1))
threshold = np.mean(Ib)

plt.plot(Ib1d)
plt.hlines(y=threshold,xmin=0,xmax=5000)
plt.show()

plt.imshow(Ib,aspect='auto')
plt.show()


m2D = interferenceGratingModelsJK.gratingContrastMichelson(Ib)
c2D = interferenceGratingModelsJK.meanDynamicRange(Ib)

# NILS = interferenceGratingModelsJK.NILS(Ib,x,w=p/4,show=True) 
LW = interferenceGratingModelsJK.LWR_JK(Ib,x, w=p/4, debug=True) 
# for e, i in enumerate(images):
#     iP = [i[:,a] for a in range(0,np.shape(i)[1])]
#     print("shape:", np.shape(iP))
#     plt.plot(xP[e]*1e9,[p for p in iP])
#     plt.xlim(-plotRange,plotRange)
#     plt.title(labels[e])
#     plt.show()
   
#     m2D = [interferenceGratingModels.gratingContrastMichelson(p) for p in iP]
#     m2D = np.mean(m2D)
#     M2D.append(m2D)
    
#     c2D =  [interferenceGratingModels.meanDynamicRange(p) for p in iP]
#     c2D = np.mean([c[0] for c in c2D])
#     C2D.append(c2D)
    
#     print('e: ', e)
#     NILS2D = np.array([interferenceGratingModelsJK.NILS(ip,xP[e], pitch/4, show=False) for ip in np.transpose(np.array(iP))])
 
#     FOURIERC2D  = [interferenceGratingModelsJK.gratingContrastFourier(ip,x*1e6, show=False) for ip, x in zip(iP,xP)]
#     #FOURIERC2D = [[0,1] for ip, x in zip(iP,xP)]
#     fC = np.mean([f[0] for f in FOURIERC2D])
   
#     NNILS = [len(a) for a in NILS2D[:,2]]
#     print(NILS2D[:,9][0:np.min(NNILS)-1])
#     NILS   = [a[0:np.min(NNILS)-1] for a in NILS2D[:,2]]
#     NILS3s = NILS2D[:,9][0:np.min(NNILS)-1] #[a[0:np.min(NNILS)-1] for a in NILS2D[:,9]]
#     NILSrmsd = NILS2D[:,8][0:np.min(NNILS)-1] #[a[0:np.min(NNILS)-1] for a in NILS2D[:][8]]
#     #LW     = [a[0:np.min(NNILS)-1] for a in NILS2D[:,3]]
   
#     #NILS = np.stack(NILS2D[:,2])
   
 
#     stdNILS = np.std(NILS)/np.mean(NILS)
#     rmsNILS = np.sqrt(np.mean(np.square(NILS)))
#     #rmsdNILS =
   
   
#     # THis is the 2D NILS distribution
#     plt.imshow(NILS)
#     plt.title('NILS - 2D dist')
#     plt.colorbar()
#     plt.show()
   
#     plt.plot(np.mean(NILS,axis=0))
#     plt.title('NILS - 1D dist')
#     plt.show()
 
#     avNILS = np.mean(NILS)

#     nils3s.append(NILS3s)
#     nilsrmsD.append(NILSrmsd)
#     fourierC2d.append(fC)
#     nils2d.append(avNILS)
#     nils2dRMS.append(rmsNILS)
#     nilsSTD.append(stdNILS)

# LW = [interferenceGratingModelsJK.LWR(i,xP[e], pitch/4, debug=False) for i in images]
# #disable LWR for speed - testing Fourier
# #LW = [[[0], 0, 0, 0] for i in images]
   
# michelsonC2d = [interferenceGratingModels.gratingContrastMichelson(i) for i in images]
# rmsC2d = [interferenceGratingModels.gratingContrastRMS(i) for i in images]
# compositeC2d = [interferenceGratingModels.meanDynamicRange(i) for i in images] #, mdrC, imbalanceC
# #        nilsC2d = [interferenceGratingModels.NILS(i,x, pitch/4, show=False) for i, x in zip(images, xP)]
# #fourierC2d = [interferenceGratingModels.gratingContrastFourier(i,x*1e6, show=False) for i, x in zip(images,xP)] #Cf,  Am, Fr, peakFr - Still unsure but seems good
# fidel2d = [interferenceGratingModelsJK.fidelity(i,I2d) for i in images]   # fidelity based on comparison to model

# # NILS mean: 1.2224229538022116
# # NILS rms: 1.3071862846507827
# # LW mean: 2.505449312098684e-08
# # LW rms: 2.5600423059289736e-08
# # LW rmsd: 5.258710418442611e-09
# # NILS mean: 1.206876656717402
# # NILS rms: 1.296013808543514
# # LW mean: 2.505449312098684e-08
# # LW rms: 2.5608638698179333e-08
# # LW rmsd: 5.298561165477978e-09
# # This is is line width error
   
# #        LWlist = [np.array(f[0]).flatten() for f in LW]
# #        plt.imshow(LW)
# #        plt.colorbar()
# #        plt.title('LW')
# #        plt.show()
   
lwRMS = LW[1]
plt.plot(lwRMS,'X')
plt.title('LW rms')
plt.show()
   
LWmean = np.mean(LW[0])
plt.plot(LW[0])
# plt.plot(LWmean,'X')
plt.title('LW')
plt.show()
   
 
dlwRMS = LW[2]
plt.plot(dlwRMS,'X')
plt.title('LW rmsd')
plt.show()

LWR = LW[3]
plt.plot(LWR,'X')
plt.title('LWR')
plt.show()
   
   


# minLen = np.min([len(a[0]) for a in LW])
# LW2d = np.stack([f[0][0:minLen] for f in LW])
# plt.imshow(LW2d,aspect=11)
# plt.show()
# stepy = 2.658184246878093e-07

# # Ca, Cb = [],[]
# # MA, MB = [],[]
# for e in range(0,500):
    
#     ratio_sum = E10 + E20
#     E1a = E10 / ratio_sum * (1 - E30[e])
#     E2a = E20 / ratio_sum * (1 - E30[e])
#     E3a = E30[e]

#     E3 = E3a * np.exp((-(x**2))/((Wz**2))) * np.exp(-1j * ((k*Z) + (k * ((x**2)/(2*R))) - E3p))

#     Ib = aerialImageITE(E1a, E2a, E3, E1p, E2p, k, theta, x, z,show=Show)
#     # 