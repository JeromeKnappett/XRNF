#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 10:15:43 2023

@author: jerome
"""
import numpy as np
import pickle

dirPath = '/home/jerome/dev/data/BEUVcoherenceRoughness/'
files = ['dataStructureNEW.pkl','dataStructureNEW_50.pkl']
labels =  ['$\sigma$', '$c_y$', '$C_M$', '$C_{RMS}$', '$C_{Composite}$', '$Fidelity$', '$NILS$', '$NILS_{\sigma_n}$', '$LWR$', '$\eta_{m=\pm1}$','$D$']
#     ['$\sigma$', '$c_y$', '$C_M$', '$C_{RMS}$', '$C_{Composite}$', '$Fidelity$', '$NILS$', '$NILS_{\sigma_n}$', '$LWR$', '$\eta_{m=0}$', '$\eta_{m=\pm1}$']
D = [27.5,27.5,27.5,27.5,27.5,
     27.5,27.5,27.5,27.5,27.5,
     27.5,27.5,27.5,27.5,27.5,
     27.5,27.5,27.5,27.5,27.5,
     27.5,27.5,27.5,27.5,27.5,
     50.0,50.0,50.0,50.0,50.0,
     50.0,50.0,50.0,50.0,50.0,
     50.0,50.0,50.0,50.0,50.0,
     50.0,50.0,50.0,50.0,50.0,
     50.0,50.0,50.0,50.0,50.0]

#savePath = '/home/jerome/dev/data/BEUVcoherenceRoughness/combined_'
picks = [pickle.load(open(dirPath + f, 'rb')) for f in files]

#    print(np.shape(picks))
#    print(picks[1])
P = []
for p in picks[1]:
#        print(p)
    p = [p[5],p[6],p[7],p[8],p[9],
         p[10],p[11],p[12],p[13],p[14],
         p[15],p[16],p[17],p[18],p[19],
         p[20],p[21],p[22],p[23],p[24],
         p[0],p[1],p[2],p[3],p[4]]
#        print("NEW")
#        print(p)
    P.append(p)
#    print(picks[1])
#    picks[1][1] = []
picks[1] = P
#    print("HERE")
#    print(picks[0])
#    print(picks[1])
picks[1] = [picks[1][0],picks[1][1],picks[1][2],picks[1][3],picks[1][4],picks[1][5],picks[1][6],picks[1][7],picks[1][8],picks[1][9]]

with open(dirPath + 'dataStructure50NEW.pkl', "wb") as f:
            pickle.dump(picks[1], f)


