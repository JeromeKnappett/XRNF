#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 16 09:39:27 2022

@author: jerome
"""

import numpy as np
from math import log10, floor, sqrt
import matplotlib.pyplot as plt
import matplotlib.patches as patches


# %%
def round_sig(x, sig=2):
    if x != 0:
        return round(x, sig - int(floor(log10(abs(x)))) - 1)
    else:
        return x


# %%
def sampleField(A, Fx, Fy, Limit=75, verbose=False, show=False):
    """
    Parameters
    ----------
    A : 2D array
        Wavefield to be sampled.
    Fx : Fraction of array to be sampled in horizontal.
    Fy : Fraction of array to be sampled in vertical.
    Limit: Maximum number of pixels allowed in any dimension
    Returns
    -------
    B: 2D array sampled from centre of A.
    """
    if verbose:
        print("-----Sampling middle part of wavefield-----")
    else:
        pass

    Ax = np.shape(A)[0]
    Ay = np.shape(A)[1]
    Sx = Fx * Ax
    Sy = Fy * Ay

    if Sx > Limit or Sy > Limit:
        print(
            "Error: Sampled area of wavefront is too large. Change Fx/Fy to a smaller value"
        )
        import sys

        sys.exit()

    _x0 = 0  # These are in _pixel_ coordinates!!
    _y0 = 0

    try:
        _x1 = int(np.max(np.shape(A[:, 0, 0])))  # These are in _pixel_ coordinates!!
        _y1 = int(np.max(np.shape(A[0, :, 0])))
    except IndexError:
        _x1 = int(np.max(np.shape(A[:, 0])))  # These are in _pixel_ coordinates!!
        _y1 = int(np.max(np.shape(A[0, :])))

    numx = _x1 - _x0  # number of points for line profile
    numy = _y1 - _y0
    midX = int(numx / 2)
    midY = int(numy / 2)

    ROI = (
        (int(midX - ((Fx) * midX)), int(midY - ((Fy) * midY))),
        (int(midX + ((Fx) * midX)), int(midY + ((Fy) * midY))),
    )

    if verbose:
        print("Original size of wavefield [pixels]: {}".format((Ax, Ay)))
        print("Sampled area size (pixels): {}".format([Sx, Sy]))
        print("Nx (pixels): {}".format(_x1))
        print("Ny (pixels): {}".format(_y1))
        print("mid x: {}".format(midX))
        print("mid y: {}".format(midY))
        print("Region of interest (pixels): {}".format(ROI))
    else:
        pass

    x0, y0 = ROI[0][0], ROI[0][1]
    x1, y1 = ROI[1][0], ROI[1][1]

    lX = ROI[1][0] - ROI[0][0]
    lY = ROI[1][1] - ROI[0][1]

    if show:
        I = abs(A.conjugate() * A)
        figure, ax = plt.subplots(1)
        rect = patches.Rectangle((x0, x0), lX, lY, edgecolor="r", facecolor="none")

        plt.imshow(I)
        ax.add_patch(rect)
        plt.title("Original Wavefield with Sampled Area")
        plt.show()
        plt.clf()
        plt.close()
    else:
        pass

    B = A[y0:y1, x0:x1]

    return B


# %%
def fromPickle(path, wavefront=False):
    import pickle

    with open(path, "rb") as a:
        w = pickle.load(a)

    return w


# %%
def fig2data(fig):
    """
    @brief Convert a Matplotlib figure to a 4D numpy array with RGBA channels and return it
    @param fig a matplotlib figure
    @return a numpy 3D array of RGBA values
    """
    # draw the renderer
    fig.canvas.draw()

    # Get the RGBA buffer from the figure
    w, h = fig.canvas.get_width_height()
    buf = np.fromstring(fig.canvas.tostring_argb(), dtype=np.uint8)
    buf.shape = (w, h, 4)

    # canvas.tostring_argb give pixmap in ARGB mode. Roll the ALPHA channel to have it in RGBA mode
    buf = np.roll(buf, 3, axis=2)
    return buf
