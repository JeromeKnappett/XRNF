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


def round_sig(x, sig=2):
    from math import log10, floor
    if x != 0:
        return round(x, sig-int(floor(log10(abs(x))))-1)
    else:
        return x

    # %%
dirPath = '/user/home/opt/xl/xl/experiments/maskLER_retry/data/'
files = ['contrastMetrics_maskLER_retry_2d.pkl']#,'contrastMetrics350_2d.pkl']
labelX = '$LER$ [um]'#'$\sigma [nm]$'
labelY = ['$C_M$','$C_{RMS}$', '$C_c$','Fidelity','NILS', 'NILS$_{\sigma_n}$', 'LWR [nm]','LER [nm]']
# ['$1 - Fidelity$', '$C_M$', '$C_{RMS}$', '$C_{Composite}$', '$NILS_{mean}$', '$NILS_{\sigma_n}$', '$LWR$']
# labelY = ['$1 - Fidelity$', '$C_M$', '$C_{RMS}$', '$C_{Composite}$', '$NILS_{mean}$', '$LWR$']
# legend = ['$c_y  = 2$','$c_y = 4$','$c_y = 6$','$c_y = 8$','$c_y = 10$']

# pickle.dump([labels,michelsonC2d,rmsC2d,compositeC2d,fidel2d,nils2d,nilsSTD,LWR], f)
savePath = None#'/home/jerome/dev/data/correctedRoughness/contrastWithoutLWR.png'
LERpick = pickle.load(open(dirPath + 'LER__maskLER_retry.pkl', 'rb'))
pick1 = pickle.load(open(dirPath + files[0], 'rb'))
# pick2 = pickle.load(open(dirPath + files[1], 'rb'))

print(LERpick[0])

A1 = [p for p in pick1[1::]]
# A2 = [p for p in pick2[1::]]
# [[1 - p for p in pick[5]], pick[2], pick[3], pick[4], pick[6], pick[7], pick[8]]
# A = [[1 - p for p in pick[5]], pick[2], pick[3], pick[4], pick[6], pick[8]]
X1 = [0.0,0.5,1.0,1.5,2.0,2.5,3.0,3.5,4.0] #[float(p[4:-4]) for p in pick1[0]]
# X2 = [int(p[:-3]) for p in pick2[0]]

print(pick1[0])

fig,ax= plt.subplots(2,3)

ax[0,0].plot(X1,A1[0],'x:',label='50 um')
ax[0,0].set_ylabel(labelY[0])
# ax[0,0].plot(X2,A2[0],'x:',label='350 um')
ax[0,1].plot(X1,[a[0] / 0.6 for a in A1[2]],'x:',label='50 um')
ax[0,1].set_ylabel(labelY[2])
# ax[0,1].plot(X2,[a[0] / 0.6 for a in A2[2]],'x:',label='350 um')
ax[0,2].plot(X1,[a/np.pi for a in A1[4]],'x:',label='50 um')
ax[0,2].set_ylabel(labelY[4])
# ax[0,3].plot(X1,[a for a in A1[4]],'x:',label='50 um')
# ax[0,3].set_ylabel(labelY[4])
# ax[0,2].plot(X2,[1 - a for a in A2[3]],'x:',label='350 um')
# ax[1,0].plot(X2,[a/np.pi for a in A2[4]],'x:',label='350 um')
ax[1,0].plot(X1,[a1*1e9 for a1 in A1[6]],'x:',label='50 um')
ax[1,0].set_ylabel(labelY[6])#'LWR [nm]')
# ax[1,1].plot(X2,[a1/a2 for a1,a2 in zip(A2[5],A2[4])],'x:',label='350 um')
ax[1,1].plot(X1,[a*1e9 for a in LERpick[1]],'x:',label='50 um')
ax[1,1].set_ylabel('LER [nm]')
ax[1,2].plot(X1,[a for a in A1[5]],'x:',label='50 um')
ax[1,2].set_ylabel(labelY[5])
# ax[1,2].plot(X2,[a*1e9 for a in A2[6]],'x:',label='350 um')

for i,a in enumerate(ax):
    for b in a:
        b.set_xlabel('$\sigma_{LER}$')

# .ylabel(labelY[0])
# plt.xlabel(labelX)
# plt.legend()
plt.tight_layout()
plt.show()