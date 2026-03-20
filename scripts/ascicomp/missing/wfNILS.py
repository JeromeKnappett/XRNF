#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 16:26:55 2020

@author: gvanriessen
"""

import action
import numpy as np
from findiff import FinDiff
from itertools import chain, zip_longest
from scipy.signal import find_peaks, peak_prominences

def NILS(pattern, axis, rx, ry, w):
    '''
    Calculate the Normalized Image Log-Slope (NILS) of a pattern
    
    pattern:  a 2d array that can be cast to float64 values, expected to contain 
              periodic patterns over axis 0 or 1.
    
    w: nominal linewidth
    
    '''
    
    #normalise or not?
    #I = pattern/np.max(pattern)
    
    
    # temporary hack
    ny, nx = np.shape(pattern)
    I = pattern[:,nx//2-100:nx//2+100]
    
    
    lnI = np.log(I.astype('float64'))
    
    #define dimensions of data in array a
    x = np.linspace(rx[0], rx[1], np.shape(I)[1])
    y = np.linspace(ry[0], ry[1], np.shape(I)[0])
    dx, dy = x[1] - x[0], y[1] - y[0]
    
    # define differentiation operators
    d_dx = FinDiff(1, dx)
    d_dy = FinDiff(0, dy)
    
    if axis==1:
        d = d_dx
    if axis ==0:
        d = d_dy
    
    grad = d(lnI,acc=10)
    
  
    
    
    
#    #  now lets find the slope at the edge
#    m = 0.5# (np.max() - np.min(gradf))/2
#    m_threshold = 0.01  # fraction of mean value within which mean values are taken to lie
#    mask = np.where( np.abs((lnI-np.min(lnI)) / np.max(lnI-np.min(lnI))  - m) > m_threshold, 0, 1)
#    gradAbs = np.abs(grad)
    
#    gradAbsMasked = np.multiply(gradAbs,mask)
#    edgeSlope = np.average(gradAbsMasked[gradAbsMasked>0])
    
    # alternative will get indexes at midooints between mininma and maxima without 
    # normalisation, and allowing for intensity variations over the image
    p1, _ = find_peaks(I, distance=3)
    p2, _ = find_peaks(1-I)
    p =  [x for x in chain.from_iterable(zip_longest(p1, p2)) if x is not None]
    sep = int(np.mean(np.diff(p))/2)
    p = [x+sep for x in p[:-1]]
    
    gradAbs = np.abs(grad)
    
    edgeSlope= np.mean(gradAbs[p])
        
    
    
    
    
    nils = w*edgeSlope
    
#    plt.imshow(gradAbsMasked[2500:3500,100:200])
#    plt.show()
    
    
    import matplotlib.pyplot as plt 
    
    plots = True
    if plots == True:
    
        # plot intensity
        plt.imshow(lnI)
        plt.colorbar()
        plt.title('ln(I)')
        plt.show()
        
        # plot d/dy
        plt.imshow(grad)
        plt.title('dln(I)/dy')
        plt.colorbar()
        plt.show()
        
        # plot |d//dy|
        plt.imshow(np.abs(grad))
        plt.title('|dln(I)/dy|')
        plt.colorbar()
        plt.show()
        
        #plot ROI and profiles
        
        w =200
        offset = 0
        yl = np.shape(I)[0]//2 -w//2 + offset
        yh = np.shape(I)[0]//2 +w//2 + offset
        
        plt.imshow(grad[yl:yh, yl:yh])
        plt.colorbar()
        plt.title('|dI/dy| (ROI)')
        plt.show()
        
        profileI = I[:,np.shape(I)[1]//2][yl:yh]
        profileI = profileI/np.max(profileI)
        
        profileN=lnI[:,np.shape(I)[1]//2][yl:yh]
        
        profileN = profileN-np.min(profileN)
        profileN = profileN/np.max(profileN)
        plt.plot(profileN,'-', label='ln(I)')
        
        profile_d_dy=grad[:,np.shape(I)[1]//2][yl:yh]
        plt.plot(profile_d_dy/np.max(profile_d_dy),'-', label = 'dln(I)/dy')
        
        #plt.plot(np.abs(profile_d_dy/np.max(profile_d_dy)), '-', label = '|dI/dy|')
        plt.legend()
        plt.show()
        
        
        # show masked intensity
        plt.imshow(np.multiply(lnI, mask)[yl:yh, yl:yh])
        plt.title('ln(I)')
        plt.colorbar()
        plt.show()
        
        # show mask
        plt.imshow(mask[yl:yh, yl:yh])
        plt.title('mask')
        plt.colorbar()
        plt.show()
        
        # show dln(I)/dy
        plt.imshow(grad[yl:yh, yl:yh])
        plt.colorbar()
        plt.title('dln(I)/dy')
        plt.show()
        
        #show masked |dln(I)/dy|
#        plt.imshow(gradAbsMasked[yl:yh, yl:yh])
#        plt.title('|dln(I)/dy|')
#        plt.colorbar()
#        plt.show()
#        
        # show profile and selected points of dI/dy
#        profile_d_dy=gradAbsMasked[:,np.shape(I)[1]//2][yl:yh]
        plt.plot(profileI,label='I')
        #plt.plot(profile_d_dy,'.',label='dln(I)/dy')
        plt.plot(profileN,'-', label='ln(I)')
        plt.plot(x[p],profileN[p], 'x')
        plt.legend()
        plt.show()
    
    
    return nils



class wfNILS(action.Action):
    """This action  NILS for a wavefront provided as argument
    
    Required named arguments (in kwargs):
        'NILSNominalLinewidth':  nominal width of lithographic feature
        'NILSAxis': axis 0 or 1 (y or x)
        'wavefront': the SRW wavefront
    
    """
    def __init__(self):
        super().__init__()
        self.description = 'Action: NILS'
        

    def perform_operation(self, *args, **kwargs):
        """The actual implementation of the  plugin 
        """
        
        
        
         
        # allow disable if {self.__class__.__name__: True}
        try:
            if kwargs['parameters'][self.__class__.__name__] == False:
                return {}
        except:
            pass
        
        w = kwargs['wavefront']
        irr = w.get_intensity()
       
        try: 
            nilsAxis = int(kwargs['parameters']['NILSAxis'])

        except:
            nilsAxis = 0
          
        try: 
            nilsNominalLinewidth = int(kwargs['parameters']['NILSNominalLinewidth'])
        except:
            nilsNominalLinewidth = 1e-9    
            

        wf_mesh = w.params.Mesh
        xmin, xmax = wf_mesh.xMin, wf_mesh.xMax
        ymin, ymax = wf_mesh.yMin, wf_mesh.yMax
        
        nils = NILS(irr[:,:,0], nilsAxis, [xmin,xmax], [ymin,ymax], nilsNominalLinewidth)
        
        return {'NILS': nils}

