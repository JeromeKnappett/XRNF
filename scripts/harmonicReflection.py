#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 11:51:29 2023

@author: jerome
"""

import numpy as np
import matplotlib.pyplot as plt
import xraydb

E = [90.44, 184.76]  # ,250]#,500] #184.76 # 130 #184.76 #90.44

harmonicWeights = [7.75, 1.25, 8, 3, 6.25]
hI = [
    [
        1164645337399296.0,
        185198984298496.0,
        1618014147444736.0,
        761429244772352.0,
        1651043578413056.0,
        1389956880662528.0,
        1577886058283008.0,
        1811446980673536.0,
        1513257567256576.0,
    ],
    [
        2266300160147456.0,
        611915509792768.0,
        2602019118383104.0,
        1900964547133440.0,
        2378011500347392.0,
        2650615806164992.0,
        2023216719593472.0,
        2802976489996288.0,
        1838728255373312.0,
    ],
]
# values for cff = 3
G = [1.6754999990165185, 1.173, 1.0083999999999946]  # ,0.7104]
M = [3.354, 2.3467, 2.0174]  # ,1.4265]
# #values for cff = 1.3
# G = [7.41969,5.19258,4.46423]#,0.7104]
# M = [6.56030,4.59231,3.94842]#,1.4265]

n = [
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
]  # np.linspace(1,20,4000) # [1,2,3,4,5,6,7,8,9] # np.linspace(1,10,2000) #[1,2,3,4,5]
ef = [
    0.1013,
    0.0,
    0.0113,
    0.0,
    0.0041,
    0.0,
    0.0021,
    0.0,
    0.0013,
]  # [0.1,0.0,0.01,0.0,0.001,0.0,0.0001,0.0,0.00001] # np.ones(len(n)) #[0.1,0.00001,0.01,0.00001,0.001]

IFE = []
EH = []
for _E, g, m, h in zip(E, G, M, hI):
    Eh = np.array(
        [_E * _n for _n in n]
    )  # np.array([184.76,2*184.76,3*184.76,4*184.76,5*184.76])
    EH.append(Eh)

    # print(np.shape(Eh))
    hp = True

    m1 = 1.3
    m2 = m  # 2
    m3 = 1.5
    # g = 1.6754999990165185 # 1.173 for 184.76 eV

    r1 = xraydb.mirror_reflectivity("Au", np.deg2rad(m1), Eh, polarization="p")
    r2 = xraydb.mirror_reflectivity("Au", np.deg2rad(m2), Eh, polarization="s")
    r3 = xraydb.mirror_reflectivity("Au", np.deg2rad(m3), Eh, polarization="p")
    rgAu = xraydb.mirror_reflectivity("Au", np.deg2rad(g), Eh, polarization="s")
    rgSi = xraydb.mirror_reflectivity("Si", np.deg2rad(g), Eh, polarization="s")

    # print(r1)
    # print(r2)
    # print(r3)
    # print(rgAu)
    # print(rgSi)
    IF = []
    for i, e in enumerate(Eh):
        # print(e)
        # print(i)
        # print(n[i])
        # I_f = r1[i]*r2[i]*r3[i]*(0.5*rgAu[i])  # without Si reflectivity term
        # I_f = r1[i]*r2[i]*r3[i]*(0.5*0.1*(rgAu[i] + rgSi[i]))  # without grating efficiency term
        # I_f = r1[i]*r2[i]*r3[i]*(0.5*(0.1**(i+1))*abs(rgAu[i] - rgSi[i]))  # without grating efficiency term
        # I_f = r1[i]*r2[i]*r3[i]*(0.5*ef[i]*(rgAu[i] + rgSi[i]))  # adding reflectivity of Au and Si
        I_f = (
            r1[i] * r2[i] * r3[i] * (0.5 * ef[i] * abs(rgAu[i] - rgSi[i]))
        )  # subtracting reflectivity of Au and Si
        # print(" ")
        # print(rgAu[i])
        # print(rgSi[i])
        # print(rgAu[i] - rgSi[i])
        IF.append(I_f)

    plt.plot(Eh / _E, r1, ".:", label="M1")
    plt.plot(Eh / _E, r2, ".:", label="M2")
    plt.plot(Eh / _E, r3, ".:", label="M3")
    plt.plot(Eh / _E, rgAu, ".:", label="$G_{Au}$")
    plt.plot(Eh / _E, rgSi, ".:", label="$G_{Si}$")
    # plt.yscale('log')
    plt.title(f"E = {_E} eV")
    plt.ylabel("Reflectivity")
    plt.xlabel("Harmonic Number")
    # plt.xlabel("Energy [eV]")
    plt.legend()
    plt.show()

    IFE.append(IF)


# c = ['blue','orange','green']

for i, e in enumerate(E):
    plt.plot(EH[i] / e, [efe * 100 for efe in IFE[i]], ".", label=f"E = {e} [eV]")
# plt.title(f"E = {E} eV")
plt.ylabel("Beamline Efficiency [\%]")
plt.xlabel("Harmonic Number")
# plt.xlabel("Energy [eV]")
plt.legend()
# plt.ylim([np.min(IF),np.max(IF)])
# plt.yscale('log')
plt.show()


hC_90 = np.sum(IFE[0][1::]) / IFE[0][0]
hC_185 = np.sum(IFE[1][1::]) / IFE[1][0]

IFE[0][1] / IFE[0][0]

# for i,e in enumerate(E):
#     plt.plot(EH[i][1::]/e,[(hi/hI[i][0])*100 for hi in hI[i][1:np.max(n)]],'.:',label=f'E = {e} [eV], @ source')
for i, e in enumerate(E):
    plt.plot(
        EH[i] / e,
        [(hi / hI[i][0]) * 100 for hi in hI[i]],
        ".:",
        label=f"E = {e} [eV], @ source",
    )
# plt.title(f"E = {E} eV")
plt.ylabel("Harmonic Contamination [\%]")
plt.xlabel("Harmonic Number")
# plt.xlabel("Energy [eV]")
plt.legend()
# plt.ylim([np.min(IF),np.max(IF)])
# plt.yscale('log')
plt.show()
print("here")
print((IFE[0][0] / IFE[0][0]) / (hI[0][0] / hI[0][0]) * 100)
for i, e in enumerate(E):
    print(
        [
            (efe / IFE[i][0]) * (hi / hI[i][0]) * 100
            for efe, hi in zip(IFE[i][1::], hI[i][1 : np.max(n)])
        ]
    )
    plt.plot(
        EH[i][1::] / e,
        [
            (efe / IFE[i][0]) * (hi / hI[i][0]) * 100
            for efe, hi in zip(IFE[i][1::], hI[i][1 : np.max(n)])
        ],
        ".:",
        label=f"E = {e} [eV] @ mask",
    )
# plt.title(f"E = {E} eV")
plt.ylabel("Harmonic Contamination [\%]")
plt.xlabel("Harmonic Number")
# plt.xlabel("Energy [eV]")
plt.legend()
# plt.ylim([np.min(IF),np.max(IF)])
# plt.yscale('log')
plt.show()

print(hC_90)
print(hC_185)
