#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 24 12:31:21 2021
@author: jknappett
"""


import action
import numpy as np
import time
from wpg.wavefront import Wavefront
import pickle

class wfPickleWave(action.Action):
    '''
    This action returns the pickled wavefield
    '''   
    def __init__(self):
        super().__init__()
        self.description = 'Action: Pickle wavefield'
        
    def perform_operation(self, *args, **kwargs):
        
        
        # allow disable if {self.__class__.__name__: True}
        try:
            if kwargs['parameters'][self.__class__.__name__] == False:
                print('...disabled.')
                return {}
        except: pass
        
        w = kwargs['wavefront']
        fdir = kwargs['parameters']['fdir']
        
        wf = Wavefront(srwl_wavefront=w)          
        
        start1 = time.time()
        wavePath = str(fdir) + "wavefield.pkl"  # Save path for wavefield pickle
        print("Saving wavefield...")
        with open(wavePath, "wb") as g:
            pickle.dump(wf, g)
        print("Wavefield written to: {}".format(wavePath))
        end1 = time.time()
        
        print('Time taken to save wavefield (s): {}'.format(end1 - start1))

        # return a dictionary.
        return {'wavePath': wavePath}
