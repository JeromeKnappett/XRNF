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

AMPs = [[0.0,4.130047940461463e-09, 8.113879195408235e-09, 1.2407000631704425e-08, 1.5591600442950036e-08, 2.1440043008828508e-08],
        [0.0,4.5212415178392555e-09, 9.460645272952142e-09, 1.3099010376638959e-08, 1.8776805796218852e-08, 2.4324646017447212e-08]]

LERs = [[5.413441208840074e-10,2.7481487701655883e-09, 4.328837724722746e-09, 7.3554552535173886e-09, 8.840734042650742e-09, 9.606381539725196e-09],
        [5.413441208840074e-10,3.1139418671295447e-09, 5.53478611314333e-09, 8.60382971673507e-09, 9.906110289171326e-09, 1.1158100954969696e-08]]
# [[3.30454009, 3.3995128,  3.75087101, 3.91552216, 4.50694119], [ 3.41846441,  4.05970329,  5.18771456,  7.79124371, 10.61398994]]
EFs = [[0.013509663134218988,0.01159051, 0.00986495, 0.00902773, 0.00714395, 0.00742158], 
       [0.013509663134218988,0.01101063, 0.01007118, 0.00808597, 0.0076919,  0.00677506]]
# [[0.01350966, 0.01250429, 0.012075,   0.01064718,0.00968001], [0.01340222, 0.0115262,  0.01102112, 0.00985921, 0.00860822]]
EF0s = [[0.2757960298511132,0.23861661749006782, 0.20144672334158512, 0.17342737893608068, 0.14928671864093715, 0.12202031231528797],
        [0.2757960298511132,0.23172243373250534, 0.19540876650860273, 0.17038559803004477, 0.13600921183104328, 0.11148739833624642]]

LWRs = [[4.849588006287376e-09, 5.980141355511317e-09, 8.809359324012706e-09, 1.2180892928621722e-08, 1.4382221646937226e-08, 1.6928853014125275e-08], 
        [4.849588006287376e-09, 6.439488981484628e-09, 1.0078107365692731e-08, 1.3783335108110229e-08, 1.7340892928309294e-08, 1.8404841485447004e-08]]
CDUs = [[5.781118344891898e-09,6.838706958244727e-09, 9.402067445920947e-09, 1.2735984038053174e-08, 1.528817150569184e-08, 1.742302265775888e-08],
        [5.781118344891898e-09,7.263532746712065e-09, 1.0618712553933559e-08, 1.423252985335891e-08, 1.7748214571472112e-08, 1.9407002278797315e-08]]

CLRs = [[0.10560543488926721,0.7802619802849241, 1.0691217288075308, 1.2571715232897174, 1.4110998303069975, 1.6016318326353671],
        [0.10560543488926721,0.8911327886790068, 1.2058647390597184, 1.382386814018214, 1.5712543621206572, 1.7738124245060223]]
# [[4.849588006287376e-09,5.980141355511317e-09, 8.809359324012706e-09, 1.2157013328256315e-08, 1.4387681264393688e-08, 1.6929602120538544e-08],
#         [4.849588006287376e-09,6.439488981484628e-09, 1.0078107365692731e-08, 1.3729426568735085e-08, 1.7340892928309294e-08, 1.8416352950990274e-08]]

# [[1.85248819114021e-10,2.0293692376721032e-10, 2.105608057014916e-10, 2.2527768329039195e-10, 2.6003221852643e-10, 2.865896661301679e-10],
       # [1.85248819114021e-10,2.062957563436123e-10, 2.131014365695951e-10, 2.5570734944935685e-10, 2.6909820644099464e-10, 3.3771092230988193e-10]]

NILSs = [[2.116186348618096,2.0908811294517373, 2.0789190216894333, 2.041860021712132, 2.001335891202929, 1.9397456508748665],
         [2.116186348618096,2.088883017367835, 2.0733176068325525, 2.030516945599258, 1.984604694208154, 1.9241254919376987]]

AMPl = [0.0,
        3.7249164431850543,
        4.536853502343667,
        5.518446489820692,
        6.4970478648742045]

LERl = [4.3635849713811906e-09, 5.242472647554529e-09, 6.0841032026263025e-09, 6.940553500825464e-09, 7.54743209000035e-09]
EFl = [0.021131529941825652, 0.020928883511721407, 0.02081171275288757, 0.02070530867342373, 0.020613622656661643]
EF0l = [0.38633866491293745, 0.3868694466019947, 0.3868162877730161, 0.3856633096456465, 0.3852231361051156]
LWRl = [1.0923908945161289e-08, 1.2398196110335176e-08, 1.3354820291403122e-08, 1.4510335516375693e-08, 1.571683515486957e-08]
# [9.955098272171686e-09, 1.0941223378511421e-08, 1.1607813936311319e-08, 1.2518395134991949e-08, 1.3652929634246246e-08]

NILSl = [1.1593819498661837, 1.2184001817604766, 1.2420006644397024, 1.228209440432311, 1.2361462469943476]

CDUl = [1.1817291530582339e-08, 1.3314161120987451e-08, 1.4251276658563772e-08, 1.5429128820236014e-08, 1.6819532021869085e-08]
CLRl = [0.2776531185441434, 1.152245736502477, 1.4205362558686379, 1.7266725126965148, 2.01208214948376]

AMPlc = [[4.341524765321773,3.766411879905553,3.2124952672360794,2.6946056828131],
        [2.503385243226183,2.3006595222372036,1.2381303522982893],
        [3.0036300170087337,2.61203604789903,1.796048147106454],
        [3.340738562744371,3.063506165870519,2.1333112482785796]
        ]

LERlc =[[6.036151551308723e-09, 5.780911773197987e-09, 5.595665079825287e-09, 5.274538711510246e-09], [5.159687504798027e-09, 5.084196764255126e-09, 4.893464563081442e-09], [5.4167622250106124e-09, 5.1852489113408345e-09, 5.019977494918283e-09], [5.5017914707522865e-09, 5.26618264731997e-09, 5.068210101259935e-09]]
EFlc = [[0.02002663458021771, 0.0200488341047381, 0.020070461086776948, 0.020090712526501634], [0.020096566383278384, 0.020104430740383417, 0.020130084724572353], [0.0200820487704601, 0.02009567936253653, 0.02011486493701255], [0.020069385619138652, 0.020078347049258646, 0.020107744765103658]]
EF0lc = [[0.366258378180974, 0.3662131701306071, 0.3662110960144475, 0.3662011095292348], 
         [0.36616753957509657, 0.36612786250115514, 0.36605572935027236]]
LWRlc =[[1.3444481821949063e-08, 1.2849448883303512e-08, 1.2702977709211797e-08, 1.2177184414304325e-08], 
        [1.2075723257167434e-08, 1.1808532824697654e-08, 1.1504334085550006e-08]]
# [[1.160945[1.3444268650532418e-08, 1.284800891795799e-08, 1.2698908866214219e-08, 1.2177023678953625e-08], [1.774148920115038e-08, 1.1805507046206605e-08, 1.1506066426741309e-08]7645550024e-08, 1.146580208690185e-08, 1.1093664284271682e-08, 1.0651700088610577e-08], [1.05138966863675e-08, 1.0398502136219855e-08, 1.0197036939931613e-08], [1.547004144029981e-08, 1.551497038008132e-08, 1.5639177303561026e-08], [1.5508012730110484e-08, 1.534350086599275e-08, 1.558811929157995e-08]]
CDUlc = [[1.4449541488619234e-08, 1.384919827651337e-08, 1.3413609436466312e-08, 1.3021944779901395e-08], 
         [1.2915901350630572e-08, 1.2710020784249557e-08, 1.243830531057649e-08]]
CLRlc = [[1.5416424435415668, 1.4105600762865649, 1.2713368914357137, 1.0942651121155331], 
         [1.0924290459059496, 1.0119957124582584, 0.8361806633108153]]

NILSlc = [[1.2593594686899343, 1.2637190478225901, 1.2677311850469586, 1.2505911568366173], [1.2567732749119784, 1.254066391522723, 1.2610696354592097], [1.2636538170562446, 1.258183745771542, 1.2605894773007162], [1.2678094274011977, 1.2677567434260468, 1.2609112380292897]]

E_off = 0#abs(EFl[0] - EFs[0][0])*100
LWR_off = 0#abs(LWRl[0] - LWRs[0][0])*1e9

LERs[0] = [l - LERs[0][0] for l in LERs[0][1:-1]]
LERs[1] = [l - LERs[1][0] for l in LERs[1][1:-2]]
LERlc[0] = [l - LERl[0] for l in LERlc[0]]
LERlc[1] = [l - LERl[0] for l in LERlc[1]]
LERl = [l - LERl[0] for l in LERl[1::]]

EFs[0] = [l - EFs[0][0] for l in EFs[0][1:-1]]
EFs[1] = [l - EFs[1][0] for l in EFs[1][1:-2]]
EFlc[0] = [l - EFl[0] for l in EFlc[0]]
EFlc[1] = [l - EFl[0] for l in EFlc[1]]
EFl = [l - EFl[0] for l in EFl[1::]]

EF0s[0] = [l - EF0s[0][0] for l in EF0s[0][1:-1]]
EF0s[1] = [l - EF0s[1][0] for l in EF0s[1][1:-2]]
EF0lc[0] = [l - EF0l[0] for l in EF0lc[0]]
EF0lc[1] = [l - EF0l[0] for l in EF0lc[1]]
EF0l = [l - EF0l[0] for l in EF0l[1::]]
    
LWRs[0] = [l - LWRs[0][0] for l in LWRs[0][1:-1]]
LWRs[1] = [l - LWRs[1][0] for l in LWRs[1][1:-2]]
LWRlc[0] = [l - LWRl[0] for l in LWRlc[0]]
LWRlc[1] = [l - LWRl[0] for l in LWRlc[1]]
LWRl = [l - LWRl[0] for l in LWRl[1::]]

CDUs[0] = [c - CDUs[0][0] for c in CDUs[0][1:-1]]
CDUs[1]  = [c - CDUs[1][0] for c in CDUs[1][1:-2]]
CDUlc[0] = [c - CDUl[0] for c in CDUlc[0]]
CDUlc[1] = [c - CDUl[0] for c in CDUlc[1]]
CDUl = [c - CDUl[0] for c in CDUl[1::]]

CLRs[0] = [c - CLRs[0][0] for c in CLRs[0][1:-1]]
CLRs[1]  = [c - CLRs[1][0] for c in CLRs[1][1:-2]]
CLRlc[0] = [c - CLRl[0] for c in CLRlc[0]]
CLRlc[1] = [c - CLRl[0] for c in CLRlc[1]]
CLRl = [c - CLRl[0] for c in CLRl[1::]]

NILSs[0] = [l - NILSs[0][0] for l in NILSs[0][1:-1]]
NILSs[1] = [l - NILSs[1][0] for l in NILSs[1][1:-2]]
NILSlc[0] = [l - NILSl[0] for l in NILSlc[0]]
NILSlc[1] = [l - NILSl[0] for l in NILSlc[1]]
NILSl = [l - NILSl[0] for l in NILSl[1::]]

AMPs[0] = AMPs[0][1:-1]
AMPs[1] = AMPs[1][1:-2]
AMPl = AMPl[1::]


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

dLER = []
dLWR = []
dCDU = []
dAMP = []
_AMP = [[a*1e9 for a in AMPs[0]],[a*1e9 for a in AMPs[1]],AMPl,AMPlc[0],AMPlc[1]]
_LWR = [LWRs[0],LWRs[1],LWRl,LWRlc[0],LWRlc[1]]
_CDU = [CDUs[0],CDUs[1],CDUl,CDUlc[0],CDUlc[1]]

for i,l in enumerate([LERs[0],LERs[1],LERl,LERlc[0],LERlc[1]]):
    for ii,_l in enumerate(l):
        dLER.append(_l)
        dLWR.append(_LWR[i][ii])
        dCDU.append(_CDU[i][ii])
        dAMP.append(_AMP[i][ii])

a,b = np.polyfit(dAMP,dLER,1)
x_fit = np.linspace(0,np.max(dAMP)+0.25,400)
y_fit = [a*_x*1e9 + b*1e9 for _x in x_fit]


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


plt.plot([a*1e9 for a in AMPs[0]],[l*1e9 for l in LERs[0]],'ro',mfc='none',label='$\sigma_{S}(c =$' + str(35) + ' nm)')
plt.plot([a*1e9 for a in AMPs[1]],[l*1e9 for l in LERs[1]],'bo',mfc='none',label='$\sigma_{S}(c =$' + str(65) + ' nm)')
plt.plot(AMPl,[l*1e9 for l in LERl],'x',color='black',label='$\sigma_{LER}(c =$' + str(60) + ' nm)')
plt.plot(AMPlc[1],[l*1e9 for l in LERlc[1]],'x',color='g',label='$\sigma_{LER}(c \geq$' + str(400) + ' nm)')
plt.plot(AMPlc[0],[l*1e9 for l in LERlc[0]],'x',color='g')#,label='$\sigma_{LER}(c =$' + str(420) + ' nm)')
# plt.plot(x_fit,y_fit,':')
# plt.plot(AMPlc[2],[l*1e9 for l in LERlc[2]],':x',color='c',label='line-edge: $c =$' + str(300) + ' nm')
# plt.plot(AMPlc[3],[l*1e9 for l in LERlc[3]],':x',color='m',label='line-edge: $c =$' + str(250) + ' nm')
# plt.text(15, 8,r'$\sigma_{S}$ ($c=35$ nm)',color='r',fontsize=8,rotation = 20) # '0.63 nm', color='g')
# plt.text(12, 9,r'$\sigma_{S}$ ($c=65$ nm)',color='b',fontsize=8,rotation = 30) # '0.63 nm', color='g')
# plt.text(-0.2, 3.5,r'$\sigma_{LER}$ ($c=60$ nm)',color='black',fontsize=8,rotation = 35) # '0.63 nm', color='g')
# plt.text(1, 6,r'$\sigma_{LER}$ ($c=420$ nm)',color='g',fontsize=8,rotation = 50) # '0.63 nm', color='g')
# plt.text(0, 8,r'$\sigma_{LER}$ ($c=420$ nm)',color='g',fontsize=8)#,rotation = 50) # '0.63 nm', color='g')

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
plt.xlim((-1,np.max(AMPs[0])*1e9 + 1))
plt.vlines(2.0,ymin=0.4,ymax=4,colors='gray',linestyles='dashed')
plt.text(1.6,4.1,'2 nm', color='gray',fontsize=10)#'$\sigma_{EBL}$',color='gray',fontsize=10)
# plt.xlim((0,,np.max(AMPs[0])*1e9))
plt.legend()
# plt.savefig('/user/home/opt/xl/xl/experiments/maskLER_retry2/figures/LER_wLegend.svg', bbox_inches='tight')
plt.show()

plt.plot([a*1e9 for a in AMPs[0]],[e*1 for e in EFs[0]],'ro',mfc='none',label='surface: $c =$' + str(35) + ' nm')
plt.plot([a*1e9 for a in AMPs[1]],[e*1 for e in EFs[1]],'bo',mfc='none',label='surface: $c =$' + str(65) + ' nm')
plt.plot(AMPl,[e*1 - E_off for e in EFl],'x',color='black',label='line-edge: $c =$' + str(60) + ' nm')
plt.plot(AMPlc[0],[e*1 - E_off for e in EFlc[0]],'x',color='g',label='line-edge: $c =$' + str(60) + ' nm')
plt.plot(AMPlc[1],[e*1 - E_off for e in EFlc[1]],'x',color='g',label='line-edge: $c =$' + str(60) + ' nm')
# plt.plot(AMPlc[2],[e*1 - E_off for e in EFlc[2]],':x',color='c',label='line-edge: $c =$' + str(60) + ' nm')
# plt.plot(AMPlc[3],[e*1 - E_off for e in EFlc[3]],':x',color='m',label='line-edge: $c =$' + str(60) + ' nm')
plt.xlabel('Mask Roughness Amplitude ($\sigma$) [nm]')
plt.ylabel('$\Delta \eta_{\pm 1}$')
# plt.ylabel('$\eta$')
# plt.legend()
# plt.savefig('/user/home/opt/xl/xl/experiments/maskLER_retry2/figures/EF.svg', bbox_inches='tight')
plt.show()

plt.plot([a*1e9 for a in AMPs[0]],[e*1 for e in EF0s[0]],'ro',mfc='none',label='surface: $c =$' + str(35) + ' nm')
plt.plot([a*1e9 for a in AMPs[1]],[e*1 for e in EF0s[1]],'bo',mfc='none',label='surface: $c =$' + str(65) + ' nm')
plt.plot(AMPl,[e*1 - E_off for e in EF0l],'x',color='black',label='line-edge: $c =$' + str(60) + ' nm')
plt.plot(AMPlc[0],[e*1 - E_off for e in EF0lc[0]],'x',color='g',label='line-edge: $c =$' + str(60) + ' nm')
plt.plot(AMPlc[1],[e*1 - E_off for e in EF0lc[1]],'x',color='g',label='line-edge: $c =$' + str(60) + ' nm')
# plt.plot(AMPlc[2],[e*1 - E_off for e in EF0lc[2]],':x',color='c',label='line-edge: $c =$' + str(60) + ' nm')
# plt.plot(AMPlc[3],[e*1 - E_off for e in EF0lc[3]],':x',color='m',label='line-edge: $c =$' + str(60) + ' nm')
plt.xlabel('Mask Roughness Amplitude ($\sigma$) [nm]')
plt.ylabel('$\Delta \eta_{0}$')
# plt.ylabel('$\eta$')
# plt.legend()
# plt.savefig('/user/home/opt/xl/xl/experiments/maskLER_retry2/figures/EF0.svg', bbox_inches='tight')
plt.show()

plt.plot([a*1e9 for a in AMPs[0]],[l*1e9 for l in LWRs[0]],'ro',mfc='none')#,label='surface: $c =$' + str(35) + ' nm')
plt.plot([a*1e9 for a in AMPs[1]],[l*1e9 for l in LWRs[1]],'bo',mfc='none')#,label='surface: $c =$' + str(65) + ' nm')
# # plt.plot(AMPl[1::],[l*1e9 for l in LWRl[1::]],':x',color='black',label='line-edge: $c =$' + str(60) + ' nm')
plt.plot(AMPl,[l*1e9 - LWR_off for l in LWRl],'x',color='black')#,label='line-edge: $c =$' + str(60) + ' nm')
plt.plot(AMPlc[0],[l*1e9 - LWR_off for l in LWRlc[0]],'x',color='g')#,label='line-edge: $c =$' + str(60) + ' nm')
plt.plot(AMPlc[1],[l*1e9 - LWR_off for l in LWRlc[1]],'x',color='g')#,label='line-edge: $c =$' + str(60) + ' nm')
# # plt.plot(AMPlc[2],[l*1e9 - LWR_off for l in LWRlc[2]],':x',color='c')#,label='line-edge: $c =$' + str(60) + ' nm')
# # plt.plot(AMPlc[3],[l*1e9 - LWR_off for l in LWRlc[3]],':x',color='m')#,label='line-edge: $c =$' + str(60) + ' nm')

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
plt.xlim((-1,np.max(AMPs[0])*1e9 + 1))
# plt.legend(title='IRDS Limits$^{*}$',fontsize=10)
# plt.savefig('/user/home/opt/xl/xl/experiments/maskLER_retry2/figures/LWR_redone.svg', bbox_inches='tight')
plt.show()


plt.plot([a*1e9 for a in AMPs[0]],[n/np.pi for n in NILSs[0]],'ro',mfc='none')#,label='surface: $c =$' + str(35) + ' nm')
plt.plot([a*1e9 for a in AMPs[1]],[n/np.pi for n in NILSs[1]],'bo',mfc='none')#,label='surface: $c =$' + str(65) + ' nm')
# plt.plot(AMPl[1::],[l*1e9 for l in LWRl[1::]],':x',color='black',label='line-edge: $c =$' + str(60) + ' nm')
plt.plot(AMPl,[n/np.pi for n in NILSl],'x',color='black')#,label='line-edge: $c =$' + str(60) + ' nm')
plt.plot(AMPlc[0],[n/np.pi for n in NILSlc[0]],'x',color='g')#,label='line-edge: $c =$' + str(60) + ' nm')
plt.plot(AMPlc[1],[n/np.pi for n in NILSlc[1]],'x',color='g')#,label='line-edge: $c =$' + str(60) + ' nm')
# plt.plot(AMPlc[2],[l*1e9 - LWR_off for l in LWRlc[2]],':x',color='c')#,label='line-edge: $c =$' + str(60) + ' nm')
# plt.plot(AMPlc[3],[l*1e9 - LWR_off for l in LWRlc[3]],':x',color='m')#,label='line-edge: $c =$' + str(60) + ' nm')
# plt.hlines(0.63,0,25,colors='gray',linestyles='--',label='$L_{25}$')
# plt.hlines(0.26,0,25,colors='gray',linestyles='--',label='$L_{10}$')
# plt.text(0, 0.65,'$L_{25}$',color='gray',fontsize=8) # '0.63 nm', color='g')
# plt.text(0, 0.28,'$L_{10}$',color='gray',fontsize=8) # '0.26 nm', color='y')
# plt.xlabel('Mask Roughness Amplitude ($\sigma$) [nm]')
plt.ylabel('$\Delta$NILS$/\pi$')
# plt.ylabel('NILS $/\pi$ ')
# # plt.legend(title='IRDS Limits$^{*}$',fontsize=10)
# plt.savefig('/user/home/opt/xl/xl/experiments/maskLER_retry2/figures/NILS.svg', bbox_inches='tight')
plt.show()


plt.plot([a*1e9 for a in AMPs[0][1::]],[lwr/ler for lwr,ler in zip(LWRs[0][1::],LERs[0][1::])],'ro',mfc='none')#,label='surface: $c =$' + str(35) + ' nm')
plt.plot([a*1e9 for a in AMPs[1][1::]],[lwr/ler for lwr,ler in zip(LWRs[1][1::],LERs[1][1::])],'bo',mfc='none')#,label='surface: $c =$' + str(65) + ' nm')
plt.plot(AMPl,[lwr/ler for lwr,ler in zip(LWRl,LERl)],'x',color='black')#,label='line-edge: $c =$' + str(60) + ' nm')
plt.plot(AMPlc[0],[lwr/ler for lwr,ler in zip(LWRlc[0],LERlc[0])],'x',color='g')#,label='line-edge: $c =$' + str(60) + ' nm')
plt.plot(AMPlc[1],[lwr/ler for lwr,ler in zip(LWRlc[1],LERlc[1])],'x',color='g')#,label='line-edge: $c =$' + str(60) + ' nm')
plt.xlabel('Mask Roughness Amplitude ($\sigma$) [nm]')
plt.ylabel('$\Delta$LWR / $\Delta$LER ')
plt.ylabel('LWR / LER ')
# plt.savefig('/user/home/opt/xl/xl/experiments/maskLER_retry2/figures/LWRoverLER_delta.svg', bbox_inches='tight')
plt.show()


plt.plot([a*1e9 for a in AMPs[0]],[l*1e9 for l in CDUs[0]],'ro',mfc='none',label='$\sigma_{S}(c =$' + str(35) + ' nm)')
plt.plot([a*1e9 for a in AMPs[1]],[l*1e9 for l in CDUs[1]],'bo',mfc='none',label='$\sigma_{S}(c =$' + str(65) + ' nm)')
plt.plot(AMPl,[l*1e9 for l in CDUl],'x',color='black',label='$\sigma_{CDU}(c =$' + str(60) + ' nm)')
plt.plot(AMPlc[1],[l*1e9 for l in CDUlc[1]],'x',color='g',label='$\sigma_{CDU}(c \geq$' + str(400) + ' nm)')
plt.plot(AMPlc[0],[l*1e9 for l in CDUlc[0]],'x',color='g')#,label='$\sigma_{CDU}(c =$' + str(420) + ' nm)')
# plt.plot(x_fit,y_fit,':')
# plt.plot(AMPlc[2],[l*1e9 for l in CDUlc[2]],':x',color='c',label='line-edge: $c =$' + str(300) + ' nm')
# plt.plot(AMPlc[3],[l*1e9 for l in CDUlc[3]],':x',color='m',label='line-edge: $c =$' + str(250) + ' nm')
# plt.text(15, 8,r'$\sigma_{S}$ ($c=35$ nm)',color='r',fontsize=8,rotation = 20) # '0.63 nm', color='g')
# plt.text(12, 9,r'$\sigma_{S}$ ($c=65$ nm)',color='b',fontsize=8,rotation = 30) # '0.63 nm', color='g')
# plt.text(-0.2, 3.5,r'$\sigma_{CDU}$ ($c=60$ nm)',color='black',fontsize=8,rotation = 35) # '0.63 nm', color='g')
# plt.text(1, 6,r'$\sigma_{CDU}$ ($c=420$ nm)',color='g',fontsize=8,rotation = 50) # '0.63 nm', color='g')
# plt.text(0, 8,r'$\sigma_{CDU}$ ($c=420$ nm)',color='g',fontsize=8)#,rotation = 50) # '0.63 nm', color='g')

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
# plt.ylabel('$\Delta$CDU [nm]')
plt.ylabel('CDU [nm]')
# plt.xlim((-1,np.max(AMPs[0])*1e9 + 1))
# plt.vlines(2.0,ymin=0.4,ymax=4,colors='gray',linestyles='dashed')
# plt.text(1.6,4.1,'2 nm', color='gray',fontsize=10)#'$\sigma_{EBL}$',color='gray',fontsize=10)
plt.xlim((-1,np.max(AMPs[0])*1e9 + 1))
plt.ylim((-0.1,np.max(CDUs[0])*1e9 + 1))
# plt.legend()
# plt.savefig('/user/home/opt/xl/xl/experiments/maskLER_retry2/figures/CDU.svg', bbox_inches='tight')
plt.show()


plt.plot([a*1e9 for a in AMPs[0]],[l for l in CLRs[0]],'ro',mfc='none',label='$\sigma_{S}(c =$' + str(35) + ' nm)')
plt.plot([a*1e9 for a in AMPs[1]],[l for l in CLRs[1]],'bo',mfc='none',label='$\sigma_{S}(c =$' + str(65) + ' nm)')
plt.plot(AMPl,[l for l in CLRl],'x',color='black',label='$\sigma_{CLR}(c =$' + str(60) + ' nm)')
plt.plot(AMPlc[1],[l for l in CLRlc[1]],'x',color='g',label='$\sigma_{CLR}(c \geq$' + str(400) + ' nm)')
plt.plot(AMPlc[0],[l for l in CLRlc[0]],'x',color='g')#,label='$\sigma_{CLR}(c =$' + str(420) + ' nm)')
# plt.plot(x_fit,y_fit,':')
# plt.plot(AMPlc[2],[l*1e9 for l in CLRlc[2]],':x',color='c',label='line-edge: $c =$' + str(300) + ' nm')
# plt.plot(AMPlc[3],[l*1e9 for l in CLRlc[3]],':x',color='m',label='line-edge: $c =$' + str(250) + ' nm')
# plt.text(15, 8,r'$\sigma_{S}$ ($c=35$ nm)',color='r',fontsize=8,rotation = 20) # '0.63 nm', color='g')
# plt.text(12, 9,r'$\sigma_{S}$ ($c=65$ nm)',color='b',fontsize=8,rotation = 30) # '0.63 nm', color='g')
# plt.text(-0.2, 3.5,r'$\sigma_{CLR}$ ($c=60$ nm)',color='black',fontsize=8,rotation = 35) # '0.63 nm', color='g')
# plt.text(1, 6,r'$\sigma_{CLR}$ ($c=420$ nm)',color='g',fontsize=8,rotation = 50) # '0.63 nm', color='g')
# plt.text(0, 8,r'$\sigma_{CLR}$ ($c=420$ nm)',color='g',fontsize=8)#,rotation = 50) # '0.63 nm', color='g')

# # Get the current axes
# ax = plt.gca()

# # Add rectangles to the plot
# for (x, y, w, h), color, alpha in zip(rectangles[0:2], colors[0:2], alphas[0:2]):
#     rect = patches.Rectangle((x, y), w, h, linewidth=1, edgecolor=None,
#                              facecolor=color, alpha=alpha)
#     ax.add_patch(rect)

# # plt.hlines(0.87,0,np.max(AMPs[0])*1e9,colors='gray',linestyles='--')
# # plt.hlines(0.35,0,np.max(AMPs[0])*1e9,colors='gray',linestyles='--')
# plt.text(10.1,1.6,'$L_{25}$', color='black', fontsize=8)
# plt.text(10.1,0.45,'$L_{10}$', color='black', fontsize=8)
plt.xlabel('Mask Roughness Amplitude ($\sigma$) [nm]')
plt.ylabel('$\Delta$CLR [nm]')
# plt.ylabel('CLR [nm]')
# plt.xlim((-1,np.max(AMPs[0])*1e9 + 1))
# plt.vlines(2.0,ymin=0.4,ymax=4,colors='gray',linestyles='dashed')
# plt.text(1.6,4.1,'2 nm', color='gray',fontsize=10)#'$\sigma_{EBL}$',color='gray',fontsize=10)
# plt.xlim((0,,np.max(AMPs[0])*1e9))
# plt.legend()
# plt.savefig('/user/home/opt/xl/xl/experiments/maskLER_retry2/figures/CLR.svg', bbox_inches='tight')
plt.show()

# X = np.linspace(0.5e-9,8.5e-9,100)
# Y = X*np.sqrt(2) - 2.e-9

# plt.plot(LERs[0],LWRs[0],'ro',mfc='none')#,label='surface: $c =$' + str(35) + ' nm')
# plt.plot(LERs[1],LWRs[1],'bo',mfc='none')#,label='surface: $c =$' + str(65) + ' nm')
# plt.plot(LERl,LWRl,'x',color='black')#,label='line-edge: $c =$' + str(60) + ' nm')
# plt.plot(LERlc[0],LWRlc[0],'x',color='g')#,label='line-edge: $c =$' + str(60) + ' nm')
# plt.plot(LERlc[1],LWRlc[1],'x',color='g')#,label='line-edge: $c =$' + str(60) + ' nm')
# plt.plot(X,Y,':')
# plt.xlabel('LER [nm]')
# # plt.ylabel('$\Delta$LWR / $\Delta$LER ')
# plt.ylabel('LWR [nm]')
# # plt.savefig('/user/home/opt/xl/xl/experiments/maskLER_retry2/figures/LWRoverLER.svg', bbox_inches='tight')
# plt.show()

Bler11 = [((l*1e9) / 1.2)**2 for l in dLER] 
Blwr11 = [((l*1e9) / 1.4)**2 for l in dLWR]
Bcdu11 = [((l*1e9) / 1.7)**2 for l in dCDU]

Bler10 = [((l*1e9) / 1.1)**2 for l in dLER] 
Blwr10 = [((l*1e9) / 1.2)**2 for l in dLWR]
Bcdu10 = [((l*1e9) / 1.5)**2 for l in dCDU]

Bler8 = [((l*1e9) / 0.8)**2 for l in dLER] 
Blwr8 = [((l*1e9) / 1.0)**2 for l in dLWR]
Bcdu8 = [((l*1e9) / 1.2)**2 for l in dCDU]




fig, ax = plt.subplots(1,1)
p8e, = ax.plot(dAMP,[1 - b for b in Bler8],'ro',mfc='none')#,label='CD = 8 nm')
p10e, = ax.plot(dAMP,[1 - b for b in Bler10],'bo',mfc='none')#,label='CD = 10 nm')
p11e, = ax.plot(dAMP,[1 - b for b in Bler11],'go',mfc='none')#,label='CD = 11 nm')
# p8w, = ax.plot(dAMP,Blwr8,'ro',mfc='none')#,label='CD = 8 nm')
# p10w, = ax.plot(dAMP,Blwr10,'bo',mfc='none')#,label='CD = 10 nm')
# p11w, = ax.plot(dAMP,Blwr11,'go',mfc='none')#,label='CD = 11 nm')
ax.set_xlabel('Mask Roughness Amplitude ($\sigma$) [nm]')
ax.set_ylabel(r'1 - $\omega$ (LER)')
ax.set_ylim((0,1))
ax.set_xlim((0,5))
# ax.legend([(p8e,p8w),(p10e,p10w),(p11e,p11w)], ['CD = 8 nm', 'CD = 10 nm', 'CD = 11 nm'],
#             handler_map={tuple: HandlerTuple(ndivide=None)},
#             title='X/O : LER/LWR')#' \n O = LWR')
# l = ax.legend([(p8e, p8w), p10e], ['data', 'models'],
#                handler_map={tuple: HandlerTuple(ndivide=None)})
# ax.legend()
# plt.savefig('/user/home/opt/xl/xl/experiments/maskLER_retry2/figures/omega_LER.svg', bbox_inches='tight')
plt.show()

plt.plot(dAMP,[1 - b for b in Blwr8],'ro',mfc='none',label='CD = 8 nm')
plt.plot(dAMP,[1 - b for b in Blwr10],'bo',mfc='none',label='CD = 10 nm')
plt.plot(dAMP,[1 - b for b in Blwr11],'go',mfc='none',label='CD = 11 nm')
plt.xlabel('Mask Roughness Amplitude ($\sigma$) [nm]')
plt.ylim((0,1))
plt.xlim((0,5))
plt.ylabel(r'1 - $\omega$ (LWR)')
plt.legend()
# plt.savefig('/user/home/opt/xl/xl/experiments/maskLER_retry2/figures/omega_LWR.svg', bbox_inches='tight')
plt.show()


plt.plot(dAMP,[1 - b for b in Bcdu8], 'ro', mfc='none')
plt.plot(dAMP,[1 - b for b in Bcdu10], 'bo', mfc='none')
plt.plot(dAMP,[1 - b for b in Bcdu11], 'go', mfc='none')
plt.xlabel('Mask Roughness Amplitude ($\sigma$) [nm]')
plt.ylim(0,1)
plt.xlim(0,5)
plt.ylabel(r'1 - $\omega$ (CDU)')
# plt.savefig('/user/home/opt/xl/xl/experiments/maskLER_retry2/figures/omega_CDU.svg', bbox_inches='tight')
plt.show()


plt.plot(dAMP,[1 - b for b in Bler11], 'ro', mfc='none', label='LER')
plt.plot(dAMP,[1 - b for b in Blwr11], 'bo', mfc='none', label='LWR')
plt.plot(dAMP,[1 - b for b in Bcdu11], 'go', mfc='none', label='CDU')
plt.xlabel('Mask Roughness Amplitude ($\sigma$) [nm]')
plt.ylabel(r'1 - $\omega$')
plt.ylim(0,1)
plt.xlim(0,5)
plt.title('CD = 11 nm')
plt.legend()
# plt.savefig('/user/home/opt/xl/xl/experiments/maskLER_retry2/figures/omega_CD11.svg', bbox_inches='tight')
plt.show()

plt.plot(dAMP,[1 - b for b in Bler10], 'ro', mfc='none', label='LER')
plt.plot(dAMP,[1 - b for b in Blwr10], 'bo', mfc='none', label='LWR')
plt.plot(dAMP,[1 - b for b in Bcdu10], 'go', mfc='none', label='CDU')
plt.xlabel('Mask Roughness Amplitude ($\sigma$) [nm]')
plt.ylabel(r'1 - $\omega$')
plt.ylim(0,1)
plt.xlim(0,5)
plt.title('CD = 10 nm')
plt.legend()
# plt.savefig('/user/home/opt/xl/xl/experiments/maskLER_retry2/figures/omega_CD10.svg', bbox_inches='tight')
plt.show()
    
plt.plot(dAMP,[1 - b for b in Bler8], 'ro', mfc='none', label='LER')
plt.plot(dAMP,[1 - b for b in Blwr8], 'bo', mfc='none', label='LWR')
plt.plot(dAMP,[1 - b for b in Bcdu8], 'go', mfc='none', label='CDU')
plt.xlabel('Mask Roughness Amplitude ($\sigma$) [nm]')
plt.ylabel(r'1 - $\omega$')
plt.ylim(0,1)
plt.xlim(0,5)
plt.title('CD = 8 nm')
plt.legend()
# plt.savefig('/user/home/opt/xl/xl/experiments/maskLER_retry2/figures/omega_CD8.svg', bbox_inches='tight')
plt.show()

# plt.plot(LWR/LER,AMPs[0],'ro',mfc='none')
# plt.plot(LWR/LER,AMPs[1],'bo',mfc='none')#,label='surface: $c =$' + str(65) + ' nm')
# plt.plot(LWR/LER,AMPl,'x',color='black')#,label='line-edge: $c =$' + str(60) + ' nm')
# plt.plot(LWR/LER,AMPlc[0],'x',color='g')#,label='line-edge: $c =$' + str(60) + ' nm')
# plt.plot([lw/le for lw,le in zip(LWR,LER)],AMPlc[1],'x',color='g')#,label='line-edge: $c =$' + str(60) + ' nm')
# # plt.plot(X,Y,':')
# plt.xlabel('Mask Roughness Amplitude ($\sigma$) [nm]')
# # plt.ylabel('$\Delta$LWR / $\Delta$LER ')
# plt.ylabel('LWR/LER')
# # plt.savefig('/user/home/opt/xl/xl/experiments/maskLER_retry2/figures/LWRoverLER.svg', bbox_inches='tight')
# plt.show()