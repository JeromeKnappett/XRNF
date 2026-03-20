#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 16 14:20:09 2021

@author: jerome
"""
import matplotlib.pyplot as plt
import numpy as np

from matplotlib.pyplot import figure
figure(figsize=(8, 6), dpi=80)
plt.style.use(['science','no-latex']) # 'ieee', 

def TMvisibility(wl,p):
    """wl: wavelength
     p: grating pitch
     
     returns - V: Fringe Visibility"""
     
    V = 1 - 2*((wl**2)/(p**2))
    
    return V

def constant_function(x):
    return np.full(x.shape,1)


def imageDistance(d, l, p, m=1):
    
    return d/(2*np.tan(np.arcsin(((m*l)/(p)))))

def testImageDistance():
    
    p = range(20,100) # grating pitch [10e-9, 14e-9, 18e-9, 22e-9, 26e-9, 30e-9, 34e-9, 38e-9] 
    l1 = 6.710553853647976e-9 #wl(0.18476)                        # wavelength
    l2 = 13.708999668288369e-9 #wl(0.09044)                       # wavelength
    d0 = 100e-6 #23.75e-6                                          # grating separation
    s = [60, 50,  40, 30, 20, 10, 5]                                  # grating size
    
    d =[100, 80, 60, 40, 20, 1]   # [100, 90, 80, 70, 60, 50, 40, 30, 20, 10]   
    s0 = 10e-6
    
    
    
    """ Calculating and plotting aerial image distances as function of grating dimension """
    Z1min = [[] for b in range(len(s))]
    Z1mid = [[] for b in range(len(s))]
    Z1max = [[] for b in range(len(s))]
    Z2min = [[] for b in range(len(s))]
    Z2mid = [[] for b in range(len(s))]
    Z2max = [[] for b in range(len(s))]
    
    for i in p:
        for j, k in enumerate(s):
            
            z1Min = imageDistance(d0-((k*1e-6)/2),l1,i*1e-9)
            z1Mid = imageDistance(d0,l1,i*1e-9)
            z1Max = imageDistance(d0+((k*1e-6)/2),l1,i*1e-9)
            z2Min = imageDistance(d0-((k*1e-6)/2),l2,i*1e-9)
            z2Mid = imageDistance(d0,l2,i*1e-9)
            z2Max = imageDistance(d0+((k*1e-6)/2),l2,i*1e-9)
            
            Z1min[j].append(z1Min)
            Z1mid[j].append(z1Mid)
            Z1max[j].append(z1Max)
            Z2min[j].append(z2Min)
            Z2mid[j].append(z2Mid)
            Z2max[j].append(z2Max)
        
    
    
    for i, l in enumerate(s):
        Zmin = np.array(Z1min[i])*1e3
        Zmax = np.array(Z1max[i])*1e3
        plt.fill_between(p,Zmin, Zmax, label=str(l)+"\u03bcm")
        plt.title("\u03BB = 6.7 nm" + " Grating separation = " + str(d0*1e6) + "\u03bcm")
        plt.xlabel("Grating Pitch [nm]")
        plt.ylabel("Aerial Image Distance [mm]")#" [\u03bcm]")    
        # plt.legend()
    plt.plot(p,np.array(Z1mid[0])*1e3, ':', color = 'black')#, label="Optimal Position")
    plt.ylim(bottom=0,top=np.max(np.array(Z1max)*1e3))
    plt.legend(loc='upper left',title="Grating Size")
    plt.show()
    plt.clf()
    plt.close()
    
    figure(figsize=(8, 6), dpi=80)
    for i, l in enumerate(s):
        Zmin = np.array(Z2min[i])*1e3
        Zmax = np.array(Z2max[i])*1e3
        plt.fill_between(p,Zmin, Zmax, label=str(l)+"\u03bcm")
        # plt.fill_between(p,Z2min[i]*1e3, Z2max[i]*1e3, label=str(l)+"\u03bcm")
        plt.title("\u03BB = 13.5 nm" + " Grating separation = "  + str(d0*1e6) + "\u03bcm")
        plt.xlabel("Grating Pitch [nm]")
        plt.ylabel("Aerial Image Distance [mm]")#[\u03bcm]")    
        # plt.legend()
    plt.plot(p,np.array(Z2mid[0])*1e3, ':', color = 'black')#, label="Optimal Position")
    plt.ylim(bottom=0,top=np.max(np.array(Z1max)*1e3))
    plt.legend(loc='upper left', title="Grating Size")
    plt.show()
    plt.clf()
    plt.close()
    
    
        
    figure(figsize=(8, 6), dpi=80)
    for i, l in enumerate(s):
        Zmin_1 = np.array(Z1min[i])*1e3
        Zmax_1 = np.array(Z1max[i])*1e3
        plt.fill_between(p,Zmin_1, Zmax_1, label=str(l)+"\u03bcm")#" - 6.7 nm")
#        plt.title("\u03BB = 6.7 nm" + " Grating separation = " + str(d0*1e6) + "\u03bcm")
#        plt.xlabel("Grating Pitch [nm]")
#        plt.ylabel("Aerial Image Distance [mm]")#" [\u03bcm]")    
        # plt.legend()
    
    for i, l in enumerate(s):
        Zmin_2 = np.array(Z2min[i])*1e3
        Zmax_2 = np.array(Z2max[i])*1e3
        plt.fill_between(p,Zmin_2, Zmax_2)#, label=str(l)+"\u03bcm - 13.5 nm")
        # plt.fill_between(p,Z2min[i]*1e3, Z2max[i]*1e3, label=str(l)+"\u03bcm")
        plt.title(" Grating separation = "  + str(d0*1e6) + "\u03bcm")
        plt.xlabel("Grating Pitch [nm]")
        plt.ylabel("Aerial Image Distance [mm]")#[\u03bcm]")    
        # plt.legend()
    plt.plot(p,np.array(Z1mid[0])*1e3, ':', color = 'black')#, label="Optimal Position")
    plt.plot(p,np.array(Z2mid[0])*1e3, ':', color = 'black')#, label="Optimal Position")
    plt.ylim(bottom=0,top=np.max(np.array(Z1max)*1e3))
    plt.legend(loc='upper left', title="Grating Size")
    plt.show()
    plt.clf()
    plt.close()
    
    
    
    """ Calculating and plotting aerial image distances as function of grating separation """
    _Z1min = [[] for b in range(len(d))]
    _Z1mid = [[] for b in range(len(d))]
    _Z1max = [[] for b in range(len(d))]
    _Z2min = [[] for b in range(len(d))]
    _Z2mid = [[] for b in range(len(d))]
    _Z2max = [[] for b in range(len(d))]
    
    for i in p:
        for j, k in enumerate(d):
            
            z1Min = imageDistance(k*1e-6-(s0/2),l1,i*1e-9)
            z1Mid = imageDistance(k*1e-6,l1,i*1e-9)
            z1Max = imageDistance(k*1e-6+(s0/2),l1,i*1e-9)
            z2Min = imageDistance(k*1e-6-(s0/2),l2,i*1e-9)
            z2Mid = imageDistance(k*1e-6,l2,i*1e-9)
            z2Max = imageDistance(k*1e-6+(s0/2),l2,i*1e-9)
            
            _Z1min[j].append(z1Min)
            _Z1mid[j].append(z1Mid)
            _Z1max[j].append(z1Max)
            _Z2min[j].append(z2Min)
            _Z2mid[j].append(z2Mid)
            _Z2max[j].append(z2Max)
        
    
    
    figure(figsize=(8, 6), dpi=80)
    for i, l in enumerate(d):
        Zmin = np.array(_Z1min[i])*1e3
        Zmax = np.array(_Z1max[i])*1e3
        plt.fill_between(p,Zmin, Zmax, label=str(l)+"\u03bcm")
        plt.title("\u03BB = 6.7 nm" + " Grating size = " + str(s0*1e6) + "\u03bcm")
        plt.xlabel("Grating Pitch [nm]")
        plt.ylabel("Aerial Image Distance [mm]")#[\u03bcm]")    
        # plt.legend()
    # plt.plot(p,np.array(_Z1mid[0])*1e3, ':', color = 'black', label="Optimal Position")
    plt.ylim(bottom=0,top=np.max(np.array(_Z1max)*1e3))
    plt.legend(loc='upper left', title="Grating Separation")
    plt.show()
    plt.clf()
    plt.close()
    
    figure(figsize=(8, 6), dpi=80)
    for i, l in enumerate(d):
        Zmin = np.array(_Z2min[i])*1e3
        Zmax = np.array(_Z2max[i])*1e3
        plt.fill_between(p,Zmin, Zmax, label=str(l)+"\u03bcm")
        # plt.fill_between(p,Z2min[i]*1e3, Z2max[i]*1e3, label=str(l)+"\u03bcm")
        plt.title("\u03BB = 13.5 nm" + " Grating size = " + str(s0*1e6) + "\u03bcm") #"\u03bcm"
        plt.xlabel("Grating Pitch [nm]")
        plt.ylabel("Aerial Image Distance [mm]")#[\u03bcm]")    
        # plt.legend()
    # plt.plot(p,np.array(_Z2mid[0])*1e3, ':', color = 'black', label="Optimal Position")
    plt.ylim(bottom=0,top=np.max(np.array(_Z1max)*1e3))
    plt.legend(loc='upper left', title="Grating Separation")
    plt.show()
    plt.clf()
    plt.close()
    
    
    
#    for i, l in enumerate(d):
#        plt.clf()
#        plt.close()
#        fig, axs = plt.subplots(2, 1)

#        Zmin1 = np.array(_Z1min[i])*1e3
#        Zmax1 = np.array(_Z1max[i])*1e3
#        axs[0].fill_between(p,Zmin1, Zmax1, label=str(l)+"\u03bcm")
#        axs[0].set_title("\u03BB = 6.7 nm" + " Grating size = " + str(s0*1e6) + "\u03bcm")
#        axs[0].set_xlabel("Grating Pitch [nm]")
#        axs[0].set_ylabel("Aerial Image Distance [mm]")#[\u03bcm]")    
#        
#        Zmin1 = np.array(_Z2min[i])*1e3
#        Zmax1 = np.array(_Z2max[i])*1e3
#        axs[1].fill_between(p,Zmin1, Zmax1, label=str(l)+"\u03bcm")
#        # plt.fill_between(p,Z2min[i]*1e3, Z2max[i]*1e3, label=str(l)+"\u03bcm")
#        axs[1].set_title("\u03BB = 13.5 nm" + " Grating size = " + str(s0*1e6) + "\u03bcm") ##"\u03bcm"
#        axs[1].set_xlabel("Grating Pitch [nm]")
#        axs[1].set_ylabel("Aerial Image Distance [mm]")#[\u03bcm]")    
#        # plt.legend()
#    plt.ylim(bottom=0)
#    # plt.legend(loc='upper left', title="Grating Separation")
#    plt.show()
#    plt.clf()
#    plt.close()
    
    

    
    D = np.linspace(1,100,100)
    D1 = D + 10
    D2 = D + 20
    D3 = D + 30
    D4 = D + 40
    P = np.linspace(20,100,100)
    S = np.linspace(1,100,100)
    
    print("Shape of D: {}".format(np.shape(D)))
    print("Shape of P: {}".format(np.shape(P)))
    print("Shape of S: {}".format(np.shape(S)))
#    z = imageDistance(D*1e-6, l1, P*1e-9)

#    print("Shape of z: {}".format(np.shape(z)))
    
#    print("D: {}".format(D))
#    print("P: {}".format(P))
#    print("z: {}".format(z))
    
    
    from mpl_toolkits import mplot3d


    plt.rcParams['legend.fontsize'] = 10
    fig = plt.figure(figsize=(8,8), dpi=80)
    ax = fig.add_subplot(111, projection='3d')
    
    X, Y = np.meshgrid(D, P)
#    X1, Y = np.meshgrid(D1, P)
#    X2, Y = np.meshgrid(D2, P)
#    X3, Y = np.meshgrid(D3, P)
#    X4, Y = np.meshgrid(D4, P)
    z = imageDistance(X*1e-6, l1, Y*1e-9)
    z1 = imageDistance(X*1e-6+(100e-6/2), l1, Y*1e-9)
    z2 = imageDistance(X*1e-6-(100e-6/2), l1, Y*1e-9)
    z3 = imageDistance(X*1e-6+(10e-6/2), l1, Y*1e-9)
    z4 = imageDistance(X*1e-6-(10e-6/2), l1, Y*1e-9)
    z5= imageDistance(X*1e-6+(20e-6/2), l1, Y*1e-9)
    z6 = imageDistance(X*1e-6-(20e-6/2), l1, Y*1e-9)
    z7 = imageDistance(X*1e-6+(30e-6/2), l1, Y*1e-9)
    z8 = imageDistance(X*1e-6-(30e-6/2), l1, Y*1e-9)
    z9 = imageDistance(X*1e-6+(40e-6/2), l1, Y*1e-9)
    z10 = imageDistance(X*1e-6-(40e-6/2), l1, Y*1e-9)
#    z11 = imageDistance(X*1e-6+(50e-6/2), l1, Y*1e-9)
#    z12 = imageDistance(X*1e-6-(50e-6/2), l1, Y*1e-9)
#    z3 = imageDistance(X3*1e-6, l1, Y*1e-9)
#    z4 = imageDistance(X4*1e-6, l1, Y*1e-9)
#    ax.plot3D(X,Y,z)
    # print(z[0])
    # for i, j in zip(range(0,len(D)), range(0,len(P))):
    #     if z[i,j] < 0:
    #         z[i,j] = None
    #     if z1[i,j] < 0:
    #         z1[i,j] = None
    #     if z2[i,j] < 0:
    #         z2[i,j] = None
    #     if z3[i,j] < 0:
    #         z3[i,j] = None
    #     if z4[i,j] < 0:
    #         z4[i,j] = None
    #     if z5[i,j] < 0:
    #         z5[i,j] = None
    #     if z6[i,j] < 0:
    #         z6[i,j] = None
    #     if z7[i,j] < 0:
    #         z7[i,j] = None
    #     if z8[i,j] < 0:
    #         z8[i,j] = None
    #     if z9[i,j] < 0:
    #         z9[i,j] = None
    #     if z10[i,j] < 0:
    #         z10[i,j] = None
    #     else:
    #         pass

    
#ax.plot_surface(X, Y, Z, color='darkorange', alpha=0.8)
    img1 = ax.plot_surface(X, z*1e3, Y,  alpha=1, color='grey', label = "Ideal")
    img1._facecolors2d=img1._facecolor3d
    img1._edgecolors2d=img1._edgecolor3d
    img2 = ax.plot_surface(X, z3*1e3, Y,  alpha=1, color='purple', label="10 mictrons")
    img2._facecolors2d=img2._facecolor3d
    img2._edgecolors2d=img2._edgecolor3d
    img3 = ax.plot_surface(X, z4*1e3, Y,  alpha=1, color='purple')
    img3._facecolors2d=img3._facecolor3d
    img3._edgecolors2d=img3._edgecolor3d
    img4 = ax.plot_surface(X, z5*1e3, Y,  alpha=1, color='red', label="20 microns")
    img4._facecolors2d=img4._facecolor3d
    img4._edgecolors2d=img4._edgecolor3d
    img5 = ax.plot_surface(X, z6*1e3, Y,  alpha=1, color='red')
    img5._facecolors2d=img5._facecolor3d
    img5._edgecolors2d=img5._edgecolor3d
    img6 = ax.plot_surface(X, z7*1e3, Y,  alpha=1, color='orange', label="30 microns")
    img6._facecolors2d=img6._facecolor3d
    img6._edgecolors2d=img6._edgecolor3d
    img7 = ax.plot_surface(X, z8*1e3, Y,  alpha=1, color='orange')
    img7._facecolors2d=img7._facecolor3d
    img7._edgecolors2d=img7._edgecolor3d
    img8 = ax.plot_surface(X, z9*1e3, Y,  alpha=1, color='green', label="40 microns")
    img8._facecolors2d=img8._facecolor3d
    img8._edgecolors2d=img8._edgecolor3d
    img9 = ax.plot_surface(X, z10*1e3, Y,  alpha=1, color='green')
    img9._facecolors2d=img9._facecolor3d
    img9._edgecolors2d=img9._edgecolor3d
    img10 = ax.plot_surface(X, z1*1e3, Y,  alpha=1, color='blue', label="100 microns")
    img10._facecolors2d=img10._facecolor3d
    img10._edgecolors2d=img10._edgecolor3d
    img11 = ax.plot_surface(X, z2*1e3, Y,  alpha=1, color='blue')
    img11._facecolors2d=img11._facecolor3d
    img11._edgecolors2d=img11._edgecolor3d
#    img2 = ax.plot_surface(X, z11*1e3, Y,  alpha=1, color='blue', label="100 microns")
#    img2._facecolors2d=img2._facecolor3d
#    img2._edgecolors2d=img2._edgecolor3d
#    img3 = ax.plot_surface(X, z12*1e3, Y,  alpha=1, color='blue')
#    img3._facecolors2d=img3._facecolor3d
#    img3._edgecolors2d=img3._edgecolor3d

#    
#    fill_between_3d(ax, *set1, *set2, mode = 1)
    ax.set_xlabel('Grating Separation [um]')
    ax.set_ylabel('Aerial Image Distance [mm]')
    ax.set_zlabel('Pitch [nm]')
    ax.set_ylim3d(bottom=0)
    ax.view_init(20, -40)
    
    
    ax.legend()
    plt.show()
    
#    ax.contour3D(P, D, z, 50, cmap='binary')
#    print("Saving 3D plot to: " +  "/data/experiments/plots/3Ddistance.png")
#    plt.savefig("/data/experiments/plots/3Ddistance.png")
    plt.clf()
    plt.close()
    
    
    # print("Distance for 6.7 nm wavelength (pitch, distance):")
    # print((p,Z1))
    
    # print("Distance for 13.7 nm wavelength (pitch, distance):")
    # print((p,Z2))
    


def test():
    BEUV = 6.7 # wavelength
    EUV = 13.5
    Vbeuv = []
    Veuv = []
    
    p = range(10,120,1)
    
    for i in p:
        Vbeuv.append(TMvisibility(BEUV,i))
        Veuv.append(TMvisibility(EUV,i))
        # print("Grating pitch: {}".format(i))
        # print("Fringe visibility: {}".format(V))


    plt.plot(p,Vbeuv, label="TM - 6.7 nm")
    plt.plot(p,Veuv, label="TM - 13.5 nm")
    plt.plot(p, constant_function(np.array(p)), label="TE")
    plt.ylabel("Fringe Visibility")
    plt.xlabel("Grating Pitch [nm]")
    plt.ylim(0,1.05)
    plt.legend()
    plt.show()
    
if __name__ == '__main__':
    # test()
    testImageDistance()
    
    
     
