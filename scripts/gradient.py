#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 14:19:12 2022

@author: jerome
"""

import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 255, 100)
image = np.tile(x, (100, 1)).T

plt.imshow(image, cmap="gray")
plt.colorbar()
plt.show()
