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
        if el_name == 'zero_drift':
            # zero_drift: drift 3.0m
            el.append(srwlib.SRWLOptD(
                _L=v.op_zero_drift_L,
            ))
            pp.append(v.op_zero_drift_pp)
        elif el_name == 'Initial_Phase':
            # Initial_Phase: watch 3.0m
            pass
        elif el_name == 'Aperture':
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
        elif el_name == 'FZP_Aperture':
            # Mask_Aperture: aperture 37.0m
            el.append(srwlib.SRWLOptA(
                _shape=v.op_FZP_Aperture_shape,
                _ap_or_ob='a',
                _Dx=v.op_FZP_Aperture_Dx,
                _Dy=v.op_FZP_Aperture_Dy,
                _x=v.op_FZP_Aperture_x,
                _y=v.op_FZP_Aperture_y,
            ))
            pp.append(v.op_FZP_Aperture_pp)
        elif el_name == 'FZP':
            # FZP: Fresnel Zone Plate 37.0m
            el.append(srwlib.SRWLOptZP(
                    _nZones=v.op_FZP_nZones,
                    _rn=v.op_FZP_rn,
                    _thick=v.op_FZP_thick,
                    _delta1=v.op_FZP_delta1,
                    _atLen1=v.op_FZP_atLen1,
                    _delta2=v.op_FZP_delta2,
                    _atLen2=v.op_FZP_atLen2,
                    _x=v.op_FZP_x,
                    _y=v.op_FZP_y,
                    _e=v.op_FZP_e,
            ))
            pp.append(v.op_FZP_pp)
#        elif el_name == 'FZP':
#            # FZP: lens 37.0m
#            el.append(srwlib.SRWLOptL(
#                _Fx=v.op_FZP_Fx,
#                _Fy=v.op_FZP_Fy,
#                _x=v.op_FZP_x,
#                _y=v.op_FZP_y,
#            ))
#            pp.append(v.op_FZP_pp)
        elif el_name == 'Optical_Axis_Angle':    # Added by JK
            # Redefining optical axis and plane to sample wavefront
            el.append(srwlib.SRWLOptAng(
                    _ang_x=v.op_Optical_Axis_Angle_ang_x,
                    _ang_y=v.op_Optical_Axis_Angle_ang_y,
                    _shift_x=v.op_Optical_Axis_Angle_shift_x,
                    _shift_y=v.op_Optical_Axis_Angle_shift_y,
            ))
            pp.append(v.op_Optical_Axis_Angle_pp)
        elif el_name == 'Aperture_Before_M1':
            # Aperture_Before_M1: drift 3.0m
            el.append(srwlib.SRWLOptD(
                _L=v.op_Aperture_Before_M1_L,
            ))
            pp.append(v.op_Aperture_Before_M1_pp)
        elif el_name == 'Before_M1':
            # Before_M1: watch 15.0m
            pass
        elif el_name == 'Phase_Before_M1':
            # Phase_Before_M1: watch 15.0m
            pass
        elif el_name == 'Obstacle':
            # Obstacle: obstacle 15.0m
            el.append(srwlib.SRWLOptA(
                _shape=v.op_Obstacle_shape,
                _ap_or_ob='o',
                _Dx=v.op_Obstacle_Dx,
                _Dy=v.op_Obstacle_Dy,
                _x=v.op_Obstacle_x,
                _y=v.op_Obstacle_y,
            ))
            pp.append(v.op_Obstacle_pp)
        elif el_name == 'Aperture2':
            # Aperture2: aperture 15.0m
            el.append(srwlib.SRWLOptA(
                _shape=v.op_Aperture2_shape,
                _ap_or_ob='a',
                _Dx=v.op_Aperture2_Dx,
                _Dy=v.op_Aperture2_Dy,
                _x=v.op_Aperture2_x,
                _y=v.op_Aperture2_y,
            ))
            pp.append(v.op_Aperture2_pp)
        elif el_name == 'Mask':
            # Mask: sample 37.0m
            el.append(srwl_uti_smp.srwl_opt_setup_transm_from_file(
                file_path=v.op_Mask_file_path,
                resolution=v.op_Mask_resolution,
                thickness=v.op_Mask_thick,
                delta=v.op_Mask_delta,
                atten_len=v.op_Mask_atten_len,
                xc=v.op_Mask_horizontalCenterCoordinate,
                yc=v.op_Mask_verticalCenterCoordinate,
                area=None if not v.op_Mask_cropArea else (
                    v.op_Mask_areaXStart,
                    v.op_Mask_areaXEnd,
                    v.op_Mask_areaYStart,
                    v.op_Mask_areaYEnd,
                ),
                extTr=v.op_Mask_extTransm,
                rotate_angle=v.op_Mask_rotateAngle,
                rotate_reshape=bool(int(v.op_Mask_rotateReshape)),
                cutoff_background_noise=v.op_Mask_cutoffBackgroundNoise,
                background_color=v.op_Mask_backgroundColor,
                tile=None if not v.op_Mask_tileImage else (
                    v.op_Mask_tileRows,
                    v.op_Mask_tileColumns,
                ),
                shift_x=v.op_Mask_shiftX,
                shift_y=v.op_Mask_shiftY,
                invert=bool(int(v.op_Mask_invert)),
                is_save_images=True,
                prefix='Mask_sample',
                output_image_format=v.op_Mask_outputImageFormat,
            ))
            pp.append(v.op_Mask_pp)       
        elif el_name == 'After_YDS':
            # After_YDS: watch 15.0m
            pass
        elif el_name == 'Phase_After_YDS':
            # Phase_After_YDS: watch 15.0m
            pass
        elif el_name == 'Phase_After_YDS_Far_Field':
            # Phase_After_YDS_Far_Field: drift 15.0m
            el.append(srwlib.SRWLOptD(
                _L=v.op_Phase_After_YDS_Far_Field_L,
            ))
            pp.append(v.op_Phase_After_YDS_Far_Field_pp)
        elif el_name == 'maskObstacle':
            # Mask: sample 37.0m
            el.append(srwl_uti_smp.srwl_opt_setup_transm_from_file(
                file_path=v.op_maskObstacle_file_path,
                resolution=v.op_maskObstacle_resolution,
                thickness=v.op_maskObstacle_thick,
                delta=v.op_maskObstacle_delta,
                atten_len=v.op_maskObstacle_atten_len,
                xc=v.op_maskObstacle_horizontalCenterCoordinate,
                yc=v.op_maskObstacle_verticalCenterCoordinate,
                area=None if not v.op_maskObstacle_cropArea else (
                    v.op_maskObstacle_areaXStart,
                    v.op_maskObstacle_areaXEnd,
                    v.op_maskObstacle_areaYStart,
                    v.op_maskObstacle_areaYEnd,
                ),
                extTr=v.op_maskObstacle_extTransm,
                rotate_angle=v.op_maskObstacle_rotateAngle,
                rotate_reshape=bool(int(v.op_maskObstacle_rotateReshape)),
                cutoff_background_noise=v.op_maskObstacle_cutoffBackgroundNoise,
                background_color=v.op_maskObstacle_backgroundColor,
                tile=None if not v.op_maskObstacle_tileImage else (
                    v.op_maskObstacle_tileRows,
                    v.op_maskObstacle_tileColumns,
                ),
                shift_x=v.op_maskObstacle_shiftX,
                shift_y=v.op_maskObstacle_shiftY,
                invert=bool(int(v.op_maskObstacle_invert)),
                is_save_images=True,
                prefix='maskObstacle_sample',
                output_image_format=v.op_maskObstacle_outputImageFormat,
            ))
            pp.append(v.op_maskObstacle_pp)     
        elif el_name == 'maskSubstrate':
            # Mask: sample 37.0m
            el.append(srwl_uti_smp.srwl_opt_setup_transm_from_file(
                file_path=v.op_maskSubstrate_file_path,
                resolution=v.op_maskSubstrate_resolution,
                thickness=v.op_maskSubstrate_thick,
                delta=v.op_maskSubstrate_delta,
                atten_len=v.op_maskSubstrate_atten_len,
                xc=v.op_maskSubstrate_horizontalCenterCoordinate,
                yc=v.op_maskSubstrate_verticalCenterCoordinate,
                area=None if not v.op_maskSubstrate_cropArea else (
                    v.op_maskSubstrate_areaXStart,
                    v.op_maskSubstrate_areaXEnd,
                    v.op_maskSubstrate_areaYStart,
                    v.op_maskSubstrate_areaYEnd,
                ),
                extTr=v.op_maskSubstrate_extTransm,
                rotate_angle=v.op_maskSubstrate_rotateAngle,
                rotate_reshape=bool(int(v.op_maskSubstrate_rotateReshape)),
                cutoff_background_noise=v.op_maskSubstrate_cutoffBackgroundNoise,
                background_color=v.op_maskSubstrate_backgroundColor,
                tile=None if not v.op_maskSubstrate_tileImage else (
                    v.op_maskSubstrate_tileRows,
                    v.op_maskSubstrate_tileColumns,
                ),
                shift_x=v.op_maskSubstrate_shiftX,
                shift_y=v.op_maskSubstrate_shiftY,
                invert=bool(int(v.op_maskSubstrate_invert)),
                is_save_images=True,
                prefix='maskSubstrate_sample',
                output_image_format=v.op_maskSubstrate_outputImageFormat,
            ))
            pp.append(v.op_maskSubstrate_pp) 
        elif el_name == 'Grating':
            # Grating: sample 37.0m
            el.append(srwl_uti_smp.srwl_opt_setup_transm_from_file(
                file_path=v.op_Grating_file_path,
                resolution=v.op_Grating_resolution,
                thickness=v.op_Grating_thick,
                delta=v.op_Grating_delta,
                atten_len=v.op_Grating_atten_len,
                xc=v.op_Grating_horizontalCenterCoordinate,
                yc=v.op_Grating_verticalCenterCoordinate,
                area=None if not v.op_Grating_cropArea else (
                    v.op_Grating_areaXStart,
                    v.op_Grating_areaXEnd,
                    v.op_Grating_areaYStart,
                    v.op_Grating_areaYEnd,
                ),
                extTr=v.op_Grating_extTransm,
                rotate_angle=v.op_Grating_rotateAngle,
                rotate_reshape=bool(int(v.op_Grating_rotateReshape)),
                cutoff_background_noise=v.op_Grating_cutoffBackgroundNoise,
                background_color=v.op_Grating_backgroundColor,
                tile=None if not v.op_Grating_tileImage else (
                    v.op_Grating_tileRows,
                    v.op_Grating_tileColumns,
                ),
                shift_x=v.op_Grating_shiftX,
                shift_y=v.op_Grating_shiftY,
                invert=bool(int(v.op_Grating_invert)),
                is_save_images=True,
                prefix='Grating_sample',
                output_image_format=v.op_Grating_outputImageFormat,
            ))
            pp.append(v.op_Grating_pp)
        elif el_name == 'Drift_Mask_To_AerialImage':
            # Drift_Mask_To_AerialImage: drift 37.0m
            el.append(srwlib.SRWLOptD(
                _L=v.op_Drift_Mask_To_AerialImage_L,
            ))
            pp.append(v.op_Drift_Mask_To_AerialImage_pp)
        elif el_name == 'Far_Field':
            # Far_Field: watch 20.0m
            pass
        elif el_name == 'Phase_Far_Field':
            # Phase_Far_Field: watch 20.0m
            pass
        elif el_name == 'final_resize':
            # resize only
            pp.append(v.op_final_resize_pp)
        
    #pp.append(v.op_fin_pp)
    return srwlib.SRWLOptC(el, pp)


    
from wpg.srw.srwl_bl import srwl_uti_merge_options
varParam = srwl_uti_merge_options(varParam, options)

def main():
    import os
    os.chdir('/user/home/opt/xl/xl/experiments/beamPolarisation17/data')
    v = srwl_bl.srwl_uti_parse_options(varParam, use_sys_argv=True)
    op = set_optics(v)
    v.ws = True
    v.ws_pl = 'xy'
    mag = None
    if v.rs_type == 'm':
        mag = srwlib.SRWLMagFldC()
        mag.arXc.append(0)
        mag.arYc.append(0)
        mag.arMagFld.append(srwlib.SRWLMagFldM(v.mp_field, v.mp_order, v.mp_distribution, v.mp_len))
        mag.arZc.append(v.mp_zc)
   
    
    if v.wfr_file =='':
        srwl_bl.SRWLBeamline(_name=v.name, _mag_approx=mag).calc_all(v, op)
        w = v.w_res
        
    else: # do propagation in parts using customised beamline
      
        print('Loading wavefront from file {}'.format(v.wfr_file) )
        w = Wavefront()
        w.load_hdf5(v.wfr_file)

        BL = srwl_blx.beamline(v, _op=op)
        BL.printOE()
        BL.show(w._srwl_wf,v)
        BL.calc_part(v, wfr=w._srwl_wf)
        BL.show(w._srwl_wf,v)
    
    
if __name__ == '__main__':
    main()
