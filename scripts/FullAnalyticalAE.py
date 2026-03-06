
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 15:24:08 2025

@author: jerome
"""

"""
The following functions are taken from the supporting information from
'Development of EUV interference lithography for 25 nm line/space patterns',
A.K Sahoo et al.

"""

import numpy as np
import matplotlib.pyplot as plt
import pickle
import tifffile
import plotting
from NILS import calculate_mean_nils

def wl(E):
        #return wavelength for energy E in keV
        return  12.39e-10/E


def opticalAxisIntercept(d, l, offset, theta=0, m = 1):
    """ return distance from grating plane at which m= 1 order intercepts optical axis
    when grating is displaced by 'offset' from optical axis."""
    
    #tan theta = d / offset   CHECK THIS  46r
    #return offset*np.tan(diffractionAngle(d,l,theta,m))
    return offset / (2*np.tan(diffractionAngle(d,l,theta,m)))


def diffractionAngle(wl, p, phi=0, m = 1):
    # Use grating equation to determine diffraction angle  
    # (m = order; l = lambda, wavelength; d = spacing)
    theta = np.arcsin(np.sin(phi) + m*wl/p)
    return theta

def aerialImageDistance(d,p,m,wl):
    z = (d*np.sqrt((p**2) - ((m**2)*(wl**2))))/(2*m*wl)
    return z

def EfromTiffs(files, mid=None, N=1000, n=1):
    if mid == None:
        mid = [(int(np.shape(f)[0] / 2), int(np.shape(f)[1] / 2)) for f in files]

    EhR = [tifffile.imread(f + "ExReal.tif") for f in files]
    EvR = [tifffile.imread(f + "EyReal.tif") for f in files]
    EhI = [tifffile.imread(f + "ExIm.tif") for f in files]
    EvI = [tifffile.imread(f + "EyIm.tif") for f in files]

    imagesEhR = [t[m[0] - n : m[0] + n, m[1] - N : m[1] + N] for t, m in zip(EhR, mid)]
    imagesEvR = [t[m[0] - n : m[0] + n, m[1] - N : m[1] + N] for t, m in zip(EvR, mid)]
    imagesEhI = [t[m[0] - n : m[0] + n, m[1] - N : m[1] + N] for t, m in zip(EhI, mid)]
    imagesEvI = [t[m[0] - n : m[0] + n, m[1] - N : m[1] + N] for t, m in zip(EvI, mid)]

    # method
    Eh = [ExR + ExI * 1j for ExR, ExI in zip(imagesEhR, imagesEhI)]
    Ev = [EyR + EyI * 1j for EyR, EyI in zip(imagesEvR, imagesEvI)]  # EvR + EvI*1j
    cE = [Ex + Ey for Ex, Ey in zip(Eh, Ev)]  # Eh + Ev
    return cE

def aerialImageE(E1a,E2a,E1p,E2p,E3,k,theta,x,w,t,show=True):
    
    E1 = E1a * np.exp((1j * k * x * np.sin(theta)) - (w*t) - E1p)
    E2 = E2a * np.exp((-1j * k * x * np.sin(theta)) - (w*t) - E2p)
    
    # E3 = E3a * np.exp((1j * k * x) - (w*t) - E3p)
    
    E = E1 + E2# + E3
    
    I = abs(E**2)
    
    if show:
        plt.plot([a*1e6 for a in x],I)
#        plt.plot([a*1e6 for a in x],abs(E3**2))
#        plt.plot([a*1e6 for a in x],np.angle(E3)/np.pi)
        plt.xlabel('x [nm]')
        plt.ylabel('I [a.u]')
        # plt.ylim(0,1)
        plt.show()
    
    return E,I
#    print(I)

def aerialImageETE(E1a,E2a,E3,E1p,E2p,k,theta,x,z,show=True):
    
    E1 = E1a * np.exp(1j * ((k * x * np.sin(theta)) - (k * z * np.cos(theta))) - E1p)
    E2 = E2a * np.exp(1j * ((-k * x * np.sin(theta)) - (k * z * np.cos(theta))) - E2p)
    
    
    E = E1 + E2# + E3
    
    I = abs(E**2)
    
    if show:
        plt.plot([a*1e6 for a in x],I)
#        plt.plot([a*1e6 for a in x],abs(E3**2))
#        plt.plot([a*1e6 for a in x],np.angle(E3)/np.pi)
        plt.xlabel('x [nm]')
        plt.ylabel('I [a.u]')
        # plt.ylim(0,1)
        plt.show()
    
    return E,I

def analyticalAE(x,A1,A2,AT,pT,wT,k,theta,z,R):
    # a = k*x*np.sin(theta)
    # b = z + ((x**2)/(2*R))
    # c = -pT - ((x**2)/(wT**2))
    
    I = (A1**2 + A2**2 + (AT**2)*np.exp(2*(-pT - ((x**2)/(wT**2)))) + 
         2*A1*A2*np.cos(2*(k*x*np.sin(theta))) + 
         2*A1*AT*np.exp((-pT - ((x**2)/(wT**2))))*np.cos((k*x*np.sin(theta))+(z + ((x**2)/(2*R)))) + 
         2*A2*AT*np.exp((-pT - ((x**2)/(wT**2))))*np.sin((k*x*np.sin(theta))+(z + ((x**2)/(2*R)))))
    
    return I

def test():
    path = "/home/jerome/dev/data/correctedBlockDiffraction/"
    savePath = None #path + "AE_ap_tran_sim_large.pdf"
    fmat = 'pdf'

    # res and middle pixels of images
    res = [
        (4.832552851219838e-09, 3.853038352405723e-07),
        (4.832457034313024e-09, 3.8431154968763494e-07),
    ]
    mid = [(196, 19887), (96, 7405)]

    N = 1000  # number of pixels to take for line profile  - 1200 for roughness aerial images
    n = 1  # number of pixels to average over for line profile - 15 for roughness aerial images
    plotRange = 5000  # range of aerial image plot in nm

    files = ["apertureDiffraction", "blockDiffraction"]

    fileNames = [path + f for f in files]

    c = 299792458
    E10 = 0.50    # E10 + E20 = 1.0
    E20 = 0.50 
    E30 = 0.02 #0.83 #75/100 # value of transmission through mask in Masters thesis
    E1p = 0 * 1/2 * np.pi
    E2p = 0*np.pi
    E3p = (1)*np.pi
    wl = 6.7e-9 # 13.5e-9 #6.7e-9
    k = (2*np.pi)/wl
    p = 200.0e-9
    theta = diffractionAngle(wl,p)
    w=c*k#1/wl
#    mu = 0.8

#    These work when pitch is halved
#    scaleT = 10e6
#    scaleAE = 2.5e5

    scaleT = 5e6
    scaleAE = scaleT #2.5e5
    Show = False

    xR = N*res[0][0]
    
    x = np.linspace(-xR,xR,2*N)
    
    z = aerialImageDistance(100e-6, p=p, m=1, wl=wl)
    t =  0*z/c
    
    ratio_sum = E10 + E20
    E1a = E10 / ratio_sum * (1 - E30)
    E2a = E20 / ratio_sum * (1 - E30)
    E3a = E30
    
    # Wo = 10.0e-6
    Wz = 3000.0e-6   #beam size at z (1/e^2)
    R = 15.5         #radius of curvature
    Z = 9.5          #propagation distance from waist
    
    # E3 = E3a * np.exp((-1j * k * x) - E3p)
    # E3 = E3a * np.exp(-1j * ((k*Z) + (k * ((x**2)/(2*R))) - E3p))
    E3 = E3a * np.exp((-(x**2))/((Wz**2))) * np.exp(-1j * ((k*Z) + (k * ((x**2)/(2*R))) - E3p))     
    E32d = np.tile(E3,(2*n,1))
    
    Ea,Ia = aerialImageE(E1a,E2a,E1p,E2p,E3,k,theta,x,w,t,show=Show)
    Eb,Ib = aerialImageETE(E1a, E2a, E3, E1p, E2p, k, theta, x, z,show=Show)
    Ea2d = np.tile(Ea,(2*n,1))
    Eb2d = np.tile(Eb,(2*n,1))

    Et = EfromTiffs(fileNames, mid, N, n)

    resAE = (2.5011882651601634e-09, 2.426754806976689e-07)
    midAE = (196, 12188)
    
    Es = [Et[0],Et[1],E32d,Ea2d,Eb2d]
#    for i,e in enumerate(Es):
#        prof = abs((e.mean(0)/np.max(e))**2)
#        plt.plot(x,prof/np.max(prof),label=str(i+1))
#    plt.legend()
#    plt.show()
#
    
    print([np.shape(e) for e in Es])
#
    I_T = abs(E32d**2)
    I_ap = abs((Et[0])**2)
    I_ap_T = abs((Et[0] + scaleT*E32d)**2)
    I_AE_ap_s = abs((Ea2d*scaleAE + Et[0])**2)
    I_AE_ap_w = abs((Eb2d*scaleAE + Et[0] + Et[1])**2)
    I_AE_T_s = abs((Ea2d*scaleAE + scaleT*E32d)**2)
    I_AE_T_w = abs((Eb2d*scaleAE + scaleT*E32d)**2)
    I_AE_ap_T_s = abs((Ea2d*scaleAE + Et[0] + Et[1] + scaleT*E32d)**2)
    I_AE_ap_T_w = abs((Ea2d*scaleAE + Et[0] + Et[1] + scaleT*E32d)**2)
#
    
#    pick = pickle.load(open('/home/jerome/dev/data/correctedBlockDiffraction/50um_50SSA.pkl', 'rb'))
#    tiffAE = pick[0]
#    resAE = (pick[1],pick[2])
#    midAE = np.shape(tiffAE)[0]//2, np.shape(tiffAE)[1]//2 - 93
    I1 = np.sum(abs(Ea**2))
    I2 = np.sum(abs(Eb**2))
    I3 = np.sum(abs(E3**2))
    
    print('Total I1:   ', I1)
    print('Total I2:   ', I2)
    print('Total IT:   ', I3)

    print("% contamination: ", 100*(I3/(I1 + I2 + I3)))
    
    tiffAE = tifffile.imread("/home/jerome/dev/data/aerialImages/imagePlaneintensity.tif")
    imageAE = tiffAE[midAE[0] - n : midAE[0] + n, midAE[1] - 2 * N : midAE[1] + 2 * N]
    profileAE = imageAE.mean(0)
    xAE = np.linspace(-2 * N * resAE[0], 2 * N * resAE[0], 4 * N)
    xP = [np.linspace(-N * r[0], N * r[0], 2 * N) for r in res]
    yP = [np.linspace(-n * r[1], n * r[1], 2 * n) for r in res]

#    Isum = I[0] + I[1]

    Itot = [
#            I_T,
            I_ap,
            I_ap_T,
#            I_AE_ap_s,
#            I_AE_T_s,
#            I_AE_ap_w,
#            I_AE_T_w,
#            I_AE_ap_T_s,
            I_AE_ap_T_w,
            imageAE
            ]
#    [I[0], imageAE, I[1], Isum]
    midTOT = [(196, 19887), (96, 7405), (196, 12188)]
    # 1D PLOT
    profs = [i.mean(0) / np.max(i) for i in Itot]
    
    titles = [
#        "Transmission",
        "Aperture",
        "Aperture + Transmission",
        "Aperture + AE (Sahoo)",
#        "Aperture + AE (Wang)",
#        "Transmission + AE (Sahoo)",
        "Aperture + Transmission + AE (Sahoo)",
        "Aperture + AE + Transmission (Wang)",
        "AE (simulated)",
#        "Two-Grating Mask Model",
#        "Photon Block Mask Layer",
#        "Summed",
    ]
    
    print([np.shape(i) for i in Itot])
    print([np.shape(i) for i in profs])
    
    
##    for i,p in enumerate(profs):
##        plt.plot(xP[0],p,label=titles[i])
    plt.plot([_x*1e9 for _x in xP[0]],profs[0],'r',label='Aperture')
    plt.plot([_x*1e9 for _x in xP[0]],profs[1],'b',label='Aperture+Transmission')
#    plt.plot([_x*1e9 for _x in xP[0]],profs[2],'--',label='Sahoo + Aperture')
#    plt.plot([_x*1e9 for _x in x],profs[3],'--',label='Wang + Aperture')
#    plt.plot([_x*1e9 for _x in x],profs[4],label='Sahoo + A + T')
#    plt.plot([_x*1e9 for _x in x],profs[2],label='Wang + A + T')
#    plt.plot([_x*1e9 for _x in x],abs(Ea**2),label='Sahoo')
#    plt.plot([_x*1e9 for _x in x],abs(Eb**2),label='Wang')
    plt.plot([_x*1e9 for _x in xAE],profileAE/np.max(profileAE),'gray',alpha=0.7,label="AE (simulated)")
    plt.legend()
    plt.xlim(-plotRange,plotRange)
    if savePath:
        plt.savefig(savePath, format=fmat)
    plt.show()
#    
    resTOT = [
#        (x[1]-x[0],x[1]-x[0]),
        (4.832552851219838e-09, 3.853038352405723e-07),
#        (x[1]-x[0],x[1]-x[0]),
#        (x[1]-x[0],x[1]-x[0]),
        (x[1]-x[0],x[1]-x[0]),
        (x[1]-x[0],x[1]-x[0]),
#        (x[1]-x[0],x[1]-x[0]),
        (2.5011882651601634e-09, 2.426754806976689e-07),
#        (4.832552851219838e-09, 3.853038352405723e-07),
    ]
    print((x[1]-x[0],x[1]-x[0]))
#    plotting.plotOneD(
#        profs,
#        d=[r[0] for r in resTOT],
#        sF=1e6,
#        xlim=[-plotRange/2, plotRange/2],
#        ylim=None,
#        describe=False,
#        split=None,
#        customX=[X * 1e9 for X in [xP[0],
##                                   xP[0],
##                                   xP[0],
#                                   xP[0],
##                                   xP[0],
#                                   xP[0],
##                                   xP[0],
#                                   xAE]],
#        title=None,
#        labels=titles,
#        xLabel=["Position [nm]"],
#        yLabel=["Intensity [a.u]"],  # [ph/s/.1\%bw/mm²]'],
#        aspct="auto",
#        lStyle=["-","-","--","--"],
#        lWidth=1,
#        pStyle="",
#        fSize=10,
#        figSize=(10,6),
#        dpi=100,
##        color=[0, 1, 3, 4],
##        savePath=savePath,
#    )
def testAnalyticalAEI():
    E10 = 0.40    # E10 + E20 = 1.0
    E20 = 0.60 
    E30 = 0.1 #0.83 #75/100 # value of transmission through mask in Masters thesis
    E1p = 0 * 1/2 * np.pi
    E2p = 0*np.pi
    E3p = 2.*np.pi
    wl = 6.7e-9 # 13.5e-9 #6.7e-9
    k = (2*np.pi)/wl
    p = 100.0e-9
    theta = diffractionAngle(wl,p)
    
    # Wo = 10.0e-6
    Wz = 1000.0e-6   #beam size at z (1/e^2)
    R = 0.05         #radius of curvature
    
    xR = 300e-9
    xN = 5000
    
    x = np.linspace(-xR/2,xR/2,xN)
    
    z = aerialImageDistance(100e-6, p=p, m=1, wl=wl)
    #1.5e-12 
    # range(0,10)
    # 0#1.0*1e-6
    # [(Z*1e-1)/c for Z in z]
    # z/c #1.0e-9
    
    pf = np.arange(0,1.01,0.1)
    
    P = [np.pi*f for f in pf]
    
    ratio_sum = E10 + E20
    E1a = E10 / ratio_sum * (1 - E30)
    E2a = E20 / ratio_sum * (1 - E30)
    E3a = E30
    
#    print(E1a,E2a,E30)
    for p in P:
        i = analyticalAE(x, E1a, E2a, E3a, p, Wz, k, theta, z, R)
        plt.plot([a*1e9 for a in x],i)
    plt.show()
    
    
    E3 = E3a #* np.exp((-(x**2))/((Wz**2))) * np.exp(-1j * ((k*z) + (k * ((x**2)/(2*R))) - E3p))
    
    Ea,Ia = aerialImageE(E1a,E2a,E1p,E2p,E3,k,theta,x,w=0,t=0)
#    Eb,Ib = aerialImageETE(E1a, E2a, E3, E1p, E2p, k, theta, x, z)
    
    Ia = abs(Ea + E3)**2
#    Ib = abs(Eb + E3)**2
    
    I = analyticalAE(x, E1a, E2a, E3a, E3p, Wz, k, theta, z, R)
    plt.plot([a*1e9 for a in x],I,label='Full Analytical')
    plt.plot([a*1e9 for a in x],Ia,label='Sahoo')
#    plt.plot([a*1e9 for a in x],Ib,label='Wang')
#    plt.plot([a*1e9 for a in x],abs(E3)**2)
    plt.legend()
    plt.show()
    
    I1 = np.sum(abs(Ea)**2)
#    I2 = np.sum(abs(Eb)**2)
    I3 = np.sum(abs(E3)**2)
    
    print('Total I1:   ', I1)
#    print('Total I2:   ', I2)
    print('Total IT:   ', I3)

    print("% contamination: ", 100*(I3/(I1 + I3)))
    
    nils = calculate_mean_nils(Ia, w=25.0e-9, dx=x[1] - x[0], debug_plot=True)
    
    print('mean nils: ', nils)
if __name__ == '__main__':
    testAnalyticalAEI()
#    test()