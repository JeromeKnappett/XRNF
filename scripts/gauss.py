#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 11 15:05:09 2022

@author: jerome
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def gauss(a, n, sigma):
    """
    a = maximum angle
    n = number of angular points
    sigma = standard deviation
    """

    theta = np.linspace(-a, a, n)
    G = [np.exp((-1 * (t**2)) / (2 * (sigma**2))) for t in theta]

    plt.plot(theta, G)
    plt.show()


def gauss2D(nx, ny, mu, sigma):
    # Initializing value of x-axis and y-axis
    # in the range -1 to 1
    x, y = np.meshgrid(np.linspace(-1, 1, nx), np.linspace(-1, 1, ny))
    dst = np.sqrt(x * x + y * y)

    # Calculating Gaussian array
    gauss = np.array(np.exp(-((dst - mu) ** 2 / (2.0 * sigma**2))))

    kernel = 6 * sigma - 1
    print("Kernel: {}".format(kernel))
    print("2D Gaussian array :\n")
    # print(gauss)
    plt.imshow(gauss)
    plt.title("Gaussian")
    plt.show()

    return gauss


# def testCarray(A):


#     D = []

#     for x, a in enumerate(A):
#         print(a)
#         for y, b in enumerate(a):
#             print(b)

#             d = np.sqrt((x**2)+(y**2))

#             # print(d)
#             D.append(d)

#     D = np.reshape(np.array(D),(5,5))
#     print(D)
#     print(np.shape(D))


#     return(D)


def testCarray(A, B):
    ny, nx = np.shape(A)
    midY, midX = int(ny / 2), int(nx / 2)
    print(midY, midX)

    D = []
    COH = []

    for x, a in enumerate(A):
        # print(a)
        for y, b in enumerate(a):
            # print(b)

            dx = midX - x
            dy = midY - y
            d = np.sqrt((dx**2) + (dy**2))

            # D.append(d)

            for i, c in enumerate(B):
                # print(c)
                for j, e in enumerate(c):
                    # print(e)
                    _dx = midX - i
                    _dy = midY - j
                    _d = np.sqrt((_dx**2) + (_dy**2))

                    dD = d - _d

                    C = b * e.conjugate()

                    print(C)
                    D.append(dD)
                    COH.append(C)

    print("HERE")
    print(np.shape(COH))

    # chS = np.reshape(np.array(),(ny,nx))
    print(COH)

    df = pd.DataFrame({"pSep": D, "coherence": COH})
    print(df)

    DF = df.groupby(["pSep"]).mean()
    print(DF)

    print(DF["coherence"])
    # print(DF)

    # print(D)
    # print(np.shape(D))

    # print(COH)
    # print(np.shape(COH))

    dC = DF["coherence"].to_numpy()
    # pS = DF['pSep'].to_numpy()

    _dC = np.reshape(dC[1:-1], (ny, nx))

    plt.imshow(_dC)
    plt.show()

    return D


def testGauss():
    nx = 5
    ny = 5

    mu1 = 0
    sigma1 = 1

    G1 = gauss2D(nx, ny, mu1, sigma1)

    mu2 = 0
    sigma2 = 0.5

    G2 = gauss2D(nx, ny, mu2, sigma2)

    # print(G1)

    # testCarray(G1,G2)


def test():
    a = np.pi / 6
    n = 100
    sigma = 1

    gauss(a, n, sigma)


if __name__ == "__main__":
    testGauss()
