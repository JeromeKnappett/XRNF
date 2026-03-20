#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 14:51:47 2023

@author: -
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.axis import Axis  
import matplotlib.ticker as mticker
# from matplotlib import set_major_formatter
import itertools
import xraydb


plt.rcParams["figure.figsize"] = (4,4)

dataPath = '/user/home/data/HarmonicContam/XPS/Au4f_calcs_new.xlsx'

names =  ['HHC standard high flux settings','HHC standard low flux settings', 'HHC circular pol high flux','HHC cff=1.4 high flux','HHC cff=1.4 low flux']

pickleResults = False
savePath = '/user/home/data/HarmonicContam/plots/'
#None
fmat = 'jpg'

# ['HHC high flux cff=1.4 offset=-3']
#['HHC standard high flux settings','HHC standard low flux settings', 'HHC circular pol high flux','HHC cff=1.4 high flux','HHC cff=1.4 low flux','HHC high flux cff=1.4 offset=-3']
energy = [130,    150,   170,   185,     190,    210,    230,   250,   270,   290,   310,   330,   350]
r_E =    [0.25625,0.2575,0.2583,0.259375,0.25992,0.26088,0.2625,0.2625,0.2625,0.2625,0.2625,0.2625,0.2625]
rows=[None,[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16,17],[18,19,20,21],[22,23,24,25],[26,27,28,29],[30,31,32,33],[34,35,36],[37,38,39],[40,41,42],[43,44,45]]

q = 1.60218e-19 # fundamental electron charge in C

table = []
harmonicContam_MFP = []
harmonicContam = []
FLXX = []
CRNT = []
for _n,n in enumerate(names):
    HCC_MFP = []
    HCC = []
    FLUX = []
    current = []
    print('\n', n)
    if _n >= 2:
        energy = energy[0:12]
    else:
        pass
    for i,e in enumerate(energy):
        if i > 0:
            if rows[i-1] != None:
                [rows[i].append(r) for r in rows[i-1]]
                # srows = sorted(rows[i])
        # else:
        #     srows = rows[i]
        if e > 250:
            nrows = 3
        else:
            nrows = 4
        
        # print(rows[i])
        # print(min(rows[i]))
        # print(max(rows[i]))
        
        table = pd.read_excel(dataPath,
                                 sheet_name = n,
                                 # header = 0,
                                 # index_col = 0,
                                 usecols = "A:M,O:R",
                                 skiprows=rows[i],
                                 nrows = nrows)
        
        fE = list(table['Fundamental Energy'])[0]
        fFlux = list(table['photons/s'])[0]
        fSig = list(table['cross section'])[0]
        fMFP = list(table['IMFP (TPP-2M) (S. Tanuma, C. J. Powell, D. R. Penn:Surf. Interf. Anal. 21(1994)165)'])[0]
        fCurrent = list(table['Measured current'])[0]
        # print(fE)
        # print(xraydb.mirror_reflectivity('Au', 0.0349066, fE, polarization='p'))
        fR = xraydb.mirror_reflectivity('Au', np.deg2rad(2.0), fE, polarization='p')
        
        # Reflectivity of each harmonic at M4
        R = [xraydb.mirror_reflectivity('Au', np.deg2rad(2.0), e, polarization='p') for e in list(table['Harmonic energy'])]
        rR = [r/fR for r in R]
        fFlux = fFlux*fR
        # print(rR[0])
        
        # print(table)
        # print(np.shape(table))
        EpS = [_R*(a/q) for a,_R in zip(list(table['Measured current']),list(table['Responsivity']))] # electrons/second
        # PpS = [(electrons/(energy/3.7)) for electrons, energy in zip(EpS,list(table['Harmonic energy']))] # photons/second
        
        # PpS = [((3.65*current) / (q*energy*res))*(1/ref) for current,energy,res,ref in zip(list(table['Measured current']),list(table['Harmonic energy']),list(table['Responsivity']),R)]
        PpS = [((3.65*current) / (q*energy*res))*(1/ref) for current,energy,res,ref in zip(list(table['Measured current']),list(table['Harmonic energy']),list(table['Responsivity']),R)]
        
        fFlux = PpS[0]
        
        SpA_MFP = [(fSig/s) * (fFlux/f) * (fMFP/m) * a for s,f,m,a in zip(list(table['cross section']),PpS,list(table['IMFP (TPP-2M) (S. Tanuma, C. J. Powell, D. R. Penn:Surf. Interf. Anal. 21(1994)165)']),list(table['area of fundamental peak']))] 
        SpA = [(fSig/s) * (fFlux/f) * a for s,f,a in zip(list(table['cross section']),PpS,list(table['area of fundamental peak']))] 
        
        HC_MFP = [(Ah/As) for Ah,As in zip(list(table['area of harmonic peak']),SpA_MFP)]
        HC = [(Ah/As) for Ah,As in zip(list(table['area of harmonic peak']),SpA)]
        # HC = [Ah / (fFlux * s * l) for Ah,s,l in zip(list(table['area of harmonic peak']),list(table['cross section']),list(table['MFP']))]
        # HC = [(Ah * a) / (fFlux * f * s) for Ah,a,f,s,l in zip(list(table['area of harmonic peak']),list(table['area of fundamental peak']),PpS,list(table['cross section']),list(table['MFP']))]
        
        # Iterating to improve accuracy
        it = 0
        while it < 200:
            # print(n)
            # print('\n here')
            # print(HC[::])
            # print(np.sum(HC))
            FC_MFP = HC_MFP[0] - np.sum(HC_MFP[1::])
            FC = HC[0] - np.sum(HC[1::])
            # print('\n')
            # print(FC)
            # print(FC_MFP)
            # print(np.sum(HC[1::]))
            # print(it)
            # PpS = [(electrons/(energy/3.7)) for electrons, energy in zip(EpS,list(table['Harmonic energy']))] # photons/second
            # print('\n PpS')
            # print(PpS)
            PpS_MFP = PpS
            # fFlux_MFP = FC_MFP*PpS[0]
            PpS[0] = FC*PpS[0]
            PpS_MFP[0] = FC_MFP*PpS_MFP[0]
            # fFlux = PpS[0]
            # print(PpS)
            # print(fFlux*1e-12)
            SpA_MFP = [(fSig/s) * (fFlux/f) * a for s,f,a in zip(list(table['cross section']),PpS_MFP,list(table['area of fundamental peak']))]
            SpA = [(fSig/s) * (fFlux/f) * a for s,f,a in zip(list(table['cross section']),PpS,list(table['area of fundamental peak']))]
            # _SpA = [(f/fFlux) * a for f,a in zip(PpS,list(table['area of fundamental peak']))]
            # print(list(table['area of fundamental peak'])[0])
            # print((fFlux/PpS[0])) #*list(table['area of fundamental peak'])[0])
            # print(_SpA) #*list(table['area of fundamental peak'])[0])
            # print('\n here again')
            # _SpA_MFP[0] = list(table['area of fundamental peak'])[0]
            # _SpA[0] = list(table['area of fundamental peak'])[0]
            
            # SpA_MFP = [(fSig/s)*a for s,a in zip(list(table['cross section']),_SpA_MFP)] 
            # SpA = [(fSig/s)*a for s,a in zip(list(table['cross section']),_SpA)] 
            # print(_SpA[0]*1e-6)
            HC_MFP = [Ah/As for Ah,As in zip(list(table['area of harmonic peak']),SpA_MFP)]
            HC = [Ah/As for Ah,As in zip(list(table['area of harmonic peak']),SpA)]
            # HC = [Ah / (fFlux * s * l) for Ah,s,l in zip(list(table['area of harmonic peak']),list(table['cross section']),list(table['MFP']))]
            # HC = [(Ah * a) / (fFlux * f * s) for Ah,a,f,s,l in zip(list(table['area of harmonic peak']),list(table['area of fundamental peak']),PpS,list(table['cross section']),list(table['MFP']))]
            HC[0] = 1.0 - np.sum(HC[1::])
            HC_MFP[0] = 1.0 - np.sum(HC_MFP[1::])
            
            # print('\n HC')
            # print(HC)
            it = it + 1
        #     plt.plot(HC,label=str(it))
        # plt.legend()
        HCC_MFP.append(HC_MFP)
        HCC.append(HC)
        FLUX.append(fFlux)
        current.append(fCurrent)
        
    # plt.show()
    harmonicContam_MFP.append(HCC_MFP)
    harmonicContam.append(HCC)
    FLXX.append(FLUX)
    CRNT.append(current)

lim = [0.01,35]
fig, axs = plt.subplots(2,2,figsize=(7,7))

# print(harmonicContam_MFP)

for i,H in enumerate(harmonicContam_MFP):
    if i == 0:
        style = '--x'
        
        style = ':.'
        colours = ['r','g']
        name = 'HF (standard)'
        j,k = 0,0
    elif i==1:
        style = ':.'
        colours = ['r','g']
        name = 'LF (standard)'
        j,k = 0,1
    elif i==2:
        pass
        # style = '--o'
        
        # style = ':.'
        # colours = ['r','g']
        # name = 'HF (circpol)'
        # j,k = 2,0
    elif i==3:
        style = '--*'
        
        style = ':.'
        colours = ['r','g']
        name = 'HF (cff=1.4)'
        j,k = 1,0
    elif i==4:
        # pass
        style = ':*'
        
        style = ':.'
        colours = ['r','g']
        name = 'LF (cff=1.4)'
        j,k = 1,1
    elif i==5:
        pass
        # style = ':.'
        # colours = ['r','g']
        # name = 'HF (cff=1.4,offset=-3%)'
        # j,k = 2,1
    # print(H)
    h4 = []
    for h in H:
        try:
            H4 = h[3]
        except IndexError:
            H4 = 0
        h4.append(H4)
    print('\n here')
    print([h[0]*100 for h in H[0:12]])
    # axs[j,k].plot(energy[0:12],[h[0]*100 for h in H[0:12]],style,label='1st: ')#+name)
    if i in [0,1,3,4]:
        axs[j,k].plot(energy[0:12],[h[1] for h in H[0:12]],style,color=colours[0],label='$n=2$')#+name)
        axs[j,k].plot(energy[0:12],[h[2] for h in H[0:12]],style,color=colours[1],label='$n=3$')#+name)
        axs[j,k].plot(energy[0:12],h4[0:12],style,color='b',label='$n=4$')#+name)
        h2 = [h[1] for h in H[0:12]]
        h3 = [h[2] for h in H[0:12]]
        HSUM = [H2 + H3 + H4 for H2,H3,H4 in zip(h2,h3,h4)] #np.sum([h2,h3,h4])
        print(HSUM)
        axs[j,k].plot(energy[0:12],HSUM,style,color='y',label='$n>1$')#+name)
        # axs[j,k].set_title(name)
    # axs[j,k].set_ylim(lim)
    # axs[j,k].set_yscale('log')#,limit_range_for_scale(vmin=0,vmax=35))
    # axs[j,k].set_ylim(lim)
    # axs[j,k].yaxis.set_major_formatter(mticker.ScalarFormatter())
    if pickleResults:
        import pickle
        with open('/user/home/data/HarmonicContam/XPS/' + name + '.pkl','wb') as f:
            pickle.dump(H, f,protocol=2)
            
        with open('/user/home/data/HarmonicContam/XPS/' + name + '_MFP.pkl','wb') as f:
            pickle.dump(harmonicContam_MFP[i], f,protocol=2)
        with open('/user/home/data/HarmonicContam/XPS/' + name + '_FLUX.pkl','wb') as f:
            pickle.dump(FLXX[i], f,protocol=2)
        with open('/user/home/data/HarmonicContam/XPS/' + name + '_CRNT.pkl','wb') as f:
            pickle.dump(CRNT[i], f,protocol=2)
    h4 = []
    
    
axs[1,0].set_xlabel('Photon Energy [eV]')
axs[1,1].set_xlabel('Photon Energy [eV]')
axs[0,0].set_ylabel('$\Phi_n / \Phi$')
axs[1,0].set_ylabel('$\Phi_n / \Phi$')
axs[0,1].legend(['$n=2$','$n=3$','$n=4$','$n>1$'])
# fig.tight_layout()
# plt.legend()
if savePath:
    plt.savefig(savePath+'_vs_flux_n_cff'+'.'+fmat,format=fmat)
plt.show()

names = ['HF ($C_{ff}$=2)','LF ($C_{ff}$=2)','HF ($C_{ff}$=2) circ. pol.','HF ($C_{ff}$=1.4)','LF ($C_{ff}$=1.4)']

for i,H in enumerate(harmonicContam_MFP):
    if i == 0:
        style = '--x'
        
        style = ':.'
        colours = ['r','g']
        name = 'HF (standard)'
        j,k = 0,0
        
    h4 = []
    for h in H:
        try:
            H4 = h[3]
        except IndexError:
            H4 = 0
        h4.append(H4)
        
    plt.plot(energy[0:12],[h[1] for h in H[0:12]],style,color=colours[0],label='$n=2$')#+name)
    plt.plot(energy[0:12],[h[2] for h in H[0:12]],style,color=colours[1],label='$n=3$')#+name)
    plt.plot(energy[0:12],h4[0:12],style,color='b',label='$n=4$')#+name)
    h2 = [h[1] for h in H[0:12]]
    h3 = [h[2] for h in H[0:12]]
    HSUM = [H2 + H3 + H4 for H2,H3,H4 in zip(h2,h3,h4)] #np.sum([h2,h3,h4])
    print(HSUM)
    plt.plot(energy[0:12],HSUM,style,color='y',label='$n>1$')#+name)
    plt.title(names[i])
    plt.xlabel('Photon Energy [eV]',fontsize=12)
    plt.ylabel('$\Phi_n / \Phi$',fontsize=12)
    # plt.ylim([0,35])
    plt.legend()
    if savePath:
        plt.savefig(savePath+names[i]+'.'+fmat,format=fmat)
    plt.show()
    
    0.09603889979560527
    0.0754649120997119
    
    0.03179390996689759
    0.019442455464079918
    
    0.07077310580473885
    0.07527331342826914
# hc = harmonicContam_MFP[0]
# print(hc)
# print([h[3]*100 for h in hc])
# hc2 = [h[1]*100 for h in hc]#[0:12]]
# hc3 = [h[2]*100 for h in hc]#[0:12]]
# hc4 = [h[3]*100 for h in hc]
# plt.plot(energy,hc2,label='2nd')
# plt.plot(energy,hc3,label='3rd')
# plt.plot(energy,hc4,label='4th')
# plt.plot(energy,[c2+c3+c4 for c2,c3,c4 in zip(hc2,hc3,hc4)],label='sum')
# plt.legend()
# plt.xlabel('Photon Energy [eV]')
# plt.ylabel('% $\Phi$')
# plt.show()

fig, axs = plt.subplots(3,1)

for i,H in enumerate(harmonicContam):
    if i == 0:
        style = ':.'
        colours = 'r'
        name = 'HF (standard)'
    elif i==1:
        style = ':.'
        colours = 'g'
        name = 'LF (standard)'
    elif i==2:
        style = ':.'
        colours = 'b'
        name = 'HF (circpol)'
    elif i==3:
        style = ':.'
        colours = 'y'
        name = 'HF (cff=1.4)'
    elif i==4:
        style = ':.'
        colours = 'black'
        name = 'LF (cff=1.4)'
    elif i==5:
        style = ':.'
        colours = 'o'
        name = 'HF (cff=1.4,offset=-3%)'
    # print(np.nanmin(H))
    axs[0].plot(energy[0:12],[h[1] for h in H[0:12]],style,color=colours,label=name)
    axs[1].plot(energy[0:12],[h[2] for h in H[0:12]],style,color=colours,label=name)
    axs[2].plot(energy[0:12],[np.sum(h[1::]) for h in H[0:12]],style,color=colours,label=name)
    axs[0].set_title('2nd Harmonic')
    axs[1].set_title('3rd Harmonic')
    axs[2].set_title('Total Harmonic Content')
    for ax in axs:
        ax.set_xlabel('Photon Energy [eV]')
        ax.set_ylabel('$\Phi_n / \Phi$')
        ax.set_yscale('log')
        ax.yaxis.set_major_formatter(mticker.ScalarFormatter())
    # axs[j,k].set_ylim(lim)
    # axs[j,k].set_yscale('log')#,limit_range_for_scale(vmin=0,vmax=35))
    # axs[j,k].set_ylim(lim)
    axs[0].yaxis.set_major_formatter(mticker.ScalarFormatter())
    
axs[0].legend()
fig.tight_layout()
# plt.legend()
if savePath:
    plt.savefig(savePath+'all_together'+'.'+fmat,format=fmat)
plt.show()

colours = ['r','g','b','y','black','o']
for i,H in enumerate(harmonicContam):
    plt.plot(energy[0:12],[np.sum(h[1::]) for h in H[0:12]],style,color=colours[i],label=names[i])
plt.ylabel('$\zeta$')
plt.xlabel('Photon Energy [eV]')
plt.legend()
if savePath:
    plt.savefig(savePath+'totalContam'+'.'+fmat,format=fmat)
plt.show()