#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  3 14:57:45 2021

@author: jerome
"""

import numpy as np
from math import log10, floor
import imageio

import matplotlib.pyplot as plt
import pylab
import pickle

#plt.style.use(['science','no-latex']) # 'ieee', 
pylab.rcParams['figure.figsize'] = (10.0, 8.0)

def round_sig(x, sig=2):
    if x != 0:
        return round(x, sig-int(floor(log10(abs(x))))-1)
    else:
        return x
    
def IoverGrating(image,GA,dx,dy,show=False):
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
    
    lX, lY = int(GA/dx),int(GA/dy)
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
    
    s0 = (np.max(g0)-np.min(g0)) / (np.max(g0) + np.min(g0))
    sr = (np.max(gr)-np.min(gr)) / (np.max(gr) + np.min(gr))
    sl = (np.max(gl)-np.min(gl)) / (np.max(gl) + np.min(gl))
    su = (np.max(gu)-np.min(gu)) / (np.max(gu) + np.min(gu))
    sd = (np.max(gd)-np.min(gd)) / (np.max(gd) + np.min(gd))
    
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
        plt.xlim(midX-500,midX+500)
        plt.ylim(midY-500,midY+500)
        plt.show()
    
    return Gsum, Csum, S

SX = [300]#,400,500,600,1000,1100,1200,1300,1400,1500] #[100,200,300,400,500,600,700,800,900,1000,1100,1200,1300,1400,1500]
# [1000,1100,1200,1300,1400,1500] #[400,500,800,900,1000]#[400,500,600,700,800,900]#,1000,1500]#[200,300,400,500]
SY = [200,300,400,500,600,700,800,900]
#[25,50,75,100,125,150,175,200,250,300,350,500,1000]

SY = SX

dirPath ='/user/home/opt/xl/xl/experiments/BEUVphaseSpace/data/' 
order = ['WBSi_n' + str(n) + '_type20' for n in [1]]#,2,3,4,5]] #'_cff1.4offset0_m1_sx' + str(x) + 'sy' + str(x) + 'FIXED' for x in SX] 
# ['atMask_cff1.4offset0_m1_sx900sy' + str(y) for y in SY]
# ['atMask_cff1.4offset0_m1_sx' + str(x) + 'sy' + str(x) for x in SX] 
# ['atMask_cff1.4offset0_m1_sx' + str(x) + 'sy300' for x in SX]
# ['atMask_cff1.4offset0_m1_sx1500sy' + str(y) for y in SY]
# ['atMask_cff1.4offset-3_m1_sx1500sy' + str(y) for y in SY]                    # keeping sx @ 1500 um
# ['atMask_cff1.4offset-3_m1_sx' + str(x) + 'sy300' for x in SX]                # keeping sy @ 300 um
# ['atMask_cff1.4offset-3_m1_sx' + str(x) + 'sy' + str(x) for x in SX]          # keeping sy and sx equal  
# ['atMask_sx' + str(x) + 'sy500' for x in SX]                                  # keeping sy @ 500 um
# ['atMask_cff1.4offset-3_m1']#'atMask_cff2offset0_m1','atMask_cff1.4offset0_m1']

trials =[ str(o) + '/' for o in order] 
mePR ='res_int_pr_me.dat' 
#'IntensityDist_SE.dat' 
#'res_int_pr_me.dat' 

justPlot = False

SAVE = False
pick = True
forStokes = True

#data = 'res_int_pr_me.dat' 

#for p in dirPath:
#    nx = str(np.loadtxt(p + 'res_int_pr_me.dat', dtype=str, comments=None, skiprows=6, max_rows=1, usecols=(0)))[1:]#[1:3]
#    ny = str(np.loadtxt(p + 'res_int_pr_me.dat', dtype=str, comments=None, skiprows=9, max_rows=1, usecols=(0)))[1:]#[1:3]
#    print("Initial resolution (x,y): {}".format((nx,ny)))
#    I = np.reshape(np.loadtxt(p + 'res_int_pr_me.dat',skiprows=10), (int(nx),int(ny)))         # Initial intensity     


if justPlot:
    I = imageio.imread(dirPath + 'afterBlock4000/afterBlock4000intensity.tif')
    Ix = I[60,:]
    
    plt.imshow(I, aspect='auto')
    plt.title("multi e intensity")
    plt.colorbar()
    plt.show()
    
    plt.plot(Ix)
    plt.xlabel('x-position [pixels]')
    plt.ylabel('intensity')
    plt.show()
    
    exit()
#break
else:
    pass

for t in trials:
    plt.clf()
    plt.close()
    name = t[0:len(str(t))-1]
    print("Analysing trial: {}".format(name))
    nx = str(np.loadtxt(dirPath+t+mePR, dtype=str, comments=None, skiprows=6, max_rows=1, usecols=(0)))[1:]#[1:3]
    ny = str(np.loadtxt(dirPath+t+mePR, dtype=str, comments=None, skiprows=9, max_rows=1, usecols=(0)))[1:]#[1:3]
    xMin = str(np.loadtxt(dirPath+t+mePR, dtype=str, comments=None, skiprows=4, max_rows=1, usecols=(0)))[1:]#[1:3]
    xMax = str(np.loadtxt(dirPath+t+mePR, dtype=str, comments=None, skiprows=5, max_rows=1, usecols=(0)))[1:]#[1:3]
    rx = float(xMax)-float(xMin)
    dx = np.divide(rx,float(nx))
    yMin = str(np.loadtxt(dirPath+t+mePR, dtype=str, comments=None, skiprows=7, max_rows=1, usecols=(0)))[1:]#[1:3]
    yMax = str(np.loadtxt(dirPath+t+mePR, dtype=str, comments=None, skiprows=8, max_rows=1, usecols=(0)))[1:]#[1:3]
    ry = float(yMax)-float(yMin)
    dy = np.divide(ry,float(ny))
    
    numC = int(str(np.loadtxt(dirPath+t+mePR, dtype=str, comments=None, skiprows=10, max_rows=1, usecols=(0)))[1:])#[1:3]
    
    print("Resolution (x,y): {}".format((nx,ny)))
    print("xRange: {}".format(rx))
    print("xMax: {}".format(xMax))
    print("xMin: {}".format(xMin))
    print("yRange: {}".format(rx))
    print("yMax: {}".format(xMax))
    print("yMin: {}".format(xMin))
    print("Dx, Dy : {}".format((dx,dy)))
    
    I = np.reshape(np.loadtxt(dirPath+t+mePR,skiprows=10), (numC, int(ny),int(nx)))         # Propagated multi-electron intensity
    Iflat = I.flatten()
    
    if forStokes:
        import time
        import array
        E = np.loadtxt(dirPath+t+mePR,skiprows=10)
        nTot = int(nx)*int(ny)
        Eh = E[0:2*nTot]
        Ev = E[2*nTot::]
    
        Ex = array.array('f',[0]*nTot*2)
        Ey = array.array('f',[0]*nTot*2)
        
        start = time.time()
        print("Reshaping and saving electric field for stokes analysis... ")
        for i in range(nTot):
            i2 = i*2
            i2p1 = i2 + 1
#            print(i)
#            print(ex[i2p1])
#            print(ev[n+i])
            Ex[i2] = Eh[i]
            Ex[i2p1] = Eh[nTot + i]
            Ey[i2] = Ev[i]
            Ey[i2p1] = Ev[nTot + i]
    
        
        with open(dirPath + t+t[0:len(t)-1]+ 'EforS.pkl', "wb") as f:
                pickle.dump([Ex,Ey, nx, ny, dx, dy], f)
        
        end = time.time()
        print("Time taken to reshape and save electric field (s): ", (end-start))
    
    plt.plot(Iflat)
    plt.show()
          
    """ Creating array of custom tick markers for plotting """
    sF = 1 #e6
    tickAx = [round_sig(-rx*sF/2),
              round_sig(-rx*sF/4),
              0,
              round_sig(rx*sF/4),
              round_sig(rx*sF/2)
              ]
    tickAy = [round_sig(-ry*sF/2),
              round_sig(-ry*sF/4),
              0,
              round_sig(ry*sF/4),
              round_sig(ry*sF/2)]
    
    try:
        Ise = imageio.imread(dirPath + t + 'intensity.tif')
        plt.imshow(Ise, aspect='auto')
        plt.title("single electron intensity")
        plt.colorbar()
        plt.show()
    except NameError:
        pass
    except FileNotFoundError:
        pass
    
    if numC > 1:
        I1 = I[0,:,:]
        I2 = I[1,:,:]
        I3 = I[2,:,:]
        I4 = I[3,:,:]
    
        plt.imshow(I1)
        plt.title("I - component 1: {}".format(name))
        plt.colorbar()
        plt.show()
        
        smin = np.min(I)
        smax = np.max(I)
        fig, axs = plt.subplots(2, 2)
        #plt.clf()
        #plt.close()
        axs[0,0].imshow(I1, aspect='auto')#, vmin=smin, vmax=smax)
        #plt.xticks(np.arange(0,float(nx)+1,float(nx)/4),tickAx)
        #plt.yticks(np.arange(0,float(ny)+1,float(ny)/4),tickAy)
        #plt.xlabel("position [m]") # [\u03bcm]")
        #plt.xlabel("position [m]") # [\u03bcm]")
        axs[0,0].set_title("C #1") #Multi-Electron Intensity")
        im = axs[1,0].imshow(I2, aspect='auto')#, vmin=smin, vmax=smax)
        axs[1,0].set_title("C #2")
        axs[0,1].imshow(I3, aspect='auto')#, vmin=smin, vmax=smax)
        axs[0,1].set_title("C #3")
        axs[1,1].imshow(I4, aspect='auto')#, vmin=smin, vmax=smax)
        axs[1,1].set_title("C #4")
#        fig.subplots_adjust(right=0.8)
#        cbar_ax = fig.add_axes([0.82, 0.4, 0.025, 0.2])
#        fig.colorbar(im,cax=cbar_ax)
        #plt.savefig(dirPath + "plots/" + "intensity" + name + ".png")
        #print("Saving intensity plot to: {}".format("plots/" + "intensity" + name + ".png"))
        plt.show()
        #plt.clf()
        #plt.close()
        if SAVE:
            imageio.imwrite(dirPath+t+t[0:len(t)-1]+'ExReal.tif',np.float32(I1))        
            imageio.imwrite(dirPath+t+t[0:len(t)-1]+'ExIm.tif',np.float32(I2))        
            imageio.imwrite(dirPath+t+t[0:len(t)-1]+'EyReal.tif',np.float32(I3))        
            imageio.imwrite(dirPath+t+t[0:len(t)-1]+'EyIm.tif',np.float32(I4))
        else:
            pass
        if pick:
            with open(dirPath + t+t[0:len(t)-1]+ 'Efields.pkl', "wb") as f:
                pickle.dump([np.float32(I1),np.float32(I2),np.float32(I3),np.float32(I4), dx, dy], f)
        else:
            pass

    else:
        plt.imshow(I[0,:,:], aspect='auto')
        plt.title("Multi-electron intensity: ".format(name))
        plt.xticks(np.arange(0,int(nx)+1,int(nx)/4),tickAx)
        plt.yticks(np.arange(0,int(ny)+1,int(ny)/4),tickAy)
        plt.colorbar()
#        if SAVE == True:
#            print("Saving propagated intensity plot to: " + dirPath + "plots/" + "Propintensity" + name + ".png")
#            plt.savefig(dirPath + "plots/" + "Propintensity" + name + ".png")
        plt.show()
        
        if SAVE:
#            imageio.imwrite(dirPath+'tiffs/'+t[0:len(t)-1]+'intensity.tif',np.float32(I[0,:,:]))
            imageio.imwrite(dirPath+t+t[0:len(t)-1]+'intensity.tif',np.float32(I[0,:,:]))
        else:
            pass
        
        if pick:
            with open(dirPath + t+t[0:len(t)-1]+ '.pkl', "wb") as f:
                pickle.dump([np.float32(I[0,:,:]), dx, dy], f)
        else:
            pass
    
    
    try:
        ix = str(np.loadtxt(dirPath + t + 'res_int_se.dat', dtype=str, comments=None, skiprows=6, max_rows=1, usecols=(0)))[1:4]#[1:3]
        iy = str(np.loadtxt(dirPath + t + 'res_int_se.dat', dtype=str, comments=None, skiprows=9, max_rows=1, usecols=(0)))[1:4]#[1:3]
        print("Initial resolution (x,y): {}".format((ix,iy)))
        I0 = np.reshape(np.loadtxt(dirPath + t + 'res_int_se.dat',skiprows=10), (int(ix),int(iy)))         # Initial intensity     
    except OSError:
        print("No initial intensity file found...")
    except ValueError:
        print("Unexpected initial dimensions - Initial intensity file could not be reshaped")
        pass
    #try:
    #    I = np.reshape(np.loadtxt(dirPath + 'res_int_pr_me.dat',skiprows=11), (nx,ny))          # Propagated intensity
    #except OSError:
    #    print("No propagated intensity file found...")
    #except ValueError:
    #    print("Unexpected initial dimensions - Propagated intensity file could not be reshaped")
    #    pass
    try:
        cX = np.reshape(np.loadtxt(dirPath + t + 'res_int_pr_me_dcx.dat',skiprows=11), (int(nx),int(nx)))     # Horizontal coherence
        cY = np.reshape(np.loadtxt(dirPath + t + 'res_int_pr_me_dcy.dat',skiprows=11), (int(ny),int(ny)))     # Vertical coherence    
        dCx = np.diagonal(np.squeeze(cX))
        dCy = np.diagonal(np.squeeze(cY))
    except OSError:
        print("No coherence files found...")
    except ValueError:
        print("Unexpected initial dimensions - Coherence files could not be reshaped")
        pass
    try:
        miX = np.reshape(np.loadtxt(dirPath + t + 'res_int_pr_me_mix.dat',skiprows=11), (int(nx),int(nx),2))  # Horizontal mutual intensity
        miY = np.reshape(np.loadtxt(dirPath + t + 'res_int_pr_me_miy.dat',skiprows=11), (int(ny),int(ny),2)) # Vertical mutual intensity
    except OSError:
        print("No mutual intensity files found...")
    except ValueError:
        print("Unexpected initial dimensions - Mutual intensity files could not be reshaped")
        pass
    
    
    
    """ Plotting intensity, coherence """
    try:
        plt.clf()
        plt.close()
        plt.imshow(I0)
        plt.xticks(np.arange(0,nx+1,nx/4),tickAx)
        plt.yticks(np.arange(0,ny+1,ny/4),tickAy)
        plt.xlabel("position [m]") # [\u03bcm]")
        plt.xlabel("position [m]") # [\u03bcm]")
        plt.title("Initial intensity, : " + name)
        plt.colorbar()
        if SAVE == True:
            plt.savefig(dirPath + "plots/" + "initialintensity" + name + ".png")
            print("Saving initial intensity plot to: {}".format("plots/" + "initialintensity" +name + ".png"))
        plt.show()
        plt.clf()
        plt.close()
    except NameError:
        print("No initial intensity file...")
    except TypeError:
        print("... initial intensity file may be wrong dimensions")
        pass
    
    try:
        plt.clf()
        plt.close()
        plt.imshow(I)
        plt.xticks(np.arange(0,nx+1,nx/4),tickAx)
        plt.yticks(np.arange(0,ny+1,ny/4),tickAy)
        plt.xlabel("position [m]") # [\u03bcm]")
        plt.xlabel("position [m]") # [\u03bcm]")
        plt.title("Intensity, e =" + name)
        plt.colorbar()
        if SAVE == True:
            plt.savefig(dirPath + "plots/" + "intensity" + name + ".png")
            print("Saving intensity plot to: {}".format("plots/" + "intensity" + name + ".png"))
        plt.show()
        plt.clf()
        plt.close()
    except NameError:
        print("No propagated intensity file...")
    except TypeError:
        print("... propagated intensity file may be wrong dimensions")
        pass