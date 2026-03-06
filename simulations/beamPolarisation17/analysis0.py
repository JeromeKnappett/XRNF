#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 17:16:04 2020


This is a basic example of how to handle the pickled results from a batch 
simulation (i.e. from doExperiment/runner)

@author: -
"""
import numpy as np
import matplotlib.pyplot as plt
import pickle
from matplotlib.font_manager import FontProperties

#import xl.runner as runner

dirPath = '/user/home/opt/xl/xl/experiments/beamPolarisation17/data/'

batchOutputFile = dirPath + 't180/results.pickle'




def trials(results):
        return [k for k,v in results.items()]
       
def resultsKeys(results):
        return [k for k,v  in results['trial_0']['results'].items()]
    
def parameterKeys(results):
        return [k for k,v  in results['trial_0']['parameters'].items()]

    
def listValues(results, key):
        try:
            V =  [results[trial]['results'][key] for trial in trials(results)] 
        except KeyError:
            try:
                V =  [results[trial]['parameters'][key] for trial in trials(results)] 
            except KeyError:
                print('Valid values not found for ' + key)
                V=[]
        
        return V
    
def plot(results,*args,**kwargs):
                
        xKey = kwargs['x']
        yKey = kwargs['y']
            
        x = listValues(results,xKey)
        y = listValues(results,yKey)
               
        if x !=[] and y!=[]:
            fontP = FontProperties()
            fontP.set_size('xx-small')    
            plt.plot(x,y,'o')   #label=...
            plt.xlabel(xKey)
            plt.ylabel(yKey)
            plt.legend(loc='upper left', bbox_to_anchor=(1, 0.5), prop=fontP)
            plt.show()   
    

#        
results = pickle.load( open(batchOutputFile, 'rb')  )


x = listValues(results, 'x')

#intensity profiles
# for v in listValues(results, 'Intensity/Total/Y/profile'):
#     plt.plot(v,y)
#     plt.title('Intensity (x=0)')
#     plt.show()
 
#intensity profiles
for v in listValues(results, 'Intensity/Total/X/profile')[::2]:
    plt.plot(np.transpose(x),v)
    plt.xlim([-0.1,0.1])
    plt.title('Intensity (y=0)')
plt.show()
 

plot(results,x='und_bx',y='Intensity/Total/contrastMichelson')


Bx = listValues(results,'und_bx')
By = listValues(results, 'und_by')
theta = [np.arctan(_By/(_Bx+1e-9)) for _Bx, _By in zip(Bx, By)]


plt.plot(theta, listValues(results, 'Intensity/Total/contrastMichelson'),'ro')
plt.ylim([0.99,1.01])
plt.plot()

 #print(" ")
 #print("Results Key")
 #print(resultsKeys(results))

 