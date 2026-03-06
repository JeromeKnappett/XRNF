#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  3 14:57:45 2021

@author: jerome
"""

import numpy as np
from math import log10, floor
# import imageio

import matplotlib.pyplot as plt
import pylab
# import pickle
# from tqdm import tqdm
#plt.style.use(['science','no-latex']) # 'ieee', 
pylab.rcParams['figure.figsize'] = (10.0, 8.0)

def round_sig(x, sig=2):
    if x != 0:
        return round(x, sig-int(floor(log10(abs(x))))-1)
    else:
        return x

dirPath = '/user/home/opt/xl/xl/experiments/BEUVbeamComparison_HF/data/atMask_cff1.4offset0_m1_sx1500sy1500FIXED/'
#'/user/home/opt/xl/xl/experiments/BEUVbeamComparison_HF/data/atMask_cff1.4offset-3_m1/'#'/user/home/opt/xl/xl/experiments/BEUVbeamProfile/data/fixed//m1_aerialImage_SE/'  #'/user/home/opt/xl/xl/experiments/fullbeamPolarisation/'#'/user/home/opt/xl/xl/experiments/beamCoherence2/data/' 
order = range(12,14)#[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]

trials =['intermediateIntensity/' + str(o) + '/' for o in order] #['data/'] #['fullRes_5000e/', 'fullRes_100e/'] #['120_1000x1000/']#'200e/','10000e/', '120e_250ir/']
intPR = 'IntensityDist_SE_intermed_'

# 'intermediateIntensity/' + 

checkSampling = False
samplingDiagnostics = False
# justPlot = True
# SAVE = False
# pick = False
# forStokes = False

elements = ['WBS exit',
            'M1 incident',
            'M1 exit',
            'M2 (PGM) incident',
            'M2 (PGM) exit',
            'Grating (PGM) incident',
            'Grating (PGM) exit',
            'Exit aperture incident',
            'Exit aperture exit',
            'M3 incident',
            'M3 exit',
            'SSA incident',
            'SSA exit',
            'BDA incident',
            'BDA exit',
            'Photon Block exit',
            'Mask exit',
            'Aerial Image',
            'Pinhole exit',
            'FarField',
            'Detector w/ beamstop'
            ]


propDist = [0,0.82,
            0,3.38,
            0,0.2,
            0,1.0,
            0,0.6,
            0,7.0,
            0,9.5,
            0,0.0,
            0,0.0,
            0,0.0,
            0,0.0,
            0,0.0,
            0,0.0]

sizes = [(0.00071,0.00084),(0.00071,0.00084),    # WBS
         (0.42,0.03),(0.42,0.03),                # M1
         (0.46,0.05),(0.46,0.05),                # M2 (PGM)
         (0.15,0.02),(0.15,0.02),                # Grating (PGM)
         (0.01,0.02),(0.01,0.02),                # Exit Aperture
         (0.24,0.04),(0.24,0.04),                # M3
         (10.0e-6,15.0e-6),(10.0e-6,15.0e-6),    # SSA 
         (100.0e-6,100.0e-6),(100.0e-6,100.0e-6),# BDA
         (10.0e-6,10.0e-6),(10.0e-6,10.0e-6),    # Photon Block
         (10.0e-6,10.0e-6),(10.0e-6,10.0e-6),    # Mask
         ]

noElemsSinceAp = [0, # WBS     !!!
                  1, # M1 i
                  2, # M1 e
                  3, # M2 e
                  4, # M2 e
                  5, # G i
                  6, # G 3
                  7, # Exit Ap i
                  0, # Exit ap !!!
                  1, # M3 i
                  2, # M3 e
                  3, # SSA i
                  0, # SSA     !!!
                  1, # BDA i
                  0, # BDA     !!!
                  0, # PB      !!!
                  0, # Mask    !!!
                  1, # AI
                  ]

dx_prev,dy_prev = [],[]
sx_prev,sy_prev = [],[]
D, R, N = [],[],[]
for e,o in enumerate(order):
    numXticks = 5
    numYticks = 5
    fSize = 15
    if e == 0:
        print(f"Element number:                      {e}")
        # print(f"Intensity data file: {dirPath + 'InitialIntensity.dat'}")
        print(f"Plane:                               {'WBS incident'}")
        
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
        plt.colorbar().set_label(label='Intensity [$ph/s/.1\%bw$]',size=fSize)
        
        plt.text(int(nx)-int((1*int(nx))/5),int(ny)-int((4*int(ny))/20),f"nx: {int(nx)}", color='r',fontsize=fSize)
        plt.text(int(nx)-int((1*int(nx))/5),int(ny)-int((3*int(ny))/20),f"ny: {int(ny)}", color='r',fontsize=fSize)
        plt.text(int(nx)-int((1*int(nx))/5),int(ny)-int((2*int(ny))/20),f"dx: {float(dx)} m", color='r',fontsize=fSize)
        plt.text(int(nx)-int((1*int(nx))/5),int(ny)-int((1*int(ny))/20),f"dy: {float(dy)} m", color='r',fontsize=fSize)
        plt.show()
        if checkSampling:
            from FWarbValue import getFWatValue
            fwhmx, fwhmy = getFWatValue(I, dx=dx, dy=dy,show=False,verbose=False)
            print(f"ROI (x,y):                          {(rx*1e3,ry*1e3)} mm")
            print(f"Intensity FWHM (x,y):               {(fwhmx*1e3,fwhmy*1e3)} mm")
            print(f"ROI/FWHM (x,y):                     {(round_sig(rx/fwhmx),round_sig(ry/fwhmy))}")
            if rx >= 3*fwhmx:
                print(f"Horizontal ROI                       GOOD! (ROI/FWHM (x) needs to be above 3 -> can decrease range by {3*fwhmx/rx})")
            else:
                print(f"Horizontal ROI                       BAD! (ROI/FWHM (x) needs to be above 3 -> increase range by {3*fwhmx/rx})")
            if ry >= 3*fwhmy:
                print(f"Vertical ROI                         GOOD! (ROI/FWHM (x) needs to be above 3 -> can decrease range by {3*fwhmx/rx})")
            else:   
                print(f"Verticalal ROI                       BAD! (ROI/FWHM (x) needs to be above 3 -> increase range by {3*fwhmy/ry})")
    if o == max(order)+1:
        print(max(order))
        print(f"Element number:                      {o-1}")
        print(f"Intensity data file: {dirPath + 'IntensityDist_SE.dat'}")
        print(f"Plane:                               {elements[o-1]}")
        
        nx = str(np.loadtxt(dirPath + str('IntensityDist_SE.dat'), dtype=str, comments=None, skiprows=6, max_rows=1, usecols=(0)))[1:]#[1:3]
        ny = str(np.loadtxt(dirPath + str('IntensityDist_SE.dat'), dtype=str, comments=None, skiprows=9, max_rows=1, usecols=(0)))[1:]#[1:3]
        xMin = str(np.loadtxt(dirPath + str('IntensityDist_SE.dat'), dtype=str, comments=None, skiprows=4, max_rows=1, usecols=(0)))[1:]#[1:3]
        xMax = str(np.loadtxt(dirPath + str('IntensityDist_SE.dat'), dtype=str, comments=None, skiprows=5, max_rows=1, usecols=(0)))[1:]#[1:3]
        rx = float(xMax)-float(xMin)
        dx = np.divide(rx,float(nx))
        yMin = str(np.loadtxt(dirPath + str('IntensityDist_SE.dat'), dtype=str, comments=None, skiprows=7, max_rows=1, usecols=(0)))[1:]#[1:3]
        yMax = str(np.loadtxt(dirPath + str('IntensityDist_SE.dat'), dtype=str, comments=None, skiprows=8, max_rows=1, usecols=(0)))[1:]#[1:3]
        ry = float(yMax)-float(yMin)
        dy = np.divide(ry,float(ny))
        I = np.reshape(np.loadtxt(dirPath+str('IntensityDist_SE.dat'),skiprows=10), (int(ny),int(nx)))
        
        plt.imshow(I,aspect='auto')
        plt.title(f"{elements[o-1]} : {propDist[o-1]} m propagation",fontsize=fSize)
    
        plt.xticks([int((float(nx)-1.0)*(a/(numXticks-1.0))) for a in range(numXticks)], [round_sig(float(nx)*dx*(b/(numXticks-1.0))*1e3) for b in range(-int((numXticks-1.0)/2.0),int((numXticks/2.0 + 1.0)))],fontsize=fSize)
        plt.yticks([int((float(ny)-1.0)*(a/(numYticks-1.0))) for a in range(numYticks)], [round_sig(float(ny)*dy*(b/(numYticks-1.0))*1e3) for b in range(-int((numYticks-1.0)/2.0),int((numYticks/2.0 + 1.0)))],fontsize=fSize)
        plt.xlabel('x - position [mm]',fontsize=fSize)
        plt.ylabel('y - position [mm]',fontsize=fSize)
        # plt.colorbar(label='Intensity [$ph/s/.1\%bw$]',labelsize=fSize)
        plt.colorbar().set_label(label='Intensity [$ph/s/.1\%bw$]',size=fSize)
        
        plt.text(int(nx)-int((1*int(nx))/5),int(ny)-int((4*int(ny))/20),f"nx: {int(nx)}", color='r',fontsize=fSize)
        plt.text(int(nx)-int((1*int(nx))/5),int(ny)-int((3*int(ny))/20),f"ny: {int(ny)}", color='r',fontsize=fSize)
        plt.text(int(nx)-int((1*int(nx))/5),int(ny)-int((2*int(ny))/20),f"dx: {float(dx)} m", color='r',fontsize=fSize)
        plt.text(int(nx)-int((1*int(nx))/5),int(ny)-int((1*int(ny))/20),f"dy: {float(dy)} m", color='r',fontsize=fSize)
        plt.show()
        if checkSampling:
            from FWarbValue import getFWatValue
            fwhmx, fwhmy = getFWatValue(I, dx=dx, dy=dy,show=False,verbose=False)
            print(f"ROI (x,y):                          {(rx*1e3,ry*1e3)} mm")
            print(f"Intensity FWHM (x,y):               {(fwhmx*1e3,fwhmy*1e3)} mm")
            print(f"ROI/FWHM (x,y):                     {(round_sig(rx/fwhmx),round_sig(ry/fwhmy))}")
            if rx >= 3*fwhmx:
                print(f"Horizontal ROI                       GOOD! (ROI/FWHM (x) needs to be above 3 -> can decrease range by {3*fwhmx/rx})")
            else:
                print(f"Horizontal ROI                       BAD! (ROI/FWHM (x) needs to be above 3 -> increase range by {3*fwhmx/rx})")
            if ry >= 3*fwhmy:
                print(f"Vertical ROI                         GOOD! (ROI/FWHM (x) needs to be above 3 -> can decrease range by {3*fwhmx/rx})")
            else:   
                print(f"Verticalal ROI                       BAD! (ROI/FWHM (x) needs to be above 3 -> increase range by {3*fwhmy/ry})")
    
    else:
        Ifile = dirPath + 'intermediateIntensity/' + intPR + str(o) + '.dat'
        print(" ")
        print(f"Element number:                      {o-1}")
        # print(f"Intensity data file: {Ifile}")
        # print(" ")
        print(f"Plane:                               {elements[o-1]}")
        print(f"Distance from last element:          {propDist[o-1]} m")
        nx = str(np.loadtxt(Ifile, dtype=str, comments=None, skiprows=6, max_rows=1, usecols=(0)))[1:]
        ny = str(np.loadtxt(Ifile, dtype=str, comments=None, skiprows=9, max_rows=1, usecols=(0)))[1:]
        xMax = str(np.loadtxt(Ifile, dtype=str, comments=None, skiprows=5, max_rows=1, usecols=(0)))[1:]
        xMin = str(np.loadtxt(Ifile, dtype=str, comments=None, skiprows=4, max_rows=1, usecols=(0)))[1:]
        yMax = str(np.loadtxt(Ifile, dtype=str, comments=None, skiprows=8, max_rows=1, usecols=(0)))[1:]
        yMin = str(np.loadtxt(Ifile, dtype=str, comments=None, skiprows=7, max_rows=1, usecols=(0)))[1:]
        rx = float(xMax)-float(xMin)
        ry = float(yMax)-float(yMin)
        dx = np.divide(rx,float(nx))
        dy = np.divide(ry,float(ny))
        I = np.reshape(np.loadtxt(Ifile, skiprows=10),(int(ny),int(nx)))
        
            
        plt.imshow(I,aspect='auto')
        # plt.title(f"Intensity at element #{e}")
        plt.title(f"{elements[o-1]} : {propDist[o-1]} m propagation",fontsize=fSize)
        plt.xticks([int((float(nx)-1.0)*(a/(numXticks-1.0))) for a in range(numXticks)], [round_sig(float(nx)*dx*(b/(numXticks-1.0))*1e6) for b in range(-int((numXticks-1.0)/2.0),int((numXticks/2.0 + 1.0)))],fontsize=fSize)
        plt.yticks([int((float(ny)-1.0)*(a/(numYticks-1.0))) for a in range(numYticks)], [round_sig(float(ny)*dy*(b/(numYticks-1.0))*1e6) for b in range(-int((numYticks-1.0)/2.0),int((numYticks/2.0 + 1.0)))],fontsize=fSize)
        plt.xlabel('x - position [um]',fontsize=fSize)
        plt.ylabel('y - position [um]',fontsize=fSize)
        # plt.colorbar(label='Intensity [$ph/s/.1\%bw$]',labelsize=fSize)
        plt.colorbar().set_label(label='Intensity [$ph/s/.1\%bw$]',size=fSize)
        plt.text(int(nx)-int((1*int(nx))/4),int(ny)-int((4*int(ny))/20),f"nx: {int(nx)}", color='r',fontsize=fSize)
        plt.text(int(nx)-int((1*int(nx))/4),int(ny)-int((3*int(ny))/20),f"ny: {int(ny)}", color='r',fontsize=fSize)
        plt.text(int(nx)-int((1*int(nx))/4),int(ny)-int((2*int(ny))/20),f"dx: {round_sig(float(dx),3)} m", color='r',fontsize=fSize)
        plt.text(int(nx)-int((1*int(nx))/4),int(ny)-int((1*int(ny))/20),f"dy: {round_sig(float(dy),3)} m", color='r',fontsize=fSize)
        plt.show()
        
        if checkSampling:
            from FWarbValue import getFWatValue
            fwhmx, fwhmy = getFWatValue(I, dx=dx, dy=dy,show=False,verbose=False)
            try:
                fwx, fwy = getFWatValue(I, dx=dy, dy=dy, frac=0.01, smoothing='gauss',sparams=200, show=False,verbose=False)
            except RuntimeError:
                fwx,fwy = sizes[e][0], sizes[e][1]
            print(f"ROI (x,y):                          {(rx*1e3,ry*1e3)} mm")
            print(f"Intensity FWHM (x,y):               {(fwhmx*1e3,fwhmy*1e3)} mm")
            print(f"Intensity FW (x,y):                 {(fwx*1e3,fwy*1e3)} mm")
            print(f"ROI/FW (x,y):                       {(round_sig(rx/fwx),round_sig(ry/fwy))}")
            if rx >= 3*fwx:
                print(f"Horizontal ROI                        GOOD! (ROI/FW (x) needs to be above 3 -> can decrease range by {3*fwhmx/rx})")
            else:
                print(f"Horizontal ROI                        BAD! (ROI/FW (x) needs to be above 3 -> increase range by {3*fwhmx/rx})")
            if ry >= 3*fwy:
                print(f"Vertical ROI                          GOOD! (ROI/FW (x) needs to be above 3 -> can decrease range by {3*fwhmx/rx})")
            else:   
                print(f"Vertical ROI                          BAD! (ROI/FW (x) needs to be above 3 -> increase range by {3*fwhmy/ry})")
            
            # propFromAp = np.sum(propDist[e-noElemsSinceAp[e]:e])
            if propDist[e] != 0: # propFromAp > 0: #propDist[e] > 0:
                wl = 6.7e-9
                # sizeX = sizes[e][0]
                # sizeY = sizes[e][1]
                sizeX = sx_prev[e-1]
                sizeY = sy_prev[e-1]
                # sizeX = sizes[e-noElemsSinceAp[e]][0]
                # sizeY = sizes[e-noElemsSinceAp[e]][1]
                propFromAp = np.sum(propDist[e-noElemsSinceAp[e]:e])
                
                # Checking minimum sampling requirements
                dX_FF = (propDist[e]*wl)/(2*sizeX)
                dY_FF = (propDist[e]*wl)/(2*sizeY)
                # # dX_FF = (propFromAp*wl)/(2*sizeX)
                # # dY_FF = (propFromAp*wl)/(2*sizeY)
                # # print(dx_prev[e-1])
                # # dX_NF = (propDist[e]*wl) / (sizeX - dx_prev[e-1]*int(nx))
                # # dY_NF = (propDist[e]*wl) / (sizeY - dy_prev[e-1]*int(ny))
                # # dX_NF = (propFromAp*wl) / (sizeX - dx_prev[e-1-noElemsSinceAp[e]]*int(nx))
                # # dY_NF = (propFromAp*wl) / (sizeY - dy_prev[e-1-noElemsSinceAp[e]]*int(ny))
                # dX_NF = (propDist[e]*wl) / (sizeX - dx_prev[e-1]*int(nx))
                # dY_NF = (propDist[e]*wl) / (sizeY - dy_prev[e-1]*int(ny))
                
                # print(f"Size of previous aperture (x,y):    {(sizeX,sizeY)} m")
                print(f"Beam size at previous element (x,y):{(sizeX,sizeY)} m")
                print(f"Sampling at previous plane (x,y):   {(dx_prev[e-1-noElemsSinceAp[e]],dy_prev[e-1-noElemsSinceAp[e]])} m")
                print(f"Sampling at this plane (x,y):       {(dx,dy)} m")
                print(f"Distance from previous aperture:     {propFromAp} m")
                
                print("--FF--")
                if dX_FF >= dx:
                    print(f'Horizontal sampling:                 GOOD! (Min sampling = {round_sig(dX_FF, 3)} m, ')
                    print(f"                                            Can decrease sampling by factor of {dx/dX_FF})")
                else:
                    print(f"Horizontal sampling:                 BAD! (Min sampling = {round_sig(dX_FF, 3)} m, ")
                    print(f"                                           Increase sampling by factor of {dx/dX_FF})")
                if dY_FF >= dy:
                    print(f'Vertical sampling:                   GOOD! (Min sampling = {round_sig(dY_FF, 3)} m, ')
                    print(f"                                            Can decrease sampling by factor of {dy/dY_FF})")
                else:
                    print(f"Vertical sampling:                   BAD! (Min sampling = {round_sig(dY_FF, 3)} m, ")
                    print(f"                                           Increase sampling by factor of {dy/dY_FF})")
                
                # print("--NF--")
                # if dX_NF >= dx:
                #     print('Horizontal sampling:                 GOOD!')
                # else:
                #     print(f"Horizontal sampling:                BAD! (Min sampling = {round_sig(dX_NF, 3)} m, ")
                #     print(f"                                          Increase sampling by factor of {dx/dX_NF})")
                # if dY_NF >= dy:
                #     print('Vertical sampling:                  GOOD!')
                # else:
                #     print(f"Vertical sampling:                  BAD! (Min sampling = {round_sig(dY_NF, 3)} m, ")
                #     print(f"                                          Increase sampling by factor of {dy/dY_NF})")
            
            else:
                dX_FF,dY_FF = dx,dy
                
            dx_prev.append(dx);dy_prev.append(dy)
            sx_prev.append(fwx);sy_prev.append(fwy)
            D.append((dX_FF,dY_FF))
            R.append([3*fwx,3*fwy,rx,ry])
        # dx_prev.append(dx);dy_prev.append(dy)
        # sx_prev.append(fwx);sy_prev.append(fwy)
        N.append((nx,ny))
        
        
samplingDiagnostics = True
if samplingDiagnostics:
    fig, ax = plt.subplots(4,1,sharex=True)
    ax[0].plot(elements,dx_prev,'x:',label='x - current')
    ax[0].plot(elements,dy_prev,'x:',label='y - current')
    ax[0].plot(elements[1::2],[d[0] for d in D[1::2]],'x:',label='x - optimal')
    ax[0].plot(elements[1::2],[d[1] for d in D[1::2]],'x:',label='y - optimal')
    ax[0].set_ylabel('Resolution [m]')
    ax[1].plot(elements,[r[2] for r in R],'x:',label='rx - current')
    ax[1].plot(elements,[r[3] for r in R],'x:',label='ry - current')
    ax[1].plot(elements,[r[0] for r in R],'x:',label='rx - optimal')
    ax[1].plot(elements,[r[1] for r in R],'x:',label='ry - optimal')
    ax[1].set_ylabel('Range [m]')
    ax[2].plot(elements,[int(n[0]) for n in N],'x:',label='x - current')
    ax[2].plot(elements,[int(n[1]) for n in N],'x:',label='y - current')
    ax[2].plot(elements,[r[0]/d[0] for r,d in zip(R,D)],'x:',label='x - optimal')
    ax[2].plot(elements,[r[1]/d[1] for r,d in zip(R,D)],'x:',label='y - optimal')
    ax[2].set_ylabel('Number of pixels [N]')
    ax[3].plot(elements,sx_prev,'x:',label='x')
    ax[3].plot(elements,sy_prev,'x:',label='y')
    ax[3].set_ylabel('Beam full width [m]')
    ax[3].set_xlabel('Plane of Beamline')
    ax[0].legend()
    for a in ax:
        a.set_yscale('log')
    fig.autofmt_xdate(rotation=45)
    fig.tight_layout()
    plt.show()
    