#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 15:27:48 2024

@author: -
"""

import numpy as np
import xraydb
import pandas as pd

def SXRbeamlineTransmission(E,PGM_eff):
    
    m1 = 1
    m2 = 2.28214 #2
    m3 = 1.5
    
    R = []
    EN = []
    
    for e in E:
        r1 = xraydb.mirror_reflectivity("Au", np.deg2rad(m1), e, polarization="p")
        r2 = xraydb.mirror_reflectivity("Au", np.deg2rad(m2), e, polarization="s")
        r3 = xraydb.mirror_reflectivity("Au", np.deg2rad(m3), e, polarization="p")
        ePGM = PGM_eff
        
        print('M1 reflectivity: ', r1)
        print('M2 reflectivity: ', r2)
        print('M3 reflectivity: ', r3)
        
        R.append(r1*r2*r3*ePGM)
        EN.append(e/1000)
    
    
    T = pd.DataFrame({'Photon energy (eV)': EN,'Reflectivity': R})
    
    return T



def test():
    writePath = '/user/home/opt/xl/xl/'
    # E = np.linspace(90,33000.0, num = 33000)
    E = [293.0]
    T = SXRbeamlineTransmission(E, PGM_eff=1)
    print(T)    
    # T.to_csv(writePath + 'beamlineTransmission.csv',index=False)
        
if __name__ == '__main__':
    test()