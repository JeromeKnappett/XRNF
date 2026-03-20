#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 11 15:05:09 2022

@author: jerome
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from useful import round_sig

def gauss(a,n,sigma):
    """
    a = maximum angle
    n = number of angular points
    sigma = standard deviation
    """
    
    theta = np.linspace(-a,a,n)
    G = [np.exp((-1*(t**2))/(2*(sigma**2))) for t in theta]
    
    plt.plot(theta,G)
    plt.show()
    

def gauss2D(nx,ny, mu, sigma):
    # Initializing value of x-axis and y-axis
    # in the range -1 to 1
    x, y = np.meshgrid(np.linspace(-1,1,nx), np.linspace(-1,1,ny))
    dst = np.sqrt(x*x+y*y)
  
    # Calculating Gaussian array
    gauss = np.array(np.exp(-( (dst-mu)**2 / ( 2.0 * sigma**2 ) ) ))
  
    kernel = 6*sigma - 1
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

def testCarray(A,B):
    print("starting")
    print(np.shape(A))
    # print(A)
    ny,nx = np.shape(A)[0], np.shape(A)[1]
    midY, midX = (ny-1)/2, (nx-1)/2
    print(midY, midX)
    
    Dx = []
    Dy = []
    COH = []
    NC = []
    
    for x, a in enumerate(A):
        # print(a)
        for y, b in enumerate(a):
            # print(b)
            
            dx = midX - x
            dy = midY - y
            d = np.sqrt((dx**2)+(dy**2))
            # print(f'  x,y  :   {(x,y)}')
            # print(f' dx,dy :   {(dx,dy)}')
            # D.append(d)
            
            for i, c in enumerate(B):
                # print(c)
                for j, e in enumerate(c):
                    # print(e)
                    _dx = midX - i
                    _dy = midY - j
                    _d = np.sqrt((_dx**2)+(_dy**2))
                    # print(f'  i,j  :     {(i,j)}')
                    # print(f' _dx,_dy :   {(_dx,_dy)}')
                    
                    # dD = round_sig(d - _d, 2)
                    dDx = abs(x - i) #dx - _dx
                    dDy = abs(y - j) #dy - _dy
                    
                    C = abs(b.conjugate()*e)
                    nc = C/(np.sqrt((abs(b)**2))*np.sqrt((abs(e)**2)))
                    
                    # print(C)
                    Dx.append(dDx)
                    Dy.append(dDy)
                    COH.append(C)
                    NC.append(nc)
                    
    
    dC = np.reshape(NC,(nx*ny,nx,ny))
    # print(dC)
    print(np.shape(dC))
    print('HERE')
    print(np.shape(Dx))
    print(np.unique(Dx))
    print(np.shape(np.unique(Dx)))
    # print('hereeeeee')
    # # print(D)
    # # chS = np.reshape(np.array(),(ny,nx))
    # print(COH)
    
    T = []
    for c in dC:
        # # nC = c/abs(np.squeeze(A*A.conjugate()))
        # # plt.imshow(nC)
        # plt.imshow(c)
        # plt.colorbar()
        # plt.show()
        
        trial = c.mean()
        T.append(trial)
        print(trial)
    
    T = np.reshape(T,(nx,ny))
    plt.imshow(T)
    plt.show()    
    
    normC = dC.mean(0)
    
    plt.imshow(abs(A))
    plt.title("I")
    plt.colorbar()
    plt.show()
    
    df = pd.DataFrame({'xSep': Dx,
                       'ySep': Dy,
                       'coherence': [c[0] for c in NC]})
    # print(df)
    
    DF = df.groupby(['xSep','ySep']).mean()
    print(DF)
    # print(DF['pSep'])
    DFc = np.array(DF[['coherence']])
    
    # print('Here')
    # print(DFc)
    print('heerre')
    print(np.shape(DFc))
    
    # print(D)
    # print(np.shape(D))
    
    # print(COH)
    # print(np.shape(COH))
    
    degC = DF['coherence'].to_numpy()
    print(degC)
    print(np.shape(degC))
    # pS = DF['pSep'].to_numpy()
    
    _dC = np.reshape(degC,(ny,nx))
    print(_dC)
    
    plt.imshow(_dC)
    plt.colorbar()
    plt.show()
    
    plt.plot(_dC[0:7][0])
    plt.plot(_dC[0][0:7])
    plt.show()
    
    plt.imshow(normC)
    plt.colorbar()
    plt.show()
    
    # return(D)

def testGauss():
    nx = 5
    ny = 5

    mu1 = 0
    sigma1 = 1
        
    G1 = gauss2D(nx,ny,mu1,sigma1)
    
    mu2 = 0
    sigma2 = 0.5
    
    G2 = gauss2D(nx,ny,mu2,sigma2)
    
    # print(G1)
    
    testCarray(G1,G1)
    
    
def test():
    a = np.pi/6
    n = 100
    sigma = 1
    
    gauss(a,n,sigma)
    
    
def testCoherence():
    from wpg.generators import build_gauss_wavefront
    from wpg.wavefront import Wavefront
    try:
        from wpg.srw import srwlpy as srwl
    except ImportError:
        import srwlpy as srwl
    from usefulWavefield import getComplex
    from useful import fromPickle, sampleField, round_sig
    
    eMin = 50e6
    Nx = 75
    Ny = 75
    Nz = 1
    xMin = -10e-6
    xMax = 10e-6
    yMin = -10e-6
    yMax = 10e-6
    zMin = 1000
    Fx = 1/10
    Fy = 1/10
    print('Running Test:')
    print('building wavefront...')
    w1 = build_gauss_wavefront(Nx,Ny,Nz,eMin/1000,xMin,xMax,yMin,yMax,1,3e-6,3e-6,1) 
    w2 = build_gauss_wavefront(Nx,Ny,Nz,eMin/1000,xMin,xMax,yMin,yMax,1,2e-7,2e-7,1) 
    
    wf1 = Wavefront(srwl_wavefront=w1)
    wf2 = Wavefront(srwl_wavefront=w2)
    
    # wf = wf0.toComplex()
    
    """From pickled wavefield """
    path = '/home/jerome/Documents/MASTERS/data/YDStest/13nm/' #wavefieldME_TEST_500um_.pkl' #'/home/jerome/dev/wavefieldME_TEST_500um_.pkl'
    waveName = path + 'wavefieldME_TEST_50um_.pkl'
    print("-----Loading Wavefield-----")
    wf = fromPickle(waveName)
    wf = Wavefront(srwl_wavefront=wf)
    extra = "_200nm"
    pathI = path + "Intensity" + extra + ".png" # Save path for horizontal coherence profile plot
    pathCpX = path + "CpX" + extra + ".png" # Save path for horizontal coherence profile plot
    pathCpY = path + "CpY" + extra + ".png" # Save path for vertical coherence profile plot
    pathWX = path + "WX" + extra + ".png" # Save path for horizontal complex wavefield plot
    pathWY = path + "WY" + extra + ".png" # Save path for vertical complex wavefield plot
    
    
    pathCP = path + "CoherenceProfile" + extra + ".png" # Save path for horizontal/vertical mutual intensity profiles
    pathJP = path + "MutualIntensityPlots" + extra + ".png" # Save path for Mutual Intensity plots
    pathJ = path + "MutualIntensity" + extra + ".png" # Save path for Mutual Intensity

    """Coherence from pyplot """
    #coherenceProfiles(wf,
    #                  pathI, pathCpX, pathCpY, pathWX, pathWY)

    cw1 = getComplex(wf1)
    cw2 = getComplex(wf2)
    cwH = getComplex(wf1,'horizontal')
    cwV = getComplex(wf1,'vertical')
    I = wf1.get_intensity()
    cX = cw1[:,int(int(np.max(np.shape(cw1[:,0,0])))/2)]
    cY = cw1[int(int(np.max(np.shape(cw1[0,:,0])))/2),:]
    Ix = I[:,int(int(np.max(np.shape(I[:,0,0])))/2)]
    Iy = I[int(int(np.max(np.shape(I[0,:,0])))/2),:]
    
    """Mutual Intensity """
    
    
    A_T1 = sampleField(cw1, Fx=Fx, Fy=Fy, limit = 1000, verbose=True, show=True)
    A_T2 = sampleField(cw2, Fx=Fx, Fy=Fy, limit = 1000)#, verbose=True, show=True)
    
    C = testCarray(A_T1, A_T2)
    
    plt.imshow(abs(C)/abs(np.sqrt(np.squeeze(A_T1)**2)))
    plt.title('C by convolution')
    plt.colorbar()
    plt.show()
    
    plt.imshow(abs(A_T1))
    plt.colorbar()
    plt.show()
    plt.imshow(abs(A_T2))
    plt.colorbar()
    plt.show()
    
    # profileMI(np.squeeze(cX),np.squeeze(cY), verbose=True, show=True)
    # mutualIntensity(cw,cwH,cwV, Fx=Fx, Fy=Fy, verbose=True, show=True)#, pathCP, pathJP, pathJ)
    
    
def testConvolve():
    from scipy import signal
    from scipy import misc
    ascent = misc.ascent()
    scharr = np.array([[ -3-3j, 0-10j,  +3 -3j],
                       [-10+0j, 0+ 0j, +10 +0j],
                       [ -3+3j, 0+10j,  +3 +3j]]) # Gx + j*Gy
    grad = signal.convolve2d(ascent, scharr, boundary='symm', mode='same')
    import matplotlib.pyplot as plt
    fig, (ax_orig, ax_mag, ax_ang) = plt.subplots(3, 1, figsize=(6, 15))
    ax_orig.imshow(ascent, cmap='gray')
    ax_orig.set_title('Original')
    ax_orig.set_axis_off()
    ax_mag.imshow(np.absolute(grad), cmap='gray')
    ax_mag.set_title('Gradient magnitude')
    ax_mag.set_axis_off()
    ax_ang.imshow(np.angle(grad), cmap='hsv') # hsv is cyclic, like angles
    ax_ang.set_title('Gradient orientation')
    ax_ang.set_axis_off()
    fig.show()
if __name__ == '__main__':
    # testGauss()
    testCoherence()
    # testConvolve()