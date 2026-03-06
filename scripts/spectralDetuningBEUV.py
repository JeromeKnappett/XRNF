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


def sourceCoherence(wl,size,div):
    term1 = (2 * np.pi * div) / (wl)
    term2 = 1 / (2 * size)
    print(term1)
    print(term2)
    print(term1**2 - term2**2)
    print((term1**2 - term2**2)**(0.5))
    coh_len = abs( term1**2 - term2**2 )**(-0.5)
    k = (2*np.pi) / wl
    
    # checking emittance
    e = size*div
    if e >= 1/(2*k):
        print('\n emittance satisfies inequality! :)')
        print('e = ', e)
        print('1/2k = ', 1/(2*k))
    elif e <= 1/(2*k):
        print('\n emittance doesnt satisfy inequality! :(')
        print('e = ', e)
        print('1/2k = ', 1/(2*k))
    
    term4 = 4 * (k**2) * (size**2) * (div**2) 
    coh_len2 = (2 * size) / (np.sqrt(abs(term4 - 1)))

    print('here')
#    print(term4)
#    print(np.sqrt(abs(term4 - 1)))
#    print(coh_len2)
    print(coh_len - coh_len2)
    
    deg_coh = coh_len / size
    term3 = deg_coh**2 + 4
    print(term3)
    deg_coh_n = deg_coh / (np.sqrt(term3))
    
    return coh_len, deg_coh, deg_coh_n

colours = plt.rcParams["axes.prop_cycle"].by_key()["color"]

#dirPath = "/home/jerome/dev/data/spectralDetuning/"
#savePath = dirPath
#M = [1, 3, 5, 7, 9, 11]
#
#save = False
#
#E0 = 187.38631882706142  # 184.76
#dE = 10

dirPath = '/home/jerome/Documents/PhD/Data/'
#"/home/jerome/dev/data/spectralDetuning/"
M = [1, 3, 5]

save = False

E0 = 185.0
dE = 10

savePath = dirPath + str(int(E0)) + '/'
# save = True
# savePath = '/home/jerome/Documents/MASTERS/Figures/plots/'

n_flux = 'res_flux_' + str(int(E0)) + '_'
n_brilliance = 'res_brilliance_' + str(int(E0)) + '_'
n_divx = 'res_divx_' + str(int(E0)) + '_'
n_divy = 'res_divy_' + str(int(E0)) + '_'
n_sizex = 'res_sizex_' + str(int(E0)) + '_'
n_sizey = 'res_sizey_' + str(int(E0)) + '_'

# Div X plots
Dxfiles = [n_divx + str(m) + ".dat" for m in M]
for i, f in enumerate(Dxfiles):
    D = np.loadtxt(savePath + f, dtype=str, comments=None, skiprows=1)
    e = np.array(D[:, 0], dtype="float")
    f = np.array(D[:, 1], dtype="float")
    delta = e - E0 * M[i]
    plt.plot(delta, f, label="m = " + str(M[i]))
    
    divX = f[len(f)//2]

plt.ylabel("Horizontal Divergence [rad]")
plt.xlabel("Photon Energy [eV]")
plt.legend()
if save:
    plt.savefig(savePath + "xDiv.png")
plt.show()

# Div Y plots
Dyfiles = [n_divy + str(m) + ".dat" for m in M]
for i, f in enumerate(Dyfiles):
    D = np.loadtxt(savePath + f, dtype=str, comments=None, skiprows=1)
    e = np.array(D[:, 0], dtype="float")
    f = np.array(D[:, 1], dtype="float")
    delta = e - E0 * M[i]
    plt.plot(delta, f, label="m = " + str(M[i]))

    divY = f[len(f)//2]
    
plt.ylabel("Vertical Divergence [rad]")
plt.xlabel("Photon Energy [eV]")
plt.legend()
if save:
    plt.savefig(savePath + "yDiv.png")
plt.show()


# Beam Size X plots
Sxfiles = [n_sizex + str(m) + ".dat" for m in M]
for i, f in enumerate(Sxfiles):
    D = np.loadtxt(savePath + f, dtype=str, comments=None, skiprows=1)
    e = np.array(D[:, 0], dtype="float")
    f = np.array(D[:, 1], dtype="float")
    delta = e - E0 * M[i]
    plt.plot(delta, f, label="m = " + str(M[i]))
    
    sizeX = f[len(f)//2]

plt.ylabel("Horizontal Beam Size [m]")
plt.xlabel("Photon Energy [eV]")
plt.legend()
if save:
    plt.savefig(savePath + "xSize.png")
plt.show()

# Beam Size Y plots
Syfiles = [n_sizey + str(m) + ".dat" for m in M]
for i, f in enumerate(Syfiles):
    D = np.loadtxt(savePath + f, dtype=str, comments=None, skiprows=1)
    e = np.array(D[:, 0], dtype="float")
    f = np.array(D[:, 1], dtype="float")
    delta = e - E0 * M[i]
    plt.plot(delta, f, label="m = " + str(M[i]))
    
    sizeY = f[len(f)//2]

plt.ylabel("Vertical Beam Size [m]")
plt.xlabel("Photon Energy [eV]")
plt.legend()
if save:
    plt.savefig(savePath + "ySize.png")
plt.show()


# dif = [b-B[0] for b in B[1::]]
# print(np.shape(dif))
# meanDif = np.mean(dif,axis=0)
# bestEnergy = DELTA[0][np.where(meanDif == meanDif.max())]
# for i,d in enumerate(dif):
#     plt.plot(DELTA[0],d,label='m = ' + str(2*i+3))
#     index = np.where(d == d.max())
#     print(DELTA[0][index])
# plt.plot(DELTA[0],meanDif, label='mean')
# plt.axvline(x=bestEnergy, linestyle=':',color='black')
# plt.text(x=1,y=0.2e13,s='E = ' + str(bestEnergy) + ' eV')
# plt.legend()
# plt.show()


B = []
DELTA = []

# Flux plots
Ffiles = [n_flux + str(m) + ".dat" for m in M]
for i, f in enumerate(Ffiles):
    D = np.loadtxt(savePath + f, dtype=str, comments=None, skiprows=1)
    e = np.array(D[:, 0], dtype="float")
    f = np.array(D[:, 1], dtype="float")
    delta = e - E0 * M[i]
    plt.plot(delta, f, label="m = " + str(M[i]))
    
    B.append(f)
    DELTA.append(delta)

plt.ylabel("Flux [ph/s/.1\%bw]")
plt.xlabel("Photon Energy [eV]")
plt.legend()
if save:
    plt.savefig(savePath + "flux.png")
#plt.show()


# Finding brilliance difference with no detuning
x0 = DELTA[0][np.where(abs(DELTA[0]) == abs(DELTA[0]).min())]
B0 = B[0][np.where(abs(DELTA[0]) == abs(DELTA[0]).min())]
Bdif_0 = [b[np.where(abs(DELTA[0]) == abs(DELTA[0]).min())] / B0 for b in B[1::]]

plt.axvline(x=x0, linestyle=":", color="black")
plt.text(x=x0 + 0.5, y=0.0, s="E=" + str(E0), fontsize=6)
for i, bd in enumerate(Bdif_0):
    plt.text(
        x=x0 + 5,
        y=(B0/10) * (i+12),
        s="$B_0 (m= $"
        + str(M[i + 1])
        + ") = "
        + str(round_sig(float(bd)))
        + "$B_0 (m=1)$",
        fontsize=6,
    )


# Finding brilliance difference at m=1 peak
xp = DELTA[0][np.where(B[0] == B[0].max())]
Bp = B[0][np.where(B[0] == B[0].max())]
Bdif_p = [b[np.where(B[0] == B[0].max())] / Bp for b in B[1::]]



plt.axvline(x=xp, linestyle=":", color="gray")
plt.text(
    x=xp + 0.5,
    y=0.25e9,
    s="E=" + str(round_sig(float(E0 + xp), 5)),
    fontsize=6,
    color="gray",
)
for i, bd in enumerate(Bdif_p):
    plt.text(
        x=x0 + 5,
        y=(B0/10) * (i+10),
        s="$B_p (m= $"
        + str(M[i + 1])
        + ") = "
        + str(round_sig(float(bd)))
        + "$B_p (m=1)$",
        fontsize=6,
        color="gray",
    )

# Finding optimal difference with B(m=1) >= B0(m=1)
Bdif = [b / B[0] for b in B[1::]]
Bdifmean = np.mean(Bdif, axis=0)
Bdif_acceptable = Bdifmean[np.where(B[0] >= B0)]
xbest = DELTA[0][
    np.where(Bdifmean == Bdif_acceptable.min())
]  # DELTA[0][np.where(B[0] >= B0)]
Bbest = B[0][np.where(DELTA[0] == xbest)]
Bdif_best = [b[np.where(B[0] == Bbest)] / Bbest for b in B[1::]]

plt.axvline(x=xbest, linestyle=":", color="blue")
plt.text(
    x=xbest + 0.5,
    y=0.5e9,
    s="E=" + str(round_sig(float(E0 + xbest), 5)),
    fontsize=6,
    color="blue",
)
for i, bd in enumerate(Bdif_best):
    plt.text(
        x=x0 + 5,
        y=(B0/10) * (i+8),
        s="$B(m= $" + str(M[i + 1]) + ") = " + str(round_sig(float(bd))) + "$B(m=1)$",
        fontsize=6,
        color="blue",
    )

plt.text(x = x0 + 10, y = (B0 / 10) * (2 + 8), s = str(round_sig(((float(E0 + xbest) - E0)/E0)*100)) + '% offset',fontsize=6,color='blue')
plt.text(x = x0 + 10, y = (B0 / 10) * (2 + 12), s = str(round_sig(((float(E0 + xp) - E0)/E0)*100)) + '% offset',fontsize=6,color='gray')

# bestEnergy = DELTA[0][np.where(Bdifmean == Bdifmean.min())]
# plt.axvline(x=bestEnergy, linestyle=':',color='black')
# plt.text(x=1,y=0.2e13,s='E = ' + str(bestEnergy) + ' eV')
plt.show()

print("Optimised undulator offset for flux [%]: ", ((float(E0 + xp) - E0)/E0)*100 )
print("Optimised undulator offset for harmonic suppression [%]: ", ((float(E0 + xbest) - E0)/E0)*100 )

##Finding flux difference with no detuning
#_x0 = _DELTA[0][np.where(abs(_DELTA[0])==abs(_DELTA[0]).min())]
#F0 = F[0][np.where(abs(_DELTA[0])==abs(_DELTA[0]).min())]
#Fdif_0 = [b[np.where(abs(_DELTA[0])==abs(_DELTA[0]).min())] / F0 for b in F[1::]]
#
#plt.axvline(x=_x0, linestyle=':',color='black')
#plt.text(x=_x0-2.5, y=0.0, s='E=' + str(E0),fontsize=6)
#for i,bd in enumerate(Fdif_0):
#    plt.text(x=_x0-10,y=(F0/10)*(i+9),s='$F_0 (m= $' + str(M[i+1]) + ') = ' + str(round_sig(bd)) + '$F_0 (m=1)$',fontsize=6)
#
##Finding flux difference at m=1 peak
#xp = _DELTA[0][np.where(F[0] == F[0].max())]
#Fp = F[0][np.where(F[0] == F[0].max())]
#Fdif_p = [b[np.where(F[0] == F[0].max())] / Fp for b in F[1::]]
#
#plt.axvline(x=xp, linestyle=':',color='gray')
#plt.text(x=xp-2.5, y=0.0, s='E=' + str(round_sig(E0 + xp,5)),fontsize=6,color='gray')
#for i,bd in enumerate(Fdif_p):
#    plt.text(x=_x0-10,y=(F0/10)*(i+4),s='$F_p (m= $' + str(M[i+1]) + ') = ' + str(round_sig(bd)) + '$F_p (m=1)$',fontsize=6,color='gray')
#
##Finding optimal difference with F(m=1) >= F0(m=1)
#Fdif = [b / F[0] for b in F[1::]]
#Fdifmean = np.mean(Fdif,axis=0)
#Fdif_acceptable = Fdifmean[np.where(F[0] >= F0)]
#xbest = _DELTA[0][np.where(Fdifmean == Fdif_acceptable.min())] #_DELTA[0][np.where(F[0] >= F0)]
#Fbest = F[0][np.where(_DELTA[0] == xbest)]
#Fdif_best = [b[np.where(F[0] == Fbest)] / Fbest for b in F[1::]]
#
#plt.axvline(x=xbest, linestyle=':',color='blue')
#plt.text(x=_x0+xbest+0.1, y=0.5e9, s='E=' + str(round_sig(E0 + xbest,5)),fontsize=6,color='blue')
#for i,bd in enumerate(Fdif_best):
#    plt.text(x=xp+1,y=(F0/10)*(i+8),s='$F(m= $' + str(M[i+1]) + ') = ' + str(round_sig(bd)) + '$F(m=1)$',fontsize=6,color='blue')
#
## bestEnergy = DELTA[0][np.where(Bdifmean == Bdifmean.min())]
## plt.axvline(x=bestEnergy, linestyle=':',color='black')
## plt.text(x=1,y=0.2e13,s='E = ' + str(bestEnergy) + ' eV')
#plt.show()

#print("Optimised undulator offset [%]: ", ((float(E0 + xp) - E0)/E0)*100 )

B = []
DELTA = []

# Brilliance plots
Bfiles = [n_brilliance + str(m) + ".dat" for m in M]
for i, f in enumerate(Bfiles):
    D = np.loadtxt(savePath + f, dtype=str, comments=None, skiprows=1)
    e = np.array(D[:, 0], dtype="float")
    f = np.array(D[:, 1], dtype="float")
    delta = e - E0 * M[i]

    B.append(f)
    DELTA.append(delta)

    plt.plot(delta, f, label="m = " + str(M[i]))

plt.ylabel("Brilliance [ph/s/.1/mr$^2$/mm$^2$]")
plt.xlabel("Photon Energy [eV]")
plt.legend()
if save:
    plt.savefig(savePath + "brilliance.png")
#plt.show()

# Finding brilliance difference with no detuning
x0 = DELTA[0][np.where(abs(DELTA[0]) == abs(DELTA[0]).min())]
B0 = B[0][np.where(abs(DELTA[0]) == abs(DELTA[0]).min())]
Bdif_0 = [b[np.where(abs(DELTA[0]) == abs(DELTA[0]).min())] / B0 for b in B[1::]]

plt.axvline(x=x0, linestyle=":", color="black")
plt.text(x=x0 + 0.5, y=0.0, s="E=" + str(E0), fontsize=6)
for i, bd in enumerate(Bdif_0):
    plt.text(
        x=x0 - 10,
        y=(B0 / 6) * (i + 16),
        s="$B_0 (m= $"
        + str(M[i + 1])
        + ") = "
        + str(round_sig(float(bd)))
        + "$B_0 (m=1)$",
        fontsize=6,
    )

# Finding brilliance difference at m=1 peak
xp = DELTA[0][np.where(B[0] == B[0].max())]
Bp = B[0][np.where(B[0] == B[0].max())]
Bdif_p = [b[np.where(B[0] == B[0].max())] / Bp for b in B[1::]]



plt.axvline(x=xp, linestyle=":", color="gray")
plt.text(
    x=xp + 0.5,
    y=0.25e13,
    s="E=" + str(round_sig(float(E0 + xp), 5)),
    fontsize=6,
    color="gray",
)
for i, bd in enumerate(Bdif_p):
    plt.text(
        x=x0 - 10,
        y=(B0 / 6) * (i + 14),
        s="$B_p (m= $"
        + str(M[i + 1])
        + ") = "
        + str(round_sig(float(bd)))
        + "$B_p (m=1)$",
        fontsize=6,
        color="gray",
    )

# Finding optimal difference with B(m=1) >= B0(m=1)
Bdif = [b / B[0] for b in B[1::]]
Bdifmean = np.mean(Bdif, axis=0)
Bdif_acceptable = Bdifmean[np.where(B[0] >= B0)]
xbest = DELTA[0][
    np.where(Bdifmean == Bdif_acceptable.min())
]  # DELTA[0][np.where(B[0] >= B0)]
Bbest = B[0][np.where(DELTA[0] == xbest)]
Bdif_best = [b[np.where(B[0] == Bbest)] / Bbest for b in B[1::]]

plt.axvline(x=xbest, linestyle=":", color="blue")
plt.text(
    x=xbest + 0.5,
    y=0.5e13,
    s="E=" + str(round_sig(float(E0 + xbest), 5)),
    fontsize=6,
    color="blue",
)
for i, bd in enumerate(Bdif_best):
    plt.text(
        x=x0 - 10,
        y=(B0 / 6) * (i + 12),
        s="$B(m= $" + str(M[i + 1]) + ") = " + str(round_sig(float(bd))) + "$B(m=1)$",
        fontsize=6,
        color="blue",
    )

plt.text(x = x0 - 5, y = (B0 / 6) * (2 + 12), s = str(round_sig(((float(E0 + xbest) - E0)/E0)*100)) + '% offset',fontsize=6,color='blue')
plt.text(x = x0 - 5, y = (B0 / 6) * (2 + 16), s = str(round_sig(((float(E0 + xp) - E0)/E0)*100)) + '% offset',fontsize=6,color='gray')

# bestEnergy = DELTA[0][np.where(Bdifmean == Bdifmean.min())]
# plt.axvline(x=bestEnergy, linestyle=':',color='black')
# plt.text(x=1,y=0.2e13,s='E = ' + str(bestEnergy) + ' eV')
plt.show()

print("Optimised undulator offset for brilliance [%]: ", ((float(E0 + xp) - E0)/E0)*100 )
print("Optimised undulator offset for harmonic suppression [%]: ", ((float(E0 + xbest) - E0)/E0)*100 )

print(sizeX)
print(sizeY)
print(divX)
print(divY)

coh_lenX, dcX, dcnX = sourceCoherence(6.7e-9,sizeX,divX)
print('x-coherence length =              ', coh_lenX)
print('x-coherence degree =              ', dcX)
print('x-coherence degree (normalised) = ', dcnX)

coh_lenY, dcY, dcnY = sourceCoherence(6.7e-9,sizeY,divY)
print('y-coherence length =              ', coh_lenY)
print('y-coherence degree =              ', dcY)
print('y-coherence degree (normalised) = ', dcnY)


betaX

 
