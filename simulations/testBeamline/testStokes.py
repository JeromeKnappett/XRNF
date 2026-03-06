#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 15:22:21 2022

@author: -
"""

from utilStokes import getStokes, getStokesParamFromStokes, normaliseStoke, plotStokes
from wpg.srwlib import SRWLStokes, SRWLWfr
import numpy as np
import matplotlib.pyplot as plt
import pickle
from wpg.wavefront import Wavefront

def testStokes():
    
    savePath = None
    toPickle = False
    saveIntensity = True
    
    # path = 'wavefield_1.pkl'
#    path = '/user/home/opt/xl/xl/experiments/correctedAngle_coherence3/data/' #'/user/home/opt/xl/xl/experiments/lowEnergyBeam/data/'
#    '/user/home/opt/xl/xl/experiments/correctedAngle_coherence3/data/'
    
#    names =['atM1']
    
    path = '/user/home/opt/xl/xl/experiments/testBeamline/data/'
    names = ['Vgrad','Vgrad4000','Vgrad8000','Vgrad12000','Vgrad16000','Vgrad25000','Vgrad50000']#['8nmTMincident','8nmTEincident']#['20nmTMincident','20nmTMexit','20nmTEincident','20nmTEexit','24nmTMincident','24nmTMexit','24nmTEincident','24nmTEexit']
    files = [path + str(n) + '/' + str(n) + 'EforS.pkl' for n in names]
    E = 184.76  #photon energy
    
    
    picks = [pickle.load(open(f, 'rb')) for f in files]
    N = [(int(p[2]),int(p[3])) for p in picks]
    nTot = [n[0]*n[1] for n in N]
    res = [(p[4],p[5]) for p in picks]
    Ex = [p[0] for p in picks]
    Ey = [p[1] for p in picks]
    
    STOKES = []
    Itot = []
    Ixtot = []
    Iytot = []
    
    for i, n in enumerate(names):
        print(' ')
        print(f'Analysing {n}')
#        ch, cv, r, n in zip(Ex,Ey,res,N): 
        
        # Defining parameters
        wf = SRWLWfr() #Initial Electric Field Wavefront    
        
        wf.allocate(1, N[i][0], N[i][1]) #Numbers of points vs Photon Energy (1), Horizontal and Vertical Positions (dummy)
        wf.mesh.zStart = 0 #Longitudinal Position [m] at which Electric Field has to be calculated, i.e. the position of the first optical element
        wf.mesh.eStart = E #Initial Photon Energy [eV]
        wf.mesh.eFin = E #Final Photon Energy [eV]
        wf.mesh.xStart = (-N[i][0]/2)*res[i][0] #Initial Horizontal Position [m]
        wf.mesh.xFin = (N[i][0]/2)*res[i][0] #Final Horizontal Position [m]
        wf.mesh.yStart = (-N[i][1]/2)*res[i][1] #Initial Vertical Position [m]
        wf.mesh.yFin = (N[i][1]/2)*res[i][1] #Final Vertical Position [m]
        wf.arEx = Ex[i]
        wf.arEy = Ey[i]
        wf.mesh.ne = 1
        
        w = Wavefront(srwl_wavefront=wf)
        
        itot = np.squeeze(w.get_intensity(polarization='total'))
        ix = np.squeeze(w.get_intensity(polarization='horizontal'))
        iy = np.squeeze(w.get_intensity(polarization='vertical'))
        
        ixTOT = np.sum(ix)
        iyTOT = np.sum(iy)
        
        _c = 299792458
        epsilon = 8.854187817e-12
        
        Imtot_w = np.sum(itot)*(_c/2*epsilon) # W/m^2
        ITOT = Imtot_w*(1/1.602e-19)*(1/E)*0.0001
        
        Imtot = np.sum(ITOT*res[i][0]*res[i][1])
        
        print(f"Total energy:       {ITOT}")
        print(f"Total Ix:           {ixTOT}")
        print(f"Total Iy:           {iyTOT}")
        
        fig, ax = plt.subplots(1,3)
        ax[0].imshow(ix, aspect='auto')
        ax[0].set_title("horizontal intensity")
        ax[1].imshow(itot,aspect='auto')
        ax[1].set_title("total intensity")
        ax[2].imshow(iy, aspect='auto')
        ax[2].set_title("vertical intensity")
        plt.show()
        
        plt.imshow(ix,aspect='auto')
        plt.colorbar()
        plt.show()
        
        
        print ('-----Getting Stokes parameters-----')
        S, Dx, Dy = getStokes(wf, mutual=0, Fx = 1, Fy = 1)
        s= getStokesParamFromStokes(S,d=2)
        sn = normaliseStoke(s,d=2)
        plotStokes(s,dx=res[i][0], dy=res[i][1], extra=False, savePath=savePath)
        
        
        Int = S.to_int()
#        plt.plot(Int)
#        plt.title('Int from Stk')
#        plt.show()
        
        I2D = np.reshape(Int,(N[i][0],N[i][1]))
        plt.imshow(I2D)
        plt.title('Int from Stk')
        plt.colorbar()
        plt.show()
        
        Itot.append(Imtot)
        Ixtot.append(ixTOT)
        Iytot.append(iyTOT)
        
        STOKES.append(sn)
        
        if saveIntensity:
            with open(path + str(n) + '.pkl', "wb") as f:
                pickle.dump([np.float32(itot), res[i][0], res[i][1]], f)
            import tifffile
            tifffile.imwrite(path + str(n) + '/intensity.tif',itot)
        
#    dS0tm = STOKES[1][0] - STOKES[0][0]
#    dS1tm = STOKES[1][1] - STOKES[0][1]
#    dS2tm = STOKES[1][2] - STOKES[0][2]
#    dS3tm = STOKES[1][3] - STOKES[0][3]
#    dS0te = STOKES[3][0] - STOKES[2][0]
#    dS1te = STOKES[3][1] - STOKES[2][1]
#    dS2te = STOKES[3][2] - STOKES[2][2]
#    dS3te = STOKES[3][3] - STOKES[2][3]
#    
#    dStm = [dS0tm,dS1tm,dS2tm,dS3tm] 
#    dSte = [dS0te,dS1te,dS2te,dS3te] 
#    
#    plotStokes(dStm,dx=res[0][0],dy=res[0][1])
#    plotStokes(dSte,dx=res[0][0],dy=res[0][1])
#    
#    Irat = [Itot[1]/Itot[0], Itot[3]/Itot[2]]
#    Ixrat = [Ixtot[1]/Ixtot[0], Ixtot[3]/Ixtot[2]]
#    Iyrat = [Iytot[1]/Iytot[0], Iytot[3]/Iytot[2]]
    
    if toPickle:
        for i, sn in enumerate(STOKES):
            with open(path + names[i] + '_stokes.pkl', "wb") as f:
                pickle.dump(sn, f)
    else:
        pass
    
    plotNames = ['20nmTM','20nmTE','24nmTM','24nmTE']
    
    fig, ax = plt.subplots(3,1)
    for e in range(0,int(len(Itot)/2)):
        print(e)
        e2 = e*2
        e2p1 = e2 + 1
        
        iRAT = Itot[e2p1]/Itot[e2]
        ixRAT = Ixtot[e2p1]/Ixtot[e2]
        iyRAT = Iytot[e2p1]/Iytot[e2]
        
        print(iRAT)
        print(ixRAT)
        print(iyRAT)
        
        ax[0].plot(plotNames[e],iRAT, 'x')
        ax[1].plot(plotNames[e],ixRAT, 'x')
        ax[2].plot(plotNames[e],iyRAT, 'x')
    
    ax[0].set_title('total flux ratio')
    ax[1].set_title('x flux ratio')
    ax[2].set_title('y flux ratio')
    plt.show()
#    
#    plt.plot(['TM','TE'],Irat)
#    plt.title("Total Flux Ratio")
#    plt.show()
#    
#    plt.plot(['TM','TE'],Ixrat)
#    plt.title("x-intensity ratio")
#    plt.show()
#    plt.plot(['TM','TE'],Iyrat)
#    plt.title("y-intensity ratio")
#    plt.show()
    
#    plotStokes([dS0,dS1,dS2,dS3],dx=res[0][0],dy=res[0][1])
#    
#    plt.plot(cL)
#    plt.title("from trey script")
#    plt.show()
    
# %%
if __name__ == '__main__':
    testStokes()
