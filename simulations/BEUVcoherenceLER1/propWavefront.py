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
    
    multi =  False
    values = ['001','005','01','05','1','5']
    
    path = '/user/home/opt/xl/xl/experiments/maskLER1/data/rms10exit'
    
    if multi:
        for i, p in enumerate(path):
            print(p)
            initialWavefront= p + '/wf_final.hdf'
            outPath= p + '/driftVol/'
            savePath = p + '/propagationPlot.png'
            
            zRange = values[i]*0.0002
            zPlanes= 50
            
            
            wf = Wavefront()
            wf.load_hdf5(initialWavefront)
            plotWavefront(wf, 'Wavefront input', cuts=True)
            
            [nx, ny, xmin, xmax, ymin, ymax] = get_mesh(wf)
            dx, dy = (xmax-xmin)/nx, (ymax-ymin)/ny
            print('Mesh grid period: {}x{}'.format(dx,dy))
            
            # define driftVol
            distances=(0.0,zRange,zPlanes)
            dVol=driftVol(distances,
                          [0, 0, 1.0, 0, 0, 1.0, 10.0, 1.0, 1.0, 0, 0, 0],#Use_PP(),#(semi_analytical_treatment=1.0,zoom=1, sampling=1),
                          outputPath = outPath, 
                          zoomXOutput = 1.0,     # reduce size of output, keep all significant features
                          zoomYOutput = 1.0,     # reduce size of output, keep all significant features
                          resampleOutput=1.0,     # reduce size of output, proportional loss of resolution
                          method=1,
                          saveIntensity=True,
                          saveComplex=False,
                          postProcessFunction=None)
            
        #    beamline.append(dVol,Use_PP())
            
            # Propagate through driftVol
            dVol.propagate(wf)
            
            plotPropWave(outPath + 'intensity/',
                         zRange,zPlanes,res=dx,axis='hor',log=True, lMin=1e10, savePath=savePath,plotProfiles=True)
   
    else:
        initialWavefront= path + '/wf_final.hdf'
        outPath= path + '/driftVol/'
        savePath = path + '/propagationPlot'
        
        zRange = 300e-6 #225e-6 #was 300e-6
        zPlanes= 50 # 150    #was 200
        
        
        wf = Wavefront()
        wf.load_hdf5(initialWavefront)
        plotWavefront(wf, 'Wavefront input', cuts=True)
        
        [nx, ny, xmin, xmax, ymin, ymax] = get_mesh(wf)
        dx, dy = (xmax-xmin)/nx, (ymax-ymin)/ny
        print('Mesh grid period: {}x{}'.format(dx,dy))
#        
        # define driftVol
        distances=(0.0,zRange,zPlanes)
        dVol=driftVol(distances,
                      [0, 0, 1.0, 0, 0, 1.0, 1.0, 1.0, 1.0, 0, 0, 0],
                      #[0, 0, 1.0, 0, 0, 1.4, 10.0, 1.0, 0.125, 0, 0, 0],# Use_PP(),#(semi_analytical_treatment=1.0,zoom=1, sampling=1),
                      outputPath = outPath, 
                      zoomXOutput = 1.0,     # reduce size of output, keep all significant features
                      zoomYOutput = 1.0,     # reduce size of output, keep all significant features
                      resampleOutput=1.0,     # reduce size of output, proportional loss of resolution
                      method=1,
                      saveIntensity=True,
                      saveComplex=False,
                      postProcessFunction=None)
        
    #    beamline.append(dVol,Use_PP())
        
        # Propagate through driftVol
        dVol.propagate(wf)
#        
        plotPropWave(outPath + 'intensity/',
                     zRange,zPlanes,res=dx,axis='hor',log=True, lMin=1e11, savePath=savePath,plotProfiles=False)
#        animatePropWave(outPath + 'intensity/')
#        printWFDictUgly(wf)

def plotPropWave(path,zRange,zPlanes,res,axis,startPlane=0,log=False,lMin=1,savePath=False,plotProfiles=False):
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
             log=log,lMin=lMin,
             savePath=savePath,
             plotProfiles=plotProfiles)
    #1.0993007331597748e-05x1.0908304144859974e-05
    
def animatePropWave(path,startPlane=0):
    import os
    import tifffile
    from utils import animateWF
    
    tiffs = []
    for file in os.listdir(path):
        if file.endswith(".tif"):
            tiffs.append(file)
            
#    print(tiffs.sort(key='float'))
    sortedTiffs = sorted(tiffs, key=lambda x: float(x[:-4]))[startPlane::]
#    print(tiffs)
    print(sortedTiffs)
    I = [tifffile.imread(path + t) for t in sortedTiffs]
    
    animateWF(I,_filename=path+'movie.mp4')
    
    
    
#def animateWF(wf,_filename=''):
#    """
#    wf should be a wf with multiple slices... For now (Testing) it is a list of image arrays
#    if filename given a movie file will be saved
#    """
#
#    import matplotlib.animation as animation
#
#    fig = plt.figure()
#
#    ims = []
#
#    for i in range(0,len(wf)-1):
#        print(i)
#
#        im = plt.imshow(wf[i], animated=True,aspect='auto') #aspect added by JK
#        ims.append([im])
#
#
#    ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True, repeat_delay=500)
#    plt.show()
#
#    if _filename != '':
#        ani.save(_filename)

def test():
    
    import os
    path = '/user/home/opt/xl/xl/experiments/blockThickness/data/merge/driftVol/'
    
    tiffs = []
    for file in os.listdir(path):
        if file.endswith(".tif"):
            tiffs.append(file)
            
#    print(tiffs.sort(key='float'))
    sortedTiffs = sorted(tiffs, key=lambda x: float(x[:-4]))
    
    print(sortedTiffs)
    
    for index, file in enumerate(sortedTiffs):
        os.rename(os.path.join(path, file), os.path.join(path, ''.join([str(index+ 74), '.tif'])))
#    
    tiffs = []
    for file in os.listdir(path):
        if file.endswith(".tif"):
            tiffs.append(file)
            
#    print(tiffs.sort(key='float'))
    sortedTiffs = sorted(tiffs, key=lambda x: float(x[:-4]))
    print(sortedTiffs)
#    plotPropWave(outPath + 'intensity/',
#                 zRange,zPlanes,res=dx,axis='hor',log=True, 
#                 lMin=5e11, savePath=savePath,plotProfiles=True)


if __name__=='__main__':
#    test()
    propWavefront()
#    plotPropWave()
    