#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 11:50:23 2021

@author: jerome

Beamline definition is based on output from Sirepo/SRW.

"""
#!/usr/bin/env python
import os
try:
    __IPYTHON__
    import sys
    del sys.argv[1:]
except:
    pass

try:
    from wpg.srw import srwlpy as srwl
except ImportError:
    import srwlpy as srwl

from xl.srwl_blx import *
from wpg.wavefront import Wavefront#, srw_info, get_intensity

import srwl_bl as srwl_bl
import srwlib as srwlib
#import srwlpy
import srwl_uti_smp as srwl_uti_smp

from params import *

def set_optics(v=None):
    el = []
    pp = []
    names = opNames  # changed (gvr)
    for el_name in names:
        if el_name == 'Aperture':
            # Aperture: aperture 3.0m
            el.append(srwlib.SRWLOptA(
                _shape=v.op_Aperture_shape,
                _ap_or_ob='a',
                _Dx=v.op_Aperture_Dx,
                _Dy=v.op_Aperture_Dy,
                _x=v.op_Aperture_x,
                _y=v.op_Aperture_y,
            ))
            pp.append(v.op_Aperture_pp)
        elif el_name == 'Grating1':
            # Grating1: Grating1 3.0m
            el.append(srwl_uti_smp.srwl_opt_setup_transm_from_file(
                file_path=v.op_Grating1_file_path,
                resolution=v.op_Grating1_resolution,
                thickness=v.op_Grating1_thick,
                delta=v.op_Grating1_delta,
                atten_len=v.op_Grating1_atten_len,
                xc=v.op_Grating1_xc,
                yc=v.op_Grating1_yc,
                area=None if not v.op_Grating1_cropArea else (
                    v.op_Grating1_areaXStart,
                    v.op_Grating1_areaXEnd,
                    v.op_Grating1_areaYStart,
                    v.op_Grating1_areaYEnd,
                ),
                extTr=v.op_Grating1_extTransm,
                rotate_angle=v.op_Grating1_rotateAngle,
                rotate_reshape=bool(int(v.op_Grating1_rotateReshape)),
                cutoff_background_noise=v.op_Grating1_cutoffBackgroundNoise,
                background_color=v.op_Grating1_backgroundColor,
                tile=None if not v.op_Grating1_tileImage else (
                    v.op_Grating1_tileRows,
                    v.op_Grating1_tileColumns,
                ),
                shift_x=v.op_Grating1_shiftX,
                shift_y=v.op_Grating1_shiftY,
                invert=bool(int(v.op_Grating1_invert)),
                is_save_images=False,
                prefix='Grating1_sample',
                output_image_format=v.op_Grating1_outputImageFormat,
            ))
            pp.append(v.op_Grating1_pp)
        elif el_name == 'Drift_Between_Gratings':
            # Drift_Between_Gratings: drift 3.0m
            el.append(srwlib.SRWLOptD(
                _L=v.op_Drift_Between_Gratings_L,
            ))
            pp.append(v.op_Drift_Between_Gratings_pp)
        elif el_name == 'Grating2':
            # Grating2: Grating1 3.0001m
            el.append(srwl_uti_smp.srwl_opt_setup_transm_from_file(
                file_path=v.op_Grating2_file_path,
                resolution=v.op_Grating2_resolution,
                thickness=v.op_Grating2_thick,
                delta=v.op_Grating2_delta,
                atten_len=v.op_Grating2_atten_len,
                xc=v.op_Grating2_xc,
                yc=v.op_Grating2_yc,
                area=None if not v.op_Grating2_cropArea else (
                    v.op_Grating2_areaXStart,
                    v.op_Grating2_areaXEnd,
                    v.op_Grating2_areaYStart,
                    v.op_Grating2_areaYEnd,
                ),
                extTr=v.op_Grating2_extTransm,
                rotate_angle=v.op_Grating2_rotateAngle,
                rotate_reshape=bool(int(v.op_Grating2_rotateReshape)),
                cutoff_background_noise=v.op_Grating2_cutoffBackgroundNoise,
                background_color=v.op_Grating2_backgroundColor,
                tile=None if not v.op_Grating2_tileImage else (
                    v.op_Grating2_tileRows,
                    v.op_Grating2_tileColumns,
                ),
                shift_x=v.op_Grating2_shiftX,
                shift_y=v.op_Grating2_shiftY,
                invert=bool(int(v.op_Grating2_invert)),
                is_save_images=False,
                prefix='Grating2_sample',
                output_image_format=v.op_Grating2_outputImageFormat,
            ))
            pp.append(v.op_Grating2_pp)
        elif el_name == 'Drift_To_Image':
            # Drift_To_Image: drift 3.0001m
            el.append(srwlib.SRWLOptD(
                _L=v.op_Drift_To_Image_L,
            ))
            pp.append(v.op_Drift_To_Image_pp)
            pass

    return srwlib.SRWLOptC(el, pp)

    
from wpg.srw.srwl_bl import srwl_uti_merge_options
varParam = srwl_uti_merge_options(varParam, options)

if __name__ == '__main__':
    import os
    os.chdir('/user/home/opt/xl/xl/experiments/maskAllignment/data')
    v = srwl_bl.srwl_uti_parse_options(varParam, use_sys_argv=True)
    op = set_optics(v)
    
    #v.wm = True
    #v.wm_pl = 'xy'
    #v.wm_ns = v.sm_ns = 5
    
    #v.ws = True
    #v.ws_pl = 'xy'
    mag = None
    if v.rs_type == 'm':
        mag = srwlib.SRWLMagFldC()
        mag.arXc.append(0)
        mag.arYc.append(0)
        mag.arMagFld.append(srwlib.SRWLMagFldM(v.mp_field, v.mp_order, v.mp_distribution, v.mp_len))
        mag.arZc.append(v.mp_zc)
   
    
    if v.wfr_file =='':
        srwl_bl.SRWLBeamline(_name=v.name, _mag_approx=mag).calc_all(v, op)
        #w = v.w_res
        
    else: # do propagation in parts using customised beamline
      
        print('Loading wavefront from file {}'.format(v.wfr_file) )
        w = Wavefront()
        w.load_hdf5(v.wfr_file)

        BL = srwl_blx.beamline(v, _op=op)
        BL.printOE()
        BL.show(w._srwl_wf,v)
        BL.calc_part(v, wfr=w._srwl_wf)
        BL.show(w._srwl_wf,v)
    
    

