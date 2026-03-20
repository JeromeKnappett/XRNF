#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  2 11:29:21 2023

@author: jerome
"""

import numpy as np
import matplotlib.pyplot as plt
import imageio


def round_sig(x, sig=2):
    from math import floor, log10

    if x != 0:
        return round(x, sig - int(floor(log10(abs(x)))) - 1)
    else:
        return x

from bisect import bisect_left

def take_closest(myList, myNumber):
    """
    Assumes myList is sorted. Returns closest value to myNumber.

    If two numbers are equally close, return the smallest number.
    """
    pos = bisect_left(myList, myNumber)
    if pos == 0:
        return myList[0]
    if pos == len(myList):
        return myList[-1]
    before = myList[pos - 1]
    after = myList[pos]
    if after - myNumber < myNumber - before:
        return after
    else:
        return before

colours = plt.rcParams["axes.prop_cycle"].by_key()["color"]
fSize = 6
#dirPath = "/home/jerome/dev/data/spectralDetuning/"
#savePath = dirPath
#M = [1, 3, 5, 7, 9, 11]
#
#save = False
#
#E0 = 187.38631882706142  # 184.76
#dE = 10

dirPath = '/user/home/data/spectralDetuning/'
#'/home/jerome/Documents/PhD/Data/'
#"/home/jerome/dev/data/spectralDetuning/"
M = [1]#, 3, 5]

Bf = [0.4605,0.4571,0.4530]
nameModifier = ['','_detuned','_detuned2']
colours = ['black','red','blue']
styles = ['solid','dashed','dotted']


save = False

EF = 185.0
dE = 10

savePath = dirPath + str(int(EF)) + '/'
# save = True
# savePath = '/home/jerome/Documents/MASTERS/Figures/plots/'

n_flux = 'res_flux_' + str(int(EF)) + '_'
n_brilliance = 'res_brilliance_' + str(int(EF)) + '_'
OFF = []

B = []
DELTA = []

# Flux plots
Ffiles = [n_flux + str(m) + nameModifier[0] + ".dat" for m in M]
for i, f in enumerate(Ffiles):
    D = np.loadtxt(savePath + f, dtype=str, comments=None, skiprows=1)
    f = np.array(D[:, 1], dtype="float")
    e = np.array(D[:, 0], dtype="float")

    if i ==0:
        E0 = e[len(e)//2]
        # dE = E0 - EF
        # offset = (dE/EF)*100
        dB = Bf[0] - Bf[0]
        offset = (dB/Bf[0])*100
        OFF.append(offset)
        plt.plot(e, f, label="m = " + str(M[i]),color=colours[0], linestyle=styles[i])
    else:
        e = [_e - (M[i]-1)*E0 for _e in e]
        # print('hereh', e)
        plt.plot(e, f,label="m = " + str(M[i]),color=colours[0], linestyle=styles[i])
    delta = e - E0 * M[i]

    B.append(f)
    DELTA.append(delta)

plt.ylabel("Flux [ph/s/.1\%bw]")
plt.xlabel("Photon Energy [eV]")
plt.legend()
if save:
    plt.savefig(savePath + "flux.png")
#plt.show()


# # Finding brilliance difference with no detuning
x0 = E0 #DELTA[0][np.where(abs(DELTA[0]) == abs(DELTA[0]-E0).min())]
B0 = B[0][np.where(abs(DELTA[0]) == abs(DELTA[0]).min())]
# Bdif_0 = [b[np.where(abs(DELTA[0]) == abs(DELTA[0]).min())] / B0 for b in B[1::]]

# print('here', x0)
# for i, bd in enumerate(Bdif_0):
#     plt.text(
#         x=x0 + 5,
#         y=(B0/10) * (i+12),
#         s="$B_0 (m= $"
#         + str(M[i + 1])
#         + ") = "
#         + str(round_sig(float(bd)))
#         + "$B_0 (m=1)$",
#         fontsize=6,
#     )


# Finding difference at desired fundamental energy
# print('here')
# print(E0)
# print(EF)
Ed = EF-E0
# print(Ed)
# print(np.shape(DELTA))
xF = take_closest(e, EF)
# min(DELTA, key=lambda x:abs(x-Ed))
#take_closest(DELTA, E0-EF)
#DELTA[0][np.where(E0 - DELTA[0] == EF)]
BF = B[0][np.where(e == xF)]
Bdif_F = [b[np.where(B[0] == BF)] / BF for b in B[1::]]

# print('xf = ', xF)
# print('bf = ', BF)
# print('bdif_f = ', Bdif_F)

plt.axvline(x=xF, linestyle=":", color="gray")
# plt.text(
#     x=xF + 0.5,
#     y=0.5e9,
#     s="E=" + str(round_sig(float(xF), 5)),
#     fontsize=6,
#     color="gray",
# )

plt.text(x=195,y=4.5e9,s=str(round_sig(OFF[0],3)) + '% offset',fontsize=fSize,color=colours[0])
plt.text(x=196.5,y=4.25e9, s="$E_0$=" + str(round_sig(E0,5)) +' eV', fontsize=fSize,color=colours[0])
# for i, bf in enumerate(Bdif_F):
#     print('\n')
#     print(bf)
#     plt.text(
#         x=x0 + 7.75,
#         y=(B0/10) * (i+4),
#         s="$B(m= $" + str(M[i + 1]) + ") = " + str(round_sig(float(bf))) + "$B(m=1)$",
#         fontsize=6,
#         color=colours[0],
#     )

# plt.text(x = x0 + 10, y = (B0 / 10) * (2 + 8), s = str(round_sig(((float(E0 + xbest) - E0)/E0)*100)) + '% offset',fontsize=6,color='blue')
# plt.text(x = x0 + 10, y = (B0 / 10) * (2 + 12), s = str(round_sig(((float(E0 + xp) - E0)/E0)*100)) + '% offset',fontsize=6,color='gray')

# bestEnergy = DELTA[0][np.where(Bdifmean == Bdifmean.min())]
# plt.axvline(x=bestEnergy, linestyle=':',color='black')
# plt.text(x=1,y=0.2e13,s='E = ' + str(bestEnergy) + ' eV')

print('Peak Flux: ', np.max(B))


B = []
DELTA = []
Ffiles = [n_flux + str(m) + nameModifier[1] + ".dat" for m in M]
for i, f in enumerate(Ffiles):
    D = np.loadtxt(savePath + f, dtype=str, comments=None, skiprows=1)
    f = np.array(D[:, 1], dtype="float")
    e = np.array(D[:, 0], dtype="float")

    if i ==0:
        E0 = e[len(e)//2]
        # dE = E0 - EF
        # offset = (dE/EF)*100
        dB = Bf[1] - Bf[0]
        offset = (dB/Bf[0])*100
        OFF.append(offset)
        plt.plot(e, f, label="m = " + str(M[i]),color=colours[1], linestyle=styles[i])
    else:
        e = [_e - (M[i]-1)*E0 for _e in e]
        # print('hereh', e)
        plt.plot(e, f,label="m = " + str(M[i]),color=colours[1], linestyle=styles[i])
    delta = e - E0 * M[i]

    B.append(f)
    DELTA.append(delta)

plt.ylabel("Flux [ph/s/.1\%bw]")
plt.xlabel("Photon Energy [eV]")
# plt.legend()
if save:
    plt.savefig(savePath + "flux.png")
#plt.show()


# # Finding brilliance difference with no detuning
x0 = E0 #DELTA[0][np.where(abs(DELTA[0]) == abs(DELTA[0]-E0).min())]
B0 = B[0][np.where(abs(DELTA[0]) == abs(DELTA[0]).min())]

# Finding difference at desired fundamental energy
# print('here')
# print(E0)
# print(EF)
Ed = EF-E0
# print(Ed)
# print(np.shape(DELTA))
# xF = take_closest(e, EF)
# min(DELTA, key=lambda x:abs(x-Ed))
#take_closest(DELTA, E0-EF)
#DELTA[0][np.where(E0 - DELTA[0] == EF)]
BF = B[0][np.where(e == xF)]
Bdif_F = [b[np.where(B[0] == BF)] / BF for b in B[1::]]

# print('xf = ', xF)
# print('bf = ', BF)
# print('bdif_f = ', Bdif_F)

# plt.axvline(x=xF, linestyle=":", color="blue")
# plt.text(
#     x=xF + 0.5,
#     y=0.5e9,
#     s="E=" + str(round_sig(float(xF), 5)),
#     fontsize=6,
#     color='gray'',
# )

plt.text(x=195,y=4.0e9,s=str(round_sig(OFF[1],3)) + '% offset',fontsize=fSize,color=colours[1])
plt.text(x=196.5,y=3.75e9, s="$E_0$=" + str(round_sig(E0,5)) +' eV', fontsize=6,color=colours[1])
# for i, bf in enumerate(Bdif_F):
#     # print('\n')
#     # print(bf)
#     # print(M[i+1])
#     plt.text(
#         x=x0 + 5,
#         y=(B0/10) * (i+8),
#         s="$B(m= $" + str(M[i + 1]) + ") = " + str(round_sig(float(bf))) + "$B(m=1)$",
#         fontsize=6,
#         color=colours[1],
#     )
    

print('Peak Flux: ', np.max(B))

B = []
DELTA = []
Ffiles = [n_flux + str(m) + nameModifier[2] + ".dat" for m in M]
for i, f in enumerate(Ffiles):
    D = np.loadtxt(savePath + f, dtype=str, comments=None, skiprows=1)
    f = np.array(D[:, 1], dtype="float")
    e = np.array(D[:, 0], dtype="float")

    if i ==0:
        E0 = e[len(e)//2]
        # dE = E0 - EF
        # offset = (dE/EF)*100
        dB = Bf[2] - Bf[0]
        offset = (dB/Bf[0])*100
        OFF.append(offset)
        plt.plot(e, f, label="m = " + str(M[i]),color=colours[2], linestyle=styles[i])
    else:
        e = [_e - (M[i]-1)*E0 for _e in e]
        # print('hereh', e)
        plt.plot(e, f,label="m = " + str(M[i]),color=colours[2], linestyle=styles[i])
    delta = e - E0 * M[i]

    B.append(f)
    DELTA.append(delta)

plt.ylabel("Flux [ph/s/.1\%bw]")
plt.xlabel("Photon Energy [eV]")
# plt.legend()
if save:
    plt.savefig(savePath + "flux.png")
#plt.show()


# # Finding brilliance difference with no detuning
x0 = E0 #DELTA[0][np.where(abs(DELTA[0]) == abs(DELTA[0]-E0).min())]
B0 = B[0][np.where(abs(DELTA[0]) == abs(DELTA[0]).min())]

# Finding difference at desired fundamental energy
# print('here')
# print(E0)
# print(EF)
Ed = EF-E0
# print(Ed)
# print(np.shape(DELTA))
xF = take_closest(e, EF)
# min(DELTA, key=lambda x:abs(x-Ed))
#take_closest(DELTA, E0-EF)
#DELTA[0][np.where(E0 - DELTA[0] == EF)]
BF = B[0][np.where(e == xF)]
Bdif_F = [b[np.where(B[0] == BF)] / BF for b in B[1::]]

# print('xf = ', xF)
# print('bf = ', BF)
# print('bdif_f = ', Bdif_F)

# plt.axvline(x=xF, linestyle=":", color="blue")
# plt.text(
#     x=xF + 0.5,
#     y=0.5e9,
#     s="E=" + str(round_sig(float(xF), 5)),
#     fontsize=6,
#     color='gray'',
# )

plt.text(x=195,y=3.5e9,s=str(round_sig(OFF[2],3)) + '% offset',fontsize=fSize,color=colours[2])
plt.text(x=196.5,y=3.25e9, s="$E_0$=" + str(round_sig(E0,5)) +' eV', fontsize=6,color=colours[2])
# for i, bf in enumerate(Bdif_F):
#     print('\n')
#     print(bf)
#     plt.text(
#         x=x0 + 5,
#         y=(B0/10) * (i+8),
#         s="$B(m= $" + str(M[i + 1]) + ") = " + str(round_sig(float(bf))) + "$B(m=1)$",
#         fontsize=6,
#         color=colours[2],
#     )


plt.show()


print('Peak Flux: ', np.max(B))

# print("Optimised undulator offset for flux [%]: ", ((float(E0 + xp) - E0)/E0)*100 )
# print("Optimised undulator offset for harmonic suppression [%]: ", ((float(E0 + xbest) - E0)/E0)*100 )

print("Optimised undulator offset from fundamental for flux [%]: ", offset )


OFF = []
B = []
DELTA = []

# Brilliance plots
Bfiles = [n_brilliance + str(m) + nameModifier[0] + ".dat" for m in M]
for i, f in enumerate(Bfiles):
    D = np.loadtxt(savePath + f, dtype=str, comments=None, skiprows=1)
    f = np.array(D[:, 1], dtype="float")
    e = np.array(D[:, 0], dtype="float")
    
    if i ==0:
        E0 = e[len(e)//2]
        # dE = E0 - EF
        # offset = (dE/EF)*100
        dB = Bf[0] - Bf[0]
        offset = (dB/Bf[0])*100
        OFF.append(offset)
        plt.plot(e, f, label="m = " + str(M[i]),color=colours[0], linestyle=styles[i])
    else:
        e = [_e - (M[i]-1)*E0 for _e in e]
        # print('hereh', e)
        plt.plot(e, f,label="m = " + str(M[i]),color=colours[0], linestyle=styles[i])
    delta = e - E0 * M[i]

    B.append(f)
    DELTA.append(delta)


plt.ylabel("Brilliance [ph/s/.1/mr$^2$/mm$^2$]")
plt.xlabel("Photon Energy [eV]")
plt.legend()
if save:
    plt.savefig(savePath + "brilliance.png")
#plt.show()

# Finding brilliance difference with no detuning
x0 = E0 #DELTA[0][np.where(abs(DELTA[0]) == abs(DELTA[0]-E0).min())]
B0 = B[0][np.where(abs(DELTA[0]) == abs(DELTA[0]).min())]
# Bdif_0 = [b[np.where(abs(DELTA[0]) == abs(DELTA[0]).min())] / B0 for b in B[1::]]


# Finding difference at desired fundamental energy
# print('here')
# print(E0)
# print(EF)
Ed = EF-E0
# print(Ed)
# print(np.shape(DELTA))
xF = take_closest(e, EF)
# min(DELTA, key=lambda x:abs(x-Ed))
#take_closest(DELTA, E0-EF)
#DELTA[0][np.where(E0 - DELTA[0] == EF)]
BF = B[0][np.where(e == xF)]
Bdif_F = [b[np.where(B[0] == BF)] / BF for b in B[1::]]

# print('xf = ', xF)
# print('bf = ', BF)
# print('bdif_f = ', Bdif_F)

# plt.axvline(x=xF, linestyle=":", color="blue")
# plt.text(
#     x=xF + 0.5,
#     y=0.5e9,
#     s="E=" + str(round_sig(float(xF), 5)),
#     fontsize=6,
#     color=colours[0],
# )
# for i, bf in enumerate(Bdif_F):
#     print('\n')
#     print(bf)
#     plt.text(
#         x=x0 + 5,
#         y=(B0/10) * (i+8),
#         s="$B(m= $" + str(M[i + 1]) + ") = " + str(round_sig(float(bf))) + "$B(m=1)$",
#         fontsize=6,
#         color=colours[0],
#     )

if np.max(B) >= 1.1e13:
    plt.text(x=195,y=1.5e13,s=str(round_sig(OFF[0],3)) + '% offset',fontsize=fSize,color=colours[0])
    plt.text(x=196.5,y=1.4e13, s="$E_0$=" + str(round_sig(E0,5)) +' eV', fontsize=fSize,color=colours[0])
else:
    plt.text(x=195,y=7.5e12,s=str(round_sig(OFF[0],3)) + '% offset',fontsize=fSize,color=colours[0])
    plt.text(x=196.5,y=7.0e12, s="$E_0$=" + str(round_sig(E0,5)) +' eV', fontsize=fSize,color=colours[0])

    
# plt.text(x = x0 - 5, y = (B0 / 6) * (12), s = str(round_sig(((float(E0 + xbest) - E0)/E0)*100)) + '% offset',fontsize=6,color='blue')
# plt.text(x = x0 - 5, y = (B0 / 6) * (16), s = str(round_sig(((float(E0 + xp) - E0)/E0)*100)) + '% offset',fontsize=6,color='gray')

# bestEnergy = DELTA[0][np.where(Bdifmean == Bdifmean.min())]
# plt.axvline(x=bestEnergy, linestyle=':',color='black')
# plt.text(x=1,y=0.2e13,s='E = ' + str(bestEnergy) + ' eV')

print('Peak Brilliance: ', np.max(B))


B = []
DELTA = []
Bfiles = [n_brilliance + str(m) + nameModifier[1] + ".dat" for m in M]
for i, f in enumerate(Bfiles):
    D = np.loadtxt(savePath + f, dtype=str, comments=None, skiprows=1)
    f = np.array(D[:, 1], dtype="float")
    e = np.array(D[:, 0], dtype="float")
    
    if i ==0:
        E0 = e[len(e)//2]
        # dE = E0 - EF
        # offset = (dE/EF)*100
        dB = Bf[1] - Bf[0]
        offset = (dB/Bf[0])*100
        OFF.append(offset)
        plt.plot(e, f, label="m = " + str(M[i]),color=colours[1], linestyle=styles[i])
    else:
        e = [_e - (M[i]-1)*E0 for _e in e]
        # print('hereh', e)
        plt.plot(e, f,label="m = " + str(M[i]),color=colours[1], linestyle=styles[i])
    delta = e - E0 * M[i]

    B.append(f)
    DELTA.append(delta)

plt.ylabel("Brilliance [ph/s/.1/mr$^2$/mm$^2$]")
plt.xlabel("Photon Energy [eV]")
# plt.legend()
if save:
    plt.savefig(savePath + "brilliance.png")
#plt.show()

# Finding brilliance difference with no detuning
x0 = E0 #DELTA[0][np.where(abs(DELTA[0]) == abs(DELTA[0]-E0).min())]
B0 = B[0][np.where(abs(DELTA[0]) == abs(DELTA[0]).min())]

# Finding difference at desired fundamental energy
Ed = EF-E0
xF = take_closest(e, EF)
# min(DELTA, key=lambda x:abs(x-Ed))
#take_closest(DELTA, E0-EF)
#DELTA[0][np.where(E0 - DELTA[0] == EF)]
BF = B[0][np.where(e == xF)]
Bdif_F = [b[np.where(B[0] == BF)] / BF for b in B[1::]]

# print('xf = ', xF)
# print('bf = ', BF)
# print('bdif_f = ', Bdif_F)

# plt.axvline(x=xF, linestyle=":", color="blue")
# plt.text(
#     x=xF + 0.5,
#     y=0.5e9,
#     s="E=" + str(round_sig(float(xF), 5)),
#     fontsize=6,
#     color=colours[1],
# )
# for i, bf in enumerate(Bdif_F):
#     print('\n')
#     print(bf)
#     plt.text(
#         x=x0 + 5,
#         y=(B0/10) * (i+8),
#         s="$B(m= $" + str(M[i + 1]) + ") = " + str(round_sig(float(bf))) + "$B(m=1)$",
#         fontsize=6,
#         color=colours[1],
#     )

if np.max(B) >= 1.1e13:
    plt.text(x=195,y=1.3e13,s=str(round_sig(OFF[1],3)) + '% offset',fontsize=fSize,color=colours[1])
    plt.text(x=196.5,y=1.2e13, s="$E_0$=" + str(round_sig(E0,5)) +' eV', fontsize=fSize,color=colours[1])
else:
    plt.text(x=195,y=6.5e12,s=str(round_sig(OFF[1],3)) + '% offset',fontsize=fSize,color=colours[1])
    plt.text(x=196.5,y=6.0e12, s="$E_0$=" + str(round_sig(E0,5)) +' eV', fontsize=fSize,color=colours[1])


print('Peak Brilliance: ', np.max(B))

B = []
DELTA = []
Bfiles = [n_brilliance + str(m) + nameModifier[2] + ".dat" for m in M]
for i, f in enumerate(Bfiles):
    D = np.loadtxt(savePath + f, dtype=str, comments=None, skiprows=1)
    f = np.array(D[:, 1], dtype="float")
    e = np.array(D[:, 0], dtype="float")

    if i ==0:
        E0 = e[len(e)//2]
        # dE = E0 - EF
        # offset = (dE/EF)*100
        dB = Bf[2] - Bf[0]
        offset = (dB/Bf[0])*100
        OFF.append(offset)
        plt.plot(e, f, label="m = " + str(M[i]),color=colours[2], linestyle=styles[i])
    else:
        e = [_e - (M[i]-1)*E0 for _e in e]
        # print('hereh', e)
        plt.plot(e, f,label="m = " + str(M[i]),color=colours[2], linestyle=styles[i])
    delta = e - E0 * M[i]

    B.append(f)
    DELTA.append(delta)

plt.ylabel("Brilliance [ph/s/.1/mr$^2$/mm$^2$]")
plt.xlabel("Photon Energy [eV]")
# plt.legend()
if save:
    plt.savefig(savePath + "brilliance.png")
#plt.show()

# Finding brilliance difference with no detuning
x0 = E0 #DELTA[0][np.where(abs(DELTA[0]) == abs(DELTA[0]-E0).min())]
B0 = B[0][np.where(abs(DELTA[0]) == abs(DELTA[0]).min())]

# Finding difference at desired fundamental energy
Ed = EF-E0
xF = take_closest(e, EF)
# min(DELTA, key=lambda x:abs(x-Ed))
#take_closest(DELTA, E0-EF)
#DELTA[0][np.where(E0 - DELTA[0] == EF)]
BF = B[0][np.where(e == xF)]
Bdif_F = [b[np.where(B[0] == BF)] / BF for b in B[1::]]

# print('xf = ', xF)
# print('bf = ', BF)
# print('bdif_f = ', Bdif_F)

plt.axvline(x=xF, linestyle=":", color="gray")
# plt.text(
#     x=xF + 0.5,
#     y=0.5e9,
#     s="E=" + str(round_sig(float(xF), 5)),
#     fontsize=6,
#     color='gray',
# )


# for i, bf in enumerate(Bdif_F):
#     print('\n')
#     print(bf)
#     plt.text(
#         x=x0 + 5,
#         y=(B0/10) * (i+8),
#         s="$B(m= $" + str(M[i + 1]) + ") = " + str(round_sig(float(bf))) + "$B(m=1)$",
#         fontsize=6,
#         color=colours[2],
#     )
if np.max(B) >= 1.1e13:
    plt.text(x=195,y=1.1e13,s=str(round_sig(OFF[2],3)) + '% offset',fontsize=fSize,color=colours[2])
    plt.text(x=196.5,y=1.0e13, s="$E_0$=" + str(round_sig(E0,5)) +' eV', fontsize=fSize,color=colours[2])
else:
    plt.text(x=195,y=5.5e12,s=str(round_sig(OFF[2],3)) + '% offset',fontsize=fSize,color=colours[2])
    plt.text(x=196.5,y=5.0e12, s="$E_0$=" + str(round_sig(E0,5)) +' eV', fontsize=fSize,color=colours[2])
    

plt.show()

print('Peak Brilliance: ', np.max(B))

# print("Optimised undulator offset for brilliance [%]: ", ((float(E0 + xp) - E0)/E0)*100 )
# print("Optimised undulator offset for harmonic suppression [%]: ", ((float(E0 + xbest) - E0)/E0)*100 )
print("Optimised undulator offset from fundamental for brilliance [%]: ", OFF[1] )#((float(EF + xp) - EF)/EF)*100 )
