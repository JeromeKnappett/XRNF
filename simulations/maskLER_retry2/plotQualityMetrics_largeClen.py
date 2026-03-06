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
dirPath = '/user/home/opt/xl/xl/experiments/maskLER_retry2/data/'
files = ['dataStructure_largeClen.pkl']# ['contrastMetrics_maskLER_retry_2d.pkl']#,'contrastMetrics350_2d.pkl']
labelX = '$LER$ [um]'#'$\sigma [nm]$'
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
          # 'LER [nm]', #10
          '$\eta_{AE}$', # 11
          '$\eta_{0}$'  #12
          ] 



# ['$1 - Fidelity$', '$C_M$', '$C_{RMS}$', '$C_{Composite}$', '$NILS_{mean}$', '$NILS_{\sigma_n}$', '$LWR$']
# labelY = ['$1 - Fidelity$', '$C_M$', '$C_{RMS}$', '$C_{Composite}$', '$NILS_{mean}$', '$LWR$']
# legend = ['$c_y  = 2$','$c_y = 4$','$c_y = 6$','$c_y = 8$','$c_y = 10$']

# pickle.dump([labels,michelsonC2d,rmsC2d,compositeC2d,fidel2d,nils2d,nilsSTD,LWR], f)
savePath = None#'/home/jerome/dev/data/correctedRoughness/contrastWithoutLWR.png'
LERpick = pickle.load(open(dirPath + 'LER__maskLER_retry_largeClen.pkl', 'rb'))
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
LERa = [[4.341524765321773,3.766411879905553,3.2124952672360794,2.6946056828131],
        [2.503385243226183,2.3006595222372036,1.2381303522982893]]
        # [3.0036300170087337,2.61203604789903,1.796048147106454],
        # [3.340738562744371,3.063506165870519,2.1333112482785796]
        # ]
LERc = [[4.207935647188462e-07,4.1866500868478874e-07,4.157535506570951e-07,4.153690610189768e-07],
        [4.058608130355334e-07,3.990313969385507e-07,2.881471602326983e-07]]
        # [3.046195669327372e-07,3.0004584918501986e-07,2.5527064832483523e-07],
        # [2.554779981374661e-07,2.5195598054173894e-07,2.2568477083960977e-07]
        # ]

print(pick1[0])
X1 = LERa

print('Ideal Mask Metrics ---')
# print(A1)
for i,a in enumerate(A1):
    if i != 9 and i != 8:
        print('\n')
        print(i)
        print(labelY[i])
        print(np.shape(a))
        print(a[0])
    else:
        print('\n')
        print(labelY[i])
        print(np.shape(a[4][0]))
        # print(a[3][0])
print(a[0] for a in A1)

LWR = [l[3] for l in A1[9]]
CDU = [l[4] for l in A1[9]]
CLR = [l[5] for l in A1[9]]
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
# print('\n here... ')
# for a in A1[9]:
#     print(a[3]*1e9)# for a in A1[9])
# print('... there')
ef = [A1[10][0:4],A1[10][4:7],A1[10][7:10],A1[10][10::]]
ef0 = [A1[11][0:4],A1[11][4:7],A1[11][7:10],A1[11][10::]]

Cm =  [A1[0][0:4],A1[0][4:7],A1[0][7:10],A1[0][10::]] #np.reshape(A1[0],(5,5))
Crms = [A1[2][0:4],A1[2][4:7],A1[2][7:10],A1[2][10::]] # np.reshape(A1[2],(5,5))
Cc = [A1[3][0:4],A1[3][4:7],A1[3][7:10],A1[3][10::]] # np.reshape([a/0.6 for a in A1[3]],(5,5))
F = [A1[5][0:4],A1[5][4:7],A1[5][7:10],A1[5][10::]] # np.reshape(A1[5],(5,5))
NILS = [A1[6][0:4],A1[6][4:7],A1[6][7:10],A1[6][10::]] # np.reshape([a/np.pi for a in A1[6]],(5,5))
NILSs = [A1[7][0:4],A1[7][4:7],A1[7][7:10],A1[7][10::]] # np.reshape([a/np.pi for a in A1[7]],(5,5))
# NILSsn = np.reshape([a/np.pi for a in A1[8]],(5,5))
# LWR = [a[3] for a in A1[9]]#[A1[9][3][0:4],A1[9][3][4:7],A1[9][3][7:10],A1[9][3][10::]] # np.reshape([a[3]*1e9 for a in A1[9]],(5,5))

LWR = [LWR[0:4],LWR[4:7],LWR[7:10],LWR[10::]]
CDU = [CDU[0:4],CDU[4:7],CDU[7:10],CDU[10::]]
CLR = [CLR[0:4],CLR[4:7],CLR[7:10],CLR[10::]]
# ef = np.reshape(A1[10],(5,5))

AMP = LERa# np.reshape([a*1e9 for a in AMP],(5,5))
LER = [LERpick[2][0:4],LERpick[2][4:7],LERpick[2][7:10],LERpick[2][10::]] # np.reshape([l*1e9 for l in LERpick[2][1::]],(5,5))

print('LWR here')
print(LWR)

print(NILS)
# print([l*1e9 for l in LERpick[2]])
print(pick1[0])
# X1 = LERa

# fig.subplots_adjust(bottom=0.5,hspace=5.33)   ##  Need to play with this number.
# # 
# for a,l in zip(AMP,LER):
#     # a = [0.0] + a
#     # l = [LERpick[2][0]*1e9] + l
#     a = np.insert(a,0,0.0)
#     l = np.insert(l,0,LERpick[2][0]*1e9)
#     plt.plot(a,l,':x')
#     # plt.plot(AMP[-1],LER[-2],':x')
# plt.show()

# print(LER[3],LER[4])

# print(ef[3],ef[4])

print('LER')
print(LER)
print('ef')
print(ef)
print('ef0')
print(ef0)
print('LWR')
print(LWR)
print('CDU')
print(CDU)
print('CLR')
print(CLR)

fig,ax= plt.subplots(3,3)

for i,a in enumerate(AMP):
    ax[0,0].plot(a,Cm[i],':x')
    ax[0,1].plot(a,[c/0.6 for c in Cc[i]],':x')
    ax[0,2].plot(a,[n/np.pi for n in NILS[i]],':x')
    ax[1,0].plot(a,LWR[i],':x')
    ax[1,1].plot(a,LER[i],':x')
    ax[1,2].plot(a,[c*1e9 for c in CDU[i]],':x') #[l*1e9 for l in dLWRrms[i]],':x')
    ax[2,0].plot(a,[1 - f for f in F[i]],':x')
    ax[2,1].plot(a,ef[i],':x')
    ax[2,2].plot(a,ef0[i],':x')

ax[0,0].set_ylabel(labelY[0])
    
ax[0,1].set_ylabel(labelY[3])
ax[0,2].set_ylabel(labelY[6])
ax[1,0].set_ylabel('LWR [nm]')
ax[1,1].set_ylabel('LER [nm]')
ax[1,2].set_ylabel('CDU [nm]') #'LWR [nm]')
ax[2,0].set_ylabel(labelY[5])
ax[2,1].set_ylabel(labelY[10])
ax[2,2].set_ylabel(labelY[11])
ax[2,2].legend(labels=[str(c) + ' nm' for c in [420,400,300,250]])#, bbox_to_anchor=(1.75,-0.35), title='$c_y$') #loc="lower center"
for a in [ax[2,0],ax[2,1],ax[2,2]]:
    a.set_xlabel('$\sigma_{SR}$ [nm]')
fig.tight_layout()
plt.show()

# fig,ax= plt.subplots(3,3)

#     # dataStructure = [sigma, #cY,
#     #                  michelsonC2d,rmsC2d,[c[0] for c in compositeC2d],
#     #                   fidel2d,
#     #                   nils2d,
#     #                   nilsSTD,
#     #                   LWR,
#     #                   E1]
    
    

# print(LERpick[1])

# print([a[3] for a in A1[9]])


# ax[0,0].plot(X1,A1[0],'x:',color='black',label='50 um')
# ax[0,0].set_ylabel(labelY[0])
# ax[0,0].vlines(5,ymin=np.min(A1[0]),ymax=np.max(A1[0]), color='r', linestyle=':')
# # ax[0,0].plot(X2,A2[0],'x:',label='350 um')
# ax[0,1].plot(X1,[a / 0.6 for a in A1[3]],'x:',color='black',label='50 um')
# ax[0,1].set_ylabel(labelY[3])
# # ax[0,1].vlines(5,ymin=np.min(A1[2])*0.6,ymax=np.max(A1[2])*0.6, color='r', linestyle=':')
# ax[0,1].vlines(5,ymin=np.min(A1[3])/0.6,ymax=np.max(A1[3])/0.6, color='r', linestyle=':')
# # ax[0,1].plot(X2,[a[0] / 0.6 for a in A2[2]],'x:',label='350 um')
# ax[0,2].plot(X1,[a/np.pi for a in A1[6]],'x:',color='black',label='50 um')
# ax[0,2].set_ylabel(labelY[6])
# ax[0,2].vlines(5,ymin=np.min(A1[6])/np.pi,ymax=np.max(A1[6])/np.pi, color='r', linestyle=':')
# # ax[0,3].plot(X1,[a for a in A1[4]],'x:',label='50 um')
# # ax[0,3].set_ylabel(labelY[4])
# # ax[0,2].plot(X2,[1 - a for a in A2[3]],'x:',label='350 um')
# # ax[1,0].plot(X2,[a/np.pi for a in A2[4]],'x:',label='350 um')
# ax[1,0].plot(X1,[a1[3] for a1 in A1[9]],'x:',color='black',label='50 um')
# ax[1,0].set_ylabel(labelY[9])#'LWR [nm]')
# # ax[1,0].vlines(5,ymin=np.min(A1[7][2])*1e9,ymax=np.max(A1[7][2])*1e9, color='r', linestyle=':')
# # ax[1,1].plot(X2,[a1/a2 for a1,a2 in zip(A2[5],A2[4])],'x:',label='350 um')
# ax[1,1].plot(X1,[a*1e9 for a in LERpick[1]],'x:',color='black',label='50 um')
# ax[1,1].vlines(5,ymin=np.min(LERpick[1])*1e9,ymax=np.max(LERpick[1])*1e9, color='r', linestyle=':')
# ax[1,1].set_ylabel('LER [nm]')
# ax[1,2].plot(X1,[np.mean(a)/np.pi for a in A1[8]],'x:',color='black',label='50 um')
# ax[1,2].set_ylabel(labelY[8])
# ax[1,2].vlines(5,ymin=np.min([np.mean(a)/np.pi for a in A1[8]]),ymax=np.max([np.mean(a)/np.pi for a in A1[8]]), color='r', linestyle=':')
# ax[2,0].plot(X1,A1[5],'x:',color='black',label='50 um')
# ax[2,0].set_ylabel(labelY[5])
# ax[2,0].vlines(5,ymin=np.min(A1[5]),ymax=np.max(A1[5]), color='r', linestyle=':')
# ax[2,1].plot(X1,A1[10],'x:',color='black',label='50 um')
# ax[2,1].set_ylabel(labelY[10])
# ax[2,1].vlines(5,ymin=np.min(A1[10]),ymax=np.max(A1[10]), color='r', linestyle=':')
# ax[2,2].plot(X1,[a/np.pi for a in A1[7]],'x:',color='black',label='50 um')
# ax[2,2].set_ylabel(labelY[7])
# ax[2,2].vlines(5,ymin=np.min([a/np.pi for a in A1[7]]),ymax=np.max([a/np.pi for a in A1[7]]), color='r', linestyle=':')
# # ax[1,2].plot(X2,[a*1e9 for a in A2[6]],'x:',label='350 um')

# for i,a in enumerate(ax):
#     for b in a:
#         b.set_xlabel('$\sigma_{LER}$')
#         # b.vlines(5,ymin=0,ymax=1,color='r', linestyle=':',transform=b.get_yaxis_transform())

# # .ylabel(labelY[0])
# # plt.xlabel(labelX)
# # plt.legend()
# # plt.tight_layout()
# plt.show()

# import pandas as pd
# # dF = pd.DataFrame(np.concatenate([labels,avPeaks,sumPeaks,rmsPeaks,
# #                              michelsonC,rmsC,[c[0] for c in compositeC],
# #                              [f[0] for f in fourierC],[n[0] for n in nilsC]]),

# # dataStructure = [LERa,LERc,
# #                  A1[0],[a / 0.6 for a in A1[2]],
# #                  [a/np.pi for a in A1[4]],
# #                  [a1*1e9 for a1 in A1[7]],
# #                  [a*1e9 for a in LERpick[1]],
# #                  [np.mean(a)/np.pi for a in A1[6]],
# #                  A1[3],
# #                  A1[8],
# #                  A1[5]
# #                  ]
# # for d in dataStructure:
# #     print(np.shape(d))

# # dF = pd.DataFrame(np.array(dataStructure).T,
# #                   columns=['RMS roughness',
# #                            'Corr Length',
# #                            'Michelson C', #'rms C', 
# #                            'composite C',
# #                            'NILS',
# #                            'LWR',
# #                            'LER',
# #                            'NILS$_{\sigma_n} / \pi$',
# #                            'Fidelity',
# #                            '$\eta_{AE}$',
# #                            'NILS$_{\sigma} / \pi$'])
# # correlations = dF.corr()
# # import seaborn as sns

# # sns.heatmap(np.abs(correlations),cmap='gray',vmin=0,vmax=1,annot=True) #'vlag',vmin=-1,vmax=1,annot=True)
# # plt.show()


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