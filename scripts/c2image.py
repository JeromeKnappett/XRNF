#!/usr/bin/env python
#
# Name: c2image.py
# Author: Cameron M. Kewish
#
# Description:
# Python script to transform a complex array into an RGB image, mapping phase
# to hue, amplitude to value and keeping maximum saturation.
#
# Returns:
#   RGB                 RGB array representing hue and value for complex phase
#                       and amplitude, with full colour saturation
#
# Dependencies:
#   numpy, matplotlib.colors.hsv_to_rgb
#
# To do:
#
# History:
#
# 2017-09-18: Cameron M. Kewish, first version forked from PtyPy/complex2hsv.


def c2image(cin, vmin=0., vmax=None):
    """
    Syntax:
        c2image(cin, vmin=0., vmax=None)

    Python script to transform a complex array into an RGB image, mapping phase
    to hue, amplitude to value and keeping maximum saturation.

    Parameters:
        cin                   (ndarray) : complex two-dimensional input image

    Optional parameters:
        vmin, vmax              (float) : clip amplitude to this interval
                                        : [default vmin = 0.0, vmax = None]
    Returns:
        rgb                   (ndarray) : RGB conversion of HSV image output
    """

    import numpy as np
    import matplotlib.colors

    # HSV channels
    h = 0.5 * np.angle(cin) / np.pi + 0.5
    s = np.ones(cin.shape)
    v = abs(cin)

    if vmin is None:
        vmin = v.min()

    if vmax is None:
        vmax = v.max()

    if vmin == vmax:
        v = np.ones_like(v) * v.mean()
        v = v.clip(0.0, 1.0)

    else:
        assert vmin < vmax
        v = (v.clip(vmin, vmax)-vmin)/(vmax-vmin)

    hsv = np.transpose(np.asarray((h, s, v)), (1, 2, 0))

    return matplotlib.colors.hsv_to_rgb(hsv)

# def arr_creat(upperleft, upperright, lowerleft, lowerright):    
#     import matplotlib.pyplot as plt
#     import numpy as np
    
#     arr = np.linspace(np.linspace(lowerleft, lowerright, arrwidth), 
#                       np.linspace(upperleft, upperright, arrwidth), arrheight, dtype=int)
#     return arr[:, :, None]

def complexCbar(c,N, show=False):
    import matplotlib.pyplot as plt
    import numpy as np
    # import plotting
    from colormap2d import ColorMap2D
    
    pmin,pmax = np.min(c.imag), np.max(c.imag) #np.min(np.angle(c)), np.max(np.angle(c))
    imin,imax = np.min(c.real), np.max(c.real) #np.min(np.abs(c)), np.max(np.abs(c))

    i1 = np.linspace(imin,imax,N)
    p1 = np.linspace(pmin,pmax,N)
    ph = np.linspace(np.min(np.angle(c)),np.max(np.angle(c)),N)
    ah = np.linspace(-1,1,N)
    
    di = abs(i1[1]-i1[0])
    dp = abs(p1[1]-p1[0])
    dP = abs(ph[1]-ph[0])
    dA = abs(ah[1]-ah[0])
    
    i2 = np.tile(i1,[N,1])
    p2 = np.flipud(np.tile(p1,[N,1]).T)
    
    # print(p1)
    # print(i1)
    
    cBar = np.array([i + p*1j for i,p in zip(i2.flatten(),p2.flatten())])
    cBar = np.reshape(cBar,[N,N])
    
    cb = c2image(cBar)
    
    # if show:
    #     plotting.plotTwoD(cb,
    #                       dx=dA,
    #                       dy=dP,
    #                       xLabel='Amplitude [|A|]',
    #                       yLabel='Phase [rad]',
    #                       numXticks=3,
    #                       numYticks=3,
    #                       cbar=False,
    #                       aspct=3)
    # else:
    #     pass
    return cb,di,dP,dA

def test():
    import pickle
    dirPath = '/user/home/opt/xl/xl/experiments/correctedWBS_beamCharacterisation/data/aerialImageEfield/'
    
    files = ['aerialImageEfieldEfields.pkl']
    #['atM1EfieldsNEW.pkl']
    #['aerialImageEfieldEfieldsNEW.pkl']
    # ['beforeBDA_efield_sx200sy200EfieldsNEW.pkl','beforeBDA_efield_sx200sy200_10000eEfieldsNEW.pkl']
    #,'maskExitEfieldEfieldsNEW.pkl','aerialImageEfieldEfieldsNEW.pkl']
    #['atM1EfieldsNEW.pkl'] 

    T = [pickle.load(open(dirPath + f, 'rb')) for f in files]
    EhR = [p[0] for p in T]
    EhI = [p[1] for p in T]
    EvR = [p[2] for p in T]
    EvI = [p[3] for p in T]
    res = [(p[4],p[5]) for p in T]
    Eh = [eR + eI*1j for eR,eI in zip(EhR,EhI)]
    Ev = [eR + eI*1j for eR,eI in zip(EvR,EvI)]
    # E = [np.sqrt((h**2) + (v**2)) for h,v in zip(Eh,Ev)]
    E = [eh + ev for eh,ev in zip(Eh,Ev)]
    
    complexCbar(E[0],1000)

if __name__ == '__main__':
    test()