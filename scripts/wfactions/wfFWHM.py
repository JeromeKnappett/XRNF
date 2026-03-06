#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 16:26:55 2020

@author: gvanriessen
"""

from xl.action import Action

import numpy as np
#from wpg.wavefront import Wavefront



class wfFWHM(Action):
    """This action  finds the FWHM of beam in wavefront provided as argument
    """
    def __init__(self):
        super().__init__()
        self.description = 'Action: FWHM'
        

    def perform_operation(self, *args, **kwargs):
        """The actual implementation of the  plugin 
        """
        
        # allow disable if {self.__class__.__name__: True}
        try:
            if kwargs['parameters'][self.__class__.__name__] == False:
                print("...disabled.")
                return {}
        except:
            pass
        
        w = kwargs['wavefront']
        
        irr = w.get_intensity()
        irr_max = np.max(irr)

        wf_mesh = w.params.Mesh
        nx, ny = wf_mesh.nx, wf_mesh.ny
        xmin, xmax = wf_mesh.xMin, wf_mesh.xMax
        ymin, ymax = wf_mesh.yMin, wf_mesh.yMax

        x_axis = np.linspace(xmin, xmax, nx)
        y_axis = np.linspace(ymin, ymax, ny)
 
        # get peak postion
        irr_x = irr[ny // 2, :]
        irr_y = irr[:, nx // 2]
        xc = np.max(x_axis[np.where(irr_x == np.max(irr_x))])
        yc = np.max(y_axis[np.where(irr_y == np.max(irr_y))])
        
        irr_x = irr[np.max(np.where(y_axis == yc)), :]
        fwhmx = 0.
        idx = np.where(irr_x >= irr_max / 2)
        if np.size(idx) > 0:
            fwhmx = np.max(x_axis[np.where(irr_x >= irr_max / 2)]) - np.min(
                              x_axis[np.where(irr_x >= irr_max / 2)])
        
        irr_y = irr[:, np.max(np.where(x_axis == xc))]
        fwhmy = 0.
        idx = np.where(irr_y >= irr_max / 2)
        if np.size(idx) > 0:
            fwhmy = np.max(y_axis[np.where(irr_y >= irr_max / 2)]) - np.min(
                              y_axis[np.where(irr_y >= irr_max / 2)])
        
        return {'fwhm_x': fwhmx, 'fwhm_y': fwhmy, 'peakPos_x': xc, 'peakPos_y':yc, 'peakIntensity': irr_max}

