#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 16:26:55 2020

@author: gvanriessen
"""

from xl.action import Action
import os

class wfSave(Action):
    """This action saves the wavefront to a HDF5 file
    """
    def __init__(self):
        super().__init__()
        self.description = 'Action: Save wavefront to HDF'

    def perform_operation(self, *args, **kwargs):
        """The actual implementation of the  plugin 
        """
        # allow disable if {self.__class__.__name__: True}
        try:
            if kwargs['parameters'][self.__class__.__name__] == False:
                print('...disabled.')
                return {}
        except:
            pass
        
        try:
            w      = kwargs['wavefront']
            fname  = kwargs['parameters']['wfr_file']
            fdir   = kwargs['parameters']['fdir']
            path = os.path.join(fdir,fname)
        except:
            # todo: improve by printing descriptive error / arg checking
            print('FAILED:' + self.description)
            
        else:
            try:
                w.store_hdf5(path)
                print('Wrote wavefront file to ' + path )
            except Exception as e:
                print('Write wavefront to file ' + path + ' failed: ', e)
                path = None

        return {'path': path} 
