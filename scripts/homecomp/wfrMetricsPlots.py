#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  5 08:17:11 2020

@author: gvanriessen
"""


import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import numpy as np

def plotProfileXZ(metrics,key='contrastMichelson',
                  polarisation=['Total','Vertical','Horizontal']):
    
    ''' Plot any dict value that exists for each profile item in each  dict 
        in list of dicts metrics.
        Plot against z position 
    '''
    fontP = FontProperties()
    fontP.set_size('xx-small')
    
    Z = [M['z'] for M in metrics]
    n = np.size(metrics)
    A = [None] * n
    for pol in polarisation:
        for i,M in zip(range(n),metrics):
            try:
                A[i] = M['profiles']['Intensity'+pol+'X'][key]
            except Exception as e: print(e)
    
        plt.plot(Z,A,'o',label=key + ' (pol: '+pol+')')
    plt.xlabel('Z [m]')
    plt.ylabel(key)
    plt.legend(loc='upper left', bbox_to_anchor=(1, 0.5), prop=fontP)
    plt.show()    
    

def plotHorizontalIntensityProfiles(metrics,
                                    polarisation=['Total','Vertical','Horizontal']
                                    ):

    fontP = FontProperties()
    fontP.set_size('xx-small')
    
    # plot x profiles
    plt.title('Horizontal Intensity Profiles, z = %f m'%(metrics[0]['z']),fontsize=8)
    for M in metrics:
        for pol in polarisation:
            try:
                plt.plot(M['x'],
                         M['profiles']['Intensity'+pol+'X']['profile'],
                         label='Intensity ('+pol+' Pol.)'
                         )
            except:
                pass
    #plt.rcParams["figure.figsize"] = [2,10]    
    plt.ylabel('Intensity [units?]')
    plt.xlabel('position [um????]')
    plt.legend(loc='upper left', bbox_to_anchor=(1, 0.5), prop=fontP)
    plt.show
        
    
def plotVerticalIntensityProfiles(metrics,
                                   polarisation=['Total','Vertical','Horizontal']
                                   ):
       
    fontP = FontProperties()
    fontP.set_size('xx-small')
    
    # plot y profiles
    for M in metrics:
        plt.title('Vertical Intensity Profiles, z = %f m'%(M['z']),fontsize=8)
        for pol in polarisation:
            try:
                plt.plot(M['y'],
                         M['profiles']['Intensity'+pol+'Y']['profile'],
                         label='Intensity ('+pol+' Pol.)'
                         )
            except:
                pass
    #plt.rcParams["figure.figsize"] = [2,10]    
    plt.ylabel('Intensity [units?]')
    plt.xlabel('position [um????]')
    plt.legend(loc='upper left', bbox_to_anchor=(1, 0.5), prop=fontP)
    plt.show
        
        
        