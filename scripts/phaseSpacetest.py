#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 10:49:18 2024

@author: jerome
"""

import numpy as np
import matplotlib.pyplot as plt
from math import e
import tifffile
import matplotlib.gridspec as gridspec
from mpl_toolkits.axes_grid1 import make_axes_locatable
import csv
import pickle
#from getPhaseSpace_threshold import phase_gradient_from_center, compute_divergence_from_phase_gradient, plot_divergence_vs_distance, plot_total_intensity_and_phase
import FWatArbValue

def electronPhaseSpace(file,bins,plot=True,savePath=None):
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
            # print(row)
            # print([float(value) for value in row])
            data.append([float(value) for value in row])
    
    # # Convert the list to a numpy array
    # data_array = np.array(data)
    # print(np.shape(data_array))
    # print(np.shape(data))
    print(type(data))
    
    x = [d[0] for d in data]
    _x = [d[1] for d in data]
    y = [d[2] for d in data]
    _y = [d[3] for d in data]
    elecE = [d[4] for d in data]
    
    print(type(x))
    
    if savePath:
        savePathX = savePath + '_x_'
        savePathY = savePath + '_y_'
        
    if plot:
        scatter_with_histograms([a*1e6 for a in x],[b*1e6 for b in _x], bins=bins,labels=["x [$\mu$m]","x' [$\mu$rad]"],savePath=savePathX)
        scatter_with_histograms([a*1e6 for a in y],[b*1e6 for b in _y], bins=bins,labels=["y [$\mu$m]","y' [$\mu$rad]"],savePath=savePathY)
    else:
        pass
    
    # plt.scatter([a*1e3 for a in x],[b*1e6 for b in _x],facecolors='none', edgecolors='black')
    # plt.xlabel("x [mm]")
    # plt.ylabel("x' [$\mu$rad]")
    # plt.show()
    
    # plt.scatter([a*1e3 for a in y],[b*1e6 for b in _y],facecolors='none', edgecolors='black')
    # plt.xlabel("y [mm]")
    # plt.ylabel("y' [$\mu$rad]")
    # plt.show()
    
    return data

def scatter_with_histograms(x, y, bins=10,labels=[None,None],savePath=None):
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
    
    bins_method = 'auto'
#    'auto'
#    'fd'
#    'doane'
#    'scott'
#    'stone'
#    'rice'
#    'sturges'
#    'sqrt'
    # Create a figure with a grid of subplots
    fig = plt.figure(figsize=(4, 4))
    grid = plt.GridSpec(4, 4, hspace=0.4, wspace=0.4)
    
    labelSize = 8

    # Main scatter plot
    scatter_ax = fig.add_subplot(grid[1:4, 0:3])
    scatter_ax.scatter(x, y,facecolors='none', edgecolors='black')
    scatter_ax.set_xlabel(labels[0],fontsize=labelSize)
    scatter_ax.set_ylabel(labels[1],fontsize=labelSize)

    # Histogram for x-axis
    x_hist_ax = fig.add_subplot(grid[0, 0:3], sharex=scatter_ax)
    x_hist, x_bin_edges, _ = x_hist_ax.hist(x, bins=bins_method, color='gray')
    x_bin_centers = (x_bin_edges[:-1] + x_bin_edges[1:]) / 2
    
    # Plot the line profile
    x_hist_ax.plot(x_bin_centers, x_hist, '--', color='black')
    
    x_hist_ax.set_ylabel('Count',fontsize=labelSize)
#    x_hist_ax.set_title(labels[0],fontsize=labelSize)

    # Calculate FWHM for x-axis histogram
#    x_fwhm = calculate_fwhm(x_hist, x_bin_edges) / 2
    # x_fwhm = FWarbValue.getFWatValue(,dx,dy,frac=0.5,cuts='xy'
    
    # Histogram for y-axis
    y_hist_ax = fig.add_subplot(grid[1:4, 3], sharey=scatter_ax)
    y_hist, y_bin_edges, _ = y_hist_ax.hist(y, bins=bins_method, orientation='horizontal', color='gray')
    y_bin_centers = (y_bin_edges[:-1] + y_bin_edges[1:]) / 2
    
    # Plot the line profile
    y_hist_ax.plot(y_hist,y_bin_centers, '--', color='black')
    # y_hist_ax.plot(y_hist, y_bin_centers, marker='o', linestyle='-', color='gray')
    
    y_hist_ax.set_xlabel('Count',fontsize=labelSize)
#    y_hist_ax.set_title(labels[1],fontsize=labelSize)

    # Calculate FWHM for y-axis histogram
#    y_fwhm = calculate_fwhm(y_hist, y_bin_edges) / 2

    if savePath:
        plt.savefig(savePath, format='eps')
#    plt.show()

    # Calculate the 2D histogram
    histogram, xedges, yedges = np.histogram2d(x, y, bins=[x_bin_edges,y_bin_edges], range=None)
    dx = xedges[1]-xedges[0]
    dy = yedges[1]-yedges[0]

    x_fwhm, y_fwhm ,x_smooth, y_smooth= FWatArbValue.getFWatValue(histogram,dx,dy,frac=1/2,cuts='xy',centered=False,
                                                                  smoothing='gauss',
#                                                                  smoothing='savgol',
#                                                                  sparams=30,
#                                                                  show=True,
                                                                  show=False
                                                                  )
    x_fwhm, y_fwhm = x_fwhm / 2, y_fwhm / 2                                         
    
    x_hist_ax.annotate(f'FWHM: {x_fwhm:.2f}', xy=(0.95, 0.9), xycoords='axes fraction', ha='right', va='top', fontsize=labelSize-4)
    y_hist_ax.annotate(f'FWHM: {y_fwhm:.2f}', xy=(0.9, 0.98), xycoords='axes fraction', ha='right', va='top', fontsize=labelSize-4)

    # Plot the 2D histogram as an image
    fig, ax = plt.subplots()
    cax = ax.imshow(histogram.T, origin='lower', cmap='viridis', extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]],aspect='auto')
    fig.colorbar(cax, ax=ax, label='macro electrons')
    ax.set_xlabel(labels[0],fontsize=labelSize)
    ax.set_ylabel(labels[1],fontsize=labelSize)
    # ax.set_title('2D Histogram of Scatter Plot')
#    plt.text(int(nx)-int((1*int(nx))/5),int(ny)-int((4*int(ny))/20),f"nx: {int(nx)}", color='r',fontsize=fSize)
#    if savePath:
#        ax.savefig(savePath + 'HIST', format='eps')
    plt.show()
    
    print('Number of bins (x,y): ', (len(x_bin_edges),len(y_bin_edges)))
    print('FWHM of smoothed histogram (size, div):   ', (x_fwhm,y_fwhm))

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


bins = 70
ne = 4000
#100
#1000
#2000
#4000
#10000
#20000
#30000

dirPath = '/home/jerome/Documents/PhD/Data/electronBeam/'

file = dirPath + 'electron_phase_space_total_' + str(ne) + '.csv'

savePath ='/home/jerome/Documents/PhD/Data/electronBeam/phase_space_ne' + str(ne) + '_bins' + str(bins)

electronPhaseSpace(file,bins=bins,savePath = savePath)


ne20000_20 = (355.60328438567035, 45.74469105874871), (6.737057240609538, 1.7147195214560051)
ne20000_50 = (331.8963987599593, 39.20973519321311), (5.838782941861604, 1.7833083023142442)
ne20000_80 = (325.9696773535318, 39.209735193213135), (5.614214367174597, 1.80045549752881)
ne20000_100 = (343.74984157281335, 39.20973519321322), (5.838782941861581, 1.78330830231425)
ne20000_150 = (363.5055795942394, 38.33840774447515), (5.9884953249862605, 1.7375824484087508)