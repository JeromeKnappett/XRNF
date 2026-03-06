#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  1 10:53:23 2022

@author: jerome
"""
import numpy as np
import matplotlib.pyplot as plt


def radiusN(n, wl, f):
    rn = np.sqrt(n * wl * f + ((n**2) * (wl**2)) / 4)
    return rn


def NAfromZoneWidth(lam, dr):
    """
    Parameters
    ----------
    lam : int/float
        Wavelength in m.
    dr : int/float
        Zone width of outermost zone in m.
    Returns
    -------
    NA : Numerical aperture of FZP.
    """
    return lam / (2 * dr)


def NAfromF(r, f):
    """
    Parameters
    ----------
    r : int/float
        Distance from optical axis to outermost zone in m.
    f : int/float
        Focal length of FZP in m.
    Returns
    -------
    NA : Numerical aperture of FZP.
    """
    return r / f


def fLengthFZP(r, n, lam):
    """
    Parameters
    ----------
    r : int/float
        Distance from optical axis to outermost zone in m.
    n : int
        Number of zones.
    lam : int/float
        Wavelength in m.
    Returns
    -------
    f : Focal length of FZP in m.
    """
    f = (1 / (n * lam)) * ((r**2) - ((n**2) * (lam**2)) / 4)
    # f = (r**2)/(n*lam)
    return f


def centeredDistanceMatrix(n):
    # make sure n is odd
    x, y = np.meshgrid(range(n), range(n))
    return np.sqrt((x - (n / 2) + 1) ** 2 + (y - (n / 2) + 1) ** 2)


def centeredDistanceMatrix(n):
    # make sure n is odd
    x, y = np.meshgrid(range(n), range(n))
    return np.sqrt((x - (n / 2) + 1) ** 2 + (y - (n / 2) + 1) ** 2)


def function(d):
    return np.log(d)  # or any funciton you might have


def arbitraryfunction(d, y, n):
    from scipy.interpolate import interp1d

    x = np.arange(n)
    f = interp1d(x, y)
    return f(d.flat).reshape(d.shape)


def test():
    wl1 = 6.7e-9
    wl2 = 13.5e-9
    n = 1000
    r = 500e-6
    f1 = 150e-3
    f2 = 100e-6
    dr = 100e-9

    NAzw = NAfromZoneWidth(wl1, dr)
    NAf = NAfromF(r, f1)
    print(NAzw)
    print(NAf)
    fL = fLengthFZP(r, n, wl2)
    print(fL)

    from zone_plate import NormalFZP, fzp1D
    from useful import fig2data

    zp = NormalFZP(f=10.888, w=6.7, N=1667, _DEBUG=True)
    # Preview the zone plate.
    plt.clf()
    plt.close()
    zpFig = zp.plot(save=False, file_ext="tif")  # dpi=1060

    # fzp = fig2data(zpFig)
    print(zpFig)
    plt.imshow(zpFig)
    plt.show()
    # n = 1024
    # rad = int(n/2)
    # fzp = fzp1D(6.7, 250, 10.888, num_data=n)
    # fzp_rad = fzp[rad:n]

    # # plt.clf()
    # # plt.close()
    # # plt.plot(fzp_rad)
    # # # plt.xlim(400,625)
    # # plt.show()

    # d = centeredDistanceMatrix(rad)
    # # y = np.random.randint(0,100,n) # this can be your vector
    # f = arbitraryfunction(d,fzp_rad,rad)
    # plt.plot(np.arange(rad),arbitraryfunction(np.arange(rad),fzp_rad,rad))
    # plt.show()
    # plt.imshow(f.T,origin='lower',interpolation='nearest')
    # plt.colorbar()
    # plt.show()

    # Idata = fig2data(I)

    # Rendering high DPI will take a long time or fail, so only set it
    # when saving directly to disk.

    # zp.plot(save=False, dpi=1060)


if __name__ == "__main__":
    test()
