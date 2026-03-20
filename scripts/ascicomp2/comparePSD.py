#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 10:33:53 2025

@author: -
"""

import numpy as np
import matplotlib.pyplot as plt
from math import log10, floor
import tifffile
from scipy.interpolate import interp1d
from scipy.signal import savgol_filter, find_peaks

def round_sig(x, sig=2):
    if x != 0:
        return round(x, sig-int(floor(log10(abs(x))))-1)
    else:
        return x
    
def extract_roi(array, roi):
    """
    Extract the region of interest (ROI) from a 2D array using pixel indices.
    
    Parameters
    ----------
    array : np.ndarray
        2D input array.
    roi : tuple of four ints
        (y_start, y_end, x_start, x_end) in pixel coordinates.
        The slice will be array[y_start:y_end, x_start:x_end].
    
    Returns
    -------
    np.ndarray
        The sub-array corresponding to the ROI.
    """
    y1, y2, x1, x2 = roi
    return array[y1:y2, x1:x2]

def compute_horizontal_psd(roi_data,dx=1):
    """
    Compute the horizontal (x-direction) 1D PSD from a 2D ROI in a one-sided manner:
      1) For each row, perform the real-valued FFT (rfft) along x.
      2) Compute the power spectrum for each row.
      3) Average across all rows -> 1D PSD vs. frequency in x.
    
    Returns
    -------
    freq_x : np.ndarray
        1D array of spatial frequencies [cycles/pixel], from 0 to Nyquist.
        Zero frequency is at the left end.
    psd_x : np.ndarray
        1D array of PSD values (averaged over rows).
    """
    Ny, Nx = roi_data.shape
    
    # For rfft, the output length along x is Nx//2 + 1 (one-sided)
    n_half = Nx//2 + 1
    
    # Prepare an array to accumulate PSD from each row
    psd_rows = np.zeros((Ny, n_half), dtype=np.float64)
    
    for i in range(Ny):
        row = roi_data[i, :]
        # Real FFT along x
        fft_row = np.fft.rfft(row)  
        # Compute power
        psd_rows[i, :] = np.abs(fft_row)**2
    
    # Average across rows
    psd_x = psd_rows.mean(axis=0)
    
    # Frequency array (cycles per pixel)
    freq_x = np.fft.rfftfreq(Nx,d=dx)  # from 0 to 0.5 in steps of 1/Nx
    
    return freq_x, psd_x

def compute_vertical_psd(roi_data,dy=1):
    """
    Compute the vertical (y-direction) 1D PSD from a 2D ROI in a one-sided manner:
      1) For each column, perform rfft along y.
      2) Compute the power spectrum for each column.
      3) Average across all columns -> 1D PSD vs. frequency in y.
    
    Returns
    -------
    freq_y : np.ndarray
        1D array of spatial frequencies [cycles/pixel], from 0 to Nyquist.
        Zero frequency is at the left end.
    psd_y : np.ndarray
        1D array of PSD values (averaged over columns).
    """
    Ny, Nx = roi_data.shape
    
    # We'll transpose so columns become rows
    data_T = roi_data.T  # shape => (Nx, Ny)
    
    # For rfft along each "row" in data_T (which was originally a column)
    n_half = Ny // 2 + 1
    psd_cols = np.zeros((Nx, n_half), dtype=np.float64)
    
    for j in range(Nx):
        col = data_T[j, :]  # one column of the original
        fft_col = np.fft.rfft(col)
        psd_cols[j, :] = np.abs(fft_col)**2
    
    # Average across columns
    psd_y = psd_cols.mean(axis=0)
    
    # Frequencies in cycles/pixel for y
    freq_y = np.fft.rfftfreq(Ny,d=dy)
    
    return freq_y, psd_y

def psd_difference(freqA, psdA, freqB, psdB, n_points=300):
    """
    Compute the difference (A - B) between two 1D PSDs, taking care of 
    frequency mismatch by interpolating onto a common frequency axis.

    Parameters
    ----------
    freqA : np.ndarray
        Frequencies for PSD A (e.g., cycles/pixel, cycles/nm, etc.). Must be 1D.
    psdA : np.ndarray
        Power spectral density values for PSD A, same shape as freqA.
    freqB : np.ndarray
        Frequencies for PSD B, 1D.
    psdB : np.ndarray
        Power spectral density values for PSD B, same shape as freqB.
    n_points : int, optional
        Number of points in the common frequency grid.

    Returns
    -------
    freq_common : np.ndarray
        The common frequency array (length = n_points).
    psd_diff : np.ndarray
        The difference PSD_A(freq) - PSD_B(freq) at each point of freq_common.

    Notes
    -----
    - We only consider the overlapping frequency region where both PSDs exist.
    - Uses linear interpolation (np.interp). If you want more advanced interpolation, 
      you can use scipy.interpolate.interp1d with e.g., kind='cubic'.
    """

    # 1. Determine overlapping frequency range
    f_min = max(freqA.min(), freqB.min())
    f_max = min(freqA.max(), freqB.max())

    if f_min >= f_max:
        raise ValueError("No overlapping frequency range between the two PSDs.")

    # 2. Create a common frequency grid in the overlapping region
    freq_common = np.linspace(f_min, f_max, n_points)

    # 3. Interpolate PSD_A and PSD_B onto the common grid
    #    np.interp requires freq to be strictly increasing, so ensure freq arrays are sorted.
    sortA = np.argsort(freqA)
    sortB = np.argsort(freqB)
    
    freqA_sorted = freqA[sortA]
    psdA_sorted  = psdA[sortA]
    freqB_sorted = freqB[sortB]
    psdB_sorted  = psdB[sortB]

    # psdA_interp = np.interp(freq_common, freqA_sorted, psdA_sorted)
    # psdB_interp = np.interp(freq_common, freqB_sorted, psdB_sorted)

    fA = interp1d(freqA_sorted, psdA_sorted, kind='cubic', bounds_error=False, fill_value="extrapolate")
    fB = interp1d(freqB_sorted, psdB_sorted, kind='cubic', bounds_error=False, fill_value="extrapolate")
    
    psdA_interp = fA(freq_common)
    psdB_interp = fB(freq_common)


    # 4. Compute difference at each frequency
    psd_diff = psdA_interp / psdB_interp
    
    return freq_common, psd_diff


def find_prominent_frequencies(freq, psd, 
                               smooth=True,
                               window_length=9,
                               polyorder=3,
                               prominence=1.5,
                               distance=10,
                               height=None):
    """
    Identify the most prominent peaks (local maxima) in a 1D PSD curve.
    Optionally smooth the PSD to reduce noise before finding peaks.
    
    Parameters
    ----------
    freq : np.ndarray
        1D array of frequency values (e.g. cycles/nm).
    psd : np.ndarray
        1D array of PSD values corresponding to freq.
    smooth : bool, optional
        Whether to apply a Savitzky-Golay filter for smoothing (default=True).
    window_length : int, optional
        Window length for Savitzky-Golay filter (must be odd, default=9).
    polyorder : int, optional
        Polynomial order for Savitzky-Golay filter (default=3).
    prominence : float, optional
        Required prominence of peaks. Larger => fewer peaks (default=0.0).
    distance : int, optional
        Minimum horizontal distance (in number of points) between neighboring peaks.
        Larger => fewer peaks. Default=1.
    height : float or tuple, optional
        Required height of peaks. e.g., height=0.01 => only peaks >0.01. 
        Or a tuple (min, max). Default=None => no height constraint.
    
    Returns
    -------
    freq_peaks : np.ndarray
        Frequencies at which peaks occur.
    psd_peaks : np.ndarray
        PSD values at those peak frequencies.
    psd_smoothed : np.ndarray
        The smoothed PSD (if `smooth=True`), or original PSD (if `smooth=False`).
    peak_indices : np.ndarray
        Indices of the peaks in `psd_smoothed`.
    
    Notes
    -----
    - Savitzky-Golay smoothing can help reduce noise but can also shift or
      alter peak shapes if the window is too large.
    - You can tweak 'prominence', 'height', and 'distance' to filter out 
      smaller local maxima.
    - If your PSD array has zeros or extremely small values, you might want 
      to offset them (e.g., psd + 1e-14).
    """
    # Optional smoothing
    if smooth:
        # Ensure window_length is < length of psd and is odd
        window_length = min(window_length, len(psd) if len(psd)%2==1 else len(psd)-1)
        if window_length < 3:
            window_length = 3  # minimal odd window
        # Apply Savitzky-Golay filter
        psd_smoothed = savgol_filter(psd, window_length=window_length, polyorder=polyorder)
    else:
        psd_smoothed = psd
    
    # Find peaks in the smoothed PSD
    # 'prominence', 'distance', 'height' can be tuned
    peak_indices, _ = find_peaks(psd_smoothed, 
                                 prominence=prominence, 
                                 distance=distance,
                                 height=height)
    
    # Extract frequencies and PSD values at those peak locations
    freq_peaks = freq[peak_indices]
    psd_peaks = psd_smoothed[peak_indices]
    
    return freq_peaks, psd_peaks, psd_smoothed, peak_indices


def main():
    
    aiPath ='/user/home/opt_old/xl/xl/experiments/correctedAngle_roughness/data/24/'
    # '/user/home/opt_old/xl/xl/experiments/correctedAngle_roughness/data/ideal/'
    # '/user/home/opt_old/xl/xl/experiments/correctedAngle_roughness/data/14/'
    # '/user/home/opt_old/xl/xl/experiments/correctedAngle_roughness/data/19/'
    # '/user/home/opt_old/xl/xl/experiments/correctedAngle_roughness/data/4/'
    # '/user/home/opt_old/xl/xl/experiments/correctedAngle_roughness/data/24/'
    # '/user/home/opt_old/xl/xl/experiments/correctedAngle_roughness/data/20/'
    maskPath = '/data/xfm/18872/temp/masks/'
    savePath = '/home/jerome/Documents/MASTERS/Figures/plots/roughness/'
    aiFile = 'res_int_pr_me.dat'
    maskFile = 'T20nm_2.50000_10.00000_2.50000_mask.tif'
    # 'T20nm_vert_mask.tif'
    # 'T20nm_2.50000_6.00000_2.50000_mask.tif'
    # 'T20nm_2.50000_8.00000_2.50000_mask.tif'
    # 'T20nm_2.50000_2.00000_2.50000_mask.tif'
    # 'T20nm_2.50000_10.00000_2.50000_mask.tif' 
    # 'T20nm_0.50000_10.00000_2.50000_mask.tif'
    
    # print(maskFile[14:15])
    try:
        print(maskFile[14:16])
        Cx = int(maskFile[14:16])
    except:
        Cx = int(maskFile[14:15])
    # try:
    #     Cx = int(maskFile[14:15])
    # except:
    #     Cx = 100
    
    print('Cx = ', Cx)
    N = 4000-160#1200                               # number of pixels to take for line profile  - 1200 for roughness aerial images
    n = int(3860/97)                                 # number of pixels to average over for line profile - 15 for roughness aerial images
    # plotRange = 1000                       # range of aerial image plot in nm

    # Loading aerial image intensity file
    nx = str(np.loadtxt(aiPath+aiFile, dtype=str, comments=None, skiprows=6, max_rows=1, usecols=(0)))[1:]#[1:3]
    ny = str(np.loadtxt(aiPath+aiFile, dtype=str, comments=None, skiprows=9, max_rows=1, usecols=(0)))[1:]#[1:3]
    xMin = str(np.loadtxt(aiPath+aiFile, dtype=str, comments=None, skiprows=4, max_rows=1, usecols=(0)))[1:]#[1:3]
    xMax = str(np.loadtxt(aiPath+aiFile, dtype=str, comments=None, skiprows=5, max_rows=1, usecols=(0)))[1:]#[1:3]
    rx = float(xMax)-float(xMin)
    dx = np.divide(rx,float(nx))
    yMin = str(np.loadtxt(aiPath+aiFile, dtype=str, comments=None, skiprows=7, max_rows=1, usecols=(0)))[1:]#[1:3]
    yMax = str(np.loadtxt(aiPath+aiFile, dtype=str, comments=None, skiprows=8, max_rows=1, usecols=(0)))[1:]#[1:3]
    ry = float(yMax)-float(yMin)
    dy = np.divide(ry,float(ny))
    
    numC = 1
    I = np.reshape(np.loadtxt(aiPath+aiFile,skiprows=10), (numC,int(ny),int(nx)))   #CHANGED BY JK      # Propagated multi-electron intensity
    I = np.squeeze(I)
    # Iflat = I.flatten()
    
    print("Resolution (x,y): {}".format((nx,ny)))
    print("xRange: {}".format(rx))
    print("xMax: {}".format(xMax))
    print("xMin: {}".format(xMin))
    print("yRange: {}".format(rx))
    print("yMax: {}".format(yMax))
    print("yMin: {}".format(yMin))
    print("Dx, Dy : {}".format((dx,dy)))
    
    # Loading mask file
    mask = tifffile.imread(maskPath + maskFile)
    mask = np.rot90(mask[1131:4991,6500:10500])
    
    
    # plt.imshow(np.log(I),aspect='auto')
    # plt.colorbar()
    # plt.show()
    
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
    
    
    
    # res and middle pixels of images
    # res = np.full((np.shape(files)[0],2), [2.5011882651601634e-09, 2.426754806976689e-07])
    mid = (196, 12188)
    pitch = 100e-9
    d = int(13.75e-6 / dx)
    
    aiROI = [mid[0] - int(n/2), mid[0] + int(n/2), mid[1] - int(N/2), mid[1] + int(N/2)]
    
    
    names = ['Mask','Aerial Image','0 order', '-1 order']         
    AI = I[aiROI[0]:aiROI[1],aiROI[2]:aiROI[3]] #mid[0] - int(n/2):mid[0] + int(n/2),mid[1] - int(N/2):mid[1] + int(N/2)]
    I0 = I[aiROI[0]:aiROI[1],aiROI[2] - int(d):aiROI[3] - int(d)]
    In1 = I[aiROI[0]:aiROI[1],aiROI[2] + int(2*d):aiROI[3] + int(2*d)]
    # print(aiROI[2] + int(2*d), aiROI[3] + int(2*d))
    
    fig, ax = plt.subplots(2,2)
    ax[0,0].imshow(mask,aspect='auto')
    ax[0,1].imshow(AI,aspect='auto')
    ax[1,0].imshow(I0,aspect='auto')
    ax[1,1].imshow(In1,aspect='auto')
    ax[0,0].set_title("Mask")
    ax[0,1].set_title("Aerial Image")
    ax[1,0].set_title("0 order")
    ax[1,1].set_title("-1 order")
    # for a in ax:
    #     a.set_xticks(tickAx)
    #     a.set_xticklabels(np.arange(0,int(nx)+1,int(nx)/4))
    #     a.set_yticks(np.arange(0,int(ny)+1,int(ny)/4))
    #     # plt.colorbar()
    plt.xlim((1/(Cx+2),1/(Cx-2)))
    fig.tight_layout()
    plt.show()
    
    
    fx, fy = [],[]
    Px,Py = [],[]
    peakFx, peakPx = [], []
    smoothX, peak_i = [], []
    for i,a in enumerate([mask,AI,I0,In1]):
        if i==0:
            freq_x, psd_x = compute_horizontal_psd(a,dx=2.5)
            freq_y, psd_y = compute_vertical_psd(a,dy=2.5)
        else:
            freq_x, psd_x = compute_horizontal_psd(a,dx=dx*1e9)
            freq_y, psd_y = compute_vertical_psd(a,dy=dy*1e9)
            
        
        fxp, pxp, px_s, pxi = find_prominent_frequencies(freq_x, np.log10(psd_x))
        # fp, pxp, px_s, pxi = find_prominent_frequencies(freq_x, psd_x)
        
        print('size of arrays')
        print('fx: ', np.shape(freq_x))
        print('fy: ', np.shape(freq_y))
        print('px: ', np.shape(psd_x))
        print('py: ', np.shape(psd_y))
        fx.append(freq_x)
        fy.append(freq_y)
        Px.append(psd_x)
        Py.append(psd_y)
        
        peakFx.append(fxp)
        peakPx.append(pxp)
        smoothX.append(px_s)
        peak_i.append(pxi)
    
    
    fig, ax = plt.subplots(2,2)
    ax[0,0].loglog(fx[0],Px[0])
    ax[0,0].set_title('Mask')
    ax[0,1].loglog(fx[1],Px[1])
    ax[0,1].set_title('Aerial Image')
    ax[1,0].loglog(fx[2],Px[2])
    ax[1,0].set_title('0 order')
    ax[1,1].loglog(fx[3],Px[3])
    ax[1,1].set_title('-1 order')
    for a in [ax[0,0],ax[1,0],ax[0,1],ax[1,1]]:
        a.axvline(1/Cx,0,1,ls=':',color='black')
    fig.tight_layout()
    plt.show()
    # print(peak_i[0])
    # print(peakFx[0])
    B = 0
    X = 0.3
    # -- Horizontal PSD --
    for i,f in enumerate(fx):
        plt.loglog(f, Px[i]/np.max(Px[i])+ B, label=names[i])
        # plt.loglog(f, np.exp(smoothX[i]/np.max(smoothX[i])) + B, label=names[i])
        fp = [f[p] for p in peak_i[i]]
        pp = [smoothX[i][p]/np.max(smoothX[i])  for p in peak_i[i]]
        plt.loglog(fp,np.exp(pp) + B,'X',color='r')
        B += X
    plt.title('Horizontal PSD (log scale)')
    plt.xlabel('Spatial frequency [/nm]')
    plt.ylabel('Power [a.u]')
    plt.axvline(1/Cx,0,1,ls=':',color='black',label=f'$c_x = ${Cx} nm')#np.max(np.exp(smoothX[i]/np.max(smoothX[i])) + B),':')#, label=f'$c_x = ${Cx} nm')#, ymax, kwargs)
    plt.legend()
    plt.xlim((1/(Cx+2),1/(Cx-2)))
    plt.grid(True,which='both')
    plt.show()
    
    B = 0
    X = 0.2
    # -- Horizontal PSD --
    for i,f in enumerate(fx):
        plt.plot(f, (Px[i]/np.max(Px[i]))+ B, label=names[i])
        # plt.plot(f, smoothX[i]/np.max(smoothX[i]) + B, label=names[i])
        # plt.plot(f[peak_i[i]],smoothX[peak_i[i]]/np.max(smoothX[peak_i[i]]),'X')
        # fp = [f[p] for p in peak_i[i]]
        # pp = [smoothX[i][p]/np.max(smoothX[i])  for p in peak_i[i]]
        # plt.plot(fp,pp + B,'X',color='r')
        B += X
    plt.title('Horizontal PSD (linear scale)')
    plt.xlabel('Spatial frequency [/nm]')
    plt.ylabel('Power [a.u]')
    plt.axvline(1/Cx,0,1,ls=':',color='black',label=f'$c_x = ${Cx} nm')#, ymax, kwargs)
    plt.legend()
    plt.xlim((1/(Cx+2),1/(Cx-2)))
    # plt.xscale('log')
    # plt.yscale('log')
    plt.grid(True,which='both')
    plt.show()
    
    B = 0
    X = 0.1
    # -- Horizontal PSD --
    for i,f in enumerate(fx[1::]):
        plt.loglog(f, (Px[i+1]/np.max(Px[i+1]))+ B, label=names[i+1])
        # plt.plot(f, smoothX[i+1]/np.max(smoothX[i+1]) + B, label=names[i+1])
        B += X
    plt.title('Horizontal PSD (linear scale)')
    plt.xlabel('Spatial frequency [/nm]')
    plt.ylabel('Power [a.u]')
    plt.axvline(1/Cx,0,1,ls=':',color='black',label=f'$c_x = ${Cx} nm')
    plt.legend()
    plt.xlim((1/(Cx+2),1/(Cx-2)))
    # plt.xscale('log')
    # plt.yscale('log')
    plt.grid(True,which='both')
    plt.show()
    
    # # -- Vertical PSD --
    # for i,f in enumerate(fy):
    #     plt.loglog(f, Py[i]/np.max(Py[i]),':.', label=names[i])
    # plt.title('Vertical PSD (log scale)')
    # plt.xlabel('Spatial frequency [/nm]')
    # plt.ylabel('Power [a.u]')
    # plt.legend()
    # plt.grid(True,which='both')
    # plt.show()
    
    # # -- Vertical PSD --
    # for i,f in enumerate(fy):
    #     plt.plot(f, (Py[i]/np.max(Py[i])),':.', label=names[i])
    # plt.title('Vertical PSD (linear scale)')
    # plt.xlabel('Spatial frequency [/nm]')
    # plt.ylabel('Power [a.u]')
    # plt.legend()
    # plt.xscale('log')
    # # plt.yscale('log')
    # plt.grid(True,which='both')
    # plt.show()
    
    B = 0
    X = 0.03
    fig, ax = plt.subplots()
    # Mask comparison
    for i,f in enumerate(fx[1::]):
        # df,dp = psd_difference(f, smoothX[i+1]/np.max(smoothX[i+1]), fx[0], smoothX[0]/np.max(smoothX[0]),n_points=2000)
        df,dp = psd_difference(f, Px[i+1]/np.max(Px[i+1]), fx[0], Px[0]/np.max(Px[0]),n_points=2000)
        dp[dp < 1e-14] = 0
        sx = 1/df
        ax.plot(df, dp/np.max(dp) + B, label=names[1::][i])
        B += X
    # ax.axhline(0, color='k', linestyle='--', alpha=0.5)
    ax.set_title('PSD(order) - PSD(mask) [log scale]')
    ax.set_xlabel('Spatial frequency [/nm]')
    ax.set_ylabel('Power [a.u]')
    plt.axvline(1/Cx,0,1,ls=':',color='black',label=f'$c_x = ${Cx} nm')
    ax.legend()
    plt.xlim((1/(Cx+2),1/(Cx-2)))
    # ax.set_xscale('log')
    # ax.set_yscale('log')
    ax.grid(True,which='both')
    # plt.show()
    ax.set_ylim(0,0.1)
    # 2) Define forward/backward transforms: freq <-> period
    def freq_to_period(f):
        return 1.0 / f
    
    def period_to_freq(p):
        return 1.0 / p
    
    # 3) Create the top axis, telling it how to convert from freq to period
    ax_top = ax.secondary_xaxis('top', functions=(freq_to_period, period_to_freq))
    ax_top.set_xlabel("Period [nm]")
    plt.tight_layout()
    plt.show()
    
    # for i, fx in enumerate(peakFx):
    #     plt.plot([1/f for f in fx], peakPx[i]/np.max(peakPx[i]),label=names[i])
    # ax.set_title('periods of peak frequencies')
    # ax.set_xlabel('Spatial period [nm]')
    # ax.set_ylabel('Power [a.u]')
    # ax.legend()
    # # ax.set_xscale('log')
    # # ax.set_yscale('log')
    # ax.grid(True,which='both')
    # plt.show()
    
    print('----- Peak spatial frequencies -----')
    print('Mask:')
    print([1/p for p in peakFx[0]])
    print('Aerial Image:')
    print([1/p for p in peakFx[1]])
    print('0 order:')
    print([1/p for p in peakFx[2]])
    print('-1 order:')
    print([1/p for p in peakFx[3]])
    # for i,a in enumerate([AI,I0,In1]):
    #     plt.loglog(freq_x, psd_x/np.max(psd_x), label=names[i])
        
    # plt.title('Horizontal PSD (One-sided)')
    # plt.xlabel('Spatial frequency [/nm]')
    # plt.ylabel('Power [a.u]')
    # plt.legend()
    # plt.grid(True,which='both')
    # plt.show()
    
    # freq_x1, psd_x1 = compute_horizontal_psd(mask,dx=2.5)
    # freq_x2, psd_x2 = compute_horizontal_psd(AI,dx=dx*1e9)
    
    # freq_y1, psd_y1 = compute_vertical_psd(mask,dy=2.5)
    # freq_y2, psd_y2 = compute_vertical_psd(AI,dy=dy*1e9)
        
    
    # # -------------------------------------------------------------------------
    # # 4. Plot horizontal (left) and vertical (right) PSDs
    # #    Zero frequency is at x=0 on each plot
    # # -------------------------------------------------------------------------
    # fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    # # -- Horizontal PSD --
    # plt.loglog(freq_x1, psd_x1/np.max(psd_x1), label='mask - Horizontal')
    # plt.loglog(freq_x2, psd_x2/np.max(psd_x2), label='aerial image - Horizontal')
    # plt.title('Horizontal PSD (One-sided)')
    # plt.xlabel('Spatial frequency [cycles/nm]')
    # plt.ylabel('Power')
    # plt.legend()
    # plt.grid(True,which='both')
    # plt.show()
    
    # # -- Vertical PSD --
    # plt.loglog(freq_y1, psd_y1/np.max(psd_y1), label='mask - Vertical')
    # plt.loglog(freq_y2, psd_y2/np.max(psd_y2), label='aerial image - Vertical')
    # plt.title('Vertical PSD (One-sided)')
    # plt.xlabel('Spatial frequency [cycles/nm]')
    # plt.ylabel('Power')
    # plt.legend()
    # plt.grid(True, which='both')
    
    # # plt.tight_layout()
    # plt.show()
    # plt.plot()
if __name__ == "__main__":
    main()

