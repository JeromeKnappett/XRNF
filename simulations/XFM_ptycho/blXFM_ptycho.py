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
    # for el_name in names:
    #     if el_name == 'zero_drift':
    #         # zero_drift: drift 20.0m
    #         el.append(srwlib.SRWLOptD(
    #             _L=v.op_zero_drift_L,
    #         ))
    #         pp.append(v.op_zero_drift_pp)
    #     elif el_name == 'Aperture':
    #         # Aperture: aperture 20.0m
    #         el.append(srwlib.SRWLOptA(
    #             _shape=v.op_Aperture_shape,
    #             _ap_or_ob='a',
    #             _Dx=v.op_Aperture_Dx,
    #             _Dy=v.op_Aperture_Dy,
    #             _x=v.op_Aperture_x,
    #             _y=v.op_Aperture_y,
    #         ))
    #         pp.append(v.op_Aperture_pp)
    #     elif el_name == 'afterAp1_atAp2':
    #         # afterAp1_atAp2: drift 20.0m
    #         el.append(srwlib.SRWLOptD(
    #             _L=v.op_afterAp1_atAp2_L,
    #         ))
    #         pp.append(v.op_afterAp1_atAp2_pp)
    #     elif el_name == 'Aperture2':
    #         # Aperture2: aperture 21.0m
    #         el.append(srwlib.SRWLOptA(
    #             _shape=v.op_Aperture2_shape,
    #             _ap_or_ob='a',
    #             _Dx=v.op_Aperture2_Dx,
    #             _Dy=v.op_Aperture2_Dy,
    #             _x=v.op_Aperture2_x,
    #             _y=v.op_Aperture2_y,
    #         ))
    #         pp.append(v.op_Aperture2_pp)
    #     elif el_name == 'afterAp2_Sample':
    #         # afterAp2_Sample: drift 21.0m
    #         el.append(srwlib.SRWLOptD(
    #             _L=v.op_afterAp2_Sample_L,
    #         ))
    #         pp.append(v.op_afterAp2_Sample_pp)
    #     elif el_name == 'Sample':
    #         # Sample: sample 22.0m
    #         el.append(srwl_uti_smp.srwl_opt_setup_transm_from_file(
    #             file_path=v.op_Sample_file_path,
    #             resolution=v.op_Sample_resolution,
    #             thickness=v.op_Sample_thick,
    #             delta=v.op_Sample_delta,
    #             atten_len=v.op_Sample_atten_len,
    #             xc=v.op_Sample_xc,
    #             yc=v.op_Sample_yc,
    #             area=None if not v.op_Sample_cropArea else (
    #                 v.op_Sample_areaXStart,
    #                 v.op_Sample_areaXEnd,
    #                 v.op_Sample_areaYStart,
    #                 v.op_Sample_areaYEnd,
    #             ),
    #             extTr=v.op_Sample_extTransm,
    #             rotate_angle=v.op_Sample_rotateAngle,
    #             rotate_reshape=bool(int(v.op_Sample_rotateReshape)),
    #             cutoff_background_noise=v.op_Sample_cutoffBackgroundNoise,
    #             background_color=v.op_Sample_backgroundColor,
    #             tile=None if not v.op_Sample_tileImage else (
    #                 v.op_Sample_tileRows,
    #                 v.op_Sample_tileColumns,
    #             ),
    #             shift_x=v.op_Sample_shiftX,
    #             shift_y=v.op_Sample_shiftY,
    #             invert=bool(int(v.op_Sample_invert)),
    #             is_save_images=False,
    #             prefix='Sample_sample',
    #             output_image_format=v.op_Sample_outputImageFormat,
    #         ))
    #         pp.append(v.op_Sample_pp)
    #     elif el_name == 'Sample_Block':
    #         # Sample_Block: drift 22.0m
    #         el.append(srwlib.SRWLOptD(
    #             _L=v.op_Sample_Block_L,
    #         ))
    #         pp.append(v.op_Sample_Block_pp)
    #     elif el_name == 'Block':
    #         # Block: sample 22.5m
    #         el.append(srwl_uti_smp.srwl_opt_setup_transm_from_file(
    #             file_path=v.op_Block_file_path,
    #             resolution=v.op_Block_resolution,
    #             thickness=v.op_Block_thick,
    #             delta=v.op_Block_delta,
    #             atten_len=v.op_Block_atten_len,
    #             xc=v.op_Block_xc,
    #             yc=v.op_Block_yc,
    #             area=None if not v.op_Block_cropArea else (
    #                 v.op_Block_areaXStart,
    #                 v.op_Block_areaXEnd,
    #                 v.op_Block_areaYStart,
    #                 v.op_Block_areaYEnd,
    #             ),
    #             extTr=v.op_Block_extTransm,
    #             rotate_angle=v.op_Block_rotateAngle,
    #             rotate_reshape=bool(int(v.op_Block_rotateReshape)),
    #             cutoff_background_noise=v.op_Block_cutoffBackgroundNoise,
    #             background_color=v.op_Block_backgroundColor,
    #             tile=None if not v.op_Block_tileImage else (
    #                 v.op_Block_tileRows,
    #                 v.op_Block_tileColumns,
    #             ),
    #             shift_x=v.op_Block_shiftX,
    #             shift_y=v.op_Block_shiftY,
    #             invert=bool(int(v.op_Block_invert)),
    #             is_save_images=False,
    #             prefix='Block_sample',
    #             output_image_format=v.op_Block_outputImageFormat,
    #         ))
    #         pp.append(v.op_Block_pp)
    #     elif el_name == 'Pinhole':
    #         # Pinhole: aperture
    #         el.append(srwlib.SRWLOptA(
    #             _shape=v.op_Pinhole_shape,
    #             _ap_or_ob='a',
    #             _Dx=v.op_Pinhole_Dx,
    #             _Dy=v.op_Pinhole_Dy,
    #             _x=v.op_Pinhole_x,
    #             _y=v.op_Pinhole_y,
    #         ))
    #         pp.append(v.op_Pinhole_pp)
    #     elif el_name == 'Block_detector':
    #         # Block_detector: drift 22.5m
    #         el.append(srwlib.SRWLOptD(
    #             _L=v.op_Block_detector_L,
    #         ))
    #         pp.append(v.op_Block_detector_pp)
    # if want_final_propagation:
    #     pp.append(v.op_fin_pp)
    
    for el_name in names:
        if el_name == 'Aperture_1':
            # Aperture_1: aperture 20.0m
            el.append(srwlib.SRWLOptA(
                _shape=v.op_Aperture_1_shape,
                _ap_or_ob='a',
                _Dx=v.op_Aperture_1_Dx,
                _Dy=v.op_Aperture_1_Dy,
                _x=v.op_Aperture_1_x,
                _y=v.op_Aperture_1_y,
            ))
            pp.append(v.op_Aperture_1_pp)
        elif el_name == 'afterAp1_atAp2':
            # afterAp1_atAp2: drift 20.0m
            el.append(srwlib.SRWLOptD(
                _L=v.op_afterAp1_atAp2_L,
            ))
            pp.append(v.op_afterAp1_atAp2_pp)
        elif el_name == 'Aperture_2':
            # Aperture_2: aperture 45.0m
            el.append(srwlib.SRWLOptA(
                _shape=v.op_Aperture_2_shape,
                _ap_or_ob='a',
                _Dx=v.op_Aperture_2_Dx,
                _Dy=v.op_Aperture_2_Dy,
                _x=v.op_Aperture_2_x,
                _y=v.op_Aperture_2_y,
            ))
            pp.append(v.op_Aperture_2_pp)
        elif el_name == 'afterAp2_Sample':
            # afterAp2_Sample: drift 45.0m
            el.append(srwlib.SRWLOptD(
                _L=v.op_afterAp2_Sample_L,
            ))
            pp.append(v.op_afterAp2_Sample_pp)
        elif el_name == 'Aperture_3':
            # Aperture_3: aperture 70.0m
            el.append(srwlib.SRWLOptA(
                _shape=v.op_Aperture_3_shape,
                _ap_or_ob='a',
                _Dx=v.op_Aperture_3_Dx,
                _Dy=v.op_Aperture_3_Dy,
                _x=v.op_Aperture_3_x,
                _y=v.op_Aperture_3_y,
            ))
            pp.append(v.op_Aperture_3_pp)
            
        elif el_name == 'Lens':
            # Lens: lens 2.5m
            el.append(srwlib.SRWLOptL(
                _Fx=v.op_Lens_Fx,
                _Fy=v.op_Lens_Fy,
                _x=v.op_Lens_x,
                _y=v.op_Lens_y,
            ))
            pp.append(v.op_Lens_pp)
            
        elif el_name == 'SamplePinhole':
            # SamplePinhole: sample 70.0m
            el.append(srwl_uti_smp.srwl_opt_setup_transm_from_file(
                file_path=v.op_SamplePinhole_file_path,
                resolution=v.op_SamplePinhole_resolution,
                thickness=v.op_SamplePinhole_thick,
                delta=v.op_SamplePinhole_delta,
                atten_len=v.op_SamplePinhole_atten_len,
                xc=v.op_SamplePinhole_xc,
                yc=v.op_SamplePinhole_yc,
                area=None if not v.op_SamplePinhole_cropArea else (
                    v.op_SamplePinhole_areaXStart,
                    v.op_SamplePinhole_areaXEnd,
                    v.op_SamplePinhole_areaYStart,
                    v.op_SamplePinhole_areaYEnd,
                ),
                extTr=v.op_SamplePinhole_extTransm,
                rotate_angle=v.op_SamplePinhole_rotateAngle,
                rotate_reshape=bool(int(v.op_SamplePinhole_rotateReshape)),
                cutoff_background_noise=v.op_SamplePinhole_cutoffBackgroundNoise,
                background_color=v.op_SamplePinhole_backgroundColor,
                tile=None if not v.op_SamplePinhole_tileImage else (
                    v.op_SamplePinhole_tileRows,
                    v.op_SamplePinhole_tileColumns,
                ),
                shift_x=v.op_SamplePinhole_shiftX,
                shift_y=v.op_SamplePinhole_shiftY,
                invert=bool(int(v.op_SamplePinhole_invert)),
                is_save_images=False,
                prefix='SamplePinhole_sample',
                output_image_format=v.op_SamplePinhole_outputImageFormat,
            ))
            pp.append(v.op_SamplePinhole_pp)
        
        elif el_name == 'Sample':
            # Sample: sample 70.0m
            el.append(srwl_uti_smp.srwl_opt_setup_transm_from_file(
                file_path=v.op_Sample_file_path,
                resolution=v.op_Sample_resolution,
                thickness=v.op_Sample_thick,
                delta=v.op_Sample_delta,
                atten_len=v.op_Sample_atten_len,
                xc=v.op_Sample_xc,
                yc=v.op_Sample_yc,
                area=None if not v.op_Sample_cropArea else (
                    v.op_Sample_areaXStart,
                    v.op_Sample_areaXEnd,
                    v.op_Sample_areaYStart,
                    v.op_Sample_areaYEnd,
                ),
                extTr=v.op_Sample_extTransm,
                rotate_angle=v.op_Sample_rotateAngle,
                rotate_reshape=bool(int(v.op_Sample_rotateReshape)),
                cutoff_background_noise=v.op_Sample_cutoffBackgroundNoise,
                background_color=v.op_Sample_backgroundColor,
                tile=None if not v.op_Sample_tileImage else (
                    v.op_Sample_tileRows,
                    v.op_Sample_tileColumns,
                ),
                shift_x=v.op_Sample_shiftX,
                shift_y=v.op_Sample_shiftY,
                invert=bool(int(v.op_Sample_invert)),
                is_save_images=False,
                prefix='Sample_sample',
                output_image_format=v.op_Sample_outputImageFormat,
            ))
            pp.append(v.op_Sample_pp)
                    
        elif el_name == 'SampleBalls':
            # SampleBalls: sample 70.0m
            el.append(srwl_uti_smp.srwl_opt_setup_transm_from_file(
                file_path=v.op_SampleBalls_file_path,
                resolution=v.op_SampleBalls_resolution,
                thickness=v.op_SampleBalls_thick,
                delta=v.op_SampleBalls_delta,
                atten_len=v.op_SampleBalls_atten_len,
                xc=v.op_SampleBalls_xc,
                yc=v.op_SampleBalls_yc,
                area=None if not v.op_SampleBalls_cropArea else (
                    v.op_SampleBalls_areaXStart,
                    v.op_SampleBalls_areaXEnd,
                    v.op_SampleBalls_areaYStart,
                    v.op_SampleBalls_areaYEnd,
                ),
                extTr=v.op_SampleBalls_extTransm,
                rotate_angle=v.op_SampleBalls_rotateAngle,
                rotate_reshape=bool(int(v.op_SampleBalls_rotateReshape)),
                cutoff_background_noise=v.op_SampleBalls_cutoffBackgroundNoise,
                background_color=v.op_SampleBalls_backgroundColor,
                tile=None if not v.op_SampleBalls_tileImage else (
                    v.op_SampleBalls_tileRows,
                    v.op_SampleBalls_tileColumns,
                ),
                shift_x=v.op_SampleBalls_shiftX,
                shift_y=v.op_SampleBalls_shiftY,
                invert=bool(int(v.op_SampleBalls_invert)),
                is_save_images=False,
                prefix='SampleBalls_sample',
                output_image_format=v.op_SampleBalls_outputImageFormat,
            ))
            pp.append(v.op_SampleBalls_pp)
        
        elif el_name == 'prop2pinhole':
            # prop2pinhole: drift 45.0m
            el.append(srwlib.SRWLOptD(
                _L=v.op_prop2pinhole_L,
            ))
            pp.append(v.op_prop2pinhole_pp)
            
        elif el_name == 'pinhole':
            # pinhole: aperture 70.0m
            el.append(srwlib.SRWLOptA(
                _shape=v.op_pinhole_shape,
                _ap_or_ob='a',
                _Dx=v.op_pinhole_Dx,
                _Dy=v.op_pinhole_Dy,
                _x=v.op_pinhole_x,
                _y=v.op_pinhole_y,
            ))
            pp.append(v.op_pinhole_pp)
        
        elif el_name == 'prop2detector':
            # prop2detector: drift 45.0m
            el.append(srwlib.SRWLOptD(
                _L=v.op_prop2detector_L,
            ))
            pp.append(v.op_prop2detector_pp)
            
        elif el_name == 'prop2detector2':
            # prop2detector2: drift 45.0m
            el.append(srwlib.SRWLOptD(
                _L=v.op_prop2detector2_L,
            ))
            pp.append(v.op_prop2detector2_pp)
        elif el_name == 'Obstacle':
            # Obstacle: obstacle 9.0m
            el.append(srwlib.SRWLOptA(
                _shape=v.op_Obstacle_shape,
                _ap_or_ob='o',
                _Dx=v.op_Obstacle_Dx,
                _Dy=v.op_Obstacle_Dy,
                _x=v.op_Obstacle_x,
                _y=v.op_Obstacle_y,
            ))
            pp.append(v.op_Obstacle_pp)    
        elif el_name == 'resample':
            # prop2detector2: drift 45.0m
            el.append(srwlib.SRWLOptD(
                _L=v.op_resample_L,
            ))
            pp.append(v.op_resample_pp)

    return srwlib.SRWLOptC(el, pp)

    
from wpg.srw.srwl_bl import srwl_uti_merge_options
varParam = srwl_uti_merge_options(varParam, options)

if __name__ == '__main__':
    import os
    os.chdir('/user/home/opt/xl/xl/experiments/XFM/data')
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
    
    

