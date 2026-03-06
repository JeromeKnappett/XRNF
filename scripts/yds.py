#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  1 09:53:28 2021

@author: jerome
"""
import numpy as np
import imageio
import matplotlib.pyplot as plt
import scipy.ndimage
from scipy import signal

from scipy.ndimage import gaussian_filter
import random

import time


def makeYDS(nx,ny,xdim,ydim,sSep,sWidth,sLen,rotation,path=None):
    
    
    if sSep >= xdim-sWidth:
        print("ERROR")
        print("Slit separation too great, increase dimensions")
        return None
    
    print(" ")
    print("----- Creating YDS -----")
    
    start = time.time()
    rX = xdim/nx   # x resolution [m]
    rY = ydim/ny   # y resolution [m]
    r = sSep/rX    # slit separation in pixels
    l = sLen/rY    # slit length in pixels
    w = sWidth/rX  # slit width in pixels
    
    # defining slits
    sLoc1_x1 = nx/2 - r/2 - w/2
    sLoc1_x2 = nx/2 - r/2 + w/2
    sLoc2_x1 = nx/2 + r/2 - w/2
    sLoc2_x2 = nx/2 + r/2 + w/2
    
    sLocX = np.array([sLoc1_x1, sLoc1_x2, sLoc2_x1 , sLoc2_x2])
    
    sLoc1y = ny/2 - l/2
    sLoc2y = ny/2 + l/2
    
    sLocY = np.array([sLoc1y,sLoc2y])
    
    # Making sure slits are defined only at integer pixel values   
    if all(x == int for x in sLocX):
        pass
    else:
        sLocX = np.rint(sLocX).astype(int) 
        # print(" ")
        # print("!!!WARNING!!!")
        # print("Slit separation is not an integer value of pixels, allignment may be affected.")
        # print(" ")    
        
    if all(y == int for y in sLocY):
        pass
    else:
        sLocY = np.rint(sLocY).astype(int)
        # print(" ")
        # print("!!!WARNING!!!")
        # print("Slit length is not an integer value of pixels, allignment may be affected.")
        # print(" ")
    
    # print("Slit separation [pixels]: {}".format(r))
    # print("Slit #1 location [pixels] again: {}".format((sLoc1_x1,sLoc1_x2)))
    # print("Slit #2 location [pixels] again: {}".format((sLoc2_x1,sLoc2_x2)))
    # print("Shape of sLocX: {}".format(np.shape(sLocX)))
    # print("Slit #1 location [pixels] array: {}".format((sLocX[0],sLocX[1])))
    # print("Slit #2 location [pixels] array: {}".format((sLocX[2],sLocX[3])))
    # print("sLocX: {}".format(sLocX))
    
    # Creating empty array
    mesh = np.zeros([nx,ny])

    # Setting slits value to 255    
    mesh[sLocX[0]:sLocX[1],sLocY[0]:sLocY[1]] = 255
    mesh[sLocX[2]:sLocX[3],sLocY[0]:sLocY[1]] = 255
    
    # rotating array as desired
    mesh = scipy.ndimage.rotate(mesh,rotation)
    
    # showing slit before convolution
    pad = 4
    if rotation == 0:
        plt.imshow(mesh[sLocX[0]-pad:sLocX[1]+pad,sLocY[0]-pad:sLocY[1]+pad])
    else:
        plt.imshow(scipy.ndimage.rotate(mesh,360-rotation)[sLocX[0]-pad:sLocX[1]+pad,sLocY[0]-pad:sLocY[1]+pad])
    
    plt.title("Slit (before convolution)")
    plt.show()
    plt.clf()
    plt.close()    
    
    end = time.time()
    print("Time taken to create YDS...  {} seconds".format(end-start))
    print("shape of YDS: {}".format(np.shape(mesh)))
    
    
    # convolving with gaussian
    print("----- Convolving with Gaussian -----")
    start1 = time.time()
#    fwhm = sigma * np.sqrt(8 * np.log(2)) = 3*nx
#    sigma = (3*nx)/(np.sqrt(8 * np.log(2)))
    
    sigma =2/3 # rX/(2*np.sqrt(8*np.log(2))) #(1/6)*((nx*3)+1) #rX/(2*np.sqrt(8*np.log(2)))
#    G = gauss2D(nx,ny,mu=0,sigma=sigma)
    mesh = gaussian_filter(mesh, sigma=sigma)
#    print("shape of G: {}".format(np.shape(G)))
#    mesh = scipy.signal.convolve2d(np.array(mesh),np.array(G))
    end1 = time.time()
    print("Time taken to convolve with gaussian...  {} seconds".format(end1-start1))
    
    # showing slit after convolution    
    if rotation == 0:
        plt.imshow(mesh[sLocX[0]-pad:sLocX[1]+pad,sLocY[0]-pad:sLocY[1]+pad])
    else:
        plt.imshow(scipy.ndimage.rotate(mesh,360-rotation)[sLocX[0]-pad:sLocX[1]+pad,sLocY[0]-pad:sLocY[1]+pad])
    plt.title("Slit (after convolution)")
    plt.show()
    
    if rotation != 0:
        print("New shape of YDS after rotation: {}".format(np.shape(mesh)))
        nx = np.shape(mesh)[0]
        ny = np.shape(mesh)[1]
        rX = xdim/nx
        rY = ydim/ny
        print("New resolution of YDS after rotation (x,y) [m]: {}".format((rX,rY)))
    
    plt.imshow(mesh)
    plt.title("YDS")
    plt.xticks([0, int(nx/4), int(nx/2), int(3*nx/4), nx],[-xdim/2, -xdim/4, 0, xdim/4, xdim/2])
    plt.yticks([0, ny/4, ny/2, 3*ny/4, ny],[-ydim/2, -ydim/4, 0, ydim/4, ydim/2])
    plt.show()
    
    
    if path != None:
        imageio.imwrite(path,np.uint8(mesh))
        print("YDS written to: {}".format(path))
        
    
    # Show YDS dimensions
    print("Pixels (x,y): {}".format((nx,ny)))
    print("Dimensions (x,y) [m]: {}".format((xdim,ydim)))
    print("Resolution (x,y) [m]: {}".format((rX,rY)))
    print("Slit Separation [m]: {}".format(sSep))
    print("Slit Width [m]: {}".format(sWidth))
    print("Slit Length [m]: {}".format(sLen))
    
    return rX,rY,nx,ny

def testYDS():
    
    nX = 7500    # number of pixels in x
    nY = 7500    # number of pixels in y
    xDim = 150e-6 # size in x
    yDim = 150e-6 # size in y
    sSep = 20e-6  # slit separation
    sW = 1.0e-6   # slit width
    sL = 100e-6   # slit length
    rot = 0       # rotation angle
    
    numRots = 2   # number of rotations
    numSeps = 1   # number of slit separations
    theta = np.linspace(0,90,numRots)      # angles
    sep = np.linspace(50e-6,50e-6,numSeps) # separations
    
    # path to save tiff file
    path = '/user/home/opt/xl/xl/experiments/masks/testYDS'
    
    for n, s in zip(range(numSeps), sep):
        Rx = []
        Ry = []
        Nx = []
        Ny = []
        print(" ")
        print("----- Creating mask #{} ----- ".format(n+1))
        print("Slit separation: {} microns".format(s*1e6))
        for i, t in zip(range(numRots),theta):
            print(" ")
            print("Rotation #{}: {} degrees".format(int(i+1),t))
            p = str(path+'s' + str(int(np.rint(s*1e6))) + 't' + str(int(t)) + '.tif') # save path
            print("Save path: {}".format(p))
            
            print("xDim:       {}".format(xDim))
            print("slit width: {}".format(sW))
            print("Separation: {}".format(s))

            print("t = {}".format(t))
            rx, ry, nx, ny = makeYDS(nX,nY,xDim,yDim,s,sW,sL,t,path=p)
            
            Rx.append(rx)
            Ry.append(ry)
            Nx.append(nx)
            Ny.append(ny)
        
        #if numRots >= 2:
        #    plt.plot(theta,Rx, label ="rx")
        #    plt.plot(theta,Ry, label="ry")
        #    # plt.plot(theta,nY, label="ny")
        #    plt.title("Slit separation: " + str(s*1e6) + " microns")
        #    plt.xlabel("rotation (degrees)")
        #    plt.ylabel("pixel size (m)")
        #    plt.legend()
        #    plt.show()
        #    
        #    plt.plot(theta,Nx, label ="nx")
        #    plt.plot(theta,Ny, label="ny")
        #    plt.title("Slit separation: " + str(s*1e6) + " microns")
        #    plt.xlabel("rotation (degrees)")
        #    plt.ylabel("pixels")
        #    plt.legend()
        #    plt.show()
            

    
    # for x,L,c in zip(inB,range(numCorrLengths),c_length):
    #     for i in Rh:
        
def testGauss():
    nx = 100
    ny = 100
    mu = 0
    sigma = 1
    G = gauss2D(nx,ny,mu,sigma)
    
    

def gauss2D(nx,ny, mu, sigma):
    # Initializing value of x-axis and y-axis
    # in the range -1 to 1
    x, y = np.meshgrid(np.linspace(-1,1,nx), np.linspace(-1,1,ny))
    dst = np.sqrt(x*x+y*y)
  
    # Calculating Gaussian array
    gauss = np.array(np.exp(-( (dst-mu)**2 / ( 2.0 * sigma**2 ) ) ))
  
    kernel = 6*sigma - 1
    print("Kernel: {}".format(kernel))
    print("2D Gaussian array :\n")
    # print(gauss)
    plt.imshow(gauss)
    plt.title("Gaussian")
    plt.show()
    
    return gauss


if __name__ == '__main__':
    testYDS()
    # testGauss()
