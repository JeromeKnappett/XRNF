#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
useful.py
=========
General utility functions for wavefield and optics calculations.

Merged from:
  - scripts/homecomp/useful.py
  - scripts/homecomp/local/clean/useful.py

Functions
---------
Maths:
    round_sig               -- round to significant figures

Array operations:
    getLineProfile          -- extract horizontal or vertical line profile
    sampleField             -- extract central sub-region of a 2D array

I/O:
    fromPickle              -- load object from pickle file

Geometry / optics:
    normVec                 -- normalise a 3D vector
    nFromAng                -- unit vector from angle
    getDeltaBeta            -- x-ray refractive index components (delta, beta)
    thicknessForPhaseShift  -- material thickness for a given phase shift

Tests:
    test                    -- basic vector normalisation test
"""

import numpy as np
from math import log10, floor, sqrt
import matplotlib.pyplot as plt
import matplotlib.patches as patches


# =============================================================================
# Maths
# =============================================================================

def round_sig(x, sig=2):
    """
    Round x to a given number of significant figures.

    Parameters
    ----------
    x : float
    sig : int, optional
        Number of significant figures. Default 2.

    Returns
    -------
    float
    """
    if x != 0:
        return round(x, sig - int(floor(log10(abs(x)))) - 1)
    else:
        return x


# =============================================================================
# Array operations
# =============================================================================

def getLineProfile(a, axis=0, mid=None, show=False):
    """
    Extract a line profile through the centre of a 2D array.

    Parameters
    ----------
    a : ndarray, shape (ny, nx)
        Input 2D array.
    axis : {0, 1}, optional
        0 = vertical profile (along y at centre x),
        1 = horizontal profile (along x at centre y). Default 0.
    mid : tuple of int or None, optional
        (row, col) of the profile centre. If None, uses array centre.
    show : bool, optional
        Plot the profile. Default False.

    Returns
    -------
    ndarray
        1D line profile.
    """
    nx, ny = np.shape(a)[1], np.shape(a)[0]
    if mid is None:
        midX, midY = int(nx / 2), int(ny / 2)
    else:
        midX, midY = int(mid[1]), int(mid[0])

    if axis == 0:
        p = a[:, midX]
        title = 'vertical profile'
    elif axis == 1:
        p = a[midY, :]
        title = 'horizontal profile'

    if show:
        plt.plot(p)
        plt.title(title)
        plt.show()

    return p


def sampleField(A, Fx, Fy, limit=75, verbose=False, show=False):
    """
    Extract a central sub-region from a 2D (or 3D) array.

    Parameters
    ----------
    A : ndarray
        Input array, shape (ny, nx) or (ny, nx, nc).
    Fx : float
        Fraction of array width to sample (0 < Fx <= 1).
    Fy : float
        Fraction of array height to sample (0 < Fy <= 1).
    limit : int, optional
        Maximum allowed pixels in any sampled dimension. Default 75.
    verbose : bool, optional
        Print sampling details. Default False.
    show : bool, optional
        Display the array with the sampled region overlaid. Default False.

    Returns
    -------
    ndarray
        Sampled sub-array.
    """
    if verbose:
        print("-----Sampling middle part of array-----")

    Ax = np.shape(A)[1]
    Ay = np.shape(A)[0]
    Sx = Fx * (Ax - 1)   # Ax-1 for correct even-array centring
    Sy = Fy * (Ay - 1)

    if Sx > limit or Sy > limit:
        print("Error: Sampled area is too large. Reduce Fx/Fy.")
        import sys
        sys.exit()

    try:
        _x1 = int(np.max(np.shape(A[:, 0, 0])))
        _y1 = int(np.max(np.shape(A[0, :, 0])))
    except IndexError:
        _x1 = int(np.max(np.shape(A[:, 0])))
        _y1 = int(np.max(np.shape(A[0, :])))

    midX = int((Ax - 1) / 2)
    midY = int((Ay - 1) / 2)

    ROI = (
        (int(midX - Sx / 2), int(midY - Sy / 2)),
        (int(midX + Sx / 2), int(midY + Sy / 2)),
    )

    x0, y0 = ROI[0][0], ROI[0][1]
    x1, y1 = ROI[1][0], ROI[1][1]
    lX = x1 - x0
    lY = y1 - y0

    if verbose:
        print("Original size [pixels]:          {}".format((Ax, Ay)))
        print("Sampled area size (pixels):      {}".format([Sx, Sy]))
        print("Nx (pixels):                     {}".format(_x1))
        print("Ny (pixels):                     {}".format(_y1))
        print("Mid x:                           {}".format(midX))
        print("Mid y:                           {}".format(midY))
        print("Region of interest (pixels):     {}".format(ROI))
        print("Start of sample area (x,y):      {}".format((x0, y0)))
        print("Size of sample area (x,y):       {}".format((lX, lY)))

    if show:
        I = abs(A.conjugate() * A)
        figure, ax = plt.subplots(1)
        rect = patches.Rectangle((x0, y0), lX, lY, edgecolor='r', facecolor='none')
        plt.imshow(I, aspect='auto')
        ax.add_patch(rect)
        plt.title("Original Wavefield with Sampled Area")
        plt.show()
        plt.clf()
        plt.close()

    return A[y0:y1, x0:x1]


# =============================================================================
# I/O
# =============================================================================

def fromPickle(path):
    """
    Load an object from a pickle file.

    Parameters
    ----------
    path : str
        Path to the pickle file.

    Returns
    -------
    object
        Unpickled object.
    """
    import pickle
    with open(path, 'rb') as f:
        return pickle.load(f)


# =============================================================================
# Geometry / optics
# =============================================================================

def normVec(x, y, z):
    """
    Normalise a 3D vector.

    Parameters
    ----------
    x, y, z : float or ndarray
        Vector components.

    Returns
    -------
    nx, ny, nz : float or ndarray
        Unit vector components.
    """
    N = np.sqrt(x**2 + y**2 + z**2)
    return x / N, y / N, z / N


def nFromAng(theta):
    """
    Compute a unit vector in the xz-plane from an angle from the z-axis.

    Parameters
    ----------
    theta : float
        Angle from z-axis [rad].

    Returns
    -------
    nx, ny, nz : float
        Unit vector components.
    """
    y = 0
    z = 1
    x = z * np.tan(theta)
    return normVec(x, y, z)


def getDeltaBeta(material, energy, density=None):
    """
    Return x-ray refractive index components for a material.

    Requires the ``xraydb`` package.

    Parameters
    ----------
    material : str
        Chemical formula (e.g. 'Ni', 'Ni3Al', 'SiO2').
    energy : float
        X-ray photon energy [eV].
    density : float or None, optional
        Material density [g/cm^3]. If None, uses tabulated atomic density
        (only valid for pure elements).

    Returns
    -------
    delta : float
        Refractive index decrement.
    beta : float
        Absorption index.
    atlen : float
        Attenuation length [m].
    """
    import xraydb
    if density is None:
        density = xraydb.atomic_density(material)
    delta, beta, atlen = xraydb.xray_delta_beta(material, density, energy)
    return delta, beta, atlen * 1e-2  # convert cm to m


def thicknessForPhaseShift(wl, ps, delta):
    """
    Calculate material thickness required for a given x-ray phase shift.

    Parameters
    ----------
    wl : float
        Wavelength [m].
    ps : float
        Desired phase shift [rad].
    delta : float
        Refractive index decrement of the material.

    Returns
    -------
    float
        Required thickness [m].
    """
    return (wl * ps) / (delta * np.pi)


# =============================================================================
# Tests
# =============================================================================

def test():
    """Basic vector normalisation test."""
    x = 100e-6
    y = 0
    z = 10.888e-3
    theta = np.arctan(x / z)

    nx, ny, nz = normVec(x, y, z)
    print("normVec:  ", nx, ny, nz)
    nx, ny, nz = nFromAng(theta)
    print("nFromAng: ", nx, ny, nz)


if __name__ == '__main__':
    m = 'Ni'
    density = None
    e = 186
    wl = 6.7e-9
    ps = 2 * np.pi * 0.01
    d, b, a = getDeltaBeta(m, energy=e, density=density)
    print(f'delta = {d},  beta = {b},  atten len = {a} m')
    t = thicknessForPhaseShift(wl=wl, ps=ps, delta=d)
    print(f'Thickness for 1% phase shift: {t * 1e9:.2f} nm')
