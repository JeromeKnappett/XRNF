#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 16:26:55 2020

@author: gvanriessen
"""

import os
import imageio
from xl.action import Action

class wfSaveIntensity(Action):
    """This action saves the wavefront to a HDF5 file
    """
    def __init__(self):
        super().__init__()
        self.description = 'Action: Save wavefront intensity to TIF file'

    def perform_operation(self, *args, **kwargs):
        
        # allow disable if {self.__class__.__name__: True}
        try:
            if kwargs['parameters'][self.__class__.__name__] == False:
                return {}
        except:
            pass
        
        """The actual implementation of the  plugin 
        """
        try:
            w      = kwargs['wavefront']
            fdir   = kwargs['parameters']['fdir']
        except:
            # todo: improve by printing descriptive error / arg checking
            print('FAILED:' + self.description)
            
        else:
            pathI = os.path.join(fdir,'intensity.tif') 
            pathP = os.path.join(fdir,'phase.tif') 
            I = w.get_intensity()[:,:,0]
            P = w.get_phase()[:,:,0]
             
            imageio.imwrite(pathI, I) 
            imageio.imwrite(pathP, P) 
            
        return {'intensityPath': pathI,'phasePath': pathP} 
