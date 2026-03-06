#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 15:04:04 2022

@author: -
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import pylab
pylab.rcParams['figure.figsize'] = (10.0, 8.0)

def round_sig(x, sig=2):
    from math import log10, floor
    if x != 0:
        return round(x, sig-int(floor(log10(abs(x))))-1)
    else:
        return x
    
# %%
def getLineProfile(a,axis=0, mid=None, show=False):
    nx, ny = np.shape(a)[1], np.shape(a)[0]
    if mid == None:
        midX, midY = int(nx/2), int(ny/2)
    else:
        midX, midY = int(mid[1]), int(mid[0])    
    # print(midX)
    
    if axis == 0:
        p = a[:,midX]
        title = 'vertical profile'
    elif axis == 1:
        p = a[midY,:]
        title = 'horizontal profile'
    
    if show:
        plt.plot(p)
        plt.title(title)
        plt.show()
    
    return p



def propPlot(I,zRange,zPlanes,res=1,axis='hor',log=False,lMin=1,savePath=False,plotProfiles=False,verbose=True):
    cmap='viridis'
    p=[]
    for e,i in enumerate(I):
        if verbose:
            print(f'Getting profile #{e+1} out of {len(I)}')
        if axis=='hor':
            profile = getLineProfile(i,axis=1)
        elif axis=='ver':
            profile = getLineProfile(i,axis=0)
        p.append(profile)
#        print(f'max p: {np.max(profile)}')
        if plotProfiles:
            plt.plot(profile, label=f'#{e}')
        else:
            pass
    if plotProfiles:
        plt.legend()
        plt.show()
#    print(np.shape(p))
    nx,ny = np.shape(p)[0],np.shape(p)[1]
    dx = zRange/zPlanes
#    print('Here')
    p = np.squeeze(np.transpose(p))
    #p = [[i if i>1.0e5 else 0.0 for i in row] for row in p]

#    maxp = np.
    if log:
        
        print(lMin)
        print(abs(np.max(p)))
        im = plt.imshow(p, aspect='auto',norm=LogNorm(vmin=lMin,vmax=abs(np.nanmax(p))),cmap=cmap)
    else:
        im = plt.imshow(p, aspect='auto',cmap=cmap)
    plt.yticks([int((ny-1)*(b/(9-1))) for b in range(0,9)],
               [round_sig(ny*res*(a/(9-1))) for a in range(-int((9-1)/2),int((9/2 + 1)))],fontsize=10 )
    plt.xticks([int((nx-1)*(b/(9-1))) for b in range(0,9)],
               [round_sig(nx*dx*(a/(9-1))) for a in  range(0,int((9 + 1)))],fontsize=10)
#    plt.xticks([int((nx-1)*(b/(9-1))) for b in range(0,9)],
#               [round_sig(nx*dx*(a/(9-1))) for a in  range(-int((9-1)/2),int((9/2 + 1)))],fontsize=10)
    plt.colorbar(label='intensity [a.u]').ax.tick_params(labelsize=10)
    plt.xlabel('Propagation Distance [m]',fontsize=15 )#[\u03bcm]')
    if axis == 'hor':
        plt.ylabel('x [m]',fontsize=15 )#[\u03bcm]')
    if axis == 'ver':
        plt.ylabel('y [m]',fontsize=15 )#[\u03bcm]')
    plt.title(label='Propagation Plot')
    plt.tight_layout()
    if savePath:
        print(f'Saving propagation plot to: {savePath}')
        plt.savefig(savePath + '.eps', dpi=300)
        import pickle
        with open(savePath + '.pkl', "wb") as f:
            pickle.dump(im, f)
    plt.show()
    
    
def testPropPlot():
    import os
    import tifffile
    path= '/user/home/opt/xl/xl/experiments/focusedIL/data/maskExitUF/driftVol/intensity/'
    #'/user/home/opt/xl/xl/experiments/focusedIL/data/maskExitUF/driftVol/intensity/'
    #'/user/home/opt/xl/xl/experiments/propDisTolerance/data/tiffs/' 
    #'/user/home/opt/xl/xl/experiments/focusedIL/data/atFZP/driftVol/intensity/'
    
    tiffs = []
    for file in os.listdir(path):
        if file.endswith(".tif"):
            tiffs.append(file)
            
#    print(tiffs.sort(key='float'))
    sortedTiffs = sorted(tiffs, key=lambda x: float(x[:-4]))
    print(tiffs)
    print(sortedTiffs)
    I = [tifffile.imread(path + t) for t in sortedTiffs]
    zRange =300.0e-6 #20*dof
    zPlanes=60
    
    propPlot(I,zRange,zPlanes,
             res=6.3628772840996375e-09,
             axis='hor',
             log=True)
#5.295857275073647e-09,1.0950733509158233e-07

def testPropPlotManual():
    res = [(3.317631116498579e-09,5.0412035231282055e-09),
           (4.3861701380034884e-07,6.663653540690268e-07),
           (8.772501331310375e-07,1.33279809558251e-06),
           (1.3158832524617261e-06,1.999230837095993e-06),
           (1.7545163717924144e-06,2.6656635786094766e-06),
           (2.193149491123103e-06,3.3320963201229596e-06),
           (2.6317826104537913e-06,3.998529061636443e-06),
           (3.07041572978448e-06,4.664961803149926e-06),
           (3.5090488491151696e-06,5.331394544663409e-06),
           (3.947681968445858e-06,5.9978272861768915e-06),
           (4.3863150877765454e-06,6.664260027690376e-06),
           (4.824948207107235e-06,7.330692769203858e-06),
           (5.263581326437925e-06,7.997125510717343e-06)]
    
    dx,dy = [r[0] for r in res], [r[1] for r in res]
    print(np.diff(dx))
    print(np.diff(dy))
    print(dx[0]-np.diff(dx).mean())
    print(dy[0]-np.diff(dy).mean())
    
    files = ['/user/home/opt/xl/xl/experiments/speckleFocused/data/focusCheck' + str(r) + 'mm/intensity.tif' for r in range(7,14)]
    
           
if __name__ == '__main__':
#    testPropPlot()
    #testPropPlotManual()
    testPropPlot()
    