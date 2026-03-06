#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 17:16:04 2020


This is a basic example of how to handle the pickled results from a batch 
simulation (i.e. from doExperiment/runner)

@author: -
"""
import numpy as np
import matplotlib.pyplot as plt
import pickle
from matplotlib.font_manager import FontProperties
from math import log10, floor
#import wfCoherence
#import experiments.utilStokes as utilStokes
import pickle

#import xl.runner as runner

# %%
def round_sig(x, sig=2):
    if x != 0:
        return round(x, sig-int(floor(log10(abs(x))))-1)
    else:
        return x

dirPath = '/user/home/opt/xl/xl/experiments/beamPolarisation17/data/'
batchOutputFile = dirPath + '225LV/results.pickle'


trialData = ['E/', 'CL/', 'CR/', 'LD/', 'LH/', 'LV/']
# pickles = ['mt' + str(i) + '.pkl' for i in range(1240, 1256)]
    
ran = range(0,180,10)
#ran = [0,90]

folders = ['t' + str(i) + '/' for i in ran]
wfr_files = [dirPath + f + 'wf_final.hdf' for f in folders]

#wfr_files = [dirPath + str(t) + 'wf_final.hdf' for t in trialData]

print("------Starting sumWaves Function------")
#utilStokes.sumWaves(wfr_files, sampleFraction=0.5,stokes=0, norm='E',plots=dirPath + 'newplots/', savePath=dirPath+'wf_sumLinear.hdf')
#utilStokes.sumStokes(wfr_files, sampleFraction=0.1,dimensions=1,display=True,plotsPath=dirPath + 'newplots/', savePath=dirPath+'stokes_sumLinear1D.pkl')


mePR = 'res_int_pr_me.dat'

pickles = ['t' + str(i) + '.pkl' for i in ran]    # Put None to disable analysis of pickle files

fromPickles = True
fromDats = False

#data = 'res_int_pr_me.dat' 

#for p in dirPath:
#    nx = str(np.loadtxt(p + 'res_int_pr_me.dat', dtype=str, comments=None, skiprows=6, max_rows=1, usecols=(0)))[1:]#[1:3]
#    ny = str(np.loadtxt(p + 'res_int_pr_me.dat', dtype=str, comments=None, skiprows=9, max_rows=1, usecols=(0)))[1:]#[1:3]
#    print("Initial resolution (x,y): {}".format((nx,ny)))
#    I = np.reshape(np.loadtxt(p + 'res_int_pr_me.dat',skiprows=10), (int(nx),int(ny)))         # Initial intensity     
plt.clf()
plt.close()


s0x = []
s1x = []
s2x = []
s3x = []
s0y = []
s1y = []
s2y = []
s3y = []

for i, t in enumerate(folders):
    plt.clf()
    plt.close()
    name = t[0:len(str(t))-1]
    print("Analysing trial: {}".format(name))
    if fromPickles == True:
        name = str(pickles[i])[0:len(str(pickles[i]))-4]      
        print("Loading pickled wavefield")
        with open(dirPath + t + str(pickles[i]), 'rb') as f:
            r = pickle.load(f)
        nx = r['results']['params/Mesh/nx']
        xMax = r['results']['params/Mesh/xMax']
        xMin = r['results']['params/Mesh/xMin']
        rx = np.subtract(xMax,xMin)
        dx = np.divide(rx,nx)
        # resolutionX.append(dx)
        # nX.append(nx)
        ny = r['results']['params/Mesh/ny']
        yMax = r['results']['params/Mesh/yMax']
        yMin = r['results']['params/Mesh/yMin']
        ry = np.subtract(yMax,yMin)
        dy = np.divide(ry,ny)   
        # resolutionY.append(dy)
        # nY.append(ny)
    
        print("(xMin,xMax) [m]: {}".format((xMin,xMax)))
        print("x-Range [m]: {}".format(rx))
        print("(yMin,yMax) [m]: {}".format((yMin,yMax)))
        print("y-Range [m]: {}".format(ry))
        print("Dimensions (Nx,Ny) [pixels]: {}".format((nx,ny)))
        print("Resolution (dx,dy) [m]: {}".format((dx,dy)))
    
        Ix = r['results']['Intensity/Total/X/profile']
        Iy = r['results']['Intensity/Total/Y/profile']
        IxH = r['results']['Intensity/Horizontal/X/profile']
        IyH = r['results']['Intensity/Horizontal/Y/profile']
        IxV = r['results']['Intensity/Vertical/X/profile']
        IyV = r['results']['Intensity/Vertical/Y/profile']
        # Xprofiles.append(Ix)
        # Yprofiles.append(Iy)

        # plt.clf()
        # plt.close()
        # plt.plot(Ix, ':o',label='x-cut')
        # plt.title("Horizontal intensity"+ name)
        # plt.xlim(int(nx/2)-5000,int(nx/2)+5000)
        # print("Saving intensity plot to: " + dirPath + 'plots/exitIntensityX' + name + '.png')
        # plt.savefig(dirPath + 'plots/IntensityX' + name + '.png')
        # plt.show()
        
        # print(nx)
        # plt.clf()
        # plt.close()    
        # plt.plot(Iy, ':o', label='y-cut')
        # plt.title("Vertical intensity"+ name)
        # plt.xlim(int(ny/2)-5000,int(ny/2)+5000)
        # print("Saving intensity plot to: " + dirPath + 'plots/IntensityY' + name + '.png')
        # plt.savefig(dirPath + 'plots/IntensityY' + name + '.png')
        # plt.show()
        
        try:   
            cm = r['results']['Intensity/Total/contrastMichelson']
            crms = r['results']['Intensity/Total/contrastRMS']
            cmdrC = r['results']['Intensity/Total/meanDynamicRangeC']
            cmdrC1 = r['results']['Intensity/Total/meanDynamicRangeC1']
            cmdrC2 = r['results']['Intensity/Total/meanDynamicRangeC2']
            ciod = r['results']['Intensity/Total/integratedOpticalDensity']
            #cf = r['results']['Intensity/Total/contrastFourier']
            #cn = r['results']['Intensity/Total/NILS']
        except KeyError:
            print("... No contrast metrics")
        
        try:
            S0x = r['results']['stk0X']
            S1x = r['results']['stk1X']
            S2x = r['results']['stk2X']
            S3x = r['results']['stk3X']
            S0y = r['results']['stk0Y']
            S1y = r['results']['stk1Y']
            S2y = r['results']['stk2Y']
            S3y = r['results']['stk3Y']
            dPolx = r['results']['stkDpolX']
            dPoly = r['results']['stkDpolY']
            s0x.append(S0x)
            s1x.append(S1x)
            s2x.append(S2x)
            s3x.append(S3x)
            s0y.append(S0y)
            s1y.append(S1y)
            s2y.append(S2y)
            s3y.append(S3y)        
    
        except KeyError:
            print("... No 1D Stokes cuts")
            pass
            
        # cM.append(cm)
        # cRMS.append(crms)
        # cMDRC.append(cmdrC)
        # cMDRC1.append(cmdrC1)
        # cMDRC2.append(cmdrC2)
        # cIOD.append(cIOD)
        #cF.append(cf)
        #cNILS.append(cn)
        
        
        """ Creating array of custom tick markers for plotting """
        sF = 1 #e6
        tickAx = [round_sig(-rx*sF/2),
                  round_sig(-rx*sF/4),
                  0,
                  round_sig(rx*sF/4),
                  round_sig(rx*sF/2)
                  ]
        # tX.append(tickAx)
        tickAy = [round_sig(-ry*sF/2),
                  round_sig(-ry*sF/4),
                  0,
                  round_sig(ry*sF/4),
                  round_sig(ry*sF/2)]
        # tY.append(tickAy)
        
        nA = 10000        

        # TOTAL POLARISATION
        plt.clf()
        plt.close()
        plt.plot(Ix, label= 'horizontal')
        plt.plot(Iy, label= 'vertical')
        plt.title("Intensity" + name)
        plt.legend()
        plt.xticks(np.arange(0,ny+1,ny/4),tickAy)
        plt.xlabel("position [m]")
        print("Saving Intensity plot to: {}".format(dirPath + "plots/" + "Intensity" + name + ".png"))
        plt.savefig(dirPath + "plots/" + "Intensity" + name + ".png")
        plt.show()
        plt.clf()
        plt.close()
        
        plt.plot(Iy, '.')
        plt.plot(Iy, ':')
        plt.title("Aerial Image (hor-p)" + name)
        plt.xlim(int(ny/2) - nA, int(ny/2) + nA)
        plt.xticks([int(ny/2)-nA, int(ny/2)-int(nA/2), int(ny/2), int(ny/2)+int(nA/2), int(ny/2)+nA],[round_sig(-nA*dy*1e6), round_sig(-int(nA/2)*dy*1e6), 0, round_sig(int(nA/2)*dy*1e6), round_sig(nA*dy*1e6)] )
        #plt.xlim(5000,10000)
        plt.xlabel("position [\u03bcm]")
        print("Saving Aerial Image plot to: {}".format(dirPath + "plots/" + "aerialImage" + name + ".png"))
        plt.savefig(dirPath + "plots/" + "aerialImage" + name + ".png")
        plt.show()
        plt.clf()
        plt.close()    


        #plt.plot(Iy, '.')
        #plt.plot(Iy, ':')
        #plt.title("Aerial Image (hor-p)" + name)
        #plt.xlim(int(ny/2) - nA, int(ny/2) + nA)
        #plt.xticks([int(ny/2)-nA, int(ny/2)-int(nA/2), int(ny/2), int(ny/2)+int(nA/2), int(ny/2)+nA],[round_sig(-nA*dy*1e6), round_sig
#(-int(nA/2)*dy*1e6), 0, round_sig(int(nA/2)*dy*1e6), round_sig(nA*dy*1e6)] )
        #plt.xlim(25000,30000)
        #plt.xlabel("position [\u03bcm]")
        #print("Saving Aerial Image plot to: {}".format(dirPath + "plots/" + "aerialImageExit2" + name + ".png"))
        #plt.savefig(dirPath + "plots/" + "aerialImageExit2" + name + ".png")
        #plt.show()
        #plt.clf()
        #plt.close()

        
        # HORIZONTAL POLARISATION
        plt.clf()
        plt.close()
        #plt.plot(IxH, label= 'horizontal')
        plt.plot(IyH, label= 'vertical')
        plt.title("Intensity (hor-p)" + name)
        plt.legend()
        plt.xticks(np.arange(0,ny+1,ny/4),tickAy)
        plt.xlabel("position [m]")
        print("Saving Intensity plot (hor-p) to: {}".format(dirPath + "plots/" + "IntensityhorP" + name + ".png"))
        plt.savefig(dirPath + "plots/" + "IntensityhorP" + name + ".png")
        plt.show()
        plt.clf()
        plt.close()
        
        plt.plot(IyV, '.')
        plt.plot(IyV, ':')
        plt.title("Aerial Image" + name)
        plt.xlim(int(ny/2) - nA, int(ny/2) + nA)
        plt.xticks([int(ny/2)-nA, int(ny/2)-int(nA/2), int(ny/2), int(ny/2)+int(nA/2), int(ny/2)+nA],[round_sig(-nA*dy*1e6), round_sig(-int(nA/2)*dy*1e6), 0, round_sig(int(nA/2)*dy*1e6), round_sig(nA*dy*1e6)] )
        plt.xlabel("position [\u03bcm]")
        print("Saving Aerial Image (hor-p) plot to: {}".format(dirPath + "plots/" + "aerialImagehorP" + name + ".png"))
        plt.savefig(dirPath + "plots/" + "aerialImagehorP" + name + ".png")
        plt.show()
        plt.clf()
        plt.close()    
        
        # VERTICAL POLARISATION
        plt.clf()
        plt.close()
        #plt.plot(IxV, label= 'horizontal')
        plt.plot(IyV, label= 'vertical')
        plt.title("Intensity (ver-p)" + name)
        plt.legend()
        plt.xticks(np.arange(0,ny+1,ny/4),tickAy)
        plt.xlabel("position [m]")
        print("Saving Intensity (ver-p) plot to: {}".format(dirPath + "plots/" + "IntensityverP" + name + ".png"))
        plt.savefig(dirPath + "plots/" + "IntensityverP" + name + ".png")
        plt.show()
        plt.clf()
        plt.close()
        
        plt.plot(IyV, '.')
        plt.plot(IyV, ':')
        plt.title("Aerial Image (ver-p)" + name)
        plt.xlim(int(ny/2) - nA, int(ny/2) + nA)
        plt.xticks([int(ny/2)-nA, int(ny/2)-int(nA/2), int(ny/2), int(ny/2)+int(nA/2), int(ny/2)+nA],[round_sig(-nA*dy*1e6), round_sig(-int(nA/2)*dy*1e6), 0, round_sig(int(nA/2)*dy*1e6), round_sig(nA*dy*1e6)] )
        plt.xlabel("position [\u03bcm]")
        print("Saving Aerial Image (ver-p) plot to: {}".format(dirPath + "plots/" + "aerialImageverP" + name + ".png"))
        plt.savefig(dirPath + "plots/" + "aerialImageverP" + name + ".png")
        plt.show()
        plt.clf()
        plt.close()
        
        try:
            fig, axs = plt.subplots(2, 2)
            im = axs[0, 0].plot(S0y)
            axs[0, 0].set_title('S0: y-cut')
            axs[0, 1].plot(S1y)
            axs[0, 1].set_title('S1: y-cut')
            axs[1, 0].plot(S2y)
            axs[1, 0].set_title('S2: y-cut')
            axs[1, 1].plot(S3y)
            axs[1, 1].set_title('S3: y-cut')
        
            for ax in axs.flat:
                ax.set(xlabel="y position [pixels]", ylabel=" ")
            # Hide x labels and tick labels for top plots and y ticks for right plots.
            print("Saving Stokes Cuts Plots to: {}".format(dirPath + 'plots/stokesPlotsYcut' + name + '.png'))
            plt.savefig(dirPath + 'plots/stokesPlotsYcut' + name + '.png')
            plt.show()
            plt.clf()
            
            fig, axs = plt.subplots(2, 2)
            im = axs[0, 0].plot(S0x)
            axs[0, 0].set_title('S0: x-cut')
            axs[0, 1].plot(S1x)
            axs[0, 1].set_title('S1: x-cut')
            axs[1, 0].plot(S2x)
            axs[1, 0].set_title('S2: x-cut')
            axs[1, 1].plot(S3x)
            axs[1, 1].set_title('S3: x-cut')
        
            for ax in axs.flat:
                ax.set(xlabel="x position [pixels]", ylabel=" ")
            # Hide x labels and tick labels for top plots and y ticks for right plots.
            print("Saving Stokes Cuts Plots to: {}".format(dirPath + 'plots/stokesPlotsXcut' + name + '.png'))
            plt.savefig(dirPath + 'plots/stokesPlotsXcut' + name + '.png')
            plt.show()
            plt.clf()
            
            print("----- Shape of deg Pol array: {}".format(np.shape(dPolx)))
            
            fig, axs = plt.subplots(1, 2)
            axs[0].plot(dPolx)
            axs[0].set_title("Degree of Polarisation x-cut: " + name)
            axs[1].plot(dPoly)
            axs[1].set_title("Degree of Polarisation y-cut: " + name)
            print("Saving Degree of Polarisation plot to: {}".format(dirPath + "plots/DegPol" + name + ".png"))
            plt.savefig(dirPath + "plots/DegPol" + name + ".png")
            plt.show()
            plt.clf()
            plt.close()
        except NameError:
            print("No 1D stokes data file...")
        except TypeError:
            print("... 1D stokes data may be wrong dimensions")
        except IndexError:
            print("... Unexpected shape for Degree of Polarisation cuts")
            pass        
    else:
        print("Ignoring pickled wavefield")
        pass
        
    if fromDats == True:
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
        
        # Dx = Dx[0]
        # Dy = Dy[0]
        # Nx = Nx[0]
        # Ny = Ny[0]
    
        # # Defining ticks and labels for plotting
        # Xtix = [0,     int(Nx)/4, int(Nx)/2, 3*int(Nx)/4, int(Nx)]
        # Xlab = [-Dx/2, -Dx/4,     0,         Dx/4,        Dx/2]
        # Ytix = [0,     int(Ny)/4, int(Ny)/2, 3*int(Ny)/4, int(Ny)]
        # Ylab = [-Dy/2, -Dy/4,     0,         Dy/4,        Dy/2]
            
        
        if numC > 1:
            I1 = abs(I[0,:,:])
            I2 = abs(I[1,:,:])
            I3 = abs(I[2,:,:])
            I4 = abs(I[3,:,:])
        
            plt.imshow(I1)
            plt.title("I - component 1: {}".format(name))
            plt.show()
            
            fig, axs = plt.subplots(2, 2)
            #plt.clf()
            #plt.close()
            axs[0,0].imshow(I1)
            #plt.xticks(np.arange(0,float(nx)+1,float(nx)/4),tickAx)
            #plt.yticks(np.arange(0,float(ny)+1,float(ny)/4),tickAy)
            #plt.xlabel("position [m]") # [\u03bcm]")
            #plt.xlabel("position [m]") # [\u03bcm]")
            axs[0,0].set_title("C #1") #Multi-Electron Intensity")
            axs[1,0].imshow(I2)
            axs[1,0].set_title("C #2")
            axs[0,1].imshow(I3)
            axs[0,1].set_title("C #3")
            axs[1,1].imshow(I4)
            axs[1,1].set_title("C #4")
            #plt.colorbar()
            plt.savefig(dirPath + "plots/" + "intensity" + name + ".png")
            print("Saving intensity plot to: {}".format("plots/" + "intensity" + name + ".png"))
            plt.show()
            plt.clf()
            plt.close()
        else:
            plt.imshow(I[0,:,:])
            plt.title("Multi-electron intensity: {}".format(name))
            plt.colorbar()
            plt.show()
        
        
        
        
        
        try:
            print("Getting Initial Intensity...")
            ix = str(np.loadtxt(dirPath + t + 'res_int_se.dat', dtype=str, comments=None, skiprows=6, max_rows=1, usecols=(0)))[1:4]#[1:3]
            iy = str(np.loadtxt(dirPath + t + 'res_int_se.dat', dtype=str, comments=None, skiprows=9, max_rows=1, usecols=(0)))[1:4]#[1:3]
            print("Initial resolution (x,y): {}".format((ix,iy)))
            I0 = np.reshape(np.loadtxt(dirPath + t + 'res_int_se.dat',skiprows=10), (int(ix),int(iy)))         # Initial intensity     
        except OSError:
            print("No initial intensity file found...")
        except ValueError:
            print("Unexpected initial dimensions - Initial intensity file could not be reshaped")
            pass
        try:
            Im = np.reshape(np.loadtxt(dirPath + 'res_int_pr_me.dat',skiprows=11), (nx,ny))          # Propagated intensity
        except OSError:
            print("No propagated me-intensity file found...")
        except ValueError:
            print("Unexpected initial dimensions - Propagated intensity file could not be reshaped")
            pass
        try:
            Is = np.reshape(np.loadtxt(dirPath + 'res_int_pr_se.dat',skiprows=11), (nx,ny))          # Propagated intensity
        except OSError:
            print("No propagated se-intensity file found...")
        except ValueError:
            print("Unexpected initial dimensions - Propagated intensity file could not be reshaped")
            pass
        try:
            print("Getting Horizontal and Vertical Coherence...")
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
            print("Getting Horizontal and Vertical Mutual Intensity...")
            miX = np.reshape(np.loadtxt(dirPath + t + 'res_int_pr_me_mix.dat',skiprows=11), (int(nx),int(nx),2))  # Horizontal mutual intensity
            miY = np.reshape(np.loadtxt(dirPath + t + 'res_int_pr_me_miy.dat',skiprows=11), (int(ny),int(ny),2)) # Vertical mutual intensity
        except OSError:
            print("No mutual intensity files found...")
        except ValueError:
            print("Unexpected initial dimensions - Mutual intensity files could not be reshaped")
            pass
        
        
        
        """ Plotting intensity, coherence """
        print(" ")
        print("----- Plotting -----")
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
            plt.savefig(dirPath + "plots/" + "initialintensity" + name + ".png")
            print("Saving initial intensity plot to: {}".format("plots/" + "initialintensity" + name + ".png"))
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
            plt.imshow(Is)
            plt.xticks(np.arange(0,nx+1,nx/4),tickAx)
            plt.yticks(np.arange(0,ny+1,ny/4),tickAy)
            plt.xlabel("position [m]") # [\u03bcm]")
            plt.xlabel("position [m]") # [\u03bcm]")
            plt.title("Intensity, s.e : " + name)
            plt.colorbar()
            plt.savefig(dirPath + "plots/" + "intensity-se" + name + ".png")
            print("Saving intensity plot to: {}".format("plots/" + "intensity-se" + name + ".png"))
            plt.show()
            plt.clf()
            plt.close()
        except NameError:
            print("No propagated se-intensity file...")
        except TypeError:
            print("... propagated se-intensity file may be wrong dimensions")
            pass
                
        try:
            plt.clf()
            plt.close()
            plt.imshow(Im)
            plt.xticks(np.arange(0,nx+1,nx/4),tickAx)
            plt.yticks(np.arange(0,ny+1,ny/4),tickAy)
            plt.xlabel("position [m]") # [\u03bcm]")
            plt.xlabel("position [m]") # [\u03bcm]")
            plt.title("Intensity, m.e :" + name)
            plt.colorbar()
            plt.savefig(dirPath + "plots/" + "intensity-me" + name + ".png")
            print("Saving intensity plot to: {}".format("plots/" + "intensity-me" + name + ".png"))
            plt.show()
            plt.clf()
            plt.close()
        except NameError:
            print("No propagated me-intensity file...")
        except TypeError:
            print("... propagated me-intensity file may be wrong dimensions")
            pass
        
        try:
            plt.imshow(cX)
            plt.title("Horizontal Coherence, e =" + name)
            plt.colorbar()
            plt.savefig(dirPath + "plots/" + "coherenceHor" + name + ".png")
            print("Saving horizontal coherence plot to: {}".format("plots/" + "coherenceHor" + name + ".png"))
            plt.show()
            plt.clf()
            plt.close()
            
        
            plt.plot(cX[:,int(int(nx)/2)], label="vertical")#, '.', markersize = 1, label="vertical")
            plt.plot(cX[int(int(nx)/2),:], label="horizontal")#, '.', markersize = 1, label="horizontal")
            plt.plot(np.diagonal(np.squeeze(cX)), label="diagonal")  #, '.', markersize = 1, label="diagonal")   
            plt.plot(np.diagonal(np.fliplr(cX)), label='diagonal flipped')
            plt.plot((I[0,int(int(ny)/2),:]/np.max(I[0,int(int(ny)/2),:])), label="intensity")#, '.', markersize = 1, label="intensity")
            plt.xticks(np.arange(0,int(nx)+1,int(nx)/4),tickAx)
            plt.xlabel("position [m]") # [\u03bcm]")
            plt.title("Horizontal Coherence (cuts): " + name)
            plt.legend()
            plt.savefig(dirPath + "plots/" + "coherenceHorCuts" + name + ".png")
            print("Saving horizontal coherence cuts plot to: {}".format("plots/" + "coherenceHorCuts" + name + ".png"))
            plt.show()
            plt.clf()
            plt.close()
            
            plt.imshow(cY)
            plt.title("Vertical Coherence, : " + name)
            plt.colorbar()
            plt.savefig(dirPath + "plots/" + "coherenceVer" + name + ".png")
            print("Saving vertical coherence plot to: {}".format("plots/" + "coherenceVer" + name + ".png"))
            plt.show()
            plt.clf()
            plt.close()
        
            
            plt.plot(cY[:,int(int(ny)/2)], label="vertical")#, '.', markersize = 1, label="vertical")
            plt.plot(cY[int(int(ny)/2),:], label="horizontal")#, '.', markersize = 1, label="horizontal")
            plt.plot(np.diagonal(np.squeeze(cY)), label="diagonal")   #, '.', markersize = 1, label="diagonal")   
            plt.plot(np.diagonal(np.fliplr(cY)), label='diagonal flipped')
            plt.plot((I[0,:,int(int(nx)/2)]/np.max(I[0,:,int(int(nx)/2)])), label="intensity")#, '.', markersize = 1, label="intensity")
            plt.xticks(np.arange(0,int(ny)+1,int(ny)/4),tickAy)
            plt.xlabel("position [m]") # [\u03bcm]")
            plt.title("Vertical Coherence (cuts), : " + name)
            plt.legend()
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
    else:
        pass
    
    
# Summing stokes and plotting
S0X = sum(s0x)
S1X = sum(s1x)
S2X = sum(s2x)
S3X = sum(s3x)
S0Y = sum(s0y)
S1Y = sum(s1y)
S2Y = sum(s2y)
S3Y = sum(s3y)

plt.clf()
plt.close()
fig, axs = plt.subplots(2, 2)
im = axs[0, 0].plot(S0Y)
axs[0, 0].set_title('FINAL S0: y-cut')
axs[0, 1].plot(S1Y)
axs[0, 1].set_title('FINAL S1: y-cut')
axs[1, 0].plot(S2Y)
axs[1, 0].set_title('FINAL S2: y-cut')
axs[1, 1].plot(S3Y)
axs[1, 1].set_title('FINAL S3: y-cut')

for ax in axs.flat:
    ax.set(xlabel="y position [pixels]", ylabel=" ")
# Hide x labels and tick labels for top plots and y ticks for right plots.
print("Saving Stokes Cuts Plots to: {}".format(dirPath + 'plots/stokesPlotsFinalYcut' + str(pickles[0])[0:len(str(pickles))-3] + '.png'))
plt.savefig(dirPath + 'plots/stokesPlotsFinalYcut' + str(pickles[0])[0:len(str(pickles[0]))-3] + '.png')
plt.show()
plt.clf()

fig, axs = plt.subplots(2, 2)
im = axs[0, 0].plot(S0X)
axs[0, 0].set_title('FINAL S0: x-cut')
axs[0, 1].plot(S1X)
axs[0, 1].set_title('FINAL S1: x-cut')
axs[1, 0].plot(S2X)
axs[1, 0].set_title('FINAL S2: x-cut')
axs[1, 1].plot(S3X)
axs[1, 1].set_title('FINAL S3: x-cut')
for ax in axs.flat:
    ax.set(xlabel="x position [pixels]", ylabel=" ")
# Hide x labels and tick labels for top plots and y ticks for right plots.
print("Saving Stokes Cuts Plots to: {}".format(dirPath + 'plots/stokesPlotsFinalXcut' + str(pickles[0])[0:len(str(pickles[0]))-3] + '.png'))
plt.savefig(dirPath + 'plots/stokesPlotsFinalXcut' + str(pickles[0])[0:len(str(pickles[0]))-3] + '.png')
plt.show()

plt.clf()



sPolX = np.sqrt(S1X**2 + S2X**2 + S3X**2)
sPolY = np.sqrt(S1Y**2 + S2Y**2 + S3Y**2)
sUnPolX = S0X - sPolX
sUnPolY = S0Y - sPolY
dPolX = sPolX/S0X
dPolY = sPolY/S0Y

fig, axs = plt.subplots(1,2)
axs[0].plot(sPolX, label='x-cut')
axs[0].plot(sPolY, label='y-cut')
axs[0].legend()
axs[0].set_title('Polarised Component')
axs[1].plot(sUnPolX, label='x-cut')
axs[1].plot(sUnPolY, label='y-cut')
axs[1].legend()
axs[1].set_title('Unpolarised Component')
plt.savefig(dirPath + 'plots/polarComponents' + str(pickles[0])[0:len(str(pickles[0]))-3] + '.png')
plt.show()

plt.clf()
plt.close()
plt.plot(dPolX, label='x-cut')
plt.plot(dPolY, label='y-cut')
plt.legend()
plt.title("Degree of Polarisation")
plt.savefig(dirPath + 'plots/degPolFinal' + str(pickles[0])[0:len(str(pickles[0]))-3] + '.png')
plt.show()
plt.clf()
plt.close()
    
    
    



def trials(results):
        return [k for k,v in results.items()]
       
def resultsKeys(results):
        return [k for k,v  in results['trial_0']['results'].items()]
    
def parameterKeys(results):
        return [k for k,v  in results['trial_0']['parameters'].items()]

    
def listValues(results, key):
        try:
            V =  [results[trial]['results'][key] for trial in trials(results)] 
        except KeyError:
            try:
                V =  [results[trial]['parameters'][key] for trial in trials(results)] 
            except KeyError:
                print('Valid values not found for ' + key)
                V=[]
        
        return V
    
def plot(results,*args,**kwargs):
                
        xKey = kwargs['x']
        yKey = kwargs['y']
            
        x = listValues(results,xKey)
        y = listValues(results,yKey)
               
        if x !=[] and y!=[]:
            fontP = FontProperties()
            fontP.set_size('xx-small')    
            plt.plot(x,y,'o')   #label=...
            plt.xlabel(xKey)
            plt.ylabel(yKey)
            plt.legend(loc='upper left', bbox_to_anchor=(1, 0.5), prop=fontP)
            plt.show()   
    



