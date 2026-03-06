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

def testStokes():
    
    savePath = None
    toPickle = False
    
    # path = 'wavefield_1.pkl'
#    path = '/user/home/opt/xl/xl/experiments/correctedAngle_coherence3/data/' #'/user/home/opt/xl/xl/experiments/lowEnergyBeam/data/'
    #'/user/home/opt/xl/xl/experiments/correctedAngle_coherence3/data/'
    
#    names =['atM1']
    
    path = '/user/home/opt/xl/xl/experiments/correctedAngle_polarisation/dataNew/'
    names = ['24nmTMincident','24nmTMexit','24nmTEincident','24nmTEexit']
    #['atM1','atM1_vp']
    #['24nmTMincident','24nmTMexit','24nmTEincident','24nmTEexit']
    files = [path + str(n) + '/' + str(n) + 'EforS.pkl' for n in names]
    
    picks = [pickle.load(open(f, 'rb')) for f in files]
    N = [(int(p[2]),int(p[3])) for p in picks]
    nTot = [n[0]*n[1] for n in N]
    res = [(p[4],p[5]) for p in picks]
    Ex = [p[0] for p in picks]
    Ey = [p[1] for p in picks]
    
    STOKES = []
    
    for ch, cv, r, n in zip(Ex,Ey,res,N): 
        
        plt.plot(ch)
        plt.show()
        plt.plot(cv)
        plt.show()
        
        # Defining parameters
        wf = SRWLWfr() #Initial Electric Field Wavefront    
        
        wf.allocate(1, n[0], n[1]) #Numbers of points vs Photon Energy (1), Horizontal and Vertical Positions (dummy)
        wf.mesh.zStart = 0 #Longitudinal Position [m] at which Electric Field has to be calculated, i.e. the position of the first optical element
        wf.mesh.eStart = 184.76 #Initial Photon Energy [eV]
        wf.mesh.eFin = 184.76 #Final Photon Energy [eV]
        wf.mesh.xStart = (-n[0]/2)*r[0] #Initial Horizontal Position [m]
        wf.mesh.xFin = (n[0]/2)*r[0] #Final Horizontal Position [m]
        wf.mesh.yStart = (-n[1]/2)*r[1] #Initial Vertical Position [m]
        wf.mesh.yFin = (n[1]/2)*r[1] #Final Vertical Position [m]
        wf.arEx = ch
        wf.arEy = cv
        wf.mesh.ne = 1
        
        w = wf
        
        print ('-----Getting Stokes parameters-----')
        S, Dx, Dy = getStokes(w, mutual=0, Fx = 1, Fy = 1)
        s= getStokesParamFromStokes(S,d=2)
        sn = normaliseStoke(s,d=2)
        plotStokes(s,dx=r[0], dy=r[1], extra=False, savePath=savePath)
        
        
        
        STOKES.append(sn)
        
    dS0tm = STOKES[1][0] - STOKES[0][0]
    dS1tm = STOKES[1][1] - STOKES[0][1]
    dS2tm = STOKES[1][2] - STOKES[0][2]
    dS3tm = STOKES[1][3] - STOKES[0][3]
    dStm = [dS0tm,dS1tm,dS2tm,dS3tm] 
    plotStokes(dStm,dx=res[0][0],dy=res[0][1])
    
    try:
        dS0te = STOKES[3][0] - STOKES[2][0]
        dS1te = STOKES[3][1] - STOKES[2][1]
        dS2te = STOKES[3][2] - STOKES[2][2]
        dS3te = STOKES[3][3] - STOKES[2][3]
    
        dSte = [dS0te,dS1te,dS2te,dS3te] 
        plotStokes(dSte,dx=res[0][0],dy=res[0][1])
    except IndexError:
        pass
    
    
    if toPickle:
        for i, sn in enumerate(STOKES):
            with open(path + names[i] + '_stokes.pkl', "wb") as f:
                pickle.dump(sn, f)
    else:
        pass
    
#    plotStokes([dS0,dS1,dS2,dS3],dx=res[0][0],dy=res[0][1])
#    
#    plt.plot(cL)
#    plt.title("from trey script")
#    plt.show()
    
# %%
if __name__ == '__main__':
    testStokes()
