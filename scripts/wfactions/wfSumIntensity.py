#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 16:26:55 2020

@author: gvanriessen
"""

from xl.action import Action

import numpy as np
#from wpg.wavefront import Wavefront

class sumIntensity(Action):
    """This action  sums the intensity in the wavefront provided as argument
    """
    def __init__(self):
        super().__init__()
        self.description = 'Action: Sum intensity'

    def perform_operation(self, *args, **kwargs):
        """The actual implementation of the  plugin 
        """
        
        # allow disable if {self.__class__.__name__: True}
        try:
            if kwargs['parameters'][self.__class__.__name__] == True:
                return {}
        except:
            pass
        
        w = kwargs['wavefront']
        A = w.get_intensity()
        s = np.sum(A[:,:,0]) 
        
        
        return {'intensitySum': s}
