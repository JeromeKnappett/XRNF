#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 12:49:27 2022

@author: -
"""

import lineProfile
import moireAlignment
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.gridspec as gridspec
import tifffile
from scipy.signal import find_peaks, peak_widths
from math import floor, log10

plt.rcParams["figure.figsize"] = (12,10)

def round_sig(x, sig=2):
    if x != 0:
        return round(x, sig-int(floor(log10(abs(x))))-1)
    else:
            return x

def getProfiles(t,nx,ny,offset,show=False):
    
    x1 = lineProfile.getLineProfile(t,axis=1,mid=[int(ny/2)-offset,0],show=show)
    x2 = lineProfile.getLineProfile(t,axis=1,mid=[int(ny/2)+offset,0],show=show)

    y1 = lineProfile.getLineProfile(t,axis=0,mid=[0,int(nx/2)-offset],show=show)
    y2 = lineProfile.getLineProfile(t,axis=0,mid=[0,int(nx/2)+offset],show=show)

    return x1,x2,y1,y2

def plotSeparately(t,x1,x2,y1,y2,nx,ny,offset,px):

    figure, ax = plt.subplots(1) 
    xr1 = patches.Rectangle((0,ny/2-offset),nx,0, edgecolor=colours[0], facecolor="none", lineWidth=1)
    xr2 = patches.Rectangle((0,ny/2+offset),nx,0, edgecolor=colours[1], facecolor="none", lineWidth=1)
    yr1 = patches.Rectangle((nx/2-offset,0),0,ny, edgecolor=colours[2], facecolor="none", lineWidth=1)
    yr2 = patches.Rectangle((nx/2+offset,0),0,ny, edgecolor=colours[3], facecolor="none", lineWidth=1)
    plt.imshow(t,cmap='gray')
    
    plt.xticks([int((nx-1)*((b/(5.0-1)))) for b in range(0,5)],
               [round_sig(nx*px*1e3*(a/(5.0-1))) for a in range(-int((5-1)/2),int((5/2 + 1)))])
    plt.yticks([int((ny-1)*(b/(5.0-1))) for b in range(0,5)],
               [round_sig(ny*px*1e3*(a/(5.0-1))) for a in range(-int((5-1)/2),int((5/2 + 1)))])
                
    for r in [xr1,xr2,yr1,yr2]:
        ax.add_patch(r)
    plt.text(50,ny/2-offset-10,'x1',fontsize=20,color=colours[0])
    plt.text(50,ny/2+offset-10,'x2',fontsize=20,color=colours[1])
    plt.text(nx/2-offset+10,50,'y1',fontsize=20,color=colours[2])
    plt.text(nx/2+offset+10,50,'y2',fontsize=20,color=colours[3])
    plt.xlabel('x [mm]')
    plt.ylabel('y [mm]')
    plt.colorbar()
    plt.show()
    
    fig, ax = plt.subplots(2,1)
    ax[0].plot(x1,label='x1',color=colours[0])
    ax[0].plot(x2,label='x2',color=colours[1])
    ax[1].plot(y1,label='y1',color=colours[2])
    ax[1].plot(y2,label='y2',color=colours[3])
    ax[0].legend()
    ax[1].legend()
    plt.show()
    
def plotTogether(t,x1,x2,y1,y2,nx,ny,offset,px,indexX=None,indexY=None):
    
    x = np.linspace(0,nx,nx)
    y = np.linspace(0,ny,ny)
    
    gs = gridspec.GridSpec(2, 2,width_ratios=[10,5], height_ratios=[10,5])
    ax = [plt.subplot(gs[0]),plt.subplot(gs[1]),plt.subplot(gs[2]),plt.subplot(gs[3])]
    xr1 = patches.Rectangle((0,ny/2-offset),nx,0, edgecolor=colours[0], facecolor="none", lineWidth=1)
    xr2 = patches.Rectangle((0,ny/2+offset),nx,0, edgecolor=colours[1], facecolor="none", lineWidth=1)
    yr1 = patches.Rectangle((nx/2-offset,0),0,ny, edgecolor=colours[2], facecolor="none", lineWidth=1)
    yr2 = patches.Rectangle((nx/2+offset,0),0,ny, edgecolor=colours[3], facecolor="none", lineWidth=1)
    ax[0].imshow(t,cmap='gray')
    for a in [ax[0],ax[2]]:
        a.set_xticks([int((nx-1)*((b/(5.0-1)))) for b in range(0,5)])
        a.set_xticklabels([round_sig(nx*px*1e3*(a/(5.0-1))) for a in range(-int((5-1)/2),int((5/2 + 1)))])
    for a in [ax[0],ax[1]]:
        a.set_yticks([int((ny-1)*(b/(5.0-1))) for b in range(0,5)])
        a.set_yticklabels([round_sig(ny*px*1e3*(a/(5.0-1))) for a in range(-int((5-1)/2),int((5/2 + 1)))])
    ax[0].set_xlabel('x [mm]')
    ax[1].set_ylabel('y [mm]')
    ax[1].set_xlabel('I [a.u]')
    ax[2].set_ylabel('I [a.u]')
    for r in [xr1,xr2,yr1,yr2]:
        ax[0].add_patch(r)
    ax[1].plot(y1,x,colours[2])
    ax[1].plot(y2,x,colours[3])
    if indexY:
        ax[1].plot(y1[indexY[1]],y[indexY[1]],'x',color='black')
        ax[1].plot(y2[indexY[2]],y[indexY[2]],'x',color='blue')
        ax[1].plot(y1[indexY[3]],y[indexY[3]],'o',color='black')
        ax[1].plot(y2[indexY[4]],y[indexY[4]],'o',color='blue')
    ax[2].plot(-x1,colours[0])
    ax[2].plot(-x2,colours[1])
    if indexX:
        try:
            ax[2].plot(x[indexX[1]],-x1[indexX[1]],'x',color='black')
            ax[2].plot(x[indexX[2]],-x2[indexX[2]],'x',color='red')
            ax[2].plot(x[indexX[3]],-x1[indexX[3]],'o',color='black')
            ax[2].plot(x[indexX[4]],-x2[indexX[4]],'o',color='red')
        except IndexError:
            pass
    ax[-1].axis('off')
    plt.tight_layout()
    plt.show()

def findDisplacement(x1,x2,period,tolerance,maxindex=None,minindex=None,show=True):
    
    # peak finding and envelope fitting
    if maxindex:
        p1,_ = find_peaks(x1,distance=P-tolerance)
        p2,_ = find_peaks(x2,distance=P-tolerance)
        print(p1)
        p1 = [p1[i] for i in maxindex]
        p2 = [p2[i] for i in maxindex]
    if minindex:
        ip1,_ = find_peaks(1-x1,distance=P-tolerance)
        ip2,_ = find_peaks(1-x2,distance=P-tolerance)
        ip1 = [ip1[i] for i in minindex]
        ip2 = [ip2[i] for i in minindex]
    #
    x = np.linspace(0,len(x1),len(x1))
        
#    if maxindex:
#        p1 = [p1[i] for i in maxindex]
#        p2 = [p2[i] for i in maxindex]
#    if minindex:
#        ip1 = [ip1[i] for i in minindex]
#        ip2 = [ip2[i] for i in minindex]
#    p1 = [p1[1],p1[4]]
#    p2 = [p2[1],p2[4]]
#    ip1 = [ip1[0],ip1[1],ip1[3]]
#    ip2 = [ip2[0],ip2[1],ip2[3]]
    
    
    if show:
        plt.plot(x1)
        plt.plot(x2)
        if maxindex:
            plt.plot(x[p1],x1[p1],'x',color=colours[0],label='not used')
            plt.plot(x[p2],x2[p2],'x',color=colours[1])
            plt.plot(x[p1],x1[p1],'o',color=colours[0], label='used')
            plt.plot(x[p2],x2[p2],'o',color=colours[1])
        if minindex:
            plt.plot(x[ip1],x1[ip1],'x',color=colours[2])
            plt.plot(x[ip2],x2[ip2],'x',color=colours[3]) 
            plt.plot(x[ip1],x1[ip1],'o',color=colours[2])
            plt.plot(x[ip2],x2[ip2],'o',color=colours[3])
        plt.legend()
        plt.show()
    #
    
    dp,dt = [],[]
    if maxindex == None:
        numPoints = np.max([len(p) for p in [ip1,ip2]])
    if minindex == None:
        numPoints = np.max([len(p) for p in [p1,p2]])
    else:
        numPoints = np.max([len(p) for p in [p1,p2,ip1,ip2]])
    for i,j in enumerate(range(numPoints)):
        if maxindex:
            try:
                dP = abs(p1[i]-p2[i])*px
            except IndexError:
                pass
            dp.append(dP)
        if minindex:
            try:
                dT = abs(ip1[i]-ip2[i])*px
            except IndexError:
                pass
            dt.append(dT)
        
#        print(dP)
#        print(dT)
        
        if show:
            if maxindex:
                plt.plot(i,abs(dP),'x:',color='r')
            if minindex:
                plt.plot(i,abs(dT),'x:',color='b')
    
    if show:    
        plt.xlabel('peak number')
        plt.ylabel('distance [m]')
        plt.show()
        
    if maxindex == None:        
        meanDt = np.mean(dt)
        index = [x,ip1,ip2]
        return meanDt,index
    if minindex == None:
        meanDp = np.mean(dp)
        index = [x,p1,p2]
        return meanDp,index
    else:
        meanDp = np.mean(dp)
        meanDt = np.mean(dt)
        index = [x,p1,p2,ip1,ip2]
        return meanDp,meanDt,index
    

if __name__ == '__main__':
    #loading tiffs
    fdir = '/user/home/opt/xl/xl/experiments/maskAllignment/data2/'
    dz = [10,20,30,40,50,60,70,80,90,100]
    dx = range(50,1050,50)#1e-6
    _dx = [x*1e-6 for x in dx]
    dy = [0.0]
    file = [fdir + 'dX' + str(int(x)) + 'nm/intensity.tif' for x in dx]
    #[fdir + 'dX' + str(int(x)) + 'dY' + str(int(y)) + '/intensity.tif' for x,y in zip(dx,dy)]#[fdir +  'dZ' + str(z) + 'dX1dY2/intensity.tif' for z in dz]
    t = [tifffile.imread(f) for f in file]
    t = [T/np.max(T) for T in t]
    
    # Defining parameters
    offset = 100                                # offset from centre to take line profiles (pixels)
    px = 2.277696793002915e-07 #1.6534396482857673e-06                # pixel size of intensity image (assuming equal in x and y)
    p1 = 19e-6                                 # pitch of 1st and 3rd quadrants of grating
    p2 = 20e-6                                 # pitch of 2nd and 4th quadrants of grating 
    L = 2e-3                                   # length of grating (assuming square)
    tolerance = 150                             # tolerance for distance between peaks (in pixels)
    P = moireAlignment.moirePeriod(p1,p2)/px   # expected period of Moire fringes (in pixels)
    
    maxIndex = [1,2,3,4] #[None,None]
    minIndex = [None,None] #[0,1],[1,3]
    
    #setting colours for line profile plots
    colours = ['b','y','r','g']         # x1, x2, y1, y2
    
    ny,nx = np.shape(t[0])
    
    print('nx, ny:', nx, ny)
    
    DX = []
    DY = []
    EX = []
    EY = []
    print('Analysing....')
    for i, T in enumerate(t):
        print('# ',i)
        print(" ")
        # Taking line profiles for comparison
        x1,x2,y1,y2 = getProfiles(T,nx,ny,offset,show=False)
#       # Finding the displacement of peaks in horizontal and vertical
        dpH, indexX = findDisplacement(x1,x2,P,tolerance,maxindex=maxIndex,minindex=None,show=True)
        dpV, indexY = findDisplacement(y1,y2,P,tolerance,maxindex=maxIndex,minindex=None,show=False)
        # Finding actual misalignment
        dxP = moireAlignment.misalignmentFromMoire(dpH,p1,p2)
        dxT = moireAlignment.misalignmentFromMoire(dtH,p1,p2)
        dyP = moireAlignment.misalignmentFromMoire(dpV,p1,p2)
        dyT = moireAlignment.misalignmentFromMoire(dtV,p1,p2)
        Ex = abs(dxP - _dx[i])
        Ey = abs(dyP - dy)
    
        # Plotting
        plotTogether(T,x1,x2,y1,y2,nx,ny,offset,px,indexX)#,indexY)
        
        print("Misalignment in x (from maxima): ", dxP*1e6, " um")
    #    print("Misalignment in x (from minima): ", dxT*1e6, " um")
        print("Misalignment in y (from maxima): ", dyP*1e6, " um")
    #    print("Misalignment in y (from minima): ", dyT*1e6, " um")
    
        print('Error in misalignment (x,y): ', (Ex*1e6, Ey*1e6), ' um')
        
        DX.append(dxP)
        DY.append(dyP)
        EX.append(Ex)
        EY.append(Ey)
        
    # Plotting
#    #plotSeparately(t,x1,x2,y1,y2,nx,ny,offset,px)
#    plotTogether(t,x1,x2,y1,y2,nx,ny,offset,px)
    
#    # Finding the displacement of peaks in horizontal and vertical
#    dpH, dtH, indexX = [findDisplacement(X1,X2,P,tolerance,maxindex=[1,2,3,4],minindex=[0,1],show=False) for X1,X2 in zip(x1,x2)]
#    dpV, dtV, indexY = [findDisplacement(y1,y2,P,tolerance,maxindex=[1,2,3,4],minindex=[1,3],show=False) for Y1,Y2 in zip(y1,y2)]
    
#    # Finding actual misalignment
#    dxP = [moireAlignment.misalignmentFromMoire(dph,p1,p2) for dph in dpH]
#    dxT = [moireAlignment.misalignmentFromMoire(dth,p1,p2) for dth in dtH]
#    dyP = [moireAlignment.misalignmentFromMoire(dpv,p1,p2) for dpv in dpV]
#    dyT = [moireAlignment.misalignmentFromMoire(dtv,p1,p2) for dtv in dtV]
#    Ex = [abs(dxp - dx) for dxp in dxP]
#    Ey = [abs(dyp - dy) for dyp in dyP]
    print(EX)    

    fig, ax = plt.subplots(2,1)
    ax[0].plot(np.array(_dx)*1e6,np.array(DX)*1e6,':x',label='x')
#    ax[0].plot(np.array(_dx)*1e-6,np.array(DY)*1e6,':x',label='y')
    ax[1].plot(np.array(_dx)*1e6,np.array(EX),':x',label='erX')
#    ax[1].plot(np.array(_dx)*1e-6,np.array(EY),':x',label='erY')
    ax[1].set_xlabel('Actual misalignment [um]')
    ax[0].set_ylabel('Measured misalignment [um]')
    ax[1].set_ylabel('Error')
#    ax[1].set_ylim(0,1)
    for a in ax:
        a.legend()
    plt.show()
        
