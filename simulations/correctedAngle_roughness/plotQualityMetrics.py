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
rcParams['figure.figsize']=(12,10)
rcParams['figure.dpi']=500
rcParams.update({'font.size': 15})

def rejectOutliers(data, m = 2.0):
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
dirPath = '/user/home/opt/xl/xl/experiments/BEUVcoherenceRoughness/data/D_27.5um/'
files = ['dataStructure.pkl']# ['contrastMetrics_maskLER_retry_2d.pkl']#,'contrastMetrics350_2d.pkl']
labelX = '$LER$ [um]'#'$\sigma [nm]$'
labelY = ['$C_M$',    #0
          '$C_{RMS}$',#1
          '$C_c$',    #2
          'Fidelity', #3
          'NILS / $\pi$',     #4
          'NILS$_{\sigma} / \pi$', #5 
          'NILS$_{\sigma_n} / \pi$', #6
          'LWR [nm]', #7
          # 'LER [nm]', #8
          '$\eta_{AE}$'] #8
# ['$1 - Fidelity$', '$C_M$', '$C_{RMS}$', '$C_{Composite}$', '$NILS_{mean}$', '$NILS_{\sigma_n}$', '$LWR$']
# labelY = ['$1 - Fidelity$', '$C_M$', '$C_{RMS}$', '$C_{Composite}$', '$NILS_{mean}$', '$LWR$']
# legend = ['$c_y  = 2$','$c_y = 4$','$c_y = 6$','$c_y = 8$','$c_y = 10$']

# pickle.dump([labels,michelsonC2d,rmsC2d,compositeC2d,fidel2d,nils2d,nilsSTD,LWR], f)
savePath = None#'/home/jerome/dev/data/correctedRoughness/contrastWithoutLWR.png'
LERpick = pickle.load(open(dirPath + 'LER__BEUVcoherenceRoughness.pkl', 'rb'))
pick1 = pickle.load(open(dirPath + files[0], 'rb'))
# pick2 = pickle.load(open(dirPath + files[1], 'rb'))

#['\u03C3 = 0.5 nm ','\u03C3 = 1.0 nm ','\u03C3 = 1.5 nm ','\u03C3 = 2.0 nm','\u03C3 = 2.5 nm']
# ['\u03C3 = 0.5 nm ','\u03C3 = 1.0 nm ','\u03C3 = 1.5 nm ','\u03C3 = 2.0 nm','\u03C3 = 2.5 nm',
#           '\u03C3 = 0.5 nm ','\u03C3 = 1.0 nm ','\u03C3 = 1.5 nm ','\u03C3 = 2.0 nm','\u03C3 = 2.5 nm',
#           '\u03C3 = 0.5 nm ','\u03C3 = 1.0 nm ','\u03C3 = 1.5 nm ','\u03C3 = 2.0 nm','\u03C3 = 2.5 nm',
#           '\u03C3 = 0.5 nm ','\u03C3 = 1.0 nm ','\u03C3 = 1.5 nm ','\u03C3 = 2.0 nm','\u03C3 = 2.5 nm',
#           '\u03C3 = 0.5 nm ','\u03C3 = 1.0 nm ','\u03C3 = 1.5 nm ','\u03C3 = 2.0 nm','\u03C3 = 2.5 nm']
AMP = [1.8957491158975655e-09, 4.837936100237537e-09, 9.055242151064516e-09, 1.2549329850247491e-08, 1.638520045419863e-08, 
       2.0274745981409948e-09, 5.322494415040973e-09, 9.971287489916746e-09, 1.4552004450011793e-08, 1.961328690281936e-08, 
       2.0708649093245497e-09, 5.736255511372007e-09, 1.0891880298109786e-08, 1.674687772725672e-08, 2.5102372364189192e-08, 
       2.1254315219119853e-09, 6.0181858110299e-09, 1.1615570502176536e-08, 1.6965680619519238e-08, 2.439757423733175e-08, 
       2.223413251120878e-09, 6.281837752075332e-09, 1.1724286146324283e-08, 1.8602931512648502e-08, 2.608729150648162e-08]

dLWRrms = [[8.427646902802932e-09,8.445923043712371e-09,8.323390312136786e-09,8.433676805326568e-09,8.636950678951386e-09],
           [8.216654268061558e-09,8.43164769098587e-09,8.26403195838243e-09,8.5158835550744e-09,9.432761436582507e-09],
           [8.792456204610056e-09,8.64382485666872e-09,8.778723735080951e-09,9.611801924141647e-09,8.964208354383165e-09],
           [8.646571087976813e-09,8.704640695732781e-09,9.309411593374496e-09,1.0435498793050492e-08,1.1313335442671736e-08],
           [8.591191527244488e-09,8.863934998266011e-09,1.0532558523278013e-08,1.0792134412664117e-08,1.2902975502985469e-08]]
           
legendTitle = None #'$C_y =$ 2 nm' # None #'$C_y =$ 10 nm'
N = 1200                            # number of pixels to take for line profile  - 1200 for roughness aerial images
n = 16                             # number of pixels to average over for line profile - 15 for roughness aerial images
plotRange = 1000                       # range of aerial image plot in nm






# print(LERpick[0])
# print(pick1)
A1 = [p for p in pick1[1::]]
# A2 = [p for p in pick2[1::]]
# [[1 - p for p in pick[5]], pick[2], pick[3], pick[4], pick[6], pick[7], pick[8]]
# A = [[1 - p for p in pick[5]], pick[2], pick[3], pick[4], pick[6], pick[8]]
# X1 = [0.0,0.5,1.0,1.5,2.0,2.5,3.0,3.5,4.0] #[float(p[4:-4]) for p in pick1[0]]
# X2 = [int(p[:-3]) for p in pick2[0]]
# LERa = [0.0,
#         3.7249164431850543,
#         4.536853502343667,
#         5.518446489820692,
#         6.4970478648742045]
# LERc = [0.0,62.5,61.0,58.6,57.6]
labelY = ['$C_M$',    #0
          '$C_M$',    #1
          '$C_{RMS}$',#2
          '$C_c$',    #3
          '$C_c$',    #4
          'Fidelity', #5
          'NILS / $\pi$',     #6
          'NILS$_{\sigma} / \pi$', #7 
          'NILS$_{\sigma_n} / \pi$', #8
          'LWR [nm]', #9
          # 'LER [nm]', 
          '$\eta_{AE}$', #10
          '$\eta_{0}$'] #11

print('Ideal Mask Metrics ---')
# print(A1)
for i,a in enumerate(A1):
    if i != 9 and i != 8:
        print('\n')
        print(i)
        print(labelY[i])
        print(np.shape(a))
        print(a)
    elif i==9:
        print('\n')
        print(labelY[i])
        print(np.shape(a[3][0]))
        # print(a[3])
        # print('CDU')
        # print(a[4])
        # print('CLR')
        # print(a[5])
        print(3*(np.std(a[0]) / np.mean(a[0])) )
        # print(a[3][0])
    elif i==8:
        pass
print(a[0] for a in A1)
LWR = [a[3] for a in A1[9]]
CDU = [a[4] for a in A1[9]]
CLR = [a[5] for a in A1[9]]
print('LWR')
print(LWR)
print('CDU')
print(CDU)
print('CLR')
print(CLR)
# print('\n here... ')
for a in A1[9]:
    print(a[3]*1e9)# for a in A1[9])
# print('... there')
# LWR = []
# for a in A1[9]:
#     lw = rejectOutliers(np.array(a[0]))
#     LW = np.mean(a[0])
#     LWd = [abs(b - LW) for b in lw]
#     lwr = 3*np.std(LWd)
#     LWR.append(lwr)
#     plt.plot(LWd)
#     plt.show()

# print('LWR here')
# print(LWR[0])
# LWR = np.reshape(LWR[1::],(5,5))
# print(LWR)

ef = np.reshape(A1[10],(5,5))


plt.plot()

print(A1[6][0])

A1 = [a[1::] for a in A1]

Cm = np.reshape(A1[0],(5,5))
Crms = np.reshape(A1[2],(5,5))
Cc = np.reshape([a/0.6 for a in A1[3]],(5,5))
F = np.reshape(A1[5],(5,5))
NILS = np.reshape([a/np.pi for a in A1[6]],(5,5))
NILSs = np.reshape([a/np.pi for a in A1[7]],(5,5))
# NILSsn = np.reshape([a/np.pi for a in A1[8]],(5,5))
# LWR = np.reshape([3*(np.std(a[0]) / np.mean(a[0])) for a in A1[9]], (5,5))
# np.reshape([a[3]*1e9 for a in A1[9]],(5,5))
# ef = np.reshape(A1[10],(5,5))

AMP = np.reshape([a*1e9 for a in AMP],(5,5))
LER = np.reshape([l*1e9 for l in LERpick[2][1::]],(5,5))

print('LER here')
print([l*1e9 for l in LERpick[2]])
print(pick1[0])
print('NILS')
print([n*np.pi for n in NILS])
# X1 = LERa

# fig.subplots_adjust(bottom=0.5,hspace=5.33)   ##  Need to play with this number.
# 
for a,l in zip(AMP,LER):
    # a = [0.0] + a
    # l = [LERpick[2][0]*1e9] + l
    a = np.insert(a,0,0.0)
    l = np.insert(l,0,LERpick[2][0]*1e9)
    plt.plot(a,l,':x')
    # plt.plot(AMP[-1],LER[-2],':x')
plt.show()

print(LER[3],LER[4])

# print(ef[3],ef[4])

fig,ax= plt.subplots(3,3)

for i,a in enumerate(AMP):
    ax[0,0].plot(a,Cm[i],':x')
    ax[0,1].plot(a,Cc[i],':x')
    ax[0,2].plot(a,NILS[i],':x')
    ax[1,0].plot(a,LWR[i],':x')
    ax[1,1].plot(a,LER[i],':x')
    ax[1,2].plot(a,NILSs[i],':x') #[l*1e9 for l in dLWRrms[i]],':x')
    ax[2,0].plot(a,F[i],':x')
    ax[2,1].plot(a,ef[i],':x')
    # ax[2,2].plot(a,NILSsn[i],':x')

ax[0,0].set_ylabel(labelY[0])
    
ax[0,1].set_ylabel(labelY[3])
ax[0,2].set_ylabel(labelY[6])
ax[1,0].set_ylabel('LWR [nm]')
ax[1,1].set_ylabel('LER [nm]')
ax[1,2].set_ylabel(labelY[7]) #'LWR [nm]')
ax[2,0].set_ylabel(labelY[5])
ax[2,1].set_ylabel(labelY[10])
ax[2,2].set_ylabel(labelY[8])
# ax[1,1].legend(labels=['$C_y$ = ' + str(c) for c in [2,4,6,8,10]], bbox_to_anchor=(1.75,-0.35), ncol=5) #loc="lower center"
for a in [ax[2,0],ax[2,1],ax[2,2]]:
    a.set_xlabel('$\sigma_{SR}$ [nm]')
fig.tight_layout()
plt.show()

    # dataStructure = [sigma, #cY,
    #                  michelsonC2d,rmsC2d,[c[0] for c in compositeC2d],
    #                   fidel2d,
    #                   nils2d,
    #                   nilsSTD,
    #                   LWR,
    #                   E1]


# fig, axs = plt.subplots(3,3)



# axs[0,0].plot(sigma[0:5], michelsonC2d[0:5], 'x:')
# axs[0,0].plot(sigma[5:10], michelsonC2d[5:10], 'x:')
# axs[0,0].plot(sigma[10:15], michelsonC2d[10:15], 'x:')
# axs[0,0].plot(sigma[20:25], michelsonC2d[20:25], 'x:')
# axs[0,0].plot(sigma[15:20], michelsonC2d[15:20], 'x:')
# axs[0,0].set_title("Michelson")
# axs[0,0].set_ylabel("Contrast")

# ax[0,0].plot(X1,A1[0],'x:',color='black',label='50 um')
# ax[0,0].set_ylabel(labelY[0])
# ax[0,0].vlines(5,ymin=np.min(A1[0]),ymax=np.max(A1[0]), color='r', linestyle=':')
# # ax[0,0].plot(X2,A2[0],'x:',label='350 um')
# ax[0,1].plot(X1,[a / 0.6 for a in A1[2]],'x:',color='black',label='50 um')
# ax[0,1].set_ylabel(labelY[2])
# # ax[0,1].vlines(5,ymin=np.min(A1[2])*0.6,ymax=np.max(A1[2])*0.6, color='r', linestyle=':')
# ax[0,1].vlines(5,ymin=np.min(A1[2])/0.6,ymax=np.max(A1[2])/0.6, color='r', linestyle=':')
# # ax[0,1].plot(X2,[a[0] / 0.6 for a in A2[2]],'x:',label='350 um')
# ax[0,2].plot(X1,[a/np.pi for a in A1[4]],'x:',color='black',label='50 um')
# ax[0,2].set_ylabel(labelY[4])
# ax[0,2].vlines(5,ymin=np.min(A1[4])/np.pi,ymax=np.max(A1[4])/np.pi, color='r', linestyle=':')
# # ax[0,3].plot(X1,[a for a in A1[4]],'x:',label='50 um')
# # ax[0,3].set_ylabel(labelY[4])
# # ax[0,2].plot(X2,[1 - a for a in A2[3]],'x:',label='350 um')
# # ax[1,0].plot(X2,[a/np.pi for a in A2[4]],'x:',label='350 um')
# ax[1,0].plot(X1,[a1*1e9 for a1 in A1[7]],'x:',color='black',label='50 um')
# ax[1,0].set_ylabel(labelY[7])#'LWR [nm]')
# ax[1,0].vlines(5,ymin=np.min(A1[7])*1e9,ymax=np.max(A1[7])*1e9, color='r', linestyle=':')
# # ax[1,1].plot(X2,[a1/a2 for a1,a2 in zip(A2[5],A2[4])],'x:',label='350 um')
# ax[1,1].plot(X1,[a*1e9 for a in LERpick[1]],'x:',color='black',label='50 um')
# ax[1,1].vlines(5,ymin=np.min(LERpick[1])*1e9,ymax=np.max(LERpick[1])*1e9, color='r', linestyle=':')
# ax[1,1].set_ylabel('LER [nm]')
# ax[1,2].plot(X1,[np.mean(a)/np.pi for a in A1[6]],'x:',color='black',label='50 um')
# ax[1,2].set_ylabel(labelY[6])
# ax[1,2].vlines(5,ymin=np.min([np.mean(a)/np.pi for a in A1[6]]),ymax=np.max([np.mean(a)/np.pi for a in A1[6]]), color='r', linestyle=':')
# ax[2,0].plot(X1,A1[3],'x:',color='black',label='50 um')
# ax[2,0].set_ylabel(labelY[3])
# ax[2,0].vlines(5,ymin=np.min(A1[3]),ymax=np.max(A1[3]), color='r', linestyle=':')
# ax[2,1].plot(X1,A1[8],'x:',color='black',label='50 um')
# ax[2,1].set_ylabel(labelY[8])
# ax[2,1].vlines(5,ymin=np.min(A1[8]),ymax=np.max(A1[8]), color='r', linestyle=':')
# ax[2,2].plot(X1,[a/np.pi for a in A1[5]],'x:',color='black',label='50 um')
# ax[2,2].set_ylabel(labelY[5])
# ax[2,2].vlines(5,ymin=np.min([a/np.pi for a in A1[5]]),ymax=np.max([a/np.pi for a in A1[5]]), color='r', linestyle=':')
# # ax[1,2].plot(X2,[a*1e9 for a in A2[6]],'x:',label='350 um')

# for i,a in enumerate(ax):
#     for b in a:
#         b.set_xlabel('$\sigma_{LER}$')
#         # b.vlines(5,ymin=0,ymax=1,color='r', linestyle=':',transform=b.get_yaxis_transform())

# # .ylabel(labelY[0])
# # plt.xlabel(labelX)
# # plt.legend()
# plt.tight_layout()
# plt.show()

# import pandas as pd
# # dF = pd.DataFrame(np.concatenate([labels,avPeaks,sumPeaks,rmsPeaks,
# #                              michelsonC,rmsC,[c[0] for c in compositeC],
# #                              [f[0] for f in fourierC],[n[0] for n in nilsC]]),

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


# plt.plot(LERa,[a/np.pi for a in A1[4]],':x',color='black')
# plt.xlabel('$\sigma_{LER}$ [nm]')
# plt.ylabel(labelY[4])
# plt.show()
# plt.errorbar(LERa,[l*1e9 for l in LERpick[2]],[(l/2)*1e9 for l in LERpick[3]],fmt=':x',color='black')
# plt.xlabel('Mask $\sigma_{LER}$ [nm]')
# plt.ylabel('Aerial Image $\sigma_{LER}$ [nm]')
# plt.show()
# plt.plot(LERc[1::],[l*1e9 for l in LERpick[4][1::]], ':x', color='black')
# plt.xlabel('Mask LER $c$ [nm]')
# plt.ylabel('Aerial Image LER $c$ [nm]')
# plt.show()

# plt.plot(LERa,A1[8],'x:',color='black',label='50 um')
# plt.xlabel('Mask $\sigma_{LER}$ [nm]')
# plt.ylabel(labelY[8])
# # plt.vlines(5,ymin=np.min(A1[8]),ymax=np.max(A1[8]), color='r', linestyle=':')
# plt.show()
# # print(LWR)