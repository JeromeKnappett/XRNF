#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  1 09:53:21 2020

@author: gvanriessen
"""
try:
    import xrnl.interferenceGratingModels as gm
except ModuleNotFoundError:
    import interferenceGratingModels as gm
import os
import numpy as np
import matplotlib.pyplot as plt
import csv
from pprint import pprint



def pretty(d, indent=0):
   for key, value in d.items():
      print('\t' * indent + str(key))
      if isinstance(value, dict):
         pretty(value, indent+1)
      else:
         print('\t' * (indent+1) + str(value))
         

def getWFDictPartial(w):
    '''
    Return wavefront dictionary excluding E-field entries, e.g. arrEhor, arrEver
    '''   
    d = w._to_dict()
    return {k:v for k, v in d.items() if not k.startswith('data/arrE')}

    
def printWFDictUgly(w):
    '''
    Example showing how to traverse the wavefront dictionary
    '''    
    for (key, value) in w._wf_fields.items():   
        try: 
            # python3 hack
            if isinstance(key, bytes):
                key = key.decode('utf-8')
                
            if not key.startswith('data/arrE'):  #let's not print the data
                print(key,' ', value.value, ' ',value.attributes['units'], ' ',
                      #value.attributes['limits'], ' ',
                      value.attributes['description'], ' ',
                      value.attributes['alias']
                      )
        except: 
            pass


def wfrPropertiesInterference(*args):   
    #args = list(args) 
    filePath, wfr, index, z, dataPath = args[0]
    print('File path: {}'.format(filePath))
 
    metrics = {'index': index, 'z': z, 'datafile' : dataPath}
    
    x =  np.linspace(wfr.params.xCentre-wfr.params.Rx/2,
                      wfr.params.xCentre+wfr.params.Rx/2,
                      wfr.params.Mesh.nx)
    y =  np.linspace(wfr.params.yCentre-wfr.params.Ry/2,
                      wfr.params.yCentre+wfr.params.Ry/2,
                      wfr.params.Mesh.ny)
    metrics['x'] = x
    metrics['y'] = y
     
    profiles={}
    areas={}
    for pol in ['total','horizontal','vertical']:
        I = wfr.get_intensity(polarization=pol)
    
        P = wfr.get_phase(polarization=pol)
        for prop,W in zip(['intensity','phase'],[I,P]):
            
#            try:
#                
#                ''' analyse 2D combinations of polarisation modes and type (intensity | phase) '''
#                akey = '{}{}'.format(prop.capitalize(), pol.capitalize()) 
#                print('Area: '+ akey)
#                Cm = gm.gratingContrastMichelson(W)
#                Crms = gm.gratingContrastRMS(W)
#                C, C1, C2 = gm.meanDynamicRange(W) 
#                IOD, IODM, H, binEdges, binCenters = gm.integralOpticalDensity(W)
#                
#                areas[akey] = {'contrastMichelson' : Cm,
#                             'contrastRMS': Crms,
#                             'meanDynamicRangeC' : C,
#                             'meanDynamicRangeC1' : C1,
#                             'meanDynamicRangeC2' : C2,
#                             }
#            except Exception as e: print(e)
                
               
            
            for axis, index in zip(['x','y'],[0,1]):
                 try:
                     pkey = prop.capitalize() + pol.capitalize() + axis.capitalize()
                     print('Profile: '+ pkey)
                     ny=wfr.params.Mesh.ny
                     nx=wfr.params.Mesh.nx
                     if  axis is 'x':
                         ROI = ((0,ny//2),(nx,ny//2+1))
                         axisVals = x
                     if axis is 'y':
                         ROI = ((nx//2,0),(nx//2+1,ny))
                         axisVals = y
                     
                     prof = gm.lineProfile(W, ROI=ROI, AXIS = index)
                     Cm = gm.gratingContrastMichelson(prof)
                     Crms = gm.gratingContrastRMS(prof)
    
                     C, C1, C2 = gm.meanDynamicRange(prof) 
                     IOD, IODM, H, binEdges, binCenters =gm.integralOpticalDensity(prof)
                     Cf,  Am, Fr, peakFr  = gm.gratingContrastFourier(prof,axisVals, show=False)
            
                     plt.plot(axisVals,prof)
                     plt.show()
            
                     profiles[pkey] = {
                             'profile' : prof,
                             'contrastMichelson' : Cm,
                             'contrastRMS': Crms,
                             'meanDynamicRangeC' : C,
                             'meanDynamicRangeC1' : C1,
                             'meanDynamicRangeC2' : C2,
                             'integratedOpticalDensity' : IOD,
                             'integratedOpticalDensityMax' : IODM,
                             'histogram' : H,
                             'histogramBins' : binEdges,
                             'contrastFourier' : Cf,
                             'fundamentalFrequency' : peakFr,
                             'fourierFrequency' : Fr,
                             'fourierAmplitude' : Am
                             }
                 
                 except Exception as e: print(e)
                 
    metrics['profiles'] = profiles
    metrics['areas'] = areas            
    metrics['params'] = getWFDictPartial(wfr)
    
    #fname = filePath+'metrics_'+str(index)
    
    
#    with open(fname, 'wt') as out:
#        print(wfr.__str__(), file=out)
#        pprint(metrics, stream=out)
        
#    with open(fname, 'w') as f:
#        for key in metrics.keys():
#            f.write("%s,%s\n"%(key,metrics[key]))
#    print("Wrote wavefront metrics to %s"%fname )

    return metrics
