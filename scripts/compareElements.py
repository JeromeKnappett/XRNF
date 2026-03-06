#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 10:28:47 2024

@author: -
"""

import numpy as np
import matplotlib.pyplot as plt
import xraydb as xrdb


from matplotlib import rcParams
rcParams['figure.figsize']=(4,1.5)
rcParams['figure.dpi']=300
rcParams.update({'font.size': 4})

E = [92,185,293]

materials = ['Mo','Cr','Ni','Ta','Si','SiO2','Si3N4','Cu','Au','Sn','Pt']

symbols = ['Be','C','N','O','Ne',
           'Al','Si','Ar','Ti','Cr','Fe','Co','Ni',
           'Cu', 'Zn', 'Ga', 'Ge','Kr','Zr','Mo','Ru',
           'Rh', 'Pd', 'Ag','In', 'Sn','Xe','Ta', 'W', 'Re', 'Os', 'Ir',
           'Pt', 'Au', 'Hg','Pb', 'Bi','U']

Reuv = []
Rbeuv = []
Rsxr = []

materials = symbols
for m in materials:
    D = xrdb.get_material(m)
    delta1,beta1,atlen1 = xrdb.xray_delta_beta(m, D[1], E[0])
    delta2,beta2,atlen2 = xrdb.xray_delta_beta(m, D[1], E[1])
    delta3,beta3,atlen3 = xrdb.xray_delta_beta(m, D[1], E[2])
    
    Reuv.append(delta1/beta1)
    Rbeuv.append(delta2/beta2)
    Rsxr.append(delta3/beta3)
    
    print(f'---- Properties of {m} @ {E[0]} eV ----')
    print(f'Density:                          {D[1]} g/cm^3')
    print(f'Delta:                            {delta1} ')   
    print(f'Beta:                             {beta1} ')   
    print(f'---- Properties of {m} @ {E[1]} eV ----')
    print(f'Density:                          {D[1]} g/cm^3')
    print(f'Delta:                            {delta2} ')   
    print(f'Beta:                             {beta2} ')   
    print(f'---- Properties of {m} @ {E[2]} eV ----')
    print(f'Density:                          {D[1]} g/cm^3')
    print(f'Delta:                            {delta3} ')   
    print(f'Beta:                             {beta3} ')   
    print('\n')

plt.plot(materials,Reuv,'.',label='EUV')
plt.plot(materials,Rbeuv,'.',label='BEUV')
plt.plot(materials,Rsxr,'.',label='SXR')
plt.xlabel('Material')
plt.ylabel('delta / beta')
plt.legend()
plt.plot()
    