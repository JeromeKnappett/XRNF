#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 15:41:04 2024

@author: -
"""

import numpy as np
import matplotlib.pyplot as plt
import tifffile
import matplotlib.gridspec as gridspec
from mpl_toolkits.axes_grid1 import make_axes_locatable

# path = 'wavefield_1.pkl'
path = '/user/home/opt/xl/xl/experiments/BEUVbeamComparison_mirrorR/data/'
#slit sizes]
wl = 6.7e-9

xlim = [-0.005,0.005]
ylim = [-0.0007,0.0007]

planes = [
          'WBS_i', 'WBS_e',
          'M1_i', 'M1_e',
          'PGM_i', 'PGM_e',
          'EA_i', 'EA_e',
          'M3_i', 'M3_e',
          'SSA_i','SSA_e',
          'mask_i'
          ]
# S = 300
# sX = [25,50,75,100,125,150,175,200,225,250,300,350,500]
# sY = np.full_like(sX,200)
files = [path + p + '/' for p in planes]
# [path + 'beforeBDA_efield_sx' + str(sx) + 'sy' + str(sy) + '/beforeBDA_efield_sx' + str(sx) + 'sy' + str(sy) + 'Efields.pkl' for sx,sy in zip(sX,sY)]

# picks = [pickle.load(open(f, 'rb')) for f in files]
# EhR = [p[0] for p in picks]
# EhI = [p[1] for p in picks]
# EvR = [p[2] for p in picks]
# EvI = [p[3] for p in picks]
# res = [(p[4],p[5]) for p in picks]


# Eh = [ExR + ExI*1j for ExR,ExI in zip(EhR,EhI)]
# Ev = [EyR + EyI*1j for EyR,EyI in zip(EvR,EvI)]#EvR + EvI*1j

# E = Eh[0] + Ev[0]    
# print(np.shape(E))
# Combine into a single array
for i,f in enumerate(files):
    print(planes[i])
    I = tifffile.imread(f + 'intensity.tif')
    P = tifffile.imread(f + 'phase.tif')
    Ifile = f + 'IntensityDist_SE.dat'
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
    # E = np.stack((Eh[i], Ev[i]), axis=-1)
    # dx,dy = res[i][0],res[i][1]
    
    # print(np.shape(E))
    # # Plot total intensity and phase
    # I, P = plot_total_intensity_and_phase(E, dx, dy)
    
    intensity_threshold = np.max(I) / 10# (e**2)
    
    print('Threshold I')
    print(intensity_threshold)
    
    # Calculate phase
    # phase = calculate_phase(E)
    
    
    # Calculate the total phase
    phase_total = P + np.pi
    intensity_total = I
    
    # Plot intensity and phase
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))
    
    im0 = axs[0].imshow(intensity_total,aspect='auto')
    axs[0].set_title('Total Intensity')
    fig.colorbar(im0, ax=axs[0])
    
    im1 = axs[1].imshow(phase_total,aspect='auto')
    axs[1].set_title('Total Phase')
    fig.colorbar(im1, ax=axs[1])
    
    plt.tight_layout()
    plt.show()
    
    from getPhaseSpace_threshold import calculate_phase_gradient_threshold, phase_gradient_from_center, compute_divergence_from_phase_gradient, plot_divergence_vs_distance
    

    # Calculate the total phase
    # phase_total = np.angle(E_x + E_y)
    phase_total_xunwrap = np.unwrap(phase_total, axis=1, period=2*np.pi)
    phase_total_yunwrap = np.unwrap(phase_total, axis=0, period=2*np.pi)
    # print('shape of phase: ', np.shape(phase_total))
    
    # Calculate the phase gradient (partial derivative of the total phase)
    """For two dimensional arrays, the return will be two arrays ordered by
    axis. In this example the first array stands for the gradient in
    rows and the second one in columns direction:"""
    
    gradient_x, gradient_y_bad = phase_gradient_from_center(phase_total_xunwrap,dx,dy) #np.gradient(phase_total)
    gradient_x_bad, gradient_y = phase_gradient_from_center(phase_total_yunwrap,dx,dy) #np.gradient(phase_total)
    
    # Create the grid for calculating distance from the center
    ny, nx = I.shape
    print('here')
    print(nx,ny)
    x = np.linspace(-nx//2, nx//2, nx) * dx
    y = np.linspace(ny//2, -ny//2, ny) * dy
    X, Y = np.meshgrid(x, y)
    
    print(np.shape(X))
    print(np.shape(Y))
    
    gradient_x[np.abs(intensity_total) < intensity_threshold] = 0
    gradient_y[np.abs(intensity_total) < intensity_threshold] = 0
    
    X[np.abs(intensity_total) < intensity_threshold] = 0
    Y[np.abs(intensity_total) < intensity_threshold] = 0
    
    # # Plot phase gradient vs distance
    # plot_divergence_vs_distance(gradient_x, gradient_y, distance_from_center_x, distance_from_center_y)
    
    # Compute divergences
    divergence_x, divergence_y = compute_divergence_from_phase_gradient(wl,gradient_x/dx, gradient_y/dy,dx,dy)
    
    # Plot divergence vs distance
    plot_divergence_vs_distance(divergence_x, divergence_y, X, Y,title = planes[i],limit=[xlim,ylim])
    
    # phase_total = np.unwrap(phase_total, axis=0)#,discont=2*np.pi)#, period=np.pi)
    # phase_total = np.unwrap(phase_total, axis=1)#,discont=2*np.pi)#, period=np.pi)
    
    # # plt.plot(np.unwrap(phase_total[np.shape(phase_total)[0]//2,:]))#,period = np.pi))#, discont=np.pi))
    # # plt.show()
    # print('shape of phase: ', np.shape(phase_total))
    
    # # Calculate the phase gradient (partial derivative of the total phase)
    # """For two dimensional arrays, the return will be two arrays ordered by
    # axis. In this example the first array stands for the gradient in
    # rows and the second one in columns direction:"""

    # # >>> np.gradient(np.array([[1, 2, 6], [3, 4, 5]], dtype=float))
    # # [array([[ 2.,  2., -1.],
    # #        [ 2.,  2., -1.]]), array([[1. , 2.5, 4. ],
    # #        [1. , 1. , 1. ]])]
                                     
    # # gradient_x = sobel(phase_total, axis=0) / dx
    # # gradient_y = sobel(phase_total, axis=1) / dy
    # # gradient_x = np.gradient(phase_total, axis=0) / dx
    # # gradient_y = np.gradient(phase_total, axis=1) / dy
    
        
    # ny, nx = I.shape
    # # print('here')
    # # print(nx,ny)
    # x = np.linspace(-nx//2, nx//2, nx) * dx
    # y = np.linspace(-ny//2, ny//2, ny) * dy
    # X, Y = np.meshgrid(x, y)
    
    # # Plot intensity and phase
    # fig, axs = plt.subplots(1, 2, figsize=(12, 6))
    
    # im0 = axs[0].imshow(intensity_total, extent=[x.min(), x.max(), y.min(), y.max()], origin='lower',aspect='auto')
    # axs[0].set_title('Total Intensity')
    # fig.colorbar(im0, ax=axs[0])
    
    # im1 = axs[1].imshow(P, extent=[x.min(), x.max(), y.min(), y.max()], origin='lower',aspect='auto')
    # axs[1].set_title('Total Phase')
    # fig.colorbar(im1, ax=axs[1])
    
    # plt.tight_layout()
    # plt.show()
    
    
    # # fig, ax = plt.subplots(1,3)
    # # p2d = ax[1].imshow(phase_total,aspect='auto')
    
    # # divider = make_axes_locatable(ax[1])
    # # cax = divider.append_axes("right", size="5%", pad=0.05)
    # # #_cax = divider.append_axes("right", size="0%", pad=0.0)
    # # plt.colorbar(p2d, cax=cax, orientation='vertical',label='Phase [$\phi$]')
    # # # ax[1].colorbar()
    # # ax[1].set_title('Unwrapped phase')
    # # # plt.show()
    
    
    # from getPhaseSpace_threshold import phase_gradient_from_center, compute_divergence_from_phase_gradient, plot_divergence_vs_distance
    
    # gradient_x, gradient_y = phase_gradient_from_center(phase_total,dx,dy) #np.gradient(phase_total)
    
    # # print(np.shape(X))
    # # print(np.shape(Y))
    
    # # ax[0].plot(phase_total[np.shape(phase_total)[0]//2,:]/np.max(phase_total[np.shape(phase_total)[0]//2,:]))
    # # ax[0].plot(gradient_x[np.shape(phase_total)[0]//2,:])
    # # ax[0].set_title('x')
    # # ax[2].plot(phase_total[:,np.shape(phase_total)[1]//2]/np.max(phase_total[:,np.shape(phase_total)[1]//2]))
    # # ax[2].plot(gradient_y[:,np.shape(phase_total)[1]//2])
    # # ax[2].set_title('y')
    # # plt.tight_layout()
    # # plt.show()
        
    # gradient_x[np.abs(intensity_total) < intensity_threshold] = 0
    # gradient_y[np.abs(intensity_total) < intensity_threshold] = 0
    
    # grad_thresh = np.pi
    
    # gradient_x[np.abs(gradient_x) >= grad_thresh] = 0
    # gradient_y[np.abs(gradient_y) >= grad_thresh] = 0
    
    
    # # plt.imshow(gradient_x,aspect='auto')
    # # plt.colorbar()
    # # plt.title('phase gradient (x) - after')
    # # plt.show()
    
    # # plt.imshow(gradient_y,aspect='auto')
    # # plt.colorbar()
    # # plt.title('phase gradient (y) - after')
    # # plt.show()
    
    
    # X[np.abs(intensity_total) < intensity_threshold] = 0
    # Y[np.abs(intensity_total) < intensity_threshold] = 0
    
    # X[np.abs(gradient_x) >= grad_thresh] = 0
    # Y[np.abs(gradient_y) >= grad_thresh] = 0
    
    
    # # plt.imshow(X,aspect='auto')
    # # plt.colorbar()
    # # plt.title('X')
    # # plt.show()
    # # plt.imshow(Y,aspect='auto')
    # # plt.colorbar()
    # # plt.title('Y')
    # # plt.show()
    
    # # Calculate phase gradients
    # # gradient_x, gradient_y, distance_from_center_x, distance_from_center_y = calculate_phase_gradient(phase, dx, dy)
    
    # # Apply intensity threshold and get distances from center
    # # intensity_threshold = 0.1  # Example threshold value
    # # gradient_x, gradient_y, distance_from_center_x, distance_from_center_y = calculate_phase_gradient_threshold(E, dx, dy, intensity_threshold)
    
    # # # Plot phase gradient vs distance
    # # plot_divergence_vs_distance(gradient_x, gradient_y, distance_from_center_x, distance_from_center_y)
    
    # # Compute divergences
    # divergence_x, divergence_y = compute_divergence_from_phase_gradient(wl,gradient_x / dx, gradient_y / dy,dx,dy)
    
    # # Plot divergence vs distance
    # # print('\n here')
    # # print('helllloooooooo')
    # plot_divergence_vs_distance(divergence_x, divergence_y,X, Y,title = planes[i])
    
