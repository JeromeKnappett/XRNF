#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 13:13:33 2023

@author: -
"""

import numpy as np
import tifffile

maskPath = '/user/home/opt/xl/xl/experiments/BEUVcoherenceLER1/masks_D50/20000020.00000_0.50000_10.00000_mask.tif'

M = tifffile.imread(maskPath)

print(np.shape(M))