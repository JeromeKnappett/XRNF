#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 13 22:03:40 2020

@author: gvanriessen
"""

import action

class describeWavefront(action.Action):
    '''
    This action returns the wavefront dictionary excluding E-field entries, e.g. arrEhor, arrEver
    '''   
    def __init__(self):
        super().__init__()
        self.description = 'Action: describe wavefront'
        
    def perform_operation(self, *args, **kwargs):
        w = kwargs['wavefront']
        
        # allow disable if {self.__class__.__name__: True}
        try:
            if kwargs['parameters'][self.__class__.__name__] == True:
                return {}
        except:
            pass
        
        
        d = w._to_dict()
        return {k:v for k, v in d.items() if not k.startswith('data/arrE')}
