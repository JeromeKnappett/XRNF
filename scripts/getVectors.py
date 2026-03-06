#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 10:39:19 2022

@author: -
"""
import numpy as np
import uti_math

def getVectors(angX,angY):
    x,y,z = np.tan(angX), np.tan(angY), 1
    nvx = x/(np.sqrt((x**2)+(y**2)+(z**2)))
    nvy = y/(np.sqrt((x**2)+(y**2)+(z**2)))
    nvz = z/(np.sqrt((x**2)+(y**2)+(z**2)))
    tvx = angX*abs(nvz)
    tvy = angY*abs(nvz)    
    
    nv = [nvx, nvy, nvz]
    tv = [tvx, tvy, -(nvx*tvx + nvy*tvy)/nvz]; 
    sv = uti_math.vect3_prod_v(nv, tv)
    ex = [nvx,0,0]; ey = [0,nvy,0]; ez = [0,0,nvz]
    
    print(f"Normal vector (x,y,z): {[1-n for n in nv]}")
    print(f"Tangential vector (x,y,z): {[1-t for t in tv]}")
    print('Loc. Frame nv=', nv, ' ez=', ez)
    print([ex, ey, ez])
    print('\n----- FOR SRW -----')
    print('nvx = ', nv[1])
    print('nvy = ', nv[2])
    print('nvz = ', -nv[0])
    print('tvx = ', nv[1])
    print('tvy = ', nv[0])
    return [[tv, sv, nv], [ex, ey, ez], [ex, ey, ez]]

def test():
    #E=293, Cff=2, grating angle = 3.04321
    
    ax =np.deg2rad(3.04321)#3.3826)
    #66.88764919e-3 #np.deg2rad(3.36174)#82.729e-3 #9.184164985e-3
    ay = 0
    
    getVectors(ax,ay)
    
if __name__=='__main__':
    test()