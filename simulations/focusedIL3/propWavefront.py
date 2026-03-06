#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 12:51:17 2022

@author: -
"""

use_gpu = False

if use_gpu:
    import afnumpy as np
    import afnumpy.fft as fft
    use = 'afnumpy/GPU'
else:
    import numpy as np
    import numpy.fft as fft
    use = 'numpy/CPU'

#from wpg import srwlpy as srwl
from wpg.useful_code.wfrutils import get_mesh
from utils import plotWavefront
from driftVol import driftVol
from propPlot import propPlot

def propWavefront():
        
    # test for Jeromes project
    # propagate from input wavefield, which is at the plane of a FZP, 
    # to some distance given by zrange
    
    from wpg.optical_elements import Use_PP
    from wpg.wavefront import Wavefront
    from wfrMetrics import printWFDictUgly
    #from extensions.beamlineExt import bl
    
    path = '/user/home/opt/xl/xl/experiments/focusedIL3/data/maskExit_wap/'
   # initialWavefront='/opt/wpg/wpg/extensions/in/50Slices63dLTZP_simulationData/wf_noCS.h5'
    initialWavefront= path + 'wf_final.hdf'
    outPath= path + 'driftVol/'
    
    zRange = 300.0e-6 #20*dof
    zPlanes= 60
    
    
    wf = Wavefront()
    wf.load_hdf5(initialWavefront)
    plotWavefront(wf, 'Wavefront input', cuts=True)
    
    [nx, ny, xmin, xmax, ymin, ymax] = get_mesh(wf)
    dx, dy = (xmax-xmin)/nx, (ymax-ymin)/ny
    print('Mesh grid period: {}x{}'.format(dx,dy))
    
#    # define driftVol
#    distances=(0.0,zRange,zPlanes)
#    dVol=driftVol(distances,
#                  Use_PP(),#(semi_analytical_treatment=1.0,zoom=1, sampling=1),
#                  outputPath = outPath, 
#                  zoomXOutput = 1.0,     # reduce size of output, keep all significant features
#                  zoomYOutput = 1.0,     # reduce size of output, keep all significant features
#                  resampleOutput=1.0,     # reduce size of output, proportional loss of resolution
#                  method=1,
#                  saveIntensity=True,
#                  saveComplex=False,
#                  postProcessFunction=None)
#    
#    #beamline.append(dVol,Use_PP())
#    
#    # Propagate through driftVol
#    dVol.propagate(wf)
    
    plotPropWave(outPath + 'intensity/',
                 zRange,zPlanes,res=dx,axis='hor',log=True, lMin=1e12)
#    printWFDictUgly(wf)

def plotPropWave(path,zRange,zPlanes,res,axis,startPlane=0,log=False,lMin=1):
    import os
    import tifffile
#    path= '/user/home/opt/xl/xl/experiments/speckleFocused/data/30mm/driftVol/intensity/'
    
    tiffs = []
    for file in os.listdir(path):
        if file.endswith(".tif"):
            tiffs.append(file)
            
#    print(tiffs.sort(key='float'))
    sortedTiffs = sorted(tiffs, key=lambda x: float(x[:-4]))[startPlane::]
#    print(tiffs)
    print(sortedTiffs)
    I = [tifffile.imread(path + t) for t in sortedTiffs]
    
#    if startPlane == 0:
#        zRange = zRange
#    else:
    zRange = (zRange/zPlanes)*(zPlanes-startPlane)
    zPlanes= int(zPlanes - startPlane) 
    
    propPlot(I,zRange,zPlanes,
             res=res,
             axis=axis,
             log=log,lMin=lMin)
    #1.0993007331597748e-05x1.0908304144859974e-05

if __name__=='__main__':
    propWavefront()
#    plotPropWave()
    