#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 16 17:07:48 2021

@author: jerome
"""

import tifffile
import numpy as np
import matplotlib.pyplot as plt
import jerome.dev.scripts.interferenceGratingModelsJK as interferenceGratingModelsJK
import jerome.dev.scripts.interferenceGratingModels as interferenceGratingModels


colours = plt.rcParams["axes.prop_cycle"].by_key()["color"]


def round_sig(x, sig=2):
    from math import log10, floor

    if x != 0:
        return round(x, sig - int(floor(log10(abs(x)))) - 1)
    else:
        return x


dirPath = "/home/jerome/dev/data/aerialImages/"
savePath = "/home/jerome/Documents/MASTERS/Figures/plots/roughness/"
order = range(0, 25)
cY = [2, 2, 2, 2, 2, 4, 4, 4, 4, 4, 6, 6, 6, 6, 6, 8, 8, 8, 8, 8, 10, 10, 10, 10, 10]
sigma = [
    0.5,
    1.0,
    1.5,
    2.0,
    2.5,
    0.5,
    1.0,
    1.5,
    2.0,
    2.5,
    0.5,
    1.0,
    1.5,
    2.0,
    2.5,
    0.5,
    1.0,
    1.5,
    2.0,
    2.5,
    0.5,
    1.0,
    1.5,
    2.0,
    2.5,
]
files = ["roughness/correctedWBS/" + str(o) + "intensity.tif" for o in order]
# ['roughness/' + str(o) + 'intensity.tif' for o in order]
# ['40x40-40-blockESWintensity.tif', '100pApertureIdealintensity_close.tif','ideal27intensity.tif', '100pBlockIdealintensity.tif']
# ['fullRes_4000eintensity.tif','4000eintensity_verticalFLIP.tif']
# ['ideal27intensity.tif','roughness/20intensity.tif','roughness/21intensity.tif','roughness/22intensity.tif','roughness/23intensity.tif','roughness/24intensity.tif']
# ['100umSlitintensity.tif','200umSlitintensity.tif','300umSlitintensity.tif']
# ['100pApertureIdealintensity_close.tif','ideal27intensity.tif', '100pBlockIdealintensity.tif']
# ['roughness/' + str(o) + 'intensity.tif' for o in order]
# ['ideal27intensity.tif','roughness/5intensity.tif','roughness/6intensity.tif','roughness/7intensity.tif','roughness/8intensity.tif','roughness/9intensity.tif']
# ['ideal27intensity.tif','roughness/20intensity.tif','roughness/21intensity.tif','roughness/22intensity.tif','roughness/23intensity.tif','roughness/24intensity.tif']#, 'roughness/24intensity.tif']
# ['roughness/2intensity.tif','roughness/3intensity.tif','roughness/4intensity.tif']#, 'roughness/24intensity.tif']
# ['100pApertureintensity_close.tif','24pApertureintensity_close.tif','14pApertureintensity_close.tif']
labels = [
    "\u03C3 = 0.5 nm ",
    "\u03C3 = 1.0 nm ",
    "\u03C3 = 1.5 nm ",
    "\u03C3 = 2.0 nm",
    "\u03C3 = 2.5 nm",
    "\u03C3 = 0.5 nm ",
    "\u03C3 = 1.0 nm ",
    "\u03C3 = 1.5 nm ",
    "\u03C3 = 2.0 nm",
    "\u03C3 = 2.5 nm",
    "\u03C3 = 0.5 nm ",
    "\u03C3 = 1.0 nm ",
    "\u03C3 = 1.5 nm ",
    "\u03C3 = 2.0 nm",
    "\u03C3 = 2.5 nm",
    "\u03C3 = 0.5 nm ",
    "\u03C3 = 1.0 nm ",
    "\u03C3 = 1.5 nm ",
    "\u03C3 = 2.0 nm",
    "\u03C3 = 2.5 nm",
    "\u03C3 = 0.5 nm ",
    "\u03C3 = 1.0 nm ",
    "\u03C3 = 1.5 nm ",
    "\u03C3 = 2.0 nm",
    "\u03C3 = 2.5 nm",
]
# ['Simulated - Ideal Mask']
# ['100 \u03bcm SSA','200 \u03bcm SSA','300 \u03bcm SSA']
# ['\u03C3 = 0.5 nm ','\u03C3 = 1.0 nm ','\u03C3 = 1.5 nm ','\u03C3 = 2.0 nm','\u03C3 = 2.5 nm']
# ['hor','ver']
# ['\u03C3 = 0 nm ','\u03C3 = 0.5 nm ','\u03C3 = 1.0 nm ','\u03C3 = 1.5 nm ','\u03C3 = 2.0 nm','\u03C3 = 2.5 nm']
#            '\u03C3 = 0.5 nm ','\u03C3 = 1.0 nm ','\u03C3 = 1.5 nm ','\u03C3 = 2.0 nm','\u03C3 = 2.5 nm',
#            '\u03C3 = 0.5 nm ','\u03C3 = 1.0 nm ','\u03C3 = 1.5 nm ','\u03C3 = 2.0 nm','\u03C3 = 2.5 nm',
#            '\u03C3 = 0.5 nm ','\u03C3 = 1.0 nm ','\u03C3 = 1.5 nm ','\u03C3 = 2.0 nm','\u03C3 = 2.5 nm',
#            '\u03C3 = 0.5 nm ','\u03C3 = 1.0 nm ','\u03C3 = 1.5 nm ','\u03C3 = 2.0 nm','\u03C3 = 2.5 nm']
# ['100','200','300']
cohLength = [460, 240, 190]
# [460,240,190]
# ['Single Aperture', 'Two-Grating Mask Model', 'Photon Block Mask Layer']
# ['Aperture', 'Aerial Image', 'Block']
# ['\u03C3 = 0.5 nm ','\u03C3 = 1.0 nm ','\u03C3 = 1.5 nm ','\u03C3 = 2.0 nm','\u03C3 = 2.5 nm',
#           '\u03C3 = 0.5 nm ','\u03C3 = 1.0 nm ','\u03C3 = 1.5 nm ','\u03C3 = 2.0 nm','\u03C3 = 2.5 nm',
#           '\u03C3 = 0.5 nm ','\u03C3 = 1.0 nm ','\u03C3 = 1.5 nm ','\u03C3 = 2.0 nm','\u03C3 = 2.5 nm',
#           '\u03C3 = 0.5 nm ','\u03C3 = 1.0 nm ','\u03C3 = 1.5 nm ','\u03C3 = 2.0 nm','\u03C3 = 2.5 nm',
#           '\u03C3 = 0.5 nm ','\u03C3 = 1.0 nm ','\u03C3 = 1.5 nm ','\u03C3 = 2.0 nm','\u03C3 = 2.5 nm']
# ['\u03C3 = 0 nm ','\u03C3 = 0.5 nm ','\u03C3 = 1.0 nm ','\u03C3 = 1.5 nm ','\u03C3 = 2.0 nm','\u03C3 = 2.5 nm']

# ['\u03C3 = 1.5 nm ','\u03C3 = 2.0 nm','\u03C3 = 2.5 nm']#, '\u03C3 = 2.5 nm /$c_y =$ 10 nm']
legendTitle = None  #'$c_y =$ 10 nm'
# ['aperture diffraction - $p_G = 100 nm$','aperture diffraction - $p_G = 24 nm$','aperture diffraction - $p_G = 14 nm$']

# Specify analysis
show = False  # show initial tiffs and entire profiles
plotTogether = False  # plot aerial image profiles together
contrast = True  # compute contrast metrics
normalise = False  # normalise profiles when plotting together
subtractAperture = False  # subtract intensity from aperture
plotFromEq = False  # plot ideal intensity from equation
split = True  # split into groups by correlation length (for ploting all aerial images together)
twoD = True  # calculate two-dimensional contrast (still in development)
findCorrelation = True
printContrast = False
save = False  # save plots to savePath

N = 1000  # number of pixels to take for line profile  - 1000 for roughness aerial images
n = 35  # number of pixels to average over for line profile - 15 for roughness aerial images
plotRange = 1000  # range of aerial image plot in nm

# res and middle pixels of images
res = [
    (2.5182637683019347e-09, 1.113721350329607e-07),
    (2.5182637683019347e-09, 1.113721350329607e-07),
    (2.5182637683019347e-09, 1.113721350329607e-07),
    (2.5182637683019347e-09, 1.113721350329607e-07),
    (2.5182637683019347e-09, 1.113721350329607e-07),
    (2.5182637683019347e-09, 1.113721350329607e-07),
    (2.5182637683019347e-09, 1.113721350329607e-07),
    (2.5182637683019347e-09, 1.113721350329607e-07),
    (2.5182637683019347e-09, 1.113721350329607e-07),
    (2.5182637683019347e-09, 1.113721350329607e-07),
    (2.5182637683019347e-09, 1.113721350329607e-07),
    (2.5182637683019347e-09, 1.113721350329607e-07),
    (2.5182637683019347e-09, 1.113721350329607e-07),
    (2.5182637683019347e-09, 1.113721350329607e-07),
    (2.5182637683019347e-09, 1.113721350329607e-07),
    (2.5182637683019347e-09, 1.113721350329607e-07),
    (2.5182637683019347e-09, 1.113721350329607e-07),
    (2.5182637683019347e-09, 1.113721350329607e-07),
    (2.5182637683019347e-09, 1.113721350329607e-07),
    (2.5182637683019347e-09, 1.113721350329607e-07),
    (2.5182637683019347e-09, 1.113721350329607e-07),
    (2.5182637683019347e-09, 1.113721350329607e-07),
    (2.5182637683019347e-09, 1.113721350329607e-07),
    (2.5182637683019347e-09, 1.113721350329607e-07),
    (2.5182637683019347e-09, 1.113721350329607e-07),
]

# [(2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07),
#         (2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07),
#         (2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07),
#         (2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07),
#         (2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07)]

# 40x40
# [(1.3129759798676162e-08, 5.9406957563530543e-08),
#          (2.501173811177358e-09, 2.661641589210943e-07),
#            (2.5011240434424064e-09, 2.658184246883298e-07),
#            (2.501124043067869e-09, 2.658184246878093e-07)]


# [(2.5011240434424064e-09, 2.658184246883298e-07),
#         (2.501124043067869e-09, 2.658184246878093e-07),
#         (2.501124043067869e-09, 2.658184246878093e-07),
#         (2.501124043067869e-09, 2.658184246878093e-07),
#         (2.501124043067869e-09, 2.658184246878093e-07),
#         (2.501124043067869e-09, 2.658184246878093e-07)]
# hor vs ver
# [(1.9651759267701173e-09, 2.658184225988639e-07),
#         (1.8194278317912603e-09,3.314297299424348e-07)]
# exit slit settings
# [(2.4549295628988656e-09,2.6639171024459003e-07),
#         (2.501122539655539e-09,2.6639171024459003e-07),
#         (2.5431737001664825e-09,2.6639171024459003e-07)]


# [(2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07),
#         (2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07),
#         (2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07),
#         (2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07),
#         (2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07),(2.501124043067869e-09, 2.658184246878093e-07)]

# [(2.5011240434424064e-09, 2.658184246883298e-07),
#        (2.501124043067869e-09, 2.658184246878093e-07),
#        (2.501124043067869e-09, 2.658184246878093e-07),
#        (2.501124043067869e-09, 2.658184246878093e-07),
#        (2.501124043067869e-09, 2.658184246878093e-07),
#        (2.501124043067869e-09, 2.658184246878093e-07)]
# for block diffraction
# [(2.501173811177358e-09, 2.661641589210943e-07),
#        (2.5011240434424064e-09, 2.658184246883298e-07),
#        (2.501124043067869e-09, 2.658184246878093e-07),]
# for roughness results
# [(2.5011240434424064e-09, 2.658184246883298e-07),
# (2.501124043067869e-09, 2.658184246878093e-07),
# (2.501124043067869e-09, 2.658184246878093e-07),
# (2.501124043067869e-09, 2.658184246878093e-07),
# (2.501124043067869e-09, 2.658184246878093e-07),
# (2.501124043067869e-09, 2.658184246878093e-07)]

mid = [
    (196, 12257),
    (196, 12257),
    (196, 12257),
    (196, 12257),
    (196, 12257),
    (196, 12257),
    (196, 12257),
    (196, 12257),
    (196, 12257),
    (196, 12257),
    (196, 12257),
    (196, 12257),
    (196, 12257),
    (196, 12257),
    (196, 12257),
    (196, 12257),
    (196, 12257),
    (196, 12257),
    (196, 12257),
    (196, 12257),
    (196, 12257),
    (196, 12257),
    (196, 12257),
    (196, 12257),
    (196, 12257),
]
# 40x40
# [(1000,9430),
#    (65, 12867),  #- mid for 100pAperture
#            (65, 12899),
#            (65, 12899)]

# [(65,16377), # mask orientation
#         (108,13477)]
# [(64, 12920), # exit slits
#       (64, 12899),
#       (64, 12881)]
# [(65, 12867),  #- mid for 100pAperture
#         (65, 12899),
#         (65, 12899)]
# [(64, 12899),(64, 12899),(64, 12899),(64, 12899),(64, 12899),
#         (64, 12899),(64, 12899),(64, 12899),(64, 12899),(64, 12899),
#         (64, 12899),(64, 12899),(64, 12899),(64, 12899),(64, 12899),
#         (64, 12899),(64, 12899),(64, 12899),(64, 12899),(64, 12899),
#         (64, 12899),(64, 12899),(64, 12899),(64, 12899),(64, 12899)]

# for roughness results
# [(65, 12899),
# (65, 12899),
# (65, 12899),
# (65, 12899),
# (65, 12899),
# (65, 12899)]

pitch = 100e-9


tiffs = [tifffile.imread(dirPath + f) for f in files]
images = [t[m[0] - n : m[0] + n, m[1] - N : m[1] + N] for t, m in zip(tiffs, mid)]
if n != 0:
    profiles = [
        i.mean(0) for i in images
    ]  # [t[m[0]-n:m[0]+n,m[1]-N:m[1]+N] for t, m in zip(tiffs,mid)]
    images = [t[m[0] - n : m[0] + n, m[1] - N : m[1] + N] for t, m in zip(tiffs, mid)]
else:
    images = [t[m[0], m[1] - N : m[1] + N] for t, m in zip(tiffs, mid)]
    profiles = images
xP = [np.linspace(-N * r[0], N * r[0], 2 * N) for r in res]
yP = [np.linspace(-n * r[1], n * r[1], 2 * n) for r in res]

""" define interference grating parameters"""
wl = 6.710553853647976e-9  # wavelength in m

# Amplitude of both beams (assumed equal)
A = 1.35e5  # 0.148e5 #0.078e5  0.37e5 #0.3e5  # this may be scaled to  match simulated intensity
k = 2 * np.pi / wl
m = 1  # order of diffracted beams from each grating
d = 100e-9  # 24e-9 #100e-9 # grating spacing
# angle between the beams from each grating
theta = np.arcsin(m * wl / d)
IP = interferenceGratingModelsJK.interferenceIntensity(xP[0], k, theta, A=A)

print("Range of aerial image profile (h) [m]: ", np.max(xP[0]) - np.min(xP[0]))
if n != 0:
    print("Range of aerial image profile (v) [m]: ", np.max(yP[0]) - np.min(yP[0]))
else:
    pass
# print(len(tiffs))
# print(len(profiles))
# print(len(labels))

if show:
    if len(tiffs) == 1:
        print(np.max(tiffs[0]))
        plt.imshow(tiffs[0], aspect="auto")
        # plt.xticks([int((np.shape(tiffs[0])[1])*((a/6)-1)) for a in range(0,7)],[round_sig(np.max(xP[0])*x*1e6/3) for x in np.linspace(-3,3,7)]) #[-1, -2/3,-1/3,0,1/3,2/3,1]])
        # plt.yticks([int(np.shape(tiffs[0])[0]*(b/4)-1) for b in range(0,5)],[round_sig(np.max(yP[0])*y*1e6/2) for y in np.linspace(-2,2,5)])

        plt.yticks(
            [int(np.shape(tiffs[0])[0] * (b / 8)) for b in range(0, 9)],
            [
                round_sig(np.shape(tiffs[0])[0] * res[0][1] * (a / 8) * 1e6)
                for a in range(-4, 5)
            ],
            fontsize=15,
        )
        plt.xticks(
            [int(np.shape(tiffs[0])[1] * (b / 8)) for b in range(0, 9)],
            [
                round_sig(np.shape(tiffs[0])[1] * res[0][0] * (a / 8) * 1e6)
                for a in range(-4, 5)
            ],
            fontsize=15,
        )
        plt.colorbar()
        plt.show()

        plt.imshow(images[0], aspect="auto")
        plt.xticks(
            [int(2 * N * (a / 6) - 1) for a in range(0, 7)],
            [round_sig(np.max(xP[0]) * x * 1e6 / 3) for x in np.linspace(-3, 3, 7)],
        )  # [-1, -2/3,-1/3,0,1/3,2/3,1]])
        plt.yticks(
            [int(2 * n * (b / 4) - 1) for b in range(0, 5)],
            [round_sig(np.max(yP[0]) * y * 1e6 / 2) for y in np.linspace(-2, 2, 5)],
        )
        # plt.xlim(int(N/2 + plotRange/2),int(N/2 - plotRange/2))
        # plt.ylim(int(n/2 - 15),int(n/2 + 15))
        plt.show()

        plt.plot(profiles[0], label=labels[0])
        plt.legend()
        plt.ylabel("Intensity [ph/s/.1%bw/mm$^2$]")
        plt.xlabel("Position [nm]")
        plt.show
    else:
        fig, axs = plt.subplots(int(len(tiffs)), 1)
        for i in range(len(tiffs)):
            axs[i].imshow(tiffs[i], aspect=5)
            axs[i].set_title(labels[i])
        axs[int(len(tiffs) / 2)].set_ylabel("y-position [pixels]")
        axs[len(tiffs) - 1].set_xlabel("x-position [pixels]")
        fig.tight_layout()
        plt.show()

        fig, axs = plt.subplots(int(len(tiffs)), 1)
        for i in range(len(tiffs)):
            Imax = np.max(images)
            Imin = np.min(images)
            im = axs[i].imshow(
                images[i], aspect=2
            )  # ,vmin=Imin, vmax=Imax)# aspect=15) #cmap='gray',
            axs[i].imshow(images[i], aspect=2)  # , vmin=Imin, vmax=Imax)
            # axs[i].set_title(labels[i])
            axs[i].set_xticks([int(2 * N * (a / 6) - 1) for a in range(0, 7)])
            axs[i].set_yticks([int(2 * n * (b / 2) - 1) for b in range(0, 3)])
            axs[i].set_yticklabels(
                [round_sig(np.max(yP[i]) * y * 1e6) for y in [-1, 0, 1]]
            )
            if i < len(tiffs) - 1:
                axs[i].set_xticklabels([])
            else:
                axs[i].set_xticklabels(
                    [
                        round_sig(np.max(xP[i]) * x * 1e6)
                        for x in [-1, -2 / 3, -1 / 3, 0, 1 / 3, 2 / 3, 1]
                    ]
                )
            # if i == int(len(tiffs)/2):
            #     # cb = plt.colorbar(im,orientation = 'horizontal', fraction=0.8, anchor = (0.5, 0.0))
            #     # cb=fig.colorbar(im, ax=axs[i], aspect = 10, fraction = 0.5)# aspect=5, fraction=0.05)#009, pad=0.009, aspect=12)
            #     cb.set_label(label='Intensity [ph/s/.1%bw/mm$^2$]',labelpad=10)
            # else:
            #     pass
            # fig.colorbar(im, ax=axs[i], aspect=5, fraction=0.05)#, aspect=1.7, fraction=0.05)#, fraction=0.009, pad=0.009)
        axs[int(len(tiffs) / 2)].set_ylabel("y-position [\u03bcm]")
        # fig.colorbar(im,ax=axs[int(len(tiffs)/2)], label='Intensity [ph/s/.1%bw/mm$^2$]')
        axs[len(tiffs) - 1].set_xlabel("x-position [\u03bcm]")
        fig.tight_layout()
        if save:
            plt.savefig(savePath + "2daerialImageLabel.pdf")
            plt.savefig(savePath + "2daerialImageLabel.png", dpi=2000)
        else:
            pass
        plt.show()

        fig, axs = plt.subplots(int(len(tiffs)), 1)
        for i in range(len(tiffs)):
            axs[i].plot(xP[i] * 1e6, profiles[i], label=labels[i])
        axs[int(len(tiffs) / 2)].set_ylabel("Intensity [ph/s/.1%bw/mm$^2$]")
        axs[len(tiffs) - 1].set_xlabel("Position [\u03bcm]")
        fig.tight_layout()
        plt.show()
if subtractAperture:
    # profileSubtract = [a/np.max(a) - b/np.max(b) - c/np.max(c) for a,b,c in zip(profiles[2],profiles[1],profiles[0])]
    envelope = [
        a * profiles[0] / np.max(profiles[0]) + profiles[2] / np.max(profiles[2])
        for a in [1]
    ]  # ,1.5,2,2.5]]#,4,5,6,7]]
    envelope = [e / np.max(e) for e in envelope]
    profileSubtract = profiles[1] - profiles[0] - profiles[2]
    # plt.plot(xP[0]*1e9,profileSubtract)
    for i, e in enumerate(envelope):
        plt.plot(xP[0] * 1e9, e, label="combined envelope #" + str(i))
    plt.plot(xP[1] * 1e9, profiles[1] / np.max(profiles[1]), label="aerial image")
    plt.legend()
    plt.xlim(-int(plotRange / 2), int(plotRange / 2))
    plt.ylabel("Intensity [a.u]")
    plt.ylim(bottom=0)
    plt.xlabel("Position [nm]")
    leg1 = plt.legend(title=None, bbox_to_anchor=(0.89, -0.12), ncol=3)
    # loc='upper left')
    if save:
        plt.savefig(savePath + "combinedEnvelopeFar.pdf")
        plt.savefig(savePath + "combinedEnvelopeFar.png", dpi=2000)
    else:
        pass
    plt.show()
    for i, e in enumerate(envelope):
        plt.plot(xP[0] * 1e9, e, label="combined envelope #" + str(i))
    plt.plot(xP[1] * 1e9, profiles[1] / np.max(profiles[1]), label="aerial image")
    plt.legend()
    plt.xlim(-int(plotRange / 20), int(plotRange / 20))
    plt.ylabel("Intensity [a.u]")
    plt.ylim(bottom=0)
    plt.xlabel("Position [nm]")
    leg1 = plt.legend(title=None, bbox_to_anchor=(0.89, -0.12), ncol=3)
    # loc='upper left')
    if save:
        plt.savefig(savePath + "combinedEnvelopeClose.pdf")
        plt.savefig(savePath + "combinedEnvelopeClose.png", dpi=2000)
    else:
        pass
    plt.show()


if plotTogether:
    if normalise:
        for i, p in enumerate(profiles):
            print(" ")
            print(i)
            print(np.mean(p))
            if i == 0:
                plt.plot(xP[i] * 1e9, p / np.mean(p), label=labels[i])  #'--',
            elif i == 1:
                plt.plot(xP[i] * 1e9, p / np.mean(p), label=labels[i])
            elif i == 2:
                plt.plot(
                    xP[i] * 1e9, p / np.mean(p), label=labels[i], color=colours[i + 1]
                )
            else:
                pass
                # plt.plot(xP[i]*1e9,p/np.mean(p), '--', label=labels[i], color=colours[i])
        plt.ylabel("Intensity [a.u]")
        plt.xlim(-int(plotRange / 2), int(plotRange / 2))
        plt.ylim(bottom=0)
        plt.xlabel("Position [nm]")
        plt.legend(loc="upper left")
        # leg1 = plt.legend(title=None, bbox_to_anchor=(0.89,-0.12), ncol=3)
        # loc='upper left')
        if save:
            plt.savefig(savePath + "aerialImageSSAnormal.pdf")
            plt.savefig(savePath + "aerialImageSSAnormal.png", dpi=2000)
        else:
            pass
        plt.show()
    else:
        for i, p in enumerate(profiles):
            plt.plot(xP[i] * 1e9, p, label=labels[i])
        plt.ylabel("Intensity [ph/s/.1%bw/mm$^2$]")
        # plt.ylabel('Intensity [a.u]')
        plt.xlim(-int(plotRange / 2), int(plotRange / 2))
        plt.ylim(bottom=0)
        plt.xlabel("Position [nm]")
        leg1 = plt.legend(
            title=None, loc="upper left"
        )  # bbox_to_anchor=(0.89,-0.12), ncol=3)
        # loc='upper left')
        # if save:
        #     plt.savefig(savePath + 'aerialImageSSA.pdf')
        #     plt.savefig(savePath + 'aerialImageSSA.png', dpi=2000)
        # else:
        #     pass
        plt.show()
    if plotFromEq:
        if subtractAperture:
            profileSubtract = [
                profiles[1] / np.max(profiles[1]) - e for e in envelope
            ]  # - profiles[0]/np.max(profiles[0])  - profiles[2]/np.max(profiles[2])
            profileSubtract = [
                abs(1 - (abs(p) / np.max(abs(p)))) for p in profileSubtract
            ]
            EQplus = [
                IP / np.max(IP) + e for e in envelope
            ]  # + profiles[2]/np.max(profiles[2]) + profiles[0]/np.max(profiles[0])
            EQplus = [e / np.max(e) for e in EQplus]
            # EQplus = [1.2*e/np.max(e) - 0.3 for e in EQplus]
            for e, p in enumerate(profileSubtract):
                # plt.plot(xP[0]*1e9,p/np.max(p), label = 'aerial image - subtacted envelope # ' + str(e))
                plt.plot(
                    xP[0] * 1e9,
                    EQplus[e],
                    ":",
                    label="Eq.2.3.45 - added envelope #" + str(e),
                )
            plt.xlim(-int(plotRange / 2), int(plotRange / 2))
            plt.ylabel("Intensity [a.u]")
            plt.ylim(bottom=0)
            plt.xlabel("Position [nm]")
            plt.legend()
            if save:
                plt.savefig(savePath + "firstAerialImageProfile.pdf")
                plt.savefig(savePath + "firstAerialImageProfile.png", dpi=2000)
            plt.show()
            for e, p in enumerate(profileSubtract):
                # plt.plot(xP[0]*1e9,p/np.max(p), label = 'aerial image - subtacted envelope # ' + str(e))
                plt.plot(
                    xP[0] * 1e9,
                    EQplus[e],
                    ":",
                    label="Eq.2.3.45 - added envelope #" + str(e),
                )
            plt.plot(
                xP[1] * 1e9, profiles[1] / np.max(profiles[1]), label="aerial image"
            )
            plt.xlim(-int(plotRange / 20), int(plotRange / 20))
            plt.ylabel("Intensity [a.u]")
            plt.ylim(bottom=0)
            plt.xlabel("Position [nm]")
            plt.legend()
            if save:
                plt.savefig(savePath + "EQwEnvelopeClose.pdf")
                plt.savefig(savePath + "EQwEnvelopeClose.png", dpi=2000)
            plt.show()
            # plt.plot(xP[0]*1e9,profileSubtract/np.max(profileSubtract), label = 'aerial image - subtacted envelope')
            # plt.plot(xP[0]*1e9,1.2*(EQplus/np.max(EQplus))-0.3, ':', label = 'Eq.2.3.45 - added envelope')
        else:
            for i, p in enumerate(profiles):
                plt.plot(xP[i] * 1e9, p, label=labels[i])
            plt.plot(xP[0] * 1e9, IP, ":", label="Eq.2.3.45")
            plt.ylabel("Intensity [ph/s/.1%bw/mm$^2$]")
            plt.xlim(-int(plotRange / 2), int(plotRange / 2))
            plt.ylim(bottom=0)
            plt.xlabel("Position [nm]")
            plt.legend()
            # leg1 = plt.legend(title=None, bbox_to_anchor=(0.89,-0.12), ncol=7)
            if save:
                plt.savefig(savePath + "firstAerialImageProfile.pdf")
                plt.savefig(savePath + "firstAerialImageProfile.png", dpi=2000)
        plt.show
    else:
        pass
    # plt.xlim(-int(plotRange/2), int(plotRange/2))
    # plt.ylim(bottom=0)
    # plt.xlabel('Position [nm]')
    # leg1 = plt.legend(title=None, bbox_to_anchor=(0.89,-0.12), ncol=2)
    #            #loc='upper left')
    # # if save:
    # #     plt.savefig(savePath + 'aerialImageApNdEQ.pdf')
    # #     plt.savefig(savePath + 'aerialImageApNdEQ.png', dpi=2000)
    # # else:
    # #     pass
    # plt.show()
else:
    pass

if subtractAperture:
    # fourierC.insert(1,fourierC1[0])
    profiles.insert(0, IP)
    labels.insert(0, "analytical")
    xP.insert(0, xP[0])
    # for p in enumerate(profiles):
    #     plt.plot(p)
    # # plt.xlim(-plotRange/20,plotRange/20)
    # plt.show()
else:
    pass

if contrast:
    michelsonC = [
        interferenceGratingModelsJK.gratingContrastMichelson(p) for p in profiles
    ]
    rmsC = [interferenceGratingModelsJK.gratingContrastRMS(p) for p in profiles]
    compositeC = [
        interferenceGratingModelsJK.meanDynamicRange(p) for p in profiles
    ]  # , mdrC, imbalanceC
    nilsC = [
        interferenceGratingModelsJK.NILS(p, x, pitch / 4, show=False)
        for p, x in zip(profiles, xP)
    ]
    fourierC = [
        interferenceGratingModelsJK.gratingContrastFourier(p, x * 1e6, show=False)
        for p, x in zip(profiles, xP)
    ]  # Cf,  Am, Fr, peakFr - Still unsure but seems good
    fidel = [
        interferenceGratingModelsJK.fidelity(p, IP) for p in profiles
    ]  # fidelity based on comparison to model

    if split:
        fig, axs = plt.subplots(2, 3)
        axs[0, 0].plot(sigma[0:5], michelsonC[0:5], "x:")
        axs[0, 0].plot(sigma[5:10], michelsonC[5:10], "x:")
        axs[0, 0].plot(sigma[10:15], michelsonC[10:15], "x:")
        axs[0, 0].plot(sigma[15:20], michelsonC[15:20], "x:")
        axs[0, 0].plot(sigma[20:25], michelsonC[20:25], "x:")
        axs[0, 0].set_title("Michelson")
        axs[0, 0].set_ylabel("Contrast")
        # axs[0,0].legend(loc='lower left')
        axs[0, 1].plot(sigma[0:5], rmsC[0:5], "x:")
        axs[0, 1].plot(sigma[5:10], rmsC[5:10], "x:")
        axs[0, 1].plot(sigma[10:15], rmsC[10:15], "x:")
        axs[0, 1].plot(sigma[15:20], rmsC[15:20], "x:")
        axs[0, 1].plot(sigma[20:25], rmsC[20:25], "x:")
        axs[0, 1].set_title("RMS")
        axs[0, 2].plot(sigma[0:5], [c[0] for c in compositeC[0:5]], "x:")
        axs[0, 2].plot(sigma[5:10], [c[0] for c in compositeC[5:10]], "x:")
        axs[0, 2].plot(sigma[10:15], [c[0] for c in compositeC[10:15]], "x:")
        axs[0, 2].plot(sigma[15:20], [c[0] for c in compositeC[15:20]], "x:")
        axs[0, 2].plot(sigma[20:25], [c[0] for c in compositeC[20:25]], "x:")
        axs[0, 2].set_title("Composite")
        axs[1, 0].plot(sigma[0:5], [n[0] for n in fourierC[0:5]], "x:")
        axs[1, 0].plot(sigma[5:10], [n[0] for n in fourierC[5:10]], "x:")
        axs[1, 0].plot(sigma[10:15], [n[0] for n in fourierC[10:15]], "x:")
        axs[1, 0].plot(sigma[15:20], [n[0] for n in fourierC[15:20]], "x:")
        axs[1, 0].plot(sigma[20:25], [n[0] for n in fourierC[20:25]], "x:")
        axs[1, 0].set_title("Fourier")
        axs[1, 0].set_ylabel("Contrast")
        axs[1, 1].set_title("NILS")
        axs[1, 1].plot(sigma[0:5], fidel[0:5], "x:")
        axs[1, 1].plot(sigma[5:10], fidel[5:10], "x:")
        axs[1, 1].plot(sigma[10:15], fidel[10:15], "x:")
        axs[1, 1].plot(sigma[15:20], fidel[15:20], "x:")
        axs[1, 1].plot(sigma[20:25], fidel[20:25], "x:")
        axs[1, 1].set_title("Fidelity")
        axs[1, 2].plot(sigma[0:5], [n[0] for n in nilsC[0:5]], "x:")
        axs[1, 2].plot(sigma[5:10], [n[0] for n in nilsC[5:10]], "x:")
        axs[1, 2].plot(sigma[10:15], [n[0] for n in nilsC[10:15]], "x:")
        axs[1, 2].plot(sigma[15:20], [n[0] for n in nilsC[15:20]], "x:")
        axs[1, 2].plot(sigma[20:25], [n[0] for n in nilsC[20:25]], "x:")
        axs[1, 2].set_title("NILS")
        axs[1, 2].set_ylabel("NILS")
        # for ax in fig.axes:
        # ax.set_xticklabels(labels, rotation=45, ha='right')
        axs[1, 0].set_xlabel("\u03C3 [nm]")
        axs[1, 1].set_xlabel("\u03C3 [nm]")
        axs[1, 2].set_xlabel("\u03C3 [nm]")
        fig.tight_layout()
        # fig.subplots_adjust(bottom=0.5,hspace=5.33)   ##  Need to play with this number.
        axs[1, 1].legend(
            labels=["$c_y$ = " + str(c) for c in [2, 4, 6, 8, 10]],
            bbox_to_anchor=(2.3, -0.35),
            ncol=5,
        )  # loc="lower center"
        if save:
            plt.savefig(savePath + "contrastAll.pdf")
            plt.savefig(savePath + "contrastAll.png", dpi=2000)
        plt.show()

    else:
        fig, axs = plt.subplots(2, 3)
        axs[0, 0].plot(labels, michelsonC, "x:")
        axs[0, 0].set_title("Michelson")
        axs[0, 0].set_ylabel("Contrast")
        axs[0, 1].plot(labels, rmsC, "x:")
        axs[0, 1].set_title("RMS")
        axs[0, 2].plot(labels, [c[0] for c in compositeC], "x:")
        axs[0, 2].set_title("Composite")
        axs[1, 0].plot(labels, [n[0] for n in fourierC], "x:")
        axs[1, 0].set_title("Fourier")
        axs[1, 0].set_ylabel("Contrast")
        axs[1, 1].plot(labels, fidel, "x:")
        axs[1, 1].set_title("Fidelity")
        axs[1, 2].plot(labels, [n[0] for n in nilsC], "x:")
        axs[1, 2].set_title("NILS")
        axs[1, 2].set_ylabel("NILS")
        # for ax in fig.axes:
        #     ax.set_xticklabels(labels, rotation=45, ha='right')
        axs[1, 0].set_xlabel("SSA Width [\u03bcm]")
        axs[1, 1].set_xlabel("SSA Width [\u03bcm]")
        axs[1, 2].set_xlabel("SSA Width [\u03bcm]")
        fig.tight_layout()
        if save:
            plt.savefig(savePath + "contrastAllCy4.pdf")
            plt.savefig(savePath + "contrastAllCy4.png", dpi=2000)
        plt.show()

    if twoD:
        nils2d = []
        nils2dRMS = []
        lwRMS = []
        dlwRMS = []
        fourierC2d = []
        nils3s = []
        nilsrmsD = []
        print("getting line profiles down every pixel")
        for e, i in enumerate(images):
            iP = [i[:, a] for a in range(0, np.shape(i)[1])]
            print("shape:", np.shape(iP))
            plt.plot(xP[e] * 1e9, [p for p in iP])
            plt.xlim(-plotRange, plotRange)
            plt.title(labels[e])
            plt.show()

            LWRe = interferenceGratingModelsJK.LWR(iP, xP[e][1] - xP[e][0], dim=0)
            print("LWR: ", LWRe)

            print("e: ", e)
            NILS2D = np.array(
                [
                    interferenceGratingModelsJK.NILS(ip, xP[e], pitch / 4, show=False)
                    for ip in np.transpose(np.array(iP))
                ]
            )

            # FOURIERC2D  = [interferenceGratingModelsJK.gratingContrastFourier(ip,x*1e6, show=False) for ip, x in zip(iP,xP)]
            # FOURIERC2D  = [interferenceGratingModelsJK.gratingContrastFourier(ip,xP[e]*1e6, show=False) for ip in iP]
            # FOURIERC2D = [[0,1] for ip, x in zip(iP,xP)]
            # fC = np.mean([f[0] for f in FOURIERC2D])

            NNILS = [len(a) for a in NILS2D[:, 2]]
            print(NILS2D[:, 9][0 : np.min(NNILS) - 1])
            NILS = [a[0 : np.min(NNILS) - 1] for a in NILS2D[:, 2]]
            NILS3s = NILS2D[:, 9][
                0 : np.min(NNILS) - 1
            ]  # [a[0:np.min(NNILS)-1] for a in NILS2D[:,9]]
            NILSrmsd = NILS2D[:, 8][
                0 : np.min(NNILS) - 1
            ]  # [a[0:np.min(NNILS)-1] for a in NILS2D[:][8]]
            # LW     = [a[0:np.min(NNILS)-1] for a in NILS2D[:,3]]

            # NILS = np.stack(NILS2D[:,2])

            rmsNILS = np.sqrt(np.mean(np.square(NILS)))
            # rmsdNILS =

            # THis is the 2D NILS distribution
            plt.imshow(NILS)
            plt.title("NILS - 2D dist")
            plt.colorbar()
            plt.show()

            plt.plot(np.mean(NILS, axis=0))
            plt.title("NILS - 1D dist")
            plt.show()

            avNILS = np.mean(NILS)

            nils3s.append(np.mean(NILS3s))
            nilsrmsD.append(np.mean(NILSrmsd))
            # fourierC2d.append(fC)
            nils2d.append(avNILS)
            nils2dRMS.append(rmsNILS)

        import pickle

        with open("/home/jerome/dev/data/2dNILS3s.pkl", "wb") as p:
            pickle.dump(nils3s, p)
        with open("/home/jerome/dev/data/2dNILSrmsD.pkl", "wb") as p:
            pickle.dump(nilsrmsD, p)

        michelsonC2d = [
            interferenceGratingModels.gratingContrastMichelson(i) for i in images
        ]
        rmsC2d = [interferenceGratingModels.gratingContrastRMS(i) for i in images]
        compositeC2d = [
            interferenceGratingModels.meanDynamicRange(i) for i in images
        ]  # , mdrC, imbalanceC
        # nilsC2d = [interferenceGratingModels.NILS(i,x, pitch/4, show=False) for i, x in zip(images, xP)]
        # fourierC2d = [interferenceGratingModels.gratingContrastFourier(i,x*1e6, show=False) for i, x in zip(images,xP)] #Cf,  Am, Fr, peakFr - Still unsure but seems good
        fidel2d = [
            interferenceGratingModelsJK.fidelity(i, images[0]) for i in images[1::]
        ]  # fidelity based on comparison to model

        if split:
            LWRvalues = [
                1.8419804271566513e-10,
                1.8984990357804102e-10,
                1.813176530303753e-10,
                1.8663260790977058e-10,
                2.0904595794650548e-10,
                1.9061517390960172e-10,
                1.8895225580783887e-10,
                1.8803786502134085e-10,
                2.076845881674641e-10,
                2.2640992438387305e-10,
                1.9496931756395736e-10,
                2.0588276534061496e-10,
                2.1629204035016212e-10,
                2.465487999058053e-10,
                2.506473012365266e-10,
                1.8853697086955247e-10,
                1.9381144428450904e-10,
                2.1748924560363814e-10,
                3.2483624815113297e-10,
                1.032537180062842e-06,
                1.741373473874035e-10,
                2.0772111245895005e-10,
                2.4385662215828644e-10,
                6.342611383160777e-06,
                3.4955274262789615e-10,
            ]
            fig, axs = plt.subplots(2, 3)
            axs[0, 0].plot(sigma[0:5], [1 - f for f in fidel[0:5]], "x:")
            axs[0, 0].plot(sigma[5:10], [1 - f for f in fidel[5:10]], "x:")
            axs[0, 0].plot(sigma[10:15], [1 - f for f in fidel[10:15]], "x:")
            axs[0, 0].plot(sigma[15:20], [1 - f for f in fidel[15:20]], "x:")
            axs[0, 0].plot(sigma[20:25], [1 - f for f in fidel[20:25]], "x:")
            axs[0, 0].set_ylabel("$1-Fidelity$")
            axs[0, 1].plot(sigma[0:5], michelsonC2d[0:5], "x:")
            axs[0, 1].plot(sigma[5:10], michelsonC2d[5:10], "x:")
            axs[0, 1].plot(sigma[10:15], michelsonC2d[10:15], "x:")
            axs[0, 1].plot(sigma[20:25], michelsonC2d[20:25], "x:")
            axs[0, 1].plot(sigma[15:20], michelsonC2d[15:20], "x:")
            axs[0, 1].set_ylabel("$C_M$")
            axs[0, 2].plot(sigma[0:5], rmsC2d[0:5], "x:")
            axs[0, 2].plot(sigma[5:10], rmsC2d[5:10], "x:")
            axs[0, 2].plot(sigma[10:15], rmsC2d[10:15], "x:")
            axs[0, 2].plot(sigma[15:20], rmsC2d[15:20], "x:")
            axs[0, 2].plot(sigma[20:25], rmsC2d[20:25], "x:")
            axs[0, 2].set_ylabel("$C_{RMS}$")
            axs[1, 0].plot(sigma[0:5], [c[0] for c in compositeC2d[0:5]], "x:")
            axs[1, 0].plot(sigma[5:10], [c[0] for c in compositeC2d[5:10]], "x:")
            axs[1, 0].plot(sigma[10:15], [c[0] for c in compositeC2d[10:15]], "x:")
            axs[1, 0].plot(sigma[15:20], [c[0] for c in compositeC2d[15:20]], "x:")
            axs[1, 0].plot(sigma[20:25], [c[0] for c in compositeC2d[20:25]], "x:")
            axs[1, 0].set_ylabel("$C_{composite}$")
            axs[1, 1].plot(sigma[0:5], nils2d[0:5], "x:")
            axs[1, 1].plot(sigma[5:10], nils2d[5:10], "x:")
            axs[1, 1].plot(sigma[10:15], nils2d[10:15], "x:")
            axs[1, 1].plot(sigma[15:20], nils2d[15:20], "x:")
            axs[1, 1].plot(sigma[20:25], nils2d[20:25], "x:")
            # axs[0,1].set_title("NILS")
            axs[1, 1].set_ylabel("$NILS_{mean}$")
            axs[1, 2].plot(sigma[0:5], nils3s[0:5], "x:")
            axs[1, 2].plot(sigma[5:10], nils3s[5:10], "x:")
            axs[1, 2].plot(sigma[10:15], nils3s[10:15], "x:")
            axs[1, 2].plot(sigma[15:20], nils3s[15:20], "x:")
            axs[1, 2].plot(sigma[20:25], nils3s[20:25], "x:")
            # axs[0,2].set_title("NILS - RMS")
            axs[1, 2].set_ylabel("$NILS_{3\u03C3}$")
            # axs[2,1].plot(sigma[0:5], LWRvalues[0:5], 'x:')
            # axs[2,1].plot(sigma[5:10], LWRvalues[5:10], 'x:')
            # axs[2,1].plot(sigma[10:15], LWRvalues[10:15], 'x:')
            # axs[2,1].plot(sigma[15:19], LWRvalues[15:19], 'x:')
            # axs[2,1].plot([sigma[20], sigma[21], sigma[22], sigma[24]], [LWRvalues[20], LWRvalues[21], LWRvalues[22], LWRvalues[24]], 'x:')
            # # axs[0,2].set_title("NILS - RMS")
            # axs[2,1].set_ylabel("$LWR$")
            # axs[2,0].axis('off')
            # axs[2,2].axis('off')
            # axs[0,0].legend(loc='lower left')
            # axs[1,2].plot(sigma[0:5], fourierC2d[0:5], 'x:')
            # axs[1,2].plot(sigma[5:10], fourierC2d[5:10], 'x:')
            # axs[1,2].plot(sigma[10:15], fourierC2d[10:15], 'x:')
            # axs[1,2].plot(sigma[15:20], fourierC2d[15:20], 'x:')
            # axs[1,2].plot(sigma[20:25], fourierC2d[20:25], 'x:')
            # axs[1,2].set_ylabel("$C_{Fourier}$")

            # axs[0,2].plot(sigma[0:5], [c[0] for c in compositeC2d[0:5]], 'x:')
            # axs[0,2].plot(sigma[5:10], [c[0] for c in compositeC2d[5:10]], 'x:')
            # axs[0,2].plot(sigma[10:15], [c[0] for c in compositeC2d[10:15]], 'x:')
            # axs[0,2].plot(sigma[15:20], [c[0] for c in compositeC2d[15:20]], 'x:')
            # axs[0,2].plot(sigma[20:25], [c[0] for c in compositeC2d[20:25]], 'x:')
            # axs[0,2].set_title("Composite")
            # axs[1,0].plot(sigma[0:5], fourierC2d[0:5], 'x:')
            # axs[1,0].plot(sigma[5:10], fourierC2d[5:10], 'x:')
            # axs[1,0].plot(sigma[10:15], fourierC2d[10:15], 'x:')
            # axs[1,0].plot(sigma[15:20], fourierC2d[15:20], 'x:')
            # axs[1,0].set_title("Fourier")
            # axs[1,0].set_ylabel("Contrast")
            # # axs[1,1].set_title("NILS")
            # axs[1,1].plot(sigma[0:5], fidel[0:5], 'x:')
            # axs[1,1].plot(sigma[5:10], fidel[5:10], 'x:')
            # axs[1,1].plot(sigma[10:15], fidel[10:15], 'x:')
            # axs[1,1].plot(sigma[15:20], fidel[15:20], 'x:')
            # axs[1,1].plot(sigma[20:25], fidel[20:25], 'x:')
            # axs[1,1].set_title("Fidelity")
            # axs[1,2].plot(sigma[0:5], nils2d[0:5], 'x:')
            # axs[1,2].plot(sigma[5:10], nils2d[5:10], 'x:')
            # axs[1,2].plot(sigma[10:15], nils2d[10:15], 'x:')
            # axs[1,2].plot(sigma[15:20],nils2d[15:20], 'x:')
            # axs[1,2].plot(sigma[20:25],nils2d[20:25], 'x:')
            # axs[1,2].set_title("NILS")
            # axs[1,2].set_ylabel("NILS")
            # axs[2,0].plot(sigma[0:5], nils2dRMS[0:5], 'x:')
            # axs[2,0].plot(sigma[5:10], nils2dRMS[5:10], 'x:')
            # axs[2,0].plot(sigma[10:15], nils2dRMS[10:15], 'x:')
            # axs[2,0].plot(sigma[15:20], nils2dRMS[15:20], 'x:')
            # axs[2,0].plot(sigma[20:25], nils2dRMS[20:25], 'x:')
            # axs[2,0].set_title("NILS - RMS")
            # axs[2,0].set_ylabel("RMS")
            # axs[2,1].set_title("Line Width - RMS")
            # axs[2,1].plot(sigma[0:5], lwRMS[0:5], 'x:')
            # axs[2,1].plot(sigma[5:10], lwRMS[5:10], 'x:')
            # axs[2,1].plot(sigma[10:15], lwRMS[10:15], 'x:')
            # axs[2,1].plot(sigma[15:20], lwRMS[15:20], 'x:')
            # axs[2,1].plot(sigma[20:25], lwRMS[20:25], 'x:')
            # axs[2,2].plot(sigma[0:5], dlwRMS[0:5], 'x:')
            # axs[2,2].plot(sigma[5:10], dlwRMS[5:10], 'x:')
            # axs[2,2].plot(sigma[10:15], dlwRMS[10:15], 'x:')
            # axs[2,2].plot(sigma[15:20],dlwRMS[15:20], 'x:')
            # axs[2,2].plot(sigma[20:25],dlwRMS[20:25], 'x:')
            # axs[2,2].set_title("dLW - RMS")
            # axs[2,1].set_ylabel("Line Width")
            # for ax in fig.axes:
            # ax.set_xticklabels(labels, rotation=45, ha='right')
            axs[1, 0].set_xlabel("\u03C3 [nm]")
            axs[1, 2].set_xlabel("\u03C3 [nm]")
            axs[1, 1].set_xlabel("\u03C3 [nm]")
            fig.tight_layout()
            # fig.subplots_adjust(bottom=0.5,hspace=5.33)   ##  Need to play with this number.
            # axs[1,1].legend(labels=['$c_y$ = ' + str(c) for c in [2,4,6,8,10]], bbox_to_anchor=(1.75,-0.35), ncol=5) #loc="lower center"
            # if save:
            # plt.savefig(savePath + 'contrastAll.pdf')
            # plt.savefig(savePath + 'contrastAll.png', dpi=2000)
            plt.show()

        else:
            fig, axs = plt.subplots(3, 3)
            axs[0, 0].plot(labels, michelsonC2d, "x:")
            axs[0, 0].set_title("Michelson")
            axs[0, 0].set_ylabel("Contrast")
            axs[0, 1].plot(labels, rmsC2d, "x:")
            axs[0, 1].set_title("RMS")
            axs[0, 2].plot(labels, [c[0] for c in compositeC2d], "x:")
            axs[0, 2].set_title("Composite")
            axs[1, 0].plot(labels, fourierC2d, "x:")
            axs[1, 0].set_title("Fourier")
            axs[1, 0].set_ylabel("Contrast")
            axs[1, 1].plot(labels[1::], [(1 - f) for f in fidel2d], "x:")
            axs[1, 1].set_title("Fidelity")
            axs[1, 2].plot(labels, nils2d, "x:")
            axs[1, 2].set_title("NILS")
            axs[1, 2].set_ylabel("NILS")
            axs[2, 0].plot(labels, nils2dRMS, "x:")
            axs[2, 0].set_title("NILS - RMS")
            axs[2, 0].set_ylabel("RMS")
            axs[2, 1].plot(labels, lwRMS, "x:")
            axs[2, 1].set_title("Line Width - RMS")
            axs[2, 2].plot(labels, dlwRMS, "x:")
            axs[2, 2].set_title("dLW - RMS")
            axs[2, 2].set_ylabel("Line Width")

            # for ax in fig.axes:
            #     ax.set_xticklabels(labels, rotation=45, ha='right')
            # axs[1,0].set_xlabel('Slit Width')
            # axs[1,1].set_xlabel('Slit Width')
            # axs[1,2].set_xlabel('Slit Width')
            # fig.tight_layout()
            # if save:
            #     plt.savefig(savePath + 'contrastAllCy10.pdf')
            #     plt.savefig(savePath + 'contrastAllCy10.png', dpi=2000)
            plt.show()
    else:
        pass


if findCorrelation:
    import pandas as pd

    if twoD:
        dataStructure = [
            sigma,
            cY,
            michelsonC2d,
            rmsC2d,
            [c[0] for c in compositeC2d],
            nils2d,
            lwRMS,
            dlwRMS,
        ]
        dF = pd.DataFrame(
            np.array(dataStructure).T,
            columns=[
                "\u03C3",
                "$c_y$",
                "$C_M$",
                "$C_{RMS}$",
                "$C_{Composite}$",
                "NILS",
                "Line Width",
                "LWR",
            ],
        )
    else:
        dataStructure = [
            sigma,
            cY,
            michelsonC,
            rmsC,
            [c[0] for c in compositeC],
            [f[0] for f in fourierC],
            [n[0] for n in nilsC],
            fidel,
        ]

        # print(len(labels))
        # print("Shape of data structure: ", np.shape(dataStructure))
        # dF = pd.DataFrame(np.concatenate([labels,avPeaks,sumPeaks,rmsPeaks,
        #                              michelsonC,rmsC,[c[0] for c in compositeC],
        #                              [f[0] for f in fourierC],[n[0] for n in nilsC]]),
        dF = pd.DataFrame(
            np.array(dataStructure).T,
            columns=[
                "\u03C3",
                "$c_y$",
                "$C_M$",
                "$C_{RMS}$",
                "$C_{Composite}$",
                "$C_{Fourier}$",
                "NILS",
                "Fidelity",
            ],
        )
    correlations = dF.corr()
    import seaborn as sns

    plt.rcParams["figure.figsize"] = (8, 6)
    sns.heatmap(
        correlations, cmap="vlag", vmin=-1, vmax=1, annot=True
    )  # ,labelsize=10)#,fontSize=2)
    if save:
        plt.savefig(savePath + "correlationsAveraged.pdf")
        plt.savefig(savePath + "correlationsAveraged.png", dpi=2000)
    plt.show()

if printContrast:
    for i in range(0, len(labels)):
        print(" ")
        print("profile #{} ----------------------------------------".format(i + 1))
        print(labels[i])
        print("Michelson Contrast:              {}".format(michelsonC[i]))
        print("RMS Contrast:                    {}".format(rmsC[i]))
        print("Fourier Contrast:                {}".format(fourierC[i][0]))
        print("Composite Contrast:              {}".format(compositeC[i][0]))
        print("Imbalance Contrast:              {}".format(compositeC[i][2]))
        print("MDR Contrast:                    {}".format(compositeC[i][1]))
        print("NILS:                            {}".format(nilsC[i][0]))
        print("Fidelity:                        {}".format(fidel[i]))
        print("RMS x COMPOSITE                  {}".format(rmsC[i] * compositeC[i][0]))
