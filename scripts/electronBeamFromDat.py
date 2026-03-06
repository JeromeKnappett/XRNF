#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 23 13:10:09 2024

@author: jerome
"""



import numpy as np
import matplotlib.pyplot as plt
import pylab
from math import log10, floor
# import imageio

def round_sig(x, sig=2):
    if x != 0:
        return round(x, sig-int(floor(log10(abs(x))))-1)
    else:
        return x



pylab.rcParams['figure.figsize'] = (4.1, 4.0)
colours = plt.rcParams["axes.prop_cycle"].by_key()["color"]

dirPath = '/home/jerome/Documents/PhD/Data/185/'
E = 185
B = 0.4605
eX,eY = 10e-9, 0.009e-9 # emittance in x,y
##0.453
##0.4571
##0.4605
#
#plot = 'cuts'
##'both'
##'2d'
##'cuts'
fitGauss = True

savePath = dirPath + 'electronBeam.eps'# + str(B) + '.eps'


C = [colours[3],colours[0]]

#showParams = False
#WBSlines = True
#
#wbsX, wbsY = [0.84,4],[1,3]

numXticks = 5
numYticks = 5
fSize = 15



#print(f"Element number:                      {e}")
## print(f"Intensity data file: {dirPath + 'res_int_pr_se.dat'}")
#if e ==0:
#print(f"Plane:                               {'WBS incident'}")

# Reading .dat file and extracting values
filename = 'res_trj.dat'
#else:
#    print(f"Plane:                               {'Final'}")
#    filename = 'res_int_pr_se.dat'

D = np.loadtxt(dirPath + filename, dtype=str, comments=None, skiprows=1)
X = np.array(D[:, 1], dtype="float")
betaX = np.array(D[:, 2], dtype="float")
Y = np.array(D[:, 3], dtype="float")
betaY = np.array(D[:, 4], dtype="float")

plt.scatter([x*1e6 for x in X],[eX/b for b in betaX])
plt.show()
plt.scatter(Y,betaY)
plt.show()



#
#X = np.linspace(float(xMin)*1e3,float(xMax)*1e3,int(nx))
#Y = np.linspace(float(yMin)*1e3,float(yMax)*1e3,int(ny))
#if plot == '2d':
#    # ploting 2d intensity
#    plt.imshow(I,aspect='auto',cmap='gray')
#    # plt.title('WBS incident : 14.3 m propagation',fontsize=fSize)
#    plt.xticks([int((float(nx)-1.0)*(a/(numXticks-1.0))) for a in range(numXticks)], [round_sig(float(nx)*dx*(b/(numXticks-1.0))*1e3) for b in range(-int((numXticks-1.0)/2.0),int((numXticks/2.0 + 1.0)))],fontsize=fSize)
#    plt.yticks([int((float(ny)-1.0)*(a/(numYticks-1.0))) for a in range(numYticks)], [round_sig(float(ny)*dy*(b/(numYticks-1.0))*1e3) for b in range(-int((numYticks-1.0)/2.0),int((numYticks/2.0 + 1.0)))],fontsize=fSize)
#    plt.xlabel('x-position [mm]',fontsize=fSize)
#    plt.ylabel('y-position [mm]',fontsize=fSize)
#    # plt.colorbar(label='Intensity [$ph/s/.1\%bw$]',labelsize=fSize)
#    plt.colorbar().set_label(label='Intensity [ph/s/.1\%bw/mm$^2$]',size=fSize)
#    
#    if showParams:
#        plt.text(int(nx)-int((1*int(nx))/5),int(ny)-int((4*int(ny))/20),f"nx: {int(nx)}", color='r',fontsize=fSize)
#        plt.text(int(nx)-int((1*int(nx))/5),int(ny)-int((3*int(ny))/20),f"ny: {int(ny)}", color='r',fontsize=fSize)
#        plt.text(int(nx)-int((1*int(nx))/5),int(ny)-int((2*int(ny))/20),f"dx: {float(dx)} m", color='r',fontsize=fSize)
#        plt.text(int(nx)-int((1*int(nx))/5),int(ny)-int((1*int(ny))/20),f"dy: {float(dy)} m", color='r',fontsize=fSize)
#    else:
#        pass
#    plt.show()
#
#if plot == 'cuts':
#    
#    Ix = I[int(ny)//2,:]
#    Iy = I[:,int(nx)//2]
#    
#    
#    
#    # ploting 1d intensity profiles
#    plt.plot(X,Ix,color=colours[5])
#    #plt.xticks([int((float(nx)-1.0)*(a/(numXticks-1.0))) for a in range(numXticks)], [round_sig(float(nx)*dx*(b/(numXticks-1.0))*1e3) for b in range(-int((numXticks-1.0)/2.0),int((numXticks/2.0 + 1.0)))],fontsize=fSize)
#    plt.xlabel('x-position [mm]')
#    plt.ylabel('Intensity [ph/s/.1\%bw/mm$^2$]')
#    if WBSlines:
#        for lx,ly,c in zip(wbsX,wbsY,C):
#            plt.axvline(x=-lx/2,color=c,linestyle=':',label='WBS=' + str(lx) + r'$\times$' + str(ly) + ' mm$^2$')
#            plt.axvline(x=lx/2,color=c,linestyle=':')
#    plt.legend(frameon=True,fancybox=True,framealpha=1.0,fontsize=5)
#    
#    if fitGauss:
#        G = (np.max(I)) * np.exp(-(X**2) / (2 * (14.3**2) * ((0.053)**2)))
#        plt.plot(X,G,':g')
#    
#    plt.show()
#    
#    plt.plot(Y,Iy,color=colours[5])
#    #plt.xticks([int((float(ny)-1.0)*(a/(numYticks-1.0))) for a in range(numYticks)], [round_sig(float(ny)*dy*(b/(numYticks-1.0))*1e3) for b in range(-int((numYticks-1.0)/2.0),int((numYticks/2.0 + 1.0)))],fontsize=fSize)
#    plt.xlabel('y-position [mm]')
#    plt.ylabel('Intensity [ph/s/.1\%bw/mm$^2$]')
#    if WBSlines:
#        for lx,ly,c in zip(wbsX,wbsY,C):
#            plt.axvline(x=-ly/2,color=c,linestyle=':',label='WBS=' + str(lx) + r'$\times$' + str(ly) + ' mm$^2$')
#            plt.axvline(x=ly/2,color=c,linestyle=':')
#    plt.legend(frameon=True,fancybox=True,framealpha=1.0,fontsize=5)
#    
#    if fitGauss:
#        G = (np.max(I)) * np.exp(-(Y**2) / (2 * (14.3**2) * ((0.055)**2)))
#        plt.plot(X,G,':g')
#    
#    plt.show()    