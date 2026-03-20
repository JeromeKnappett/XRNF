#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 27 17:20:44 2021

@author: jerome
"""
import pandas as pd
import seaborn as sns
import pickle
import numpy as np
import matplotlib.pyplot as plt

def round_sig(x, sig=2):
    from math import log10, floor
    if x != 0:
        return round(x, sig-int(floor(log10(abs(x))))-1)
    else:
        return x
LW = [2.2632844241933926e-10, 2.2628547367552867e-10, 1.6024248126821441e-06, 2.256109517290475e-10, 2.3382342898458545e-10, 2.2546141726124313e-10, 2.2778532168670097e-10, 2.2396161928140426e-10, 2.347982985786529e-10, 2.6227391781020906e-10, 2.3221400658881075e-10, 2.308415623342424e-10, 2.3890920943790984e-10, 2.5916653165493446e-10, 2.4790331142586117e-10, 2.2577317554859892e-10, 2.3674669797020747e-10, 2.4739624788227333e-10, 2.992226109635963e-10, 3.1958022233467395e-10, 2.300894540755333e-10, 2.4150719041559143e-10, 2.795415539288099e-10, 2.952255127300836e-10, 3.8015089234455055e-10]

with open('/home/jerome/dev/data/aerialImages/roughness/pickles/dataStructure.pkl', 'rb') as g:             
    dataStructure = pickle.load(g)
with open('/home/jerome/dev/data/aerialImages/roughness/pickles/LW.pickle', 'rb') as h:             
    LWp = pickle.load(h)
with open('/home/jerome/dev/data/2dNILSrmsD.pkl', 'rb') as h:             
    NILSrmsD = pickle.load(h)
with open('/home/jerome/dev/data/2dNILS3s.pkl', 'rb') as h:             
    NILS3s = pickle.load(h)
with open('/home/jerome/dev/data/aerialImages/roughness/pickles/NILSALL.pkl', 'rb') as h:    
    NILSALL = pickle.load(h)
with open('/home/jerome/dev/data/aerialImages/roughness/pickles/nilsNstd.pkl', 'rb') as h:    
    NILSnSTD = pickle.load(h)
    
# dataStructure = [sigma,cY,michelsonC2d,rmsC2d, [c[0] for c in compositeC2d],
#                  nils2d, lwRMS, dlwRMS]

# m = 25e-9
# sigma3 = []
# LWRx = []
LWRx = [2.2632844241933926e-10,
 2.2628547367552867e-10,
 1.6024248126821441e-06,
 2.256109517290475e-10,
 2.3382342898458545e-10,
 2.2546141726124313e-10,
 2.2778532168670097e-10,
 2.2396161928140426e-10,
 2.347982985786529e-10,
 2.6227391781020906e-10,
 2.3221400658881075e-10,
 2.308415623342424e-10,
 2.3890920943790984e-10,
 2.5916653165493446e-10,
 2.4790331142586117e-10,
 2.2577317554859892e-10,
 2.3674669797020747e-10,
 2.4739624788227333e-10,
 2.992226109635963e-10,
 3.1958022233467395e-10,
 2.300894540755333e-10,
 2.4150719041559143e-10,
 2.795415539288099e-10,
 2.952255127300836e-10,
 3.8015089234455055e-10]
# meanLW = []
# for l in LWp:
#     stdDev3 = 3 * np.std(l[0])
#     sigma3.append(stdDev3)
#     LWRx.append(l[3])
#     varianceFromMean = np.var(l[0])
#     variance = sum((xi-m)**2 for xi in l[0]) / len(l[0])
#     mean = np.mean(l[0])
#     print('3sigma = {}, variance (f. mean) = {}, variance = {}, mean = {}'.format(stdDev3, varianceFromMean, variance, mean))
#     plt.plot(l[0])
#     plt.show()
    
#     meanLW.append(mean)
    
OGtitles = ['\u03C3','$c_y$',
            '$C_M$', '$C_{RMS}$', '$C_{composite}$',
            '$Fidelity$','$NILS_{mean}$', '$NILS_{RMS}$','$LW_{mean}$','LWR']
ind1, ind2, ind3 = OGtitles.index('$LW_{mean}$'), OGtitles.index('LWR'), OGtitles.index('$NILS_{RMS}$')
titles = [OGtitles[i] for i in range(len(OGtitles)) if i != ind1 and i != ind2 and i != ind3]
# titles.insert(ind1,'meanLW')
titles.insert(ind2,'$LWR$')
titles.insert(ind3, '$NILS_{\u03C3_n}$')
print(titles)
print(titles[8])

# for e,u in enumerate(NILSALL[20:25]):
#     plt.hist(np.array(u).flatten(),bins=100, alpha=0.5, label= str(dataStructure[0][e]))
fig, axs = plt.subplots(2,3)
axs[0,0].hist([np.array(u).flatten() for u in NILSALL[0:5]], bins=100, histtype='step', linewidth=2, label=[str(d) for d in dataStructure[0]])
axs[0,1].hist([np.array(u).flatten() for u in NILSALL[5:10]], bins=100, histtype='step', linewidth=2, label=[str(d) for d in dataStructure[0]])
axs[0,2].hist([np.array(u).flatten() for u in NILSALL[10:15]], bins=100, histtype='step', linewidth=2, label=[str(d) for d in dataStructure[0]])
axs[1,1].hist([np.array(u).flatten() for u in NILSALL[15:20]], bins=100, histtype='step', linewidth=2, label=[str(d) for d in dataStructure[0]])
axs[1,2].hist([np.array(u).flatten() for u in NILSALL[20:25]], bins=100, histtype='step', linewidth=2, label=[str(d) for d in dataStructure[0]])
axs[0,0].set_ylabel("Number of Pixels [N]")
axs[1,1].set_ylabel("Number of Pixels [N]")
axs[0,0].set_xlabel("NILS")
axs[1,1].set_xlabel("NILS")
axs[1,2].set_xlabel("NILS")
for ax in fig.axes:
    ax.set_xlim(0.75,3.75)
axs[1,0].axis('off')
plt.legend()
plt.show()
# plt.plot(NILSnSTD)

fig, axs = plt.subplots(3,1)
nMin, nMax = np.min([NILSALL[20], NILSALL[22], NILSALL[24]]), np.max([NILSALL[20], NILSALL[22], NILSALL[24]])
for i, n in enumerate([NILSALL[20], NILSALL[22], NILSALL[24]]):
    M, N = np.shape(n)
    im = axs[i].imshow(n,vmin=nMin,vmax=nMax)
    axs[i].set_xticks([int(N*(a/6)-1) for a in range(0,7)])
    axs[i].set_yticks([int(M*(b/2)-1) for b in range(0,3)])
    axs[i].set_yticklabels([round_sig(4*y) for y in [-1,0,1]], fontSize=12)
    if i == 1:
        axs[i].set_ylabel('y-position [\u03bcm]', fontSize=18)
    # elif i == 2:
    #     axs[i].set_xlabel('x-position [\u03bcm]', fontSize=18)
    else:
        pass
    # if i < len(tiffs)-1:
    #     axs[i].set_xticklabels([])
    # else:
    axs[i].set_xticklabels([round_sig(2.5*x) for x in [-1, -2/3,-1/3,0,1/3,2/3,1]], fontSize=12)
    fig.tight_layout()
cb = plt.colorbar(im,orientation = 'horizontal', fraction=0.8, anchor = (0.5, 0.0))
cb.ax.tick_params(labelsize='large')
cb.set_label('NILS', size=20)
plt.show()

dataStructure = [dataStructure[i] for i in range(len(dataStructure)) if i != ind1 and i != ind2 and i != ind3]
# dataStructure.insert(ind1, meanLW)
dataStructure.insert(ind2,LWRx)
dataStructure.insert(ind3,NILSnSTD)
print(np.shape(dataStructure))
# dataStructure[8][2], dataStructure[9][2] = dataStructure[8][1], dataStructure[9][1] 
dataStructure[8][2] = dataStructure[8][1]
# print(dataStructure[9][2])
print(dataStructure[8][2])

dF = pd.DataFrame(np.array(dataStructure).T,
                  columns=titles)

# print(len(labels))
# print("Shape of data structure: ", np.shape(dataStructure))
# dF = pd.DataFrame(np.concatenate([labels,avPeaks,sumPeaks,rmsPeaks,
#                              michelsonC,rmsC,[c[0] for c in compositeC],
#                              [f[0] for f in fourierC],[n[0] for n in nilsC]]),
# dF = pd.DataFrame(np.array(dataStructure).T,
#                   columns=['\u03C3','$c_y$',
#                            '$C_M$', '$C_{RMS}$', '$C_{Composite}$',
#                            '$C_{Fourier}$', 'NILS', 'Fidelity'])
correlations = dF.corr() 
plt.rcParams["figure.figsize"] = (8,6)
correlations = np.array(correlations)
correlations[0][1], correlations[1][0] = 0, 0
# print(np.shape(correlations))
sns.heatmap(abs(correlations),cmap='gray_r',vmin=0,vmax=1,annot=True, xticklabels = titles
                                                                    , yticklabels = titles)#,labelsize=10)#,fontSize=2) ,cmap='vlag'
# if save:
#     plt.savefig(savePath + 'correlationsAveraged.pdf')
#     plt.savefig(savePath + 'correlationsAveraged.png', dpi=2000)
plt.show()

sigma = dataStructure[0]
cLength = dataStructure[1]
michelsonC2d = dataStructure[2]
rmsC2d = dataStructure[3]
compositeC2d = dataStructure[4]
fidel = dataStructure[5]
nils2d = dataStructure[6]
nils2dRMSd = dataStructure[7]
lwRMS = dataStructure[8]
# dlwRMS = dataStructure[9]


#OG metrics plot
fig, axs = plt.subplots(3,3)
axs[0,0].plot(sigma[0:5], [1-f for f in fidel[0:5]], 'x:')
axs[0,0].plot(sigma[5:10], [1-f for f in fidel[5:10]], 'x:')
axs[0,0].plot(sigma[10:15], [1-f for f in fidel[10:15]], 'x:')
axs[0,0].plot(sigma[15:20], [1-f for f in fidel[15:20]], 'x:')
axs[0,0].plot(sigma[20:25], [1-f for f in fidel[20:25]], 'x:')
axs[0,0].set_ylabel("$1-Fidelity$")
axs[0,1].plot(sigma[0:5], michelsonC2d[0:5], 'x:')
axs[0,1].plot(sigma[5:10], michelsonC2d[5:10], 'x:')
axs[0,1].plot(sigma[10:15], michelsonC2d[10:15], 'x:')
axs[0,1].plot(sigma[20:25], michelsonC2d[20:25], 'x:')
axs[0,1].plot(sigma[15:20], michelsonC2d[15:20], 'x:')
# axs[0,0].set_title("Michelson")
axs[0,1].set_ylabel("$C_M$")
# # axs[0,0].legend(loc='lower left')
axs[0,2].plot(sigma[0:5], rmsC2d[0:5], 'x:')
axs[0,2].plot(sigma[5:10], rmsC2d[5:10], 'x:')
axs[0,2].plot(sigma[10:15], rmsC2d[10:15], 'x:')
axs[0,2].plot(sigma[15:20], rmsC2d[15:20], 'x:')
axs[0,2].plot(sigma[20:25], rmsC2d[20:25], 'x:')
axs[0,2].set_ylabel("$C_{RMS}$")
axs[1,0].plot(sigma[0:5], compositeC2d[0:5], 'x:')
axs[1,0].plot(sigma[5:10], compositeC2d[5:10], 'x:')
axs[1,0].plot(sigma[10:15], compositeC2d[10:15], 'x:')
axs[1,0].plot(sigma[15:20], compositeC2d[15:20], 'x:')
axs[1,0].plot(sigma[20:25], compositeC2d[20:25], 'x:')
axs[1,0].set_ylabel("$C_{Composite}$")
axs[1,1].plot(sigma[0:5], nils2d[0:5], 'x:')
axs[1,1].plot(sigma[5:10], nils2d[5:10], 'x:')
axs[1,1].plot(sigma[10:15], nils2d[10:15], 'x:')
axs[1,1].plot(sigma[15:20],nils2d[15:20], 'x:')
axs[1,1].plot(sigma[20:25],nils2d[20:25], 'x:')
# axs[1,2].set_title("NILS")
axs[1,1].set_ylabel("$NILS_{mean}$")
axs[1,2].plot(sigma[0:5], nils2dRMSd[0:5], 'x:')
axs[1,2].plot(sigma[5:10], nils2dRMSd[5:10], 'x:')
axs[1,2].plot(sigma[10:15], nils2dRMSd[10:15], 'x:')
axs[1,2].plot(sigma[15:20], nils2dRMSd[15:20], 'x:')
axs[1,2].plot(sigma[20:25], nils2dRMSd[20:25], 'x:')
# axs[1,2].set_title("$NILS_{RMS}$")
axs[1,2].set_ylabel("$NILS_{\u03C3_n}$")
# axs[2,1].set_title("Line Width - RMS")
# axs[,0].plot(sigma[0:5], LWmean[0:5], 'x:')
# axs[2,0].plot(sigma[5:10], LWmean[5:10], 'x:')
# axs[2,0].plot([s for s in [sigma[10],sigma[12],sigma[13],sigma[14]]], [l for l in [LWmean[10],LWmean[12],LWmean[13],LWmean[14]]], 'x:')
# axs[2,0].plot(sigma[15:20], LWmean[15:20], 'x:')
# axs[2,0].plot(sigma[20:25], LWmean[20:25], 'x:')
# # axs[2,0].set_ylim(2.2e-10,.54e-8)
# axs[2,0].set_ylabel("$LW_{mean}$")
axs[2,1].plot([s for s in [sigma[0], sigma[1], sigma[3], sigma[4]]], [l for l in [lwRMS[0],lwRMS[1],lwRMS[3],lwRMS[4]]], 'x:')
axs[2,1].plot(sigma[5:10], lwRMS[5:10], 'x:')
axs[2,1].plot(sigma[10:15], lwRMS[10:15], 'x:')
axs[2,1].plot(sigma[15:20], lwRMS[15:20], 'x:')
axs[2,1].plot(sigma[20:25], lwRMS[20:25], 'x:')
# axs[1,1].set_ylim(0.26e-7,0.29e-7)
# axs[1,1].set_ylabel("$LW_{mean}$")
# axs[1,2].plot([s for s in [sigma[0], sigma[1], sigma[3], sigma[4]]], [l for l in [dlwRMS[0],dlwRMS[1],dlwRMS[3],dlwRMS[4]]], 'x:')
# axs[1,2].plot(sigma[5:10], dlwRMS[5:10], 'x:')
# axs[1,2].plot(sigma[10:15], dlwRMS[10:15], 'x:')
# axs[1,2].plot(sigma[15:20],dlwRMS[15:20], 'x:')
# axs[1,2].plot(sigma[20:25],dlwRMS[20:25], 'x:')
# axs[2,2].set_title("dLW - RMS")
# axs[1,2].set_ylim(2.2e-10,4.2e-10)
axs[2,1].set_ylabel("LWR")
# for ax in fig.axes:
    # ax.set_xticklabels(labels, rotation=45, ha='right')
axs[2,0].axis('off')
axs[2,2].axis('off')
axs[1,0].set_xlabel('\u03C3 [nm]')
axs[2,1].set_xlabel('\u03C3 [nm]')
axs[1,2].set_xlabel('\u03C3 [nm]')
fig.tight_layout()
# fig.subplots_adjust(bottom=0.5,hspace=5.33)   ##  Need to play with this number.
# axs[1,1].legend(labels=['$c_y$ = ' + str(c) for c in [2,4,6,8,10]], bbox_to_anchor=(1.75,-0.35), ncol=5) #loc="lower center"
# if save:
    # plt.savefig(savePath + 'contrastAll.pdf')
    # plt.savefig(savePath + 'contrastAll.png', dpi=2000)
plt.show()


fig, axs = plt.subplots(5,1)

# axs[0].plot([s for s in [sigma[0], sigma[1], sigma[3], sigma[4]]], [l for l in [dlwRMS[0],dlwRMS[1],dlwRMS[3],dlwRMS[4]]], 'x:', label="$c_y = 2 nm$")
# axs[1].plot(sigma[0:5],dlwRMS[5:10], 'x:', label="$c_y = 4 nm$")
# axs[2].plot(sigma[0:5],dlwRMS[10:15], 'x:', label="$c_y = 6 nm$")
# axs[3].plot(sigma[0:5],dlwRMS[15:20], 'x:', label="$c_y = 8 nm$")
# axs[4].plot(sigma[0:5],dlwRMS[20:25], 'x:', label="$c_y = 10 nm$")
# axs[2].set_ylabel("LWR [m]")
# axs[4].set_xlabel('\u03C3 [nm]')
for ax in fig.axes:
    ax.legend(loc='right')
    # ax.set_ylim(2.2e-10,4.2e-10)
fig.tight_layout()
plt.show()