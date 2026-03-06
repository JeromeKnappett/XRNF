#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  4 13:34:24 2025

@author: -
"""

import numpy as np
import matplotlib.pyplot as plt
# import imageio
import tifffile
import pickle
from mpl_toolkits.axes_grid1.axes_divider import make_axes_locatable
# from mpl_toolkits.axes_grid1.colorbar import colorbar
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
# from useful import round_sig, getLineProfile
from math import floor, log10

colours = plt.rcParams["axes.prop_cycle"].by_key()["color"]

from matplotlib import rcParams
rcParams['figure.figsize']=(8,6)
rcParams['figure.dpi']=500
rcParams.update({'font.size': 15})

def rejectOutliers(data, m=2.0):
    d = np.abs(data - np.median(data))
    mdev = np.median(d)
    s = d/mdev if mdev else np.zeros(len(d))
    return data[s<m]

def round_sig(x, sig=2):
    from math import log10, floor
    if x != 0:
        return round(x, sig-int(floor(log10(abs(x))))-1)
    else:
        return x
    # %%
dirPath = '/user/home/opt/xl/xl/experiments/BEUVcoherence/data/'
files = ['dataStructure_350um.pkl',]#,'D_27.5um/dataStructure.pkl']# ['contrastMetrics_maskLER_retry_2d.pkl']#,'contrastMetrics350_2d.pkl']
labelX = '$LER$ [um]'#'$\sigma [nm]$'
labelY = ['$C_M$',    #0 # global measure
          '$C_M$',    #1 # line-by-line average
          '$C_{RMS}$',#2
          '$C_c$',    #3 # global
          '$C_c$',    #4 # l-b-l
          '1 - Fidelity', #5
          'NILS / $\pi$',     #6 
          'NILS$_{\sigma} / \pi$', #7 
          'NILS$_{\sigma_n} / \pi$', #8
          'LWR [nm]', #9
          # 'LER [nm]', #10
          '$\eta_{AE}$', # 11
          '$\eta_{0}$'  #12
          ] 

# dataStructure = [sigma, #cY,
#                  michelsonC2d,M2D,
#                  rmsC2d,
#                  compositeC2d,C2D,
#                  fidel2d,
#                  nils2d,
#                  nilsSTD,
#                  nilsrmsD,
#                  LW, # changed to LW from LWR - may cause issues with plotting
#                  E1,
#                  E0]

# ['$1 - Fidelity$', '$C_M$', '$C_{RMS}$', '$C_{Composite}$', '$NILS_{mean}$', '$NILS_{\sigma_n}$', '$LWR$']
# labelY = ['$1 - Fidelity$', '$C_M$', '$C_{RMS}$', '$C_{Composite}$', '$NILS_{mean}$', '$LWR$']
# legend = ['$c_y  = 2$','$c_y = 4$','$c_y = 6$','$c_y = 8$','$c_y = 10$']

# pickle.dump([labels,michelsonC2d,rmsC2d,compositeC2d,fidel2d,nils2d,nilsSTD,LWR], f)
savePath = None#'/home/jerome/dev/data/correctedRoughness/contrastWithoutLWR.png'
LERpick = pickle.load(open(dirPath + 'LER__BEUVcoherence_350SSA.pkl', 'rb'))
pick1 = pickle.load(open(dirPath + files[0], 'rb'))
# pick2 = pickle.load(open(dirPath + files[1], 'rb'))

print(LERpick[0])
# print(pick1)
A1 = [p for p in pick1[1::]]
# A2 = [p for p in pick2[1::]]
# [[1 - p for p in pick[5]], pick[2], pick[3], pick[4], pick[6], pick[7], pick[8]]
# A = [[1 - p for p in pick[5]], pick[2], pick[3], pick[4], pick[6], pick[8]]
# X1 = [0.0,0.5,1.0,1.5,2.0,2.5,3.0,3.5,4.0] #[float(p[4:-4]) for p in pick1[0]]
# X2 = [int(p[:-3]) for p in pick2[0]]
LERa = [0.0,
        3.7249164431850543,
        4.536853502343667,
        5.518446489820692,
        6.4970478648742045]
LERc = [0.0,62.5,61.0,58.6,57.6]
print(pick1[0])
X1 = LERa
# fig,ax= plt.subplots(3,3)

    # dataStructure = [sigma, #cY,
    #                  michelsonC2d,rmsC2d,[c[0] for c in compositeC2d],
    #                   fidel2d,
    #                   nils2d,
    #                   nilsSTD,
    #                   LWR,
    #                   E1]
    

print('Michelson Contrast:')
print(A1[0])
print('Michelson Contrast:')
print(A1[1])
print('Composite Contrast:')
print(A1[3])
print('Composite Contrast:')
print(A1[4])
print('LER')
print(LERpick[1])
print('LWR')
print([a[3] for a in A1[9]])
print('NILS')
print(A1[6])
# print('EF')
# print(A1[10])
# print('EF0')
# print(A1[11])


LWR = [l[3] for l in A1[9]]
CDU = [l[4] for l in A1[9]]
CLR = [l[5] for l in A1[9]]

print('CDU')
print(CDU)
print('CLR')
print(CLR)
# for i,a in enumerate(A1[9]):
#     print('n: ', i)
#     lw = rejectOutliers(np.array(a[0]))
#     LW = np.mean(lw)
#     print('lw: ', LW)
#     LWd = [abs(b - LW) for b in lw]
#     # print(LWd)
#     lwr = 3*np.std(LWd)
#     print(np.shape(lwr))
#     print(lwr)
#     LWR.append(lwr)
#     plt.plot(LWd)#[0:100])
#     plt.show()
# print(LWR)
# LWR = [3 * (np.std(a[0])/np.mean(a[0])) for a in A1[9]]

# LWd = [abs(np.mean(a[0]) - b) for b in a for a in A1[9]]
fig,ax = plt.subplots(3,3)

ax[0,0].plot(X1,A1[0],'x:',color='black',label='50 um')
ax[0,0].set_ylabel(labelY[0])
# ax[0,0].vlines(5,ymin=np.min(A1[0]),ymax=np.max(A1[0]), color='r', linestyle=':')
# ax[0,0].plot(X2,A2[0],'x:',label='350 um')
ax[0,1].plot(X1,[a / 0.6 for a in A1[3]],'x:',color='black',label='50 um')
ax[0,1].set_ylabel(labelY[3])
# ax[0,1].vlines(5,ymin=np.min(A1[2])*0.6,ymax=np.max(A1[2])*0.6, color='r', linestyle=':')
# ax[0,1].vlines(5,ymin=np.min(A1[3])/0.6,ymax=np.max(A1[3])/0.6, color='r', linestyle=':')
# ax[0,1].plot(X2,[a[0] / 0.6 for a in A2[2]],'x:',label='350 um')
ax[0,2].plot(X1,[a/np.pi for a in A1[6]],'x:',color='black',label='50 um')
ax[0,2].set_ylabel(labelY[6])
# ax[0,2].vlines(5,ymin=np.min(A1[6])/np.pi,ymax=np.max(A1[6])/np.pi, color='r', linestyle=':')
# ax[0,3].plot(X1,[a for a in A1[4]],'x:',label='50 um')
# ax[0,3].set_ylabel(labelY[4])
# ax[0,2].plot(X2,[1 - a for a in A2[3]],'x:',label='350 um')
# ax[1,0].plot(X2,[a/np.pi for a in A2[4]],'x:',label='350 um')
ax[1,0].plot(X1,[l*1e9 for l in LWR],'x:',color='black')#[a1[2] for a1 in A1[9]],'x:',color='black',label='50 um')
ax[1,0].set_ylabel(labelY[9])#'LWR [nm]')
# ax[1,0].vlines(5,ymin=np.min(A1[7][2])*1e9,ymax=np.max(A1[7][2])*1e9, color='r', linestyle=':')
# ax[1,1].plot(X2,[a1/a2 for a1,a2 in zip(A2[5],A2[4])],'x:',label='350 um')
ax[1,1].plot(X1,[a*1e9 for a in LERpick[1]],'x:',color='black',label='50 um')
# ax[1,1].vlines(5,ymin=np.min(LERpick[1])*1e9,ymax=np.max(LERpick[1])*1e9, color='r', linestyle=':')
ax[1,1].set_ylabel('LER [nm]')
ax[1,2].plot(X1,[c for c in CLR],'x:',color='black',label='50 um')
ax[1,2].set_ylabel('CDU [nm]')
# ax[1,2].vlines(5,ymin=np.min([np.mean(a)/np.pi for a in A1[8]]),ymax=np.max([np.mean(a)/np.pi for a in A1[8]]), color='r', linestyle=':')
ax[2,0].plot(X1,[1 - a for a in A1[5]],'x:',color='black',label='50 um')
ax[2,0].set_ylabel(labelY[5])
# ax[2,0].vlines(5,ymin=np.min(A1[5]),ymax=np.max(A1[5]), color='r', linestyle=':')
ax[2,1].plot(X1,A1[10],'x:',color='black',label='50 um')
ax[2,1].set_ylabel(labelY[10])
# ax[2,1].vlines(5,ymin=np.min(A1[10]),ymax=np.max(A1[10]), color='r', linestyle=':')
ax[2,2].plot(X1,A1[11],'x:',color='black',label='50 um')
ax[2,2].set_ylabel(labelY[11])
# ax[2,2].vlines(5,ymin=np.min(A1[11]),ymax=np.max([a/np.pi for a in A1[7]]), color='r', linestyle=':')
# ax[1,2].plot(X2,[a*1e9 for a in A2[6]],'x:',label='350 um')

for i,a in enumerate(ax):
    for b in a:
        b.set_xlabel('$\sigma_{LER}$')
        # b.vlines(5,ymin=0,ymax=1,color='r', linestyle=':',transform=b.get_yaxis_transform())

# .ylabel(labelY[0])
# plt.xlabel(labelX)
# plt.legend()
plt.tight_layout()
plt.show()

import pandas as pd
# dF = pd.DataFrame(np.concatenate([labels,avPeaks,sumPeaks,rmsPeaks,
#                              michelsonC,rmsC,[c[0] for c in compositeC],
#                              [f[0] for f in fourierC],[n[0] for n in nilsC]]),

# dataStructure = [LERa,LERc,
#                  A1[0],[a / 0.6 for a in A1[2]],
#                  [a/np.pi for a in A1[4]],
#                  [a1*1e9 for a1 in A1[7]],
#                  [a*1e9 for a in LERpick[1]],
#                  [np.mean(a)/np.pi for a in A1[6]],
#                  A1[3],
#                  A1[8],
#                  A1[5]
#                  ]
# for d in dataStructure:
#     print(np.shape(d))

# dF = pd.DataFrame(np.array(dataStructure).T,
#                   columns=['RMS roughness',
#                            'Corr Length',
#                            'Michelson C', #'rms C', 
#                            'composite C',
#                            'NILS',
#                            'LWR',
#                            'LER',
#                            'NILS$_{\sigma_n} / \pi$',
#                            'Fidelity',
#                            '$\eta_{AE}$',
#                            'NILS$_{\sigma} / \pi$'])
# correlations = dF.corr()
# import seaborn as sns

# sns.heatmap(np.abs(correlations),cmap='gray',vmin=0,vmax=1,annot=True) #'vlag',vmin=-1,vmax=1,annot=True)
# plt.show()


plt.plot(LERa,[a/np.pi for a in A1[4]],':x',color='black')
plt.xlabel('$\sigma_{LER}$ [nm]')
plt.ylabel(labelY[4])
plt.show()
plt.errorbar(LERa,[l*1e9 for l in LERpick[2]],[(l/2)*1e9 for l in LERpick[3]],fmt=':x',color='black')
plt.xlabel('Mask $\sigma_{LER}$ [nm]')
plt.ylabel('Aerial Image $\sigma_{LER}$ [nm]')
plt.show()
plt.plot(LERc[1::],[l*1e9 for l in LERpick[4][1::]], ':x', color='black')
plt.xlabel('Mask LER $c$ [nm]')
plt.ylabel('Aerial Image LER $c$ [nm]')
plt.show()

plt.plot(LERa,A1[8],'x:',color='black',label='50 um')
plt.xlabel('Mask $\sigma_{LER}$ [nm]')
plt.ylabel(labelY[8])
# plt.vlines(5,ymin=np.min(A1[8]),ymax=np.max(A1[8]), color='r', linestyle=':')
plt.show()
# print(LWR)