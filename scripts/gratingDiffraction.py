#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 16:59:01 2023

@author: jerome
"""

import numpy as np
import xraydb
import matplotlib.pyplot as plt


def gratingEfficiency(wl, T, dn, m=1, f=0.5):
    eta_0 = 1 - (4 * f * (1 - f)) * ((np.sin((np.pi * dn * T) / (wl)) ** 2))
    eta_m = (
        (np.sin(m * np.pi * f) * np.sin((np.pi * dn * T) / (wl))) / ((m * np.pi) / 2)
    ) ** 2

    return eta_m, eta_0


def intensityFromGrating(s, E, wl, R, N, p):
    dp = np.linspace(0, (3 * wl) / s, 10000)
    k = (2 * np.pi) / wl

    i1 = ((np.sin((N * k * p * dp) / 2)) / (np.sin((k * p * dp) / 2))) ** 2
    i2 = ((np.sin((k * s * dp) / 2)) / ((k * s * dp) / 2)) ** 2

    I = (
        ((s * E) / (wl * (R**2)))
        * (((np.sin((N * k * p * dp) / 2)) / (np.sin((k * p * dp) / 2))) ** 2)
        * (((np.sin((k * s * dp) / 2)) / ((k * s * dp) / 2)) ** 2)
    )

    #    print(I)

    print(max(I[1::]))

    plt.plot(dp, [i / np.max(I[1::]) for i in I], label="I")
    plt.plot(dp, [i / np.max(i1[1::]) for i in i1], label="i1")
    plt.plot(dp, [i / np.max(i2[1::]) for i in i2], label="i2")
    plt.legend()
    plt.show()


def test():
    wl = 6.7e-9
    T = 100e-9
    E = 1
    R = 1
    N = 1000
    p = 100e-9
    s = 1

    intensityFromGrating(s, E, wl, R, N, p)


#    dn = xraydb.xray_delta_beta('HSiO1.5'

if __name__ == "__main__":
    test()
