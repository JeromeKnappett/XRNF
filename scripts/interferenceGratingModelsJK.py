#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 29 12:40:25 2020


This is intended to be a library of methods for analysing the properties 
of interference gratings and interference patterns.  It is under development and
mostly untested  — use with caution!

@author: gvanriessen
"""


import numpy as np
from numpy import sin, cos, exp, pi, sqrt, square
from scipy.signal import periodogram
from scipy.fftpack import fft, ifft, fftfreq
from scipy.signal import find_peaks, peak_widths
from findiff import FinDiff
from itertools import chain, zip_longest
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import argrelextrema
from scipy.ndimage import gaussian_filter
import cv2
from lmfit import Model
from scipy.optimize import minimize, differential_evolution

'''

    We are interested in MTF of the optical system, which may be calculated as 
    contrast as a function of frequency.
    
    Start here with methods to define contrast'
    
'''    



def getPhaseGradient(wf,polarization='horizontal'):
    ''' return phase gradient in x and y directions for wavefield wf
    **IGNORES slices
    '''
    
    phase = np.squeeze(wf.get_phase(polarization=polarization))
    gy,gx = np.gradient(phase)
            
    return gx, gy

    
#gx,gy=getPhaseGradient(wf)
#
#
#plt.figure()
#plt.suptitle("Phase and it gradient along each axis")
#ax = plt.subplot("131")
#ax.imshow(phase)
#ax.set_title("image")
#
#ax = plt.subplot("132")
#ax.imshow(gx,vmax=0.1, vmin=-0.1)
#ax.set_title("gx")
#
#ax = plt.subplot("133")
#ax.imshow(gy, vmax=0.1, vmin=-0.1)
#ax.set_title("gy")
#
#plt.colorbar()
#plt.show()

def gauss1D(n,sigma):
    if n % 2 == 0: # n is even
        r = np.linspace(-int(n/2)+0.5,int(n/2)-0.5,n)
    else:          # n is odd 
        r = np.linspace(-int(n/2),int(n/2)+1,n)
    return [1 / (sigma*np.sqrt(2*np.pi)) * np.exp(-float(x)**2/(2*sigma**2)) for x in r]
    

def lineProfile(A, ROI=None, AXIS = 0):
    '''
    make a line profile over a region of interest in a 2D array of values A 
    '''
    if ROI is None:
        a = A
    else:
         # get number of pixels in x and y
        Nx = np.shape(A)[1]
        Ny = np.shape(A)[0]
        
        x0,y0 = ROI[0][0], ROI[0][1]
        x1,y1 = ROI[1][0], ROI[1][1]
    
        a = A[y0:y1,x0:x1]
    
    profile = np.mean(a, axis=AXIS)

    return profile


def profilePeaks(A, ROI=None, AXIS = 0, H=[0.5], show=True):
    '''
    make a line profile over a region of interest in a 2D array of values A and
    find peaks and their width, where width is taken as the width at H*maximum peak height
    
    ROI specifies a region of interest in A. It should be a tuple of tuples 
    ((x0,y0),(x1,y1)),  where (x0,y0) is lower left corner, and (x1,y1) is upper right corner
    Height (width) of ROI may be 1 for a line profile over a single row (column) of pixels
    AXIS = 1  for profile along y direction, 0 for profile along x direction
    H or values h in H=[h1,h2,...] may be a list of values between 0 and 1.
    
    Displays array, ROI and peak finding results if show is True
    
    
    Returns:
        profile: the line profile over ROI for each value in H
        pos: peak positions for each value in H
        width: width of peaks for each value in H
        boundary: positions along profile where a peak rises and falls through a 
            line at a fraction each value in H of the peak height.
        avgWidth: average of peak widths for each value in H
    '''
    profile = lineProfile(A, ROI=ROI, AXIS = AXIS)

    pos, width, boundary = findPeaks(profile, H=[0.5,0.75])
    
    # find average widths
    avgWidth = np.mean(width,axis=1) 
    
    if show is True:
        plt.imshow(A)
        plt.show()
        # plt.imshow(a)
        # plt.show()
        
        plt.plot(profile, '-')
        plt.plot(pos, profile[pos], '*')
        plt.hlines(*boundary[0], color="C2")
        plt.hlines(*boundary[1], color="C3")
        plt.show()
    
    return profile, pos, width, boundary, avgWidth



def findPeaks(S,H=0.5):
    '''
    Find peaks return their position and width at some fraction H of their height.
    peak   in signal S that is defined over a range of values in P
    
    H or values h in H=[h1,h2,...] may be a list of values between 0 and 1.
    
    All in units of pixels, i.e. no scaling to pixel length here.
    '''
    if not isinstance(H, list):
        H = [H] # make it a list of length 1
    
    peaks, _ = find_peaks(S)   # peak indexes (see scipy.signal.find_peaks docs for more options)

    widths,boundaries=[],[]
    for h in H:
        w = peak_widths(S, peaks, rel_height=h)
        widths.append( w[0] )# widths of peaks at h * height
        boundaries.append(w[1:])
    return peaks, widths, boundaries


def getImageData(filename):
    import cv2
    im = cv2.imread(filename, cv2.IMREAD_ANYDEPTH )   # open any bit depth image (more readable than -1)    
    im = np.array(im)
    return im


def gratingContrastMichelson(A):
    '''
    Return Michelson contrast: $\frac{\max(I) - \min(I)}{\max(I) + \min(I)}$
    
    Michelson contrast is highly sensitive to noise. Since it is calculated only from extrema, i.e., at two pixels
    
    In the case where the optical fringe period is comparable to pixel size, Michelson contrast is also sensitive to the phase difference,between pixel grid and optical fringe signal. 
    '''
    maxA = np.max(A)
    minA = np.min(A)
    C = (maxA-minA) / (maxA+minA)
    return C


def gratingContrastRMS(A):
    '''
    Return root mean squared contrast. 
            
    RMS contrast does not depend on the angular frequency content or the spatial distribution of contrast in the image.
    '''    
    # normalise it first  ---  wrong to do this
    #A = (A-np.min(A))/(np.max(A)-np.min(A))    
    A = (A)/ np.max(A) 

    N = np.size(A)
    mean = np.mean(A)    
    C = sqrt( 1/N * np.sum(  square((A - mean)/mean)) )
    
    # fro comparison to Michelson Contrast:
    C = C * sqrt(2)
    
    return C




#def LWR(I,  px, dim = 1):
#        
#    '''
#    parameters:
#        I: pattern
#        dim - dimension aligned to lines
#        px: length of pixel along dimension dim
#        
#    '''
#    assert (dim==0 or dim==1), "dim must be 0 or 1"
#   
#    I = np.array(I)
#    stripes = (255*I/np.max(I)).astype(np.uint8)
#    
#    print(np.shape(stripes))
#   
#    
#    #blur the image for better edge detection...
#    stripes = cv2.GaussianBlur(stripes,(3,3),0)    
    
#    delta = 0.09
#    mean = np.mean(stripes)
#    binaryMask = np.logical_and(stripes > mean*(1-delta), stripes < mean*(1+delta))
#    plt.imshow(binaryMask, cmap='gray',aspect=0.1)
#    plt.show()
    
#    stripes = np.array(iP)
#    stripes = (255*I/np.max(I)).astype(np.uint8)
#    ret, thresh = cv2.threshold(stripes,np.int(127*0.8),255,0)
#    plt.imshow(thresh)
#    plt.show()
#    #plt.colorbar()
#    contours, heirarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
#    #color = cv2.cvtColor(stripes,cv2.COLOR_GRAY2BGR)
#    stripes = cv2.drawContours(stripes, contours, -1, (255,0,0), 2)
#    #cv2.imshow("contours", stripes)
#    plt.imshow(stripes, aspect=0.1)
#        
#    # Get indices for pixels identified by Canny edge detection
#    med = np.mean(stripes) 
#    lower = int(max(0 ,0.3*med))
#    upper = int(min(255,0.7*med))
#    edges = cv2.Canny(stripes, lower, upper)
#    indices = np.argwhere(edges)
#    
#    
#    contours = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
#    cv2.drawContours(stripes,contours[0],-1, (255,255,255), thickness=2)
#    fig, ax = plt.subplots(1,figsize=(12,8))
#    plt.imshow(stripes,aspect=0.1)
#    plt.show()
#    
#
#    # find edges and their gradient
#    if dim==1:
#        dx, dy = 0,1
#    if dim==0:
#        dx, dy = 1,0
#        
#    
#    sobel = cv2.Sobel(stripes,cv2.CV_64F,dx,dy,ksize=3)>0
#    
#    
#
#    #edgesL, edgesH  = sobel<0, sobel>0
#    #indicesL, indicesH = np.argwhere(edgesL), np.argwhere(edgesH)
#
#    indices = np.argwhere(sobel)
    
    
#    aperture = 3
#    gray  = cv2.CreateImage(cv2.GetSize(stripes), 8, 1)
#    cv2.CvtColor(stripes, gray, cv2.CV_BGR2GRAY
#                )
#    dst = cv2.CreateImage(cv2.GetSize(gray), cv2.IPL_DEPTH_32F, 1)
#    cv2.Laplace(gray,dst, aperture)
#    cv2.Convert(dst, gray)
#    thresholded = cv2.CloneImage(stripes)
#    cv2.Threshold(stripes, thresholded, 50 , 255, cv2.CV_THRESH_BINARY_INV)
#    cv2.ShowImage('Laplaced grayscale', gray)
    
    
    
    # M = indices * px

    
    #plt.imshow(cv2.filter2D(stripes, -1, sobel))
    #plt.imshow(stripes[edgesL])
    
#    print(np.shape(indicesH))
#    print(np.shape(indicesL))
#    print(px)
#    LW = np.abs(np.subtract(indicesH,indicesL)) * px
#    
#    
#    M = np.size(edgesL)
#    mu =np.mean(LW)
#    
#    LWd = [np.square(w-mu) for w in LW]
#    LWR =  np.sqrt( (1/(M-1) * np.sum(np.square(LWd))   ))
#    LWR=0
#    edges=0
#    return LWR, edges
    
    

# def NILS1D(I,x,w,show=True):
    
#     lnI = np.log(I)
    
#     dx = x[1]-x[0]
#     d_dx = FinDiff(0,dx)
#     gradAbs = np.abs(d_dx(lnI,acc=10))
    
#     d = int(w/dx)
 
def rejectOutliers(data, m=2):
    data[abs(data-np.mean(data)) > m*np.std(data)] = np.nan
    return data
    
    


def rejectNAN(data):
    return data[~np.isnan(data)]
   
def sinefunction(x,a,b,c,d):
        return a+b*np.sin((d/2)*x +c) #added d term to vary the frequency of the sin function
    
def polyfunction(x,a,b,c):
    return  c*x**2 + b*x +a

def find_minimum(func, x0, method='BFGS'):
    """
    Finds the local minimum of a scalar function.
    
    Parameters:
    - func: callable, the objective function to minimize.
    - x0: array-like, initial guess.
    - method: str, optimization method (default: 'BFGS').
    
    Returns:
    - result: OptimizeResult, contains the location of the minimum and more.
    """
    result = minimize(func, x0, method=method)
    return result

def checkPeakTroughSequence(p1, p2):
 # Sanity check: ensure alternating sequence
 
    sequence = [(pos, 'peak') for pos in p1] + [(pos, 'trough') for pos in p2]
    sequence.sort()
    OK = True
    sID = []
    sType = []
    for i in range(1, len(sequence)):
        if sequence[i][1] == sequence[i - 1][1]:
            print(f"  Warning: Found two consecutive {sequence[i][1]}s at indices {sequence[i - 1][0]}, {sequence[i][0]}")
            OK = False
            sID.append(i) # append index position of error
            sType.append(sequence[i][1]) # append label peak/trough or error position
            # break
    for i,s in enumerate(sID):
        if sType[i] == 'peak':
            t = 'trough'
        elif sType[i] == 'trough':
            t = 'peak'
        d = (sequence[s][0] + sequence[s-1][0]) // 2 # find mid point between the two consecutive peaks/troughs
        
        sequence.insert(s,(d,t)) # insert new peak/trough into sequence at mid point
        # del sequence[s]
    return OK, sequence


def positionMeanIntensity(x):
    
    # return the pixel coordinate of the mean intensity in a 1D list of values a
    
    weightedMean = np.average(np.arange(len(x)), weights=x)
    
    return weightedMean

import numpy as np
from scipy.signal import find_peaks
from scipy.optimize import differential_evolution
from lmfit import Model
import matplotlib.pyplot as plt


# ──────────────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────────────

def detect_line_angle_fft(I):
    """
    Estimate the dominant line orientation in *I* using the 2-D FFT.

    Lines in the image produce a ridge in the power spectrum that is
    perpendicular to the line direction.  We find that ridge and convert
    its angle back to the line angle.

    Returns
    -------
    angle_deg : float
        Rotation angle of the lines relative to vertical, in degrees.
        Positive = clockwise tilt.
    """
    # Apodise to suppress cross-shaped FFT artefacts from hard edges
    rows, cols = I.shape
    wy = np.hanning(rows)
    wx = np.hanning(cols)
    window = np.outer(wy, wx)
    apodised = I * window

    F = np.fft.fftshift(np.abs(np.fft.fft2(apodised)) ** 2)

    # Work only in the upper half-plane to avoid ambiguity
    half = F[: rows // 2, :]

    # Suppress the DC neighbourhood (central low-frequency blob)
    cy, cx = rows // 4, cols // 2          # centre of upper-half
    mask_r = max(rows, cols) // 16
    yy, xx = np.ogrid[: rows // 2, :cols]
    half = half * (((yy - cy) ** 2 + (xx - cx) ** 2) > mask_r ** 2)

    # Find the brightest pixel in the upper-half power spectrum
    peak_idx = np.unravel_index(np.argmax(half), half.shape)
    peak_y, peak_x = peak_idx

    # Convert FFT index → angle of the *spectral ridge* then rotate 90°
    # to get the line direction
    freq_angle_rad = np.arctan2(peak_y - 0, peak_x - cols // 2)
    line_angle_rad = freq_angle_rad - np.pi / 2          # perpendicular
    angle_deg = np.degrees(line_angle_rad)

    # Fold into (−90, 90]
    if angle_deg <= -90:
        angle_deg += 180
    elif angle_deg > 90:
        angle_deg -= 180

    return angle_deg


def build_line_spines(I, p1, angle_deg):
    """
    Build a 2-D spine for every detected line in *I*.

    Strategy
    --------
    * The full-image projection already gave us seed x-positions ``p1`` at
      the image centre row (row_mid).
    * Each line tilts by ``tan(angle_deg)`` pixels horizontally per row, so
      for row *r* the spine centre is:

          col(r) = p1[line] + tan(angle_deg) * (r - row_mid)

      No intensity data is read here — only index arithmetic.

    Returns
    -------
    spines : list of 1-D int arrays, one per line, length == rows.
        spines[i][r]  is the column index of line i's centre at row r.
    """
    rows = I.shape[0]
    row_mid = rows / 2
    tan_a = np.tan(np.radians(angle_deg))

    spines = []
    for seed_col in p1:
        spine = np.array(
            [int(round(seed_col + tan_a * (r - row_mid))) for r in range(rows)],
            dtype=int,
        )
        spines.append(spine)

    return spines


def extract_slanted_scanlines(I, spine, half_width):
    """
    Extract a list of 1-D scanlines that form a slanted chunk around *spine*.

    For each row *r* the scanline is the horizontal slice:
        I[r,  spine[r] - half_width : spine[r] + half_width]

    This is a straight read of existing pixels — no interpolation.

    Returns
    -------
    scanlines : list of 1-D arrays (one per row).  Rows where the window
                falls outside the image boundary are skipped.
    row_indices : list of int  – which image rows were kept.
    spine_cols  : list of int  – spine column for each kept row (for plotting).
    """
    rows, cols = I.shape
    scanlines  = []
    row_indices = []
    spine_cols  = []

    for r in range(rows):
        c = spine[r]
        c0 = c - half_width
        c1 = c + half_width
        if c0 < 0 or c1 > cols:
            continue                      # skip rows where window clips edge
        scanlines.append(I[r, c0:c1].copy())
        row_indices.append(r)
        spine_cols.append(c)

    return scanlines, row_indices, spine_cols


# ──────────────────────────────────────────────────────────────────────────────
# Main function
# ──────────────────────────────────────────────────────────────────────────────

def LWRChunkWise_c(I, x, w, angle_deg=None, show=True, debug=True):
    """
    Calculate Line Width Roughness (LWR), Line Edge Roughness (LER), CDU,
    and CLR from a 2-D aerial image intensity array.

    Parameters
    ----------
    I         : 2-D array-like   – image intensity
    x         : 1-D array-like   – physical x-coordinates (same length as
                                   number of columns in I)
    w         : float            – nominal half-pitch in physical units
    angle_deg : float, None, or 'none'
                                 – rotation of the lines relative to vertical
                                   in degrees.
                                   * None (default) : auto-detect angle via FFT
                                     and use spine/scanline analysis.
                                   * float           : use supplied angle with
                                     spine/scanline analysis.
                                   * 'none'          : disable angle correction
                                     entirely and use the original chunkit-based
                                     methodology with no geometric corrections.
    show      : bool             – show summary plots
    debug     : bool             – show per-row diagnostic plots/prints

    Returns
    -------
    lwGlobal, rms, rmsd, LWR, LER, CDU, CLR
    """

    I = np.array(I, dtype=float)

    # ── 1. Determine operating mode and angle ─────────────────────────────────
    # 'none' (string) = original methodology, no angle correction.
    # None            = auto-detect angle via FFT.
    # float           = use supplied angle.
    use_angle = not (isinstance(angle_deg, str) and angle_deg.lower() == 'none')

    if use_angle:
        if angle_deg is None:
            angle_deg = detect_line_angle_fft(I)
            print(f"[angle] Auto-detected line tilt: {angle_deg:.3f}°")
        else:
            print(f"[angle] Using supplied line tilt: {angle_deg:.3f}°")
        # Geometric correction factors (see comments below).
        cos_a   = np.cos(np.radians(angle_deg))
        dy_phys = None          # computed after dx is known
    else:
        print("[angle] Angle correction disabled — using original methodology.")
        angle_deg = 0.0         # neutral value for any incidental trig
        cos_a     = 1.0
        dy_phys   = None

    # ── 2. Projection and peak seeding ───────────────────────────────────────
    projection = np.mean(I, axis=0)

    dx = np.mean(np.diff(x))
    d  = int(w / dx)            # nominal half-pitch in pixels

    # cos_a   : projects a horizontal edge position onto the direction truly
    #           orthogonal to the (tilted) line.
    #               pos_orthogonal = pos_horizontal * cos(angle)
    # dy_phys : physical distance between adjacent scanlines along the line.
    #           With square pixels, row pitch == dx, so dy_phys = dx / cos(angle).
    #           For no-angle mode both reduce to 1.0 * dx, preserving original
    #           behaviour exactly.
    dy_phys = dx / cos_a

    p1, _ = find_peaks(projection, distance=d)

    if len(p1) and p1[-1] > len(I[0]) - d:
        p1 = p1[:-1]

    plt.plot(x, projection, ':o', mfc='none')
    plt.plot(x[p1], projection[p1], "x")
    plt.title("Projection with detected peaks")
    plt.show()

    # ── 3. Build chunks — slanted spines or original rectangular chunks ───────
    D = int(d * 2.1)    # half-width of chunk in pixels

    if use_angle:
        spines   = build_line_spines(I, p1, angle_deg)
        iterator = spines           # loop variable is a spine array
    else:
        chunks   = chunkit(I, D, p1)
        iterator = chunks           # loop variable is a 2-D chunk array

    lwDev     = []
    lwDevSqr  = []
    lwGlobal  = []
    edgePos   = []
    clDev     = []
    # Per-edge accumulation for LER: even indices = left edges, odd = right.
    # Stored as list-of-lists, one inner list per line, alternating L/R per row.
    edgePosAll = []     # edgePosAll[line] = [L0, R0, L1, R1, ...]

    n_lines = len(iterator)

    for e, item in enumerate(iterator):
        print(f"Analysing LWR/LER of line #{e+1} of {n_lines}")

        # ── obtain scanlines depending on mode ───────────────────────────────
        if use_angle:
            scanlines, row_indices, spine_cols = extract_slanted_scanlines(
                I, item, D)
            if len(scanlines) == 0:
                print(f"  Skipping line #{e+1}: no valid scanlines.")
                continue
        else:
            # Original behaviour: item is the rectangular chunk array;
            # each row of the chunk is one scanline.
            scanlines   = list(item)          # list of 1-D arrays
            row_indices = list(range(len(scanlines)))
            spine_cols  = [p1[e]] * len(scanlines)

        threshold = 0.6 * np.mean([np.max(s) for s in scanlines])

        lw       = []
        edgePosi = []   # interleaved [L0, R0, L1, R1, ...] for this line
        COM      = []

        for si, row in enumerate(scanlines):

            com = int(positionMeanIntensity(row))
            if debug:
                print(f"COM: {com}")
                print(f"threshold I: {threshold}")

            offset = 0
            r1 = list(reversed(row[0: com + offset]))
            r2 = row[com - offset:]

            lwi = 0
            for r in [r1, r2]:
                func   = lambda x0, a, b, c, d: a + b * np.sin((d / 2) * x0 + c)
                smodel = Model(sinefunction)
                try:
                    x0 = x[len(x) // 2: len(x) // 2 + len(r)]
                    a0 =      np.max(r)
                    b0 = -1 * np.max(r)
                    c0 = -1 * (x0[1] - x0[0]) * offset
                    d0 = np.pi / (2 * w)

                    if debug or e == 1:
                        print(f"a0: {a0}, b0: {b0}, c0: {c0}, d0: {d0}")
                        scurve = a0 + b0 * np.sin((d0 * x0) + c0)

                    result = smodel.fit(r, x=x0, a=a0, b=b0, c=c0, d=d0)

                except Exception:
                    print('Fit failed for line...')

                else:
                    a = result.best_values['a']
                    b = result.best_values['b']
                    c = result.best_values['c']
                    d = result.best_values['d']

                    pos = 2 * (np.arcsin((threshold - a) / b) - c) / d

                    f_x0  = lambda x0: func(x0[0], a, b, c, d)
                    bounds = [(0, np.max(x0))]
                    res    = differential_evolution(f_x0, bounds)

                    if res.fun > threshold:
                        pos = res.x[0]

                    # In angle mode: project horizontal pos onto direction
                    # orthogonal to the line.  In no-angle mode cos_a == 1
                    # so this is a no-op, preserving original behaviour.
                    pos_stored = pos * cos_a
                    edgePosi.append(pos_stored)
                    lwi += abs(pos_stored)

                    if debug:
                        print(f"a: {a}, b: {b}, c: {c}, d: {d}")
                        if use_angle:
                            print(f"pos (horizontal): {pos:.6g},  "
                                  f"pos (orthogonal): {pos_stored:.6g}")
                        else:
                            print(f"pos: {pos_stored:.6g}")

            if debug or e == 1:
                plt.plot(x0, r, 'o', label='pattern')
                plt.plot(x0, scurve, 'x', label='initial guess')
                try:
                    plt.plot(x0, result.best_fit[:len(x0)], 'o-', label='fit')
                except Exception:
                    pass
                try:
                    plt.vlines(pos, np.min(r), np.max(r),
                               colors='r', linestyles='--', label='edge pos')
                except Exception:
                    pass
                plt.hlines(threshold, np.min(x0), np.max(x0),
                           colors='black', linestyles='--', label='threshold I')
                plt.legend()
                plt.show()

            lw.append(lwi)
            COM.append(com)

        # ── per-line LW statistics ────────────────────────────────────────────
        lwMean = np.mean(lw)
        lwDevN = [np.abs(l - lwMean) for l in lw]
        lwDev.append(lwDevN)
        lwDevSqr.append([l ** 2 for l in lwDevN])
        edgePos.append(edgePosi)
        edgePosAll.append(edgePosi)
        lwGlobal.extend(lw)

        COMmean = np.mean(COM)
        clDevN  = [np.abs(cl - COMmean) for cl in COM]
        clDev.extend(clDevN)

        # ── show overlay ──────────────────────────────────────────────────────
        if show or e == 1:
            if use_angle:
                plt.imshow(I, aspect='auto')
                plt.plot(spine_cols, row_indices, '-', color='white',
                         linewidth=0.5, label='spine')
                for si, (img_row, sc) in enumerate(zip(row_indices, spine_cols)):
                    if si >= len(COM):
                        break
                    midX = sc
                    if 2 * si < len(edgePosi):
                        edge_orth_l = edgePosi[2 * si]
                        try:
                            edgePix = midX - int((edge_orth_l / cos_a) / dx)
                            plt.plot(edgePix, img_row, 'x', color='r', markersize=2)
                        except Exception:
                            pass
                    if 2 * si + 1 < len(edgePosi):
                        edge_orth_r = edgePosi[2 * si + 1]
                        try:
                            edgePix = midX + int((edge_orth_r / cos_a) / dx)
                            plt.plot(edgePix, img_row, 'x', color='r', markersize=2)
                        except Exception:
                            pass
            else:
                # Original display: imshow the rectangular chunk
                plt.imshow(item, aspect='auto')
                for i, edge in enumerate(edgePosi):
                    midX    = COM[i // 2]
                    edge_px = edge - x0[0]
                    if i % 2 == 0:
                        plt.plot(midX, i // 2, 'o', color='white', markersize=2)
                        try:
                            edgePix = midX - int(edge_px / dx)
                            plt.plot(edgePix, i // 2, 'x', color='r', markersize=2)
                        except Exception:
                            try:
                                edgePix = edgePix - midX
                            except Exception:
                                edgePix = midX - 0.5 * midX
                            plt.plot(edgePix, i // 2, 'x', color='y', markersize=2)
                    else:
                        try:
                            edgePix = midX + int(edge_px / dx)
                            plt.plot(edgePix, i // 2, 'x', color='r', markersize=2)
                        except Exception:
                            edgePix = edgePix + midX
                            plt.plot(edgePix, i // 2, 'x', color='y', markersize=2)
                        if debug:
                            print(f"midX: {midX}, edgePix: {edgePix}, "
                                  f"chunk shape: {np.shape(item)}")
            plt.title(f"line #{e+1} of {n_lines}")
            if use_angle:
                plt.legend(loc='upper right', fontsize=6)
            plt.show()

    # ── 4. Global metrics ─────────────────────────────────────────────────────
    if debug:
        print(f"shape of lwGlobal: {np.shape(lwGlobal)}")
        print(f"shape of lwDev:    {np.shape(lwDev)}")

    if show:
        plt.plot(np.array(lwDev).flatten())
        plt.title('Line Width Deviations')
        plt.show()

        plt.imshow(lwDev, aspect='auto')
        plt.colorbar(label='line width deviation')
        plt.show()

    rms  = np.sqrt(np.nanmean(np.square(lwGlobal)))
    rmsd = np.sqrt(np.nanmean(np.square(np.array(lwDev).flatten())))

    N  = len(p1)
    # M: original code used raw row count; angle mode uses physical along-line
    # length so the metric is independent of pixel size and tilt angle.
    M  = np.shape(I)[0] if not use_angle else np.shape(I)[0] * dy_phys
    mu = np.nanmean(lwGlobal)

    sigma_lw = np.nanmean(np.sqrt(np.nanmean(lwDevSqr)))
    LWR      = 3 * sigma_lw

    # ── LER: deviation of each individual edge from its own mean position ─────
    # edgePosAll[line] = [L0, R0, L1, R1, ...] — split into left and right
    # edge signals, compute sigma for each, then average across all edges and
    # all lines.  Same 3-sigma convention as LWR.
    lerSigmas = []
    for ep in edgePosAll:
        left_edges  = np.array(ep[0::2])   # positions from r1 half-scanlines
        right_edges = np.array(ep[1::2])   # positions from r2 half-scanlines
        for edge_signal in [left_edges, right_edges]:
            if len(edge_signal) < 2:
                continue
            edge_mean = np.nanmean(edge_signal)
            edge_devs = edge_signal - edge_mean
            lerSigmas.append(np.sqrt(np.nanmean(edge_devs ** 2)))
    LER = 3 * np.nanmean(lerSigmas) if lerSigmas else float('nan')

    CDU = 3 * np.sqrt(np.nanmean([(l - mu) ** 2 for l in lwGlobal]))
    CLR = 3 * np.sqrt(np.nanmean([cd ** 2 for cd in clDev]))

    if debug:
        if use_angle:
            print(f"N: {N},  M (along-line length): {M:.4g},  dy_phys: {dy_phys:.4g}")
            print(f"cos(angle): {cos_a:.6f}  (angle: {angle_deg:.3f}°)")
        else:
            print(f"N: {N},  M (row count): {M}")
        print(f"LW mean: {mu:.4g},  RMS = {rms:.4g},  RMSd = {rmsd:.4g}")

    print(f"shape of lwDev: {np.shape(lwDev)}")
    print(f"N: {N},  M: {M}")
    print(f"CDU = {CDU}")
    print(f"CLR = {CLR}")
    print(f"LWR = {LWR}")
    print(f"LER = {LER}")

    return lwGlobal, rms, rmsd, LWR, LER, CDU, CLR

def LWRChunkWise(I,x, w, show =True, debug=True):
    
    I  = np.array(I) # convert to numpy array
    
    projection = np.mean(I, axis=0) # project image onto x-axis
    

    dx = np.mean(np.diff(x)) # get the pixel size 
    d = int(w/dx)            # nominal half-pitch in pixels
    

    p1, _ = find_peaks(projection, distance=d)#+8)   # the value of 8 was found by trial and error
    
    
    if p1[-1] > len(I[0]) - d:   # checking if the last peak has enough space for a full line width on either side
        p1=p1[0:len(p1)-1]
    
    plt.plot(x,projection,':o', mfc='none')
    plt.plot(x[p1],projection[p1],"x")
    
    # logic wrong check later.... assert abs(len(p1) - 2*len(x)/d) > 0, "Found unexpected number of peaks in the projection"

    plt.show()
    
    
    # now we chunk I so that each chunk contains one line.
    D =int(d*2.1) #  we'll use chunks 5% wider than d
    chunks = chunkit(I,D,p1)
    
    
    
    lwDev = []
    lwDevSqr = []
    lwGlobal = []
    edgePos = []
    clDev = []
    for e, chunk in enumerate(chunks):
        lw = []
        threshold = 0.6*np.mean([np.max(i) for i in chunk])  #threshold value is 60% of the mean of the maxima
        print(f"Analysing LWR of line #{e+1} of {len(chunks)}")
    
        edgePosi = []
        COM = []
        for row in chunk:
        
                # break each row into parts that encompass, respectively, the
                # leading and trailing edge of the line witha a buffer of 20% of 
                # row length in pixels
                # row = row/np.max(row)
                com = int(positionMeanIntensity(row)) 
                if debug:
                    print(f"COM: {com}")
                    print(f"threshold I: {threshold}")
                    # if show:
                    #     plt.plot(row)
                    #     plt.vlines(com,np.min(row),np.max(row))
                    #     plt.show()

                offset = 0#int(len(row)/20)
                r1 = list(reversed(row[0:com+offset])) # flip so that r1 and r2 can be treated similarly
                r2 = row[com-offset::]
                
                lwi = 0
                for r in [r1,r2]:
                    
                        # Define the full lambda
                    func = lambda x0, a, b, c, d: a + b * np.sin((d / 2) * x0 + c)
                    smodel = Model(sinefunction)
                    try:
                        x0 = x[len(x)//2:len(x)//2 + len(r)]#np.linspace(0-xoff,np.pi/2 + xoff,len(r))
                        a0 = np.max(r) #np.min(r) 
                        b0 = -1*np.max(r)
                        c0 = -1*(x0[1] - x0[0])*offset #1*(offset)
                        d0 = np.pi / (2*w) 
                        # # xoff = (np.pi/2)/20
                        # dx0 = x0[1] - x0[0]
                        if debug or e==1:
                            print(f"a0: {a0}")
                            print(f"b0: {b0}")
                            print(f"c0: {c0}")                
                            print(f"d0: {d0}")                            
                            # print(f"x0: {x0}")#[i*dx for i in range(len(row))] }")
                            
                            scurve = a0+b0*np.sin((d0*x0) + c0)
                            # plt.plot(scurve)
                            # plt.show()
                        
                        result = smodel.fit(r, 
                                            x=x0,#[i*dx for i in range(len(row)//2)], 
                                            a=a0, 
                                            b=b0, 
                                            c=c0,
                                            d=d0)              
                            
                    except:
                        print('Fit failed for line... ')
                            
                    else:
                        a = result.best_values['a']
                        b = result.best_values['b']
                        c = result.best_values['c']
                        d = result.best_values['d']
                        # x = result.best_values['x']
                            # print(f"x: {x}")#[i*dx for i in range(len(row))] }")
                        
                        pos = 2*(np.arcsin((threshold-a)/b) - c) / d
                    
                    
                        # Create a function of x0 only
                        f_x0 = lambda x0: func(x0[0], a, b, c, d)
                        
                        # Define bounds for x0 (e.g., from -10 to 10)
                        bounds = [(0, np.max(x0))]
                        
                        # Minimize
                        res = differential_evolution(f_x0, bounds)
                                                
                        # print("Minimum x0:", res.x[0])
                        # print("Minimum value:", res.fun)
                        if res.fun > threshold:
                            pos = res.x[0]
                        else:
                            pass
                    
                        edgePosi.append(pos)
                        lwi += abs(pos)  # position of edge in m
                        
                        
                        if debug:
                            print(f"a:   {a}")
                            print(f"b:   {b}")
                            print(f"c:   {c}")     
                            print(f"d:   {d}")                            
                            print(f"pos: {pos}")
                        
                if debug or e==1:
                        #print(result.fit_report())
                        plt.plot(x0,r, 'o', label='pattern')
                        plt.plot(x0,scurve, 'x', label='initial guess')
                        try:
                            plt.plot(x0,result.best_fit[0:len(x0)], 'o-', label='fit')
                        except:
                            pass
                        try:
                            plt.vlines(pos,np.min(r),np.max(r), colors='r', linestyles='--', label='edge pos')
                        except:
                            pass
                        plt.hlines(threshold,np.min(x0),np.max(x0), colors='black', linestyles='--', label='threshold I')
                        plt.legend()
                        plt.show()  
                else:
                    pass
                # threshold = 0.6*np.max(ISeg)
                lw.append(lwi)
                COM.append(com)
                # print(f"lwi:   {lwi}")
        
        # extend list of lw deviations for all chunks
        lwMean = np.mean(lw)
        lwDevN = [np.abs(l-lwMean) for l in lw]
        lwDev.append(lwDevN)
        lwDevSqr.append([l**2 for l in lwDevN])
        edgePos.append(edgePosi)
        
        # extend list of lw for all chunks
        lwGlobal.extend(lw)
        
        # calculate center line deviation
        COMmean = np.mean(COM)
        clDevN = [np.abs(cl - COMmean) for cl in COM]
        clDev.extend(clDevN)
    
        if show or e==1:
            plt.imshow(chunk,aspect='auto')
            
            for i, edge in enumerate(edgePos[e]):
                midX = COM[i//2]                 # find center of mas for each row of line
                edge = edge - x0[0]              
                if i%2==0:    
                    plt.plot(midX,i//2,'o',color='white',markersize=2)
                    # plt.vlines()
                    # plt.vlines(midX,i//2,i//2,colors='white') 
                    try:
                        edgePix = midX - int(edge/dx) # find edge position in pixels
                        plt.plot(edgePix,i//2,'x',color='r',markersize=2)
                    except:
                        try:
                            edgePix = edgePix - midX # if edgePos is invaid, plot a yellow marker at thesame distance as previous edgePos
                        except:
                            edgePix = midX - 0.5*midX
                        plt.plot(edgePix,i//2,'x',color='y',markersize=2)
                else: 
                    try:
                        edgePix = midX + int(edge/dx)
                        plt.plot(edgePix,i//2,'x',color='r',markersize=2)
                    except:
                        edgePix = edgePix + midX
                        plt.plot(edgePix,i//2,'x',color='y',markersize=2)
                # plt.vlines(edgePix,i//2,i//2,colors='r')
                # plt.vlines(COM,)            
                if debug:
                    print(f"midX:                {midX}")
                    print(f"edgePix:             {edgePix}")
                    print(f"Shape of chunk:      {np.shape(chunk)}")
                    print(f"Shape of edgePos:    {np.shape(edgePos)}")
                    print(f"Shape of edgePos[e]: {np.shape(edgePos[e])}")
                    
            plt.title(f"line #{e+1} of {len(chunks)}")
            plt.show()
    
    if debug:
        print(f" shape of lwMean: {np.shape(lwMean)}")
        # print(f"lwMean: {lwMean}")
        print(f" shape of lwGlobal: {np.shape(lwGlobal)}")
        # print(f"lwGlobal: {lwGlobal}")
        print(f" shape of lwDev:    {np.shape(lwDev)}")
        # print(f"lwDev: {lwDev}")
        
    if show:
        # plt.plot(lwMean,label='line widths')
        # plt.title('Average Line Widths')
        # plt.show()
        plt.plot(np.array(lwDev).flatten())
        plt.title('Line Width Deviations')
        plt.show()
        
        plt.imshow(lwDev,aspect='auto')
        plt.colorbar(label='line width')
        plt.show()
        
    rms  = np.sqrt(np.nanmean(np.square(lwGlobal)))   # rms of line width
    
    rmsd = np.sqrt(np.nanmean(np.square(np.array(lwDev).flatten()))) # rms deviation from mean line width, using local line widths
    
    # Eq 6 Mochi
    #standard deviation of the N lines detected in a single image is sigma:
    N = len(p1)    # number of lines detected in last row of image (assumed to be constant here)
    M = np.shape(I)[0] #len(lwGlobal)
    mu = np.nanmean(lwGlobal)
     
    sigma = np.nanmean( np.sqrt( np.nanmean( lwDevSqr) ) ) # changed to account for nans in lw array - made M values inaccurate
    # sigma = (1/N) * np.nansum( np.sqrt( (1/(M-1)) * np.nansum([l**2 for l in lwDev])))
        
        
    #line width roughness is calculated as 3*sigma:
    LWR = 3 * sigma
    
    CDU = 3*np.sqrt( np.nanmean([(l - mu)**2 for l in lwGlobal] )) # introduced CDU as global variation in line width

    CLR = 3*np.sqrt( np.nanmean( [cd**2 for cd in clDev]) ) #np.std(clDev)

    if debug:
        print('N: ', N)
        print('M: ', M)
        print('LW mean: ', mu)
        print('RMS = {}'.format(rms))
        print('RMSd = {}'.format(rmsd))
    
    print(f" shape of lwDev:    {np.shape(lwDev)}")
    print('N: ', N)
    print('M: ', M)
    #print('LWR = {}, N = {}, M = {}, mu = {}'.format(LWR,N,M,mu))
    print(f"CDU = {CDU}")
    print(f"CLR = {CLR}")
    print('LWR = {}'.format(LWR))
       
    return lwGlobal, rms, rmsd, LWR, CDU, CLR
        
            

def chunkit(A, D, P):
    """
    Extract overlapping vertical strips of width D centered at positions in P.

    Parameters:
    - A: 2D numpy array of shape (H, W)
    - D: int, width of each strip (should be odd for symmetric centering)
    - P: list or 1D numpy array of column center positions (integers)

    Returns:
    - strips: list of 2D numpy arrays, each of shape (H, D)
    """
    H, W = A.shape
    half_D = D // 2

    strips = []
    for center in P:
        start = center - half_D
        end = center + half_D + 1  # Python slices are exclusive on the right

        if start < 0 or end > W:
            # Optionally: skip or pad instead
            continue  # skip out-of-bounds strips

        strip = A[:, start:end]
        strips.append(strip)

    return strips
   


def LWR_JK(I,x,w,distance_tolerance = None,show=True, debug=False):
     """
     
     Extended version of LWR function to handle variable line widths.  A local 
     value of the nominal line width, specific to each line, is used to compute 
     the devian in width at each point along the line.
     
     Parameters
     ----------
     I : 2d intensity array.
     x : x-positions
     w : half-pitch of peaks.
     show : TYPE, optional
         DESCRIPTION. The default is True.
     debug : TYPE, optional
         DESCRIPTION. The default is False.
 
     Returns
     -------
     LW, rms, rmsd, LWR.
 
     """
    
     I = np.array(I)
     # threshold = np.mean(I) # moving thresholding to later - local threshold
     
     
     LW = [] # 2D array of line widths
     _LW = [] #1D array of line widths
     P = [] # peak positions in pixels
     for e,In in enumerate(I):    
         dx = x[1] - x[0]    
         d = int(w/dx)  # d is the nominal line width in units of pixels
 
         if distance_tolerance==None:
             distance_tolerance = d*1.9   # we can accept peak positions within the distance tolerance
     
         p1, _ = find_peaks(In, distance=d+8)   # the value of 8 was found by trial and error
         p2, _ = find_peaks(1-In, distance=d+8)
        
         if p1[0] < p2[0]:
             p1 = p1[1::]  # reject first value if it is a peak
         if p1[-1] > p2[-1]:
             p1 = p1[::-1] # reject last value if it is a peak
     
         p = np.concatenate((p1,p2))
         p.sort()
     
         sequenceOK, S = checkPeakTroughSequence(p1, p2)    
         if sequenceOK is False:
             print("Sequence check failed")
             p = [s[0] for s in S] # if sequence contains consecutive peaks/troughs then it is updated
                
         if debug:
             plt.plot(x,In)
             plt.plot(x[p1],In[p1],'x')
             plt.plot(x[p2],In[p2],'x')
             plt.show()
         
         P.append(p)
         edgePos=[]   
         print('p shape: ', np.shape(p))
         for i in range(len(p1)-1):
             print(f"iteration: {i}")
             # checking to make sure the peak being analysed lines up with the previous profile
             if e == 0: # first profile being analysed
                 dP = 0
             else:
                 print(P[e-1][i])
                 print(P[e][i])
                 dP = abs(P[e-1][i] - P[e][i])  # find difference between peak position of current and previous profile
                 print(dP)
                 print(d)
                
             if dP >= d/2:
                 print(f"peak #{i} does not line up with previous profile... adding nan")
                 edgePos.append(np.nan) # inserting an extra nan if the peak position is too far from the previous profile
             # print(f"iteration: {i}")
             
             xSeg = x[p[i]:p[i+1]]
             ISeg = In[p[i]:p[i+1]]
             
             try:
                 threshold = 0.6*np.max(ISeg)  # trys to define a threshold using maximum intensity of line
             except:
                 plt.plot(xSeg,ISeg)
                 plt.show()
                 edgePos.append(np.nan)
             
             else:
                 if len(xSeg) < distance_tolerance:
                     smodel = Model(sinefunction)
                     try:
                         a0 = np.min(ISeg)
                         if ISeg[0]>ISeg[-1]:
                             
                             b0 = -1*np.max(ISeg)   
                             c0 = xSeg[0] + (xSeg[1]-xSeg[0])
                         else:
                             
                             b0 = np.max(ISeg)
                             c0 = xSeg[0]
                             
                             
                         result = smodel.fit(ISeg, x=xSeg, a=a0, b=b0, c=c0)              
                     except:
                         print('Fit failed for line {}... ignoring.'.format(i))  
                         edgePos.append(np.nan)
                     else:
                         a = result.best_values['a']
                         b = result.best_values['b']
                         c = result.best_values['c']
                         pos =  np.arcsin((threshold-a)/b)-c
                         edgePos.append(pos)  #bad coding, but easily distinguised by filters below.
                         
                         # if debug is True:
                             #     #print(result.fit_report())
                             #     plt.plot(xSeg, ISeg, 'o', label='pattern')
                             #     plt.plot(xSeg, result.best_fit, 'o-', label='fit')
                             #     plt.vlines(pos,0,1)
                             #     plt.legend()
                             #     plt.show()  
                             #     pass
             # except:
                 # plt.plot(xSeg,ISeg)
                 # plt.show
                 # edgePos.append(np.nan)
         
         if debug is True:
             plt.plot(edgePos,'x:')
             plt.show()
     
         # The line width is the difference between the leading and trailing edge of a line (E6 in Mochi)
         lw = np.diff(edgePos)
         
         print('lw array shape')
         print(np.shape(lw))
         
         
         li  = len(lw)
         # lw = rejectNAN(lw) # commented out jk - want to keep nans in same line position
         lw = rejectOutliers(lw,3)  # reject outliers at > 3 std dev from mean
         # lw = lw[abs(lw)<w]  # reject any value that is larger than nominal linewidth
         #lw = lw[abs(lw)>w/10] # added JK to exclude spurious values of LW  < 1 nm.
         rejected = li - len(lw)
         if rejected>0:
             print('Edge detection: {} of {} failed'.format(rejected, li))
         
         # else:
         print('shape of lw:')
         print(np.shape(lw))
         LW.append(lw)
         _LW.extend(lw)
    
     LW = np.array(np.squeeze(LW))
     # LW = [l[0:len()]]
     print('LW array shape:')
     print(np.shape(LW))
     # ls = []
     for l in LW:
         print(np.shape(l))
         # ls.append(np.shape(l))
     # LW = [l[0:np.min(ls)] for l in LW]
     for _P in P:
         print(np.shape(_P))
         
     plt.imshow(LW)
     plt.colorbar()
     plt.show()
     LWT = np.array(LW).T
     print('new LW array shape:')
     print(np.shape(LWT))
     plt.imshow(LWT)
     plt.colorbar()
     plt.show()
     
     MU = []
     DL = []
     for l in LWT:
          # print('shape of l')
         # print(np.shape(l))
         mu = np.nanmean(l)
         # print('mean line width: ', mu)
         MU.append(mu)
         dl = (l - mu)**2
         # print('deviation from mean: ', dl)
         DL.append(dl)
    
     print('Shape of _LW')
     print(np.shape(_LW))
     
     print('Shape of DL')
     print(np.shape(DL))
     print(DL)
     DL = np.array(DL)
     np.shape(DL.flatten())
     
     rms  = np.sqrt(np.nanmean(np.square(_LW)))
     rmsd = np.sqrt(np.nanmean(np.square(np.subtract(_LW,w))))
     
     # Eq 6 Mochi
     #standard deviation of the N lines detected in a single image is sigma:
     N = len(p1)    # number of lines detected in last row of image (assumed to be constant here)
     M = len(_LW)
     mu = np.nanmean(MU)
     
     #sigma = (1/N)*np.sum(   np.sqrt((1/(M-1))* np.sum(  np.subtract(LW,mu)**2 )))
     sigma = (1/N)*np.nansum( np.sqrt((1/(M-1))* np.nansum( DL.flatten() )))
     
     #line width roughness is calculated as 3*sigma:
     LWR = 3 * sigma
     
     if debug:
         print('N: ', N)
         print('M: ', M)
         print('LW mean: ', mu)
         print('RMS = {}'.format(rms))
         print('RMSd = {}'.format(rmsd))
     
     #print('LWR = {}, N = {}, M = {}, mu = {}'.format(LWR,N,M,mu))
     print('LWR = {}'.format(LWR))
       
     return _LW, rms, rmsd, LWR
 
def LWR(I,x,w,distance_tolerance = None,show=True, debug=False):
    """
    Parameters
    ----------
    I : 2d intensity array.
    x : x-positions
    w : half-pitch of peaks.
    show : TYPE, optional
        DESCRIPTION. The default is True.
    debug : TYPE, optional
        DESCRIPTION. The default is False.

    Returns
    -------
    LW, rms, rmsd, LWR.

    """
   
    I = np.array(I)
    # threshold = np.mean(I) # moving thresholding to later - local threshold
    
    
    LW=[]
    for In in I:    
        dx = x[1] - x[0]    
        d = int(w/dx)  # d is the nominal line width in units of pixels

        if distance_tolerance==None:
            distance_tolerance = d*1.9   # we can accept peak positions within the distance tolerance
    
        p1, _ = find_peaks(In, distance=d+8)   # the value of 8 was found by trial and error
        p2, _ = find_peaks(1-In, distance=d+8)
       
        if p1[0] < p2[0]:
            p1 = p1[1::]  # reject first value
    
        p = np.concatenate((p1,p2))
        p.sort()
    
        sequenceOK = checkPeakTroughSequence(p1, p2)    
        if sequenceOK is False:
            print("Sequence check failed")
       
        
        edgePos=[]   
        print('p shape: ', np.shape(p))
        for i in range(len(p1)-1):
            
            print(f"iteration: {i}")
            
            xSeg = x[p[i]:p[i+1]]
            ISeg = In[p[i]:p[i+1]]
            threshold = 0.6*np.max(ISeg)
            
            if len(xSeg) < distance_tolerance:
                smodel = Model(sinefunction)
                try:
                    a0 = np.min(ISeg)
                    if ISeg[0]>ISeg[-1]:
                    
                        b0 = -1*np.max(ISeg)   
                        c0 = xSeg[0] + (xSeg[1]-xSeg[0])
                    else:
                        
                        b0 = np.max(ISeg)
                        c0 = xSeg[0]
                        
                    
                    result = smodel.fit(ISeg, x=xSeg, a=a0, b=b0, c=c0)              
                except:
                    print('Fit failed for line {}... ignoring.'.format(i))  
                    edgePos.append(np.nan)
                else:
                    a = result.best_values['a']
                    b = result.best_values['b']
                    c = result.best_values['c']
                    pos =  np.arcsin((threshold-a)/b)-c
                    edgePos.append(pos)  #bad coding, but easily distinguised by filters below.
                    
                    if debug is True:
                        #print(result.fit_report())
                        plt.plot(xSeg, ISeg, 'o', label='pattern')
                        plt.plot(xSeg, result.best_fit, 'o-', label='fit')
                        plt.vlines(pos,0,1)
                        plt.legend()
                        plt.show()  
                        pass
        
        if debug is True:
            plt.plot(edgePos)
            plt.show()
    
        # The line width is the difference between the leading and trailing edge of a line (E6 in Mochi)
        lw = np.diff(edgePos)
            
        li  = len(lw)
        lw = rejectNAN(lw)
        lw = rejectOutliers(lw,3)  # reject outliers at > 3 std dev from mean
        # lw = lw[abs(lw)<w]  # reject any value that is larger than nominal linewidth
        #lw = lw[abs(lw)>w/10] # added JK to exclude spurious values of LW  < 1 nm.
        rejected = li - len(lw)
        if rejected>0:
            print('Edge detection: {} of {} failed'.format(rejected, li))
        
        LW.extend(lw)
        
    rms  = np.sqrt(np.mean(np.square(LW)))
    rmsd = np.sqrt(np.mean(np.square(np.subtract(LW,w))))
    
    # Eq 6 Mochi
    #standard deviation of the N lines detected in a single image is sigma:
    N = len(p1)    # number of lines detected in last row of image (assumed to be constant here)
    M = len(LW)
    mu = np.mean(LW)
    
    sigma = (1/N)*np.sum(   np.sqrt((1/(M-1))* np.sum(  np.subtract(LW,mu)**2 )))
    
    #line width roughness is calculated as 3*sigma:
    LWR = 3 * sigma
    
    if debug:
        print('N: ', N)
        print('M: ', M)
        print('LW mean: ', mu)
        print('RMS = {}'.format(rms))
        print('RMSd = {}'.format(rmsd))
    
    #print('LWR = {}, N = {}, M = {}, mu = {}'.format(LWR,N,M,mu))
    print('LWR = {}'.format(LWR))
      
    return LW, rms, rmsd, LWR


#N:  121
#M:  3424
#LW mean:  2.5632687618769656e-08
#RMS = 7.160694522099752e-05
#RMSd = 7.16069406360065e-05
#LWR = 1.7756380052532015e-06
#
#N:  121
#M:  3424
#LW mean:  2.5704264927026704e-08
#RMS = 2.8949090102576417e-08
#RMSd = 1.3335537912501033e-08
#LWR = 3.302200037084337e-10

def NILS(I,x,w,show=True):
    '''
    Calculate Normalized Image Log-Slope (NILS) of a pattern
    
    NILS = w(dln(I)/dx)
    
    pattern:  a 2d array that can be cast to float64 values, expected to contain 
              periodic patterns over axis 0 or 1.
              
    I: list of intensity values
    x: list of positions corresponding to the intensity values
    w: nominal linewidth
    
    
    Modified by JK for line profiles
    '''
    
    # lnI = np.log(I[:,0].astype('float64')) 
    lnI = np.log(I).astype('float64')
#    lnI = lnI.astype('float64')

    dx = (x[1] - x[0])
    d_dx = FinDiff(0, dx)
    gradAbs = np.abs(d_dx(lnI,acc=10))
    
    d = int(w/dx)
    
    # if distance_tolerance == None:
    #     distance_tolerance = d #*1.5
    # print("x[0], x[1]: {}".format((x[0],x[1])))
    # print("d: {}".format(d))
    # print("dx: {}".format(dx))
    # print("d_dx: {}".format(d_dx))
    # print("gradAbs: {}".format(gradAbs))
    
    p1, _ = find_peaks(lnI, distance=d)#+8)
    p2, _ = find_peaks(1-lnI, distance=d)#+8)
    
    
  
    
    # plt.plot(x[p1],'.')
    # plt.title('x(p1)')
    # plt.show()
    # plt.plot(x[p2],'.')
    # plt.title('x(p2)')
    # plt.show()
    
    # print("p1: {}".format(p1))
    #p =  [x for x in chain.from_iterable(zip_longest(p1, p2)) if x is not None]
    
    p = np.concatenate((p1,p2))
    p.sort()
    
    LWpx =  np.divide(np.diff(p),2)   # check whether division of two follows defintion
    LW = np.multiply(LWpx,dx)
    meanLW = np.mean(LW)
        
    # print("sep: {}".format(sep))
    #p = [x+sep for x in p[:-1]]
    p = np.add(p[:-1], LWpx.astype(int) )
    
    #NILS = np.divide(np.multiply(w,gradAbs[p]),I[p])
    nils = np.multiply(w,gradAbs[p])
    #Check for outliers:
    NILS = []
    for n in nils:
        if n>np.pi:
           pass
        else:
           NILS.append(n)
    
    meanNILS = np.mean(NILS)
    
    rmsNILS = np.sqrt(np.mean(np.square(NILS)))
    
    rmsdNILS  = np.sqrt(np.mean(np.square(NILS-meanNILS)))
    
    stdNILS = np.std(NILS)/meanNILS # changed from 3*np.std(NILS) by JK
    
    rmsLW   = np.sqrt(np.mean(np.square(np.multiply(2,LW)))) # undo the division by two above
    rmsdLW = np.sqrt(np.mean(np.square(LW-w)))
    
    
    if show == True:
        plt.plot(x[p], lnI[p],'x') #, label='p')
        plt.plot(x[p1], lnI[p1],'x', label='p1' )
        plt.plot(x[p2], lnI[p2],'x', label='p2' )
        plt.plot(x, lnI, label='ln(I)')
        # plt.plot(x,np.max(lnI)*I/np.max(I),label='I (norm.)') # [:,0] removed for 1d profile - jk
        # plt.xlim([-0.22e-6,0.2e-6])
        plt.legend()
        plt.show()
        print('w: {}'.format(w))
        print('number of edges: {}'.format(len(NILS)))
        print('NILS mean: {}'.format(meanNILS))
        print('NILS rms: {}'.format(rmsNILS))
        print('LW mean: {}'.format(meanLW))
        print('LW rms: {}'.format(rmsLW))
        print('LW rmsd: {}'.format(rmsdLW))
        plt.clf()
        plt.close()
        # plt.plot(gradAbs[p])
        # plt.plot(NILS,'x:')
        # plt.show()
        
    # """
    # Calculate mean NILS and average peak-trough distance from a 1D intensity profile,
    # ensuring proper peak-trough alternation and reasonable spacing.

    # Parameters:
    #     profile (array-like): 1D intensity profile
    #     w (float): Physical width of peak (e.g., in microns)
    #     dx (float): Pixel size (same units as w)
    #     debug_plot (bool): Show debug plot with annotations
    #     distance_tolerance (float): Acceptable multiple of w for peak-trough spacing

    # Returns:
    #     mean_nils (float): Mean NILS across all peak sides
    #     mean_distance (float): Mean peak-to-trough distance (in physical units)
    # """
    # profile = np.asarray(I, dtype=np.float64)

    # # Replace non-positive values to avoid log issues
    # min_positive = np.min(profile[profile > 0])
    # profile[profile <= 0] = min_positive * 1e-3

    # log_I = np.log(profile)
    # dlogI_dx = np.gradient(log_I, dx)

    # # Find peaks and troughs
    # peaks, _ = find_peaks(profile,distance=d) # got rid of +8 - JK
    # troughs, _ = find_peaks(-profile,distance=d)

    # # Sanity check: ensure alternating sequence
    # sequence = [(pos, 'peak') for pos in peaks] + [(pos, 'trough') for pos in troughs]
    # sequence.sort()
    # bad_sequence_found = False
    # for i in range(1, len(sequence)):
    #     if sequence[i][1] == sequence[i - 1][1]:
    #         print(f"  Warning: Found two consecutive {sequence[i][1]}s at indices {sequence[i - 1][0]}, {sequence[i][0]}")
    #         bad_sequence_found = True
    #         break

    # nils_values = []
    # distances = []
    # midpoint_indices = []
    # skipped = 0

    # for peak in peaks:
    #     # Find nearest left and right troughs
    #     left_troughs = troughs[troughs < peak]
    #     right_troughs = troughs[troughs > peak]

    #     valid = False

    #     if len(left_troughs) > 0:
    #         left = left_troughs[-1]
    #         dist = (peak - left) * dx
    #         if dist < distance_tolerance * dx:
    #             mid_left = int(round((peak + left) / 2))
    #             if 1 <= mid_left < len(profile) - 1:
    #                 slope_left = dlogI_dx[mid_left]
    #                 nils_values.append(w * slope_left)
    #                 distances.append(dist)
    #                 midpoint_indices.append(mid_left)
    #                 valid = True

    #     if len(right_troughs) > 0:
    #         right = right_troughs[0]
    #         dist = (right - peak) * dx
    #         if dist < distance_tolerance * dx:
    #             mid_right = int(round((peak + right) / 2))
    #             if 1 <= mid_right < len(profile) - 1:
    #                 slope_right = dlogI_dx[mid_right]
    #                 nils_values.append(w * slope_right)
    #                 distances.append(dist)
    #                 midpoint_indices.append(mid_right)
    #                 valid = True

    #     if not valid:
    #         skipped += 1

    # if show:
    #     x = np.arange(len(profile)) * dx
    #     plt.figure(figsize=(10, 4))
    #     plt.plot(x, profile, label='Intensity Profile', color='blue')
    #     plt.scatter(x[peaks], profile[peaks], color='red', marker='^', label='Peaks')
    #     plt.scatter(x[troughs], profile[troughs], color='green', marker='v', label='Troughs')
    #     plt.scatter(x[midpoint_indices], profile[midpoint_indices], color='orange', marker='x', label='Midpoints')
    #     plt.xlabel('Position')
    #     plt.ylabel('Intensity')
    #     plt.title('NILS Debug Plot')
    #     plt.legend()
    #     plt.grid(True)
    #     plt.tight_layout()
    #     plt.show()
        
    #     plt.plot(x, log_I, label='Intensity Profile (log)', color='blue')
    #     plt.plot(x, np.max(log_I)*(dlogI_dx/np.max(dlogI_dx)), label='Intensity gradient (log)', color='blue')
    #     plt.scatter(x[peaks], log_I[peaks], color='red', marker='^', label='Peaks')
    #     plt.scatter(x[troughs], log_I[troughs], color='green', marker='v', label='Troughs')
    #     plt.scatter(x[midpoint_indices], log_I[midpoint_indices], color='orange', marker='x', label='Midpoints')
    #     plt.xlabel('Position')
    #     plt.ylabel('Intensity')
    #     plt.title('NILS Debug Plot')
    #     plt.legend()
    #     plt.grid(True)
    #     plt.tight_layout()
    #     plt.show()

    # mean_nils = np.mean(np.abs(nils_values)) if nils_values else np.nan
    # mean_distance = np.mean(distances) if distances else np.nan

    
    # NILS = [abs(n) for n in nils_values]
    # LW = [abs(d) for d in distances]
    # rmsNILS = np.sqrt(np.mean(np.square(NILS)))
    # rmsLW = np.sqrt(np.mean(np.square(LW)))
    
    # meanNILS = np.mean(np.abs(NILS)) if NILS else np.nan
    # meanLW = np.mean(LW) if LW else np.nan
    
    # rmsdNILS = np.sqrt(np.mean(np.square(NILS-meanNILS)))
    # rmsdLW = np.sqrt(np.mean(np.square(LW - meanLW)))
    # p1 = peaks
    # stdNILS = np.std(NILS) / meanNILS
    
    # print('NILS mean: {}'.format(meanNILS))
    # print('NILS rms: {}'.format(rmsNILS))
    # print('LW mean: {}'.format(meanLW))
    # print('LW rms: {}'.format(rmsLW))
    # print('LW rmsd: {}'.format(rmsdLW))

    # print(f" Processed {len(peaks)} peaks | Skipped: {skipped} | Valid NILS values: {len(NILS)}")
    # if bad_sequence_found:
    #     print("  Note: Peak/trough sequence inconsistency found  consider pre-filtering.")
        
    return meanNILS,  meanLW, NILS, LW, rmsNILS, rmsLW, rmsdLW, p1, rmsdNILS, stdNILS



def gratingContrastFourier(A,x, show=True):
    '''
    Fourier contrast:  amplitude of the  fundamental  frequency
    
    The estimation of contrast, using the measured magnitudes of the fundamental frequency and the DC, is correct in an ideal case.
    However, it is subject to deviations due to discretization and 'spectral leakage '
    
    A: signal, i.e. intensity
    ** Here A is assumed to be 1D
    x: list of positions corresponding to A
    
    is scaling by sqrt(2) needed for comparison to Michelsen contrast?
    
    
    THIS STILL NEEDS TO BE CHECKED  USE WITH CAUTION
    '''
       
    N = np.size(A)
    xstep = x[1]-x[0]
    
    '''
    #get the FFT of I
    Af = fft(A)
    
    # Amplitudes
    amplitudes = 2/N * np.abs(Af)
   
    # The corresponding spatial frequencies
    frequencies = fftfreq(N, d=xstep)
    
    # Find the peak frequency
    posMask = np.where(frequencies > 0) # consider only +ve
    fr =  frequencies[posMask]
    peakFrequency = fr[amplitudes[posMask].argmax()]

    if show is True:
#        plt.plot(x, A)
#        plt.title('Intensity')
#        plt.show()
#        
        #plt.semilogx(frequencies[:len(frequencies) // 2], amplitudes[:len(Af) // 2])
        plt.plot(frequencies[:len(frequencies) // 2], amplitudes[:len(Af) // 2])
        plt.title('Fourier Amplitudes')
        plt.show()
        
        
        plt.plot(frequencies[len(frequencies) // 2:len(frequencies) // 2 + 500], amplitudes[len(frequencies) // 2:len(frequencies) // 2 + 500])
        plt.title('Fourier Amplitudes (partial)')
        plt.show()

    #C = amplitudes[0] 
    
    C =  (1/(4*pi)) * 1/(xstep/1e-9) * 2/xstep * np.sqrt(2)/sqrt(square(abs(Af[0]))-np.sum(square(abs(Af[3:])))) / abs(Af[0])
    '''
    
    fs = 1/xstep   # number of samples per m    
    sfft =  fft(A)
    freqs = fftfreq(len(A)) * fs
    
    print('DEBUG: freqs ', np.shape(freqs))
    
    s = np.abs(sfft)[len(sfft)//2+1:] #[:,0] - taken out by jk for 1d profiles
    f = freqs[len(sfft)//2+1:]
    print('DEBUG: s ', np.shape(s))
    print('DEBUG: f ', np.shape(f))
    
#    m = np.squeeze(argrelextrema(np.abs(s), np.greater, order=4)) #array of indexes of the  maxima

    m = argrelextrema(np.abs(s), np.greater, order=10) #array of indexes of the  maxima
    if np.array(m).ndim > 1:
        if np.shape(m)[0] == 0:
#            print("here 1")
            print(m[1])
            m = m[1]        
        elif np.shape(m)[1] == 0:
#            print("here 2")
            print(m[0])
#        np.array(np.squeeze(m)).ndim == 1:
#            print("here", np.array(np.squeeze(m)).ndim)
            m = m[0] #np.squeeze(m)
        else:
#            print("here 3")
            m = m[0]


    print('DEBUG: m ', np.shape(m))

    y = [s[i-1] for i in m]
    x = [f[i-1] for i in m]
    
    print('DEBUG: y ', np.shape(y))
    print('DEBUG: x ', np.shape(x))
    
    
    try: 
        #print('length y ', np.shape(y), ' length m ', np.shape(m))
        index_max = np.argmax(y)
        
        print('DEBUG: index_max ', index_max)
        #print(m)
        #print(y)
        
        #print('m: ', m[0])
        #print(m[0][index_max])
        
        
        ymax = s[m[index_max]]
        xmax = f[m[index_max]]
        
        #print('ymax ', ymax)
        if show == True:
            plt.stem(freqs, np.abs(sfft), label='frequencies')
            # plt.plot(sfft)
            # plt.legend()
            # plt.show()
            # plt.plot(s, label='s')
            # plt.legend()
            # plt.show()
            
            # plt.plot(f, label='f')
            plt.xlabel("Frequency")
            plt.ylabel("Amplitude")
            # plt.xlim(-100,100)
            # plt.show()
            #plt.plot(freqs, np.abs(sfft))#,linefmt=next(cycol),label=label)
            
            plt.plot(x, y, 'x', label='dominant frequencies')
            # # plt.show()
        
            plt.plot(xmax, ymax, 'o', label = 'maximum amplitude')
            plt.legend()
            plt.show()
        
        print("Central Amplitude:        {}".format(np.max(np.abs(sfft))))
        print("Central Amplitude - ymax: {}".format(np.max(np.abs(sfft))-ymax))
        print("sum(s):                   {}".format(np.sum(s)))
        print("ymax:                     {}".format(ymax))
        print("sum(s)-ymax:              {}".format(np.sum(s)-ymax))
        fmax = np.max(np.abs(sfft))
        
    #    C = ymax/(np.sum(s)-ymax)
        C = ymax/(fmax-ymax)
        
        # first = abs((2*(ymax**2)) - (fmax**2))
        # print("first: ", first)
        # C = (np.sqrt(first))/fmax
        
    #    C = np.sqrt(((2*np.sum(s)**2-ymax**2)))/ymax
        
        print('Fourier Contrast: ', C)
    #return C, amplitudes, frequencies, peakFrequency
        return C, sfft, freqs, xmax
    
    except:
        return 0,0,0,0


def integralOpticalDensity(I,bins=256):
    '''
    calculate the integral optical density of an image from
    the histogram, which reflects the global performance of an image
    
    Set bins to a value appropriate to numerical type of I (could be done automatically)
    
    Returns:
        IOD
        IODM: maximum IOD for an image with the same number of grey levels and pixel count
        H: histogram of intensity over  a number of grey levels equal to bins
    '''
    I = bins* (I-np.min(I))/ (np.max(I)-np.min(I))
    #H, intensityBin =  np.histogram(I, bins=bins-1)
    
    H, binEdges = np.histogram(I, bins=bins)
    binCenters = binEdges[:-1] + np.diff(binEdges)/2
    
    IOD=0
    for i in range(np.shape(H)[0]):
        IOD += H[i]*binCenters[i]
        
    IODM =  np.size(I)*(bins-1)/2

    return  IOD, IODM, H, binEdges[:-1],binCenters
    


def meanDynamicRange(I, show=False):
    '''
    Calculate mean dynamic range of intensity values I using method of Lai and Von 
    Bally.
    This may be used to estimate fringe visibility in a way that is less sensitive
    to noise and more appropriate simply using V = (Imax-IMin)/(Imax-Imin)
    
    
    C compositely represents the mean dynamic range and greyscale imbalance of an
    image. Only when Cl and C2 reach the maximum values simultaneously,
    does C obtain the maximum value.The variation of C is related not only to the 
    variation of the greylevel of pixels, but also to the amount of pixels whose 
    greylevel varies.
    Thus noises with either a relative low number or relative small intensity do 
    not result in great variance of the contrast of the image itself.
    '''
    
    I1 = np.ravel(I)  # reduce 2D to 1D
    IOD,IODM,H,binEdges,binCenters = integralOpticalDensity(I1)
    
    
    # find mean of histogram and index (bin) of mean
    meanH = IOD/np.sum(H)
    #index = list(map(lambda k: k < meanH, H)).index(True)
    # index=int(meanH)  # check this carefully
    index = np.searchsorted(binCenters, meanH)
    
    N= np.size(H)
    Id = sum([x * y for x, y in zip(binCenters[:index],H[:index])]) / sum(H[:index]+1e-10)
    Ib = sum([x * y for x, y in zip(binCenters[index:N],H[index:N])]) / sum(H[index:N]+1e-10)
    
    
    if show == True:
        plt.plot(H)
        plt.axvline(x=Id, color='g', label='Upper mean')
        plt.axvline(x=meanH, color='r', label='Mean')
        plt.axvline(x=Ib, color='b', label='Lower Mean')
        plt.legend()
        plt.show()
    
    C1 = (Ib-Id)/(Ib+Id) # mean dynamic range (definition 1)
    
    
    if IOD<=IODM:
        C2 = IOD/IODM    # mean dynamic range (definition 2)
    else:
        C2 = 2 - IOD/IODM
        
    # Unfortunately,neither C1 or C2 is suficient for estimating contrast in all cases
    # Lai and Von Bally suggest the composite:
    C = C1*C2
        
    return C, C1, C2


def composite_contrast_from_hist(H, binCenters, IOD, IODM, show=False):
    """
    Compute composite contrast C from a fixed histogram.
    """

    # mean of histogram (optical density weighted)
    meanH = IOD / np.sum(H)

    # index of mean
    index = np.searchsorted(binCenters, meanH)
    index = np.clip(index, 1, len(H) - 1)

    # dark and bright means
    Id = np.sum(binCenters[:index] * H[:index]) / (np.sum(H[:index]) + 1e-10)
    Ib = np.sum(binCenters[index:] * H[index:]) / (np.sum(H[index:]) + 1e-10)

    if show:
        plt.plot(H)
        plt.axvline(x=index, color='r', label='Mean index')
        plt.legend()
        plt.show()

    # definition 1
    C1 = (Ib - Id) / (Ib + Id + 1e-10)

    # definition 2
    if IOD <= IODM:
        C2 = IOD / IODM
    else:
        C2 = 2 - IOD / IODM

    return C1 * C2, C1, C2

def meanDynamicRange_with_uncertainty(
    I,
    bins=256,
    n_mc=1000,
    resample_mode="poisson",  # "poisson" or "multinomial"
    show=False
):
    """
    Compute composite contrast C and its uncertainty via histogram-domain Monte Carlo.
    """

    # flatten image
    I1 = np.ravel(I)

    # original histogram + optical density terms
    IOD, IODM, H, binEdges, binCenters = integralOpticalDensity(I1)

    # normalize histogram to integer counts if needed
    H = np.asarray(H, dtype=float)

    # compute nominal value
    C0, C1_0, C2_0 = composite_contrast_from_hist(
        H, binCenters, IOD, IODM, show=show
    )

    # Monte Carlo resampling
    C_vals = np.zeros(n_mc)

    for k in range(n_mc):
        if resample_mode == "poisson":
            H_star = np.random.poisson(H)
        elif resample_mode == "multinomial":
            H_star = np.random.multinomial(int(np.sum(H)), H / np.sum(H))
        else:
            raise ValueError("resample_mode must be 'poisson' or 'multinomial'")

        C_vals[k], _, _ = composite_contrast_from_hist(
            H_star, binCenters, IOD, IODM
        )

    # statistics
    results = {
        "C": C0,
        "C_std": np.std(C_vals, ddof=1),
        "C_median": np.median(C_vals),
        "C_ci_68": np.percentile(C_vals, [16, 84]),
        "C_ci_95": np.percentile(C_vals, [2.5, 97.5]),
        "C_samples": C_vals,
        "C1": C1_0,
        "C2": C2_0,
    }

    return results


def correlationCoefficient(A, expected):
    return np.corrcoef(A,expected)[1,0]


def fidelity(A, reference):
    """
    Calculate fidelity as measure of similarity of A to reference
    """
    a = np.sqrt((reference-A)**2)
    b = abs(reference+A)
    c = 1/(np.size(A))
    fidelity = 1-(np.sum(a)/np.sum(b))*c
    return fidelity


def interferenceIntensityTMTM(x,k,theta,A = 1.0):
    '''
    Generate intensity profile for interfernce between TM polarised beams from
    a pair of diffraction gratings.  Based on 
    
    X Wang et al, Proceedings Volume 10809, International Conference on Extreme Ultraviolet 
    Lithography 2018; 108091Z (2018) https://doi.org/10.1117/12.2501949
    
    For two TM polarized beams, the electric field is parallel to the incident plane 
    and can be decomposed in the x and z directions regarding incident angle. In this 
    case, assuming 0 initial phases, equal amplitudes A, with the azimuthal angles 
    ϕ1 = 0°, ϕ2 = 180° and polarization angles ψ1 = 0°, ψ2 = 0°, the electric fields 
    are:
  
      E1 = A*exp(i*(k*x*np.sin(theta) - k*x*cos(theta )))
      E2 = A*exp(i*(-k*x*np.sin(theta) - k*x*cos(theta )))

    The polarisation vectors are :

      p1 = cos(theta)*y*iv+sin(tehta)*z*kv
      p2 = cos(theta)*y*iv-sin(tehta)*z*kv

    where iv, jv, kv is unit vector in x direction (i,j,k notation)
    '''
    I = 2.*square(A) + 2.*square(A) * cos(2.*k*x*sin(theta))*cos(2.*theta)
   
    return I


def interferenceIntensityTETE(x,k,theta,A = 1.0):
    '''
    Generate intensity profile for interfernce between TE polarised beams from
    a pair of diffraction gratings.  Based on 
    
    X Wang et al, Proceedings Volume 10809, International Conference on Extreme Ultraviolet 
    Lithography 2018; 108091Z (2018) https://doi.org/10.1117/12.2501949
    
    '''
    I = 2.*square(A) + 2.*square(A) * cos(2.*k*x*sin(theta))
    
    return I
    
    
def interferenceIntensityTMTE(x,k,theta,gamma, A = 1.0):
    '''
    Generate intensity profile for interfernce between a TE and TM polarised beam from
    a pair of diffraction gratings.  Based on 
    
    X Wang et al, Proceedings Volume 10809, International Conference on Extreme Ultraviolet 
    Lithography 2018; 108091Z (2018) https://doi.org/10.1117/12.2501949
    
    Polarization may by controlled by rotating the grating by certain angle gamma
    (e.g., 45°) In this case, for two-beam interference, the two diffracted beams 
    will carry both TE and TM polarizations. 
    
    '''
    I = 2.*square(A)+square(cos(gamma))* \
        (2. + cos(2.*k*x*cos(gamma)*sin(theta)) * cos(2.*theta) + \
        2.*cos(2.*k*cos(gamma)*x*sin(theta)))
    
    return I
    
    
    
def interferenceIntensity(x,k,theta, A = 1.0, gamma=0, polarisationModes=('TM','TM')):

    if (polarisationModes[0] == 'TE' and polarisationModes[1] == 'TE'):
        I = interferenceIntensityTETE(x,k,theta,A)
         
    if (polarisationModes[0] == 'TM' and polarisationModes[1] == 'TM'):
        I = interferenceIntensityTMTM(x,k,theta,A)
    
    if ((polarisationModes[0] == 'TE' and polarisationModes[1] == 'TM') \
       or (polarisationModes[0] == 'TM' and polarisationModes[1] == 'TE')):
        I = interferenceIntensityTMTE(x,k,theta,gamma,A)    
    return I



def whiteNoise(rho, sr, n, mu=0):
    '''
    parameters: 
    rho - spectral noise density unit/SQRT(Hz)
    sr  - sample rate
    n   - no of points
    mu  - mean value, optional
    
    returns:
    n points of noise signal with spectral noise density of rho
    '''
    sigma = rho * np.sqrt(sr/2)
    noise = np.random.normal(mu, sigma, n)
    return noise


def test_models():
    
   
    ''' define interference grating parameters'''
    wl = 13.5e-9 # wavelength in m
    #wl = 6.7e-9  # wavelength in m

    # Amplitude of both beams (assumed equal)
    A = 1.0  # this may be scaled to  match simulated intensity
    
    k = 2*np.pi/wl
    
    m = 1 # order of diffracted beams from each grating
    d = 20.e-9 # grating spacing
    
    # angle between the beams from each grating
    theta = np.arcsin( m *wl/d)
    
    #define x positions:
    dx=0.5e-9
    #number of points:
    n = 2000
    # grid:
    x =  np.linspace(-dx*int(n/2),dx*int(n/2),n) 
    
    cl=[]
    pl = np.linspace(20e-9, 200e-9, 10)
    plt.title('13.5 nm')
    for p in pl: 
        t=np.arcsin( m *wl/p)
        I = interferenceIntensity(x,k,t,A=A, polarisationModes=('TM','TM'))
        c = gratingContrastMichelson(I)
        cl.append(c)
        plt.plot(x*1e6, I, label='TM-TM, pitch = {:.0f} nm, contrast = {:.2f}'.format(p/1e-9, c))
        plt.legend()
    plt.show
    

    ''' plot dependence on grating pitch for TM-TM   (close-up)  '''
    
    plt.title('13.5 nm')
    for p in np.linspace(10e-9, 200e-9, 11):
        t=np.arcsin( m *wl/p)
        I = interferenceIntensity(x,k,t,A=A, polarisationModes=('TM','TM'))
        c = gratingContrastMichelson(I)
        plt.plot(x*1e6, I, label='TM-TM, pitch = {:.0f} nm, contrast = {:.2f}'.format(p/1e-9, c))
        plt.xlim(-0.05,0.05)
        plt.legend()
    plt.show
    
    
    ''' plot dependence on grating pitch for TM-TM   (close-up)  '''
    
    plt.title('13.5 nm RMS')
    for p in np.linspace(10e-9, 200e-9, 11):
        t=np.arcsin( m *wl/p)
        I = interferenceIntensity(x,k,t,A=A, polarisationModes=('TM','TM'))
        c = gratingContrastRMS(I)
        plt.plot(x*1e6, I, label='TM-TM, pitch = {:.0f} nm, contrast = {:.2f}'.format(p/1e-9, c))
        plt.xlim(-0.05,0.05)
        plt.legend()
    plt.show
    
    
    ''' plot dependence on grating pitch for TE-TE '''
    
    plt.title('13.5 nm')
    for p in np.linspace(20e-9, 200e-9, 10):
        t=np.arcsin( m *wl/p)
        I = interferenceIntensity(x,k,t,A=A, polarisationModes=('TE','TE'))
        c = gratingContrastMichelson(I)
        plt.plot(x*1e6, I, label='TE-TE, pitch = {:.0f} nm, contrast = {:.2f}'.format(p/1e-9, c))
        plt.xlim(-0.05,0.05)
        plt.legend()
    plt.show
    
    ''' plot dependence on grating pitch for TE-TE '''
    
    plt.title('13.5 nm RMS')
    for p in np.linspace(20e-9, 200e-9, 10):
        t=np.arcsin( m *wl/p)
        I = interferenceIntensity(x,k,t,A=A, polarisationModes=('TE','TE'))
        c = gratingContrastRMS(I)
        plt.plot(x*1e6, I, label='TE-TE, pitch = {:.0f} nm, contrast = {:.2f}'.format(p/1e-9, c))
        plt.xlim(-0.05,0.05)
        plt.legend()
    plt.show
    
    
    
    
    
    ''' Compare RMS and Fourier contrast vs grating pitch '''
    
    #define x positions:
    dx=1e-9
    #number of points:
    n = int(10e-6/dx)
    # grid:
    x =  np.linspace(-dx*int(n/2),dx*int(n/2),n) 
    
    fig, ax1 = plt.subplots()
    plt.title('TM-TM [10000 x 1 nm pixels]')
    ax2 = ax1.twinx()
  
    ax1.set_xlabel('Grating pitch (nm)')
    ax1.set_ylabel('RMS contrast, Michelson Contrast')
    ax2.set_ylabel('Fourier Contrast', color='b')

    cml=[]
    crl=[]
    fl = []
    pl = np.linspace(20e-9, 200e-9, 400)
    for p in pl: 
        t=np.arcsin( m *wl/p)
        I = interferenceIntensity(x,k,t,A=A, polarisationModes=('TM','TM'))
        
        ''' generate noise '''
        rho=1e-2
        sr = n  # (as period = n/sr)
        noise = whiteNoise(rho, sr, n, mu=0)
        I = I - noise
        
        
        cr = gratingContrastRMS(I)
        cm = gratingContrastMichelson(I)
        
        f, amplitudes, frequencies, peakFrequency = gratingContrastFourier(I,x, show=False)
        crl.append(cr)
        cml.append(cm)
        fl.append(f)
        
    ax1.plot(pl/1e-9, crl, 'g-', label='RMS')
    ax1.plot(pl/1e-9, cml, 'r-',  label='Michelson')
    ax2.plot(pl/1e-9, fl,  'b-', label='Fourier')
    ax1.set_ylim([0,1.2])
    ax1.set_ylim([0,1.2])
    plt.legend()

    plt.show()
    
    #########
    

    ''' Compare RMS and Fourier contrast vs noise '''
    
    #define x positions:
    dx=1e-9
    #number of points:
    n = int(10e-6/dx)
    # grid:
    x =  np.linspace(-dx*int(n/2),dx*int(n/2),n) 
    
    
    plt.title('TM-TM [10000 x 1 nm pixels]')
   
  
    plt.xlabel('rho (proportional to noise)')
    plt.ylabel('contrast')
    

    cml=[]
    crl=[]
    fl = []
    nl=[]
    Il=[]
    Imean = []
    p = 40e-9
    rho = np.linspace(0,4e-3,100)
    t=np.arcsin( m *wl/p)
    I0 = interferenceIntensity(x,k,t,A=A, polarisationModes=('TM','TM'))
    sr = n  # (as period = n/sr)


    for r in rho:
        noise = whiteNoise(r, sr, n, mu=0)
        nl.append(noise)
        I = I0 - np.mean(noise) + noise
        Imean.append(np.mean(I))
        Il.append(I)
        
        
        cr = gratingContrastRMS(I)
        cm = gratingContrastMichelson(I)
        
        f, amplitudes, frequencies, peakFrequency = gratingContrastFourier(I,x, show=False)
        crl.append(cr)
        cml.append(cm)
        fl.append(f)
        
    plt.plot(rho, crl, 'g-', label='RMS')
    plt.plot(rho, cml, 'r-',  label='Michelson')
    plt.plot(rho, fl,  'b-', label='Fourier')
    plt.legend()

    plt.show()
    
    
    #check that mean doesn't change
    plt.plot(rho, Imean)
    plt.show()
    
    
    # compare distributions:
    
    for noise in nl[::5][1:]:
        plt.hist(noise, bins=50, histtype='step')
    plt.gca().set(title='Noise Frequency Histogram', ylabel='Frequency');
    plt.show()
    
    for In in Il[::5][1:]:
        plt.hist(In, bins=50, histtype='step')
    plt.hist(I0, bins=50)    
    plt.gca().set(title='Intensity Frequency Histogram ', ylabel='Frequency');
    plt.show()
    
    
    #########
    
    
     #define x positions:
    dx=0.1e-9
    #number of points:
    n = 2000
    # grid:
    x =  np.linspace(-dx*int(n/2),dx*int(n/2),n) 
    
        # angle between the beams from each grating
    theta = np.arcsin( m *wl/d)
    
    
    ITMTM = interferenceIntensity(x,k,theta,A=A, polarisationModes=('TM','TM'))
    ITETE = interferenceIntensity(x,k,theta,A=A, polarisationModes=('TE','TE'))
   
    plt.title('13.5 nm, 40 nm pitch')
    plt.plot(x*1e6,ITETE, label='TE-TE, contrast = {:.2f}'.format(gratingContrastMichelson(ITETE)))
    plt.plot(x*1e6,ITMTM, label='TM-TM, contrast = {:.2f}'.format(gratingContrastMichelson(ITMTM)))

    for gamma in [np.pi/4]:  #np.linspace(0, np.pi/8, 2*np.pi):
        ''' generate interference intensity'''
        ITMTE = interferenceIntensity(x,k,theta, gamma=gamma, A=A, polarisationModes=('TM','TE'))

        
    #    ''' plot TM-TM intensity'''
    #    plt.plot(x*1e6,ITMTM, label='TM-TM')
    #    plt.xlabel('Position [um]')
    #    plt.ylabel('Intensity [a.u.]')
    #    plt.legend()
    #    plt.rcParams["figure.figsize"] = [7,4]
    #    plt.show()
    #    
    #    ''' plot TE-TE intensity'''
    #    plt.plot(x*1e6,ITETE, label='TE-TE')
    #    plt.xlabel('Position [um]')
    #    plt.ylabel('Intensity [a.u.]')
    #    plt.legend()
    #    plt.rcParams["figure.figsize"] = [7,4]
    #    plt.show()
    #
    #    ''' plot TM-TE intensity'''
    #    plt.plot(x*1e6,ITMTE, label='TM-TE')
    #    plt.xlabel('Position [um]')
    #    plt.ylabel('Intensity [a.u.]')
    #    plt.legend()
    #    plt.rcParams["figure.figsize"] = [7,4]
    #    plt.show()
        
        ''' plot all '''
        plt.plot(x*1e6,ITMTE, label='TM-TE, contrast = {:.2f}'.format(gratingContrastMichelson(ITMTE)))
        
    plt.xlabel('Position [um]')
    plt.ylabel('Intensity [a.u.]')
    plt.legend()
    plt.rcParams["figure.figsize"] = [7,4]
    plt.show()
    
    
    
    
    ''' Messing around with sums '''
    

    ## interpret with caution!! Summation should be done as coherent sum of E
    ITETE = interferenceIntensity(x,k,theta, A=A, polarisationModes=('TE','TE'))
    
    ITMTE = interferenceIntensity(x,k,theta, gamma=np.pi/8, A=A, polarisationModes=('TM','TE'))
    I = ITETE+ITMTE
    c=gratingContrastRMS(I)
    plt.plot(I,  label='TM-TE + TETE, gamma = pi/8, contrast = {:.2f}'.format(c))
    
    ITMTE = interferenceIntensity(x,k,theta, gamma=np.pi/6, A=A, polarisationModes=('TM','TE'))
    I = ITETE+ITMTE
    c=gratingContrastRMS(I)
    plt.plot(I, label='TM-TE + TETE, gamma = pi/6, contrast = {:.2f}'.format(c))
    
    ITMTE = interferenceIntensity(x,k,theta, gamma=np.pi/4, A=A, polarisationModes=('TM','TE'))
    I = ITETE+ITMTE
    c=gratingContrastRMS(I)
    plt.plot(I, label='TM-TE + TETE, gamma = pi/4, contrast = {:.2f}'.format(c))
    plt.legend()
    plt.show()
    
    

def test():
    
    ''' load a saved intensity profile. We will use some properties of this profile
    for simulations. '''
    import tifffile 
    
    mid1 = 65
    mid2= 143    
    N = 100
    
    m1 = 16377 #15919
    m2 = 21159
    
    n = 1
    
    # profile = np.load('profile01.npy')
    Ipath = '/user/home/opt/xl/xl/experiments/maskRoughness/data/' #beamCoherence2_op/data/' #'/home/jerome/dev/data/aerialImages/'

    files = ['beamCoherence2/data/fullRes_4000e/fullRes_4000eintensity.tif', 'beamCoherence2/data/fullRes_5000e/fullRes_5000eintensity.tif']
    
    ran = range(1,14)
    #['fullRes_100eintensity.tif', 'fullRes_2000eintensity.tif', 'fullRes_3000eintensity.tif', 'fullRes_4000eintensity.tif', 'fullRes_5000eintensity.tif', 'fullRes_10000eintensity.tif']
    #['5000e_p24TMintensity.tif'] 
    #['fullRes_100eintensity.tif', 'fullRes_2000eintensity.tif', 'fullRes_3000eintensity.tif', 'fullRes_4000eintensity.tif', 'fullRes_5000eintensity.tif', 'fullRes_10000eintensity.tif']

#    files1 = ['fullRes_1000eintensity.tif', 'fullRes_1000e_TM.tif']
    
    #['5000e_p24TEintensity.tif']
    #['fullRes_1000eintensity.tif', 'fullRes_1000e_TM.tif']
    # I_1000 = tifffile.imread(Ipath + files1[0])
    # I_1000TM = tifffile.imread(Ipath + files1[1])
    # I_5000 = tifffile.imread(Ipath + files2[0])
    # I_100 = tifffile.imread(Ipath + files2[1])
    res1 = 1.9651759267701173e-09
    res2 = (3.924772866734718e-05 + 4.546782781154186e-05)/39424
    
    resV = 1.8194278317912603e-9
    midV = 112
    mV = 13477
    
    filesV = [str(r) + '/' + str(r) + 'intensity.tif' for r in ran]
#    ['beamCoherence2_op/data/4000e/4000eintensity.tif', 'maskRoughness/data/1/1intensity.tif', 'maskRoughness/data/2/2intensity.tif', 'maskRoughness/data/3/3intensity.tif']#, 'maskRoughness/data/4/4intensity.tif']
    # ['maskRoughness/data/1/1intensity.tif', 'maskRoughness/data/2/2intensity.tif'] 
#    ['beamCoherence2_op/data/4000e/4000eintensity.tif', 'maskRoughness/data/1/1intensity.tif', 'maskRoughness/data/2/2intensity.tif', 'maskRoughness/data/3/3intensity.tif']#, 'maskRoughness/data/4/4intensity.tif']

    pickledFiles = ['maskRoughness/data/1/10.pkl', 'maskRoughness/data/2/20.pkl', 'maskRoughness/data/3/30.pkl', 'maskRoughness/data/4/40.pkl', ]
    
    V = round((res1*N)/resV)
    RV = resV*V
    
    R1 = res1*N
    M = round((res1*N)/res2)
    R2 = res2*M
    print("Range 1: {} m".format(R1))
    print("Range 2: {} m".format(R2))
    print("Range V: {} m".format(RV))
    print("M: {}".format(M))
    print("V: {}".format(V))
    
    print(filesV)
    tiffs = [tifffile.imread(Ipath + f) for f in files] # read tiff files
#    tiffs1 = [tifffile.imread(Ipath + f) for f in files1]
    tiffsV = [tifffile.imread(Ipath + f) for f in filesV]
    
    plt.imshow(tiffsV[0], aspect='auto')
    plt.show()
    print("shape of tiffsV: ", np.shape(tiffsV[0]))
    
    Iprofiles = [t[mid1-n:mid1+n,:].mean(0) for t in tiffs] # take averaged line profile through interference fringes
#    Iprofiles1 = [t[mid2-n:mid2+n,:].mean(0) for t in tiffs1]
    IprofilesV = [t[:,midV-n:midV+n].mean(1) for t in tiffsV]
    print("Shape of Iprofile: {}".format(np.shape(IprofilesV[0])))
    
    plt.plot([i for i in IprofilesV])
    plt.plot(IprofilesV[0])   
    plt.title("profiles")
    plt.show()
    
#    aerialImages = [i[m1-N:m1+N] for i in Iprofiles] # take centre of line profile
#    aerialImages1 = [i[m2-M:m2+M] for i in Iprofiles1]
    aerialImagesV = [i[mV-V:mV+V] for i in IprofilesV]
    print("Shape of AerialImages: {}".format(np.shape(aerialImagesV[0])))
    
#    plt.plot([a for a in aerialImagesV])
    plt.plot(aerialImagesV[0])
#    plt.plot(aerialImagesV[4])
    plt.title("aerial Images")
    plt.show()
    
    labelsV = ['RMS:5nm, cLen:1nm', 
               'RMS:45nm, cLen:25nm', 
               'RMS:45nm, cLen:1nm', 
               'RMS:5nm, cLen:25nm',
               'RMS:15nm, cLen:1nm', 
               'RMS:35nm, cLen:25nm', 
               'RMS:45nm, cLen:5nm', 
               'RMS:5nm, cLen:15nm',
               'RMS:25nm, cLen:1nm', 
               'RMS:25nm, cLen:25nm', 
               'RMS:45nm, cLen:10nm', 
               'RMS:5nm, cLen:10nm',
               'RMS:35nm, cLen:1nm',
               ]
    # ['RMS:5nm, cLen:1nm', 'RMS:45nm, cLen:25nm']
    #['ideal mask', 'RMS:5nm, cLen:1nm', 'RMS:45nm, cLen:25nm', 'RMS:45nm, cLen:1nm']#, 'RMS:5nm, cLen:25nm']
    labels = ['4000e-hor', '5000e-hor'] #['100e', '2000e', '3000e', '4000e', '5000e', '10000e']
    #['TM']
    #['100e', '2000e', '3000e', '4000e', '5000e', '10000e']
    labels1 = ['1000e', '1000e - TM']
    #['TE'] 
    #['1000e', '1000e - TM']
    
    # I1000 = I_1000[mid2-n:mid2+n,:].mean(0)
    # I1000TM = I_1000TM[mid2-n:mid2+n,:].mean(0)
    # I5000 = I_5000[mid1-n:mid1+n,:].mean(0)
    # I100 = I_100[mid1-n:mid1+n,:].mean(0)
    
    # profile = I5000[m1-N:m1+N]# I5000[m1-N:m1+N] #I1000TM[m2-N:m2+N]
    # profile2 = I100[m1-N:m1+N] #I1000[m2-N:m2+N]
    
#    profileN = np.size(aerialImages[0])
#    profileXs = 1.9651759267701173e-09 #1.9651759267701173e-09 #1.0e-8 # pixel scaling factor/
#    profileX = np.linspace(-0.5*profileN*profileXs, 0.5*profileN*profileXs,profileN)
    
    #-4.546782781154186e-05 #Initial Horizontal Position [m]
    #3.924772866734718e-05 #Final Horizontal Position [m]
    #39424 #Number of points vs Horizontal Position
    
#    profileN1 = np.size(aerialImages1[0])
#    profileX1s = (3.924772866734718e-05 + 4.546782781154186e-05)/39424
#    profileX1 = np.linspace(-0.5*profileN1*profileX1s, 0.5*profileN1*profileX1s,profileN1)
    
    profileV = np.size(aerialImagesV[0])
    profileVs = resV
    profileV1 = np.linspace(-0.5*profileV*profileVs, 0.5*profileV*profileVs,profileV)
    
    # print(profileX1s)
    
    ''' define interference grating parameters'''
    wl = 6.710553853647976e-9 # wavelength in m

    # Amplitude of both beams (assumed equal)
    A = 0.25e5 # 0.37e5 #0.3e5  # this may be scaled to  match simulated intensity
    
    k = 2*np.pi/wl
    
    m = 1 # order of diffracted beams from each grating
    d = 100e-9 #24e-9 #100e-9 # grating spacing
    
    # angle between the beams from each grating
    theta = np.arcsin( m *wl/d)
    
    #define x positions:
#    xstep=profileXs
#    n = profileN
#    x =  np.linspace(-xstep*int(n/2),xstep*int(n/2),n)  #np.linspace(-90e-9,90e-9,10000)
#    x1 =  np.linspace(-profileX1s*int(profileN1/2),profileX1s*int(profileN1/2),profileN1) 
    xV =  np.linspace(-profileVs*int(profileV/2),profileVs*int(profileV/2),profileV) 
    
    # noise parameters
#    rho=4*1/xstep
    ''' generate interference intensity'''
#    I = interferenceIntensity(x,k,theta,A=A)
#    I1 = interferenceIntensity(x1,k,theta,A=A)
    IV = interferenceIntensity(xV,k,theta,A=A)
    
    # ''' generate noise '''
    # sr = n  # (as period = n/sr)
    # noise = whiteNoise(rho, sr, n, mu=0)
    # # Inoisy = I + noise
    
    ''' convolve intensity with gaussian '''
    sigma =1.5 #2.7
    IV = gaussian_filter(IV, sigma=sigma)
    
    
#    plt.plot(profileX,aerialImages[0])
    # plt.plot(profileX1,aerialImages1[0])
    plt.plot(profileV1,aerialImagesV[0])
    plt.show()

    ''' plot intensity with and without noise, together with saved profile'''
    # plt.plot(x*1e6,Inoisy,label='Model amplitude + noise')
    plt.figure(figsize=(12,8))
#    plt.plot(xV*1e6,IV, label='Model amplitude')
#    for i, a in enumerate(aerialImages): #[1::]
#         print("Shape of profile: {}".format(np.shape(a)))
#         print("Plotting profile number {}".format(i+1))
#         plt.plot(profileX*1e6, a, label=labels[i])
    # for i, b in enumerate(aerialImages1):
    #     plt.plot(profileX1*1e6, b, label=labels1[i])
    for i, b in enumerate(aerialImagesV): #[0:len(aerialImagesV)+2]
        plt.plot(profileV1*1e6, b, ':o', label=labelsV[i])
    # plt.plot(profileX*1e6, profile,label='Simulated profile 1')
    # plt.plot(profileX*1e6, profile2,label='Simulated profile 2')
    plt.xlabel('Position [um]')
    plt.ylabel('Intensity [a.u.]')
    plt.ylim(bottom=0)#, top=0.5e9)
    plt.legend()
    plt.rcParams["figure.figsize"] = [7,4]
    plt.show()
    
    ''' plot intensity with and without noise, together with saved profile'''
    plt.figure(figsize=(12,8))
#    plt.plot(xV*1e6,IV, label='Model amplitude')
    for i, b in enumerate(aerialImagesV): #[0:len(aerialImagesV)+2]
        plt.plot(profileV1*1e6, b, label=labelsV[i])
    plt.xlabel('Position [um]')
    plt.ylabel('Intensity [a.u.]')
    plt.ylim(bottom=0)#, top=0.5e9)
    plt.legend()
    plt.rcParams["figure.figsize"] = [7,4]
    plt.show()

    # f=[]      # initialise frequency list
    # psd=[]    # initialise PSD list
    # MSD = []  # initialise mean spectral density list
    # signals = I + aerialImages #[I, profile, profile2] # [I,Inoisy, profile] # ['Model TM-TM', 'Simulated', 'Simulated TM-TM'] #['Model TM-TM','Model + noise', 'Simulated']
    # for s in signals:
    #     F, PSD = periodogram(s,sr)
    #     f.append(F)
    #     psd.append(PSD)
     
    from itertools import cycle
    cycol = cycle('bgrcmk')
    
    from scipy.signal import argrelextrema
    
    # ''' plot frequency spectrum '''
    # for signal,label in zip(signals,labels): 
    #     fs = 1/xstep   # number of samples per m    
    #     sfft =  fft(signal)
    #     freqs = fftfreq(len(signal)) * fs
    #     #plt.stem(freqs, np.abs(sfft),linefmt=next(cycol),label=label)
    #     plt.plot(freqs, np.abs(sfft))#,linefmt=next(cycol),label=label)

        
    #     s = np.abs(sfft)[len(sfft)//2+1:]
    #     f = freqs[len(sfft)//2+1:]
    #     m = argrelextrema(np.abs(s), np.greater, order=4) #array of indexes of the  maxima


    #     y = [s[i-1] for i in m]
    #     x = [f[i-1] for i in m]
    #     plt.plot(x, y, 'x')
        
    #     #print('length y ', np.shape(y), ' length m ', np.shape(m))
    #     index_max = np.argmax(y)
        
    #     #print('index_max ', index_max)
    #     #print(m)
    #     #print(y)
        
    #     #print('m: ', m[0])
    #     #print(m[0][index_max])
        
        
    #     ymax = s[m[0][index_max]]
    #     xmax = f[m[0][index_max]]
        
    #     #print('ymax ', ymax)
    #     plt.plot(xmax, ymax, 'o')
        
    #     R = ymax/(np.sum(s)-ymax)
    #     print('R: ', R)
        
    
    # plt.xlabel('Spatial Frequency [1/m]')
    # plt.ylabel('Frequency Domain (Spectrum) Magnitude')
    # plt.legend()
    # #plt.xlim(-1.2e7, 0.1e7)
    # plt.xlim(-fs / 2, fs / 2)
    # plt.show()
    
#    aerialImages.insert(0,aerialImagesV[2])
#    aerialImages.insert(0,aerialImagesV[1])
#    aerialImages.insert(0,aerialImagesV[0])
#    labels.insert(0,labelsV)
#    aerialImages = aerialImagesV 
    labels = labelsV# + labels
    print(labels)
        
#    RMS5nm = 0,3,7,11
#    RMS15nm = 4
#    RMS25nm = 8,9
#    RMS35nm = 5, 12
#    RMS45nm = 1,2,6,10
#    
#    c1nm = 0,2,4,8,12
#    c5nm = 6
#    c10nm = 10,11
#    c15nm = 7
#    c25nm = 1,3,5,9
    
    aerialImagesC1nm = aerialImagesV[0], aerialImagesV[4], aerialImagesV[8], aerialImagesV[12], aerialImagesV[2] 
    labelsC1nm = ['5', '15', '25', '35', '45']
    
    aerialImagesRMS5nm = aerialImagesV[0],aerialImagesV[11],aerialImagesV[7],aerialImagesV[3] 
    labelsRMS5nm = ['1', '10', '15', '25']  
    
    aerialImagesRMS45nm =aerialImagesV[2],aerialImagesV[6],aerialImagesV[10],aerialImagesV[1] 
    labelsRMS45nm = ['1', '5', '10', '25']
    
    aerialImagesV = aerialImagesRMS45nm
    labels = labelsRMS45nm
    
#    filesV = filesV[0], filesV[11], filesV[7], filesV[3], filesV[4], filesV[8], filesV[9], filesV[12], filesV[5], filesV[2], filesV[6], filesV[10], filesV[1]
#    filesVcor = filesV[0], filesV[4], filesV[8], filesV[12], filesV[2], filesV[6], filesV[11], filesV[10], filesV[7], filesV[3], filesV[9], filesV[5], filesV[1]

     # Working contrast metrics
    michelsonC = [gratingContrastMichelson(a) for a in aerialImagesV]
#     michelsonC2 = [gratingContrastMichelson(b) for b in aerialImages1]
    rmsC = [gratingContrastRMS(a) for a in aerialImagesV]
#     rmsC2 =  [gratingContrastRMS(b) for b in aerialImages1]
    compositeC = [meanDynamicRange(a) for a in aerialImagesV] #, mdrC, imbalanceC 
#     compositeC2 = [meanDynamicRange(b) for b in aerialImages1]
    nils1 = [NILS(a,profileV1, d/4, show=False) for a in aerialImagesV] 
#     nils2 = [NILS(b,profileX1*1e6, d/2, show=False) for b in aerialImages1] 
    fourierC = [gratingContrastFourier(a,profileV1*1e6, show=False) for a in aerialImagesV] #Cf,  Am, Fr, peakFr - Still unsure but seems good
#     fourierC1 = [gratingContrastFourier(b,profileX*1e6, show=False) for b in aerialImages1]
    
    
    fidel = [fidelity(a,IV) for a in aerialImagesV]   # fidelity based on comparison to model
    # fidel1 = [fidelity(b,I1) for b in aerialImages1]
    
    michelsonC5 = [gratingContrastMichelson(a) for a in aerialImagesRMS5nm]
    rmsC5 = [gratingContrastRMS(a) for a in aerialImagesRMS5nm]
    compositeC5 = [meanDynamicRange(a) for a in aerialImagesRMS5nm] #, mdrC, imbalanceC 
    nils15 = [NILS(a,profileV1, d/4, show=False) for a in aerialImagesRMS5nm] 
    fourierC5 = [gratingContrastFourier(a,profileV1*1e6, show=False) for a in aerialImagesRMS5nm] #Cf,  Am, Fr, peakFr - Still unsure but seems good
    fidel5 = [fidelity(a,IV) for a in aerialImagesRMS5nm] 
    
    # # Testing contrast metrics
    # fourierC = [gratingContrastFourier(a,profileX*1e6, show=True) for a in aerialImages] #Cf,  Am, Fr, peakFr
    # fourierC1 = [gratingContrastFourier(b,profileX*1e6, show=True) for b in aerialImages1]
    
    print("shape of RMS contrast: {}".format(np.shape(rmsC)))
    # print(michelsonC1[0])
    # print(michelsonC2)
    # print(michelsonC1[1::])
    
#    michelsonC.insert(1,michelsonC2[0])
#    michelsonC.insert(1,michelsonC2[1])
#    rmsC.insert(1,rmsC2[0])
#    rmsC.insert(1,rmsC2[1])
#    compositeC.insert(1,compositeC2[0])
#    compositeC.insert(1,compositeC2[1])
#    labels.insert(1,labels1[0])
#    labels.insert(1,labels1[1])
#    nils1.insert(1,nils2[0])
#    nils1.insert(1,nils2[1])
#    fourierC.insert(1,fourierC1[0])
#    fourierC.insert(1,fourierC1[1])
#    fidel.insert(1,fidel1[0])
#    fidel.insert(1,fidel1[1])
    
    # mc = np.concatenate(michelsonC1[0],michelsonC2) #,michelsonC1[1::]) #list(michelsonC1)[0] + list(michelsonC2)
    
    
    # print(mc)
    # print(np.concatenate(mc,michelsonC1[1::]))
    # print(michelsonC1[0] + michelsonC2 + list(michelsonC1[1::]))
    
    # michelsonC = michelsonC1[0] + michelsonC2 + michelsonC1[1::]
    # rmsC = rmsC1[0] + rmsC2 + rmsC1[1::]
    # compositeC = compositeC1[0] + compositeC2 + compositeC1[1::]
    # labels2 = labels[0] + labels1 + labels[1::]
    
    # print("Shape of compositeC: {}".format(np.shape(compositeC[0])))
    # print(compositeC)
    
    # ## GET CONTRAST THROUGH DIFFERENT METHODS
    # michelson1 = gratingContrastMichelson(profile)
    # michelson2 = gratingContrastMichelson(profile2)
    # rmscon1 = gratingContrastRMS(profile)
    # rmscon2 = gratingContrastRMS(profile2)
    # # fourier1 = gratingContrastFourier(profile,profileX*1e6)
    # # fourier2 = gratingContrastFourier(profile2,profileX*1e6)
    # composite1, mdr1, imbalance1 = meanDynamicRange(profile)
    # composite2, mdr2, imbalance2 = meanDynamicRange(profile2)
    # # nils1 = NILS(profile,profileX*1e6,50e-9)
    # # nils2 = NILS(profile2,profileX*1e6,50e-9)
    # labels2 = labels + labels1

    
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    
    ax1.plot(labels, michelsonC, label='Michelson')
    ax1.plot(labels, rmsC, label='RMS')
    ax1.plot(labels, [c[0] for c in compositeC], label='Composite')
    # ax1.plot(labels, [c[1] for c in compositeC], label='MDR')
    # ax1.plot(labels, [c[2] for c in compositeC], label='Imbalance')
    ax1.plot(labels, [f[0] for f in fourierC], label='Fourier')
#    ax1.plot(labels, [n/6 for n in nils1], label='NILS')
    ax2.plot(labels, [n[0] for n in nils1], ':', label='NILS - mean')
    ax2.plot(labels, [n[4] for n in nils1], ':', label='NILS - rms')
#    ax1.plot(labels, fidel, ':', label='Fidelity')
    ax1.legend()
    ax2.legend()
    # ax2.set_ylabel("Fidelity")
    ax2.set_ylabel("NILS")
    ax1.set_ylabel("Aerial Image Contrast")
    ax1.set_xlabel("Trial")
    plt.show()
    
    fig, axs = plt.subplots(2,3)
    
    axs[0,0].plot(labels, michelsonC)
    axs[0,0].set_title("Michelson")
    axs[0,1].plot(labels, rmsC)
    axs[0,1].set_title("RMS")
    axs[0,2].plot(labels, [c[0] for c in compositeC])
    axs[0,2].set_title("Composite")
    axs[1,0].plot(labels, [f[0] for f in  fourierC])
    axs[1,0].set_title("Fourier")
    axs[1,1].plot(labels, [n[0] for n in nils1])
    axs[1,1].set_title("NILS")
    axs[1,2].plot(labels, fidel)
    axs[1,2].set_title("Fidelity")
    plt.show()
    
    
    # print(" ")
    # print("profile #1 ---------")
    # print("Michelson Contrast:              {}".format(michelson1))
    # print("RMS Contrast:                    {}".format(rmscon1))
    # # print("Fourier Contrast:                {}".format(fourier1))
    # print("Composite Contrast:              {}".format(composite1))
    # print("Imbalance Contrast:              {}".format(imbalance1))
    # print("MDR Contrast:                    {}".format(mdr1))
    # # print("NILS:                            {}".format(nils1))
    # print(" ")
    # print("profile #2 ---------")
    # print("Michelson Contrast:              {}".format(michelson2))
    # print("RMS Contrast:                    {}".format(rmscon2))
    # # print("Fourier Contrast:                {}".format(fourier2))
    # print("Composite Contrast:              {}".format(composite2))
    # print("Imbalance Contrast:              {}".format(imbalance2))
    # print("MDR Contrast:                    {}".format(mdr2))
    # # print("NILS:                            {}".format(nils2))
    
        
 
   

#    m = argrelextrema(np.abs(sfft), np.greater) #array of indexes of the  maxima
#    y = [freqs[i] for i in m]
#    plt.plot(m, y, 'rs')
#    plt.show()
#        
#        
    
    
    
        
    # ''' plot PSD '''    
    # cutoffIndex=1 #?????????
    # for _psd, _f, _label in zip(psd,f,labels):
    #     #plt.semilogy(_f[1:], np.sqrt(_psd[1:]),label=_label)
    #     plt.semilogx(_f[1:], np.sqrt(_psd[1:]),label=_label,alpha=0.7)
    # plt.xlabel("Spatial Frequency (1/nm)")
    # plt.ylabel("PSD (arb.u./SQRT(nm))")
    # plt.axhline(rho, ls="dashed", color="r",label='rho')
    # plt.rcParams["figure.figsize"] = [4,2]
    # plt.legend()
    # plt.show()

    
    # histogramI=[]
    # histogramBins=[]
    # for _psd, signal,label in zip(psd, signals,labels): 
        
    #     IOD, IODM, H, binEdges, binCenters = integralOpticalDensity(signal)
    #     histogramI.append(H)
    #     histogramBins.append(binEdges)
    #     C, C1, C2 = meanDynamicRange(signal)
    #     # Cf,  Am, Fr, peakFr  = gratingContrastFourier(signal,x, show=False)
    #     Cm = gratingContrastMichelson(signal)
    #     fidel = fidelity(signal,signals[0])   # fidelity based on comparison to model
        

    #     print('**********',label,'***********')
    #     print('IOD: {}'.format(IOD))
    #     print('IOD max: {}'.format(IODM))
    #     print('Mean dynamic range (C): {}.  [C1 = {}, C2 = {}]'.format(C,C1,C2))
    #     # print("Mean spectral noise density = ",np.sqrt(np.mean(_psd[cutoffIndex:])), "arb.u/SQRT(1/nm)")
    #     print('Michelson contrast: {}'.format(Cm))
    #     # print ('Fourier contrast: {}'.format(Cf)) 
    #     # print ('Fundamental frequency: {}'.format(peakFr))
    #     # print('Period: {}- need to check)'.format(1/peakFr))
    #     print('Fidelity (1D): {}\n'.format(fidel))
        
       
    # ''' plot histogram '''
    # for h, e, label in zip(histogramI,histogramBins,labels):
    #     plt.bar(e,h,label=label)
    #     plt.ylabel('Frequency')
    #     plt.xlabel('Scaled Intensity')
    #     plt.legend()
    #     plt.show



def testx():
    
    ''' load a saved intensity profile. We will use some properties of this profile
    for simulations. '''
    
    profileFile = '/user/home/opt/xl/xl/experiments/beamPolarisation17ME/data/t0/profile.txt'
    XI = np.genfromtxt(profileFile, delimiter='\t')
    I = XI[:,1] 
    X = XI[:,0]
    
    res = 2.828781218482689e-10
    
    x =X*res
    print(X[0])
    print(X[1])
   
    # crop a subset for easier visualisation
    x=x[20000:25000]
    I=I[20000:25000]
    
    d = 65.e-9  # expected half-width of pattern, i.e width of line
   
    #plt.plot(x,I)
    
    nils = NILS(I,x, d/4, show=True) 


def testGaussFit():
    import tifffile 
    
    mid1 = 65
    mid2= 143    
    N = 400
    
    m1 = 16377 #15919
    m2 = 21159
    
    n = 10
    
    # profile = np.load('profile01.npy')
    Ipath = '/home/jerome/dev/data/aerialImages/'
    files = ['fullRes_10000eintensity.tif']
    
    tiffs = [tifffile.imread(Ipath + f) for f in files] # read tiff files
    Iprofiles = [t[mid1-n:mid1+n,:].mean(0) for t in tiffs] # take averaged line profile through interference fringes
    aerialImages = [i[m1-N:m1+N] for i in Iprofiles] # take centre of line profile

    profileN = np.size(aerialImages[0])
    profileXs = 1.9651759267701173e-09 #1.9651759267701173e-09 #1.0e-8 # pixel scaling factor/
    profileX = np.linspace(-0.5*profileN*profileXs, 0.5*profileN*profileXs,profileN)
    
    ''' define interference grating parameters'''
    wl = 6.710553853647976e-9 # wavelength in m
    
    # Amplitude of both beams (assumed equal)
    A = 0.3e5 # 0.37e5 #0.3e5  # this may be scaled to  match simulated intensity
    k = 2*np.pi/wl
    m = 1 # order of diffracted beams from each grating
    d = 100e-9 # grating spacing
    
    # angle between the beams from each grating
    theta = np.arcsin( m *wl/d)
    
    #define x positions:
    xstep=profileXs
    n = profileN
    x =  np.linspace(-xstep*int(n/2),xstep*int(n/2),n)
    
    ''' generate interference intensity'''
    I = interferenceIntensity(x,k,theta,A=A)
    
    # ''' convolve intensity with gaussian '''
    sigma = 3
    C = np.sqrt(sigma)
    print("1st order coherence length: {} m".format(C))
    _I1 = gaussian_filter(I, sigma=sigma)
    G = gauss1D(round(len(I)/4), sigma=sigma)
    plt.plot(G)
    plt.show()
    _I2 = np.convolve(I,G)
    
    plt.plot(_I1, label="I1")
    plt.plot(_I2[round(len(_I2)/2)-N:round(len(_I2)/2)+N], label="I2")
    plt.legend()
    plt.show()

    ''' plot intensity with and without noise, together with saved profile'''
    plt.plot(x*1e6,_I1, label='Model amplitude - function')
    plt.plot(x*1e6,_I2[round(len(I)/2)-N:round(len(I)/2)+N], label='Model amplitude - code')
    for i, a in enumerate(aerialImages):
        print("Shape of profile: {}".format(np.shape(a)))
        print("Plotting profile number {}".format(i+1))
        plt.plot(profileX*1e6, a, label="Simulated")
    plt.xlabel('Position [um]')
    plt.ylabel('Intensity [a.u.]')
    plt.ylim(bottom=0)
    plt.legend()
    plt.rcParams["figure.figsize"] = [7,4]
    plt.show()


def testTETMContrast():
    ''' define interference grating parameters'''
    wl = 6.710553853647976e-9 # wavelength in m
    
    save = False
    savePath = '/home/jerome/Documents/MASTERS/Figures/plots/testing/'
    
    # Amplitude of both beams (assumed equal)
    A = 1/2 # 0.37e5 #0.3e5  # this may be scaled to  match simulated intensity
    k = 2*np.pi/wl
    m = 1 # order of diffracted beams from each grating
    pitch = [round_sig(n,sig=5) for n in np.linspace(10e-9,100e-9,10000)]#24e-9 #24e-9 #100e-9 # grating spacing
#    print(pitch)
    
    # angle between the beams from each grating
    theta = [np.arcsin( m *wl/p) for p in pitch]
    
    #define x positions:
    xstep=0.5e-9
    n = 200000
    x = np.linspace(-xstep*int(n/2),xstep*int(n/2),n+1) #[round_sig(n,sig=5) for n in np.linspace(-xstep*int(n/2),xstep*int(n/2),n)]  #np.linspace(-90e-9,90e-9,10000)
    # print(x)
    
    # noise parameters
    rho=4*1/xstep
    ''' generate interference intensity'''
    I_TM = [interferenceIntensity(x,k,t,A=A, polarisationModes=('TM','TM')) for t in theta]
    I_TE = [interferenceIntensity(x,k,t,A=A, polarisationModes=('TE','TE')) for t in theta]
    
    # ''' generate noise '''
    # sr = n  # (as period = n/sr)
    # noise = whiteNoise(rho, sr, n, mu=0)
    # # Inoisy = I + noise
    
    ''' convolve intensity with gaussian '''
#    sigma = 1.5 #2.7
#    I = gaussian_filter(I, sigma=sigma)

    print(np.shape(I_TM))
#    plt.plot(I_TM[0])
    ''' plot intensity with and without noise, together with saved profile'''
    # plt.plot(x*1e6,Inoisy,label='Model amplitude + noise')
    fig, axs = plt.subplots(2,1)
    for p, ite, itm in zip(pitch, np.array(I_TE), np.array(I_TM)):
        axs[0].plot(x,itm)#, label='p=' + str(p))
        axs[1].plot(x,ite, label='$p_G$ = ' + str(np.round(1e9*p)) + 'nm')
    axs[0].set_ylabel('$I_{TM-TM}$   [a.u]')
    axs[1].set_ylabel('$I_{TE-TE}$   [a.u]')
    axs[1].set_xlabel('x-position [nm]')
    for ax in axs:
        # ax.set_xlim(np.min(x),np.max(x))
        # ax.set_xticks([int(a*len(x)) for a in [0, 1/4,1/2,3/4]]+ [len(x)-1])
        ax.set_xticklabels([round_sig(1e9*np.max(x)*a) for a in [-1,-4/5,-2/5,0,2/5,4/5]])
                                      #x[int(a*len(x))]) for a in [0,1/4,1/2,3/4]] + [round_sig(1e9*np.max(x))])
    # axs[0].legend(loc='lower center',title='TM-TM')
    axs[1].legend(loc='lower center', #title='Grating Pitch [nm]',
                  bbox_to_anchor=(0.5, -0.8),fancybox=True, shadow=True,ncol=5)
    # plt.legend()        
    if save:
        # plt.savefig(savePath + 'TE_TM_Intensity.pdf')
        plt.savefig(savePath + 'TE_TM_Intensity.png', dpi=2000)
    else:
        pass
    plt.show()
    
    michelsonC = [gratingContrastMichelson(a) for a in I_TM]
    rmsC = [gratingContrastRMS(a) for a in I_TM]
    compositeC = [meanDynamicRange(a, show=False) for a in I_TM] #, mdrC, imbalanceC 
    nils1 = [NILS(a,x, p/4, show=False) for a, p in zip(I_TM, pitch)] 
    fourierC = [gratingContrastFourier(a,x, show=False) for a in I_TM] #Cf,  Am, Fr, peakFr - Still unsure but seems good
#    fidel = [fidelity(a,b) for a, b in zip(I_TM, I_TE)]   # fidelity based on comparison to model

    michelsonCte = [gratingContrastMichelson(a) for a in I_TE]
    rmsCte = [gratingContrastRMS(a) for a in I_TE]
    compositeCte = [meanDynamicRange(a) for a in I_TE] #, mdrC, imbalanceC 
    nils1te = [NILS(a,x, p/4, show=False) for a, p in zip(I_TE, pitch)] 
    fourierCte = [gratingContrastFourier(a,x, show=False) for a in I_TE] #Cf,  Am, Fr, peakFr - Still unsure but seems good


    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    
    ax1.plot(pitch, michelsonC, label='Michelson')
    ax1.plot(pitch, rmsC, label='RMS')
    ax1.plot(pitch, [c[0] for c in compositeC], label='Composite')
    ax1.plot(pitch, [c[1] for c in compositeC], label='MDR')
    ax1.plot(pitch, [c[2] for c in compositeC], label='Imbalance')
    ax1.plot(pitch, [f[0] for f in fourierC], label='Fourier')
    ax2.plot(pitch, [n[0] for n in nils1], ':', label='mean NILS')
    ax2.plot(pitch, [n[4] for n in nils1], ':', label=' rms NILS')
#    ax1.plot(pitch, fidel, '--', label='Fidelity')
    ax1.legend(loc='lower center')
    ax2.legend()
    # ax2.set_ylabel("Fidelity")
    ax2.set_ylabel("NILS")
    ax1.set_ylabel("Aerial Image Contrast (TM-TM)")
    ax1.set_xlabel("Grating Pitch")
    ax1.set_xlabel("Grating Pitch [nm]")
    ax1.set_xticklabels([1e9*np.max(pitch)*a for a in [0,1/5,2/5,3/5,4/5,1]])
    if save:
        plt.savefig(savePath + 'TM_Contrast.pdf')
        plt.savefig(savePath + 'TM_Contrast.png', dpi=2000)
    else:
        pass
    plt.show()
    
    
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    
    ax1.plot(pitch, michelsonCte, label='Michelson')
    ax1.plot(pitch, rmsCte, label='RMS')
    ax1.plot(pitch, [c[0] for c in compositeCte], label='Composite')
    ax1.plot(pitch, [c[1] for c in compositeCte], label='MDR')
    ax1.plot(pitch, [c[2] for c in compositeCte], label='Imbalance')
    ax1.plot(pitch, [f[0] for f in fourierCte], label='Fourier')
    ax2.plot(pitch, [n[0] for n in nils1te], ':', label='mean NILS')
    ax2.plot(pitch, [n[4] for n in nils1te], ':', label=' rms NILS')
    ax1.legend(loc='lower center')
    ax2.legend()
    # ax2.set_ylabel("Fidelity")
    ax2.set_ylabel("NILS")
    ax1.set_ylabel("Aerial Image Contrast (TE-TE)")
    ax1.set_xlabel("Grating Pitch [nm]")
    ax1.set_xticklabels([1e9*np.max(pitch)*a for a in [0,1/5,2/5,3/5,4/5,1]])
    if save:
        plt.savefig(savePath + 'TE_Contrast.pdf')
        plt.savefig(savePath + 'TE_Contrast.png', dpi=2000)
    else:
        pass
    plt.show()
    
    
    fig, axs = plt.subplots(2,3)
    
    axs[0,0].plot(pitch, michelsonC, label='TM')
    axs[0,0].plot(pitch, michelsonCte, label='TE')
    axs[0,0].legend()
    axs[0,0].set_title("Michelson")
    axs[0,0].set_ylabel("Contrast")
    axs[0,1].plot(pitch, rmsC, label='TM')
    axs[0,1].plot(pitch, rmsCte, label='TE')
    axs[0,1].legend()
    axs[0,1].set_title("RMS")
    axs[0,2].plot(pitch, [c[0] for c in compositeC], label='TM')
    axs[0,2].plot(pitch, [c[0] for c in compositeCte], label='TE')
    axs[0,2].legend()
    axs[0,2].set_title("Composite")
    axs[1,0].plot(pitch, [f[0] for f in  fourierC], label='TM')
    axs[1,0].plot(pitch, [f[0] for f in  fourierCte], label='TE')
    axs[1,0].legend()
    axs[1,0].set_title("Fourier")
    axs[1,0].set_ylabel("Contrast")
    axs[1,0].set_xlabel("Grating Pitch")
    axs[1,1].plot(pitch, [n[0] for n in nils1], label='TM')
    axs[1,1].plot(pitch, [n[0] for n in nils1te], label='TE')
    axs[1,1].legend()
    axs[1,1].set_title("NILS")
    axs[1,1].set_xlabel("Grating Pitch")
    axs[1,2].plot(pitch, [c[2] for c in compositeC], label='TM')
    axs[1,2].plot(pitch, [c[2] for c in compositeCte], label='TE')
    axs[1,2].legend()
    axs[1,2].set_title("Imbalance")
    axs[1,2].set_xlabel("Grating Pitch")
    # for ax in axs[:,:]:
    axs[0,0].set_xticklabels([1e9*np.max(pitch)*a for a in [0,1/4,1/2,3/4,1]])
    axs[0,1].set_xticklabels([1e9*np.max(pitch)*a for a in [0,1/4,1/2,3/4,1]])
    axs[0,2].set_xticklabels([1e9*np.max(pitch)*a for a in [0,1/4,1/2,3/4,1]])
    axs[1,0].set_xticklabels([1e9*np.max(pitch)*a for a in [0,1/4,1/2,3/4,1]])
    axs[1,1].set_xticklabels([1e9*np.max(pitch)*a for a in [0,1/4,1/2,3/4,1]])
    axs[1,2].set_xticklabels([1e9*np.max(pitch)*a for a in [0,1/4,1/2,3/4,1]])
    fig.tight_layout()
    if save:
        plt.savefig(savePath + 'TETM_Contrast.pdf')
        plt.savefig(savePath + 'TETM_Contrast.png', dpi=2000)
    else:
        pass
    plt.show()

if __name__ == "__main__":

    test()
    # test_models()
    # testGaussFit()
#    testTETMContrast()