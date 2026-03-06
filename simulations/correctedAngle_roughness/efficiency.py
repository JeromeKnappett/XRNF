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

def getAerialImageEfficiency(inTiff,tiffs,inRes,res,mid,G,D,verbose=True,show=True):
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
                          extra=(700,50),verbose=verbose,show=show)
        print(E)
        E0.append(E[0])
        E1.append(E[1])
        
    return E0,E1
def test():
    dirPath = '/user/home/opt/xl/xl/experiments/correctedAngle_roughness/data/'
    #savePath = '/home/jerome/Documents/MASTERS/Figures/plots/roughness/'
    order = order = range(0,25)
    cY = [2,4,6,8,10,10]
    sigma = [0.5,1.0,1.5,2.0,2.5]#,3.0,3.5,4.0]
    files = [str(o) + '/' + str(o) + 'intensity.tif' for o in order]
    labels =  ['\u03C3 = 0.5 nm ','\u03C3 = 1.0 nm ','\u03C3 = 1.5 nm ','\u03C3 = 2.0 nm','\u03C3 = 2.5 nm','\u03C3 = 3.0 nm','\u03C3 = 3.5 nm','\u03C3 = 4.0 nm']
    legendTitle = None #'$C_y =$ 2 nm' # None #'$C_y =$ 10 nm'
    
    # Specify analysis - turn plotting on and off
    show = True                          # show initial tiffs and entire profiles
    split = False                        # split into groups by correlation length (for ploting all aerial images together)
    save = False                         # save plots to savePath
    fromPickle = False
    toPickle = False
    
    N = 2000                            # number of pixels to take for line profile  - 1200 for roughness aerial images
    n = 15                             # number of pixels to average over for line profile - 15 for roughness aerial images
    plotRange = 1000                       # range of aerial image plot in nm
    
    #middle pixels of images
    mid = np.full((np.shape(files)[0],2), (196, 12188))
    res = np.full((np.shape(files)[0],2), [2.5011882651601634e-09, 2.426754806976689e-07])
    #pitch = 100e-9
    
    # read from files - create profiles and images of sampled range
    if fromPickle:
        picks = [pickle.load(open(dirPath + f, 'rb')) for f in files]
        tiffs = [p[0] for p in picks]
        res = [(p[1],p[2]) for p in picks]
        inPick = pickle.load(open(dirPath + '/incident/incident.pkl','rb'))
        inTiff = inPick[0]
        inRes = (inPick[1],inPick[2])
#    print(res)
    else:
        res = np.full((np.shape(files)[0],2), [2.5011882651601634e-09, 2.426754806976689e-07])
        inPick = pickle.load(open(dirPath + '/incident/incident.pkl','rb'))
        inTiff = inPick[0]
        inRes = (inPick[1],inPick[2])
        try:
            tiffs = [tifffile.imread(dirPath + f) for f in files]
        except FileNotFoundError:
            tiffs = [tifffile.imread(f) for f in files]
        
    images = [t[m[0]-n:m[0]+n,m[1]-N:m[1]+N] for t, m in zip(tiffs,mid)]
#    profiles = [i.mean(0) for i in images] #[t[m[0]-n:m[0]+n,m[1]-N:m[1]+N] for t, m in zip(tiffs,mid)]
#    xP = [np.linspace(-N*r[0], N*r[0],2*N) for r in res]
#    yP = [np.linspace(-n*r[1], n*r[1],2*n) for r in res]
    
    E0,E1 = getAerialImageEfficiency(inTiff,tiffs,inRes,res,mid,G=12.0e-6,D=27.5e-6,verbose=False,show=False)
    
    E0 = np.reshape(E0,(5,5))
    E1 = np.reshape(E1,(5,5))
    
    for i,e in enumerate(E0):
        plt.plot(sigma,e,':x',label='$c_y$ = ' + str(cY[i]) + ' nm')
    plt.xlabel('RMS LER')
    plt.ylabel('0 order efficiency')
    plt.legend()
    plt.show()
    for i, e in enumerate(E1):
        plt.plot(sigma,e,':x',label='$c_y$ = ' + str(cY[i]) + ' nm')
    plt.xlabel('RMS LER')
    plt.ylabel('aerial image efficiency')
    plt.legend()
    plt.show()
    
if __name__ == '__main__':
    test()