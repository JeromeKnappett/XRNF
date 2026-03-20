#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 10:37:19 2023

@author: jerome
"""
import numpy as np
import matplotlib.pyplot as plt

dirPath = '/home/jerome/dev/data/BEUVcoherenceRoughness/'

 #MULTIPLE
files = ['dataStructureNEW.pkl','dataStructure50NEW.pkl']

labelX = '$\sigma [nm]$'
labelY = ['$C_{Composite}$', '$Fidelity$', '$NILS$', '$LWR$', '$\eta_{\pm 1}$','$NILS_{\sigma_n}$']
legend = ['$d = 27 \mu m$, $c_y = 2 nm$','$d = 27 \mu m$, $c_y = 10 nm$','$d = 50 \mu m$, $c_y = 2 nm$','$d = 50 \mu m$, $c_y = 10 nm$']

savePath = None
#'/home/jerome/onedriver/Documents/PhD/Figures/forPosters/contrastLERNILSLWR_4metrics.eps'

 # # #MULTIPLE
picks = [pickle.load(open(dirPath + f, 'rb')) for f in files]

sigma = 0
cy = 1
michelson = 2#1#2
rms = 3#2#3
composite = 4#3#4
fidelity = 5
nils = 6
_nils = 7#4#7
lwr = 8
eff = 9


# # #MULTIPLE
A = [[p[composite][0:5],p[fidelity][0:5],p[nils][0:5],p[lwr][0:5],p[eff][0:5],p[_nils][0:5]] for p in picks]
B = [[p[composite][20:25],p[fidelity][20:25],p[nils][20:25],p[lwr][20:25],p[eff][20:25],p[_nils][20:25]] for p in picks]

X = [p[0][0:5] for p in picks]
#    X = X[0][1::]

print(np.shape(A))

for a in A:
    print(a)
#        b = np.reshape(a,[5,5])
##        print(np.shape(b))
print(X)
#    
fig, ax = plt.subplots(2,3)
ax[0,0].plot(X[0],A[0][0],'x:')
ax[0,0].plot(X[0],B[0][0],'x:')
ax[0,0].plot(X[0],A[1][0],'o:')
ax[0,0].plot(X[0],B[1][0],'o:')
ax[0,0].set_ylabel(labelY[0])
ax[0,1].plot(X[0],A[0][1],'x:')
ax[0,1].plot(X[0],B[0][1],'x:')
ax[0,1].plot(X[0],A[1][1],'o:')
ax[0,1].plot(X[0],B[1][1],'o:')
ax[0,1].set_ylabel(labelY[1])
ax[0,2].plot(X[0],A[0][2],'x:')
ax[0,2].plot(X[0],B[0][2],'x:')
ax[0,2].plot(X[0],A[1][2],'o:')
ax[0,2].plot(X[0],B[1][2],'o:')
ax[0,2].set_ylabel(labelY[2])
ax[1,0].plot(X[0],A[0][3],'x:')
ax[1,0].plot(X[0],B[0][3],'x:')
ax[1,0].plot(X[0],A[1][3],'o:')
ax[1,0].plot(X[0],B[1][3],'o:')
ax[1,0].set_ylabel(labelY[3])
ax[1,0].set_xlabel(labelX)
ax[1,1].plot(X[0],A[0][4],'x:')
ax[1,1].plot(X[0],B[0][4],'x:')
ax[1,1].plot(X[0],A[1][4],'o:')
ax[1,1].plot(X[0],B[1][4],'o:')
ax[1,1].set_ylabel(labelY[4])
ax[1,1].set_xlabel(labelX)
ax[1,2].plot(X[0],A[0][5],'x:')
ax[1,2].plot(X[0],B[0][5],'x:')
ax[1,2].plot(X[0],A[1][5],'o:')
ax[1,2].plot(X[0],B[1][5],'o:')
ax[1,2].set_ylabel(labelY[5])
ax[1,2].set_xlabel(labelX)
fig.tight_layout()
fig.subplots_adjust(bottom=0.2)   ##  Need to play with this number.
fig.legend(labels=legend, loc="lower center", ncol=4) 
plt.show()
