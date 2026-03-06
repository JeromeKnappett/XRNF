#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 14 12:28:16 2024

@author: jerome
"""

import numpy as np
import matplotlib.pyplot as plt
import pylab
from math import log10, floor, e
from FWatArbValue import getFWatValue
# import imageio

def round_sig(x, sig=2):
    if x != 0:
        return round(x, sig-int(floor(log10(abs(x))))-1)
    else:
        return x



pylab.rcParams['figure.figsize'] = (4,3)
#(4.1, 4.0)
colours = plt.rcParams["axes.prop_cycle"].by_key()["color"]

dirPath = '/home/jerome/Documents/PhD/Data/185/'
#spectra/'#185/'
E = 185
#90#185
B = 0.4611
#0.4605
#0.453
#0.4571
#0.4605

# Reading .dat file and extracting values
filename = 'Intensity_WBS_m3_ME.dat'
#'InitialIntensity_n1_me.dat'
#'Intensity_WBS_m1_ME.dat'     # propagated to WBS (ME)
#'InitialIntensity_n3.dat'     # from sirepo - initial @ WBS (SE)
#'InitialIntensity_n1_me.dat' # from sirepo - initial @ WBS (ME)
#'res_int_se_' + str(E) + 'eV.dat'
#'res_int_se_B' + str(B) + '.dat'
#'InitialIntensity_n1.dat'
#'res_int_se_B' + str(B) + '.dat'
#else:
#    print(f"Plane:                               {'Final'}")
#    filename = 'res_int_pr_se.dat'

plot = 'both'
#'both'
#'2d'
#'cuts'
fitGauss = False
showParams = False
WBSlines = True
showFWHM = False
convert2flux = False
fmat = 'eps'

if convert2flux:
    savePath = dirPath + filename[0:len(filename) - 4] + '_FLUX.' + fmat
else:
    savePath = dirPath + filename[0:len(filename) - 4] + '_I.' + fmat

print('Saving to ....          ', savePath)
#dirPath + 'n3_IntensityPlot_B' + str(B) + '_withFWHM' + '.' + fmat 
#dirPath + 'n2_IntensityPlot_B' + str(B) + '.' + fmat 
#dirPath + 'n2_IntensityPlot_B' + str(B) + '_withFWHM.png' 
# dirPath + 'IntensityPlot_B' + str(B) + '.eps'

C = [colours[3],colours[0],colours[1]]

wbsX, wbsY = [0.84,4],[1,3]

numXticks = 5
numYticks = 5
fSize = 15
lineWidth = 1

#print(f"Element number:                      {e}")
## print(f"Intensity data file: {dirPath + 'res_int_pr_se.dat'}")
#if e ==0:
#print(f"Plane:                               {'WBS incident'}")
nx = str(np.loadtxt(dirPath + str(filename), dtype=str, comments=None, skiprows=6, max_rows=1, usecols=(0)))[1:]#[1:3]
ny = str(np.loadtxt(dirPath + str(filename), dtype=str, comments=None, skiprows=9, max_rows=1, usecols=(0)))[1:]#[1:3]
xMin = str(np.loadtxt(dirPath + str(filename), dtype=str, comments=None, skiprows=4, max_rows=1, usecols=(0)))[1:]#[1:3]
xMax = str(np.loadtxt(dirPath + str(filename), dtype=str, comments=None, skiprows=5, max_rows=1, usecols=(0)))[1:]#[1:3]
rx = float(xMax)-float(xMin)
dx = np.divide(rx,float(nx))
yMin = str(np.loadtxt(dirPath + str(filename), dtype=str, comments=None, skiprows=7, max_rows=1, usecols=(0)))[1:]#[1:3]
yMax = str(np.loadtxt(dirPath + str(filename), dtype=str, comments=None, skiprows=8, max_rows=1, usecols=(0)))[1:]#[1:3]
ry = float(yMax)-float(yMin)
dy = np.divide(ry,float(ny))
pa = dx*dy # pixel area in m^2

I = np.reshape(np.loadtxt(dirPath+str(filename),skiprows=10), (int(ny),int(nx)))

if convert2flux:
    I = (I*1e6) * pa

X = np.linspace(float(xMin)*1e3,float(xMax)*1e3,int(nx))
Y = np.linspace(float(yMin)*1e3,float(yMax)*1e3,int(ny))

Ix = I[int(ny)//2,:]
Iy = I[:,int(nx)//2]


fx,fy = getFWatValue(I,dx,dy,frac=1/(e**2), show=True)
print('Beam size at 1/e^2 (x,y) [mm]:   ', (fx*1e3 / 2,fy*1e3 / 2))
fxhm,fyhm = getFWatValue(I,dx,dy,frac=1/2, show=True)
#fxhm = fxhm/2.35
#fyhm = fyhm/2.35
print('Beam FWHM (x,y) [mm]:   ', (fxhm*1e3,fyhm*1e3))
#fxhmG,fyhmG, Gx, Gy = getFWatValue(I,dx,dy,frac=1/2, show=False,smoothing='gauss')
#print('Beam FWHM with gaussian fitting (x,y) [mm]:   ', (fxhmG*1e3,fyhmG*1e3))
#fxhmGe,fyhmGe, Gxe, Gye = getFWatValue(I,dx,dy,frac=1/(e**2), show=False,smoothing='gauss')
#print('Beam size at 1/e^2 with gaussian fitting (x,y) [mm]:   ', (fxhmGe*1e3,fyhmGe*1e3))

if plot == '2d':
    # ploting 2d intensity
    plt.imshow(I,aspect='auto',cmap='gray')
    # plt.title('WBS incident : 14.3 m propagation',fontsize=fSize)
    plt.xticks([int((float(nx)-1.0)*(a/(numXticks-1.0))) for a in range(numXticks)], [round_sig(float(nx)*dx*(b/(numXticks-1.0))*1e3) for b in range(-int((numXticks-1.0)/2.0),int((numXticks/2.0 + 1.0)))],fontsize=fSize)
    plt.yticks([int((float(ny)-1.0)*(a/(numYticks-1.0))) for a in range(numYticks)], [round_sig(float(ny)*dy*(b/(numYticks-1.0))*1e3) for b in range(-int((numYticks-1.0)/2.0),int((numYticks/2.0 + 1.0)))],fontsize=fSize)
    plt.xlabel('x-position [mm]',fontsize=fSize)
    plt.ylabel('y-position [mm]',fontsize=fSize)
    # plt.colorbar(label='Intensity [$ph/s/.1\%bw$]',labelsize=fSize)
    if convert2flux:
        plt.colorbar().set_label(label='Flux [ph/s/.1\%bw]',size=fSize)
    else:
        plt.colorbar().set_label(label='Intensity [ph/s/.1\%bw/mm$^2$]',size=fSize)
    
    if showParams:
        plt.text(int(nx)-int((1*int(nx))/5),int(ny)-int((4*int(ny))/20),f"nx: {int(nx)}", color='r',fontsize=fSize)
        plt.text(int(nx)-int((1*int(nx))/5),int(ny)-int((3*int(ny))/20),f"ny: {int(ny)}", color='r',fontsize=fSize)
        plt.text(int(nx)-int((1*int(nx))/5),int(ny)-int((2*int(ny))/20),f"dx: {float(dx)} m", color='r',fontsize=fSize)
        plt.text(int(nx)-int((1*int(nx))/5),int(ny)-int((1*int(ny))/20),f"dy: {float(dy)} m", color='r',fontsize=fSize)
    else:
        pass
    plt.show()

if plot == 'cuts':
    # ploting 1d intensity profiles
    plt.plot(X,Ix,color=colours[5])
    #plt.xticks([int((float(nx)-1.0)*(a/(numXticks-1.0))) for a in range(numXticks)], [round_sig(float(nx)*dx*(b/(numXticks-1.0))*1e3) for b in range(-int((numXticks-1.0)/2.0),int((numXticks/2.0 + 1.0)))],fontsize=fSize)
    plt.xlabel('x-position [mm]')
    if convert2flux:
        plt.ylabel('Flux [ph/s/.1\%bw]',size=fSize)
    else:
        plt.ylabel('Intensity [ph/s/.1%bw/mm$^2$]')
    if WBSlines:
        for lx,ly,c in zip(wbsX,wbsY,C):
            plt.axvline(x=-lx/2,color=c,linestyle=':',label='WBS=' + str(lx) + r'$\times$' + str(ly) + ' mm$^2$')
            plt.axvline(x=lx/2,color=c,linestyle=':')
    plt.legend(frameon=True,fancybox=True,framealpha=1.0,fontsize=5)
    
    if fitGauss:
#        Gx = (np.max(I)) * np.exp(-(X**2) / (2 * (14.3**2) * ((0.053)**2)))
        plt.plot(X,Gx,':g')
    
    plt.show()
    
    plt.plot(Y,Iy,color=colours[5])
    #plt.xticks([int((float(ny)-1.0)*(a/(numYticks-1.0))) for a in range(numYticks)], [round_sig(float(ny)*dy*(b/(numYticks-1.0))*1e3) for b in range(-int((numYticks-1.0)/2.0),int((numYticks/2.0 + 1.0)))],fontsize=fSize)
    plt.xlabel('y-position [mm]')
    if convert2flux:
        plt.ylabel('Flux [ph/s/.1\%bw]',size=fSize)
    else:
        plt.ylabel('Intensity [ph/s/.1%bw/mm$^2$]')
    if WBSlines:
        for lx,ly,c in zip(wbsX,wbsY,C):
            plt.axvline(x=-ly/2,color=c,linestyle=':',label='WBS=' + str(lx) + r'$\times$' + str(ly) + ' mm$^2$')
            plt.axvline(x=ly/2,color=c,linestyle=':')
    plt.legend(frameon=True,fancybox=True,framealpha=1.0,fontsize=5)
    
    if fitGauss:
#        Gy = (np.max(I)) * np.exp(-(Y**2) / (2 * (14.3**2) * ((0.04)**2)))
        plt.plot(X,Gy,':g')
        
        Gx_center = Gx[len(Gx)//2]
        Gy_center = Gy[len(Gy)//2]
        frac = 0.5
        gw_x = len(Gx[Gx>(Gx.max()*frac)])*dx
        gw_y = len(Gy[Gy>(Gy.max()*frac)])*dy
        print('Gaussian beam FWHM (x,y) [mm]:   ', (gw_x*1e3,gw_y*1e3))
    
    plt.show()

    plt.plot(X,Ix,color=colours[5],label='x')
    plt.plot(Y,Iy,color=C[0],label='y')
    plt.xlabel('x/y position [mm]')
    if convert2flux:
        plt.ylabel('Flux [ph/s/.1\%bw]',size=fSize)
    else:
        plt.ylabel('Intensity [ph/s/.1\%bw/mm$^2$]')
    plt.legend()
    plt.show()

if plot == 'both':
    # plotting together
    
    import matplotlib.gridspec as gridspec
    from mpl_toolkits.axes_grid1 import make_axes_locatable
    
    pylab.rcParams['figure.figsize'] = (4.15, 4.0)
    x,y = X,Y
    X, Y = np.meshgrid(x,y)
    #def f(x,y) :
    #    return np.exp(-(x**2/4+y**2)/.2)*np.cos((x**2+y**2)*10)**2
    data = I
    # 2d image plot with profiles
    h, w = data.shape
    gs = gridspec.GridSpec(2, 2,width_ratios=[w,w*.2], height_ratios=[h,h*.2])
    gs.update(wspace=0.05,hspace=0.05)
    ax = [plt.subplot(gs[0]),]
    ax.append(plt.subplot(gs[1], sharey=ax[0]))
    ax.append(plt.subplot(gs[2], sharex=ax[0]))
    bounds = [x.min(),x.max(),y.min(),y.max()]
    
    axi = ax[0].imshow(data, cmap='gray', extent = bounds, origin='lower')
    divider = make_axes_locatable(ax[0])
    cax = divider.append_axes("left", size="5%", pad=0.05)
    #_cax = divider.append_axes("right", size="0%", pad=0.0)
    if convert2flux:
        plt.colorbar(axi, cax=cax, orientation='vertical',label='Flux [ph/s/.1\%bw]')
    else:
        plt.colorbar(axi, cax=cax, orientation='vertical',label='Intensity [ph/s/.1\%bw/mm$^2$]')
    cax.yaxis.set_ticks_position('left')
    cax.yaxis.set_label_position('left')
    #cb = plt.colorbar(axi,ax=[ax[0]],location='left',label='Intensity [ph/s/.1\%bw/mm$^2$]')
    #ax[2].axis([data[:,w/2].max(), data[:,w/2].min(), Y.min(), Y.max()])
    ax[2].plot(x,Ix/np.max(Ix),color=colours[5])
    ax[1].plot(Iy/np.max(Iy),y,color=colours[5])
    divider2 = make_axes_locatable(ax[2])
    cax2 = divider2.append_axes("left", size="5%", pad=0.05)
    #cax3 = divider2.append_axes("right", size="15%", pad=0.065)
    ax[0].tick_params(labelleft=False,labelbottom=False)
    ax[1].invert_xaxis()
    ax[1].yaxis.tick_right()
    ax[1].yaxis.set_label_position("right")
    ax[1].set_ylabel('y-position [mm]')
    ax[2].yaxis.tick_right()
    ax[2].yaxis.set_label_position("right")
    ax[2].set_xlabel('x-position [mm]')
    ax[2].set_yticklabels([])
    #ax[1].set_yticklabels([])
    #plt.colorbar(axi, cax=cax2, orientation='vertical',label='Intensity [ph/s/.1\%bw/mm$^2$]')
    cax2.axis('off')
    #cax3.axis('off')
    #cax2.set_ylabel('here')
    #cax2.label('')
    #ax[1].set_xlabel('Intensity [ph/s/.1\%bw/mm$^2$]')#,fontsize=4)
    #ax[1].text(x=0.0, y=-0.01, s='0')
    ax[2].text(x=4.2, y=-0.05, s='0',fontsize=8)
    #ax[2].text(x=4.05, y=0.90, s='1')
    ax[2].text(x=4.25, y=0.5, s='Intensity [a.u]',fontsize=10)
    if WBSlines:
        wbs1 = ax[2].axvline(x=-wbsX[0]/2,color=C[0],linestyle=':',label='WBS=' + str(wbsX[0]) + r'$\times$' + str(wbsY[0]) + ' mm$^2$',linewidth=lineWidth)
        ax[2].axvline(x=wbsX[0]/2,color=C[0],linestyle=':',linewidth=lineWidth)
        ax[1].axhline(y=-wbsY[0]/2,color=C[0],linestyle=':',label='WBS=' + str(wbsX[0]) + r'$\times$' + str(wbsY[0]) + ' mm$^2$',linewidth=lineWidth)
        ax[1].axhline(y=wbsY[0]/2,color=C[0],linestyle=':',linewidth=lineWidth)
        wbs2 = ax[2].axvline(x=-wbsX[1]/2,color=C[1],linestyle=':',label='WBS=' + str(wbsX[1]) + r'$\times$' + str(wbsY[1]) + ' mm$^2$',linewidth=lineWidth)
        ax[2].axvline(x=wbsX[1]/2,color=C[1],linestyle=':',linewidth=lineWidth)
        ax[1].axhline(y=-wbsY[1]/2,color=C[1],linestyle=':',label='WBS=' + str(wbsX[1]) + r'$\times$' + str(wbsY[1]) + ' mm$^2$',linewidth=lineWidth)
        ax[1].axhline(y=wbsY[1]/2,color=C[1],linestyle=':',linewidth=lineWidth)
        
        import matplotlib.patches as patches
    
        rect_wbs1 = patches.Rectangle((-wbsX[0]/2,-wbsY[0]/2),wbsX[0],wbsY[0], edgecolor=C[0], facecolor="none", linestyle = ':',linewidth=lineWidth)#,hatch='|||')
        rect_wbs2 = patches.Rectangle((-wbsX[1]/2,-wbsY[1]/2),wbsX[1],wbsY[1], edgecolor=C[1], facecolor="none", linestyle = ':',linewidth=lineWidth)#,hatch='|||')
        ax[0].add_patch(rect_wbs1)
        ax[0].add_patch(rect_wbs2)
        
    #    for lx,ly,c in zip(wbsX,wbsY,C):
    #        ax[2].axvline(x=-lx/2,color=c,linestyle=':',label='WBS=' + str(lx) + r'$\times$' + str(ly) + ' mm$^2$')
    #        ax[2].axvline(x=lx/2,color=c,linestyle=':')
    #        ax[1].axhline(y=-lx/2,color=c,linestyle=':',label='WBS=' + str(lx) + r'$\times$' + str(ly) + ' mm$^2$')
    #        ax[1].axhline(y=lx/2,color=c,linestyle=':')
    if showFWHM:
        fwhmX = ax[2].axvline(x=-(fxhm*1e3)/2,color=C[2],linestyle=':',label='FWHM = ' + str(round_sig(fxhm*1e3,3)) + r'$\times$' + str(round_sig(fyhm*1e3,3)) + ' mm$^2$',linewidth=lineWidth)
        ax[2].axvline(x=(fxhm*1e3)/2,color=C[2],linestyle=':',linewidth=lineWidth)
        ax[1].axhline(y=-(fyhm*1e3)/2,color=C[2],linestyle=':',linewidth=lineWidth)
        ax[1].axhline(y=(fyhm*1e3)/2,color=C[2],linestyle=':',linewidth=lineWidth)
        
        import matplotlib.patches as patches
    
        if fitGauss:
            ax[1].plot(Gy/np.max(Gy),y,':g')
            ax[2].plot(x,Gx/np.max(Gx),':g')
        rect_fwhm = patches.Rectangle((-(fxhm*1e3)/2,-(fyhm*1e3)/2),(fxhm*1e3),(fyhm*1e3), edgecolor=C[2], facecolor="none", linestyle = ':',linewidth=lineWidth)#,hatch='|||')
        ax[0].add_patch(rect_fwhm)
    
    if WBSlines and showFWHM:
        ax[0].legend(handles=[wbs1,wbs2,fwhmX],frameon=True,fancybox=True,framealpha=1.0,fontsize=8)
#        ax[0].legend(handles=[fwhmX],frameon=True,fancybox=True,framealpha=1.0,fontsize=8)
    elif WBSlines:
#        pass
        ax[0].legend(handles=[wbs1,wbs2],frameon=True,fancybox=True,framealpha=1.0,fontsize=8)
    elif showFWHM:
        ax[0].legend(handles=[fwhmX],frameon=True,fancybox=True,framealpha=1.0,fontsize=8)
    plt.tight_layout()
    if savePath:
        plt.savefig(savePath, format=fmat)
    plt.show()
    

# Extract the 1D x- and y- coordinate arrays from X, Y
x_vals = X[0, :]        # shape (m,)
y_vals = Y[:, 0]        # shape (n,)

# Build 1D masks
WBS1maskX = (y_vals >= -wbsY[0]/2) & (y_vals <= wbsY[0]/2)
WBS1maskY = (x_vals >= -wbsX[0]/2) & (x_vals <= wbsX[0]/2)
WBS2maskX = (y_vals >= -wbsY[1]/2) & (y_vals <= wbsY[1]/2)
WBS2maskY = (x_vals >= -wbsX[1]/2) & (x_vals <= wbsX[1]/2)

# Now slice your data
WBS1 = data[WBS1maskX][:, WBS1maskY]
WBS2 = data[WBS2maskX][:, WBS2maskY]

fig, ax = plt.subplots(1,2)
ax[0].imshow(WBS1)
ax[1].imshow(WBS2)
plt.tight_layout()
plt.show()

print('Total flux over WBS 1: ', np.sum(WBS1))
print('Total flux over WBS 2: ', np.sum(WBS2))