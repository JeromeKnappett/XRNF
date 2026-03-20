#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 10:40:11 2021

@author: jerome
"""
import numpy as np
import matplotlib.pyplot as plt
from wpg.generators import build_gauss_wavefront
from wpg.wavefront import Wavefront



from PIL import Image
from PIL import ImageDraw
import imageio

# plt.style.reload_library()
# plt.style.use(['science','no-latex'])#,'ieee'])

# %%
def gratingEfficiencyDEL(m,beta,delta,d,k,b,theta = 0):
    """ DOES NOT WORK - NEED TO CHECK """
    
    ''''
    Return the diffraction efficiency of X-rays incident on an arbitrary grating
    with rectangular wire cross sections (method from Delvaille et al. (1980)):
        m: order of diffracted beam
        beta: imaginary part of refractive index
        delta: (1-real part) of refractive index
        d: grating periodicity
        k: photon energy in units of (hbar*c)
        b: thickness of mask
        theta: incident angle
        
    '''
    a = d # square grating
    
    phi = (2*np.pi*m)/(d*np.cos(theta))
    print("phi: {}".format(phi))
    

    X_0 = 0
    X_1 = a*np.cos(theta) - b*np.sin(theta)
    X_2 = a*np.cos(theta)
    X_3 = d*np.cos(theta) - b*np.sin(theta)
    X_4 = d*np.cos(theta)
    
    Z_0 = 0
    Z_1 = 0
    Z_2 = b/np.cos(theta)
    Z_3 = b/np.cos(theta)
    
    C_0 = 0
    C_1 = 1/(np.sin(theta)*np.cos(theta))
    C_2 = 0
    C_3 = -1/(np.sin(theta)*np.cos(theta))
    
    R_0 = (1/k)*(((C_0*k*beta)**2 + (k*C_0*delta + phi)**2)**(1/2))
    R_1 = (1/k)*(((C_1*k*beta)**2 + (k*C_1*delta + phi)**2)**(1/2))
    R_2 = (1/k)*(((C_2*k*beta)**2 + (k*C_2*delta + phi)**2)**(1/2))
    R_3 = (1/k)*(((C_3*k*beta)**2 + (k*C_3*delta + phi)**2)**(1/2))

    F_0 = (1/k*R_0)*np.exp(-1j*np.cos((beta*C_0)/R_0)+1j*k*(Z_0 - C_0 * X_0)*(delta + 1j*beta))*(np.exp(1j*X_1*(k*C_0*(delta+1j*beta)+phi))-(np.exp(1j*X_0*(k*C_0*(delta+1j*beta)+phi))))
    F_1 = (1/k*R_1)*np.exp(-1j*np.cos((beta*C_1)/R_1)+1j*k*(Z_1 - C_1 * X_1)*(delta + 1j*beta))*(np.exp(1j*X_2*(k*C_1*(delta+1j*beta)+phi))-(np.exp(1j*X_1*(k*C_1*(delta+1j*beta)+phi))))
    F_2 = (1/k*R_2)*np.exp(-1j*np.cos((beta*C_2)/R_2)+1j*k*(Z_2 - C_2 * X_2)*(delta + 1j*beta))*(np.exp(1j*X_3*(k*C_2*(delta+1j*beta)+phi))-(np.exp(1j*X_2*(k*C_2*(delta+1j*beta)+phi))))
    F_3 = (1/k*R_3)*np.exp(-1j*np.cos((beta*C_3)/R_3)+1j*k*(Z_3 - C_3 * X_3)*(delta + 1j*beta))*(np.exp(1j*X_4*(k*C_3*(delta+1j*beta)+phi))-(np.exp(1j*X_3*(k*C_3*(delta+1j*beta)+phi))))
   
    print("F_0: {}".format(F_0))
    print("F_1: {}".format(F_1))
    print("F_2: {}".format(F_2))
    print("F_3: {}".format(F_3))
   
    
    n = (abs(F_0 + F_1 + F_2 + F_3)**2)*((d*np.cos(theta))**(-2))
    
    print("Diffraction Efficiency [n]: {}".format(n))
    
    return n

# %%
def gratingEfficiencyHARV(m,b,d,G = 0):
    ''''
    Return the theoretical diffraction efficiency of X-rays incident on an arbitrary grating
    with rectangular wire cross sections (method from Harvey et al (2019)):
        m: order of diffracted beam
        b: slit size
        d: grating periodicity
        G: grating type - 0 = amplitude grating, 1 = phase grating
    '''
    if G == 0:
        n = ((b**2)/(d**2))*(np.sinc((m*b)/d)**2)
        
    elif G == 1:
        if b != d/2:
            print("Error: Ratio of slit size to periodicity must be 1:2 for phase grating")
            import sys
            sys.exit()
        else :
            n = np.sinc(m/2)**2
    # print("absolute grating efficiency: {}".format(n))
    
    return n
 # %%
def plotEfficiency():

    ampEff=[]
    phaEff=[]
    
    pEff_0 = []
    pEff_1 = []
    pEff_2 = []
    pEff_3 = []
    pEff_4 = []
    
    sEff_0 = []
    sEff_1 = []
    sEff_2 = []
    sEff_3 = []
    sEff_4 = []
    
    Eff_0 = []
    Eff_1 = []
    Eff_2 = []
    Eff_3 = []
    Eff_4 = []
    
    oEff = []
    
    
    period = np.array(range(1,200))
    # print("period: {}".format(period))
    slit = np.array(range(1,200))
    order = range(1,5)
    
    for p in period:
        E1 = gratingEfficiencyHARV(1,100e-9,1e-9*p,G=0)
        pEff_1.append(E1)
        E2 = gratingEfficiencyHARV(2,100e-9,1e-9*p,G=0)
        pEff_2.append(E2)
        E3 = gratingEfficiencyHARV(3,100e-9,1e-9*p,G=0)
        pEff_3.append(E3)
        E4 = gratingEfficiencyHARV(4,100e-9,1e-9*p,G=0)
        pEff_4.append(E4)
    # plt.plot(period, pEff_0, label = "m=0")
    plt.plot(period, pEff_1, label = "m=1")
    plt.plot(period, pEff_2, label = "m=2")
    plt.plot(period, pEff_3, label = "m=3")
    plt.plot(period, pEff_4, label = "m=4")
    plt.title("\u03B7\u2098 vs W\u209A (W\u209B=100 nm)")
    plt.xlabel("Period Width (W\u209A) [nm]")
    plt.ylabel("Grating Efficiency (\u03B7\u2098)")
    plt.legend()
    plt.show()
    
    
    for s in slit:
        # E0 = gratingEfficiencyHARV(0,1e-9*s,100e-9,G=0)
        # sEff_0.append(E0)
        E1 = gratingEfficiencyHARV(1,1e-9*s,100e-9,G=0)
        sEff_1.append(E1)
        E2 = gratingEfficiencyHARV(2,1e-9*s,100e-9,G=0)
        sEff_2.append(E2)
        E3 = gratingEfficiencyHARV(3,1e-9*s,100e-9,G=0)
        sEff_3.append(E3)
        E4 = gratingEfficiencyHARV(4,1e-9*s,100e-9,G=0)
        sEff_4.append(E4)
    # plt.plot(slit,sEff_0, label="m=0")
    plt.plot(slit,sEff_1, label="m=1")
    plt.plot(slit,sEff_2, label="m=2")
    plt.plot(slit,sEff_3, label="m=3")
    plt.plot(slit,sEff_4, label="m=4")
    plt.title("\u03B7\u2098 vs W\u209B (W\u209A=100 nm)")
    plt.xlabel("Slit Width (W\u209B) [nm]")
    plt.ylabel("Grating Efficiency (\u03B7\u2098)")
    plt.legend()
    plt.show()
    
    
    for s in slit:
        E0 = gratingEfficiencyHARV(0,1e-9*s,1e-9*p,G=0)
        Eff_0.append(E0)
        E1 = gratingEfficiencyHARV(1,1e-9*s,1e-9*p,G=0)
        Eff_1.append(E1)
        E2 = gratingEfficiencyHARV(2,1e-9*s,1e-9*p,G=0)
        Eff_2.append(E2)
        E3 = gratingEfficiencyHARV(3,1e-9*s,1e-9*p,G=0)
        Eff_3.append(E3)
        E4 = gratingEfficiencyHARV(4,1e-9*s,1e-9*p,G=0)
        Eff_4.append(E4)
        
    plt.plot(slit*0.005,Eff_0, label="m=0")
    plt.plot(slit*0.005,Eff_1, label="m=1")
    plt.plot(slit*0.005,Eff_2, label="m=2")
    plt.plot(slit*0.005,Eff_3, label="m=3")
    plt.plot(slit*0.005,Eff_4, label="m=4")
    plt.title("\u03B7\u2098 vs W\u209B/W\u209A")
    plt.yscale("log")
    plt.ylim(1e-4,1)
    plt.xlabel("W\u209B/W\u209A")
    plt.ylabel("Grating Efficiency (\u03B7\u2098)")
    plt.legend()
    plt.show()
    
    print("Shape of Eff_0: {}".format(np.shape(Eff_0)))
    print("Shape of Eff_1: {}".format(np.shape(Eff_1)))
    print("Shape of Eff_2: {}".format(np.shape(Eff_2)))
    print("Shape of Eff_3: {}".format(np.shape(Eff_3)))
    print("Shape of Eff_4: {}".format(np.shape(Eff_4)))
    
    tEff = np.array(Eff_0)+np.array(Eff_1)+np.array(Eff_2)+np.array(Eff_3)+np.array(Eff_4)
    totEff = np.array(Eff_1)+np.array(Eff_2)+np.array(Eff_3)+np.array(Eff_4)

    print("Shape of totEff: {}".format(np.shape(totEff)))
    
    plt.plot(slit*0.005,totEff, label = "m>0")
    plt.plot(slit*0.005,tEff, label = "m≥0")
    plt.plot(slit*0.005,Eff_0, label = "m=0")
    plt.title("\u03B7\u209C\u2092\u209C vs W\u209B/W\u209A")
    plt.xlabel("W\u209B/W\u209A")
    plt.ylabel("Total Grating Efficiency (\u03B7\u209C\u2092\u209C)")
    plt.legend()
    plt.show()
    
    
    
    for o in order:
        E = gratingEfficiencyHARV(o,1e-9,2e-9,G=1)
        oEff.append(E)
    ooEff=np.array([oEff[0], 
                   oEff[0]+oEff[1], 
                   oEff[0]+oEff[1]+oEff[2],  
                   oEff[0]+oEff[1]+oEff[2]+oEff[3]])
    print("Shape of oEff: {}".format(np.shape(oEff)))
    print("Shape of ooEff: {}".format(np.shape(ooEff)))
    plt.plot(order,oEff, label = "\u03B7\u2098")
    plt.plot(order,ooEff, label = "\u03B7\u209C\u2092\u209C")
    plt.title("\u03B7 vs m (phase grating)")
    plt.xlabel("Diffraction Order (m)")
    plt.ylabel("Grating Efficiency (\u03B7)")
    plt.legend()
    plt.show()
    
    
    
    # plt.plot(period, pEff, label="period (slit=100nm)")
    # plt.plot(slit, sEff, label="slit (period=200nm)")
    # plt.title("Grating Efficiency")
    # plt.xlabel("Size of slit/period [nm]")
    # plt.ylabel("Grating Efficiency (m=1)")
    # plt.legend()
    # plt.show()
    
    # for p in period:
    #     for s in slit:
    #         E = gratingEfficiencyHARV(1,1e-9*s,1e-9*p,G=0)
    #         ampEff.append(E)
            
    # print("Shape of ampEff: {}".format(np.shape(ampEff)))
    
    #     # s = np.reshape(stk.arS,(4,stk.mesh.nx,stk.mesh.ny))
    # plt.plot(ampEff)
    # plt.show()
    # # Eff = np.reshape(ampEff,(3,)))
    
    # # lamda = 6.7e-9
    # # p = 200e-9
    # # # m = 10
    # # NA = 0.1 #m*lamda/p
    # # # print("NA: {}".format(NA))
    
    # # m = NA*p/lamda
    # # print("m: {}".format(m))

# %%
def getImageData(filename):
    im = imageio.imread(filename)
    # show each image (can comment out for speed)
    #plt.imshow(im)
    #plt.show()
    
    # convert each image to array
    im = np.array(im)

    return im

# %%
def get_rect(x, y, width, height, angle):
    rect = np.array([(0, 0), (width, 0), (width, height), (0, height), (0, 0)])
    theta = (np.pi / 180.0) * angle
    R = np.array([[np.cos(theta), -np.sin(theta)],
                  [np.sin(theta), np.cos(theta)]])
    offset = np.array([x, y])
    transformed_rect = np.dot(rect, R) + offset
    
    return transformed_rect

# %%
def getOrders(I, m):
    ## DOESNT WORK ##
    """ 
    I : Intensity array
    m : maximum order to be analysed
    """
    
    s = np.shape(I)
    print("shape of intensity array: {}".format(s))
    
    N_ord = int((2*m)+1)

    # import image_slicer
    # image_slicer.slice(I, N_ord)
    
    # # M = np.reshape(I,(N_ord, 
    # #                   (s[0])/N_ord,
    # #                   (s[1])/N_ord ))
    
    if s[0]/N_ord != int:
        
        newshape = int(s[0]/N_ord)*N_ord
        diff = s[0] - newshape
        print("difference in shape: {}".format(diff))
        Inew = I[0:s[1],int(diff/2):int(newshape+diff/2)]
        
        plt.imshow(Inew)
        plt.title("Inew")
        
        print("New shape of I: {}".format(np.shape(Inew)))
        print("New size of I: {}".format(np.size(Inew)))
        
        
        M = np.reshape(Inew, (N_ord, int(s[1]), int((s[0]/N_ord))))
    else:
        M = np.reshape(I, (N_ord, int(s[1]), int((s[0]/N_ord))))
    
    print("New shape of intensity array: {}".format(np.shape(M)))
    
    plt.imshow(M[0])
    plt.title("test")
    plt.show()
    
    for i in range(N_ord):
        
        Mi = M[i,:,:]
        
        plt.imshow(Mi)
        plt.title(i)
        plt.show()

    
    # for i in 2*m + 1:
        
    #     m_i = np.reshape(M[i],((s2[0])/(2*m+1),(s2[1])/(2*m+1)))
    #     print(m_i)
    #     return m_i

    # return i

# %%    
def getFarField(D,lam):
    """  
    """
    r = (D**2)/(4*lam)
    
    print("Distance to Far-field [m]: {}".format(r))
    
    return r

# %%
def pixelSize(w):
    px = (w.params.Mesh.xMax - w.params.Mesh.xMin) / w.params.Mesh.nx
    py = (w.params.Mesh.yMax - w.params.Mesh.yMin) / w.params.Mesh.ny
    
    return px, py
# %%
def getEfficiency(path1, path2, path3, m = 1, pickle = 1, pathm0 = None, pathm1 = None, pathm2 = None): #, intV = 300):    
    """ Get the diffraction efficiency of a mask from intensity before mask, 
    at exit plane & after propagation.
    params:
        path1: intensity/wavefield before mask
        path2: intensity/wavefield at mask exit plane
        path3: intensity/wavefield after propagation
        m: maximum order to be analysed (accepts 0<m<5)
        pickle: input to be analysed. 0 = intensity tif files, 1 = wavefield pickle files
        pathm0: Save path for m=0 order intensity
        pathm1: Save path for m=1 order intensity
        pathm2: Save path for m=2 order intensity
    returns:
        efficiency of each order up to maximum """
    
    #from wfAnalyseWave import pixelsize
    
    if pickle == 1:

        import pickle
        with open(path1, 'rb') as wav:
            w1 = pickle.load(wav)
        with open(path2, 'rb') as wav:
            w2 = pickle.load(wav)
        with open(path3, 'rb') as wav:
            w3 = pickle.load(wav)
            
        wf1 = Wavefront(srwl_wavefront=w1)
        wf2 = Wavefront(srwl_wavefront=w2)
        wf3 = Wavefront(srwl_wavefront=w3)
        
        p1 = pixelSize(wf1)
        p2 = pixelSize(wf2)
        p3 = pixelSize(wf3)
        
        pR1 = p1[0]/p2[0]
        pR2 = p1[0]/p3[0]
        pR3 = p2[0]/p3[0]
        
        print("pixel size at mask [m]: {}".format(p1))
        print("pixel size after mask [m]: {}".format(p2))
        print("pixel size after propagation [m]: {}".format(p3))
        print("ratio of pixel sizes (p1/p2): {}".format(pR1))
        print("ratio of pixel sizes (p1/p3): {}".format(pR2))
        print("ratio of pixel sizes (p2/p3): {}".format(pR3))
        
        """ Intensity from wavefield """
        I0 = wf1.get_intensity()
        I1 = wf2.get_intensity()
        I2 = wf3.get_intensity()
        
        """ Total intensity at each plane """
        I0_tot = np.sum(I0)/(p1[0]*p1[1])    #*p1[0]#6.25e-09*s0[0]*s0[1]
        I1_tot = np.sum(I1)/(p2[0]*p2[1])     #*p2[0]#*s1[0]*s1[1]
        I2_tot = np.sum(I2)/(p3[0]*p3[1])     #*p3[0]#*s2[0]*s1[1]
        
        
    else:
        """ Intensity from tif file """
        I0 = path1 #getImageData("/home/jerome/Documents/MASTERS/data/wavefields/Efficiency/intensityIN.tif")
        I1 = path2 #getImageData('/home/jerome/Documents/MASTERS/data/wavefields/Efficiency/intensityEX_1-2.tif')
        I2 = path3 #getImageData('/home/jerome/Documents/MASTERS/data/wavefields/Efficiency/intensityPR_1-2.tif') #getImageData('/home/jerome/WPG/intensityTot_maskprop.tif')    
        
        """ Total intensity at each plane """
        I0_tot = np.sum(I0)    #*p1[0]#6.25e-09*s0[0]*s0[1]
        I1_tot = np.sum(I1)   #*p2[0]#*s1[0]*s1[1]
        I2_tot = np.sum(I2)     #*p3[0]#*s2[0]*s1[1]
    
    s0 = np.shape(I0)
    s1 = np.shape(I1)
    s2 = np.shape(I2)
    
    print("Shape of I (at mask): {}".format(s0))
    print("Shape of I (after mask): {}".format(s1))
    print("Shape of I (after propagation): {}".format(s2))
    
    F0 = s0[0]/s1[0]
    F1 = s0[0]/s2[0]
    F2 = s1[0]/s2[0]
    
    print("pixel ratio (I0/I1): {}".format(F0))
    print("pixel ratio (I0/I2): {}".format(F1))
    print("pixel ratio (I1/I2): {}".format(F2))
    
    if F0 != 1.0:
        print("WARNING! Number of pixels in intensity files does not match! Efficiency values may not be accurate!")
        
    if F1 != 1.0:
        print("WARNING! Number of pixels in intensity files does not match! Efficiency values may not be accurate!")
        
    if F2 != 1.0:
        print("WARNING! Number of pixels in intensity files does not match! Efficiency values may not be accurate!")
    
    Ir0 = (I1_tot/I0_tot)#(F0**2)*(I1_tot/I0_tot)    # ratio of intensity before & after mask
    Ir1 = (I2_tot/I0_tot) #(F1**2)*(I2_tot/I0_tot)    # ratio of intensity before & after mask
    Ir2 = (I2_tot/I1_tot) #(F2**2)*(I2_tot/I1_tot)    # ratio of intensity before & after mask
    
    print("Intensity Ratio I_ex/I_in: {}".format(Ir0))
    print("Intensity Ratio I_prop/I_in: {}".format(Ir1))
    print("Intensity Ratio I_prop/I_exit: {}".format(Ir2))
    
    
    plt.imshow(I0)
    plt.title("at mask")
    plt.colorbar()
    plt.show()
    
    plt.imshow(I1)
    plt.title("After mask")
    plt.colorbar()
    plt.show()   
    
    plt.imshow(I2)
    plt.title("after propagation")
    plt.colorbar()
    plt.show()
    
    
    print(" ")
    print("-----Total Intensity-----")
    print("At mask: {}".format(I0_tot))
    print("After mask: {}".format(I1_tot))
    print("After propagation: {}".format(I2_tot))

    """ Defining region of interest to inspect separate orders """  
    Mi = int((s2[0]/2)-300) #initial position for order sampling
    Mf = int((s2[0]/2)+300) #final position for order sampling
    
    print("coordinates for start and end of each order: {}".format((Mi,Mf)))
    
    """Finding each order"""
    
    intV = int(s2[0]/(2*m+1)) #500 # Number of pixels for segmentation interval 
    
    if m >= 1:
        # region for m=0 
        ROI_0 = ((int((s2[0]/2)-(intV/2)),Mi),((int((s2[0]/2)+(intV/2))),Mf))                    
        # region for m=+1
        ROI_1 = ((ROI_0[1][0], Mi),(ROI_0[1][0] + intV, Mf))
        # region for m=-1
        ROI_n1 =((ROI_0[0][0]-intV, Mi),(ROI_0[0][0], Mf))
    if m >= 2:      
        # region for m=+2
        ROI_2 = ((ROI_1[1][0], Mi),(ROI_1[1][0] + intV, Mf))
        # region for m=-2
        ROI_n2 = ((ROI_n1[0][0]-intV, Mi),(ROI_n1[0][0], Mf))
    if m >= 3:      
        # region for m=+3  
        ROI_3 = ((ROI_2[1][0], Mi),(ROI_2[1][0] + intV, Mf))
        # region for m=-3
        ROI_n3 = ((ROI_n2[0][0]-intV, Mi),(ROI_n2[0][0], Mf))
    if m >= 4:  
        # region for m=+4
        ROI_4 = ((ROI_3[1][0], Mi),(ROI_3[1][0] + intV, Mf))
        # region for m=-4
        ROI_n4 = ((ROI_n3[0][0]-intV, Mi),(ROI_n3[0][0], Mf))
    
    
    
    x0_0,y0_0 = ROI_0[0][0], ROI_0[0][1]
    x1_0,y1_0 = ROI_0[1][0], ROI_0[1][1]
    
    x0_1,y0_1 = ROI_1[0][0], ROI_1[0][1]
    x1_1,y1_1 = ROI_1[1][0], ROI_1[1][1]
    
    x0_n1,y0_n1 = ROI_n1[0][0], ROI_n1[0][1]
    x1_n1,y1_n1 = ROI_n1[1][0], ROI_n1[1][1]   
    
    try:
        x0_2,y0_2 = ROI_2[0][0], ROI_2[0][1]
        x1_2,y1_2 = ROI_2[1][0], ROI_2[1][1]
        
        x0_n2,y0_n2 = ROI_n2[0][0], ROI_n2[0][1]
        x1_n2,y1_n2 = ROI_n2[1][0], ROI_n2[1][1]
    
        x0_3,y0_3 = ROI_3[0][0], ROI_3[0][1]
        x1_3,y1_3 = ROI_3[1][0], ROI_3[1][1]
        
        x0_n3,y0_n3 = ROI_n3[0][0], ROI_n3[0][1]
        x1_n3,y1_n3 = ROI_n3[1][0], ROI_n3[1][1]    
        
        x0_4,y0_4 = ROI_4[0][0], ROI_4[0][1]
        x1_4,y1_4 = ROI_4[1][0], ROI_4[1][1]
        
        x0_n4,y0_n4 = ROI_n4[0][0], ROI_n4[0][1]
        x1_n4,y1_n4 = ROI_n4[1][0], ROI_n4[1][1]
    except NameError:
        pass
    
    
    A_0 = I2[y0_0:y1_0,x0_0:x1_0]
    A_1 = I2[y0_1:y1_1,x0_1:x1_1]
    A_n1 = I2[y0_n1:y1_n1,x0_n1:x1_n1]    
    try:
        A_2 = I2[y0_2:y1_2,x0_2:x1_2]
        A_n2 = I2[y0_n2:y1_n2,x0_n2:x1_n2]
        A_3 = I2[y0_3:y1_3,x0_3:x1_3]
        A_n3 = I2[y0_n3:y1_n3,x0_n3:x1_n3]
        A_4 = I2[y0_4:y1_4,x0_4:x1_4]
        A_n4 = I2[y0_n4:y1_n4,x0_n4:x1_n4]
    except NameError:
        pass
    
    plt.imshow(A_0)
    plt.title('m=0')
    plt.colorbar()
    if pathm0 != None:
        print("Saving m=0 figure to path: {}".format(pathm0))
        plt.savefig(pathm0)
    plt.show()    
    
    plt.imshow(A_1)
    plt.title('m=+1')
    plt.colorbar()
    if pathm1 != None:
        print("Saving m=1 figure to path: {}".format(pathm1))
        plt.savefig(pathm1)
    plt.show()
    
    plt.imshow(A_n1)
    plt.title('m=-1')
    plt.colorbar()
    plt.show()    
    
    try:
        plt.imshow(A_2)
        plt.title('m=+2')
        plt.colorbar()
        if pathm2 != None:
            print("Saving m=2 figure to path: {}".format(pathm2))
            plt.savefig(pathm2)
        plt.show()
        
        plt.imshow(A_n2)
        plt.title('m=-2')
        plt.colorbar()
        plt.show()    
    
        plt.imshow(A_3)
        plt.title('m=+3')
        plt.colorbar()
        plt.show()
        
        plt.imshow(A_n3)
        plt.title('m=-3')
        plt.colorbar()
        plt.show()
            
        plt.imshow(A_4)
        plt.title('m=+4')
        plt.colorbar()
        plt.show()
        
        plt.imshow(A_n4)
        plt.title('m=-4')
        plt.colorbar()
        plt.show()
    except NameError:
        pass
    
    Im_0 = np.sum(A_0)
    Im_1 = np.sum(A_1)
    Im_n1 = np.sum(A_n1)
    try:
        Im_2 = np.sum(A_2)/Ir2
        Im_n2 = np.sum(A_n2)/Ir2
        Im_3 = np.sum(A_3)/Ir2
        Im_n3 = np.sum(A_n3)/Ir2
        Im_4 = np.sum(A_4)/Ir2
        Im_n4 = np.sum(A_n4)/Ir2
    except NameError:
        pass
    
    print(" ")
    print("----- Intensity of m = 0-----")
    print("Im_1: {}".format(Im_0))
    print(" ")
    print("----- Intensity of m = +1-----")
    print("Im_1: {}".format(Im_1))
    print(" ")
    print("----- Intensity of m = -1-----")
    print("Im_n1: {}".format(Im_n1))  
    try:
        print(" ")
        print("----- Intensity of m = +2-----")
        print("Im_2: {}".format(Im_2))
        print(" ")
        print("----- Intensity of m = -2-----")
        print("Im_n2: {}".format(Im_n2))  
        print(" ")
        print("----- Intensity of m = +3-----")
        print("Im_3: {}".format(Im_3))
        print(" ")
        print("----- Intensity of m = -3-----")
        print("Im_n3: {}".format(Im_n3))  
        print(" ")
        print("----- Intensity of m = +4-----")
        print("Im_4: {}".format(Im_4))
        print(" ")
        print("----- Intensity of m = -4-----")
        print("Im_n4: {}".format(Im_n4))
    except NameError:
        pass
    
    if pickle == 1:
        """ Get Efficiency of each order """   # Not sure if should be dividing by total intensity at mask or after mask
        E0 = (Im_0/I0_tot)/p3[0] #p3[0]*(Im_0/I0_tot)
        E1 = (Im_1/I0_tot)/p3[0] # p3[0]*(Im_1/I0_tot)/p3[0] #
        En1 = (Im_n1/I0_tot)/p3[0] # p3[0]*(Im_n1/I0_tot)/p3[0] #
        
        try:
            E2 = p3[0]*(Im_2/I0_tot)
            En2 = p3[0]*(Im_n2/I0_tot)
            E3 = p3[0]*(Im_3/I0_tot)
            En3 = p3[0]*(Im_n3/I0_tot)
            E4 = p3[0]*(Im_4/I0_tot)
            En4 = p3[0]*(Im_n4/I0_tot)
        except NameError:
            pass
    else:
        """ Get Efficiency of each order """   # Not sure if should be dividing by total intensity at mask or after mask
        E0 = (Im_0/I0_tot)
        E1 = (Im_1/I0_tot)
        En1 = (Im_n1/I0_tot)
        
        try:
            E2 = (Im_2/I0_tot)
            En2 = (Im_n2/I0_tot)
            E3 = (Im_3/I0_tot)
            En3 = (Im_n3/I0_tot)
            E4 = (Im_4/I0_tot)
            En4 = (Im_n4/I0_tot)
        except NameError:
            pass
        
    print(" ")
    print("Efficiency of m=0 order: {}".format(E0))
    print("Efficiency of m=+1 order: {}".format(E1))
    print("Efficiency of m=-1 order: {}".format(En1))
    try:
        print("Efficiency of m=+2 order: {}".format(E2))
        print("Efficiency of m=-2 order: {}".format(En2))
        print("Efficiency of m=+3 order: {}".format(E3))
        print("Efficiency of m=-3 order: {}".format(En3))
        print("Efficiency of m=+4 order: {}".format(E4))
        print("Efficiency of m=-4 order: {}".format(En4))
    except NameError:
        pass
    
# %%
def test():
    
    """ Testing theoretical efficiency """
    m=1                       #order of diffracted beam
    beta = 1.76493861*1e-3    #imaginary part of refractive index
    delta = 1-(2.068231*1e-2) #(1-real part) of refractive index
    d = 200e-9 #grating periodicity
    k = 197.3 * 6.7 #photon energy in units of (hbar*c)
    b = 72e-9
    theta = 0 #np.pi/2 #incident angle
    
    # print(" ")
    # print("-----Grating efficiency (DEL)-----")
    # gratingEfficiencyDEL(m, beta, delta, d, k, b,theta)
    
    print(" ")
    print("-----Grating efficiency (amplitude)-----")
    gratingEfficiencyHARV(1,100e-9,200e-9,G=0)
    
    print(" ")
    print("-----Grating efficiency (phase)-----")
    gratingEfficiencyHARV(1,100e-9,200e-9,G=1)


    """ Testing simulated efficiency """
    eMin = 1e8
    Nx = 150
    Ny = 150
    Nz = 1
    xMin = -10e-6
    xMax = 10e-6
    yMin = -10e-6
    yMax = 10e-6
    zMin = 100
    # Fx = 1/2
    # Fy = 1/2
    
    print(" ")
    print('Running Test:')
    print('building wavefront...')
    w = build_gauss_wavefront(Nx,Ny,Nz,eMin/1000,xMin,xMax,yMin,yMax,1,1e-6,1e-6,1) 
    
    wf0 = Wavefront(srwl_wavefront=w)
    
    """ Intensity from test Gaussian """
    # I = wf0.get_intensity()
    
    directory = "/data/experiments/maskEfficiency/data/"
    
    """ Load pickled Wavefronts """
    path1 = directory + "incident/incident.pkl"
    path2 = directory + "exit/exit.pkl"
    
    n = range(1,25) #20*np.array([range(1,25)])
    m = 20
    for i in n:
        print(m*i)
        print("Finding diffraction efficiency of mask with thickness {} nm".format(m*i))
        path3 = directory + str(m*i) + "/mt" + str(m*i) + ".pkl"
        pathm0 = directory + "zeroOrder" + str(m*i)
        pathm1 = directory + "firstOrder" + str(m*i)
        pathm2 = directory + "secondOrder" + str(m*i)
        getEfficiency(path1,path2,path3,2,1, pathm0,pathm1,pathm2)
    #"20/mt20.pkl" 
    
    """ Intensity from tif file """
    I0 = getImageData(directory + "intensityIN.tif")
    I1 = getImageData(directory + "intensityEX_1-2.tif")
    I2 = getImageData(directory + "intensityPR_1-2.tif") #getImageData('/hom
    
    
    #pathm0 = directory + "zeroOrder"
    #pathm1 = directory + "firstOrder"
    #pathm2 = directory + "secondOrder"
    
    # getEfficiency(I0,I1,I2,3,0)#,540)    
    #getEfficiency(path1,path2,path3,2,1, pathm0=pathm0)#,540)   
    
# %%
def testReshape():
    
    I = getImageData('/home/jerome/Documents/MASTERS/data/wavefields/Efficiency/intensityPR_1-4.tif') 
    plt.imshow(I)
    plt.title("Intensity")
    
    getOrders(I,3)
    
# %%
if __name__ == '__main__':
    test()
   # testReshape()
