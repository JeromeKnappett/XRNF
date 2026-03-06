#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 17 14:15:36 2022

@author: jerome
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d


def centeredDistanceMatrix(n):
    # make sure n is odd
    x, y = np.meshgrid(range(n), range(n))
    return np.sqrt((x - (n / 2) + 1) ** 2 + (y - (n / 2) + 1) ** 2)


def function(d):
    return np.log(d)  # or any funciton you might have


def arbitraryfunction(d, y, n):
    x = np.arange(n)
    f = interp1d(x, y)
    return f(d.flat).reshape(d.shape)


n = 101
d = centeredDistanceMatrix(n)
y = np.random.randint(0, 100, n)  # this can be your vector
f = arbitraryfunction(d, y, n)
plt.plot(np.arange(101), arbitraryfunction(np.arange(n), y, n))
plt.show()
plt.imshow(f.T, origin="lower", interpolation="nearest")
plt.show()
