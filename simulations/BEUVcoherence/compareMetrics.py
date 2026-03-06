#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  4 11:57:24 2025

@author: -
"""
import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np
import matplotlib.patches as patches
from matplotlib.legend_handler import HandlerTuple

rcParams['figure.figsize']=(3,3.5)
rcParams['figure.dpi']=300
rcParams.update({'font.size': 10})

# [0.5, 1.0, 1.5, 2.0, 2.5, 0.5, 1.0, 1.5, 2.0, 2.5, 0.5, 1.0, 1.5, 2.0, 2.5, 0.5, 1.0, 1.5, 2.0, 2.5, 0.5, 1.0, 1.5, 2.0, 2.5]
# AMPs = [[0.0,1.8957491158975655e-09, 4.837936100237537e-09, 9.055242151064516e-09, 1.2549329850247491e-08, 1.638520045419863e-08], 
#        [0.0,2.0274745981409948e-09, 5.322494415040973e-09, 9.971287489916746e-09, 1.4552004450011793e-08, 1.961328690281936e-08]]

d50 = [50,75,100,125,150,175,200,300]
d350 = [50,75,100,125,150,175,200]

LER50 = [3.13737672319001e-09, 6.298014272635589e-09, 8.125326189682047e-09, 1.055239948118878e-08, 1.178434629528782e-08, 2.091372357924797e-08, 1.9750531825185528e-08, 2.6744588978142044e-08]
# [3.13737672319001e-09, 6.298014272635589e-09, 8.125326189682047e-09, 1.055239948118878e-08, 1.178434629528782e-08, 2.091372357924797e-08, 1.9750531825185528e-08, 2.6744588978142044e-08]
LWR50 = [3.76570645294972e-09, 7.780048614163813e-09, 1.0489807224041986e-08, 1.2064069168246823e-08, 1.7210424990269083e-08, 2.0765752530619084e-08, 2.017947974382717e-08, 3.1003573514347116e-08]
NILS50 = [2.8706083545041152, 2.8811122789153063, 2.870744614488765, 2.893850374345269, 2.773522775434887, 2.80172111792031, 2.642213450364398, 1.9606921638190036]
CDU50 = [4.64648454946472e-09, 7.937649645135814e-09, 1.0567307060418733e-08, 1.2120426800806978e-08, 1.724203622403281e-08, 2.0812614647128366e-08, 2.0206816687068308e-08, 3.1038866603750495e-08]
CLR50 = [0.0, 0.17407638731144148, 0.10763634324132176, 0.0, 0.22791949187403743, 0.0, 0.0, 0.0]
LER350 = [3.814756484900542e-09, 7.342974803782147e-09, 9.244156295227204e-09, 1.1495575955258391e-08, 1.1563028632844116e-08, 2.3404914177614798e-08, 2.3452719024098754e-08]
# [3.814602945863403e-09, 8.053860161119312e-09, 9.593385301346181e-09, 1.2056884034687646e-08, 1.1959917448368975e-08, 2.297265286321477e-08, 2.1328411825734326e-08]
# [3.814756484900542e-09, 7.342974803782147e-09, 9.244156295227204e-09, 1.1495575955258391e-08, 1.1563028632844116e-08, 2.3404914177614798e-08, 2.3470593943188145e-08]
LWR350 = [4.426264488254208e-09, 8.637301591832736e-09, 1.1951245064472721e-08, 1.4487913858309245e-08, 2.2975390598707574e-08, 3.043593059020359e-08, 3.838628272037212e-08]
NILS350 = [2.8373913133227404, 2.659960117602982, 2.3710150395048393, 2.083147578025207, 1.7397288577995194, 1.4233246657116705, 1.0793228774712333]
CDU350 = [5.066672218648173e-09, 8.758177984928551e-09, 1.1995054148825014e-08, 1.452897090451285e-08, 2.2996099489550955e-08, 3.044876347876026e-08, 3.8473048123529616e-08]
CLR350 = [0.0, 0.0, 0.0, 0.06425103907896956, 0.0, 0.0, 0.06474339140614455]

CC50_1 = [0.47990477576358037, 0.45519088398755453, 0.4529375077320989, 0.4293183130436926, 0.3793641540457867, 0.34713377599879863, 0.3736119334392787, 0.3417038957426973]
CC50_2 = [0.36251639704330646, 0.3945039518638782, 0.5502006904967839, 0.34673839238896254, 0.5536914041928277, 0.5690467021803093, 0.4302166296329305, 0.512467824975143]
CC350_1 = [0.4725395560067662, 0.441519072893289, 0.4370320170619713, 0.35209475409651575, 0.32245622822552916, 0.2825403135722022, 0.28592070152335836]
CC350_2 = [0.3613940431892083, 0.39059614976904194, 0.5763955788255603, 0.3423866674612115, 0.5494761362464926, 0.5664487087669928, 0.42196020455441613]
E_off = 0#abs(EFl[0] - EFs[0][0])*100
LWR_off = 0#abs(LWRl[0] - LWRs[0][0])*1e9

# LERs1[0] = [l - LERs1[0][0] for l in LERs1[0][1::]]
# LERs1[1] = [l - LERs1[1][0] for l in LERs1[1][1::]]
# LERs2[0] = [l - LERs2[0][0] for l in LERs2[0][1::]]
# LERs2[1] = [l - LERs2[1][0] for l in LERs2[1][1::]]
# LERs2[2] = [l - LERs2[2][0] for l in LERs2[2][1::]]

# EFs[0] = [l - EFs[0][0] for l in EFs[0][1:-1]]
# EFs[1] = [l - EFs[1][0] for l in EFs[1][1:-2]]
# EFlc[0] = [l - EFl[0] for l in EFlc[0]]
# EFlc[1] = [l - EFl[0] for l in EFlc[1]]
# EFl = [l - EFl[0] for l in EFl[1::]]

# EF0s[0] = [l - EF0s[0][0] for l in EF0s[0][1:-1]]
# EF0s[1] = [l - EF0s[1][0] for l in EF0s[1][1:-2]]
# EF0lc[0] = [l - EF0l[0] for l in EF0lc[0]]
# EF0lc[1] = [l - EF0l[0] for l in EF0lc[1]]
# EF0l = [l - EF0l[0] for l in EF0l[1::]]
    
# LWRs[0] = [l - LWRs[0][0] for l in LWRs[0][1:-1]]
# LWRs[1] = [l - LWRs[1][0] for l in LWRs[1][1:-2]]
# LWRlc[0] = [l - LWRl[0] for l in LWRlc[0]]
# LWRlc[1] = [l - LWRl[0] for l in LWRlc[1]]
# LWRl = [l - LWRl[0] for l in LWRl[1::]]

# CDUs[0] = [c - CDUs[0][0] for c in CDUs[0][1:-1]]
# CDUs[1]  = [c - CDUs[1][0] for c in CDUs[1][1:-2]]
# CDUlc[0] = [c - CDUl[0] for c in CDUlc[0]]
# CDUlc[1] = [c - CDUl[0] for c in CDUlc[1]]
# CDUl = [c - CDUl[0] for c in CDUl[1::]]

# CLRs[0] = [c - CLRs[0][0] for c in CLRs[0][1:-1]]
# CLRs[1]  = [c - CLRs[1][0] for c in CLRs[1][1:-2]]
# CLRlc[0] = [c - CLRl[0] for c in CLRlc[0]]
# CLRlc[1] = [c - CLRl[0] for c in CLRlc[1]]
# CLRl = [c - CLRl[0] for c in CLRl[1::]]

# NILSs[0] = [l - NILSs[0][0] for l in NILSs[0][1:-1]]
# NILSs[1] = [l - NILSs[1][0] for l in NILSs[1][1:-2]]
# NILSlc[0] = [l - NILSl[0] for l in NILSlc[0]]
# NILSlc[1] = [l - NILSl[0] for l in NILSlc[1]]
# NILSl = [l - NILSl[0] for l in NILSl[1::]]

# AMPs1[0] = AMPs1[0][1::]
# AMPs1[1] = AMPs1[1][1::]
# AMPs2[0] = AMPs2[0][1::]
# AMPs2[1] = AMPs2[1][1::]
# AMPs2[2] = AMPs2[2][1::]
# AMPl = AMPl[1::]


# LERs[0] = LERs[0][0:-1]
# LERs[1] = LERs[1][0:-2]
# EFs[0] = EFs[0][0:-1]
# EFs[1] = EFs[1][0:-2]
# EF0s[0] = EF0s[0][0:-1]
# EF0s[1] = EF0s[1][0:-2]
# LWRs[0] = LWRs[0][0:-1]
# LWRs[1] = LWRs[1][0:-2]
# NILSs[0] = NILSs[0][0:-1]
# NILSs[1] = NILSs[1][0:-2]
# AMPs[0] = AMPs[0][0:-1]
# AMPs[1] = AMPs[1][0:-2]
# CDUs[0] = CDUs[0][0:-1]
# CDUs[1] = CDUs[1][0:-2]
# CLRs[0] = CLRs[0][0:-1]
# CLRs[1] = CLRs[1][0:-2]

# dLER = []
# dLWR = []
# dCDU = []
# dAMP = []
# _AMP = [AMPs1[0],AMPs1[1],AMPs2[0],AMPs2[1],AMPs2[2]]
# _LWR = [LWRs1[0],LWRs1[1],LWRs2[0],LWRs2[1],LWRs2[2]]
# _CDU = [CDUs1[0],CDUs1[1],CDUs2[0],CDUs2[1],CDUs2[2]]

# for i,l in enumerate([LERs1[0],LERs1[1],LERs2[0],LERs2[1],LERs2[2]]):
#     for ii,_l in enumerate(l):
#         dLER.append(_l)
#         dLWR.append(_LWR[i][ii])
#         dCDU.append(_CDU[i][ii])
#         dAMP.append(_AMP[i][ii])

# a,b = np.polyfit(dAMP,dLER,1)
# x_fit = np.linspace(0,np.max(dAMP)+0.25,400)
# y_fit = [a*_x*1e9 + b*1e9 for _x in x_fit]


LERlim10 = [0.35,0.78]
LERlim25 = [0.87,1.94]
LWRlim10 = [0.38,0.85]
LWRlim25 = [0.99,2.21]
CDUlim10 = [0.47,1.06]
CDUlim25 = [1.19,2.65]

# Define rectangles: (x, y, width, height)
rectangles = [
    (-1, LERlim10[0], 20, LERlim10[1] - LERlim10[0]),
    (-1, LERlim25[0], 20, LERlim25[1] - LERlim25[0]),
    (-1, LWRlim10[0], 20, LWRlim10[1] - LWRlim10[0]),
    (-1, LWRlim25[0], 20, LWRlim25[1] - LWRlim25[0]),
    (-1, CDUlim10[0], 20, CDUlim10[1] - CDUlim10[0]),
    (-1, CDUlim25[0], 20, CDUlim25[1] - CDUlim25[0])
]

# Define colors and transparency for each rectangle
colors = ['y', 'pink','y', 'pink', 'y', 'pink']#, 'blue']
alphas = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5]




plt.plot(d50,[c/0.6 for c in CC50_1],'rx',mfc='none',label='SSA = 50 um')
plt.plot(d350,[c/0.6 for c in CC350_1],'bx',mfc='none',label='SSA = 350 um')
# plt.plot(d50,[c/0.6 for c in CC50_2],'ro',mfc='none',label='SSA = 50 um')
# plt.plot(d350,[c/0.6 for c in CC350_2],'bo',mfc='none',label='SSA = 350 um')
# Get the current axes
# ax = plt.gca()
# # Add rectangles to the plot
# for (x, y, w, h), color, alpha in zip(rectangles[2:4], colors[2:4], alphas[2:4]):
#     rect = patches.Rectangle((x, y), w, h, linewidth=1, edgecolor=None,
#                               facecolor=color, alpha=alpha)
#     ax.add_patch(rect)
# plt.hlines(0.99,0,np.max(AMPs[0])*1e9,colors='gray',linestyles='--',label='$L_{25}$')
# plt.hlines(0.38,0,np.max(AMPs[0])*1e9,colors='gray',linestyles='--',label='$L_{10}$')
# plt.text(15.1, 1.8,'$L_{25}$',color='black',fontsize=8) # '0.63 nm', color='g')
# plt.text(15.1, 0.46,'$L_{10}$',color='black',fontsize=8) # '0.26 nm', color='y')
plt.xlabel('Grating Separation ($d$) [\u03bcm]')
# plt.ylabel('$\Delta$LWR [nm]')
plt.ylabel('$C_C$')
# plt.xlim((-1,np.max(AMPs[0])*1e9 + 1))
# plt.legend(title='IRDS Limits$^{*}$',fontsize=10)
plt.savefig('/user/home/opt/xl/xl/experiments/BEUVcoherence/figs/compositeC.svg', bbox_inches='tight')
plt.show()




plt.plot(d50,[l*1e9 for l in LER50],'ro',mfc='none',label='SSA = 50 \u03bcm')
plt.plot(d350,[l*1e9 for l in LER350],'bo',mfc='none',label='SSA = 350 \u03bcm')

# Get the current axes
ax = plt.gca()

# # Add rectangles to the plot
# for (x, y, w, h), color, alpha in zip(rectangles[0:2], colors[0:2], alphas[0:2]):
#     rect = patches.Rectangle((x, y), w, h, linewidth=1, edgecolor=None,
#                              facecolor=color, alpha=alpha)
#     ax.add_patch(rect)

# # plt.hlines(0.87,0,np.max(AMPs[0])*1e9,colors='gray',linestyles='--')
# # plt.hlines(0.35,0,np.max(AMPs[0])*1e9,colors='gray',linestyles='--')
# plt.text(15.1,1.6,'$L_{25}$', color='black', fontsize=8)
# plt.text(15.1,0.45,'$L_{10}$', color='black', fontsize=8)
plt.xlabel('Grating Separation ($d$) [\u03bcm]')
# plt.ylabel('$\Delta$LER [nm]')
plt.ylabel('LER [nm]')
# plt.xlim((-1,np.max(AMPs2)*1e9 + 1))
# plt.vlines(2.0,ymin=0.4,ymax=4,colors='gray',linestyles='dashed')
# plt.text(1.6,4.1,'2 nm', color='gray',fontsize=10)#'$\sigma_{EBL}$',color='gray',fontsize=10)
# plt.xlim((0,,np.max(AMPs[0])*1e9))
plt.legend()
plt.savefig('/user/home/opt/xl/xl/experiments/BEUVcoherence/figs/LER_wLegend.svg', bbox_inches='tight')
plt.show()


# plt.plot(d50,[e*1 for e in EF50],'ro',mfc='none',label='$SSA=50um$')
# plt.plot(d350,[e*1 for e in EF350],'bo',mfc='none',label='$SSA=350um$')
# # plt.plot(AMPlc[2],[e*1 - E_off for e in EFlc[2]],':x',color='c',label='line-edge: $c =$' + str(60) + ' nm')
# # plt.plot(AMPlc[3],[e*1 - E_off for e in EFlc[3]],':x',color='m',label='line-edge: $c =$' + str(60) + ' nm')
# plt.xlabel('Mask Roughness Amplitude ($\sigma$) [nm]')
# # plt.ylabel('$\Delta \eta_{\pm 1}$')
# plt.ylabel('$\eta_{\pm 1}$')
# # plt.legend()
# # plt.savefig('/user/home/opt/xl/xl/experiments/maskLER_retry2/figures/EF.svg', bbox_inches='tight')
# plt.show()


# plt.plot(d50,[e*1 for e in EF050],'ro',mfc='none',label='$SSA=50um$')
# plt.plot(d350,[e*1 for e in EF0350],'bo',mfc='none',label='$SSA=350um$')
# # plt.plot(AMPlc[2],[e*1 - E_off for e in EF0lc[2]],':x',color='c',label='line-edge: $c =$' + str(60) + ' nm')
# # plt.plot(AMPlc[3],[e*1 - E_off for e in EF0lc[3]],':x',color='m',label='line-edge: $c =$' + str(60) + ' nm')
# plt.xlabel('Mask Roughness Amplitude ($\sigma$) [nm]')
# # plt.ylabel('$\Delta \eta_{0}$')
# plt.ylabel('$\eta_{0}$')
# # plt.legend()
# # plt.savefig('/user/home/opt/xl/xl/experiments/maskLER_retry2/figures/EF0.svg', bbox_inches='tight')
# plt.show()


plt.plot(d50,[l*1e9 for l in LWR50],'ro',mfc='none',label='SSA = 50 um')
plt.plot(d350,[l*1e9 for l in LWR350],'bo',mfc='none',label='SSA = 50 um')
# Get the current axes
# ax = plt.gca()
# # Add rectangles to the plot
# for (x, y, w, h), color, alpha in zip(rectangles[2:4], colors[2:4], alphas[2:4]):
#     rect = patches.Rectangle((x, y), w, h, linewidth=1, edgecolor=None,
#                               facecolor=color, alpha=alpha)
#     ax.add_patch(rect)
# plt.hlines(0.99,0,np.max(AMPs[0])*1e9,colors='gray',linestyles='--',label='$L_{25}$')
# plt.hlines(0.38,0,np.max(AMPs[0])*1e9,colors='gray',linestyles='--',label='$L_{10}$')
# plt.text(15.1, 1.8,'$L_{25}$',color='black',fontsize=8) # '0.63 nm', color='g')
# plt.text(15.1, 0.46,'$L_{10}$',color='black',fontsize=8) # '0.26 nm', color='y')
plt.xlabel('Grating Separation ($d$) [\u03bcm]')
# plt.ylabel('$\Delta$LWR [nm]')
plt.ylabel('LWR [nm]')
# plt.xlim((-1,np.max(AMPs[0])*1e9 + 1))
# plt.legend(title='IRDS Limits$^{*}$',fontsize=10)
plt.savefig('/user/home/opt/xl/xl/experiments/BEUVcoherence/figs/LWR_redone.svg', bbox_inches='tight')
plt.show()


plt.plot(d50,[n/np.pi for n in NILS50],'ro',mfc='none',label='$SSA=50um$')
plt.plot(d350,[n/np.pi for n in NILS350],'bo',mfc='none',label='$SSA=350um$')
# plt.plot(AMPlc[2],[l*1e9 - LWR_off for l in LWRlc[2]],':x',color='c')#,label='line-edge: $c =$' + str(60) + ' nm')
# plt.plot(AMPlc[3],[l*1e9 - LWR_off for l in LWRlc[3]],':x',color='m')#,label='line-edge: $c =$' + str(60) + ' nm')
# plt.hlines(0.63,0,25,colors='gray',linestyles='--',label='$L_{25}$')
# plt.hlines(0.26,0,25,colors='gray',linestyles='--',label='$L_{10}$')
# plt.text(0, 0.65,'$L_{25}$',color='gray',fontsize=8) # '0.63 nm', color='g')
# plt.text(0, 0.28,'$L_{10}$',color='gray',fontsize=8) # '0.26 nm', color='y')
plt.xlabel('Grating Separation ($d$) [\u03bcm]')
# plt.ylabel('$\Delta$NILS$/\pi$')
plt.ylabel('NILS $/\pi$ ')
# # plt.legend(title='IRDS Limits$^{*}$',fontsize=10)
plt.savefig('/user/home/opt/xl/xl/experiments/BEUVcoherence/figs/NILS.svg', bbox_inches='tight')
plt.show()


# plt.plot([a*1e9 for a in AMPs[0][1::]],[lwr/ler for lwr,ler in zip(LWRs[0][1::],LERs[0][1::])],'ro',mfc='none')#,label='surface: $c =$' + str(35) + ' nm')
# plt.plot([a*1e9 for a in AMPs[1][1::]],[lwr/ler for lwr,ler in zip(LWRs[1][1::],LERs[1][1::])],'bo',mfc='none')#,label='surface: $c =$' + str(65) + ' nm')
# plt.plot(AMPl,[lwr/ler for lwr,ler in zip(LWRl,LERl)],'x',color='black')#,label='line-edge: $c =$' + str(60) + ' nm')
# plt.plot(AMPlc[0],[lwr/ler for lwr,ler in zip(LWRlc[0],LERlc[0])],'x',color='g')#,label='line-edge: $c =$' + str(60) + ' nm')
# plt.plot(AMPlc[1],[lwr/ler for lwr,ler in zip(LWRlc[1],LERlc[1])],'x',color='g')#,label='line-edge: $c =$' + str(60) + ' nm')
# plt.xlabel('Mask Roughness Amplitude ($\sigma$) [nm]')
# plt.ylabel('$\Delta$LWR / $\Delta$LER ')
# plt.ylabel('LWR / LER ')
# plt.savefig('/user/home/opt/xl/xl/experiments/maskLER_retry2/figures/LWRoverLER_delta.svg', bbox_inches='tight')
# plt.show()


plt.plot(d50,[l*1e9 for l in CDU50],'ro',mfc='none',label='$SSA=50um$')
plt.plot(d350,[l*1e9 for l in CDU350],'bo',mfc='none',label='$SSA=350um$')
# Get the current axes
# ax = plt.gca()
# # Add rectangles to the plot
# for (x, y, w, h), color, alpha in zip(rectangles[4::], colors[4::], alphas[4::]):
#     rect = patches.Rectangle((x, y), w, h, linewidth=1, edgecolor=None,
#                               facecolor=color, alpha=alpha)
#     ax.add_patch(rect)
# # plt.hlines(0.87,0,np.max(AMPs[0])*1e9,colors='gray',linestyles='--')
# # plt.hlines(0.35,0,np.max(AMPs[0])*1e9,colors='gray',linestyles='--')
# plt.text(15.1,2.3,'$L_{25}$', color='black', fontsize=8)
# plt.text(15.1,0.7,'$L_{10}$', color='black', fontsize=8)
plt.xlabel('Grating Separation ($d$) [\u03bcm]')
# plt.ylabel('$\Delta$CDU [nm]')
plt.ylabel('CDU [nm]')
# plt.xlim((-1,np.max(AMPs[0])*1e9 + 1))
# plt.vlines(2.0,ymin=0.4,ymax=4,colors='gray',linestyles='dashed')
# plt.text(1.6,4.1,'2 nm', color='gray',fontsize=10)#'$\sigma_{EBL}$',color='gray',fontsize=10)
# plt.xlim((-1,np.max(AMPs[0])*1e9 + 1))
# plt.ylim((-0.1,np.max(CDUs[0])*1e9 + 0.4))
# plt.legend()
plt.savefig('/user/home/opt/xl/xl/experiments/BEUVcoherence/figs/CDU.svg', bbox_inches='tight')
plt.show()


plt.plot(d50,[l for l in CLR50],'ro',mfc='none',label='$SSA=50um$')
plt.plot(d350,[l for l in CLR350],'bo',mfc='none',label='$SSA=350um$')
plt.xlabel('Grating Separation ($d$) [\u03bcm]')
# plt.ylabel('$\Delta$CLR [nm]')
plt.ylabel('CLR [nm]')
# plt.xlim((-1,np.max(AMPs[0])*1e9 + 1))
# plt.vlines(2.0,ymin=0.4,ymax=4,colors='gray',linestyles='dashed')
# plt.text(1.6,4.1,'2 nm', color='gray',fontsize=10)#'$\sigma_{EBL}$',color='gray',fontsize=10)
# plt.xlim((0,,np.max(AMPs[0])*1e9))
# plt.legend()
plt.savefig('/user/home/opt/xl/xl/experiments/BEUVcoherence/figs/CLR.svg', bbox_inches='tight')
plt.show()

X = np.linspace(0.0,np.max(LER50)*1e9,100)
Y = X*np.sqrt(2)# - 2.e-9

plt.plot([l*1e9 for l in LER50],[l*1e9 for l in LWR50],'ro',mfc='none',label='SSA = 50 \u03bcm')
plt.plot([l*1e9 for l in LER350],[l*1e9 for l in LWR350],'bo',mfc='none',label='SSA = 350 \u03bcm')
# plt.plot(LERl,LWRl,'x',color='black')#,label='line-edge: $c =$' + str(60) + ' nm')
# plt.plot(LERlc[0],LWRlc[0],'x',color='g')#,label='line-edge: $c =$' + str(60) + ' nm')
# plt.plot(LERlc[1],LWRlc[1],'x',color='g')#,label='line-edge: $c =$' + str(60) + ' nm')
plt.plot(X,Y,':', label='LWR = $\sqrt{2}$LER')
plt.xlabel('LER [nm]')
# plt.ylabel('$\Delta$LWR / $\Delta$LER ')
plt.legend()
plt.ylabel('LWR [nm]')
plt.savefig('/user/home/opt/xl/xl/experiments/BEUVcoherence/figs/LWRoverLER.svg', bbox_inches='tight')
plt.show()


plt.plot([100*(abs((n1/np.pi) - (n2/np.pi)) / ((n1/np.pi) + (n2/np.pi))) for n1,n2 in zip(NILS50,NILS350)],'x')
    # [(n1/np.pi) - (n2/np.pi) for n1,n2 in zip(NILS50,NILS350)],'x')
plt.show()

# Bler11 = [((l*1e9) / 1.2)**2 for l in dLER] 
# Blwr11 = [((l*1e9) / 1.4)**2 for l in dLWR]
# Bcdu11 = [((l*1e9) / 1.7)**2 for l in dCDU]

# Bler10 = [((l*1e9) / 1.1)**2 for l in dLER] 
# Blwr10 = [((l*1e9) / 1.2)**2 for l in dLWR]
# Bcdu10 = [((l*1e9) / 1.5)**2 for l in dCDU]

# Bler8 = [((l*1e9) / 0.8)**2 for l in dLER] 
# Blwr8 = [((l*1e9) / 1.0)**2 for l in dLWR]
# Bcdu8 = [((l*1e9) / 1.2)**2 for l in dCDU]




# fig, ax = plt.subplots(1,1)
# p8e, = ax.plot(dAMP,[1 - b for b in Bler8],'ro',mfc='none')#,label='CD = 8 nm')
# p10e, = ax.plot(dAMP,[1 - b for b in Bler10],'bo',mfc='none')#,label='CD = 10 nm')
# p11e, = ax.plot(dAMP,[1 - b for b in Bler11],'go',mfc='none')#,label='CD = 11 nm')
# # p8w, = ax.plot(dAMP,Blwr8,'ro',mfc='none')#,label='CD = 8 nm')
# # p10w, = ax.plot(dAMP,Blwr10,'bo',mfc='none')#,label='CD = 10 nm')
# # p11w, = ax.plot(dAMP,Blwr11,'go',mfc='none')#,label='CD = 11 nm')
# ax.set_xlabel('Mask Roughness Amplitude ($\sigma$) [nm]')
# ax.set_ylabel(r'1 - $\omega$ (LER)')
# ax.set_ylim((0,1))
# ax.set_xlim((0,5))
# # ax.legend([(p8e,p8w),(p10e,p10w),(p11e,p11w)], ['CD = 8 nm', 'CD = 10 nm', 'CD = 11 nm'],
# #             handler_map={tuple: HandlerTuple(ndivide=None)},
# #             title='X/O : LER/LWR')#' \n O = LWR')
# # l = ax.legend([(p8e, p8w), p10e], ['data', 'models'],
# #                handler_map={tuple: HandlerTuple(ndivide=None)})
# # ax.legend()
# plt.savefig('/user/home/opt/xl/xl/experiments/maskLER_retry2/figures/omega_LER.svg', bbox_inches='tight')
# plt.show()

# plt.plot(dAMP,[1 - b for b in Blwr8],'ro',mfc='none',label='CD = 8 nm')
# plt.plot(dAMP,[1 - b for b in Blwr10],'bo',mfc='none',label='CD = 10 nm')
# plt.plot(dAMP,[1 - b for b in Blwr11],'go',mfc='none',label='CD = 11 nm')
# plt.xlabel('Mask Roughness Amplitude ($\sigma$) [nm]')
# plt.ylim((0,1))
# plt.xlim((0,5))
# plt.ylabel(r'1 - $\omega$ (LWR)')
# plt.legend()
# plt.savefig('/user/home/opt/xl/xl/experiments/maskLER_retry2/figures/omega_LWR.svg', bbox_inches='tight')
# plt.show()


# plt.plot(dAMP,[1 - b for b in Bcdu8], 'ro', mfc='none')
# plt.plot(dAMP,[1 - b for b in Bcdu10], 'bo', mfc='none')
# plt.plot(dAMP,[1 - b for b in Bcdu11], 'go', mfc='none')
# plt.xlabel('Mask Roughness Amplitude ($\sigma$) [nm]')
# plt.ylim(0,1)
# plt.xlim(0,5)
# plt.ylabel(r'1 - $\omega$ (CDU)')
# plt.savefig('/user/home/opt/xl/xl/experiments/maskLER_retry2/figures/omega_CDU.svg', bbox_inches='tight')
# plt.show()


# plt.plot(dAMP,[1 - b for b in Bler11], 'ro', mfc='none', label='LER')
# plt.plot(dAMP,[1 - b for b in Blwr11], 'bo', mfc='none', label='LWR')
# plt.plot(dAMP,[1 - b for b in Bcdu11], 'go', mfc='none', label='CDU')
# plt.xlabel('Mask Roughness Amplitude ($\sigma$) [nm]')
# plt.ylabel(r'1 - $\omega$')
# plt.ylim(0,1)
# plt.xlim(0,5)
# plt.title('CD = 11 nm')
# plt.legend()
# plt.savefig('/user/home/opt/xl/xl/experiments/maskLER_retry2/figures/omega_CD11.svg', bbox_inches='tight')
# plt.show()

# plt.plot(dAMP,[1 - b for b in Bler10], 'ro', mfc='none', label='LER')
# plt.plot(dAMP,[1 - b for b in Blwr10], 'bo', mfc='none', label='LWR')
# plt.plot(dAMP,[1 - b for b in Bcdu10], 'go', mfc='none', label='CDU')
# plt.xlabel('Mask Roughness Amplitude ($\sigma$) [nm]')
# plt.ylabel(r'1 - $\omega$')
# plt.ylim(0,1)
# plt.xlim(0,5)
# plt.title('CD = 10 nm')
# plt.legend()
# plt.savefig('/user/home/opt/xl/xl/experiments/maskLER_retry2/figures/omega_CD10.svg', bbox_inches='tight')
# plt.show()
    
# plt.plot(dAMP,[1 - b for b in Bler8], 'ro', mfc='none', label='LER')
# plt.plot(dAMP,[1 - b for b in Blwr8], 'bo', mfc='none', label='LWR')
# plt.plot(dAMP,[1 - b for b in Bcdu8], 'go', mfc='none', label='CDU')
# plt.xlabel('Mask Roughness Amplitude ($\sigma$) [nm]')
# plt.ylabel(r'1 - $\omega$')
# plt.ylim(0,1)
# plt.xlim(0,5)
# plt.title('CD = 8 nm')
# plt.legend()
# plt.savefig('/user/home/opt/xl/xl/experiments/maskLER_retry2/figures/omega_CD8.svg', bbox_inches='tight')
# plt.show()

# # plt.plot(LWR/LER,AMPs[0],'ro',mfc='none')
# # plt.plot(LWR/LER,AMPs[1],'bo',mfc='none')#,label='surface: $c =$' + str(65) + ' nm')
# # plt.plot(LWR/LER,AMPl,'x',color='black')#,label='line-edge: $c =$' + str(60) + ' nm')
# # plt.plot(LWR/LER,AMPlc[0],'x',color='g')#,label='line-edge: $c =$' + str(60) + ' nm')
# # plt.plot([lw/le for lw,le in zip(LWR,LER)],AMPlc[1],'x',color='g')#,label='line-edge: $c =$' + str(60) + ' nm')
# # # plt.plot(X,Y,':')
# # plt.xlabel('Mask Roughness Amplitude ($\sigma$) [nm]')
# # # plt.ylabel('$\Delta$LWR / $\Delta$LER ')
# # plt.ylabel('LWR/LER')
# # # plt.savefig('/user/home/opt/xl/xl/experiments/maskLER_retry2/figures/LWRoverLER.svg', bbox_inches='tight')
# # plt.show()