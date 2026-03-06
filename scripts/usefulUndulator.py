#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 09:30:51 2023

@author: jerome
"""

import numpy as np
import matplotlib.pyplot as plt


def deflectionK(B, period):
    e = 1.602176634e-19  # fundamental electron charge
    me = 9.1093837e-31  # electron mass
    c = 299792458  # speed of light
    K = (e * B * period) / (2 * np.pi * me * c)

    return K


def lorentzFactor(E):
    e = 1.602176634e-19  # fundamental electron charge
    me = 9.1093837e-31  # electron mass
    c = 299792458  # speed of light

    print(me * (c**2))

    gamma = E / ((me * (c**2) * (1 / e)))
    # gamma = 1957 * E

    return gamma


def centralRadiationCone(gamma, N):
    theta = 1 / (gamma * np.sqrt(N))

    return theta


def undulatorEquation(period, gamma, K, m=1, theta=0):
    wl = (
        (1 / m)
        * (period / (2 * (gamma**2)))
        * (1 + ((K**2) / 2) + ((gamma**2) * (theta**2)))
    )

    return wl


def test():
    E = 3.01e9
    period = 75e-3
    N = 25
    B = 0.46111878

    gamma = lorentzFactor(E)
    print("gamma = ", gamma)

    K = deflectionK(B, period)
    print("K = ", K)

    wl = undulatorEquation(period, gamma, K)
    print("wavelength = ", wl)


if __name__ == "__main__":
    test()
