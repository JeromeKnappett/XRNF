#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TEMPLATE ACTION CLASS



Created on Thu Oct  1 17:13:50 2020

@author: gvanriessen
"""


from xl.action import Action

class template(Action):
    '''
    Describe the action of the plugin here. Change only the description.
    '''   
    def __init__(self):
        super().__init__()
        self.description = 'Action: this is a template that does nothing'
        
    def perform_operation(self, *args, **kwargs):
        '''
        This method implements the action.  
        
        We expect a srw wavefront object in kwargs['wavefront'], and a dictionary
        containing parameters in kwargs['parameters']
        
        '''
        
        w = kwargs['wavefront']
        p = kwargs['parameters']
        
        
        # allow disable if {self.__class__.__name__: True}
        try:
            if kwargs['parameters'][self.__class__.__name__] == True:
                return {}
        except: pass
        
        
        '''  do something with w and p here...  '''
        
        # return a dictionary.
        return {}
