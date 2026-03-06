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
    
    # print(len(x))
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

def check_wavefield_sampling(intensity_array, dx,dy, threshold=0.01, plot_spectrum=True):
    """
    Check if the sampling of a 2D intensity array is adequate based on its spatial frequency spectrum,
    taking into account the pixel size.
    
    Parameters:
    - intensity_array: 2D numpy array representing the intensity of the wavefield.
    - pixel_size: Tuple (pixel_size_x, pixel_size_y), the physical size of each pixel in real space (in meters, microns, etc.).
    - threshold: Float, relative threshold to determine if high-frequency components near the Nyquist limit are significant.
                 Default is 0.01 (1% of total power).
    - plot_spectrum: Boolean, if True, plot the 2D spatial frequency spectrum for visualization.
    
    Returns:
    - Boolean: True if the sampling is adequate, False if undersampling is detected.
    """
    
    pixel_size = dy,dx
    # Get the dimensions of the intensity array
    nyquist_limit_x, nyquist_limit_y = intensity_array.shape[0] // 2, intensity_array.shape[1] // 2
    
    # Compute the 2D Fourier Transform of the intensity array
    fft_result = np.fft.fftshift(np.fft.fft2(intensity_array))
    
    # Compute the magnitude (or power) spectrum
    power_spectrum = np.abs(fft_result) ** 2
    
    # Sum of total power in the spectrum
    total_power = np.sum(power_spectrum)
    
    # Define the spatial frequency axis in real units
    kx = np.fft.fftfreq(intensity_array.shape[0], d=pixel_size[0])
    ky = np.fft.fftfreq(intensity_array.shape[1], d=pixel_size[1])
    
    # Shift the frequencies to center at zero
    kx = np.fft.fftshift(kx)
    ky = np.fft.fftshift(ky)
    
    # Generate the grid of spatial frequencies
    KX, KY = np.meshgrid(kx, ky)
    spatial_frequencies = np.sqrt(KX**2 + KY**2)
    
    # Nyquist frequency in real units (1 / (2 * pixel_size))
    nyquist_frequency_x = 1 / (2 * pixel_size[0])
    nyquist_frequency_y = 1 / (2 * pixel_size[1])
    
    # Define the Nyquist region: frequencies higher than this would indicate undersampling
    nyquist_region = (spatial_frequencies >= nyquist_frequency_x) | (spatial_frequencies >= nyquist_frequency_y)
    
    # Analyze power in the Nyquist region
    high_freq_power = np.sum(power_spectrum[nyquist_region])
    
    # Calculate the fraction of total power in high frequencies
    fraction_high_freq_power = high_freq_power / total_power
    
    # If the high frequency power exceeds the threshold, undersampling is detected
    is_sampling_adequate = fraction_high_freq_power < threshold
    
    if plot_spectrum:
        plt.figure(figsize=(6, 6))
        plt.imshow(np.log1p(power_spectrum), cmap='hot', extent=[kx[0], kx[-1], ky[0], ky[-1]])
        plt.title('2D Spatial Frequency Spectrum (Log Scale)')
        plt.colorbar(label='Log(Power)')
        plt.xlabel('kx (1 / unit length)')
        plt.ylabel('ky (1 / unit length)')
        plt.show()
    
    return is_sampling_adequate

# def check_wavefield_sampling(wavefield, dx, dy, oversampling_factor=2):
#     """
#     Check if the 2D wavefield (either phase or intensity) is adequately sampled.
    
#     Parameters:
#     - wavefield: 2D numpy array representing either the intensity or phase of the wavefield.
#     - dx: The spatial sampling interval in the x direction (meters/pixel).
#     - dy: The spatial sampling interval in the y direction (meters/pixel).
#     - oversampling_factor: The required factor above the Nyquist frequency to be considered oversampled.
#                            Default is 2 (i.e., twice the Nyquist frequency).
    
#     Returns:
#     - A boolean value indicating whether the wavefield is adequately sampled.
#     """
#     # Perform 2D Fourier transform of the wavefield
#     wavefield_fft = np.fft.fftshift(np.fft.fft2(wavefield))
    
#     # Get the dimensions of the wavefield
#     Nx, Ny = wavefield.shape
    
#     # Generate the frequency grids in x and y directions using the correct size
#     fx = np.fft.fftshift(np.fft.fftfreq(Nx, d=dx))
#     fy = np.fft.fftshift(np.fft.fftfreq(Ny, d=dy))
    
#     # Now create a meshgrid of the correct size to match the wavefield dimensions
#     FX, FY = np.meshgrid(fx, fy, indexing='ij')
    
#     # Calculate the 2D spatial frequencies (magnitude of spatial frequency vector)
#     freq_magnitude = np.sqrt(FX**2 + FY**2)
    
#     # Get the magnitude of the Fourier coefficients (spectrum of the wavefield)
#     wavefield_spectrum = np.abs(wavefield_fft)
    
#     # Find the highest significant spatial frequency
#     # Apply a threshold to ignore very small (insignificant) values in the spectrum
#     spectrum_threshold = np.max(wavefield_spectrum) * 0.01
#     significant_frequencies = freq_magnitude[wavefield_spectrum > spectrum_threshold]
    
#     if significant_frequencies.size > 0:
#         max_freq_wavefield = np.max(significant_frequencies)
#     else:
#         max_freq_wavefield = 0  # If no significant frequencies, set to 0
    
#     # Nyquist frequency
#     fx_nyquist = 1 / (2 * dx)
#     fy_nyquist = 1 / (2 * dy)
#     f_nyquist = np.sqrt(fx_nyquist**2 + fy_nyquist**2)
    
#     # Check if the maximum frequency is less than Nyquist frequency / oversampling_factor
#     adequately_sampled = max_freq_wavefield < (f_nyquist / oversampling_factor)
    
#     # Print results
#     print("Max spatial frequency (wavefield):", max_freq_wavefield)
#     print("Nyquist frequency:", f_nyquist)
#     print("Oversampling factor:", oversampling_factor)
#     print("Adequately sampled:", adequately_sampled)
    
#     # Plot the 2D frequency spectrum and overlay the Nyquist and maximum spatial frequencies
#     plt.figure(figsize=(8, 6))
#     plt.imshow(np.log1p(wavefield_spectrum), extent=[fx[0], fx[-1], fy[0], fy[-1]], origin='lower', cmap='inferno',aspect='auto')
#     plt.colorbar(label='Log Spectrum Intensity')
    
#     # Mark the max spatial frequency and Nyquist frequency on the plot
#     plt.contour(FX, FY, freq_magnitude, levels=[max_freq_wavefield], colors='blue', linestyles='dashed', label='Max Spatial Frequency')
#     plt.contour(FX, FY, freq_magnitude, levels=[f_nyquist], colors='green', linestyles='solid', label='Nyquist Frequency')
    
#     # Add text annotations
#     plt.text(0.05, 0.95, f"Max Freq: {max_freq_wavefield:.2f}", color='blue', fontsize=12, transform=plt.gca().transAxes)
#     plt.text(0.05, 0.9, f"Nyquist Freq: {f_nyquist:.2f}", color='green', fontsize=12, transform=plt.gca().transAxes)
#     if adequately_sampled:
#         plt.text(0.05, 0.85, f"OVERSAMPLED", color='white', fontsize=12, transform=plt.gca().transAxes)
#     else:
#         plt.text(0.05, 0.85, f"UNDERSAMPLED", color='white', fontsize=12, transform=plt.gca().transAxes)
        
    
#     # Labels and title
#     plt.title("2D Frequency Spectrum")
#     plt.xlabel("Spatial Frequency in X (1/m)")
#     plt.ylabel("Spatial Frequency in Y (1/m)")
#     plt.show()
    
#     # plt.imshow(freq_magnitude)
#     # plt.show()
    
#     return adequately_sampled


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


# ne = 30000
# np = 15

# eFiles = ['/user/home/opt/xl/xl/experiments/BEUVphaseSpace/data/WBSi_ne' + str(ne) + '/res_int_pr_me.dat' + str(n) + 'electron_phase_space.csv' for n in range(1,np)]

# # ebeamData = []
# xSize = []
# xDiv = []
# ySize = []
# yDiv = []
# eSpread = []

# for i,ef in enumerate(eFiles):
#     print("analysing data from processor #", i+1)
#     data = electronPhaseSpace(ef,bins=50,plot=False)
    
#     xSize.append([d[0] for d in data])
#     xDiv.append([d[1] for d in data])
#     ySize.append([d[2] for d in data])
#     yDiv.append([d[3] for d in data])
#     eSpread.append([d[4] for d in data])
    
#     # x = np.loadtxt(file, dtype=str, comments=None, skiprows=1, usecols=(0))
#     # _x = np.loadtxt(file, dtype=str, comments=None, skiprows=1, usecols=(1))
#     # y = np.loadtxt(file, dtype=str, comments=None, skiprows=1, usecols=(2))
#     # _y = np.loadtxt(file, dtype=str, comments=None, skiprows=1, usecols=(3))
#     # E = np.loadtxt(file, dtype=str, comments=None, skiprows=1, usecols=(4))


# # x = [d[0] for d in data]
# # _x = [d[1] for d in data]
# # y = [d[2] for d in data]
# # _y = [d[3] for d in data]
# # elecE = [d[4] for d in data]

# xSize = [x for xs in xSize for x in xs]
# xDiv = [x for xs in xDiv for x in xs]
# ySize = [x for xs in ySize for x in xs]
# yDiv = [x for xs in yDiv for x in xs]

# # xsize, xdiv = scatter_with_histograms([a*1e6 for a in xSize],[b*1e6 for b in xDiv], bins=60,labels=["x","x'"])
# # ysize, ydiv = scatter_with_histograms([a*1e6 for a in ySize],[b*1e6 for b in yDiv], bins=60,labels=["y","y'"])
# scatter_with_histograms([a*1e6 for a in xSize],[b*1e6 for b in xDiv], bins=60,labels=["x","x'"])
# scatter_with_histograms([a*1e6 for a in ySize],[b*1e6 for b in yDiv], bins=60,labels=["y","y'"])


tiffs = False
EforS = False

# path = 'wavefield_1.pkl'
path = '/user/home/opt/xl/xl/experiments/XFM_ptycho/data/phaseSpace/'
#slit sizes]
wl = 0.1486627e-9

planes = [
           'initial', 
           'ap1_ex',
           # 'ap2_in', 
           'ap2_ex',
           'ap3_in',
           'ap3_ex',
           'lens_ex',
           'FZP_in',
           'FZP_ex',
          # 'detector_in',
          # 'detector_ex'
          # 'afterFZP',
          # 'atDetector'
          # 'M1_i', 'M1_e',
          # 'PGM_i', 'PGM_e',
          # 'EA_i', 'EA_e',
          # 'M3_i', 'M3_e',
          # 'SSA_i', 'SSA_e',
          # 'mask_i'
          ]

res = [
        (1.234567901234568e-06,1.234567901234568e-06),
        (1.54320987654321e-07,1.54320987654321e-07),
        # (6.290518788015208e-07,6.290672481611053e-07),
        (1.572629697003802e-07,1.5726681204027632e-07),
        (6.340081524712266e-07,6.340241462622868e-07),
        (6.340081524712265e-09,6.340241462622868e-09),
        (6.340081524712265e-09,6.340241462622868e-09),
        (1.2684513318070552e-08,1.2684833303633704e-08),
       # (1.2684513318070552e-08,1.2684833303633704e-08),
       # (1.2842188865566015e-06,1.2842512828727487e-06),
       # (6.241303788665083e-05,6.24146123476156e-05)
       ]
# planes = ['WBSi_ne100',
#           'WBSi_ne1000',
#           'WBSi_ne2000'
#           # 'WBSi_ne100',
#           ]


# S = 300
# sX = [25,50,75,100,125,150,175,200,225,250,300,350,500]
# sY = np.full_like(sX,200)
# files = [path + p + '/' + p + 'Efields.pkl' for p in planes]
# [path + 'beforeBDA_efield_sx' + str(sx) + 'sy' + str(sy) + '/beforeBDA_efield_sx' + str(sx) + 'sy' + str(sy) + 'Efields.pkl' for sx,sy in zip(sX,sY)]


# eFiles = [path + p + '/' + 'res_int_pr_me.datelectron_phase_space.csv' for p in planes]

# data = [electronPhaseSpace(f,bins=40) for f in eFiles]

# picks = [pickle.load(open(f, 'rb')) for f in files]

# if EforS:
#     Eh = [p[0] for p in picks]
#     Ev = [p[1] for p in picks]
#     dx = [p[4] for p in picks]
#     dy = [p[5] for p in picks]

# else:
#     EhR = [p[0] for p in picks]
#     EhI = [p[1] for p in picks]
#     EvR = [p[2] for p in picks]
#     EvI = [p[3] for p in picks]
#     res = [(p[4],p[5]) for p in picks]


#     Eh = [ExR + ExI*1j for ExR,ExI in zip(EhR,EhI)]
#     Ev = [EyR + EyI*1j for EyR,EyI in zip(EvR,EvI)]#EvR + EvI*1j

# E = Eh[0] + Ev[0]    
# print(np.shape(E))
# Combine into a single array
for i,f in enumerate(planes):
    print('\n')
    print(planes[i])
    
    # if tiffs:
    I = tifffile.imread(path + f + '/' + 'intensity.tif')
    P = tifffile.imread(path + f + '/' + 'phase.tif')
    
    dx, dy = res[i][0], res[i][1]
    
    # Ifile = path + f + '/' + 'res_int_pr_se.dat'
    # nx = str(np.loadtxt(Ifile, dtype=str, comments=None, skiprows=6, max_rows=1, usecols=(0)))[1:]
    # ny = str(np.loadtxt(Ifile, dtype=str, comments=None, skiprows=9, max_rows=1, usecols=(0)))[1:]
    # xMax = str(np.loadtxt(Ifile, dtype=str, comments=None, skiprows=5, max_rows=1, usecols=(0)))[1:]
    # xMin = str(np.loadtxt(Ifile, dtype=str, comments=None, skiprows=4, max_rows=1, usecols=(0)))[1:]
    # yMax = str(np.loadtxt(Ifile, dtype=str, comments=None, skiprows=8, max_rows=1, usecols=(0)))[1:]
    # yMin = str(np.loadtxt(Ifile, dtype=str, comments=None, skiprows=7, max_rows=1, usecols=(0)))[1:]
    # rx = float(xMax)-float(xMin)
    # ry = float(yMax)-float(yMin)
    # dx = np.divide(rx,float(nx))
    # dy = np.divide(ry,float(ny))
    
    # else:
    #     E = np.stack((Eh[i], Ev[i]), axis=-1)
    #     try:
    #         dx,dy = res[i][0],res[i][1]
    #     except:
    #         pass
    #     # print(np.shape(E))
    #     # # Plot total intensity and phase
    #     I, P = plot_total_intensity_and_phase(E, dx, dy)
        
    # # E = np.stack((Eh[i], Ev[i]), axis=-1)
    # # dx,dy = res[i][0],res[i][1]
    
    # # print(np.shape(E))
    # # # Plot total intensity and phase
    # # I, P = plot_total_intensity_and_phase(E, dx, dy)
    
    intensity_threshold = np.max(I) / (e**2)
    
    # print('Threshold I')
    # print(intensity_threshold)
    
    # Calculate phase
    # phase = calculate_phase(E)
    
    
    # Calculate the total phase
    phase_total = P
    intensity_total = I
    phase_total = np.unwrap(phase_total, axis=0,period=2*np.pi)#,discont=2*np.pi)#, period=np.pi)
    phase_total = np.unwrap(phase_total, axis=1,period=2*np.pi)#,discont=2*np.pi)#, period=np.pi)
    
    if np.min(phase_total) < 0:
        phase_total = phase_total + abs(np.min(phase_total))
    
    # # Calculate the center index for both dimensions
    # center_x_index = I.shape[1] // 2
    # center_y_index = I.shape[0] // 2
    
    # # Extract the x and y line profiles at the center
    # x_profile = I[center_y_index, :]
    # y_profile = I[:, center_x_index]
    
    # # Function to find the crossing points from the center
    # def find_crossing_points(profile, threshold):
    #     center_index = len(profile) // 2
    #     profile_left, profile_right = profile[:center_index], profile[center_index:]
        
    #     cross_left_indices = np.where(profile_left >= threshold)[0]
    #     x_min = cross_left_indices[-1] if len(cross_left_indices) > 0 else 0
        
    #     cross_right_indices = np.where(profile_right >= threshold)[0]
    #     x_max = center_index + cross_right_indices[0] if len(cross_right_indices) > 0 else len(profile) - 1
        
    #     return x_min, x_max
    
    # # Find the x-limits for the x and y profiles
    # x_min_x_profile, x_max_x_profile = find_crossing_points(x_profile, intensity_threshold)
    # x_min_y_profile, x_max_y_profile = find_crossing_points(y_profile, intensity_threshold)

    print('Central wrapped phase value: ', P[np.shape(phase_total)[0]//2,np.shape(phase_total)[1]//2])    
    print('Central unwrapped phase value: ', phase_total[np.shape(phase_total)[0]//2,np.shape(phase_total)[1]//2])    
    print('Max unwrapped phase value: ', np.max(phase_total))#[np.shape(phase_total)[0]//2,:]))

    plt.plot(np.unwrap(phase_total[np.shape(phase_total)[0]//2,:])/np.max(phase_total))#,period = np.pi))#, discont=np.pi))
    plt.plot(I[np.shape(phase_total)[0]//2,:]/np.max(I))
    plt.title('x')
    # plt.xlim(x_min_x_profile,x_max_x_profile)
    plt.show()
    plt.plot(np.unwrap(phase_total[:,np.shape(phase_total)[1]//2])/np.max(phase_total))#,period = np.pi))#, discont=np.pi))
    plt.plot(I[:,np.shape(phase_total)[1]//2]/np.max(I))
    plt.title('y')
    # plt.xlim(x_min_y_profile,x_max_y_profile)
    plt.show()
    # print('shape of phase: ', np.shape(phase_total))
    
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
    
    ax[0].plot(phase_total[np.shape(phase_total)[0]//2,:]/abs(np.max(phase_total[np.shape(phase_total)[0]//2,:])))
    ax[0].plot(gradient_x[np.shape(phase_total)[0]//2,:])
    ax[0].set_title('x')
    ax[2].plot(phase_total[:,np.shape(phase_total)[1]//2]/np.max(phase_total[:,np.shape(phase_total)[1]//2]))
    ax[2].plot(gradient_y[:,np.shape(phase_total)[1]//2])
    ax[2].set_title('y')
    # ax[0].set_xlim(1457,1460)
    # ax[2].set_xlim(1457,1460)
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
    
    check_wavefield_sampling(I, dx, dy)
