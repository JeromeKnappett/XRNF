#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 15:41:04 2024

@author: -
"""

import numpy as np
import matplotlib.pyplot as plt
from math import e
import tifffile
import matplotlib.gridspec as gridspec
from mpl_toolkits.axes_grid1 import make_axes_locatable
import csv
import pickle
from getPhaseSpace_threshold import phase_gradient_from_center, compute_divergence_from_phase_gradient, plot_divergence_vs_distance, plot_total_intensity_and_phase
import FWarbValue

def electronPhaseSpace(file,bins,plot=True):
    """
    Read data from a CSV file and convert it to a numpy array.
    
    Parameters:
    filename (str): The name of the input CSV file.
    
    Returns:
    numpy array: A numpy array containing the data from the CSV file.
    """
    data = []
    
    # Open the file for reading
    with open(file, mode='r') as file:
        reader = csv.reader(file)
        
        # Skip the header
        next(reader)
        
        # Read the rows and append to the data list
        for row in reader:
            data.append([float(value) for value in row])
    
    # # Convert the list to a numpy array
    # data_array = np.array(data)
    # print(data)
    
    x = [d[0] for d in data]
    _x = [d[1] for d in data]
    y = [d[2] for d in data]
    _y = [d[3] for d in data]
    elecE = [d[4] for d in data]
    
    
    x = [a*1e6 for a in x]
    xp = [a*1e6 for a in _x]
    y = [a*1e6 for a in y]
    yp = [a*1e6 for a in _y]
    
    # print(x)
    
    
    if plot:
        # xsize, xdiv = scatter_with_histograms(x,xp, bins=bins,labels=["x","x'"])
        # ysize, ydiv = scatter_with_histograms(y,yp, bins=bins,labels=["y","y'"])
        scatter_with_histograms(x,xp, bins=bins,labels=["x","x'"])
        scatter_with_histograms(y,yp, bins=bins,labels=["y","y'"])
    else:
        pass
    
    print(len(x))
    # print(np.shape(x))
    
    # plt.scatter([a*1e3 for a in x],[b*1e6 for b in _x],facecolors='none', edgecolors='black')
    # plt.xlabel("x [mm]")
    # plt.ylabel("x' [$\mu$rad]")
    # plt.show()
    
    # plt.scatter([a*1e3 for a in y],[b*1e6 for b in _y],facecolors='none', edgecolors='black')
    # plt.xlabel("y [mm]")
    # plt.ylabel("y' [$\mu$rad]")
    # plt.show()
    
    return data
    # x = np.loadtxt(file, dtype=str, comments=None, skiprows=1, usecols=(0))
    # _x = np.loadtxt(file, dtype=str, comments=None, skiprows=1, usecols=(1))
    # y = np.loadtxt(file, dtype=str, comments=None, skiprows=1, usecols=(2))
    # _y = np.loadtxt(file, dtype=str, comments=None, skiprows=1, usecols=(3))
    # E = np.loadtxt(file, dtype=str, comments=None, skiprows=1, usecols=(4))

def scatter_with_histograms(x, y, bins=10,labels=[None,None]):
    """
    Create a 2D scatter plot with histograms of the values across each axis and
    calculate the FWHM of each histogram.
    
    Parameters:
    x (list or array-like): The x-values of the scatter plot.
    y (list or array-like): The y-values of the scatter plot.
    bins (int): The number of bins for the histograms (default is 10).
    
    Returns:
    tuple: A tuple containing the FWHM of the x and y histograms.
    """
    # Create a figure with a grid of subplots
    fig = plt.figure(figsize=(10, 10))
    grid = plt.GridSpec(4, 4, hspace=0.4, wspace=0.4)

    # Main scatter plot
    scatter_ax = fig.add_subplot(grid[1:4, 0:3])
    scatter_ax.scatter(x, y,facecolors='none', edgecolors='black')
    scatter_ax.set_xlabel(labels[0])
    scatter_ax.set_ylabel(labels[1])

    # Histogram for x-axis
    x_hist_ax = fig.add_subplot(grid[0, 0:3], sharex=scatter_ax)
    x_hist, x_bin_edges, _ = x_hist_ax.hist(x, bins=bins, color='gray')
    x_bin_centers = (x_bin_edges[:-1] + x_bin_edges[1:]) / 2
    
    # Plot the line profile
    x_hist_ax.plot(x_bin_centers, x_hist, '--', color='black')
    
    x_hist_ax.set_ylabel('Count')
    x_hist_ax.set_title(labels[0])

    # Calculate FWHM for x-axis histogram
    # x_fwhm = calculate_fwhm(x_hist, x_bin_edges) / 2
    # x_fwhm = FWarbValue.getFWatValue(,dx,dy,frac=0.5,cuts='xy'
    # x_hist_ax.annotate(f'FWHM: {x_fwhm:.2f}', xy=(0.95, 0.95), xycoords='axes fraction', ha='right', va='top', fontsize=12)

    # Histogram for y-axis
    y_hist_ax = fig.add_subplot(grid[1:4, 3], sharey=scatter_ax)
    y_hist, y_bin_edges, _ = y_hist_ax.hist(y, bins=bins, orientation='horizontal', color='gray')
    y_bin_centers = (y_bin_edges[:-1] + y_bin_edges[1:]) / 2
    
    # Plot the line profile
    y_hist_ax.plot(y_hist,y_bin_centers, '--', color='black')
    # y_hist_ax.plot(y_hist, y_bin_centers, marker='o', linestyle='-', color='gray')
    
    y_hist_ax.set_xlabel('Count')
    y_hist_ax.set_title(labels[1])

    # Calculate FWHM for y-axis histogram
    # y_fwhm = calculate_fwhm(y_hist, y_bin_edges) / 2
    # y_hist_ax.annotate(f'FWHM: {y_fwhm:.2f}', xy=(0.95, 0.95), xycoords='axes fraction', ha='right', va='top', fontsize=12)


    plt.show()

    # # # Calculate the 2D histogram
    # histogram, xedges, yedges = np.histogram2d(x, y, bins=bins, range=None)

    # dx = xedges[1]-xedges[0]
    # dy = yedges[1]-yedges[0]

    # x_fwhm, y_fwhm = FWarbValue.getFWatValue(histogram,dx,dy,frac=0.5,cuts='xy',centered=True,smoothing='gauss')
    # x_fwhm, y_fwhm = x_fwhm / 2, y_fwhm / 2                                         
    
    # # Plot the 2D histogram as an image
    # fig, ax = plt.subplots()
    # cax = ax.imshow(histogram.T, origin='lower', cmap='viridis', extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]],aspect='auto')
    # fig.colorbar(cax, ax=ax, label='Counts')
    # ax.set_xlabel(labels[0])
    # ax.set_ylabel(labels[1])
    # # ax.set_title('2D Histogram of Scatter Plot')
    # plt.show()
    
    # x_fwhm, y_fwhm = FWarbValue.getFWatValue(,dx,dy,frac=0.5,cuts='xy'
    
    # return x_fwhm, y_fwhm

def calculate_fwhm(hist, bin_edges):
    """
    Calculate the full-width at half-maximum (FWHM) of a histogram.
    
    Parameters:
    hist (array-like): The histogram counts.
    bin_edges (array-like): The edges of the histogram bins.
    
    Returns:
    float: The full-width at half-maximum (FWHM).
    """
    half_max = np.max(hist) / 2
    # Calculate bin centers
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    
    # # Plot the line profile
    # plt.plot(bin_centers, hist, marker='o', linestyle='-')
    # plt.xlabel('Value')
    # plt.ylabel('Count')
    # plt.title('Line Profile of Histogram')
    # plt.grid(True)
    # # plt.show()


    # Find the points where the histogram crosses half of the maximum value
    above_half_max = np.where(hist >= half_max)[0]

    if len(above_half_max) > 1:
        fwhm = bin_centers[above_half_max[-1]] - bin_centers[above_half_max[0]]
    else:
        fwhm = 0

    return fwhm


ne = 30000
np = 15

eFiles = ['/user/home/srw2/SRW/experiments/BEUVphaseSpace/data/WBSi_ne' + str(ne) + '/res_int_pr_me.dat' + str(n) + 'electron_phase_space.csv' for n in range(1,np)]

# ebeamData = []
xSize = []
xDiv = []
ySize = []
yDiv = []
eSpread = []

for i,ef in enumerate(eFiles):
    print("analysing data from processor #", i+1)
    data = electronPhaseSpace(ef,bins=50,plot=False)
    
    xSize.append([d[0] for d in data])
    xDiv.append([d[1] for d in data])
    ySize.append([d[2] for d in data])
    yDiv.append([d[3] for d in data])
    eSpread.append([d[4] for d in data])
    
    # x = np.loadtxt(file, dtype=str, comments=None, skiprows=1, usecols=(0))
    # _x = np.loadtxt(file, dtype=str, comments=None, skiprows=1, usecols=(1))
    # y = np.loadtxt(file, dtype=str, comments=None, skiprows=1, usecols=(2))
    # _y = np.loadtxt(file, dtype=str, comments=None, skiprows=1, usecols=(3))
    # E = np.loadtxt(file, dtype=str, comments=None, skiprows=1, usecols=(4))


# x = [d[0] for d in data]
# _x = [d[1] for d in data]
# y = [d[2] for d in data]
# _y = [d[3] for d in data]
# elecE = [d[4] for d in data]

xSize = [x for xs in xSize for x in xs]
xDiv = [x for xs in xDiv for x in xs]
ySize = [x for xs in ySize for x in xs]
yDiv = [x for xs in yDiv for x in xs]

# xsize, xdiv = scatter_with_histograms([a*1e6 for a in xSize],[b*1e6 for b in xDiv], bins=60,labels=["x","x'"])
# ysize, ydiv = scatter_with_histograms([a*1e6 for a in ySize],[b*1e6 for b in yDiv], bins=60,labels=["y","y'"])
scatter_with_histograms([a*1e6 for a in xSize],[b*1e6 for b in xDiv], bins=60,labels=["x","x'"])
scatter_with_histograms([a*1e6 for a in ySize],[b*1e6 for b in yDiv], bins=60,labels=["y","y'"])


tiffs = False
EforS = False

# path = 'wavefield_1.pkl'
path = '/user/home/srw2/SRW/experiments/BEUVphaseSpace/data/'
#slit sizes]
wl = 6.7e-9

# planes = ['WBS_i', 'WBS_e',
#           'M1_i', 'M1_e',
#           'PGM_i', 'PGM_e',
#           'EA_i', 'EA_e',
#           'M3_i', 'M3_e',
#           'SSA_i', 'SSA_e',
#           'mask_i']
planes = ['WBSi_ne100',
          'WBSi_ne1000',
          'WBSi_ne2000'
          # 'WBSi_ne100',
          ]


# S = 300
# sX = [25,50,75,100,125,150,175,200,225,250,300,350,500]
# sY = np.full_like(sX,200)
# files = [path + p + '/' + p + 'Efields.pkl' for p in planes]
# [path + 'beforeBDA_efield_sx' + str(sx) + 'sy' + str(sy) + '/beforeBDA_efield_sx' + str(sx) + 'sy' + str(sy) + 'Efields.pkl' for sx,sy in zip(sX,sY)]


eFiles = [path + p + '/' + 'res_int_pr_me.datelectron_phase_space.csv' for p in planes]

data = [electronPhaseSpace(f,bins=40) for f in eFiles]

picks = [pickle.load(open(f, 'rb')) for f in files]

if EforS:
    Eh = [p[0] for p in picks]
    Ev = [p[1] for p in picks]
    dx = [p[4] for p in picks]
    dy = [p[5] for p in picks]

else:
    EhR = [p[0] for p in picks]
    EhI = [p[1] for p in picks]
    EvR = [p[2] for p in picks]
    EvI = [p[3] for p in picks]
    res = [(p[4],p[5]) for p in picks]


    Eh = [ExR + ExI*1j for ExR,ExI in zip(EhR,EhI)]
    Ev = [EyR + EyI*1j for EyR,EyI in zip(EvR,EvI)]#EvR + EvI*1j

# E = Eh[0] + Ev[0]    
# print(np.shape(E))
# Combine into a single array
for i,f in enumerate(files):
    print(planes[i])
    
    if tiffs:
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
    else:
        E = np.stack((Eh[i], Ev[i]), axis=-1)
        try:
            dx,dy = res[i][0],res[i][1]
        except:
            pass
        # print(np.shape(E))
        # # Plot total intensity and phase
        I, P = plot_total_intensity_and_phase(E, dx, dy)
        
    # E = np.stack((Eh[i], Ev[i]), axis=-1)
    # dx,dy = res[i][0],res[i][1]
    
    # print(np.shape(E))
    # # Plot total intensity and phase
    # I, P = plot_total_intensity_and_phase(E, dx, dy)
    
    intensity_threshold = np.max(I) / (e**2)
    
    print('Threshold I')
    print(intensity_threshold)
    
    # Calculate phase
    # phase = calculate_phase(E)
    
    
    # Calculate the total phase
    phase_total = P
    intensity_total = I
    phase_total = np.unwrap(phase_total, axis=0)#,discont=2*np.pi)#, period=np.pi)
    phase_total = np.unwrap(phase_total, axis=1)#,discont=2*np.pi)#, period=np.pi)
    
    # plt.plot(np.unwrap(phase_total[np.shape(phase_total)[0]//2,:]))#,period = np.pi))#, discont=np.pi))
    # plt.show()
    print('shape of phase: ', np.shape(phase_total))
    
    # Calculate the phase gradient (partial derivative of the total phase)
    """For two dimensional arrays, the return will be two arrays ordered by
    axis. In this example the first array stands for the gradient in
    rows and the second one in columns direction:"""

    # >>> np.gradient(np.array([[1, 2, 6], [3, 4, 5]], dtype=float))
    # [array([[ 2.,  2., -1.],
    #        [ 2.,  2., -1.]]), array([[1. , 2.5, 4. ],
    #        [1. , 1. , 1. ]])]
                                     
    # gradient_x = sobel(phase_total, axis=0) / dx
    # gradient_y = sobel(phase_total, axis=1) / dy
    # gradient_x = np.gradient(phase_total, axis=0) / dx
    # gradient_y = np.gradient(phase_total, axis=1) / dy
    
        
    ny, nx = I.shape
    # print('here')
    # print(nx,ny)
    x = np.linspace(-nx//2, nx//2, nx) * dx
    y = np.linspace(-ny//2, ny//2, ny) * dy
    X, Y = np.meshgrid(x, y)
    
    # Plot intensity and phase
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))
    
    im0 = axs[0].imshow(intensity_total, extent=[x.min(), x.max(), y.min(), y.max()], origin='lower',aspect='auto')
    axs[0].set_title('Total Intensity')
    fig.colorbar(im0, ax=axs[0])
    
    im1 = axs[1].imshow(P, extent=[x.min(), x.max(), y.min(), y.max()], origin='lower',aspect='auto')
    axs[1].set_title('Total Phase')
    fig.colorbar(im1, ax=axs[1])
    
    plt.tight_layout()
    plt.show()
    
    
    fig, ax = plt.subplots(1,3)
    p2d = ax[1].imshow(phase_total,aspect='auto')
    
    divider = make_axes_locatable(ax[1])
    cax = divider.append_axes("right", size="5%", pad=0.05)
    #_cax = divider.append_axes("right", size="0%", pad=0.0)
    plt.colorbar(p2d, cax=cax, orientation='vertical',label='Phase [$\phi$]')
    # ax[1].colorbar()
    ax[1].set_title('Unwrapped phase')
    # plt.show()
    
    
    gradient_x, gradient_y = phase_gradient_from_center(phase_total,dx,dy) #np.gradient(phase_total)
    
    # print(np.shape(X))
    # print(np.shape(Y))
    
    ax[0].plot(phase_total[np.shape(phase_total)[0]//2,:]/np.max(phase_total[np.shape(phase_total)[0]//2,:]))
    ax[0].plot(gradient_x[np.shape(phase_total)[0]//2,:])
    ax[0].set_title('x')
    ax[2].plot(phase_total[:,np.shape(phase_total)[1]//2]/np.max(phase_total[:,np.shape(phase_total)[1]//2]))
    ax[2].plot(gradient_y[:,np.shape(phase_total)[1]//2])
    ax[2].set_title('y')
    plt.tight_layout()
    plt.show()
        
    gradient_x[np.abs(intensity_total) < intensity_threshold] = 0
    gradient_y[np.abs(intensity_total) < intensity_threshold] = 0
    
    grad_thresh = np.pi
    
    gradient_x[np.abs(gradient_x) >= grad_thresh] = 0
    gradient_y[np.abs(gradient_y) >= grad_thresh] = 0
    
    
    # plt.imshow(gradient_x,aspect='auto')
    # plt.colorbar()
    # plt.title('phase gradient (x) - after')
    # plt.show()
    
    # plt.imshow(gradient_y,aspect='auto')
    # plt.colorbar()
    # plt.title('phase gradient (y) - after')
    # plt.show()
    
    
    X[np.abs(intensity_total) < intensity_threshold] = 0
    Y[np.abs(intensity_total) < intensity_threshold] = 0
    
    X[np.abs(gradient_x) >= grad_thresh] = 0
    Y[np.abs(gradient_y) >= grad_thresh] = 0
    
    
    # plt.imshow(X,aspect='auto')
    # plt.colorbar()
    # plt.title('X')
    # plt.show()
    # plt.imshow(Y,aspect='auto')
    # plt.colorbar()
    # plt.title('Y')
    # plt.show()
    
    # Calculate phase gradients
    # gradient_x, gradient_y, distance_from_center_x, distance_from_center_y = calculate_phase_gradient(phase, dx, dy)
    
    # Apply intensity threshold and get distances from center
    # intensity_threshold = 0.1  # Example threshold value
    # gradient_x, gradient_y, distance_from_center_x, distance_from_center_y = calculate_phase_gradient_threshold(E, dx, dy, intensity_threshold)
    
    # # Plot phase gradient vs distance
    # plot_divergence_vs_distance(gradient_x, gradient_y, distance_from_center_x, distance_from_center_y)
    
    # Compute divergences
    divergence_x, divergence_y = compute_divergence_from_phase_gradient(wl,gradient_x / dx, gradient_y / dy,dx,dy)
    
    # Plot divergence vs distance
    # print('\n here')
    # print('helllloooooooo')
    plot_divergence_vs_distance(divergence_x, divergence_y,X, Y,title = planes[i])
