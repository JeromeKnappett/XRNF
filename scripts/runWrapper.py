#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 10:47:04 2020

@author: gvanriessen
"""

#  change this line to import a particular run file
import extensions.run as sim

import sys,os
sys.path.append('./wpg/')
sys.path.append('./extensions/')

from wpg.wavefront import Wavefront
import srwl_bl
import srwlib
import srwlpy
import srwl_uti_smp


def main():
    v = srwl_bl.srwl_uti_parse_options(sim.varParam, use_sys_argv=True)
    
    # you can override parameters here to determine calculation type    
    v.si = True #'calculate single-e intensity distribution (without wavefront propagation through a beamline) 
    v.si_pl = '' #don't plot, else change to 'xy'

    v.ws = True # calculate single-electron (/ fully coherent) wavefront propagation
    v.ws_pl = ''  # don't plot, else change to 'xy'

    v.wfr_file = 'gb.h5'

    v.wm = False ##Multi-Electron (partially-coherent) Wavefront Propagation

    op = sim.set_optics(v)
    wf = srwl_bl.SRWLBeamline(_name=v.name).calc_all(v, op)

    # convert wavefront to a WPG type to allow easy writing to file
    w = Wavefront(srwl_wavefront=wf)
    w.store_hdf5(v.wfr_file)
    

if __name__ == '__main__':
    main()