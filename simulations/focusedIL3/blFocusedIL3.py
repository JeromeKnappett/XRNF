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
        if el_name == 'WBS':
            # WBS: aperture 3.0m
            el.append(srwlib.SRWLOptA(
                _shape=v.op_WBS_shape,
                _ap_or_ob='a',
                _Dx=v.op_WBS_Dx,
                _Dy=v.op_WBS_Dy,
                _x=v.op_WBS_x,
                _y=v.op_WBS_y,
            ))
            pp.append(v.op_WBS_pp)
        elif el_name == 'After_WBS_Before_Toroidal_Mirror':
            # After_WBS_Before_Toroidal_Mirror: drift 3.0m
            el.append(srwlib.SRWLOptD(
                _L=v.op_After_WBS_Before_Toroidal_Mirror_L,
            ))
            pp.append(v.op_After_WBS_Before_Toroidal_Mirror_pp)
        elif el_name == 'Toroidal_Mirror':
            # Toroidal_Mirror: toroidalMirror 15.12m
            el.append(srwlib.SRWLOptMirTor(
                _rt=v.op_Toroidal_Mirror_rt,
                _rs=v.op_Toroidal_Mirror_rs,
                _size_tang=v.op_Toroidal_Mirror_size_tang,
                _size_sag=v.op_Toroidal_Mirror_size_sag,
                _x=v.op_Toroidal_Mirror_horizontalPosition,
                _y=v.op_Toroidal_Mirror_verticalPosition,
                _ap_shape=v.op_Toroidal_Mirror_ap_shape,
                _nvx=v.op_Toroidal_Mirror_nvx,
                _nvy=v.op_Toroidal_Mirror_nvy,
                _nvz=v.op_Toroidal_Mirror_nvz,
                _tvx=v.op_Toroidal_Mirror_tvx,
                _tvy=v.op_Toroidal_Mirror_tvy,
            ))
            pp.append(v.op_Toroidal_Mirror_pp)

        elif el_name == 'After_Toroidal_Mirror_Before_PGM':
            # After_Toroidal_Mirror_Before_PGM: drift 15.12m
            el.append(srwlib.SRWLOptD(
                _L=v.op_After_Toroidal_Mirror_Before_PGM_L,
            ))
            pp.append(v.op_After_Toroidal_Mirror_Before_PGM_pp)
        elif el_name == 'Planar_Mirror':
            # Planar_Mirror: mirror 18.5m
            
            mirror_file = v.op_Planar_Mirror_hfn
            assert os.path.isfile(mirror_file), \
                'Missing input file {}, required by Planar_Mirror beamline element'.format(mirror_file)
            el.append(srwlib.srwl_opt_setup_surf_height_1d(
                srwlib.srwl_uti_read_data_cols(mirror_file, "\t", 0, 1),
                _dim=v.op_Planar_Mirror_dim,
                _ang=abs(v.op_Planar_Mirror_ang),
                _amp_coef=v.op_Planar_Mirror_amp_coef,
                _size_x=v.op_Planar_Mirror_size_x,
                _size_y=v.op_Planar_Mirror_size_y,
            ))
            
            pp.append(v.op_Planar_Mirror_pp)
        elif el_name == 'Planar_Mirror_Grating':
            # Planar_Mirror_Grating: drift 18.5m
            el.append(srwlib.SRWLOptD(
                _L=v.op_Planar_Mirror_Grating_L,
            ))
            pp.append(v.op_Planar_Mirror_Grating_pp)
        elif el_name == 'Grating':
            # Grating: grating 18.7m
            mirror = srwlib.SRWLOptMirPl(
                _size_tang=v.op_Grating_size_tang,
                _size_sag=v.op_Grating_size_sag,
                _nvx=v.op_Grating_nvx,
                _nvy=v.op_Grating_nvy,
                _nvz=v.op_Grating_nvz,
                _tvx=v.op_Grating_tvx,
                _tvy=v.op_Grating_tvy,
                _x=v.op_Grating_x,
                _y=v.op_Grating_y,
            )
            el.append(srwlib.SRWLOptG(
                _mirSub=mirror,
                _m=v.op_Grating_m,
                _grDen=v.op_Grating_grDen,
                _grDen1=v.op_Grating_grDen1,
                _grDen2=v.op_Grating_grDen2,
                _grDen3=v.op_Grating_grDen3,
                _grDen4=v.op_Grating_grDen4,
            ))
            pp.append(v.op_Grating_pp)
        elif el_name == 'Grating_Before_Exit_Aperture':
            # Grating_Before_Exit_Aperture: drift 18.7m
            el.append(srwlib.SRWLOptD(
                _L=v.op_Grating_Before_Exit_Aperture_L,
            ))
            pp.append(v.op_Grating_Before_Exit_Aperture_pp)
        elif el_name == 'Exit_Aperture':
            # Exit_Aperture: aperture 19.7m
            el.append(srwlib.SRWLOptA(
                _shape=v.op_Exit_Aperture_shape,
                _ap_or_ob='a',
                _Dx=v.op_Exit_Aperture_Dx,
                _Dy=v.op_Exit_Aperture_Dy,
                _x=v.op_Exit_Aperture_x,
                _y=v.op_Exit_Aperture_y,
            ))
            pp.append(v.op_Exit_Aperture_pp)
        elif el_name == 'After_Exit_Aperture_Before_Cylindrical_Mirror':
            # After_Exit_Aperture_Before_Cylindrical_Mirror: drift 19.7m
            el.append(srwlib.SRWLOptD(
                _L=v.op_After_Exit_Aperture_Before_Cylindrical_Mirror_L,
            ))
            pp.append(v.op_After_Exit_Aperture_Before_Cylindrical_Mirror_pp)
        elif el_name == 'Cylindrical_Mirror':
            # Cylindrical_Mirror: toroidalMirror 20.3m
            el.append(srwlib.SRWLOptMirTor(
                _rt=v.op_Cylindrical_Mirror_rt,
                _rs=v.op_Cylindrical_Mirror_rs,
                _size_tang=v.op_Cylindrical_Mirror_size_tang,
                _size_sag=v.op_Cylindrical_Mirror_size_sag,
                _x=v.op_Cylindrical_Mirror_horizontalPosition,
                _y=v.op_Cylindrical_Mirror_verticalPosition,
                _ap_shape=v.op_Cylindrical_Mirror_ap_shape,
                _nvx=v.op_Cylindrical_Mirror_nvx,
                _nvy=v.op_Cylindrical_Mirror_nvy,
                _nvz=v.op_Cylindrical_Mirror_nvz,
                _tvx=v.op_Cylindrical_Mirror_tvx,
                _tvy=v.op_Cylindrical_Mirror_tvy,
            ))
            pp.append(v.op_Cylindrical_Mirror_pp)

        elif el_name == 'After_Cylindrical_Mirror_Before_Exit_Slit':
            # After_Cylindrical_Mirror_Before_Exit_Slit: drift 20.3m
            el.append(srwlib.SRWLOptD(
                _L=v.op_After_Cylindrical_Mirror_Before_Exit_Slit_L,
            ))
            pp.append(v.op_After_Cylindrical_Mirror_Before_Exit_Slit_pp)
        elif el_name == 'Exit_Slits':
            # Exit_Slits: aperture 27.3m
            el.append(srwlib.SRWLOptA(
                _shape=v.op_Exit_Slits_shape,
                _ap_or_ob='a',
                _Dx=v.op_Exit_Slits_Dx,
                _Dy=v.op_Exit_Slits_Dy,
                _x=v.op_Exit_Slits_x,
                _y=v.op_Exit_Slits_y,
            ))
            pp.append(v.op_Exit_Slits_pp)
 
        elif el_name == 'Exit_Slits_Drift':
            # After_Exit_Slit_Before_BDA: drift 27.3m
            el.append(srwlib.SRWLOptD(
                _L=v.op_Exit_Slits_Drift_L,
            ))
            pp.append(v.op_Exit_Slits_Drift_pp)
        elif el_name == 'Exit_Slits_Cleanup':
            # Exit_Slits: aperture 
            el.append(srwlib.SRWLOptA(
                _shape=v.op_Exit_Slits_Cleanup_shape,
                _ap_or_ob='a',
                _Dx=v.op_Exit_Slits_Cleanup_Dx,
                _Dy=v.op_Exit_Slits_Cleanup_Dy,
                _x=v.op_Exit_Slits_Cleanup_x,
                _y=v.op_Exit_Slits_Cleanup_y,
            ))
            pp.append(v.op_Exit_Slits_Cleanup_pp)

        elif el_name == 'After_Exit_Slit_Before_BDA':
            # After_Exit_Slit_Before_BDA: drift 27.3m
            el.append(srwlib.SRWLOptD(
                _L=v.op_After_Exit_Slit_Before_BDA_L,
            ))
            pp.append(v.op_After_Exit_Slit_Before_BDA_pp)
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
            # FZP: lens 37.0m
            el.append(srwlib.SRWLOptL(
                _Fx=v.op_FZP_Fx,
                _Fy=v.op_FZP_Fy,
                _x=v.op_FZP_x,
                _y=v.op_FZP_y,
            ))
            pp.append(v.op_FZP_pp)
        elif el_name == 'BDA':
            # BDA: aperture 36.8m
            el.append(srwlib.SRWLOptA(
                _shape=v.op_BDA_shape,
                _ap_or_ob='a',
                _Dx=v.op_BDA_Dx,
                _Dy=v.op_BDA_Dy,
                _x=v.op_BDA_x,
                _y=v.op_BDA_y,
            ))
            pp.append(v.op_BDA_pp)
        elif el_name == 'BDA_Mask_Aperture':
            # BDA_Mask_Aperture: drift 36.8m
            el.append(srwlib.SRWLOptD(
                _L=v.op_BDA_Mask_Aperture_L,
            ))
            pp.append(v.op_BDA_Mask_Aperture_pp)
        elif el_name == 'Mask_Aperture':
            # Mask_Aperture: aperture 37.0m
            el.append(srwlib.SRWLOptA(
                _shape=v.op_Mask_Aperture_shape,
                _ap_or_ob='a',
                _Dx=v.op_Mask_Aperture_Dx,
                _Dy=v.op_Mask_Aperture_Dy,
                _x=v.op_Mask_Aperture_x,
                _y=v.op_Mask_Aperture_y,
            ))
            pp.append(v.op_Mask_Aperture_pp)
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
        elif el_name == 'Drift_Mask_To_AerialImage':
            # Drift_Mask_To_AerialImage: drift 37.0m
            el.append(srwlib.SRWLOptD(
                _L=v.op_Drift_Mask_To_AerialImage_L,
            ))
            pp.append(v.op_Drift_Mask_To_AerialImage_pp)
        elif el_name == 'Mask_Mask':
            # Mask_Mask
            el.append(srwlib.SRWLOptD(
                _L=0,
            ))
            pp.append(v.op_Mask_Mask_pp)
        elif el_name == 'Watchpoint':
            # Watchpoint: watch 37.00023m
            pass
    #pp.append(v.op_fin_pp)  removed by GVR
    return srwlib.SRWLOptC(el, pp)

    
from wpg.srw.srwl_bl import srwl_uti_merge_options
varParam = srwl_uti_merge_options(varParam, options)

if __name__ == '__main__':
    import os
    os.chdir('/user/home/opt/xl/xl/experiments/speckleFocused/data')
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
    
    

