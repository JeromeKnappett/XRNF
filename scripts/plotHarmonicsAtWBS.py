#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 10:24:08 2025

@author: jerome
"""


import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker
from matplotlib.ticker import MaxNLocator

savePath = '/home/jerome/Documents/PhD/Data/185/Harmonic_Content_atWBS'
fmat = 'eps'

M = [1,2,3,4,5]
Fw1 = [97192445049883.8,
       8215094450821.53,
       83559305373653.4,
       13880896453319.1,
       59033092423522.7,
       ]
Fw2 = [334490928796847,
       31019927370013.1,
       180128533622538,
       39250723220253.9,
       127541380136855,
       ]

wbsX, wbsY = [0.84,4],[1,3]


# HC1s = Fw1[0] / np.sum(Fw1[1::])
# HC2s = Fw1[1] / np.sum([Fw1[0]],Fw1[]:]
# HC3s = Fw1[2] / Fw1[1::]
# HC4s = Fw1[3] / Fw1[1::]
# HC5s = Fw1[4] / Fw1[1::]


# Hp = [[],[],[],[],[]]
HP1 = []
HP2 = []
for i,m in enumerate(M):
    hp1 = Fw1[i] / (np.sum(Fw1))# - Fw1[i])
    hp2 = Fw2[i] / (np.sum(Fw2))# - Fw2[i])

    # print(hp1)
    # print(hp2)
    # print('\n')
    HP1.append(hp1)
    HP2.append(hp2)
    

ax = plt.figure().gca()
ax.xaxis.set_major_locator(MaxNLocator(integer=True))
plt.plot(M,HP1,'x:',color='red', label='WBS=' + str(wbsX[0]) + r'$\times$' + str(wbsY[0]) + ' mm$^2$')
plt.plot(M,HP2,'x:',color='blue', label='WBS=' + str(wbsX[1]) + r'$\times$' + str(wbsY[1]) + ' mm$^2$')
plt.xlabel('Undulator Harmonic ($n$)')
plt.ylabel('$\zeta_{m}$ ($z$=14.3 m)')
plt.legend(frameon=True,fancybox=True,framealpha=1.0,fontsize=8)

ax.xaxis.set_minor_locator(ticker.NullLocator())
# plt.yscale('log')
plt.ylim(0,0.5)
if savePath:
    plt.savefig(savePath + '.' + fmat, format=fmat)
plt.show()

print(HP1)
print(HP2)

print('Total harmonic contamination  [%]')
print('small WBS:      ', 100*(np.sum(Fw1[1::]) / np.sum(Fw1)))
print('large WBS:      ', 100*(np.sum(Fw2[1::]) / np.sum(Fw2)))