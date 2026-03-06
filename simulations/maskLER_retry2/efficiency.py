#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 10:52:56 2023

@author: -
"""


import tifffile
import numpy as np
import matplotlib.pyplot as plt
import pickle
from utilMask_n import defineOrderROI,getEfficiency


def round_sig(x, sig=2):
    from math import log10, floor
    if x != 0:
        return round(x, sig-int(floor(log10(abs(x))))-1)
    else:
        return x

def getAerialImageEfficiency(inTiff,tiffs,inRes,res,mid,G,D,extra=(1300,100),verbose=True,show=True):
    """
    inTiff: tiff of incident intensity
    tiffs: array of tiffs of propagaed intensity
    inRes: resolution of incident intensity
    res: resolution of propagated tiffs
    mid: middle pixel position
    G: Grating size [m]
    D: Grating separation
    """
    E0, E1 = [],[]
    
    for i,t in enumerate(tiffs):
        I = [inTiff,t]
        R = [inRes,res[i]]
        print(R)
        print(mid[i][0])#*res[i][0])
        print(np.shape(t)[0]/2)
        print(np.shape(t)[1]/2)
        print(abs(np.shape(t)[0]/2 - mid[i][0]))
        print(abs(np.shape(t)[0]/2 - mid[i][0])*res[i][1])
        E = getEfficiency(I,R,m=1,G=G,
                          numGrats=2,
                          offset=((abs(np.shape(t)[1]/2 - mid[i][1])*res[i][0]) + (D/2.0),
                                  abs(np.shape(t)[0]/2 - mid[i][0])*res[i][1]),
                          extra=extra,verbose=verbose,show=show)
        print(E)
        E0.append(E[0])
        E1.append(E[1])
        
    return E0,E1

def test():
    dirPath = '/user/home/opt/xl/xl/experiments/maskLER2/data/'
    #savePath = '/home/jerome/Documents/MASTERS/Figures/plots/roughness/'
    order = ['rms05','rms10','rms15','rms20','rms25','rms30','rms35','rms40']#range(0,25)
    cY = [2,2,2,2,2,4,4,4,4,4,6,6,6,6,6,8,8,8,8,8,10,10,10,10,10]
    sigma = [0.5,1.0,1.5,2.0,2.5,3.0,3.5,4.0]
    files = [str(o) + '/' + str(o) + '.pkl' for o in order]
    labels =  ['\u03C3 = 0.5 nm ','\u03C3 = 1.0 nm ','\u03C3 = 1.5 nm ','\u03C3 = 2.0 nm','\u03C3 = 2.5 nm','\u03C3 = 3.0 nm','\u03C3 = 3.5 nm','\u03C3 = 4.0 nm']
    legendTitle = None #'$C_y =$ 2 nm' # None #'$C_y =$ 10 nm'
    
    # Specify analysis - turn plotting on and off
    show = True                          # show initial tiffs and entire profiles
    split = False                        # split into groups by correlation length (for ploting all aerial images together)
    save = False                         # save plots to savePath
    fromPickle = True
    toPickle = False
    
    N = 2000                            # number of pixels to take for line profile  - 1200 for roughness aerial images
    n = 15                             # number of pixels to average over for line profile - 15 for roughness aerial images
    plotRange = 1000                       # range of aerial image plot in nm
    
    #middle pixels of images
    mid = np.full((np.shape(files)[0],2), (399, 25025))
    #pitch = 100e-9
    
    # read from files - create profiles and images of sampled range
    if fromPickle:
        picks = [pickle.load(open(dirPath + f, 'rb')) for f in files]
        tiffs = [p[0] for p in picks]
        res = [(p[1],p[2]) for p in picks]
        inPick = pickle.load(open(dirPath + 'incident/incident.pkl','rb'))
        inTiff = inPick[0]
        inRes = (inPick[1],inPick[2])
    #    print(res)
    else:
        res = np.full((np.shape(files)[0],2), [2.5011882651601634e-09, 2.426754806976689e-07])
        try:
            tiffs = [tifffile.imread(dirPath + f) for f in files]
        except FileNotFoundError:
            tiffs = [tifffile.imread(f) for f in files]
        
    images = [t[m[0]-n:m[0]+n,m[1]-N:m[1]+N] for t, m in zip(tiffs,mid)]
    profiles = [i.mean(0) for i in images] #[t[m[0]-n:m[0]+n,m[1]-N:m[1]+N] for t, m in zip(tiffs,mid)]
    xP = [np.linspace(-N*r[0], N*r[0],2*N) for r in res]
    yP = [np.linspace(-n*r[1], n*r[1],2*n) for r in res]
    
    E0,E1 = getAerialImageEfficiency(inTiff,tiffs,inRes,res,mid,G=12.0e-6,D=27.5e-6,verbose=False,show=False)
    
    plt.plot(sigma,[e*100 for e in E0],label='$m=0$')
    plt.xlabel('RMS LER [nm]')
    plt.ylabel('% Efficiency')
    plt.legend()
    plt.show()
    plt.plot(sigma,[e*100 for e in E1],label='$m= \pm 1$')
    plt.xlabel('RMS LER [nm]')
    plt.ylabel('% Efficiency')
    plt.legend()
    plt.show()
    
    
    #plt.plot(sigma,[e*100 for e in E0],label='$m=0$')
    #plt.xlabel('RMS LER [nm]')
    ##plt.ylabel('0 order efficiency')
    ##plt.show()
    #plt.plot(sigma,[e*100 for e in E1],label='$m= \pm 1$')
    #plt.xlabel('RMS LER [nm]')
    #plt.ylabel('% Efficiency')
    #plt.legend()
    #plt.show()
    
    fig, ax0 = plt.subplots()
    ax1 = ax0.twinx()
    ax0.plot(sigma,[e*100 for e in E0],':x',color='blue',label='$m=0$')
    ax1.plot(sigma,[e*100 for e in E1],':x',color='red',label='$m= \pm 1$')
    ax0.set_ylabel('% Efficiency ($m=0$)')
    ax1.set_ylabel('% Efficiency ($m= \pm 1$)')
    ax1.spines['left'].set_color('blue')
    ax1.spines['right'].set_color('red')
    ax0.yaxis.label.set_color('blue')
    ax0.tick_params(axis='y', colors='blue')
    ax1.yaxis.label.set_color('red')
    ax1.tick_params(axis='y', colors='red')
    ax0.set_xlabel('RMS LER [nm]')
    fig.tight_layout()
    plt.show()
    
    
    dE0 = 100*((E0[-1] - E0[0])/E0[0])
    dE1 = 100*((E1[0] - E1[-1])/E1[0])
    print(" ")
    print("Percentage increase in zero order efficiency:   {} %".format(dE0))
    print("Percentage decrease in aerial image efficiency: {} %".format(dE1))
    
if __name__ == '__main__':
    test()