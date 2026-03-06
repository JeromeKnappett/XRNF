#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 14:56:31 2023

@author: -
"""
import numpy as np
import matplotlib.pyplot as plt
import pickle

plt.rcParams["figure.figsize"] = (5,4)
plt.rcParams.update({'font.size': 50})
FSIZE = 12

data = pickle.load(open('/user/home/opt/xl/xl/experiments/BEUVbeamComparison_HF/data/fixed/simData_cff2.pkl', 'rb'))

SX = data[0]
F = data[1]
IG = data[2]
IC = data[3]
fxX = data[4]
fwY = data[5]

fig, ax = plt.subplots(1,1)

ax2 = ax.twinx()

ax.plot(SX,IG,'o',label='$I^G_1$',color='black',markerfacecolor='none')
ax2.plot(SX,F,'o',label='$\Phi_1$ x 6',color='red',markerfacecolor='none')
ax.set_xlabel('SSA size [microns]',fontsize=FSIZE)
ax.set_ylabel("$I^G_1$ [ph/s/cm$^2$]",fontsize=FSIZE)#"Intensity [ph/s/cm$^2$]")
ax2.set_ylabel('$\Phi_1$ [ph/s]',fontsize=FSIZE)
ax.spines['left'].set_color('black')
ax.spines['right'].set_color('red')

ax.yaxis.label.set_color('black')
ax.tick_params(axis='y', colors='black')
ax2.yaxis.label.set_color('red')
ax2.tick_params(axis='y', colors='red')



# plt.plot(SX,IG,'o',label='$I^G_1$',color='black',markerfacecolor='none')#' [ph/s/cm$^2$]')
# plt.plot(SX,[f*6 for f in F],'o',label='$\Phi_1$ x 6',color='red',markerfacecolor='none')
# plt.legend()
plt.show()

# fig, ax = plt.subplots()
print(IG)