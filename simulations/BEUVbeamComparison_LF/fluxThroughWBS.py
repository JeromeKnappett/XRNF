#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 16:34:12 2023

@author: -
"""
import numpy as np
import matplotlib.pyplot as plt
from usefulWavefield import round_sig

def IoverGrating(image,Gx,Gy,dx,dy,show=False):
    """
    Parameters
    ----------
    image : 2D array
        image for processing.
    GA : float
        1D size of grating area (assuming square grating).
    dx : float
        image resolution in x.
    dy : float
        image resolution in x.
    show : bool, optional
        Specify whether to show grating area over image. The default is False.

    Returns
    -------
    Gsum : float
        summed intensity over 4-grating area.
    Csum : float
        summed intensity over central area (equal to single grating size).
    S : float
        Intensity slope over grating area (definition taken from Meng et al - J. Synchrotron Rad. (2021). 28, 902-909
                                           https://doi.org/10.1107/S1600577521003398)
    """
    from utilMask_n import defineOrderROI
    
    lX, lY = int(Gx/dx),int(Gy/dy)
    G, Isum = defineOrderROI(image,res=(dx,dy),
                             m=1,dX=lX,dY=lY,show=False)
    _G,_Isum = defineOrderROI(np.rot90(image),res=(dx,dy),
                              m=1,dX=lX,dY=lY,show=False)
        
    Gsum = Isum[1] + Isum[2] + _Isum[1] + _Isum[2]
    Csum = Isum[0]
    
    # defining ROIs for grating areas
    nx,ny = np.shape(image)[1],np.shape(image)[0]
    numXticks, numYticks = 15,15
    sF = 1e3
    midX,midY = np.shape(image)[1]//2, np.shape(image)[0]//2
    
    # plt.imshow(image,aspect='auto')
    # plt.show()
    
    ROI_0 = ((int((midX)-(lX/2)),int((midY) - (lY/2))),((int((midX)+(lX/2))),int((midY) + (lY/2))))   
    ROI_r = ((ROI_0[1][0], int((midY) - (lY/2)))), (ROI_0[1][0] + lX, int((midY) + (lY/2)))
    ROI_l = ((ROI_0[0][0] - lX, int((midY) - (lY/2)))),(ROI_0[0][0], int((midY) + (lY/2)))
    ROI_u = ((int((midX)-(lX/2)), ROI_0[1][1]),((int((midX)+(lX/2))), ROI_0[1][1] + lY))
    ROI_d = ((int((midX)-(lX/2)), ROI_0[0][1]-lY),((int((midX)+(lX/2))), ROI_0[0][1]))
    
    # getting intensity slopes over each grating area
    g0 = image[ROI_0[0][1]:ROI_0[1][1],ROI_0[0][0]:ROI_0[1][0]]
    gr = image[ROI_r[0][1]:ROI_r[1][1],ROI_r[0][0]:ROI_r[1][0]]
    gl = image[ROI_l[0][1]:ROI_l[1][1],ROI_l[0][0]:ROI_l[1][0]]
    gu = image[ROI_u[0][1]:ROI_u[1][1],ROI_u[0][0]:ROI_u[1][0]]
    gd = image[ROI_d[0][1]:ROI_d[1][1],ROI_d[0][0]:ROI_d[1][0]]
    
    # if show:
    #     fig,ax = plt.subplots(2,2)
    #     ax[0,0].imshow(gl,aspect='auto')
    #     ax[0,0].set_title('left')
    #     ax[0,1].imshow(gu,aspect='auto')
    #     ax[0,1].set_title('top')
    #     ax[1,0].imshow(gd,aspect='auto')
    #     ax[1,0].set_title('bottom')
    #     ax[1,1].imshow(gr,aspect='auto')
    #     ax[1,1].set_title('right')
    #     plt.show()
        
    #     print(np.shape(gr))
    #     print(np.shape(gl))
    #     print(np.shape(gu))
    #     print(np.shape(gd))
    
    try:
        s0 = (np.max(g0)-np.min(g0)) / (np.max(g0) + np.min(g0))
    except ValueError:
        s0 = 0
    try:
        sr = (np.max(gr)-np.min(gr)) / (np.max(gr) + np.min(gr))
    except ValueError:
        sr = 0
    try:
        sl = (np.max(gl)-np.min(gl)) / (np.max(gl) + np.min(gl))
    except ValueError:
        sl = 0
    try:
        su = (np.max(gu)-np.min(gu)) / (np.max(gu) + np.min(gu))
    except ValueError:
        su = 0
    try:
        sd = (np.max(gd)-np.min(gd)) / (np.max(gd) + np.min(gd))
    except ValueError:
        sd = 0
    
    S = np.max([sr,sl,su,sd])
    
    if show:
        import matplotlib.patches as patches
    
        figure, ax = plt.subplots(1)
        rect_r = patches.Rectangle((ROI_r[0][0],ROI_r[0][1]),lX,lY, edgecolor='r', facecolor="none",hatch='|||')
        rect_l = patches.Rectangle((ROI_l[0][0],ROI_l[0][1]),lX,lY, edgecolor='r', facecolor="none",hatch='|||')
        rect_u = patches.Rectangle((ROI_u[0][0],ROI_u[0][1]),lX,lY, edgecolor='r', facecolor="none",hatch='---')
        rect_d = patches.Rectangle((ROI_d[0][0],ROI_d[0][1]),lX,lY, edgecolor='r', facecolor="none",hatch='---')
        # plt.imshow(A_0,aspect='auto')
        plt.imshow(image,aspect='auto')
        ax.add_patch(rect_r)
        ax.add_patch(rect_l)
        ax.add_patch(rect_u)
        ax.add_patch(rect_d)
        # plt.title('E = ' + str(90 + (count*10)) + ' eV')
        plt.colorbar(label='Intensity [ph/s/cm$^2$]')#[counts]')
        plt.yticks([int((ny-1.0)*(b/(numYticks-1.0))) for b in range(0,numYticks)],
                   [round_sig(ny*dy*(a/(numYticks-1.0))*sF,1) for a in range(-int((numYticks-1.0)/2.0),int((numYticks/2.0 + 1.0)))],fontsize=10)
        plt.xticks([int((nx-1.0)*(b/(numXticks-1.0))) for b in range(0,numXticks)],
                   [round_sig(nx*dx*(a/(numXticks-1.0))*sF,1) for a in  range(-int((numXticks-1.0)/2.0),int((numXticks/2.0 + 1.0)))],fontsize=10)
        plt.xlabel('x [mm]')
        plt.ylabel('y [mm]')
        # plt.xlim(midX-100,midX+100)
        # plt.ylim(midY-100,midY+100)
        plt.show()
    
    return Gsum, Csum, S


fSize = 10
numXticks = 5
numYticks = 5

dirPath = '/user/home/opt/xl/xl/experiments/BEUVharmonic1/data/m3atM1_smallWBS/'


nx = str(np.loadtxt(dirPath + str('InitialIntensity.dat'), dtype=str, comments=None, skiprows=6, max_rows=1, usecols=(0)))[1:]#[1:3]
ny = str(np.loadtxt(dirPath + str('InitialIntensity.dat'), dtype=str, comments=None, skiprows=9, max_rows=1, usecols=(0)))[1:]#[1:3]
xMin = str(np.loadtxt(dirPath + str('InitialIntensity.dat'), dtype=str, comments=None, skiprows=4, max_rows=1, usecols=(0)))[1:]#[1:3]
xMax = str(np.loadtxt(dirPath + str('InitialIntensity.dat'), dtype=str, comments=None, skiprows=5, max_rows=1, usecols=(0)))[1:]#[1:3]
rx = float(xMax)-float(xMin)
dx = np.divide(rx,float(nx))
yMin = str(np.loadtxt(dirPath + str('InitialIntensity.dat'), dtype=str, comments=None, skiprows=7, max_rows=1, usecols=(0)))[1:]#[1:3]
yMax = str(np.loadtxt(dirPath + str('InitialIntensity.dat'), dtype=str, comments=None, skiprows=8, max_rows=1, usecols=(0)))[1:]#[1:3]
ry = float(yMax)-float(yMin)
dy = np.divide(ry,float(ny))
I = np.reshape(np.loadtxt(dirPath+str('InitialIntensity.dat'),skiprows=10), (int(ny),int(nx)))

plt.imshow(I,aspect='auto')
plt.title('WBS incident : 14.3 m propagation',fontsize=fSize)

plt.xticks([int((float(nx)-1.0)*(a/(numXticks-1.0))) for a in range(numXticks)], [round_sig(float(nx)*dx*(b/(numXticks-1.0))*1e3) for b in range(-int((numXticks-1.0)/2.0),int((numXticks/2.0 + 1.0)))],fontsize=fSize)
plt.yticks([int((float(ny)-1.0)*(a/(numYticks-1.0))) for a in range(numYticks)], [round_sig(float(ny)*dy*(b/(numYticks-1.0))*1e3) for b in range(-int((numYticks-1.0)/2.0),int((numYticks/2.0 + 1.0)))],fontsize=fSize)
plt.xlabel('x - position [mm]',fontsize=fSize)
plt.ylabel('y - position [mm]',fontsize=fSize)
# plt.colorbar(label='Intensity [$ph/s/.1\%bw$]',labelsize=fSize)
plt.colorbar().set_label(label='Intensity [$ph/s/.1\%bw/mm^2$]',size=fSize)

plt.text(int(nx)-int((1*int(nx))/5),int(ny)-int((4*int(ny))/20),f"nx: {int(nx)}", color='r',fontsize=fSize)
plt.text(int(nx)-int((1*int(nx))/5),int(ny)-int((3*int(ny))/20),f"ny: {int(ny)}", color='r',fontsize=fSize)
plt.text(int(nx)-int((1*int(nx))/5),int(ny)-int((2*int(ny))/20),f"dx: {float(dx)} m", color='r',fontsize=fSize)
plt.text(int(nx)-int((1*int(nx))/5),int(ny)-int((1*int(ny))/20),f"dy: {float(dy)} m", color='r',fontsize=fSize)
plt.show()

TotI = np.sum(I)

GSx=0.71e-3; GSy=0.84e-3
GBx=1.198e-3; GBy=1.488e-3

gb,cb,sb = IoverGrating(I, Gx=GBx,Gy=GBy, dx=dx, dy=dy,show=True)
gs,cs,ss = IoverGrating(I, Gx=GSx,Gy=GSy, dx=dx, dy=dy,show=True)

Is = gs + cs
Ib = gb + cb

print("Range (x,y):    ", (rx,ry))

TotI = TotI*10000 # from /cm^2 to /m^2
TotI = TotI*(dx*dy) # from per unit area to total intensity

print(dx)
print(dy)

print(" ")
print(TotI)
print((cs*10000*(dx*dy)))
print((cb*10000*(dx*dy)))

print(cb/cs)

IF = 3353002814399.3916
IF_s = 955973506237.989*10000*(dx*dy)
IF_b = 2307707845526.684*10000*(dx*dy)
IFr = 2.413987239675847

I2 = 1977732239631.5576
I2_s = 45568645148.70477
I2_b = 148455244008.71835

print(" ")
print(TotI/IF)
print(TotI/(IF + I2 + TotI))
print((cs*10000*(dx*dy))/(IF_s + cs*10000*(dx*dy) + I2_s))
print((cb*10000*(dx*dy))/(IF_b + cb*10000*(dx*dy) + I2_b))