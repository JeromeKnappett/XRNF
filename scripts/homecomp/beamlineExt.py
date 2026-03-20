#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 27 10:21:08 2019

@author: gvanriessen
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

"""
Wrapper for WPG beamline to extend some utility functions for convenience

"""

import wpg.srwlib as srwlib
from wpg.srwlib import srwl
from wpg.utils import srw_obj2str
from wpg.optical_elements import Screen, Empty, WPGOpticalElement
from wpg.wpg_uti_wf import plot_intensity_map, averaged_intensity,calculate_fwhm, get_intensity_on_axis
from wpg.wpg_uti_oe import show_transmission 
import os.path

from wpg.beamline import Beamline
from utils import plotWavefront, show_transmissionFunctionCplx, J2EV

from wpg.srwlib import SRWLOptD as Drift

from husl import complex_to_rgb
from wpg.useful_code.wfrutils import get_mesh
import imageio
import numpy as np

class bl(Beamline):
    """
    Set of optical elements and propagation parameters.
    """

    def __init__(self, srwl_beamline=None, description=None):
         super(bl, self).__init__(srwl_beamline=srwl_beamline)
                
         self.description=description       


    def __str__(self):
        """
        String representaion of beamline (used with print function).

        :return: string
        """        
        return self.description + ': ' + super(bl, self).__str__()
  
    def propagate(self, 
                  wfr,  
                  plot=False, 
                  describe=True,
                  outFilePath=None, 
                  propagationOverride=None):
        """
        Propagate wavefront through beamline.

        :param wfr: Input wavefront (will be rewritten after propagation)
        :type wfr: wpg.wavefront.Wavefront
        """
        
        #for propagation_option in super(bl, self).propagation_options:
        #    print ('X')

        
        print ('Propagating through ' + self.description)
        super(bl, self).propagate(wfr)
        
        if (plot == True) or ((describe == True) and (self.description is not None)) or (outFilePath is not None):
          
            # Create a temporary screen 
            screen = oeScreen(filename=outFilePath,
                              writeIntensity=(outFilePath!=None),
                              showIntensity=plot,
                              description=self.description + ' [screen]')
            metrics = screen.propagate(wfr)
        else:
            metrics = None
            
        
        #print ('Intensity on axis = %e ' % (get_intensity_on_axis(wfr)))
        #print ('FWHM = %e ' % (calculate_fwhm(wfr)))
        return metrics
 
#class oeDrift(Drift):
#    
#    """Optical Element: Drift Space"""
#    
#    def __init__(self,length=0, description=None):
#        """
#        :param _L: Length [m]
#        
#        """
#        self.length=length
#        super(oeDrift, self).__init__()
#        
#        self.description=description
#    
#    def propagate(self, wfr, propagation_parameters):
#        """ Overloaded propagate """
#
#        
#        print('Propagating through drift: ' + self.description)
#       
#        beamline = wpg.srwlib.SRWLOptC([], propagation_parameters)
#        srwl.PropagElecField(wfr._srwl_wf, beamline)
           

class oeResample(Empty):
    """Optical element: Resample, extends Empty
    Uused for sampling and zooming wavefront
    
    TAKEN FROM WPG:  ATTRIBUTION TODO
    """

    def __init__(self, propagation_parameters, description=None):
        super(oeResample, self).__init__()
        self.propagation_parameters = propagation_parameters
        self.description = description

    def propagate(self, wfr):
        """
        Propagate wavefront through empty propagator,
        used for sampling and resizing wavefront
        """
        super(oeResample, self).propagate(wfr, self.propagation_parameters)


