#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 10:15:51 2021

@author: jerome
"""
import pickle
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import pylab

from labellines import labelLine, labelLines

plt.style.use(["science", "no-latex"])  # 'ieee',
pylab.rcParams["figure.figsize"] = (10.0, 8.0)

path = "/home/jerome/dev/experiments/beamPolarisation11/data/"
# pickles = [path + 's25-0prop.pkl']

pickles = []

sep = range(25, 226, 25)
angle = range(0, 91, 45)


pickWav = "/home/jerome/dev/experiments/maskEfficiency16/data/mt-exit1340.pkl"  # exit-f0-825.pkl' mt-exit1050.pkl
with open(pickWav, "rb") as g:
    r = pickle.load(g)

    nx = r["results"]["params/Mesh/nx"]
    xMax = r["results"]["params/Mesh/xMax"]
    xMin = r["results"]["params/Mesh/xMin"]
    rx = np.subtract(xMax, xMin)
    dx = np.divide(rx, nx)
    ny = r["results"]["params/Mesh/ny"]
    yMax = r["results"]["params/Mesh/yMax"]
    yMin = r["results"]["params/Mesh/yMin"]
    ry = np.subtract(yMax, yMin)
    dy = np.divide(ry, ny)

    print("(xMin,xMax) [m]: {}".format((xMin, xMax)))
    print("x-Range [m]: {}".format(rx))
    print("(yMin,yMax) [m]: {}".format((yMin, yMax)))
    print("y-Range [m]: {}".format(ry))
    print("Dimensions (Nx,Ny) [pixels]: {}".format((nx, ny)))
    print("Resolution (dx,dy) [m]: {}".format((dx, dy)))

    Ix = r["results"]["Intensity/Total/X/profile"]
    Iy = r["results"]["Intensity/Total/Y/profile"]

    plt.plot(Ix, label="x-profile")
    plt.plot(Iy, label="y-profile")
    plt.legend()
    plt.show()


#
# for i in sep:
#    for j in angle:
#        p = path + 's' + str(i) + '-' + str(j) + 'prop.pkl'
#
#        pickles.append(p)
#
#
# for p in pickles:
#    try:
#        with open(p, 'rb') as g:
#            wD = pickle.load(g)
#
#        print("Shape of wD[0]: {}".format(np.shape(wD[0])))
#        print("Shape of wD[1]: {}".format(np.shape(wD[1])))
#        print("Shape of wD[2]: {}".format(np.shape(wD[2])))
#        print("Shape of wD[3]: {}".format(np.shape(wD[3])))
#        print("Shape of wD[4]: {}".format(np.shape(wD[4])))
#        print("Shape of wD[5]: {}".format(np.shape(wD[5])))
#
#        nz = 100
#        nx = 4000
#        ny = 4000
#
#        Izx = np.reshape(wD[0], (nx,nz+1))
#
#        from matplotlib.colors import LogNorm
#
#        plt.clf()
#        plt.close()
#        figure(figsize=(8, 8), dpi=80)
#        plt.imshow(Izx, aspect='auto')
#        plt.colorbar()
#        plt.title("Propagation plot - X")
#    #    plt.savefig(dirPath + 'plots/' + pk[0:len(str(pk))-4] + 'propPlotX.png')
#        plt.show()
#
#        plt.clf()
#        plt.close()
#        figure(figsize=(8, 8), dpi=80)
#        plt.imshow(abs(Izx), aspect='auto', norm=LogNorm(),vmin=1, vmax=np.max(abs(Izx)))
#        plt.colorbar()
#        plt.title("Propagation plot - X (LOG NORMALISED)")
#    #    plt.savefig(dirPath + 'plots/' + pk[0:len(str(pk))-4] + 'propPlotXLOGNORM.png')
#        plt.show()
#
#        Izy = np.reshape(wD[1], (ny,nz+1))
#
#        plt.clf()
#        plt.close()
#        figure(figsize=(8, 8), dpi=80)
#        plt.imshow(Izy, aspect='auto', vmin=0, vmax = 1e11)
#        plt.colorbar()
#        plt.title("Propagation plot - Y")
#    #    plt.savefig(dirPath + 'plots/' + pk[0:len(str(pk))-4] + 'propPlotY.png')
#        plt.show()
#
#        plt.clf()
#        plt.close()
#        figure(figsize=(8, 8), dpi=80)
#        plt.imshow(abs(Izy), aspect='auto', norm=LogNorm(),vmin=1e6, vmax=np.max(abs(Izy)))
#        plt.colorbar()
#        plt.title("Propagation plot - Y (LOG NORMALISED)")
#    #    plt.savefig(dirPath + 'plots/' + pk[0:len(str(pk))-4] + 'propPlotYLOGNORM.png')
#        plt.show()
#
#        plt.clf()
#        plt.close()
#        plt.plot(wD[0])
#        plt.title("propArray[0]")
#        print("Saving x-intensity vs z plot...")
#    #    plt.savefig(dirPath + "plots/" + pk[0:len(str(pk))-4] + "XvsZ_0.png")
#        plt.show()
#
#        plt.clf()
#        plt.close()
#        figure(figsize=(8, 8), dpi=80)
#        plt.plot(wD[1])
#        plt.title("propArray[1]")
#        print("Saving y-intensity vs z plot...")
#    #    plt.savefig(dirPath + "plots/" + pk[0:len(str(pk))-4] + "XvsZ_1.png")
#        plt.show()
#
#        # plt.clf()
#        # plt.close()
#        # figure(figsize=(8, 8), dpi=80)
#        # plt.plot(wD[2])
#        # plt.title("propArray[2], P: " + pk[0:len(str(pk))-4])
#        # print("Saving y-intensity vs z plot...")
#        # plt.savefig(dirPath + "plots/" + pk[0:len(str(pk))-4] + "XvsZ_2.png")
#        # plt.show()
#
#        # plt.clf()
#        # plt.close()
#        # figure(figsize=(8, 8), dpi=80)
#        # plt.plot(wD[3])
#        # plt.title("propArray[3], P: " + pk[0:len(str(pk))-4])
#        # print("Saving y-intensity vs z plot...")
#        # plt.savefig(dirPath + "plots/" + pk[0:len(str(pk))-4] + "XvsZ_3.png")
#        # plt.show()
#
#        plt.clf()
#        plt.close()
#        figure(figsize=(8, 8), dpi=80)
#        plt.plot(wD[4])
#        plt.title("propArray[4]")
#        print("Saving y-intensity vs z plot...")
#    #    plt.savefig(dirPath + "plots/" + pk[0:len(str(pk))-4] + "XvsZ_4.png")
#        plt.show()
#
#        plt.clf()
#        plt.close()
#        figure(figsize=(8, 8), dpi=80)
#        plt.plot(wD[5])
#        plt.title("propArray[5]")
#        print("Saving y-intensity vs z plot...")
#    #    plt.savefig(dirPath + "plots/" + pk[0:len(str(pk))-4] + "XvsZ_5.png")
#        plt.show()
#    except FileNotFoundError:
#        print("No file found: {}".format(p))
#        pass
#
