#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 27 12:31:21 2021
@author: jknappett
"""

import action
from wfutils import check_sampling

class wfCheckSampling(action.Action):
    '''
    This action checks wavefront sampling and prints a report
    '''   
    def __init__(self):
        super().__init__()
        self.description = 'Action: Check Sampling'
        
    def perform_operation(self, *args, **kwargs):
        
        
        # allow disable if {self.__class__.__name__: True}
        try:
            if kwargs['parameters'][self.__class__.__name__] ==False:
                print('...disabled.')
                return {}
        except: pass
        
        w = kwargs['wavefront']
        
        print("-----Checking Wavefront Sampling-----")

        ret, report = check_sampling(w)
        
        print(ret)
        print(report)


        # return a dictionary.
        return {'samplingRet': ret, 'samplingReport': report}
