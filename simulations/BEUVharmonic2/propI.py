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

#plt.style.use(['science','no-latex']) # 'ieee', 
pylab.rcParams['figure.figsize'] = (10.0, 8.0)

def round_sig(x, sig=2):
    if x != 0:
        return round(x, sig-int(floor(log10(abs(x))))-1)
    else:
        return x

dirPath ='/user/home/opt/xl/xl/experiments/BEUVharmonic2/data/'  #'/user/home/opt/xl/xl/experiments/fullbeamPolarisation/'#'/user/home/opt/xl/xl/experiments/beamCoherence2/data/' 

trials =['atMask_ME/']#,'m3_atMask_ME/','m5_atMask_ME/','m7_atMask_ME/','m9_atMask_ME/']#'fixed/','m7_atMask_MEfixed/','m9_atMask_MEfixed/']#,'150um/']#,'beforeBDA_efield_sx200/','beforeBDA_efield_sx500/'] #['data/'] #['fullRes_5000e/', 'fullRes_100e/'] #['120_1000x1000/']#'200e/','10000e/', '120e_250ir/']
mePR = 'res_int_pr_me.dat'

justPlot = False

SAVE = True
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
    
    try:
        plt.imshow(cX)
        plt.title("Horizontal Coherence, e =" + name)
        plt.colorbar()
        if SAVE == True:
            plt.savefig(dirPath + "plots/" + "coherenceHor" + name + ".png")
            print("Saving horizontal coherence plot to: {}".format("plots/" + "coherenceHor" + name + ".png"))
        plt.show()
        plt.clf()
        plt.close()
        
    
        plt.plot(cX[:,int(int(nx)/2)], label="vertical")#, '.', markersize = 1, label="vertical")
        plt.plot(cX[int(int(nx)/2),:], label="horizontal")#, '.', markersize = 1, label="horizontal")
        plt.plot(np.diagonal(np.squeeze(cX)), label="diagonal")  #, '.', markersize = 1, label="diagonal")   
        plt.plot((I[0,int(int(ny)/2),:]/np.max(I[0,int(int(ny)/2),:])), label="intensity")#, '.', markersize = 1, label="intensity")
        plt.xticks(np.arange(0,int(nx)+1,int(nx)/4),tickAx)
        plt.xlabel("position [m]") # [\u03bcm]")
        plt.title("Horizontal Coherence (cuts): " + name)
        plt.legend()
        if SAVE == True:
            plt.savefig(dirPath + "plots/" + "coherenceHorCuts" + name + ".png")
            print("Saving horizontal coherence cuts plot to: {}".format("plots/" + "coherenceHorCuts" + name + ".png"))
        plt.show()
        plt.clf()
        plt.close()
        
        plt.imshow(cY)
        plt.title("Vertical Coherence, : " + name)
        plt.colorbar()
        if SAVE == True:
            plt.savefig(dirPath + "plots/" + "coherenceVer" + name + ".png")
            print("Saving vertical coherence plot to: {}".format("plots/" + "coherenceVer" + name + ".png"))
        plt.show()
        plt.clf()
        plt.close()
    
        
        plt.plot(cY[:,int(int(ny)/2)], label="vertical")#, '.', markersize = 1, label="vertical")
        plt.plot(cY[int(int(ny)/2),:], label="horizontal")#, '.', markersize = 1, label="horizontal")
        plt.plot(np.diagonal(np.squeeze(cY)), label="diagonal")   #, '.', markersize = 1, label="diagonal")   
        plt.plot((I[0,:,int(int(nx)/2)]/np.max(I[0,:,int(int(nx)/2)])), label="intensity")#, '.', markersize = 1, label="intensity")
        plt.xticks(np.arange(0,int(ny)+1,int(ny)/4),tickAy)
        plt.xlabel("position [m]") # [\u03bcm]")
        plt.title("Vertical Coherence (cuts), : " + name)
        plt.legend()
        if SAVE == True:
            plt.savefig(dirPath + "plots/" + "coherenceHorCuts" + name + ".png")
            print("Saving horizontal coherence cuts plot to: {}".format("plots/" + "coherenceHorCuts" + name + ".png"))
        plt.show()
        plt.clf()
        plt.close()
    #    plt.clf()
    #    plt.close()
#        clX, clY = wfCoherence.getCoherenceLength(dCx, dCy, 0.7, dirPath + "plots/" + "coherenceLen" + name + ".png")
#        print("Horizontal Coherence Length [m]: {}".format(abs(clX*dx)))
#        print("Vertical Coherence Length [m]: {}".format(abs(clY*dy)))
#        clx.append(abs(clX*dx))
    #    cly.append(abs(clY*dy))
    #    plt.clf()
    #    plt.close()
    except NameError:
        print("No coherence files...")
    except TypeError:
        print("... coherence files may be wrong dimensions")
        pass
    
    try:
        plt.close()
        plt.clf()
        fig, axs = plt.subplots(2, 3)
        axs[0,0].imshow(miX[:,:,0])
        axs[0,0].set_title("J - Horizontal (1)")
        axs[0,1].imshow(miX[:,:,1])
        axs[0,1].set_title("J - Horizontal (2)")
        axs[0,2].imshow(miX.mean(2))
        axs[0,2].set_title("J - Horizontal (mean)")
        axs[1,0].imshow(miX[:,:,0]/np.max(I))
        axs[1,0].set_title("J (1) - Normalised to I")
        axs[1,1].imshow(miX[:,:,1]/np.max(I))
        axs[1,1].set_title("J (2) - Normalised to I")
        axs[1,2].imshow(miX.mean(2)/np.max(I))
        axs[1,2].set_title("J (mean) - Normalised to I")
        if SAVE == True:
            print("Saving horizontal mutual intensity (J) plots to: {}".format(dirPath + "plots/" + "mutualIntensityHor" + name + ".png"))
            plt.savefig(dirPath + "plots/" + "mutualIntensityHor" + name + ".png")
        plt.show()
        plt.close()
        plt.clf()
            
        plt.close()
        plt.clf()
        fig, axs = plt.subplots(2, 3)
        axs[0,0].imshow(miY[:,:,0])
        axs[0,0].set_title("J - Vertical (1)")
        axs[0,1].imshow(miY[:,:,1])
        axs[0,1].set_title("J - Vertical (2)")
        axs[0,2].imshow(miY.mean(2))
        axs[0,2].set_title("J - Vertical (mean)")
        axs[1,0].imshow(miY[:,:,0]/np.max(I))
        axs[1,0].set_title("J (1) - Normalised to I")
        axs[1,1].imshow(miY[:,:,1]/np.max(I))
        axs[1,1].set_title("J (2) - Normalised to I")
        axs[1,2].imshow(miY.mean(2)/np.max(I))
        axs[1,2].set_title("J (mean) - Normalised to I")
        if SAVE == True:
            print("Saving vertical mutual intensity (J) plots to: {}".format(dirPath + "plots/" + "mutualIntensityVer" + name + ".png"))
            plt.savefig(dirPath + "plots/" + "mutualIntensityVer" + name + ".png")
        plt.show()
        plt.close()
        plt.clf()
    except NameError:
        print("No mutual intensity files...")
    except TypeError:
        print("... MI files may be wrong dimensions")
        pass