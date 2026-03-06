#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 15 11:49:03 2024

@author: jerome
"""

import numpy as np
import matplotlib.pyplot as plt

## intensity HC (large wbs)
#HC0 = [2.7579046543999843, 0.24211744539999683, 1.443013762399972, 0.3233712223999934, 1.0338984299999872]
#HC1 = [4.25488735519999, 0.7599316359999949, 2.129378140000009, 1.4428164991999926, 1.0094900580000035]
#HC2 = [4.8734584864, 1.387417580799996, 1.462379674400005, 1.9729589599999988, 0.9156544939999985]
## flux HC
#HC0 = [3.2928788480000004, 0.287083488, 1.7092414720000002, 0.380875136, 1.221138816]
#HC1 = [51.05865105919989, 9.119179750399939, 25.552535193600107, 17.31379704319991, 12.113878720000042]
#HC2 = [58.4814975232, 16.649011443199953, 17.548556019200063, 23.675508019199988, 10.987852895999982]

# flux HC (small wbs)
HC0 = [0.957570176, 0.07738929600000001, 0.806494272, 0.136922064, 0.594228928]
HC1 = [10.373134633600019, 1.8594073871999968, 5.245392112000129, 4.258431232000011, 1.4920700600000345]
HC2 = [5.736751427200041, 1.420325798400006, 0.5656065854000139, 1.8547698432000148, 0.49165643499999884]

## first 3 harmonics
#H1p = [h[0]/np.sum([h[0],h[1],h[2]]) for h in [HC0,HC1,HC2]]
#H2p = [h[1]/np.sum([h[0],h[1],h[2]]) for h in [HC0,HC1,HC2]]
#H3p = [h[2]/np.sum([h[0],h[1],h[2]]) for h in [HC0,HC1,HC2]]
#H4p = [h[3]/np.sum([h[0],h[1],h[2]]) for h in [HC0,HC1,HC2]]
#H5p = [h[4]/np.sum([h[0],h[1],h[2]]) for h in [HC0,HC1,HC2]]

# first 5 harmonics
H1p = [h[0]/np.sum(h) for h in [HC0,HC1,HC2]]
H2p = [h[1]/np.sum(h) for h in [HC0,HC1,HC2]]
H3p = [h[2]/np.sum(h) for h in [HC0,HC1,HC2]]
H4p = [h[3]/np.sum(h) for h in [HC0,HC1,HC2]]
H5p = [h[4]/np.sum(h) for h in [HC0,HC1,HC2]]

print(H1p)
print(H2p)
print(H3p)
print(H4p)
print(H5p)
#
M = [0,0.738,1.63]
plt.plot(M,H1p,label='n=1')
plt.plot(M,H2p,'o:',label='n=2')
plt.plot(M,H3p,'o:',label='n=3')
#plt.plot(M,H4p,'o:',label='n=4')
#plt.plot(M,H5p,'o:',label='n=5')
plt.plot(M,[1-h for h in H1p],'o:',label='sum')
plt.legend()
plt.show()

print(1-H1p[0])
#        
#    plt.plot(energy[0:12],[h[1]*100 for h in H[0:12]],style,color=colours[0],label='2nd')#+name)
#    plt.plot(energy[0:12],[h[2]*100 for h in H[0:12]],style,color=colours[1],label='3rd')#+name)
#    plt.plot(energy[0:12],h4[0:12],style,color='b',label='4th')#+name)
#    h2 = [h[1]*100 for h in H[0:12]]
#    h3 = [h[2]*100 for h in H[0:12]]
#    HSUM = [H2 + H3 + H4 for H2,H3,H4 in zip(h2,h3,h4)] #np.sum([h2,h3,h4])
#    print(HSUM)
#    plt.plot(energy[0:12],HSUM,style,color='y',label='sum')#+name)