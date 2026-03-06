#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  3 14:57:45 2021

@author: jerome
"""

import numpy as np
from math import log10, floor
import imageio
import pickle

import matplotlib.pyplot as plt
import pylab

def round_sig(x, sig=2):
    if x != 0:
        return round(x, sig-int(floor(log10(abs(x))))-1)
    else:
        return x

def IoverArea(image,Ax,Ay,dx,dy,show=False):
    """
    Parameters
    ----------
    image : 2D array
        image for processing.
    GAx,GAy : float
              x and y size of area (assuming square).
    dx : float
        image resolution in x.
    dy : float
        image resolution in x.
    show : bool, optional
        Specify whether to show grating area over image. The default is False.

    Returns
    -------
    sum : float
        summed intensity over central area (equal to single grating size).
    """
    from utilMask_n import defineOrderROI
    
    lX, lY = int(Ax/dx),int(Ay/dy)
    G, Isum = defineOrderROI(image,res=(dx,dy),
                             m=0,dX=lX,dY=lY,show=True)
    # _G,_Isum = defineOrderROI(np.rot90(image),res=(dx,dy),
                              # m=1,dX=lX,dY=lY,show=False)
        
    # Gsum = Isum[1] + Isum[2] + _Isum[1] + _Isum[2]
    Csum = Isum[0]
    
    # defining ROIs for grating areas
    nx,ny = np.shape(image)[1],np.shape(image)[0]
    numXticks, numYticks = 15,15
    sF = 1e3
    midX,midY = np.shape(image)[1]//2, np.shape(image)[0]//2
    
    # plt.imshow(image,aspect='auto')
    # plt.show()
    
    ROI_0 = ((int((midX)-(lX/2)),int((midY) - (lY/2))),((int((midX)+(lX/2))),int((midY) + (lY/2))))   
    # ROI_r = ((ROI_0[1][0], int((midY) - (lY/2)))), (ROI_0[1][0] + lX, int((midY) + (lY/2)))
    # ROI_l = ((ROI_0[0][0] - lX, int((midY) - (lY/2)))),(ROI_0[0][0], int((midY) + (lY/2)))
    # ROI_u = ((int((midX)-(lX/2)), ROI_0[1][1]),((int((midX)+(lX/2))), ROI_0[1][1] + lY))
    # ROI_d = ((int((midX)-(lX/2)), ROI_0[0][1]-lY),((int((midX)+(lX/2))), ROI_0[0][1]))
    
    # # getting intensity slopes over each grating area
    g0 = image[ROI_0[0][1]:ROI_0[1][1],ROI_0[0][0]:ROI_0[1][0]]
    # gr = image[ROI_r[0][1]:ROI_r[1][1],ROI_r[0][0]:ROI_r[1][0]]
    # gl = image[ROI_l[0][1]:ROI_l[1][1],ROI_l[0][0]:ROI_l[1][0]]
    # gu = image[ROI_u[0][1]:ROI_u[1][1],ROI_u[0][0]:ROI_u[1][0]]
    # gd = image[ROI_d[0][1]:ROI_d[1][1],ROI_d[0][0]:ROI_d[1][0]]
    
    # # if show:
    # #     fig,ax = plt.subplots(2,2)
    # #     ax[0,0].imshow(gl,aspect='auto')
    # #     ax[0,0].set_title('left')
    # #     ax[0,1].imshow(gu,aspect='auto')
    # #     ax[0,1].set_title('top')
    # #     ax[1,0].imshow(gd,aspect='auto')
    # #     ax[1,0].set_title('bottom')
    # #     ax[1,1].imshow(gr,aspect='auto')
    # #     ax[1,1].set_title('right')
    # #     plt.show()
        
    # #     print(np.shape(gr))
    #     print(np.shape(gl))
    #     print(np.shape(gu))
    #     print(np.shape(gd))
    
    s0 = (np.max(g0)-np.min(g0)) / (np.max(g0) + np.min(g0))
    # sr = (np.max(gr)-np.min(gr)) / (np.max(gr) + np.min(gr))
    # sl = (np.max(gl)-np.min(gl)) / (np.max(gl) + np.min(gl))
    # su = (np.max(gu)-np.min(gu)) / (np.max(gu) + np.min(gu))
    # sd = (np.max(gd)-np.min(gd)) / (np.max(gd) + np.min(gd))
    
    # S = np.max([sr,sl,su,sd])
    
    if show:
        import matplotlib.patches as patches
    
        figure, ax = plt.subplots(1)
        rect_a = patches.Rectangle((ROI_0[0][0],ROI_0[0][1]),lX,lY, edgecolor='r', facecolor="none")#,hatch='|||')
        # plt.imshow(A_0,aspect='auto')
        plt.imshow(image,aspect='auto')
        ax.add_patch(rect_a)
        # plt.title('E = ' + str(90 + (count*10)) + ' eV')
        plt.colorbar(label='Intensity [ph/s/cm$^2$]')#[counts]')
        plt.yticks([int((ny-1.0)*(b/(numYticks-1.0))) for b in range(0,numYticks)],
                   [round_sig(ny*dy*(a/(numYticks-1.0))*sF,1) for a in range(-int((numYticks-1.0)/2.0),int((numYticks/2.0 + 1.0)))],fontsize=10)
        plt.xticks([int((nx-1.0)*(b/(numXticks-1.0))) for b in range(0,numXticks)],
                   [round_sig(nx*dx*(a/(numXticks-1.0))*sF,1) for a in  range(-int((numXticks-1.0)/2.0),int((numXticks/2.0 + 1.0)))],fontsize=10)
        plt.xlabel('x [mm]')
        plt.ylabel('y [mm]')
        # plt.xlim(midX-500,midX+500)
        # plt.ylim(midY-500,midY+500)
        plt.show()
    
    return G, Isum

e = 2.718281828459045235360287471352

sx = [1.4,2] #np.arange(10,165,5) #[1.4,2] #np.arange(10,165,5)
sy = np.arange(10,55,5)
SY = 25

eff = [0.03267384491294766,0.04451154279639219]

dirPath ='/user/home/opt/xl/xl/experiments/BEUVharmonic3/data/'  #'/user/home/opt/xl/xl/experiments/fullbeamPolarisation/'#'/user/home/opt/xl/xl/experiments/beamCoherence2/data/' 

trials = ['atWBS_MEm1/','atWBS_MEm2/','atWBS_MEm3/','atWBS_MEm4/','atWBS_MEm5/']
# ['atMask_ME/']#,'m3_atMask_ME/','m5_atMask_ME/','m7_atMask_ME/','m9_atMask_ME/']#'fixed/','m7_atMask_MEfixed/','m9_atMask_MEfixed/']#,'150um/']#,'beforeBDA_efield_sx200/','beforeBDA_efield_sx500/'] #['data/'] #['fullRes_5000e/', 'fullRes_100e/'] #['120_1000x1000/']#'200e/','10000e/', '120e_250ir/']
mePR = 'res_int_pr_me.dat'
# 'IntensityDist_SE.dat'
# 'res_int_pr_me.dat'

justPlot = False

SAVE = True
pick = True
forStokes = False

analyse = True

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

FWHM = []
totI = []

TOTI = []
Itot = []
FWx, FWy = [], []
IG, IC = [], []
F_bWBS, F_sWBS = [],[]
for i,t in enumerate(trials):
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
    
    try:
        numC = int(str(np.loadtxt(dirPath+t+mePR, dtype=str, comments=None, skiprows=10, max_rows=1, usecols=(0)))[1:])#[1:3]
    except:
        numC = 1
        
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
        EhIm = E[0:nTot]
        EhRe = E[nTot:2*nTot]
        EvIm = E[2*nTot:3*nTot]
        EvRe = E[3*nTot::]
#        Eh = E[0:2*nTot]
#        Ev = E[2*nTot::]
#        print(np.shape(Eh))
#        print(np.shape(Ev))
        
        plt.plot(E)
        plt.show()
        
        fig,ax = plt.subplots(1,2)
        ax[0].plot(EhRe)
        ax[0].set_title('Eh (Re)')
        ax[1].plot(EhIm)
        ax[1].set_title('Eh (Im)')
        plt.show()
        fig,ax = plt.subplots(1,2)
        ax[0].plot(EvRe)
        ax[0].set_title('Ev (Re)')
        ax[1].plot(EvIm)
        ax[1].set_title('Ev (Im)')
        plt.show()
    
        Ex = array.array('f',[0]*nTot*2)
        Ey = array.array('f',[0]*nTot*2)
    
        start = time.time()
        print("Reshaping and saving electric field for stokes analysis... ")
        for i in range(0,nTot):
            i2 = i*2
            i2p1 = i2 + 1
#            print(i)
#            print(ex[i2p1])
#            print(ev[n+i])
            Ex[i2] = EhRe[i]
            Ey[i2] = EvRe[i]
            try:
                Ex[i2p1] = EhIm[i]
                Ey[i2p1] = EvIm[i]
            except IndexError:
                print("Error")
                pass
    
        
        with open(dirPath + t+t[0:len(t)-1]+ 'EforS.pkl', "wb") as f:
                pickle.dump([Ex,Ey, nx, ny, dx, dy], f)
        
        end = time.time()
        print("Time taken to reshape and save electric field (s): ", (end-start))
#    plt.plot(Iflat)
#    plt.show()
          
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
    
        plt.imshow(I1, aspect='auto')
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
        
    if analyse:
        # from FWarbValue import getFWatValue
        # fwx,fwy = getFWatValue(I[0,:,:],dx=dx,dy=dy,cuts='xy',show=False)
        # I = (I[0,:,:] / 1.0e-6) * dx * dy
        # isum = np.sum(I)
        
        # FWHM.append((fwx,fwy))
        # totI.append(isum)
        
        
    
        I = I[0,:,:]
        ranPix =[np.shape(I)[1],np.shape(I)[0]] #[800,3000] #[(11.0e-6 / dx) * 800, (11.0e-6 / dy) * 700]
        ran = [eran*eres for eran,eres in zip(ranPix,[dx,dy])]
        print('Range: ', ran)
        print('Pixel Range: ', ranPix)
        
        
        I = I[int(np.shape(I)[0]//2 - ranPix[1]//2):int(np.shape(I)[0]//2 + ranPix[1]//2),
              int(np.shape(I)[1]//2 - ranPix[0]//2):int(np.shape(I)[1]//2 + ranPix[0]//2)]
        
        # print(np.shape(I)[0]//2)
        # print(np.shape(I)[1]//2)
        plt.imshow(I)
        plt.show()
        
        # print(int(np.shape(I)[0]//2 - ranPix[1]//2))
        # print(int(np.shape(I)[0]//2 + ranPix[1]//2))
        # print(int(np.shape(I)[1]//2 - ranPix[0]//2))
        # print(int(np.shape(I)[1]//2 + ranPix[0]//2))
        
        # # convering from ph/s/0.1%bw/mm^2 to ph/s/mm^2
        # grad = 0.000396378#*0.628324754030457
        # intercept = 0.019051304
        # # try:
        # #     slv = (2/1.4)*SY[e] #350
        # # except IndexError:
        # slv = (2/1.4)*SY
        # bw = (slv*grad) + intercept
        # bw = bw
        
        # print('\n BW: ', bw)
        
        Ga = 50.0e-6
        WBSb = [4.0e-3,3.0e-3]
        WBSs = [0.84e-3,1.0e-3]
        
        # eff = 0.04451154279639219 # cff = 2, grating E = 10% - fixed angle
        #0.027501275406876923
        #0.03935212451203237 # cff = 3, grating E = 10%
        #0.03569853100423892 # cff = 2, grating E = 10%
        #0.027501275406876923 # cff = 1.4, grating E = 10%
                
        # 0.03737340348858282, 0.02216367235357039, 0.004297207161730262, 0.0005147820098211518
        
        # print('\n')
        # print(bw)
        # I = I * bw/0.1 * eff[i]
        
        # converting from ph/s/mm^2/.1%bw to ph/s/.1%bw
        I = (I / 1.0e-6) * (dx*dy)
        
        from FWarbValue import getFWatValue
        fwhmx,fwhmy = getFWatValue(I,frac=1/e,dx=dx,dy=dy,cuts='xy',
                                    centered=True,smoothing=None,#'gauss',
                                    verbose=False,show=True)

    
        # G, C, S = IoverGrating(I, GA=Ga, dx=dy, dy=dy, show=True)
        # _G, _C, _S = IoverGrating(I, GA=1.0e-3, dx=dy, dy=dy, show=True)
        
        q = 1.60218e-19
        
        g,F_wbsB = IoverArea(I,Ax=WBSb[0],Ay=WBSb[1],dx=dx,dy=dy,show=True)
        g,F_wbsS = IoverArea(I,Ax=WBSs[0],Ay=WBSs[1],dx=dx,dy=dy,show=True)
        
        
        
        TOTI = np.sum(I)
        # Itot.append(TOTI / (ran[0]*ran[1] * 10000))
        FWx.append(fwhmx*1e3);FWy.append(fwhmy*1e3)
        # I_bigWBS = ()
        # IG.append((G / (4 * Ga * Ga * 10000)))
        # IC.append((_C / (1.0e-3 * 1.0e-3 * 10000)))
        print('Flux over small WBS:      ', F_wbsS)
        print('Flux over big WBS:        ', F_wbsB)
        print('Total Flux:               ', TOTI)
        Itot.append(TOTI)
        F_sWBS.append(F_wbsS)
        F_bWBS.append(F_wbsB)
        
        
print("Total Flux: ", Itot)
print("Flux over small WBS: ", F_sWBS)
print("Flux over large WBS: ", F_bWBS)
print('FWHMx (mm): ', FWx)
print('FWHMy (mm): ', FWy)