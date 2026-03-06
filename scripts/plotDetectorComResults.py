#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 16:07:57 2023

@author: jerome
"""
import pickle
import plotting
import numpy as np

path = "/home/jerome/Downloads/results_cff1.4offset0.pkl"

P = pickle.load(open(path, "rb"))

# data
energy_range = P[0]
driftX, driftY = P[1], P[2]
iTot, er = P[3], P[4]
pTot, erP = P[5], P[6]
gsums, csums = P[7], P[8]
s = P[9]
FWHMx, FWHMy = P[10], P[11]

# sim
Ieuv, Ibeuv = P[12], P[13]
Peuv, Pbeuv = P[14], P[15]
IGeuv, IGbeuv = P[16], P[17]
PGeuv, PGbeuv = P[18], P[19]
Ceuv, Cbeuv = P[20], P[21]
Seuv, Sbeuv = P[22], P[23]
EfwhmX, EfwhmY, BfwhmX, BfwhmY = P[24], P[25], P[26], P[27]

# fits
H1I,H3I,H1P,H3P,H1G,H3G,H1C,H3C,H1S,H3S = P[28],P[29],P[30],P[31],P[32],P[33],P[34],P[35],P[36],P[37]
H1fwx,H1fwy,H3fwx,H3fwy = P[38],P[39],P[40],P[41]
H1FWx,H1FWy,H3FWx,H3FWy = P[42],P[43],P[44],P[45]
XPS,XPSe = P[46],P[47]

print(np.shape(energy_range))
print(np.shape(driftX))


midX = [2,
        2,2,2,
        10,10,10,
        9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,
        9,9,
        7,
        8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8]
midY = [2,
        2,2,2,
        2,
        6,6,6,6,
        10,10,10,
        5,5,5,5,5,5,
        4,4,4,4,4,4,4,
        1,1,1,1,1,1,1,
        0,0,0,0,0,0,0,0,0,0]

print(np.shape(midX))
print(np.shape(midY))

# print(np.shape(driftX))

driftX = [d + x for d,x in zip(driftX[0:21],midX)]
driftY = [d + y for d,y in zip(driftY[0:21],midY)]


# print(np.shape(driftX))
# print(np.shape(driftY))

# plotting.plotOneD(
#     [driftX, driftY],
#     sF=11,
#     error=[5.5, 5.5],
#     customX=[energy_range[0:21], energy_range[0:21]],
#     labels=["horizontal", "vertical"],
#     xLabel=["Photon Energy [eV]"],
#     yLabel=["Beam Drift [$\mu$m]"],
#     figSize=(3, 3),
#     lStyle="",
#     pStyle=".",
# )

#
#plotting.plotOneD(
#    [iTot[0:21], Ieuv, Ibeuv],
#    sF=1,
#    error=[er[0:21], None, None],
#    customX=[energy_range[0:21], 90, 185],
#    labels=["data", "simulation", None],
#    xLabel=["Photon Energy [eV]"],
#    yLabel=["Total Intensity [ph/s/cm$^2$]"],
#    figSize=(3, 3),
#    lStyle="",
#    pStyle=[".", "x", "x"],
#    color=[0, 1, 1],
#)
#
#plotting.plotOneD(
#    [H1I[0:21], Ieuv, Ibeuv],
#    sF=1,
#    # error=[er[0:21], None, None],
#    customX=[energy_range[0:21], 90, 185],
#    labels=["fit to data", "simulation", None],
#    xLabel=["Photon Energy [eV]"],
#    yLabel=["Total Intensity [ph/s/cm$^2$]"],
#    figSize=(3, 3),
#    lStyle="",
#    pStyle=[".", "x", "x"],
#    color=[0, 1, 1],
#)

plotting.plotOneD([
    # [iTot[0:21], 
     H1I[0:21],H3I[0:21], [Ieuv[0]], [Ibeuv[0]]],
    sF=1,
    # error=[er[0:21], None, None, None, None],
    customX=[energy_range[0:21], energy_range[0:21], 90, 185],
    labels=[
        # "data",
            "H1 fit", "H3 fit","simulation", None],
    xLabel=["Photon Energy [eV]"],
    yLabel=["Total Intensity [ph/s/cm$^2$]"],
    figSize=(3, 3),
    lStyle="",
    pStyle=[".", ".", "x", "x"],
    color=[
        # 0, 
        2, 3, 1, 1],
)

#
#plotting.plotOneD(
#    [pTot[0:21], Peuv, Pbeuv],
#    sF=1,
#    error=[erP[0:21], None, None],
#    customX=[energy_range[0:21], 90, 185],
#    labels=["data", "simulation", None],
#    xLabel=["Photon Energy [eV]"],
#    yLabel=["Total Power [mJ/s/cm$^2$]"],
#    figSize=(3, 3),
#    lStyle="",
#    pStyle=[".", "x", "x"],
#    color=[0, 1, 1],
#)
#
#plotting.plotOneD(
#    [H1P[0:21], Peuv, Pbeuv],
#    sF=1,
#    # error=[erP[0:21], None, None],
#    customX=[energy_range[0:21], 90, 185],
#    labels=["fit to data", "simulation", None],
#    xLabel=["Photon Energy [eV]"],
#    yLabel=["Total Power [mJ/s/cm$^2$]"],
#    figSize=(3, 3),
#    lStyle="",
#    pStyle=[".", "x", "x"],
#    color=[0, 1, 1],
#)


plotting.plotOneD([
    # [pTot[0:21], 
     H1P[0:21], H3P[0:21], [Peuv[0]], [Pbeuv[0]]],
    sF=1,
    # error=[erP[0:21], None, None,None, None],
    customX=[energy_range[0:21], energy_range[0:21], 90, 185],
    labels=[
        # "data",
            "H1 fit", "H3 fit", "simulation", None],
    xLabel=["Photon Energy [eV]"],
    yLabel=["Total Power [mJ/s/cm$^2$]"],
    figSize=(3, 3),
    lStyle="",
    pStyle=[".", ".", "x", "x"],
    color=[2, 3, 1, 1],
)


#
#plotting.plotOneD(
#    [gsums[0:21], IGeuv, IGbeuv],
#    sF=1,
#    error=None,
#    customX=[energy_range[0:21], 90, 185],
#    labels=["data", "simulation", None],
#    xLabel=["Photon Energy [eV]"],
#    yLabel=["Total Intensity over Grating [ph/s/cm$^2$]"],
#    figSize=(3, 3),
#    lStyle="",
#    pStyle=[".", "x", "x"],
#    color=[0, 1, 1],
#)
#
#plotting.plotOneD(
#    [H1G[0:21], IGeuv, IGbeuv],
#    sF=1,
#    error=None,
#    customX=[energy_range[0:21], 90, 185],
#    labels=["fit to data", "simulation", None],
#    xLabel=["Photon Energy [eV]"],
#    yLabel=["Total Intensity over Grating [ph/s/cm$^2$]"],
#    figSize=(3, 3),
#    lStyle="",
#    pStyle=[".", "x", "x"],
#    color=[0, 1, 1],
#)


plotting.plotOneD([
    # [gsums[0:21], 
     H1G[0:21], H3G[0:21], [IGeuv[0]], [IGbeuv[0]]],
    sF=1,
    customX=[energy_range[0:21], energy_range[0:21], 90, 185],
    labels=[
        # "data",
            "H1 fit", "H3 fit", "simulation", None],
    xLabel=["Photon Energy [eV]"],
    yLabel=["Total Intensity over Grating [ph/s/cm$^2$]"],
    figSize=(3, 3),
    lStyle="",
    pStyle=[".", ".", "x", "x"],
    color=[2, 3, 1, 1],
)

q = 1.60218e-19
gPsums = [g*q*e*1000 for g,e in zip(gsums,energy_range)]
H1GP = [g*q*e*1000 for g,e in zip(H1G,energy_range)]
H3GP = [g*q*e*1000 for g,e in zip(H3G,energy_range)]

plotting.plotOneD([
    # [gPsums[0:21], 
     H1GP[0:21], H3GP[0:21], [PGeuv[0]], [PGbeuv[0]]],
    sF=1,
    customX=[energy_range[0:21], energy_range[0:21], 90, 185],
    labels=[
        # "data",
            "H1 fit", "H3 fit", "simulation", None],
    xLabel=["Photon Energy [eV]"],
    yLabel=["Total Power over Grating [mJ/s/cm$^2$]"],
    figSize=(3, 3),
    lStyle="",
    pStyle=[".", ".", "x", "x"],
    color=[2, 3, 1, 1],
)

#
#plotting.plotOneD(
#    [s[0:21], [Seuv], [Sbeuv]],
#    sF=1,
#    error=None,
#    customX=[energy_range[0:21], 90, 185],
#    labels=["data", "simulation", None],
#    xLabel=["Photon Energy [eV]"],
#    yLabel=["Intensity Slope over Grating Area"],
#    figSize=(3, 3),
#    lStyle="",
#    pStyle=[".", "x", "x"],
#    color=[0, 1, 1],
#)
#
#plotting.plotOneD(
#    [H1S[0:21], [Seuv], [Sbeuv]],
#    sF=1,
#    error=None,
#    customX=[energy_range[0:21], 90, 185],
#    labels=["fit to data", "simulation", None],
#    xLabel=["Photon Energy [eV]"],
#    yLabel=["Intensity Slope over Grating Area"],
#    figSize=(3, 3),
#    lStyle="",
#    pStyle=[".", "x", "x"],
#    color=[0, 1, 1],
#)


plotting.plotOneD([
    # [s[0:21], 
     H1S[0:21], H3S[0:21], [Seuv], [Sbeuv]],
    sF=1,
    error=None,
    customX=[energy_range[0:21], energy_range[0:21], 90, 185],
    labels=[
        # "data",
        "H1 fit", "H3 fit", "simulation", None],
    xLabel=["Photon Energy [eV]"],
    yLabel=["Intensity Slope over Grating Area"],
    figSize=(3, 3),
    lStyle="",
    pStyle=[".", ".", "x", "x"],
    color=[2, 3, 1, 1],
)

#plotting.plotOneD(
#    [FWHMx[0:21], FWHMy[0:21], [EfwhmX], [EfwhmY], [BfwhmX], [BfwhmY]],
#    sF=1e3,
#    error=None,  # [11e-3,11e-3,11e-3,11e-3,11e-3,11e-3],
#    customX=[energy_range[0:21], energy_range[0:21], 90, 90, 185, 185],
#    labels=[
#        "horizontal (data)",
#        "vertical (data)",
#        "horizontal (simulation)",
#        "vertical (simulation)",
#        None,
#        None,
#    ],
#    xLabel=["Photon Energy [eV]"],
#    yLabel=["Intensity FWHM [mm]"],
#    figSize=(3, 3),
#    lStyle="",
#    pStyle=["*", "*", "x", "x", "x", "x"],
#    color=[0, 1, 2, 3, 2, 3],
#)
#
#
#plotting.plotOneD(
#    [[h*1e-3 for h in H1FWx[0:21]],[h*1e-3 for h in H1FWy[0:21]], [EfwhmX], [EfwhmY], [BfwhmX], [BfwhmY]],
#    sF=1e3,
#    error=None,  # [11e-3,11e-3,11e-3,11e-3,11e-3,11e-3],
#    customX=[energy_range[0:21], energy_range[0:21], 90, 90, 185, 185],
#    labels=[
#        "horizontal (fit)",
#        "vertical (fit)",
#        "horizontal (simulation)",
#        "vertical (simulation)",
#        None,
#        None,
#    ],
#    xLabel=["Photon Energy [eV]"],
#    yLabel=["Intensity FWHM [mm]"],
#    figSize=(3, 3),
#    lStyle="",
#    pStyle=[".", ".", "x", "x", "x", "x"],
#    color=[0, 1, 2, 3, 2, 3],
#)

print('\n',np.shape(H1FWx))
print(H1FWx)

plotting.plotOneD([
    # [FWHMx[0:21], FWHMy[0:21],
     [h for h in H1fwx[0:21]],[h for h in H1fwy[0:21]], [EfwhmX], [EfwhmY], [BfwhmX], [BfwhmY]],
    sF=1e3,
    error=None,  # [11e-3,11e-3,11e-3,11e-3,11e-3,11e-3],
    customX=[energy_range[0:21], energy_range[0:21], 90, 90, 185, 185],
    labels=[
        # "x (data)",
        # "y (data)",
        "x (H1 fit)",
        "y (H1 fit)",
        "x (simulation)",
        "y (simulation)",
        None,
        None,
    ],
    xLabel=["Photon Energy [eV]"],
    yLabel=["Intensity FWHM [mm]"],
    figSize=(3, 3),
    lStyle="",
    pStyle=[".", ".", "x", "1", "x", "1"],
    color=[2, 3, 1, 1, 1, 1],
)



plotting.plotOneD([
    # [FWHMx[0:21], 
     [h for h in H1fwx[0:21]],[h for h in H3fwx[0:21]],[EfwhmX],[BfwhmX]],
    sF=1e3,
    error=None,  # [11e-3,11e-3,11e-3,11e-3,11e-3,11e-3],
    customX=[energy_range[0:21], energy_range[0:21], 90, 185],
    labels=[
        # "data",
        "H1 fit",
        "H3 fit",
        "simulation",
        None,
    ],
    xLabel=["Photon Energy [eV]"],
    yLabel=["Horizontal Intensity FWHM [mm]"],
    figSize=(3, 3),
    lStyle="",
    pStyle=[".",".", "x", "x"],
    color=[2, 3, 1, 1]
)

plotting.plotOneD([
    # [FWHMy[0:21], 
     [h*1e-3 for h in H1FWy[0:21]],[h*1e-3 for h in H3FWy[0:21]],[EfwhmY],[BfwhmY]],
    sF=1e3,
    error=None,  # [11e-3,11e-3,11e-3,11e-3,11e-3,11e-3],
    customX=[energy_range[0:21], energy_range[0:21], 90, 185],
    labels=[
        # "data",
        "H1 fit",
        "H3 fit",
        "simulation",
        None,
    ],
    xLabel=["Photon Energy [eV]"],
    yLabel=["Vertical Intensity FWHM [mm]"],
    figSize=(3, 3),
    lStyle="",
    pStyle=[".",".", "x", "x"],
    color=[2, 3, 1, 1]
)

# plotting.plotOneD(
#     [h1/(h1+h3) for h1,h3 in zip(H1G,H3G)],
#     sF=1,
#     error=None,
#     customX=[energy_range[0:21]],
#     labels=["fit to data"],
#     xLabel=["Photon Energy [eV]"],
#     yLabel=["Fraction of Intensity over Grating [ph/s/cm$^2$]"],
#     figSize=(3, 3),
#     lStyle="",
#     pStyle=["."],
#     color=0,
# )

T1 = [g + c for g,c in zip(H1G,H1C)]
T3 = [g + c for g,c in zip(H3G,H3C)]

import matplotlib.pyplot as plt
# #plt.plot(energy_range[0:21],[h1/(h1+h3) for h1,h3 in zip(H1G,H3G)],'.',label='grating')
# #plt.plot(energy_range[0:21],[h1/(h1+h3) for h1,h3 in zip(H1C,H3C)],'.',label='center')
# plt.plot(energy_range[0:21],[h1/(h1+h3) for h1,h3 in zip(T1[0:21],T3[0:21])],'.',label='both')
# plt.xlabel('Photon Energy [eV]')
# plt.ylabel('Fraction of Fundamental Harmonic in Total Intensity')
# #plt.legend()
# plt.show()

# #plt.plot(energy_range[0:21],[h3/(h1+h3) for h1,h3 in zip(H1G,H3G)],'.',label='grating')
# #plt.plot(energy_range[0:21],[h3/(h1+h3) for h1,h3 in zip(H1C,H3C)],'.',label='center')
# plt.plot(energy_range[0:21],[h3/(h1+h3) for h1,h3 in zip(T1[0:21],T3[0:21])],'.',label='both')
# plt.xlabel('Photon Energy [eV]')
# plt.ylabel('Fraction of 3rd Harmonic in Total Intensity')
# #plt.legend()
# plt.show()

# #plt.plot(energy_range[0:21],[h3/h1 for h1,h3 in zip(H1G,H3G)],'.',label='grating')
# #plt.plot(energy_range[0:21],[h3/h1 for h1,h3 in zip(H1C,H3C)],'.',label='center')
# plt.plot(energy_range[0:21],[h3/h1 for h1,h3 in zip(T1[0:21],T3[0:21])],'.',label='both')
# plt.xlabel('Photon Energy [eV]')
# plt.ylabel('Ratio of Intensities of 1st and 3rd Harmonic')
# #plt.legend()
# plt.show()

# #plt.plot(energy_range[1:21],[h1/h3 for h1,h3 in zip(H1G[1::],H3G[1::])],'.',label='grating')
# #plt.plot(energy_range[1:21],[h1/h3 for h1,h3 in zip(H1C[1::],H3C[1::])],'.',label='center')
# plt.plot(energy_range[1:21],[h1/h3 for h1,h3 in zip(T1[1:21],T3[1:21])],'.',label='both')
# plt.xlabel('Photon Energy [eV]')
# plt.ylabel('Ratio of Intensities of 3rd and 1st Harmonic')
# #plt.legend()
# plt.show()

# plt.plot(energy_range[0:len(H1G)],[g1/(g1 + g3) for g1,g3 in zip(H1I,H3I)],'.',label='Fundamental')
plt.plot(energy_range[0:len(H1G)],[g3/(g1 + g3) for g1,g3 in zip(H1I,H3I)],'.',label='Total I')
# plt.plot(energy_range[0:len(H1G)],[g3/(g1 + g3) for g1,g3 in zip(T1,T3)],'.',label='I over grating')
plt.plot(XPSe,[np.sum(x[1::]) for x in XPS],'x',label='XPS data')
plt.xlabel('Photon Energy [eV]')
plt.ylabel('$I_3 / I_{sum}$')
plt.legend()
plt.show()

# (p,
#              d=1,
#              sF=1,
#              xlim=None,
#              ylim=None,
#              error = None,
#              describe=False,
#              split=None,
#              customX = None,
#              title=None,
#              labels=None,
#              xLabel=None,
#              yLabel=None,
#              figSize=(10,12),
#              aspct='auto',
#              lStyle='-',
#              lWidth=1,
#              pStyle='',
#              fSize=10,
#              color= None,
#              savePath=None):
