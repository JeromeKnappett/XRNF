#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 24 15:49:16 2021

@author: jerome
"""

import numpy as np
import matplotlib.pyplot as plt
import pickle
from matplotlib.font_manager import FontProperties
import plt_style
import pickle

def round_sig(x, sig=2):
    from math import floor, log10
    if x != 0:
        return round(x, sig-int(floor(log10(abs(x))))-1)
    else:
        return x

colours = plt.rcParams["axes.prop_cycle"].by_key()["color"]

dirPath = '/home/jerome/dev/data/contrast/'
savePath = dirPath

save = True

with open(dirPath + 'compositeTE.pkl', 'rb') as y:
    cte = pickle.load(y)
with open(dirPath + 'compositeTM.pkl', 'rb') as p:
    ctm = pickle.load(p)
with open(dirPath + 'fourierTE.pkl', 'rb') as q:
    fte = pickle.load(q)
with open(dirPath + 'fourierTM.pkl', 'rb') as r:
    ftm = pickle.load(r)
with open(dirPath + 'michelsonTE.pkl', 'rb') as z:
    mte = pickle.load(z)
with open(dirPath + 'michelsonTM.pkl', 'rb') as o:
    mtm = pickle.load(o)
with open(dirPath + 'nilsTE.pkl', 'rb') as bH1:
    nte = pickle.load(bH1)
with open(dirPath + 'nilsTM.pkl', 'rb') as bH2:
    ntm = pickle.load(bH2)
with open(dirPath + 'rmsTE.pkl', 'rb') as bH3:
    rte = pickle.load(bH3)
with open(dirPath + 'rmsTM.pkl', 'rb') as bH4:
    rtm = pickle.load(bH4)

pitch = [round_sig(n,sig=5) for n in np.linspace(10e-9,100e-9,201)]

fig, ax1 = plt.subplots()
ax2 = ax1.twinx()

ax1.plot(pitch, mtm, label='Michelson')
ax1.plot(pitch, rtm, label='RMS')
ax1.plot(pitch, [c[0] for c in ctm], label='Composite')
ax1.plot(pitch, [c[1] for c in ctm], label='MDR')
ax1.plot(pitch, [c[2] for c in ctm], label='Imbalance')
ax1.plot(pitch, ftm, label='Fourier')
ax2.plot(pitch, [n[0] for n in ntm], ':', label='NILS')
# ax2.plot(pitch, [n[4] for n in ntm], ':', label=' rms NILS')
#    ax1.plot(pitch, fidel, '--', label='Fidelity')
ax1.legend(loc='lower center')
ax2.legend()
# ax2.set_ylabel("Fidelity")
ax2.set_ylabel("NILS")
ax1.set_ylabel("Aerial Image Contrast (TM-TM)")
ax1.set_xlabel("Grating Pitch")
ax1.set_xlabel("Grating Pitch ($p_G$) [nm]")
ax1.set_xticklabels([1e9*np.max(pitch)*a for a in [0,1/5,2/5,3/5,4/5,1]])
if save:
    plt.savefig(savePath + 'TM_Contrast.pdf')
    plt.savefig(savePath + 'TM_Contrast.png', dpi=2000)
else:
    pass
plt.show()


fig, ax1 = plt.subplots()
ax2 = ax1.twinx()

ax1.plot(pitch, mte, label='Michelson')
ax1.plot(pitch, rte, label='RMS')
ax1.plot(pitch, [c[0] for c in cte], label='Composite')
ax1.plot(pitch, [c[1] for c in cte], label='MDR')
ax1.plot(pitch, [c[2] for c in cte], label='Imbalance')
ax1.plot(pitch, fte, label='Fourier')
# ax2.plot(pitch, [n[0] for n in nte], ':', label='mean NILS')
# ax2.plot(pitch, [n[4] for n in nte], ':', label=' rms NILS')
ax1.legend(loc='lower center')
# ax2.legend()
# ax2.set_ylabel("Fidelity")
ax2.set_ylabel("NILS")
ax1.set_ylabel("Aerial Image Contrast (TE-TE)")
ax1.set_xlabel("Grating Pitch ($p_G$) [nm]")
ax1.set_xticklabels([1e9*np.max(pitch)*a for a in [0,1/5,2/5,3/5,4/5,1]])
if save:
    plt.savefig(savePath + 'TE_Contrast.pdf')
    plt.savefig(savePath + 'TE_Contrast.png', dpi=2000)
else:
    pass
plt.show()


fig, axs = plt.subplots(2,3)

axs[0,0].plot(pitch, mtm, label='TM')
axs[0,0].plot(pitch, mte, label='TE')
axs[0,0].legend()
axs[0,0].set_title("Michelson")
axs[0,0].set_ylabel("Contrast")
axs[0,1].plot(pitch, rtm, label='TM')
axs[0,1].plot(pitch, rte, label='TE')
axs[0,1].legend()
axs[0,1].set_title("RMS")
axs[0,2].plot(pitch, [c[0] for c in ctm], label='TM')
axs[0,2].plot(pitch, [c[0] for c in cte], label='TE')
axs[0,2].legend()
axs[0,2].set_title("Composite")
axs[1,0].plot(pitch, ftm, label='TM')
axs[1,0].plot(pitch, fte, label='TE')
axs[1,0].legend()
axs[1,0].set_title("Fourier")
axs[1,0].set_ylabel("Contrast")
axs[1,0].set_xlabel('$p_G$')
axs[1,1].plot(pitch, [c[2] for c in ctm], label='TM')
axs[1,1].plot(pitch, [c[2] for c in cte], label='TE')
axs[1,1].legend()
axs[1,1].set_title("Imbalance")
axs[1,1].set_xlabel('$p_G$')
axs[1,2].plot(pitch, [n[0] for n in ntm], label='TM')
axs[1,2].plot(pitch, [n[0] for n in nte], label='TE')
axs[1,2].legend()
axs[1,2].set_title("NILS")
axs[1,2].set_xlabel('$p_G$')
axs[1,2].set_ylabel("NILS")
# for ax in axs[:,:]:
axs[0,0].set_xticklabels([2e9*np.max(pitch)*a for a in [0,1/4,1/2,3/4,1]])
axs[0,1].set_xticklabels([2e9*np.max(pitch)*a for a in [0,1/4,1/2,3/4,1]])
axs[0,2].set_xticklabels([2e9*np.max(pitch)*a for a in [0,1/4,1/2,3/4,1]])
axs[1,0].set_xticklabels([2e9*np.max(pitch)*a for a in [0,1/4,1/2,3/4,1]])
axs[1,1].set_xticklabels([2e9*np.max(pitch)*a for a in [0,1/4,1/2,3/4,1]])
axs[1,2].set_xticklabels([2e9*np.max(pitch)*a for a in [0,1/4,1/2,3/4,1]])
fig.tight_layout()
if save:
    plt.savefig(savePath + 'TETM_Contrast.pdf')
    plt.savefig(savePath + 'TETM_Contrast.png', dpi=2000)
else:
    pass
plt.show()