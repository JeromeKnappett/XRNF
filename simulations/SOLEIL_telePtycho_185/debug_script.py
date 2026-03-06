#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 28 14:18:49 2025

@author: -
"""

import ipdb
import __builtin__

def open(name, mode='', buffer=0):
    if name == 'test_cmd_mi.h5':
        ipdb.set_trace()  ######### Break Point ###########
    return __builtin__.open(name, mode, buffer)

# f = open('myfile.txt', 'r')