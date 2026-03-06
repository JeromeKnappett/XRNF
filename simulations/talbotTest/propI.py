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

SX = [200,300,400,500,600,700,800,900,1000,1100,1200,1300,1400,1500] #[100,200,300,400,500,600,700,800,900,1000,1100,1200,1300,1400,1500]
# [1000,1100,1200,1300,1400,1500] #[400,500,800,900,1000]#[400,500,600,700,800,900]#,1000,1500]#[200,300,400,500]
SY = [200,300,400,500,600,700,800,900]
#[25,50,75,100,125,150,175,200,250,300,350,500,1000]

SY = SX
cff = 2.0

dirPath ='/user/home/opt/xl/xl/experiments/BEUVbeamComparison_HF/data/fixed/' 
order = ['atMask_cff1.4offset0_m1_sx' + str(x) + 'sy' + str(x) + 'FIXED' for x in SX] 
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
mePR ='IntensityDist_SE.dat' 
#'IntensityDist_SE.dat' 
#'res_int_pr_me.dat' 

justPlot = False

SAVE = False
pick = True
forStokes = False

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

Itot = []
FWx,FWy = [],[]
IG = []
IC = []
for e,t in enumerate(trials):
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
    
    numC = 1 #int(str(np.loadtxt(dirPath+t+mePR, dtype=str, comments=None, skiprows=10, max_rows=1, usecols=(0)))[1:])#[1:3]
    
    print("Resolution (x,y): {}".format((nx,ny)))
    print("xRange: {}".format(rx))
    print("xMax: {}".format(xMax))
    print("xMin: {}".format(xMin))
    print("yRange: {}".format(rx))
    print("yMax: {}".format(xMax))
    print("yMin: {}".format(xMin))
    print("Dx, Dy : {}".format((dx,dy)))
    
    
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
    
        end = time.time()
        
        plt.plot(Ex)
        plt.title('Ex')
        plt.show()
        plt.plot(Ey)
        plt.title('Ey')
        plt.show()
        print("Time taken to reshape electric field (s): ", (end-start))
        
        with open(dirPath + t+t[0:len(t)-1]+ 'EforS.pkl', "wb") as f:
                pickle.dump([Ex,Ey, nx, ny, dx, dy], f)
    
#    
#        """Copy compenents of Electric Field to Stokes structure"""
#        
#        nTot = nx*ny
#        nTotSt = nTot*4
#        nTot2 = nTot*2
#        nTot3 = nTot*3       
#        for i in range(nTot):
#            i2 = i*2
#            i2p1 = i2 + 1
#            reEx = Ex[i2]
#            imEx = Ex[i2p1]
#            reEy = Ey[i2]
#            imEy = Ey[i2p1]
#            _stokes.arS[i] = self.arEx[i2] #reEx
#            _stokes.arS[i + nTot] = self.arEx[i2p1] #imEx
#            _stokes.arS[i + nTot2] = self.arEy[i2] #reEy
#            _stokes.arS[i + nTot3] = self.arEy[i2p1] #imEy

#            nTotSt = nTot*4
#            nTot2 = nTot*2
#            nTot3 = nTot*3        
#            for i in range(nTot):
#                i2 = i*2
#                i2p1 = i2 + 1
#                reEx = self.arEx[i2]
#                imEx = self.arEx[i2p1]
#                reEy = self.arEy[i2]
#                imEy = self.arEy[i2p1]
#                intLinX = reEx*reEx + imEx*imEx
#                intLinY = reEy*reEy + imEy*imEy
#            _stokes.arS[i] = intLinX + intLinY
#            #_stokes.arS[i + nTot] = intLinX - intLinY
#            if(_n_stokes_comp > 1): _stokes.arS[i + nTot] = intLinX - intLinY #OC04052018
#            #_stokes.arS[i + nTot2] = -2*(reEx*reEy + imEx*imEy) #check sign
#            if(_n_stokes_comp > 2): _stokes.arS[i + nTot2] = 2*(reEx*reEy + imEx*imEy) #OC04052018 #check sign (in SRW for Igor: -2*(ReEX*ReEZ + ImEX*ImEZ))
#            #_stokes.arS[i + nTot3] = 2*(-reEx*reEy + imEx*imEy) #check sign
#            if(_n_stokes_comp > 3): _stokes.arS[i + nTot3] = 2*(reEx*imEy - imEx*reEy) 
    
#    plt.plot(Iflat)
#    plt.show()
          
    """ Creating array of custom tick markers for plotting """
    sF = 1e3 #e6
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
    
    if SAVE or pick:
        I = np.reshape(np.loadtxt(dirPath+t+mePR,skiprows=10), (numC,int(ny),int(nx)))   #CHANGED BY JK      # Propagated multi-electron intensity
        Iflat = I.flatten()
        
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
        
        plt.imshow(I1*I1 + I3*I3)
        plt.title('I1,I3')
        plt.show()
        plt.imshow(I2*I2 + I4*I4)
        plt.title('I2,I4')
        plt.show()
        
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
        
#        uti_plot.uti_data_file_plot(dirPath + t + mePR)
#            """Generate plot from configuration in _fname
#
#    :param str _fname: config loaded from here
#    :param bool _read_labels: whether to read labels from _fname
#    :param float _e: photon energy adjustment
#    :param float _x: horizonal position adjustment
#    :param float _y: vertical position adjustment
#    :param bool _graphs_joined: if true, all plots in a single figure
#    :param bool _multicolumn_data: if true, visualize multicolumn data data
#    :param str _column_x: column for horizontal axis
#    :param str _column_x: column for vertical axis
#    :param str _scale: the scale to use for plotting data (linear by default, but could use log, log2, log10)  
#    :param int _width_pixels: the width of the final plot in pixels  

    else:
        plt.imshow(I[0,:,:], aspect='auto')
        plt.title("Multi-electron intensity: ".format(name))
        plt.xticks(np.arange(0,int(nx)+1,int(nx)/4),tickAx)
        plt.yticks(np.arange(0,int(ny)+1,int(ny)/4),tickAy)
        plt.xlabel('x [mm]')
        plt.ylabel('y [mm]')
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
        
        # convering from ph/s/0.1%bw/mm^2 to ph/s/mm^2
        grad = 0.000396378#*0.628324754030457
        intercept = 0.019051304
        try:
            slv = (2/cff)*SY[e] #350
        except IndexError:
            slv = (2/cff)*SY
        bw = (slv*grad) + intercept
        bw = bw
        
        print('\n BW: ', bw)
        
        Ga = 50.0e-6
        

        eff = 0.04451154279639219 # cff = 2, grating E = 10% - fixed angle
        #0.027501275406876923
        #0.03935212451203237 # cff = 3, grating E = 10%
        #0.04451154279639219 # cff = 2, grating E = 10% - fixed angle
        #0.03267384491294766 # cff = 1.4, grating E = 10%
                
        # 0.03737340348858282, 0.02216367235357039, 0.004297207161730262, 0.0005147820098211518
        
        print('\n')
        print(bw)
        I = I * bw/0.1 * eff
        
        # converting from ph/s/mm^2 to ph/s
        I = (I / 1.0e-6) * (dx*dy)
        
        from FWarbValue import getFWatValue
        fwhmx,fwhmy = getFWatValue(I,frac=0.5,dx=dx,dy=dy,cuts='xy',
                                    centered=True,smoothing='gauss',
                                    verbose=False,show=True)

    
        G, C, S = IoverGrating(I, GA=Ga, dx=dy, dy=dy, show=True)
        _G, _C, _S = IoverGrating(I, GA=1.0e-3, dx=dy, dy=dy, show=True)
        
        q = 1.60218e-19
        
        
        TOTI = np.sum(I)
        Itot.append(TOTI / (ran[0]*ran[1] * 10000))
        FWx.append(fwhmx*1e3);FWy.append(fwhmy*1e3)
        IG.append((G / (4 * Ga * Ga * 10000)))
        IC.append((_C / (1.0e-3 * 1.0e-3 * 10000)))
        
# if pick:
#     with open(dirPath + 'simData_cff2.pkl', "wb") as f:
#         pickle.dump([SX,Itot,IG,IC,FWx,FWy], f)
else:
    pass
        
        
        # if gratingArea:
        #     Geuv,Ceuv,Seuv = IoverGrating(EUVtiff, GA=Ga, dx=EUVres[0], dy=EUVres[1],show=False)
        #     GeuvSE,CeuvSE,SeuvSE = IoverGrating(EUVtiff_SE, GA=Ga, dx=EUVres[0], dy=EUVres[1],show=False)
        #     Gbeuv,Cbeuv,Sbeuv = IoverGrating(BEUVtiff, GA=Ga, dx=BEUVres[0], dy=BEUVres[1],show=False)
        #     GbeuvSE,CbeuvSE,SbeuvSE = IoverGrating(BEUVtiff_SE, GA=Ga, dx=BEUVres[0], dy=BEUVres[1],show=False)
        #     GB3,CB3,SB3 = IoverGrating(B3,GA=Ga,dx=m3res[0],dy=m3res[1],show=True)
        #     GB3 = GB3  / (4 * Ga*Ga*10000)
            
        #     G135,C135,S135 = IoverGrating(tiff135, GA=Ga, dx=res135[0], dy=res135[1],show=True)
        #     G250,C250,S250 = IoverGrating(tiff250, GA=Ga, dx=res250[0], dy=res250[1],show=True)
            
        #     Ceuv = Ceuv/(Ga*Ga*10000)
        #     CeuvSE = CeuvSE/(Ga*Ga*10000)
        #     Cbeuv = Cbeuv/(Ga*Ga*10000)
        #     CbeuvSE = CbeuvSE/(Ga*Ga*10000)
            
        #     IGAeuv.append(Geuv/(4*Ga*Ga*10000)) #IsumEUV[1] + IsumEUV[2] + _IsumEUV[1] + _IsumEUV[2])
        #     IGAeuv.append(GeuvSE/(4*Ga*Ga*10000)) #IsumEUV[1] + IsumEUV[2] + _IsumEUV[1] + _IsumEUV[2])
        #     IGAbeuv.append(Gbeuv/(4*Ga*Ga*10000)) #IsumBEUV[1] + IsumBEUV[2] + _IsumBEUV[1] + _IsumBEUV[2])
        #     IGAbeuv.append(GbeuvSE/(4*Ga*Ga*10000)) #IsumBEUV[1] + IsumBEUV[2] + _IsumBEUV[1] + _IsumBEUV[2])
        #     PGAeuv.append((Geuv*q*90.44*1000)/(4*Ga*Ga*10000)) #(IsumEUV[1] + IsumEUV[2] + _IsumEUV[1] + _IsumEUV[2])*EtoJ*1000)
        #     PGAeuv.append((GeuvSE*q*90.44*1000)/(4*Ga*Ga*10000)) #(IsumEUV[1] + IsumEUV[2] + _IsumEUV[1] + _IsumEUV[2])*EtoJ*1000)
        #     PGAbeuv.append((Gbeuv*q*184.76*1000)/(4*Ga*Ga*10000))
        #     PGAbeuv.append((GbeuvSE*q*184.76*1000)/(4*Ga*Ga*10000))
            
        #     _IGA.append(G135 / (4*Ga*Ga*10000))
        #     _IGA.append(G250 / (4*Ga*Ga*10000))
    
    
plt.plot(SX,Itot,'x:')
plt.xlabel('SSA width')
plt.ylabel('Flux [ph/s]')
plt.show()
plt.plot(SX,IG,'x:')
plt.xlabel('SSA width')
plt.ylabel('I over Grating [ph/s/cm$^2$]')
plt.show()
plt.plot(SX,IC,'x:')
plt.xlabel('SSA width')
plt.ylabel('I over central 1mm^2 [ph/s/cm$^2$]')
plt.show()

print(Itot)
print(IG)
print(IC)
plt.plot(SX,FWx,'x:',label='x')
plt.plot(SX,FWy,'x:',label='y')
plt.xlabel('SSA width')
plt.ylabel('FWHM [mm]')
plt.legend()
plt.show()

print(FWx)
print(FWy)
    
#     try:
#         ix = str(np.loadtxt(dirPath + t + 'res_int_se.dat', dtype=str, comments=None, skiprows=6, max_rows=1, usecols=(0)))[1:4]#[1:3]
#         iy = str(np.loadtxt(dirPath + t + 'res_int_se.dat', dtype=str, comments=None, skiprows=9, max_rows=1, usecols=(0)))[1:4]#[1:3]
#         print("Initial resolution (x,y): {}".format((ix,iy)))
#         I0 = np.reshape(np.loadtxt(dirPath + t + 'res_int_se.dat',skiprows=10), (int(ix),int(iy)))         # Initial intensity     
#     except OSError:
#         print("No initial intensity file found...")
#     except ValueError:
#         print("Unexpected initial dimensions - Initial intensity file could not be reshaped")
#         pass
#     #try:
#     #    I = np.reshape(np.loadtxt(dirPath + 'res_int_pr_me.dat',skiprows=11), (nx,ny))          # Propagated intensity
#     #except OSError:
#     #    print("No propagated intensity file found...")
#     #except ValueError:
#     #    print("Unexpected initial dimensions - Propagated intensity file could not be reshaped")
#     #    pass
#     try:
#         cX = np.reshape(np.loadtxt(dirPath + t + 'res_int_pr_me_dcx.dat',skiprows=11), (int(nx),int(nx)))     # Horizontal coherence
#         cY = np.reshape(np.loadtxt(dirPath + t + 'res_int_pr_me_dcy.dat',skiprows=11), (int(ny),int(ny)))     # Vertical coherence    
#         dCx = np.diagonal(np.squeeze(cX))
#         dCy = np.diagonal(np.squeeze(cY))
#     except OSError:
#         print("No coherence files found...")
#     except ValueError:
#         print("Unexpected initial dimensions - Coherence files could not be reshaped")
#         pass
#     try:
#         miX = np.reshape(np.loadtxt(dirPath + t + 'res_int_pr_me_mix.dat',skiprows=11), (int(nx),int(nx),2))  # Horizontal mutual intensity
#         miY = np.reshape(np.loadtxt(dirPath + t + 'res_int_pr_me_miy.dat',skiprows=11), (int(ny),int(ny),2)) # Vertical mutual intensity
#     except OSError:
#         print("No mutual intensity files found...")
#     except ValueError:
#         print("Unexpected initial dimensions - Mutual intensity files could not be reshaped")
#         pass
    
    
    
#     """ Plotting intensity, coherence """
#     try:
#         plt.clf()
#         plt.close()
#         plt.imshow(I0)
#         plt.xticks(np.arange(0,nx+1,nx/4),tickAx)
#         plt.yticks(np.arange(0,ny+1,ny/4),tickAy)
#         plt.xlabel("position [m]") # [\u03bcm]")
#         plt.xlabel("position [m]") # [\u03bcm]")
#         plt.title("Initial intensity, : " + name)
#         plt.colorbar()
#         if SAVE == True:
#             plt.savefig(dirPath + "plots/" + "initialintensity" + name + ".png")
#             print("Saving initial intensity plot to: {}".format("plots/" + "initialintensity" +name + ".png"))
#         plt.show()
#         plt.clf()
#         plt.close()
#     except NameError:
#         print("No initial intensity file...")
#     except TypeError:
#         print("... initial intensity file may be wrong dimensions")
#         pass
    
#     try:
#         plt.clf()
#         plt.close()
#         plt.imshow(I)
#         plt.xticks(np.arange(0,nx+1,nx/4),tickAx)
#         plt.yticks(np.arange(0,ny+1,ny/4),tickAy)
#         plt.xlabel("position [m]") # [\u03bcm]")
#         plt.xlabel("position [m]") # [\u03bcm]")
#         plt.title("Intensity, e =" + name)
#         plt.colorbar()
#         if SAVE == True:
#             plt.savefig(dirPath + "plots/" + "intensity" + name + ".png")
#             print("Saving intensity plot to: {}".format("plots/" + "intensity" + name + ".png"))
#         plt.show()
#         plt.clf()
#         plt.close()
#     except NameError:
#         print("No propagated intensity file...")
#     except TypeError:
#         print("... propagated intensity file may be wrong dimensions")
#         pass
    
#     try:
#         plt.imshow(cX)
#         plt.title("Horizontal Coherence, e =" + name)
#         plt.colorbar()
#         if SAVE == True:
#             plt.savefig(dirPath + "plots/" + "coherenceHor" + name + ".png")
#             print("Saving horizontal coherence plot to: {}".format("plots/" + "coherenceHor" + name + ".png"))
#         plt.show()
#         plt.clf()
#         plt.close()
        
    
#         plt.plot(cX[:,int(int(nx)/2)], label="vertical")#, '.', markersize = 1, label="vertical")
#         plt.plot(cX[int(int(nx)/2),:], label="horizontal")#, '.', markersize = 1, label="horizontal")
#         plt.plot(np.diagonal(np.squeeze(cX)), label="diagonal")  #, '.', markersize = 1, label="diagonal")   
#         plt.plot((I[0,int(int(ny)/2),:]/np.max(I[0,int(int(ny)/2),:])), label="intensity")#, '.', markersize = 1, label="intensity")
#         plt.xticks(np.arange(0,int(nx)+1,int(nx)/4),tickAx)
#         plt.xlabel("position [m]") # [\u03bcm]")
#         plt.title("Horizontal Coherence (cuts): " + name)
#         plt.legend()
#         if SAVE == True:
#             plt.savefig(dirPath + "plots/" + "coherenceHorCuts" + name + ".png")
#             print("Saving horizontal coherence cuts plot to: {}".format("plots/" + "coherenceHorCuts" + name + ".png"))
#         plt.show()
#         plt.clf()
#         plt.close()
        
#         plt.imshow(cY)
#         plt.title("Vertical Coherence, : " + name)
#         plt.colorbar()
#         if SAVE == True:
#             plt.savefig(dirPath + "plots/" + "coherenceVer" + name + ".png")
#             print("Saving vertical coherence plot to: {}".format("plots/" + "coherenceVer" + name + ".png"))
#         plt.show()
#         plt.clf()
#         plt.close()
    
        
#         plt.plot(cY[:,int(int(ny)/2)], label="vertical")#, '.', markersize = 1, label="vertical")
#         plt.plot(cY[int(int(ny)/2),:], label="horizontal")#, '.', markersize = 1, label="horizontal")
#         plt.plot(np.diagonal(np.squeeze(cY)), label="diagonal")   #, '.', markersize = 1, label="diagonal")   
#         plt.plot((I[0,:,int(int(nx)/2)]/np.max(I[0,:,int(int(nx)/2)])), label="intensity")#, '.', markersize = 1, label="intensity")
#         plt.xticks(np.arange(0,int(ny)+1,int(ny)/4),tickAy)
#         plt.xlabel("position [m]") # [\u03bcm]")
#         plt.title("Vertical Coherence (cuts), : " + name)
#         plt.legend()
#         if SAVE == True:
#             plt.savefig(dirPath + "plots/" + "coherenceHorCuts" + name + ".png")
#             print("Saving horizontal coherence cuts plot to: {}".format("plots/" + "coherenceHorCuts" + name + ".png"))
#         plt.show()
#         plt.clf()
#         plt.close()
#     #    plt.clf()
#     #    plt.close()
# #        clX, clY = wfCoherence.getCoherenceLength(dCx, dCy, 0.7, dirPath + "plots/" + "coherenceLen" + name + ".png")
# #        print("Horizontal Coherence Length [m]: {}".format(abs(clX*dx)))
# #        print("Vertical Coherence Length [m]: {}".format(abs(clY*dy)))
# #        clx.append(abs(clX*dx))
#     #    cly.append(abs(clY*dy))
#     #    plt.clf()
#     #    plt.close()
#     except NameError:
#         print("No coherence files...")
#     except TypeError:
#         print("... coherence files may be wrong dimensions")
#         pass
    
# #    try:
# #        plt.close()
# #        plt.clf()
# #        fig, axs = plt.subplots(2, 3)
# #        axs[0,0].imshow(miX[:,:,0])
# #        axs[0,0].set_title("J - Horizontal (1)")
# #        axs[0,1].imshow(miX[:,:,1])
# #        axs[0,1].set_title("J - Horizontal (2)")
# #        axs[0,2].imshow(miX.mean(2))
# #        axs[0,2].set_title("J - Horizontal (mean)")
# #        axs[1,0].imshow(miX[:,:,0]/np.max(I))
# #        axs[1,0].set_title("J (1) - Normalised to I")
# #        axs[1,1].imshow(miX[:,:,1]/np.max(I))
# #        axs[1,1].set_title("J (2) - Normalised to I")
# #        axs[1,2].imshow(miX.mean(2)/np.max(I))
# #        axs[1,2].set_title("J (mean) - Normalised to I")
# #        if SAVE == True:
# #            print("Saving horizontal mutual intensity (J) plots to: {}".format(dirPath + "plots/" + "mutualIntensityHor" + name + ".png"))
# #            plt.savefig(dirPath + "plots/" + "mutualIntensityHor" + name + ".png")
# #        plt.show()
# #        plt.close()
# #        plt.clf()
# #            
# #        plt.close()
# #        plt.clf()
# #        fig, axs = plt.subplots(2, 3)
# #        axs[0,0].imshow(miY[:,:,0])
# #        axs[0,0].set_title("J - Vertical (1)")
# #        axs[0,1].imshow(miY[:,:,1])
# #        axs[0,1].set_title("J - Vertical (2)")
# #        axs[0,2].imshow(miY.mean(2))
# #        axs[0,2].set_title("J - Vertical (mean)")
# #        axs[1,0].imshow(miY[:,:,0]/np.max(I))
# #        axs[1,0].set_title("J (1) - Normalised to I")
# #        axs[1,1].imshow(miY[:,:,1]/np.max(I))
# #        axs[1,1].set_title("J (2) - Normalised to I")
# #        axs[1,2].imshow(miY.mean(2)/np.max(I))
# #        axs[1,2].set_title("J (mean) - Normalised to I")
# #        if SAVE == True:
# #            print("Saving vertical mutual intensity (J) plots to: {}".format(dirPath + "plots/" + "mutualIntensityVer" + name + ".png"))
# #            plt.savefig(dirPath + "plots/" + "mutualIntensityVer" + name + ".png")
# #        plt.show()
# #        plt.close()
# #        plt.clf()
# #    except NameError:
# #        print("No mutual intensity files...")
# #    except TypeError:
# #        print("... MI files may be wrong dimensions")
# #        pass