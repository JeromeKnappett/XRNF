#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 16:28:32 2025

@author: -
"""

import numpy as np
import matplotlib.pyplot as plt
import tifffile
from math import floor, log10\

def round_sig(x, sig=2):
    if x != 0:
        return round(x, sig-int(floor(log10(abs(x))))-1)
    else:
        return x
    
def combine_intensity_phase(intensity, phase):
    """
    Given intensity and phase arrays (same shape),
    returns a complex electric field array E = sqrt(I) * exp(i * phase).

    Parameters
    ----------
    intensity : np.ndarray
        2D (or nD) array representing intensity.
    phase : np.ndarray
        2D (or nD) array representing phase (radians).

    Returns
    -------
    np.ndarray
        Complex electric field array of the same shape.
    """
    return np.sqrt(intensity) * np.exp(1j * phase)


def Complex2HSV(z, rmin, rmax, hue_start=90):
    from matplotlib.colors import hsv_to_rgb
    # get amplidude of z and limit to [rmin, rmax]
    amp = np.abs(z)
    amp = np.where(amp < rmin, rmin, amp)
    amp = np.where(amp > rmax, rmax, amp)
    ph = np.angle(z, deg=1) + hue_start
    # HSV are values in range [0,1]
    h = (ph % 360) / 360
    s = 0.85 * np.ones_like(h)
    v = (amp -rmin) / (rmax - rmin)
    return hsv_to_rgb(np.dstack((h,s,v)))


path = '/user/home/opt/xl/xl/experiments/XFM_teleptycho/data/testPhaseSpace/atPinhole/'

NX,NY = 8000,3000
_NX,_NY = 100,100


I = tifffile.imread(path + '/' + 'intensity.tif')
P = tifffile.imread(path + '/' + 'phase.tif')


# (ny, nx) = np.shape(I)
xi = -0.00012869358965143972 #Initial Horizontal Position [m]
xf = 0.00012613493977386305 #Final Horizontal Position [m]
nx = 25480 #Number of points vs Horizontal Position
yi = -0.00015574296140587597 #Initial Vertical Position [m]
yf = 0.00015320177767720242 #Final Vertical Position [m]
ny = 12150 #Number of points vs Vertical Position

dx = (xf-xi)/nx
dy = (yf-yi)/ny

I = I[(ny//2)-(NY//2):(ny//2)+(NY//2),(nx//2)-(NX//2):(nx//2)+(NX//2)]
P = P[(ny//2)-(NY//2):(ny//2)+(NY//2),(nx//2)-(NX//2):(nx//2)+(NX//2)]

numXticks = 5
numYticks = 5
sF = 1e6
fSize = 6

C = combine_intensity_phase(I, P)

C = Complex2HSV(C,np.min(abs(C)),np.max(abs(C)))
        
print(np.shape(C))


# plt.figure()
plt.imshow(C)
plt.yticks([int((NY-1.0)*(b/(numYticks-1.0))) for b in range(0,numYticks)],
            [round_sig(NY*dy*(a/(numYticks-1.0))*sF) for a in range(-int((numYticks-1.0)/2.0),int((numYticks/2.0 + 1.0)))])#,fontsize=fSize )
plt.xticks([int((NX-1.0)*(b/(numXticks-1.0))) for b in range(0,numXticks)],
            [round_sig(NX*dx*(a/(numXticks-1.0))*sF) for a in  range(-int((numXticks-1.0)/2.0),int((numXticks/2.0 + 1.0)))])#,fontsize=fSize)
plt.xlabel('x [$\mu$m]')
plt.ylabel('y [$\mu$m]')
plt.title('Complex Wavefield')
# plt.colorbar()
plt.show()
# plt.figure()
plt.imshow(I)
plt.yticks([int((NY-1.0)*(b/(numYticks-1.0))) for b in range(0,numYticks)],
            [round_sig(NY*dy*(a/(numYticks-1.0))*sF) for a in range(-int((numYticks-1.0)/2.0),int((numYticks/2.0 + 1.0)))])#,fontsize=fSize )
plt.xticks([int((NX-1.0)*(b/(numXticks-1.0))) for b in range(0,numXticks)],
            [round_sig(NX*dx*(a/(numXticks-1.0))*sF) for a in  range(-int((numXticks-1.0)/2.0),int((numXticks/2.0 + 1.0)))])#,fontsize=fSize)
plt.xlabel('x [$\mu$m]')
plt.ylabel('y [$\mu$m]')
plt.title('Wavefield Intensity')
plt.colorbar()
plt.show()
# plt.figure()
plt.imshow(P)
plt.yticks([int((NY-1.0)*(b/(numYticks-1.0))) for b in range(0,numYticks)],
            [round_sig(NY*dy*(a/(numYticks-1.0))*sF) for a in range(-int((numYticks-1.0)/2.0),int((numYticks/2.0 + 1.0)))])#,fontsize=fSize )
plt.xticks([int((NX-1.0)*(b/(numXticks-1.0))) for b in range(0,numXticks)],
            [round_sig(NX*dx*(a/(numXticks-1.0))*sF) for a in  range(-int((numXticks-1.0)/2.0),int((numXticks/2.0 + 1.0)))])#,fontsize=fSize)
plt.xlabel('x [$\mu$m]')
plt.ylabel('y [$\mu$m]')
plt.title('Wavefield Phase')
plt.colorbar()
plt.show()

midX,midY = np.shape(I)[1]//2,np.shape(I)[0]//2

# fig, ax = plt.subplots(2,2)
# ax[0,0].imshow(C[midY-_NY:midY+_NY,midX-_NX-3000:midX+_NX-3000])
# ax[0,0].set_title('-1 order (left)')
# ax[0,1].imshow(C[midY-_NY:midY+_NY,midX-_NX:midX+_NX])
# ax[0,1].set_title('centre')
# ax[1,0].imshow(C[midY-_NY:midY+_NY,midX-_NX+3000:midX+_NX+3000])
# ax[1,0].set_title('+1 order (right)')
# ax[1,1].imshow(C[midY-_NY:midY+_NY,midX-_NX+1000:midX+_NX+1000])
# ax[1,1].set_title('+1 order and zero order (right)')
# for a in [ax[0,0],ax[0,1],ax[1,0],ax[1,1]]:
#     a.set_xticks([int(((2*_NX)-1.0)*(b/(numXticks-1.0))) for b in range(0,numXticks)])
#     a.set_xticklabels([round_sig((2*_NX)*dx*(a/(numXticks-1.0))*sF) for a in  range(-int((numXticks-1.0)/2.0),int((numXticks/2.0 + 1.0)))])#,fontsize=fSize)
#     a.set_yticks([int(((2*_NY)-1.0)*(b/(numYticks-1.0))) for b in range(0,numYticks)])
#     a.set_yticklabels([round_sig((2*_NY)*dy*(a/(numYticks-1.0))*sF) for a in range(-int((numYticks-1.0)/2.0),int((numYticks/2.0 + 1.0)))])#,fontsize=fSize )
# for a in [ax[1,0],ax[1,1]]:
#     a.set_xlabel('x [microns]')
# for a in [ax[0,0],ax[1,0]]:
#     a.set_ylabel('y [microns]')
# plt.tight_layout()
# plt.show()

# fig, ax = plt.subplots(2,2)
# ax[0,0].imshow(I[midY-_NY:midY+_NY,midX-_NX-3000:midX+_NX-3000])
# ax[0,0].set_title('-1 order (left)')
# ax[0,1].imshow(I[midY-_NY:midY+_NY,midX-_NX:midX+_NX])
# ax[0,1].set_title('centre')
# ax[1,0].imshow(I[midY-_NY:midY+_NY,midX-_NX+3000:midX+_NX+3000])
# ax[1,0].set_title('+1 order (right)')
# ax[1,1].imshow(I[midY-_NY:midY+_NY,midX-_NX-1000:midX+_NX-1000])
# ax[1,1].set_title('+1 order and zero order (left)')
# for a in [ax[0,0],ax[0,1],ax[1,0],ax[1,1]]:
#     a.set_xticks([int(((2*_NX)-1.0)*(b/(numXticks-1.0))) for b in range(0,numXticks)])
#     a.set_xticklabels([round_sig((2*_NX)*dx*(a/(numXticks-1.0))*sF) for a in  range(-int((numXticks-1.0)/2.0),int((numXticks/2.0 + 1.0)))])#,fontsize=fSize)
#     a.set_yticks([int(((2*_NY)-1.0)*(b/(numYticks-1.0))) for b in range(0,numYticks)])
#     a.set_yticklabels([round_sig((2*_NY)*dy*(a/(numYticks-1.0))*sF) for a in range(-int((numYticks-1.0)/2.0),int((numYticks/2.0 + 1.0)))])#,fontsize=fSize )
# for a in [ax[1,0],ax[1,1]]:
#     a.set_xlabel('x [microns]')
# for a in [ax[0,0],ax[1,0]]:
#     a.set_ylabel('y [microns]')
# plt.tight_layout()
# plt.show()

# fig, ax = plt.subplots(2,2)
# ax[0,0].imshow(P[midY-_NY:midY+_NY,midX-_NX-3000:midX+_NX-3000])
# ax[0,0].set_title('-1 order (left)')
# ax[0,1].imshow(P[midY-_NY:midY+_NY,midX-_NX:midX+_NX])
# ax[0,1].set_title('centre')
# ax[1,0].imshow(P[midY-_NY:midY+_NY,midX-_NX+3000:midX+_NX+3000])
# ax[1,0].set_title('+1 order (right)')
# ax[1,1].imshow(P[midY-_NY:midY+_NY,midX-_NX-1000:midX+_NX-1000])
# ax[1,1].set_title('-1 order and zero order (left)')
# for a in [ax[0,0],ax[0,1],ax[1,0],ax[1,1]]:
#     a.set_xticks([int(((2*_NX)-1.0)*(b/(numXticks-1.0))) for b in range(0,numXticks)])
#     a.set_xticklabels([round_sig((2*_NX)*dx*(a/(numXticks-1.0))*sF) for a in  range(-int((numXticks-1.0)/2.0),int((numXticks/2.0 + 1.0)))])#,fontsize=fSize)
#     a.set_yticks([int(((2*_NY)-1.0)*(b/(numYticks-1.0))) for b in range(0,numYticks)])
#     a.set_yticklabels([round_sig((2*_NY)*dy*(a/(numYticks-1.0))*sF) for a in range(-int((numYticks-1.0)/2.0),int((numYticks/2.0 + 1.0)))])#,fontsize=fSize )
# for a in [ax[1,0],ax[1,1]]:
#     a.set_xlabel('x [microns]')
# for a in [ax[0,0],ax[1,0]]:
#     a.set_ylabel('y [microns]')
# plt.tight_layout()
# plt.show()

fig,ax = plt.subplots(1,5)
ax[0].imshow(C[midY-_NY:midY+_NY,midX-_NX-3000:midX+_NX-3000])
ax[0].set_title('-1')
ax[1].imshow(C[midY-_NY:midY+_NY,midX-_NX-1000:midX+_NX-1000])
ax[1].set_title('-1 / 0')
ax[2].imshow(C[midY-_NY:midY+_NY,midX-_NX+24:midX+_NX+24])
ax[2].set_title('0')
ax[3].imshow(C[midY-_NY:midY+_NY,midX-_NX+1000:midX+_NX+1000])
ax[3].set_title('+1 / 0')
ax[4].imshow(C[midY-_NY:midY+_NY,midX-_NX+3000:midX+_NX+3000])
ax[4].set_title('+1')
for a in ax:
    a.set_xticks([int(((2*_NX)-1.0)*(b/(numXticks-1.0))) for b in range(0,numXticks)])
    a.set_xticklabels([round_sig((2*_NX)*dx*(a/(numXticks-1.0))*sF) for a in  range(-int((numXticks-1.0)/2.0),int((numXticks/2.0 + 1.0)))],fontsize=fSize)
    a.set_xlabel('x [$\mu$m]')
    a.set_yticks([int(((2*_NY)-1.0)*(b/(numYticks-1.0))) for b in range(0,numYticks)])
for a in ax[1::]:
    a.set_yticklabels([])#,fontsize=fSize )
ax[0].set_yticklabels([round_sig((2*_NY)*dy*(a/(numYticks-1.0))*sF) for a in range(-int((numYticks-1.0)/2.0),int((numYticks/2.0 + 1.0)))])
ax[0].set_ylabel('y [$\mu$m]')
# plt.tight_layout()
plt.show()


fig,ax = plt.subplots(1,5)
ax[0].imshow(I[midY-_NY:midY+_NY,midX-_NX-3000:midX+_NX-3000])
ax[0].set_title('-1')
ax[1].imshow(I[midY-_NY:midY+_NY,midX-_NX-1000:midX+_NX-1000])
ax[1].set_title('-1 / 0')
ax[2].imshow(I[midY-_NY:midY+_NY,midX-_NX+24:midX+_NX+24])
ax[2].set_title('0')
ax[3].imshow(I[midY-_NY:midY+_NY,midX-_NX+1000:midX+_NX+1000])
ax[3].set_title('+1 / 0')
ax[4].imshow(I[midY-_NY:midY+_NY,midX-_NX+3000:midX+_NX+3000])
ax[4].set_title('+1')
for a in ax:
    a.set_xticks([int(((2*_NX)-1.0)*(b/(numXticks-1.0))) for b in range(0,numXticks)])
    a.set_xticklabels([round_sig((2*_NX)*dx*(a/(numXticks-1.0))*sF) for a in  range(-int((numXticks-1.0)/2.0),int((numXticks/2.0 + 1.0)))],fontsize=fSize)
    a.set_xlabel('x [$\mu$m]')
    a.set_yticks([int(((2*_NY)-1.0)*(b/(numYticks-1.0))) for b in range(0,numYticks)])
for a in ax[1::]:
    a.set_yticklabels([])#,fontsize=fSize )
ax[0].set_yticklabels([round_sig((2*_NY)*dy*(a/(numYticks-1.0))*sF) for a in range(-int((numYticks-1.0)/2.0),int((numYticks/2.0 + 1.0)))])
ax[0].set_ylabel('y [$\mu$m]')
# plt.tight_layout()
plt.show()

fig,ax = plt.subplots(1,5)
ax[0].imshow(P[midY-_NY:midY+_NY,midX-_NX-3000:midX+_NX-3000])
ax[0].set_title('-1')
ax[1].imshow(P[midY-_NY:midY+_NY,midX-_NX-1000:midX+_NX-1000])
ax[1].set_title('-1 / 0')
ax[2].imshow(P[midY-_NY:midY+_NY,midX-_NX+24:midX+_NX+24])
ax[2].set_title('0')
ax[3].imshow(P[midY-_NY:midY+_NY,midX-_NX+1000:midX+_NX+1000])
ax[3].set_title('+1 / 0')
ax[4].imshow(P[midY-_NY:midY+_NY,midX-_NX+3000:midX+_NX+3000])
ax[4].set_title('+1')
for a in ax:
    a.set_xticks([int(((2*_NX)-1.0)*(b/(numXticks-1.0))) for b in range(0,numXticks)])
    a.set_xticklabels([round_sig((2*_NX)*dx*(a/(numXticks-1.0))*sF) for a in  range(-int((numXticks-1.0)/2.0),int((numXticks/2.0 + 1.0)))],fontsize=fSize)
    a.set_xlabel('x [$\mu$m]')
    a.set_yticks([int(((2*_NY)-1.0)*(b/(numYticks-1.0))) for b in range(0,numYticks)])
for a in ax[1::]:
    a.set_yticklabels([])#,fontsize=fSize )
ax[0].set_yticklabels([round_sig((2*_NY)*dy*(a/(numYticks-1.0))*sF) for a in range(-int((numYticks-1.0)/2.0),int((numYticks/2.0 + 1.0)))])
ax[0].set_ylabel('y [$\mu$m]')
# plt.tight_layout()
plt.show()