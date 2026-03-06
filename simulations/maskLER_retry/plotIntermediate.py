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
pylab.rcParams['figure.figsize'] = (8.0, 6.0)

def round_sig(x, sig=2):
    if x != 0:
        return round(x, sig-int(floor(log10(abs(x))))-1)
    else:
        return x

def check_wavefield_sampling(wavefield, dx, dy, oversampling_factor=2):
    """
    Check if the 2D wavefield (either phase or intensity) is adequately sampled.
    
    Parameters:
    - wavefield: 2D numpy array representing either the intensity or phase of the wavefield.
    - dx: The spatial sampling interval in the x direction (meters/pixel).
    - dy: The spatial sampling interval in the y direction (meters/pixel).
    - oversampling_factor: The required factor above the Nyquist frequency to be considered oversampled.
                           Default is 2 (i.e., twice the Nyquist frequency).
    
    Returns:
    - A boolean value indicating whether the wavefield is adequately sampled.
    """
    # Perform 2D Fourier transform of the wavefield
    wavefield_fft = np.fft.fftshift(np.fft.fft2(wavefield))
    
    # Get the dimensions of the wavefield
    Nx, Ny = wavefield.shape
    
    # Generate the frequency grids in x and y directions using the correct size
    fx = np.fft.fftshift(np.fft.fftfreq(Nx, d=dx))
    fy = np.fft.fftshift(np.fft.fftfreq(Ny, d=dy))
    
    # Now create a meshgrid of the correct size to match the wavefield dimensions
    FX, FY = np.meshgrid(fx, fy, indexing='ij')
    
    # Calculate the 2D spatial frequencies (magnitude of spatial frequency vector)
    freq_magnitude = np.sqrt(FX**2 + FY**2)
    
    # Get the magnitude of the Fourier coefficients (spectrum of the wavefield)
    wavefield_spectrum = np.abs(wavefield_fft)
    
    # Find the highest significant spatial frequency
    # Apply a threshold to ignore very small (insignificant) values in the spectrum
    spectrum_threshold = np.max(wavefield_spectrum) * 0.01
    significant_frequencies = freq_magnitude[wavefield_spectrum > spectrum_threshold]
    
    if significant_frequencies.size > 0:
        max_freq_wavefield = np.max(significant_frequencies)
    else:
        max_freq_wavefield = 0  # If no significant frequencies, set to 0
    
    # Nyquist frequency
    fx_nyquist = 1 / (2 * dx)
    fy_nyquist = 1 / (2 * dy)
    f_nyquist = np.sqrt(fx_nyquist**2 + fy_nyquist**2)
    
    # Check if the maximum frequency is less than Nyquist frequency / oversampling_factor
    adequately_sampled = max_freq_wavefield < (f_nyquist / oversampling_factor)
    
    # Print results
    print("Max spatial frequency (wavefield):", max_freq_wavefield)
    print("Nyquist frequency:", f_nyquist)
    print("Oversampling factor:", oversampling_factor)
    print("Adequately sampled:", adequately_sampled)
    
    # Plot the 2D frequency spectrum and overlay the Nyquist and maximum spatial frequencies
    plt.figure(figsize=(8, 6))
    plt.imshow(np.log1p(wavefield_spectrum), extent=[fx[0], fx[-1], fy[0], fy[-1]], origin='lower', cmap='inferno',aspect='auto')
    plt.colorbar(label='Log Spectrum Intensity')
    
    # Mark the max spatial frequency and Nyquist frequency on the plot
    plt.contour(FX, FY, freq_magnitude, levels=[max_freq_wavefield], colors='blue', linestyles='dashed', label='Max Spatial Frequency')
    plt.contour(FX, FY, freq_magnitude, levels=[f_nyquist], colors='green', linestyles='solid', label='Nyquist Frequency')
    
    # Add text annotations
    plt.text(0.05, 0.95, f"Max Freq: {max_freq_wavefield:.2f}", color='blue', fontsize=12, transform=plt.gca().transAxes)
    plt.text(0.05, 0.9, f"Nyquist Freq: {f_nyquist:.2f}", color='green', fontsize=12, transform=plt.gca().transAxes)
    if adequately_sampled:
        plt.text(0.05, 0.85, f"OVERSAMPLED", color='white', fontsize=12, transform=plt.gca().transAxes)
    else:
        plt.text(0.05, 0.85, f"UNDERSAMPLED", color='white', fontsize=12, transform=plt.gca().transAxes)
        
    
    # Labels and title
    plt.title("2D Frequency Spectrum")
    plt.xlabel("Spatial Frequency in X (1/m)")
    plt.ylabel("Spatial Frequency in Y (1/m)")
    plt.show()
    
    return adequately_sampled

dirPath = '/user/home/opt/xl/xl/experiments/maskLER_retry/data/test/afterMask1/'#'data/phaseSpace/atDetector/'
#'/user/home/opt/xl/xl/experiments/XFM_ptycho/data/PtychoTest/pos1/'
#FZP/FZPprop_1mm/'
#FZP_exit/'
#'aerial_image/AI_p200/'#grating_nearfield/afterPinhole_1cm/'  #'/user/home/opt/xl/xl/experiments/fullbeamPolarisation/'#'/user/home/opt/xl/xl/experiments/beamCoherence2/data/' 
order = [16,17]#[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]#,9,10,11,12,13,14]

trials =[str(o) + '/' for o in order] #['data/'] #['fullRes_5000e/', 'fullRes_100e/'] #['120_1000x1000/']#'200e/','10000e/', '120e_250ir/']
intPR = 'IntensityDist_intermed_'
#'intElement_intermed_'

checkSampling = True
samplingDiagnostics = False
save_all = False
# justPlot = True
# SAVE = False
# pick = False
# forStokes = False

# to do: make elements a list with each having a [name, type, size] - JK

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
            'Mask 1 exit',
            'Mask 2 exit',
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
    print(e)
    print(np.max(order))
    numXticks = 5
    numYticks = 5
    fSize = 15
    # if e == 0:
    #     pass
    #     print(f"Element number:                      {e}")
    #     # print(f"Intensity data file: {dirPath + 'res_int_pr_se.dat'}")
    #     if e ==0:
    #         print(f"Plane:                               {'WBS incident'}")
    #         filename = 'IntensityDist'#'res_int_se.dat'
    #     else:
    #         print(f"Plane:                               {'Final'}")
    #         filename = 'res_int_pr_me.dat'
            
    #     nx = str(np.loadtxt(dirPath + str(filename), dtype=str, comments=None, skiprows=6, max_rows=1, usecols=(0)))[1:]#[1:3]
    #     ny = str(np.loadtxt(dirPath + str(filename), dtype=str, comments=None, skiprows=9, max_rows=1, usecols=(0)))[1:]#[1:3]
    #     xMin = str(np.loadtxt(dirPath + str(filename), dtype=str, comments=None, skiprows=4, max_rows=1, usecols=(0)))[1:]#[1:3]
    #     xMax = str(np.loadtxt(dirPath + str(filename), dtype=str, comments=None, skiprows=5, max_rows=1, usecols=(0)))[1:]#[1:3]
    #     rx = float(xMax)-float(xMin)
    #     dx = np.divide(rx,float(nx))
    #     yMin = str(np.loadtxt(dirPath + str(filename), dtype=str, comments=None, skiprows=7, max_rows=1, usecols=(0)))[1:]#[1:3]
    #     yMax = str(np.loadtxt(dirPath + str(filename), dtype=str, comments=None, skiprows=8, max_rows=1, usecols=(0)))[1:]#[1:3]
    #     ry = float(yMax)-float(yMin)
    #     dy = np.divide(ry,float(ny))
    #     I = np.reshape(np.loadtxt(dirPath+str(filename),skiprows=10), (int(ny),int(nx)))
        
    #     plt.imshow(I,aspect='auto')
    #     # plt.title('WBS incident : 14.3 m propagation',fontsize=fSize)
    #     plt.xticks([int((float(nx)-1.0)*(a/(numXticks-1.0))) for a in range(numXticks)], [round_sig(float(nx)*dx*(b/(numXticks-1.0))*1e3) for b in range(-int((numXticks-1.0)/2.0),int((numXticks/2.0 + 1.0)))],fontsize=fSize)
    #     plt.yticks([int((float(ny)-1.0)*(a/(numYticks-1.0))) for a in range(numYticks)], [round_sig(float(ny)*dy*(b/(numYticks-1.0))*1e3) for b in range(-int((numYticks-1.0)/2.0),int((numYticks/2.0 + 1.0)))],fontsize=fSize)
    #     plt.xlabel('x - position [mm]',fontsize=fSize)
    #     plt.ylabel('y - position [mm]',fontsize=fSize)
    #     # plt.colorbar(label='Intensity [$ph/s/.1\%bw$]',labelsize=fSize)
    #     plt.colorbar().set_label(label='Intensity [$ph/s/.1\%bw$]',size=fSize)
        
    #     plt.text(int(nx)-int((1*int(nx))/5),int(ny)-int((4*int(ny))/20),f"nx: {int(nx)}", color='r',fontsize=fSize)
    #     plt.text(int(nx)-int((1*int(nx))/5),int(ny)-int((3*int(ny))/20),f"ny: {int(ny)}", color='r',fontsize=fSize)
    #     plt.text(int(nx)-int((1*int(nx))/5),int(ny)-int((2*int(ny))/20),f"dx: {float(dx)} m", color='r',fontsize=fSize)
    #     plt.text(int(nx)-int((1*int(nx))/5),int(ny)-int((1*int(ny))/20),f"dy: {float(dy)} m", color='r',fontsize=fSize)
    #     plt.show()
    #     if checkSampling:
    #         sampling = check_wavefield_sampling(I, dx, dy, oversampling_factor=2)
    #         if sampling:
    #             print('\n :):):) ADEQUATELY SAMPLED :):):)')
    #         else:
                
    #             print('\n :(:(:( INADEQUATELY SAMPLED :(:(:(')
    #         # from FWarbValue import getFWatValue
    #         # fwhmx, fwhmy = getFWatValue(I, dx=dx, dy=dy,show=False,verbose=False)
    #         # print(f"ROI (x,y):                          {(rx*1e3,ry*1e3)} mm")
    #         # print(f"Intensity FWHM (x,y):               {(fwhmx*1e3,fwhmy*1e3)} mm")
    #         # print(f"ROI/FWHM (x,y):                     {(round_sig(rx/fwhmx),round_sig(ry/fwhmy))}")
    #         # if rx >= 3*fwhmx:
    #         #     print(f"Horizontal ROI                       GOOD! (ROI/FWHM (x) needs to be above 3 -> can decrease range by {3*fwhmx/rx})")
    #         # else:
    #         #     print(f"Horizontal ROI                       BAD! (ROI/FWHM (x) needs to be above 3 -> increase range by {3*fwhmx/rx})")
    #         # if ry >= 3*fwhmy:
    #         #     print(f"Vertical ROI                         GOOD! (ROI/FWHM (x) needs to be above 3 -> can decrease range by {3*fwhmx/rx})")
    #         # else:   
    #         #     print(f"Verticalal ROI                       BAD! (ROI/FWHM (x) needs to be above 3 -> increase range by {3*fwhmy/ry})")
                    
    Ifile = dirPath + intPR + str(o) + '.dat'
    print(" ")
    print(f"Element number:                      {o}")
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
    
        
    # plt.imshow(np.log(I),aspect='auto')
    plt.imshow(I,aspect='auto')
    # plt.title(f"Intensity at element #{e}")
    plt.title(f"{elements[o-1]}", fontsize=fSize) # : {propDist[o-1]}" m propagation, #{o-1}",fontsize=fSize)
    plt.xticks([int((float(nx)-1.0)*(a/(numXticks-1.0))) for a in range(numXticks)], [round_sig(float(nx)*dx*(b/(numXticks-1.0))*1e6) for b in range(-int((numXticks-1.0)/2.0),int((numXticks/2.0 + 1.0)))],fontsize=fSize)
    plt.yticks([int((float(ny)-1.0)*(a/(numYticks-1.0))) for a in range(numYticks)], [round_sig(float(ny)*dy*(b/(numYticks-1.0))*1e6) for b in range(-int((numYticks-1.0)/2.0),int((numYticks/2.0 + 1.0)))],fontsize=fSize)
    plt.xlabel('x - position [um]',fontsize=fSize)
    plt.ylabel('y - position [um]',fontsize=fSize)
    # plt.colorbar(label='Intensity [$ph/s/.1\%bw$]',labelsize=fSize)
    plt.colorbar().set_label(label='Intensity [$ph/s/.1\%bw$]',size=fSize)
    plt.text(int(nx)-int((1*int(nx))/3),int(ny)-int((6*int(ny))/20),f"nx: {int(nx)}", color='r',fontsize=fSize)
    plt.text(int(nx)-int((1*int(nx))/3),int(ny)-int((5*int(ny))/20),f"ny: {int(ny)}", color='r',fontsize=fSize)
    plt.text(int(nx)-int((1*int(nx))/3),int(ny)-int((4*int(ny))/20),f"dx: {round_sig(float(dx),3)} m", color='r',fontsize=fSize)
    plt.text(int(nx)-int((1*int(nx))/3),int(ny)-int((3*int(ny))/20),f"dy: {round_sig(float(dy),3)} m", color='r',fontsize=fSize)
    plt.text(int(nx)-int((1*int(nx))/3),int(ny)-int((2*int(ny))/20),f"Rx: {round_sig(float(rx),3)} m", color='r',fontsize=fSize)
    plt.text(int(nx)-int((1*int(nx))/3),int(ny)-int((1*int(ny))/20),f"Ry: {round_sig(float(ry),3)} m", color='r',fontsize=fSize)
    plt.show()
    
    # if e >=2:
    #     plt.imshow(I[int(ny)//2 - 100:int(ny)//2 + 100,int(nx)//2 - 100:int(nx)//2 + 100])
    #     plt.show()
    if save_all:
        imgtype = np.uint32 #np.uint16 # np.unit32
        maxval = 4294967295 #65536
        import imageio
        Ilog = np.array(np.log(I))
        I = np.array(I)
        # Check if the data fits within uint32 range
        if I.max() <= maxval: #4294967295:
            # Safe to convert
            I = I.astype(imgtype)#32)
            Ilog = Ilog.astype(imgtype)
        else:
            # Scaling needed to fit within uint32 range
            scale_factor = I.max() / maxval #4294967295
            I = (I / maxval).astype(np.uint32) #4294967295).astype(np.uint32)
            Ilog = Ilog.astype(imgtype) #4294967295).astype(np.uint32)
        
        # import imageio
        # I = np.array(I)#,dtype=np.uint32)
        # # I = I/np.max(I)
        # I = I.astype(np.int32)
        
        plt.imshow(I,aspect='auto')
        plt.show()
        
        imageio.imwrite(dirPath + elements[o-1] + '.tif',I)
        imageio.imwrite(dirPath + elements[o-1] + '_log.tif',Ilog)
    
    if checkSampling:
        sampling = check_wavefield_sampling(I, dx, dy, oversampling_factor=2)
        if sampling:
            print('\n :):):) ADEQUATELY SAMPLED :):):)')
        else:
            
            print('\n :(:(:( INADEQUATELY SAMPLED :(:(:(')
        # from FWarbValue import getFWatValue
        # fwhmx, fwhmy = getFWatValue(I, dx=dx, dy=dy,show=False,verbose=False)
        # fwx, fwy = getFWatValue(I, dx=dy, dy=dy, frac=0.01, smoothing='gauss',sparams=200, show=False,verbose=False)
        # print(f"ROI (x,y):                          {(rx*1e3,ry*1e3)} mm")
        # print(f"Intensity FWHM (x,y):               {(fwhmx*1e3,fwhmy*1e3)} mm")
        # print(f"Intensity FW (x,y):                 {(fwx*1e3,fwy*1e3)} mm")
        # print(f"ROI/FW (x,y):                       {(round_sig(rx/fwx),round_sig(ry/fwy))}")
        # if rx >= 3*fwx:
        #     print(f"Horizontal ROI                        GOOD! (ROI/FW (x) needs to be above 3 -> can decrease range by {3*fwhmx/rx})")
        # else:
        #     print(f"Horizontal ROI                        BAD! (ROI/FW (x) needs to be above 3 -> increase range by {3*fwhmx/rx})")
        # if ry >= 3*fwy:
        #     print(f"Vertical ROI                          GOOD! (ROI/FW (x) needs to be above 3 -> can decrease range by {3*fwhmx/rx})")
        # else:   
        #     print(f"Vertical ROI                          BAD! (ROI/FW (x) needs to be above 3 -> increase range by {3*fwhmy/ry})")
        
        # # propFromAp = np.sum(propDist[e-noElemsSinceAp[e]:e])
        # if propDist[e] != 0: # propFromAp > 0: #propDist[e] > 0:
        #     wl = 1.4878875e-10 #6.7e-9
        #     # sizeX = sizes[e][0]
        #     # sizeY = sizes[e][1]
        #     sizeX = sx_prev[e-1]
        #     sizeY = sy_prev[e-1]
        #     # sizeX = sizes[e-noElemsSinceAp[e]][0]
        #     # sizeY = sizes[e-noElemsSinceAp[e]][1]
        #     propFromAp = np.sum(propDist[e-noElemsSinceAp[e]:e])
            
        #     # Checking minimum sampling requirements
        #     dX_FF = (propDist[e]*wl)/(2*sizeX)
        #     dY_FF = (propDist[e]*wl)/(2*sizeY)
        #     # dX_FF = (propFromAp*wl)/(2*sizeX)
        #     # dY_FF = (propFromAp*wl)/(2*sizeY)
        #     # print(dx_prev[e-1])
        #     # dX_NF = (propDist[e]*wl) / (sizeX - dx_prev[e-1]*int(nx))
        #     # dY_NF = (propDist[e]*wl) / (sizeY - dy_prev[e-1]*int(ny))
        #     # dX_NF = (propFromAp*wl) / (sizeX - dx_prev[e-1-noElemsSinceAp[e]]*int(nx))
        #     # dY_NF = (propFromAp*wl) / (sizeY - dy_prev[e-1-noElemsSinceAp[e]]*int(ny))
        #     dX_NF = (propDist[e]*wl) / (sizeX - dx_prev[e-1]*int(nx))
        #     dY_NF = (propDist[e]*wl) / (sizeY - dy_prev[e-1]*int(ny))
            
        #     # print(f"Size of previous aperture (x,y):    {(sizeX,sizeY)} m")
        #     print(f"Beam size at previous element (x,y):{(sizeX,sizeY)} m")
        #     print(f"Sampling at previous plane (x,y):   {(dx_prev[e-1-noElemsSinceAp[e]],dy_prev[e-1-noElemsSinceAp[e]])} m")
        #     print(f"Sampling at this plane (x,y):       {(dx,dy)} m")
        #     print(f"Distance from previous aperture:     {propFromAp} m")
            
        #     print("--FF--")
        #     if dX_FF >= dx:
        #         print(f'Horizontal sampling:                 GOOD! (Min sampling = {round_sig(dX_FF, 3)} m, ')
        #         print(f"                                            Can decrease sampling by factor of {dx/dX_FF})")
        #     else:
        #         print(f"Horizontal sampling:                 BAD! (Min sampling = {round_sig(dX_FF, 3)} m, ")
        #         print(f"                                           Increase sampling by factor of {dx/dX_FF})")
        #     if dY_FF >= dy:
        #         print(f'Vertical sampling:                   GOOD! (Min sampling = {round_sig(dY_FF, 3)} m, ')
        #         print(f"                                            Can decrease sampling by factor of {dy/dY_FF})")
        #     else:
        #         print(f"Vertical sampling:                   BAD! (Min sampling = {round_sig(dY_FF, 3)} m, ")
        #         print(f"                                           Increase sampling by factor of {dy/dY_FF})")
            
        #     # print("--NF--")
        #     # if dX_NF >= dx:
        #     #     print('Horizontal sampling:                 GOOD!')
        #     # else:
        #     #     print(f"Horizontal sampling:                BAD! (Min sampling = {round_sig(dX_NF, 3)} m, ")
        #     #     print(f"                                          Increase sampling by factor of {dx/dX_NF})")
        #     # if dY_NF >= dy:
        #     #     print('Vertical sampling:                  GOOD!')
        #     # else:
        #     #     print(f"Vertical sampling:                  BAD! (Min sampling = {round_sig(dY_NF, 3)} m, ")
        #     #     print(f"                                          Increase sampling by factor of {dy/dY_NF})")
        
        # else:
        #     dX_FF,dY_FF = dx,dy
        # dx_prev.append(dx);dy_prev.append(dy)
        # sx_prev.append(fwx);sy_prev.append(fwy)
        # N.append((nx,ny))
        # D.append((dX_FF,dY_FF))
        # R.append([3*fwx,3*fwy,rx,ry])
    
import imageio
I = imageio.imread(dirPath + 'intensity.tif')

nx,ny = np.shape(I)[1], np.shape(I)[0]

plt.imshow(I,aspect='auto')
plt.colorbar()
plt.show()

print(nx,ny)
dx,dy = 4.9925659778685604e-09, 7.663191092658936e-08

sx,sy = 1000,100


plt.imshow(I,aspect='auto')
# plt.xticks([200,400,600,800],labels=[str(x*5.0) for x in [200,400,600,800]])
plt.xlabel('x [um]')
plt.colorbar()
plt.show()

plt.imshow(I[ny//2 - sy//2:ny//2 + sy//2, nx//2 - sx//2:nx//2 + sx//2],aspect='auto')
plt.xticks([200,400,600,800],labels=[str(x*5.0) for x in [200,400,600,800]])
plt.xlabel('x [um]')
plt.colorbar()
plt.show()
        
samplingDiagnostics = False
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
    