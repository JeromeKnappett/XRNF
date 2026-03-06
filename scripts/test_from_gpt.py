#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 18 11:54:44 2025

@author: jerome
"""

"""
Merged Script Example

This script combines:
  - TIFF-based field loading from the first script
  - 2D Gaussian beam generation from the second script
  - Summation with E1, E2 in 1D for an aerial image plot.

Make sure you have 'tifffile' installed:
   pip install tifffile

And that your TIFF files exist at the specified paths.
"""

import numpy as np
import matplotlib.pyplot as plt
import tifffile

###############################################################################
# 1) Utility Functions (from first script)
###############################################################################

def diffractionAngle(wl, p, phi=0, m=1):
    """
    Use the grating equation to determine diffraction angle:
      sin(theta_out) = sin(phi) + m*(wl/p)
    """
    return np.arcsin(np.sin(phi) + m * wl / p)

def EfromTiffs(files, mid=None, N=1000, n=1):
    """
    Given a list of file "stems" [e.g. "apertureDiffraction", "blockDiffraction", ...],
    load the ExReal, EyReal, ExIm, EyIm TIFs for each stem, then combine them
    into a complex field cE = E_x + E_y. Each element cE[i] will be a 2D numpy array.

    Args:
      files (List[str]): base file paths (no extension), e.g. ["apertureDiffraction", "blockDiffraction"]
      mid (List[(int,int)] or None): list of centers (row,col). If None, the center is chosen as half the array shape.
      N (int): half-width in the horizontal dimension to extract
      n (int): half-width in the vertical dimension to extract

    Returns:
      cE (List[2D complex arrays]): A list of 2D complex fields
    """
    if mid is None:
        # We'll need to read the TIFF to get shape first, but let's just do a quick approach:
        # If you already know the shape, define mid explicitly or do a 2-pass read.
        # Here, we do a quick 2-pass approach.
        mid = []
        for f in files:
            # For shape, we can peek at one of the TIFs, e.g. "ExReal"
            exr_path = f + "ExReal.tif"
            temp_img = tifffile.imread(exr_path)
            rmid = temp_img.shape[0]//2
            cmid = temp_img.shape[1]//2
            mid.append((rmid, cmid))

    # Load all TIFs
    EhR = [tifffile.imread(f + "ExReal.tif") for f in files]
    EhI = [tifffile.imread(f + "ExIm.tif")  for f in files]
    EvR = [tifffile.imread(f + "EyReal.tif") for f in files]
    EvI = [tifffile.imread(f + "EyIm.tif")  for f in files]

    # Extract subarrays around 'mid' (vertical: n, horizontal: N)
    imagesEhR = [img[m[0]-n:m[0]+n, m[1]-N:m[1]+N] for img,m in zip(EhR, mid)]
    imagesEhI = [img[m[0]-n:m[0]+n, m[1]-N:m[1]+N] for img,m in zip(EhI, mid)]
    imagesEvR = [img[m[0]-n:m[0]+n, m[1]-N:m[1]+N] for img,m in zip(EvR, mid)]
    imagesEvI = [img[m[0]-n:m[0]+n, m[1]-N:m[1]+N] for img,m in zip(EvI, mid)]

    # Combine real + imaginary, Eh + Ev
    Eh = [ExR + 1j*ExI for ExR, ExI in zip(imagesEhR, imagesEhI)]
    Ev = [EyR + 1j*EyI for EyR, EyI in zip(imagesEvR, imagesEvI)]

    # cE is Eh + Ev
    cE = [eh + ev for eh, ev in zip(Eh, Ev)]
    return cE

###############################################################################
# 2) Gaussian Beam Generation (from second script)
###############################################################################

def gaussianBeam2D(x, y, w0, z, R, k, amplitude_factor, phase_offset=0.0):
    """
    Create a 2D Gaussian beam with a simple quadratic phase term.

    Args:
        x, y: 1D coordinate arrays
        w0: Beam waist
        z:  Propagation distance (used in phase)
        R:  Radius of curvature (used in quadratic phase)
        k:  Wave number (2*pi/wavelength)
        amplitude_factor: overall amplitude scaling
        phase_offset: additional global phase to add to beam

    Returns:
        E2D: Complex 2D field array of shape (len(y), len(x)).
    """
    xx, yy = np.meshgrid(x, y)
    # Gaussian envelope
    envelope = np.exp(- (xx**2 + yy**2) / w0**2)
    # Quadratic phase factor
    quad_phase = np.exp(
        -1j * k * (
            z + (xx**2 + yy**2)/(2.0 * R)
        )
    )
    E2D = amplitude_factor * envelope * quad_phase * np.exp(1j * phase_offset)
    return E2D

###############################################################################
# 3) Main test function: combine TIFF-based fields, a Gaussian beam, and E1/E2
###############################################################################

def testMerged():
    """
    1. Load tiff-based fields (e.g. from "apertureDiffraction", "blockDiffraction").
    2. Create a 2D Gaussian beam as the 'third beam' (optional or as an extra).
    3. Slice them to 1D.
    4. Add with E1, E2 fields and plot final intensity.
    """
    # ------------------
    # PART A: Load TIFF fields
    # ------------------
    path = "/home/jerome/dev/data/correctedBlockDiffraction/"
    files = ["apertureDiffraction", "blockDiffraction"]
    fileNames = [path + f for f in files]

    # Example: Let's define the center (mid) and extraction width (N, n)
    # Adjust these based on your actual TIFF sizes
    # If mid=None, the function does a naive center = shape//2
    mid = [(200, 10000), (100, 7000)]
    N   = 1000  # half-width horizontally
    n   = 1     # half-width vertically (we'll just get a single row band)

    # Load each file's complex field
    # cE is a list of 2D arrays: cE[0], cE[1]
    tiff_fields = EfromTiffs(fileNames, mid=mid, N=N, n=n)

    # tiff_fields[0] -> Aperture diffraction field, shape (2*n, 2*N)
    # tiff_fields[1] -> Block diffraction field, shape (2*n, 2*N)
    print("Loaded TIFF-based fields shapes:", [arr.shape for arr in tiff_fields])

    # Combine them into one field if you like, or keep separate
    # For demonstration, let's sum them: E_tiff_sum = cE[0] + cE[1]
    E_tiff_sum = tiff_fields[0] + tiff_fields[1]  # shape (2*n, 2*N)

    # We'll treat E_tiff_sum as a "2D" field. Since n=1, it's basically 2 rows x 2000 columns.

    # ------------------
    # PART B: 2D Gaussian beam
    # ------------------
    wl = 6.7e-9
    k  = 2*np.pi / wl
    w0 = 1.0e-3
    z  = 1.0e5
    R  = 10.0
    E3a = 0.02 * np.sqrt(2)  # example amplitude factor
    E3p = 0.0

    # For convenience, define x,y arrays that match your TIFF's dimension in meters
    # Suppose your TIFF covers 2*N columns, each pixel is "dx" wide.
    # You need to know the pixel size in your actual data.
    # Let's guess dx = 4.832e-9 (like from your example).
    dx = 4.832e-9
    Nx = 2*N
    # For vertical direction, n=1 => 2*n=2 rows, dy is maybe ~ 3.85e-7 or something.
    # In practice, you should check your TIFF's actual pixel dimension. We'll guess:
    dy = 3.853e-7
    Ny = 2*n

    xVals = np.linspace(-N*dx, N*dx, Nx)
    yVals = np.linspace(-n*dy, n*dy, Ny)

    # Build the Gaussian beam
    E_gauss_2D = gaussianBeam2D(
        xVals, yVals, w0=w0, z=z, R=R,
        k=k,
        amplitude_factor=E3a,
        phase_offset=E3p
    )
    print("E_gauss_2D shape:", E_gauss_2D.shape)

    # Combine Gaussian beam with TIFF-based fields
    # E_total_2D = E_tiff_sum + E_gauss_2D
    E_tiff_plus_gauss = E_tiff_sum + E_gauss_2D

    # ------------------
    # PART C: E1, E2 in 1D
    # ------------------
    # We'll define E1, E2 along the horizontal dimension xVals.
    # Because the TIFF data is 2D with shape (Ny, Nx), let's take the middle row to keep it 1D.
    mid_row_index = Ny // 2  # ~ 1 if n=1
    # Extract the 1D slice from TIFF + Gaussian
    E_tiff_gauss_1D = E_tiff_plus_gauss[mid_row_index, :]  # shape (Nx,)

    # Interference field E1, E2
    p     = 100.0e-9
    theta = diffractionAngle(wl, p, phi=0.0, m=1)
    wfreq = 1.0 / wl
    t     = 0.0

    # Example amplitude distribution
    E10 = 0.5
    E20 = 0.5
    E30 = 0.02
    ratio_sum = E10 + E20
    E1a = (E10 / ratio_sum) * (1 - E30)
    E2a = (E20 / ratio_sum) * (1 - E30)

    E1p = 0.0
    E2p = 0.0

    # Build 1D coordinate (same length as xVals)
    # xVals are in meters.
    # We'll define E1, E2 on that axis:
    E1 = E1a * np.exp(1j*k*xVals*np.sin(theta) - wfreq*t - E1p)
    E2 = E2a * np.exp(-1j*k*xVals*np.sin(theta) - wfreq*t - E2p)

    # Summation
    E_final_1D = E1 + E2 + E_tiff_gauss_1D
    I_final_1D = np.abs(E_final_1D**2)

    # ------------------
    # PART D: Plot the 1D result
    # ------------------
    plt.figure()
    plt.plot(xVals*1e9, I_final_1D, label="Total sum")
    plt.xlabel("x [nm]")
    plt.ylabel("Intensity [a.u.]")
    plt.title("Final 1D Intensity")
    plt.legend()
    plt.show()

    # Optionally, print intensities or contamination fraction:
    I1 = np.sum(np.abs(E1)**2)
    I2 = np.sum(np.abs(E2)**2)
    ItiffGauss = np.sum(np.abs(E_tiff_gauss_1D)**2)
    I_tot = I1 + I2 + ItiffGauss
    print("I1:", I1)
    print("I2:", I2)
    print("Itiff+gauss (1D slice):", ItiffGauss)
    print("Fraction from TIFF+Gauss: %.2f%%" % (100*ItiffGauss / I_tot))

###############################################################################
# Entry Point
###############################################################################
if __name__ == "__main__":
    testMerged()
