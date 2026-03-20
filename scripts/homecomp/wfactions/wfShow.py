#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 16:26:55 2020

@author: gvanriessen
"""

import action

from uti_plot import uti_plot2d1d, uti_plot_show

class showWavefront(action.Action):
    """This action  plots the intensity and phaser in the wavefront provided as argument,
    Phase is plotted only if parameters.si_plp is 'xy', 'yx', 'XY', or 'YX'
    Intensity is plotted only if parameters.si_pli is 'xy', 'yx', 'XY', or 'YX'
    Other plotting parameters are 'inherited from parameters.si_* values.
    """
    def __init__(self):
        super().__init__()
        self.description = 'Action: show wavefront'

    def perform_operation(self, *args, **kwargs):
        """The actual implementation of the  plugin 
        TODO: return path to saved plots?
        """
        wfr = kwargs['wavefront']
        _v = kwargs['parameters']
        
        # allow disable if {self.__class__.__name__: True}
        try:
            if kwargs['parameters'][self.__class__.__name__] == False:
                print('...disabled.')
                return {}
        except:
            pass
        

        if _v['ws_pli'] in ['xy','yx','XY','YX']:
            
            '''plot intensity'''
            I2D = wfr.get_intensity()
            I = I2D[:,:,0].ravel()  # convert to column-wise (C-aligned) 1D list
                  
            # CODE BELOW adapted  from  srwl_bl.py

            sValLabel = 'Flux per Unit Surface'
            sValUnit = 'ph/s/.1%bw/mm^2'
            if(_v['w_u'] == 0):
                sValLabel = 'Intensity'
                sValUnit = 'a.u.'
            elif(_v['w_u'] == 2):
                if(_v['w_ft'] == 't'):
                    sValLabel = 'Power Density'
                    sValUnit = 'W/mm^2'
                elif(_v['w_ft'] == 'f'):
                    sValLabel = 'Spectral Fluence'
                    sValUnit = 'J/eV/mm^2'

            uti_plot2d1d(
                I,
                [wfr.params.Mesh.xMin, wfr.params.Mesh.xMax, wfr.params.Mesh.nx],
                [wfr.params.Mesh.yMin, wfr.params.Mesh.yMax, wfr.params.Mesh.ny],
                0, #0.5*(mesh_ws.xStart + mesh_ws.xFin),
                0, #0.5*(mesh_ws.yStart + mesh_ws.yFin),
                ['Horizontal Position', 'Vertical Position', sValLabel],
                ['m', 'm', sValUnit],
                True)
        else: 
            print('ws_pli parameter not set to xy, yx, XY, or YX...not plotting.')
              

        if _v['ws_plp'] in ['xy','yx','XY','YX']:
                
            ''' now plot phase '''
            P2D = wfr.get_phase()
            P = P2D[:,:,0].ravel()  # convert to column-wise (C-aligned) 1D list
            
            
            # CODE BELOW adapted  from  srwl_bl.py

            sValLabel = 'Phase'
            sValUnit = 'rad.'

            uti_plot2d1d(
                P,
                [wfr.params.Mesh.xMin, wfr.params.Mesh.xMax, wfr.params.Mesh.nx],
                [wfr.params.Mesh.yMin, wfr.params.Mesh.yMax, wfr.params.Mesh.ny],
                0, #0.5*(mesh_ws.xStart + mesh_ws.xFin),
                0, #0.5*(mesh_ws.yStart + mesh_ws.yFin),
                ['Horizontal Position', 'Vertical Position', sValLabel],
                ['m', 'm', sValUnit],
                True)
        else: 
            print('ws_plp parameter not set to xy, yx, XY, or YX...not plotting.')
              

        uti_plot_show()

