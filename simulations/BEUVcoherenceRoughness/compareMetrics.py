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

AMPs1 = [[4.1, 8.1, 12.4, 15.5],# 21.4],
         [4.5, 9.5, 13.1]]#, 18.7, 24.3]]
AMPs2 = [[5.4, 10.4, 16.8],# 21.1, 28.4],
         [5.9, 12.5],# 18.1, 26.9, 29.9],
         [6.9, 13.4]]#, 22.0, 27.6, 36.3]]

LERi1 = 3.1607450146927265e-09 #2.8054819585299972e-09
LERi2 = 7.64326171478159e-09 #1.2036794426916629e-08
EFi1 = 0.0196337996370894
EFi2 = 0.015093850171848673
EF0i1 = 0.3737137884351939
EF0i2 = 0.3646827293037703
LWRi1 = 3.647081620744343e-09
LWRi2 = 1.3136891239674473e-08
CDUi1 = 4.0843517676927076e-09
CDUi2 = 1.542430994012242e-08
CLRi1 = 0.20732863481710878
CLRi2 = 0.3311776518423789
NILSi1 = 2.0996178928737277
NILSi2 = 0.93326759274242

ideals = [LERi1,LERi2,EFi1,EFi2,EF0i1,EF0i2,LWRi1,LWRi2,CDUi1,CDUi2,CLRi1,CLRi2,NILSi1,NILSi2]

LERs1 = [[3.7261536609128895e-09, 5.2072639617356e-09, 7.108179410901867e-09, 7.941028700794521e-09],# 9.356224104216244e-09,
         [3.875050630168276e-09, 5.7976854899762335e-09, 7.619003005455367e-09]]#, 8.916935740707048e-09, 9.708894562965612e-09

# [[3.4276575781921522e-09, 5.449992912118864e-09, 7.910385776644557e-09, 9.142162133507221e-09],# 1.0202850449692418e-08],
         # [3.7196606163901497e-09, 6.539113874367776e-09, 8.845756531733933e-09]]#, 1.0067720991040138e-08, 1.1494850593343638e-08]]
LERs2 = [[1.0389560727140874e-08, 1.2867315012354414e-08, 1.4181014347905319e-08],# 1.5625537791620487e-08, 1.7208072533517255e-08, 
         [9.541466955958114e-09, 1.1790917217887792e-08],# 1.3770530194244056e-08, 1.4163786599509075e-08, 1.5314664505614583e-08, 
         [1.024349750383675e-08, 1.2452023768278332e-08]]#, 1.4063581207035406e-08, 1.5155157264403266e-08, 1.6680982502394474e-08


# [[1.1075842632468046e-08, 1.2227716839781921e-08, 1.3625777836728238e-08],# 1.4529760909438248e-08, 1.6934482814741007e-08],
#          [1.2679817380990724e-08, 1.1792143650930597e-08],# 1.2721899332398716e-08, 1.3093881044949024e-08, 1.3900200270738866e-08],
#          [1.2314357586915656e-08, 1.2150936074433785e-08]]# 1.284678867746724e-08, 1.440357949543175e-08, 1.5983165751337032e-08]]


# [[1.4555755977069698e-08, 1.4117544063727275e-08, 1.4903949553806088e-08],# 1.5410950697199763e-08, 1.749152050927735e-08],
#          [1.6063889977504068e-08, 1.4521042560011403e-08],# 1.4660079372622925e-08, 1.462891071619916e-08, 1.549261728219116e-08],
#          [1.610828648983387e-08, 1.9705822838970256e-08]]#, 1.4737317741180919e-08, 1.857915426984802e-08, 1.7510652720960238e-08]]
LERe1 = [[6.798872253801575e-10, 7.371275826395969e-10, 9.138828777538342e-10, 8.709745774734087e-10],# 1.1180895705396292e-09, 
         [7.259554414584677e-10, 7.330294589243062e-10, 9.108880333743866e-10]]#, 9.315651188132437e-10, 1.3644887406392314e-09]]

LERe2 = [[5.6459021863578875e-09, 2.7222642690142586e-09, 1.923341642297551e-09],# 2.119851722850235e-09, 1.936874794569016e-09, 
         [0, 3.080754909765566e-09],# 3.347170164857119e-09, 2.2841360956124416e-09, 2.6525977195182065e-09, 
         [6.405949266675216e-09, 3.810949991602124e-09]]#, 2.504622340605443e-09, 2.2980556783469044e-09, 2.046353572430948e-09]]

LERc1 = [[6.962939103405197e-08, 7.001942800239504e-08, 7.817112904632521e-08, 7.634808211214057e-08],# 8.318012306450662e-08, 
         [6.853114811306416e-08, 7.124322437870423e-08, 7.95694541290715e-08]]#, 8.578716917293406e-08, 1.1085966169293116e-07]

LERc2 = [[6.640151720706334e-08, 1.0774313609054975e-07, 1.0978493777138264e-07],# 1.304041227077944e-07, 1.3918972731953638e-07, 
         [5e-08, 6.92190717975995e-08],# 7.92671860746456e-08, 8.681826628004835e-08, 1.1314365337265432e-07, 
         [6.433567785163536e-08, 7.255233436919013e-08]]#, 7.947251825669026e-08, 1.3095576405196223e-07, 1.1238811658268242e-07]]

EFs1 = [[0.011334939552669421, 0.00973261870529341, 0.008902381266043495, 0.0070366300683740194],# 0.007310827973110793],
        [0.010861230137595393, 0.00993360535729353, 0.007980375040016367]]#, 0.007580746007634057, 0.006662799220310095]]
EFs2 = [[0.011546169314870392, 0.009531388106326163, 0.007362081048431609],# 0.00647308722499533, 0.005366867638228557],
        [0.011936060811521845, 0.010135471234779895],# 0.00870632068131372, 0.007206792749506207, 0.005951636620841627],
        [0.011626057915944264, 0.009518435415991056]]#, 0.008135524967331945, 0.006398999059778816, 0.005662170625364543]]

# [[0.01350966, 0.01250429, 0.012075,   0.01064718,0.00968001], [0.01340222, 0.0115262,  0.01102112, 0.00985921, 0.00860822]]
EF0s1 = [[0.22219355166370452, 0.18087545509379907, 0.15571027729573023, 0.1340360068476132],# 0.10954653910156606],
        [0.20806152658564686, 0.17545295750284257, 0.1529813268002976]]#, 0.12211493641002986, 0.10009186073820724]]
EF0s2 = [[0.2790653059338022, 0.2231489550615145, 0.16238011845679204],# 0.13607968446154145, 0.0999069459389053],
         [0.291208612028796, 0.24206030669965367],# 0.19980736256403264, 0.16367889087895687, 0.12445116760841574],
         [0.2834589014671881, 0.22503118791780446]]#, 0.18537356842109687, 0.13779577194584725, 0.11357312793234227]]

LWRs1 = [[5.035241244320599e-09, 8.306822122737306e-09, 1.199994074327729e-08, 1.462978031513632e-08],# 1.704054276354152e-08],
         [5.590778387598818e-09, 9.542567396440916e-09, 1.3650742563604748e-08]]#, 1.7341369713319563e-08, 1.8245339405073083e-08]]
LWRs2 = [[1.6285466246820527e-08, 2.2694188326090104e-08, 2.6524080102003717e-08],# 2.8756665252726438e-08, 3.090461217861144e-08],
         [1.5160421409916145e-08, 1.951254203651511e-08],# 2.3322132350252588e-08, 2.5811410399632673e-08, 2.7519763430471843e-08],
         [1.5578447883381446e-08, 2.0027433400991886e-08]]#, 2.4529129907019714e-08, 2.8701630261774727e-08, 3.018100264911589e-08]]

CDUs1 = [[5.844825665453213e-09, 8.755070243822064e-09, 1.2481559629569354e-08, 1.5165704881254044e-08],# 1.755314208288055e-08],
        [6.256422938088322e-09, 9.980453707506761e-09, 1.4191831698975662e-08]]#, 1.7727507698240602e-08, 1.981470221261526e-08]]
CDUs2 = [[1.790187171806814e-08, 2.3454619086364923e-08, 2.7133480892145634e-08],# 2.884705369547864e-08, 3.034294863935049e-08],
         [1.700780468439949e-08, 2.0423421609766812e-08],# 2.4104135404329823e-08, 2.6198295187563332e-08, 2.7617480354649458e-08],
         [1.7306755814760954e-08, 2.1063551081252504e-08]]#, 2.480399444181133e-08, 2.851981288844928e-08, 3.0177778537318245e-08]]

CLRs1 = [[0.7688672025844802, 1.1333722085110478, 1.3260758722684782, 1.4440303121963947],# 1.6486915290248056],
        [0.9013104299138164, 1.2507514810432698, 1.4291207419469585]]#, 1.623206225539519, 1.7785735642135605]]
CLRs2 = [[1.111493236039025, 1.3380522155796637, 1.3859351981331485],# 1.4454106186885605, 1.488309552144379],
         [0.9705569012321801, 1.233058779958171],# 1.3252401627518644, 1.3934554508441936, 1.420281884082206],
         [1.0918162677873242, 1.2734860326757291]]#, 1.3720634465525077, 1.405278025438921, 1.4465343390367909]]
# [[4.849588006287376e-09,5.980141355511317e-09, 8.809359324012706e-09, 1.2157013328256315e-08, 1.4387681264393688e-08, 1.6929602120538544e-08],
#         [4.849588006287376e-09,6.439488981484628e-09, 1.0078107365692731e-08, 1.3729426568735085e-08, 1.7340892928309294e-08, 1.8416352950990274e-08]]

# [[1.85248819114021e-10,2.0293692376721032e-10, 2.105608057014916e-10, 2.2527768329039195e-10, 2.6003221852643e-10, 2.865896661301679e-10],
       # [1.85248819114021e-10,2.062957563436123e-10, 2.131014365695951e-10, 2.5570734944935685e-10, 2.6909820644099464e-10, 3.3771092230988193e-10]]

NILSs1 = [[2.105292245208747, 2.1034089907687465, 2.062532008480139, 2.016015828424365],# 1.9587492916544438],
         [2.119993703712176, 2.095748180007353, 2.0471436017689557]]#, 1.997299982843545, 1.9300794614172603]]
NILSs2 = [[0.8851250294567251, 0.8727636010592683, 0.8529903760992077],# 0.8240317575842223, 0.7914921851594128],
          [0.8636689068836376, 0.8595835318504554],# 0.8500722259008557, 0.8321018285296253, 0.8144374462086735],
          [0.8635888981202827, 0.8583818356041574]]#, 0.8425396466472169, 0.8188914207129104, 0.787468204244999]]
E_off = 0#abs(EFl[0] - EFs[0][0])*100
LWR_off = 0#abs(LWRl[0] - LWRs[0][0])*1e9



LERs1[0] = [l - LERi1 for l in LERs1[0]]
LERs1[1] = [l - LERi1 for l in LERs1[1]]
LERs2[0] = [l - LERi2 for l in LERs2[0]]
LERs2[1] = [l - LERi2 for l in LERs2[1]]
LERs2[2] = [l - LERi2 for l in LERs2[2]]

EFs1[0] = [l - EFi1 for l in EFs1[0]]
EFs1[1] = [l - EFi1  for l in EFs1[1]]
EFs2[0] = [l - EFi2  for l in EFs2[0]]
EFs2[1] = [l - EFi2 for l in EFs2[1]]
EFs2[2] = [l - EFi2 for l in EFs2[2]]

EF0s1[0] = [l - EF0i1 for l in EF0s1[0]]
EF0s1[1] = [l - EF0i1 for l in EF0s1[1]]
EF0s2[0] = [l - EF0i2 for l in EF0s2[0]]
EF0s2[1] = [l - EF0i2 for l in EF0s2[1]]
EF0s2[2] = [l - EF0i2 for l in EF0s2[2]]
    
LWRs1[0] = [l - LWRi1 for l in LWRs1[0]]
LWRs1[1] = [l - LWRi1 for l in LWRs1[1]]
LWRs2[0] = [l - LWRi2 for l in LWRs2[0]]
LWRs2[1] = [l - LWRi2 for l in LWRs2[1]]
LWRs2[2] = [l - LWRi2 for l in LWRs2[2]]

CDUs1[0] = [c - CDUi1 for c in CDUs1[0]]
CDUs1[1] = [c - CDUi1 for c in CDUs1[1]]
CDUs2[0] = [c - CDUi2 for c in CDUs2[0]]
CDUs2[1] = [c - CDUi2 for c in CDUs2[1]]
CDUs2[2] = [c - CDUi2 for c in CDUs2[2]]

CLRs1[0] = [c - CLRi1 for c in CLRs1[0]]
CLRs1[1] = [c - CLRi1 for c in CLRs1[1]]
CLRs2[0] = [c - CLRi2 for c in CLRs2[0]]
CLRs2[1] = [c - CLRi2 for c in CLRs2[1]]
CLRs2[2] = [c - CLRi2 for c in CLRs2[2]]

NILSs1[0] = [l - NILSi1 for l in NILSs1[0]]
NILSs1[1] = [l - NILSi1 for l in NILSs1[1]]
NILSs2[0] = [l - NILSi2 for l in NILSs2[0]]
NILSs2[1] = [l - NILSi2 for l in NILSs2[1]]
NILSs2[2] = [l - NILSi2 for l in NILSs2[2]]

# # AMPs1[0] = AMPs1[0][1::]
# AMPs1[1] = AMPs1[1][1::]
# AMPs2[0] = AMPs2[0][1::]
# AMPs2[1] = AMPs2[1][1::]
# AMPs2[2] = AMPs2[2][1::]
# AMPl = AMPl[1::]

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

# plt.errorbar(AMPs1[0],[l*1e9 for l in LERs1[0]],[l*1e9 for l in LERe1[0]],marker='o',linestyle='',color='r',mfc='none',label='$d=27.5$ \u03bcm ($c =$' + str(47) + ' nm)')
# plt.errorbar(AMPs1[1],[l*1e9 for l in LERs1[1]],[l*1e9 for l in LERe1[1]],marker='o',linestyle='',color='b',mfc='none',label='$d=27.5$ \u03bcm ($c =$' + str(83) + ' nm)')
# plt.errorbar(AMPs2[0],[l*1e9 for l in LERs2[0]],[l*1e9 for l in LERe2[0]],marker='x',linestyle='',color='g',label='$d=50$ \u03bcm ($c =$' + str(64) + ' nm)')
# plt.errorbar(AMPs2[1],[l*1e9 for l in LERs2[1]],[l*1e9 for l in LERe2[1]],marker='x',linestyle='',color='orange',label='$d=50$ \u03bcm ($c =$' + str(110) + ' nm)')
# plt.errorbar(AMPs2[2],[l*1e9 for l in LERs2[2]],[l*1e9 for l in LERe2[2]],marker='x',linestyle='',color='c',label='$d=50$ \u03bcm ($c =$' + str(145) + ' nm)')
plt.plot(AMPs1[0],[l*1e9 for l in LERs1[0]],'ro',mfc='none',label='$d=27.5$ \u03bcm ($c =$' + str(47) + ' nm)')
plt.plot(AMPs1[1],[l*1e9 for l in LERs1[1]],'bo',mfc='none',label='$d=27.5$ \u03bcm ($c =$' + str(83) + ' nm)')
plt.plot(AMPs2[0],[l*1e9 for l in LERs2[0]],'x',color='g',label='$d=50$ \u03bcm ($c =$' + str(64) + ' nm)')
plt.plot(AMPs2[1],[l*1e9 for l in LERs2[1]],'x',color='orange',label='$d=50$ \u03bcm ($c =$' + str(110) + ' nm)')
plt.plot(AMPs2[2],[l*1e9 for l in LERs2[2]],'x',color='c',label='$d=50$ \u03bcm ($c =$' + str(145) + ' nm)')
# plt.plot(0,LERi1*1e9,'bo',mfc='none')
# plt.plot(0,LERi2*1e9,'x',color='g')
# Get the current axes
ax = plt.gca()

# Add rectangles to the plot
for (x, y, w, h), color, alpha in zip(rectangles[0:2], colors[0:2], alphas[0:2]):
    rect = patches.Rectangle((x, y), w, h, linewidth=1, edgecolor=None,
                             facecolor=color, alpha=alpha)
    ax.add_patch(rect)

# plt.hlines(0.87,0,np.max(AMPs[0])*1e9,colors='gray',linestyles='--')
# plt.hlines(0.35,0,np.max(AMPs[0])*1e9,colors='gray',linestyles='--')
plt.text(15.1,1.6,'$L_{25}$', color='black', fontsize=8)
plt.text(15.1,0.45,'$L_{10}$', color='black', fontsize=8)
plt.xlabel('Mask Roughness Amplitude ($\sigma$) [nm]')
plt.ylabel('$\Delta$LER [nm]')
# plt.ylabel('LER [nm]')
# plt.vlines(2.0,ymin=0.4,ymax=4,colors='gray',linestyles='dashed')
# plt.text(1.6,4.1,'2 nm', color='gray',fontsize=10)#'$\sigma_{EBL}$',color='gray',fontsize=10)
plt.xlim((-1,np.max(AMPs2[0]) + 1))
plt.ylim((-0.1,np.max(LERs2[0])*1e9 + 0.4))
# plt.legend()
plt.savefig('/user/home/opt/xl/xl/experiments/BEUVcoherenceRoughness/figures/LER.svg', bbox_inches='tight')
plt.show()


plt.plot(AMPs1[0],[e*1 for e in EFs1[0]],'ro',mfc='none',label='$d=27.5$ \u03bcm ($c =$' + str(47) + ' nm)')
plt.plot(AMPs1[1],[e*1 for e in EFs1[1]],'bo',mfc='none',label='$d=27.5$ \u03bcm ($c =$' + str(83) + ' nm)')
plt.plot(AMPs2[0],[e*1 for e in EFs2[0]],'x',color='g',label='$d=50$ \u03bcm ($c =$' + str(64) + ' nm)')
plt.plot(AMPs2[1],[e*1 for e in EFs2[1]],'x',color='orange',label='$d=50$ \u03bcm ($c =$' + str(110) + ' nm)')
plt.plot(AMPs2[2],[e*1 for e in EFs2[2]],'x',color='c',label='$d=50$ \u03bcm ($c =$' + str(145) + ' nm)')
# plt.plot(AMPlc[2],[e*1 - E_off for e in EFlc[2]],':x',color='c',label='line-edge: $c =$' + str(60) + ' nm')
# plt.plot(AMPlc[3],[e*1 - E_off for e in EFlc[3]],':x',color='m',label='line-edge: $c =$' + str(60) + ' nm')
plt.xlabel('Mask Roughness Amplitude ($\sigma$) [nm]')
plt.ylabel('$\Delta \eta_{\pm 1}$')
# plt.ylabel('$\eta_{\pm 1}$')
# plt.legend()
plt.savefig('/user/home/opt/xl/xl/experiments/BEUVcoherenceRoughness/figures/EF.svg', bbox_inches='tight')
plt.show()


plt.plot(AMPs1[0],[e*1 for e in EF0s1[0]],'ro',mfc='none',label='$d=27.5$ \u03bcm ($c =$' + str(47) + ' nm)')
plt.plot(AMPs1[1],[e*1 for e in EF0s1[1]],'bo',mfc='none',label='$d=27.5$ \u03bcm ($c =$' + str(83) + ' nm)')
plt.plot(AMPs2[0],[e*1 for e in EF0s2[0]],'x',color='g',label='$d=50$ \u03bcm ($c =$' + str(64) + ' nm)')
plt.plot(AMPs2[1],[e*1 for e in EF0s2[1]],'x',color='orange',label='$d=50$ \u03bcm ($c =$' + str(110) + ' nm)')
plt.plot(AMPs2[2],[e*1 for e in EF0s2[2]],'x',color='c',label='$d=50$ \u03bcm ($c =$' + str(145) + ' nm)')
# plt.plot(AMPlc[2],[e*1 - E_off for e in EF0lc[2]],':x',color='c',label='line-edge: $c =$' + str(60) + ' nm')
# plt.plot(AMPlc[3],[e*1 - E_off for e in EF0lc[3]],':x',color='m',label='line-edge: $c =$' + str(60) + ' nm')
plt.xlabel('Mask Roughness Amplitude ($\sigma$) [nm]')
plt.ylabel('$\Delta \eta_{0}$')
# plt.ylabel('$\eta_{0}$')
# plt.legend()
plt.savefig('/user/home/opt/xl/xl/experiments/BEUVcoherenceRoughness/figures/EF0.svg', bbox_inches='tight')
plt.show()


plt.plot(AMPs1[0],[l*1e9 for l in LWRs1[0]],'ro',mfc='none',label='$d=27.5$ \u03bcm ($c =$' + str(47) + ' nm)')
plt.plot(AMPs1[1],[l*1e9 for l in LWRs1[1]],'bo',mfc='none',label='$d=27.5$ \u03bcm ($c =$' + str(83) + ' nm)')
plt.plot(AMPs2[0],[l*1e9 for l in LWRs2[0]],'x',color='g',label='$d=50$ \u03bcm ($c =$' + str(64) + ' nm)')
plt.plot(AMPs2[1],[l*1e9 for l in LWRs2[1]],'x',color='orange',label='$d=50$ \u03bcm ($c =$' + str(110) + ' nm)')
plt.plot(AMPs2[2],[l*1e9 for l in LWRs2[2]],'x',color='c',label='$d=50$ \u03bcm ($c =$' + str(145) + ' nm)')
# Get the current axes
ax = plt.gca()
# Add rectangles to the plot
for (x, y, w, h), color, alpha in zip(rectangles[2:4], colors[2:4], alphas[2:4]):
    rect = patches.Rectangle((x, y), w, h, linewidth=1, edgecolor=None,
                              facecolor=color, alpha=alpha)
    ax.add_patch(rect)
# plt.hlines(0.99,0,np.max(AMPs[0])*1e9,colors='gray',linestyles='--',label='$L_{25}$')
# plt.hlines(0.38,0,np.max(AMPs[0])*1e9,colors='gray',linestyles='--',label='$L_{10}$')
plt.text(15.1, 1.8,'$L_{25}$',color='black',fontsize=8) # '0.63 nm', color='g')
plt.text(15.1, 0.46,'$L_{10}$',color='black',fontsize=8) # '0.26 nm', color='y')
plt.xlabel('Mask Roughness Amplitude ($\sigma$) [nm]')
plt.ylabel('$\Delta$LWR [nm]')
# plt.ylabel('LWR [nm]')
plt.xlim((-1,np.max(AMPs2[0]) + 1))
plt.ylim(-0.1,np.max(LWRs2[0])*1e9 + 1.0)
# plt.legend(title='IRDS Limits$^{*}$',fontsize=10)
plt.savefig('/user/home/opt/xl/xl/experiments/BEUVcoherenceRoughness/figures/LWR.svg', bbox_inches='tight')
plt.show()


plt.plot(AMPs1[0],[n/np.pi for n in NILSs1[0]],'ro',mfc='none',label='$d=27.5$ \u03bcm ($c =$' + str(47) + ' nm)')
plt.plot(AMPs1[1],[n/np.pi for n in NILSs1[1]],'bo',mfc='none',label='$d=27.5$ \u03bcm ($c =$' + str(83) + ' nm)')
plt.plot(AMPs2[0],[n/np.pi for n in NILSs2[0]],'x',color='g',label='$d=50$ \u03bcm ($c =$' + str(64) + ' nm)')
plt.plot(AMPs2[1],[n/np.pi for n in NILSs2[1]],'x',color='orange',label='$d=50$ \u03bcm ($c =$' + str(110) + ' nm)')
plt.plot(AMPs2[2],[n/np.pi for n in NILSs2[2]],'x',color='c',label='$d=50$ \u03bcm ($c =$' + str(145) + ' nm)')
# plt.plot(AMPlc[2],[l*1e9 - LWR_off for l in LWRlc[2]],':x',color='c')#,label='line-edge: $c =$' + str(60) + ' nm')
# plt.plot(AMPlc[3],[l*1e9 - LWR_off for l in LWRlc[3]],':x',color='m')#,label='line-edge: $c =$' + str(60) + ' nm')
# plt.hlines(0.63,0,25,colors='gray',linestyles='--',label='$L_{25}$')
# plt.hlines(0.26,0,25,colors='gray',linestyles='--',label='$L_{10}$')
# plt.text(0, 0.65,'$L_{25}$',color='gray',fontsize=8) # '0.63 nm', color='g')
# plt.text(0, 0.28,'$L_{10}$',color='gray',fontsize=8) # '0.26 nm', color='y')
plt.xlabel('Mask Roughness Amplitude ($\sigma$) [nm]')
plt.ylabel('$\Delta$NILS$/\pi$')
# plt.ylabel('NILS $/\pi$ ')
# plt.legend()
plt.savefig('/user/home/opt/xl/xl/experiments/BEUVcoherenceRoughness/figures/NILS.svg', bbox_inches='tight')
plt.show()

plt.plot(AMPs1[0],[n/np.pi for n in NILSs1[0]],'ro',mfc='none',label='$d=27.5$ \u03bcm ($c =$' + str(47) + ' nm)')
plt.plot(AMPs1[1],[n/np.pi for n in NILSs1[1]],'bo',mfc='none',label='$d=27.5$ \u03bcm ($c =$' + str(83) + ' nm)')
plt.xlabel('Mask Roughness Amplitude ($\sigma$) [nm]')
plt.ylabel('$\Delta$NILS$/\pi$')
# plt.ylabel('NILS $/\pi$ ')
# plt.legend()
plt.savefig('/user/home/opt/xl/xl/experiments/BEUVcoherenceRoughness/figures/NILS_27.5.svg', bbox_inches='tight')
plt.show()

plt.plot(AMPs2[0],[n/np.pi for n in NILSs2[0]],'x',color='g',label='$d=50$ \u03bcm ($c =$' + str(64) + ' nm)')
plt.plot(AMPs2[1],[n/np.pi for n in NILSs2[1]],'x',color='orange',label='$d=50$ \u03bcm ($c =$' + str(110) + ' nm)')
plt.plot(AMPs2[2],[n/np.pi for n in NILSs2[2]],'x',color='c',label='$d=50$ \u03bcm ($c =$' + str(145) + ' nm)')
# plt.plot(AMPlc[2],[l*1e9 - LWR_off for l in LWRlc[2]],':x',color='c')#,label='line-edge: $c =$' + str(60) + ' nm')
# plt.plot(AMPlc[3],[l*1e9 - LWR_off for l in LWRlc[3]],':x',color='m')#,label='line-edge: $c =$' + str(60) + ' nm')
# plt.hlines(0.63,0,25,colors='gray',linestyles='--',label='$L_{25}$')
# plt.hlines(0.26,0,25,colors='gray',linestyles='--',label='$L_{10}$')
# plt.text(0, 0.65,'$L_{25}$',color='gray',fontsize=8) # '0.63 nm', color='g')
# plt.text(0, 0.28,'$L_{10}$',color='gray',fontsize=8) # '0.26 nm', color='y')
plt.xlabel('Mask Roughness Amplitude ($\sigma$) [nm]')
plt.ylabel('$\Delta$NILS$/\pi$')
# plt.ylabel('NILS $/\pi$ ')
# plt.legend()
plt.savefig('/user/home/opt/xl/xl/experiments/BEUVcoherenceRoughness/figures/NILS_50.svg', bbox_inches='tight')
plt.show()


# plt.plot([a*1e9 for a in AMPs[0][1::]],[lwr/ler for lwr,ler in zip(LWRs[0][1::],LERs[0][1::])],'ro',mfc='none')#,label='surface: $c =$' + str(35) + ' nm')
# plt.plot([a*1e9 for a in AMPs[1][1::]],[lwr/ler for lwr,ler in zip(LWRs[1][1::],LERs[1][1::])],'bo',mfc='none')#,label='surface: $c =$' + str(65) + ' nm')
# plt.plot(AMPl,[lwr/ler for lwr,ler in zip(LWRl,LERl)],'x',color='black')#,label='line-edge: $c =$' + str(60) + ' nm')
# plt.plot(AMPlc[0],[lwr/ler for lwr,ler in zip(LWRlc[0],LERlc[0])],'x',color='g')#,label='line-edge: $c =$' + str(60) + ' nm')
# plt.plot(AMPlc[1],[lwr/ler for lwr,ler in zip(LWRlc[1],LERlc[1])],'x',color='g')#,label='line-edge: $c =$' + str(60) + ' nm')
# plt.xlabel('Mask Roughness Amplitude ($\sigma$) [nm]')
# plt.ylabel('$\Delta$LWR / $\Delta$LER ')
# plt.ylabel('LWR / LER ')
# plt.savefig('/user/home/opt/xl/xl/experiments/BEUVcoherenceRoughness/figures/LWRoverLER_delta.svg', bbox_inches='tight')
# plt.show()


plt.plot(AMPs1[0],[l*1e9 for l in CDUs1[0]],'ro',mfc='none',label='$d=27.5$ \u03bcm ($c =$' + str(47) + ' nm)')
plt.plot(AMPs1[1],[l*1e9 for l in CDUs1[1]],'bo',mfc='none',label='$d=27.5$ \u03bcm ($c =$' + str(83) + ' nm)')
plt.plot(AMPs2[0],[l*1e9 for l in CDUs2[0]],'x',color='g',label='$d=50$ \u03bcm ($c =$' + str(64) + ' nm)')
plt.plot(AMPs2[1],[l*1e9 for l in CDUs2[1]],'x',color='orange',label='$d=50$ \u03bcm ($c =$' + str(110) + ' nm)')
plt.plot(AMPs2[2],[l*1e9 for l in CDUs2[2]],'x',color='c',label='$d=50$ \u03bcm ($c =$' + str(145) + ' nm)')
# Get the current axes
ax = plt.gca()
# Add rectangles to the plot
for (x, y, w, h), color, alpha in zip(rectangles[4::], colors[4::], alphas[4::]):
    rect = patches.Rectangle((x, y), w, h, linewidth=1, edgecolor=None,
                              facecolor=color, alpha=alpha)
    ax.add_patch(rect)
# plt.hlines(0.87,0,np.max(AMPs[0])*1e9,colors='gray',linestyles='--')
# plt.hlines(0.35,0,np.max(AMPs[0])*1e9,colors='gray',linestyles='--')
plt.text(15.1,2.3,'$L_{25}$', color='black', fontsize=8)
plt.text(15.1,0.7,'$L_{10}$', color='black', fontsize=8)
plt.xlabel('Mask Roughness Amplitude ($\sigma$) [nm]')
plt.ylabel('$\Delta$CDU [nm]')
# plt.ylabel('CDU [nm]')
# plt.xlim((-1,np.max(AMPs[0])*1e9 + 1))
# plt.vlines(2.0,ymin=0.4,ymax=4,colors='gray',linestyles='dashed')
# plt.text(1.6,4.1,'2 nm', color='gray',fontsize=10)#'$\sigma_{EBL}$',color='gray',fontsize=10)
plt.xlim((-1,np.max(AMPs2[0]) + 1))
plt.ylim((-0.1,np.max(CDUs2[0])*1e9 + 1.0))
# plt.legend()
plt.savefig('/user/home/opt/xl/xl/experiments/BEUVcoherenceRoughness/figures/CDU.svg', bbox_inches='tight')
plt.show()


plt.plot(AMPs1[0],[l for l in CLRs1[0]],'ro',mfc='none',label='$d=27.5$ \u03bcm ($c =$' + str(47) + ' nm)')
plt.plot(AMPs1[1],[l for l in CLRs1[1]],'bo',mfc='none',label='$d=27.5$ \u03bcm ($c =$' + str(83) + ' nm)')
plt.plot(AMPs2[0],[l for l in CLRs2[0]],'x',color='g',label='$d=50$ \u03bcm ($c =$' + str(64) + ' nm)')
plt.plot(AMPs2[1],[l for l in CLRs2[1]],'x',color='orange',label='$d=50$ \u03bcm ($c =$' + str(110) + ' nm)')
plt.plot(AMPs2[2],[l for l in CLRs2[2]],'x',color='c',label='$d=50$ \u03bcm ($c =$' + str(145) + ' nm)')
plt.xlabel('Mask Roughness Amplitude ($\sigma$) [nm]')
plt.ylabel('$\Delta$CLR [nm]')
# plt.ylabel('CLR [nm]')
# plt.xlim((-1,np.max(AMPs[0])*1e9 + 1))
# plt.vlines(2.0,ymin=0.4,ymax=4,colors='gray',linestyles='dashed')
# plt.text(1.6,4.1,'2 nm', color='gray',fontsize=10)#'$\sigma_{EBL}$',color='gray',fontsize=10)
# plt.xlim((0,,np.max(AMPs[0])*1e9))
# plt.legend()
plt.savefig('/user/home/opt/xl/xl/experiments/BEUVcoherenceRoughness/figures/CLR.svg', bbox_inches='tight')
plt.show()

X = np.linspace(0.0,np.max(LERs2[2])*1e9,100)
Y = X*np.sqrt(2)# - 2.e-9

plt.plot([l*1e9 for l in LERs1[0]],[l*1e9 for l in LWRs1[0]],'ro',mfc='none',label='$d=27.5$ \u03bcm ($c =$' + str(47) + ' nm)')
plt.plot([l*1e9 for l in LERs1[1]],[l*1e9 for l in LWRs1[1]],'bo',mfc='none',label='$d=27.5$ \u03bcm ($c =$' + str(83) + ' nm)')
plt.plot([l*1e9 for l in LERs2[0]],[l*1e9 for l in LWRs2[0]],'x',color='g',label='$d=50$ \u03bcm ($c =$' + str(64) + ' nm)')
plt.plot([l*1e9 for l in LERs2[1]],[l*1e9 for l in LWRs2[1]],'x',color='orange',label='$d=50$ \u03bcm ($c =$' + str(110) + ' nm)')
plt.plot([l*1e9 for l in LERs2[2]],[l*1e9 for l in LWRs2[2]],'x',color='c',label='$d=50$ \u03bcm ($c =$' + str(145) + ' nm)')
plt.plot(X,Y,':', label='LWR = $\sqrt{2}$LER')
plt.xlabel('LER [nm]')
plt.ylabel('$\Delta$LWR / $\Delta$LER ')
# plt.ylabel('LWR [nm]')
plt.legend()
plt.savefig('/user/home/opt/xl/xl/experiments/BEUVcoherenceRoughness/figures/deltaLWRoverLER.svg', bbox_inches='tight')
plt.show()


# plt.plot(AMPs1[0],[l*1e9 for l in LERc1[0]])
# plt.show()
# plt.plot(AMPs1[0],[l*1e9 for l in LERc1[0]],'ro',mfc='none',label='$d=27.5$ \u03bcm ($c =$' + str(47) + ' nm)')
# plt.plot(AMPs1[1],[l*1e9 for l in LERc1[1]],'bo',mfc='none',label='$d=27.5$ \u03bcm ($c =$' + str(83) + ' nm)')
# plt.plot(AMPs2[0],[l*1e9 for l in LERc2[0]],'x',color='g',label='$d=50$ \u03bcm ($c =$' + str(64) + ' nm)')
# plt.plot(AMPs2[1],[l*1e9 for l in LERc2[1]],'x',color='orange',label='$d=50$ \u03bcm ($c =$' + str(110) + ' nm)')
# plt.plot(AMPs2[2],[l*1e9 for l in LERc2[2]],'x',color='c',label='$d=50$ \u03bcm ($c =$' + str(145) + ' nm)')
# plt.xlabel('Mask Roughness Amplitude [nm]')
# plt.ylabel('LER Correlation Length [nm]')
# plt.show()
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
# plt.savefig('/user/home/opt/xl/xl/experiments/BEUVcoherenceRoughness/figures/omega_LER.svg', bbox_inches='tight')
# plt.show()

# plt.plot(dAMP,[1 - b for b in Blwr8],'ro',mfc='none',label='CD = 8 nm')
# plt.plot(dAMP,[1 - b for b in Blwr10],'bo',mfc='none',label='CD = 10 nm')
# plt.plot(dAMP,[1 - b for b in Blwr11],'go',mfc='none',label='CD = 11 nm')
# plt.xlabel('Mask Roughness Amplitude ($\sigma$) [nm]')
# plt.ylim((0,1))
# plt.xlim((0,5))
# plt.ylabel(r'1 - $\omega$ (LWR)')
# plt.legend()
# plt.savefig('/user/home/opt/xl/xl/experiments/BEUVcoherenceRoughness/figures/omega_LWR.svg', bbox_inches='tight')
# plt.show()


# plt.plot(dAMP,[1 - b for b in Bcdu8], 'ro', mfc='none')
# plt.plot(dAMP,[1 - b for b in Bcdu10], 'bo', mfc='none')
# plt.plot(dAMP,[1 - b for b in Bcdu11], 'go', mfc='none')
# plt.xlabel('Mask Roughness Amplitude ($\sigma$) [nm]')
# plt.ylim(0,1)
# plt.xlim(0,5)
# plt.ylabel(r'1 - $\omega$ (CDU)')
# plt.savefig('/user/home/opt/xl/xl/experiments/BEUVcoherenceRoughness/figures/omega_CDU.svg', bbox_inches='tight')
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
# plt.savefig('/user/home/opt/xl/xl/experiments/BEUVcoherenceRoughness/figures/omega_CD11.svg', bbox_inches='tight')
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
# plt.savefig('/user/home/opt/xl/xl/experiments/BEUVcoherenceRoughness/figures/omega_CD10.svg', bbox_inches='tight')
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
# plt.savefig('/user/home/opt/xl/xl/experiments/BEUVcoherenceRoughness/figures/omega_CD8.svg', bbox_inches='tight')
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
# # # plt.savefig('/user/home/opt/xl/xl/experiments/BEUVcoherenceRoughness/figures/LWRoverLER.svg', bbox_inches='tight')
# # plt.show()