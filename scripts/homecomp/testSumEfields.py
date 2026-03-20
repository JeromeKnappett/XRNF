#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 19 12:00:44 2022

@author: jerome
"""
import numpy as np
import matplotlib.pyplot as plt
import interferenceGratingModelsJK

def testSumEfields():
    import tifffile
    import apDiffraction
    
    path = '/home/jerome/dev/data/correctedBlockDiffraction/'
    #slit sizes]
    sX = [100,200]#,350,400,500]#,750,1000] #[100,200,300,350,300,500,750,1000] #,400,500,750,1000]
    sY = [250,250]
        
    N = 1000                            # number of pixels to take for line profile  - 1200 for roughness aerial images
    n = 1                             # number of pixels to average over for line profile - 15 for roughness aerial images
    plotRange = 10000                       # range of aerial image plot in nm
    
    # res and middle pixels of images
    res =   [(4.832552851219838e-09, 3.853038352405723e-07),(4.832457034313024e-09, 3.8431154968763494e-07)]
    mid =   [(196, 19887),(96, 7405)]
    pitch = 100e-9
    
    
    resAE = (2.5011882651601634e-09, 2.426754806976689e-07)
    midAE = (196, 12188)
    
    tiffAE = tifffile.imread(path + 'imagePlaneintensity.tif')
    imageAE = tiffAE[midAE[0]-n:midAE[0]+n,midAE[1]-2*N:midAE[1]+2*N]
    profileAE = imageAE.mean(0)
    xAE = np.linspace(-2*N*resAE[0], 2*N*resAE[0],4*N)
    
    
    files = ['apertureDiffraction','blockDiffraction']
    
    fileNames = [path + f for f in files]
    
    EhR = [tifffile.imread(f + 'ExReal.tif') for f in fileNames] 
    EvR = [tifffile.imread(f + 'EyReal.tif') for f in fileNames] 
    EhI = [tifffile.imread(f + 'ExIm.tif') for f in fileNames] 
    EvI = [tifffile.imread(f + 'EyIm.tif') for f in fileNames] 
    
    imagesEhR = [t[m[0]-n:m[0]+n,m[1]-N:m[1]+N] for t, m in zip(EhR,mid)]
    imagesEvR = [t[m[0]-n:m[0]+n,m[1]-N:m[1]+N] for t, m in zip(EvR,mid)]
    imagesEhI = [t[m[0]-n:m[0]+n,m[1]-N:m[1]+N] for t, m in zip(EhI,mid)]
    imagesEvI = [t[m[0]-n:m[0]+n,m[1]-N:m[1]+N] for t, m in zip(EvI,mid)]
    profileshR = [i.mean(0) for i in imagesEhR] 
    profilesvR = [i.mean(0) for i in imagesEvR] 
    profileshI = [i.mean(0) for i in imagesEhI] 
    profilesvI = [i.mean(0) for i in imagesEvI] 
    xP = [np.linspace(-N*r[0], N*r[0],2*N) for r in res]
    yP = [np.linspace(-n*r[1], n*r[1],2*n) for r in res]



    ''' define interference grating parameters'''
    wl = 6.710553853647976e-9 # wavelength in m
    
    # Amplitude of both beams (assumed equal)
    A = 1.35e5 #0.148e5 #0.078e5  0.37e5 #0.3e5  # this may be scaled to  match simulated intensity
    k = 2*np.pi/wl
    m = 1 # order of diffracted beams from each grating
    d = 100e-9 #24e-9 #100e-9 # grating spacing
    # angle between the beams from each grating
    theta = np.arcsin( m *wl/d)
    IP = interferenceGratingModelsJK.interferenceIntensity(xP[0],k,theta,A=A)

    
    # method 3
    Eh = [ExR + ExI*1j for ExR,ExI in zip(imagesEhR,imagesEhI)]
    Ev = [EyR + EyI*1j for EyR,EyI in zip(imagesEvR,imagesEvI)]#EvR + EvI*1j
    cE = [Ex + Ey for Ex, Ey in zip(Eh,Ev)] #Eh + Ev

    # plt.imshow(EhR[0], aspect='auto')
    # plt.show()

    realE = []
    imagE = []
    IX = []
    
    for i, e in enumerate(cE):
        I = abs(e.conjugate()*e)
        ex = e[int(np.shape(e)[0]/2),:]
        ey = e[:,int(np.shape(e)[1]/2)]
        Ix = I[int(np.shape(I)[0]/2),:]
        Iy = I[:,int(np.shape(I)[1]/2)]
        
        print('shape of yP: ', np.shape(yP[i]))
        print('shape of ey: ', np.shape(np.real(ey)))
        
        plt.imshow(I, aspect='auto')
        plt.title("Intensity")
        plt.show()
        
        plt.plot(Ix)
        plt.show()
        
        # fig, axs = plt.subplots(2,2)
        # axs[0,0].plot(xP[i],np.real(ex))
        # axs[0,0].set_title('Horizontal electric field - Real')
        # axs[0,1].plot(yP[i],np.real(ey))
        # axs[0,1].set_title('Vertical electric field - Real')
        # axs[1,0].plot(xP[i],np.imag(ex))
        # axs[1,0].set_title('Horizontal electric field - Im')
        # axs[1,1].plot(yP[i],np.imag(ey))
        # axs[1,1].set_title('Vertical electric field - Im')
        # # axs[2].plot(e)
        # # axs[2].title('Complex electric field')
        # plt.tight_layout()
        # plt.show()
        
        realE.append(np.real(ex))
        imagE.append(np.imag(ex))
        IX.append(Ix)
    
    plt.plot(xP[0],IX[0]/np.max(IX[0]), label=files[0])
    plt.plot(xAE,profileAE/np.max(profileAE), label='Aerial Image')
    plt.plot(xP[1],IX[1]/np.max(IX[1]), label=files[1])
    plt.legend()
    plt.show()
    
    A = 1
    E = realE[0]**2+realE[1]**2 + A*2*np.sqrt(realE[0]*realE[1])*np.sin(abs(imagE[0]-imagE[1]))#np.cos(imagE[0]-imagE[1])#*np.sin(imagE[1]-imagE[0])
    E_0 = np.sqrt(realE[0]**2+realE[1]**2) # + A*2*np.sqrt(realE[0]*realE[1])*np.cos(imagE[0]-imagE[1])*np.sin(imagE[1]-imagE[0])
    # I = IX[0] + IX[1] + A*2*np.sqrt(IX[0]*IX[1])*np.cos(imagE[1]-imagE[0])*np.sin(imagE[1]-imagE[0])
    
    profSUB = (E/np.max(E))*((IP)/np.max(IP))
    
    #TRYING OTHER METHOD
    # ESUM = abs(apDiffraction.sumTwoE(realE[0],imagE[0],realE[1],imagE[1],A))**2
    
    # print(np.shape(I)
    plt.plot(xP[0]*1e9,E_0/np.max(E_0), label='Esum')
    plt.plot(xP[0]*1e9,E/np.max(E), label='Esum1')
    # plt.plot(xP[0]*1e9,I/np.max(I), label='Isum')
    plt.plot(xP[0]*1e9,IX[0]/np.max(IX[0]), label='I aperture')
    # plt.plot(xP[0]*1e9,ESUM/np.max(ESUM), label='Esum2')
    plt.plot(xAE*1e9,profileAE/np.max(profileAE), label='AE')
    # plt.plot(xP[0]*1e9,IP/np.max(IP)-0.2, label='Ideal')
    # plt.plot(xP[0]*1e9,profSUB/np.max(profSUB), label='E - Ideal')
    plt.xlim(-int(plotRange/2), int(plotRange/2))
    plt.ylim(bottom=0)
    plt.legend()
    plt.show()
    
    # plt.imshow(imageAE, aspect='auto')
    # plt.show()
    # plt.plot(xAE,profileAE)
    # plt.show()
    
if __name__ == '__main__':
    testSumEfields()