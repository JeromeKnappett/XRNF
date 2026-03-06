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
        if el_name == 'zero_drift1':
            # zero_drift1: drift 20.0m
            el.append(srwlib.SRWLOptD(
                _L=v.op_zero_drift1_L,
            ))
            pp.append(v.op_zero_drift1_pp)
        elif el_name == 'M1A':
            # M1A: mirror 20.0m
            mirror_file = v.op_M1A_hfn
            assert os.path.isfile(mirror_file), \
                'Missing input file {}, required by M1A beamline element'.format(mirror_file)
            el.append(srwlib.srwl_opt_setup_surf_height_1d(
                srwlib.srwl_uti_read_data_cols(mirror_file, "\t", 0, 1),
                _dim=v.op_M1A_dim,
                _ang=abs(v.op_M1A_ang),
                _amp_coef=v.op_M1A_amp_coef,
                _size_x=v.op_M1A_size_x,
                _size_y=v.op_M1A_size_y,
            ))
            pp.append(v.op_M1A_pp)
        elif el_name == 'M1Ae_M1Bi':
            # M1Ae_M1Bi: drift 20.0m
            el.append(srwlib.SRWLOptD(
                _L=v.op_M1Ae_M1Bi_L,
            ))
            pp.append(v.op_M1Ae_M1Bi_pp)
        elif el_name == 'M1B':
            # M1B: toroidalMirror 20.978m
            el.append(srwlib.SRWLOptMirTor(
                _rt=v.op_M1B_rt,
                _rs=v.op_M1B_rs,
                _size_tang=v.op_M1B_size_tang,
                _size_sag=v.op_M1B_size_sag,
                _x=v.op_M1B_horizontalPosition,
                _y=v.op_M1B_verticalPosition,
                _ap_shape=v.op_M1B_ap_shape,
                _nvx=v.op_M1B_nvx,
                _nvy=v.op_M1B_nvy,
                _nvz=v.op_M1B_nvz,
                _tvx=v.op_M1B_tvx,
                _tvy=v.op_M1B_tvy,
            ))
            pp.append(v.op_M1B_pp)

        elif el_name == 'M1Be_A1i':
            # M1Be_A1i: drift 20.978m
            el.append(srwlib.SRWLOptD(
                _L=v.op_M1Be_A1i_L,
            ))
            pp.append(v.op_M1Be_A1i_pp)
        elif el_name == 'A1':
            # A1: aperture 22.0m
            el.append(srwlib.SRWLOptA(
                _shape=v.op_A1_shape,
                _ap_or_ob='a',
                _Dx=v.op_A1_Dx,
                _Dy=v.op_A1_Dy,
                _x=v.op_A1_x,
                _y=v.op_A1_y,
            ))
            pp.append(v.op_A1_pp)
        elif el_name == 'A1e_PGMi':
            # A1e_PGMi: drift 22.0m
            el.append(srwlib.SRWLOptD(
                _L=v.op_A1e_PGMi_L,
            ))
            pp.append(v.op_A1e_PGMi_pp)
        elif el_name == 'VDG1':
            # VDG1: grating 25.256m
            mirror = srwlib.SRWLOptMirPl(
                _size_tang=v.op_VDG1_size_tang,
                _size_sag=v.op_VDG1_size_sag,
                _nvx=v.op_VDG1_nvx,
                _nvy=v.op_VDG1_nvy,
                _nvz=v.op_VDG1_nvz,
                _tvx=v.op_VDG1_tvx,
                _tvy=v.op_VDG1_tvy,
                _x=v.op_VDG1_x,
                _y=v.op_VDG1_y,
            )
            opEl=srwlib.SRWLOptG(
                _mirSub=mirror,
                _m=v.op_VDG1_m,
                _grDen=v.op_VDG1_grDen,
                _grDen1=v.op_VDG1_grDen1,
                _grDen2=v.op_VDG1_grDen2,
                _grDen3=v.op_VDG1_grDen3,
                _grDen4=v.op_VDG1_grDen4,
                _e_avg=v.op_VDG1_e_avg,
                _cff=v.op_VDG1_cff,
                _ang_graz=v.op_VDG1_ang,
                _ang_roll=v.op_VDG1_rollAngle,
            )
            el.append(opEl)
            pp.append(v.op_VDG1_pp)

        elif el_name == 'VDG1_M2A':
            # VDG1_M2A: drift 25.256m
            el.append(srwlib.SRWLOptD(
                _L=v.op_VDG1_M2A_L,
            ))
            pp.append(v.op_VDG1_M2A_pp)
        elif el_name == 'M2A':
            # M2A: mirror 25.756m
            mirror_file = v.op_M2A_hfn
            assert os.path.isfile(mirror_file), \
                'Missing input file {}, required by M2A beamline element'.format(mirror_file)
            el.append(srwlib.srwl_opt_setup_surf_height_1d(
                srwlib.srwl_uti_read_data_cols(mirror_file, "\t", 0, 1),
                _dim=v.op_M2A_dim,
                _ang=abs(v.op_M2A_ang),
                _amp_coef=v.op_M2A_amp_coef,
                _size_x=v.op_M2A_size_x,
                _size_y=v.op_M2A_size_y,
            ))
            pp.append(v.op_M2A_pp)
        elif el_name == 'M2A_M3':
            # M2A_M3: drift 25.756m
            el.append(srwlib.SRWLOptD(
                _L=v.op_M2A_M3_L,
            ))
            pp.append(v.op_M2A_M3_pp)
        elif el_name == 'M3':
            # M3: toroidalMirror 30.084m
            el.append(srwlib.SRWLOptMirTor(
                _rt=v.op_M3_rt,
                _rs=v.op_M3_rs,
                _size_tang=v.op_M3_size_tang,
                _size_sag=v.op_M3_size_sag,
                _x=v.op_M3_horizontalPosition,
                _y=v.op_M3_verticalPosition,
                _ap_shape=v.op_M3_ap_shape,
                _nvx=v.op_M3_nvx,
                _nvy=v.op_M3_nvy,
                _nvz=v.op_M3_nvz,
                _tvx=v.op_M3_tvx,
                _tvy=v.op_M3_tvy,
            ))
            pp.append(v.op_M3_pp)

        elif el_name == 'PGMe_A2i':
            # PGMe_A2i: drift 30.084m
            el.append(srwlib.SRWLOptD(
                _L=v.op_PGMe_A2i_L,
            ))
            pp.append(v.op_PGMe_A2i_pp)
        elif el_name == 'A2':
            # A2: aperture 38.412m
            el.append(srwlib.SRWLOptA(
                _shape=v.op_A2_shape,
                _ap_or_ob='a',
                _Dx=v.op_A2_Dx,
                _Dy=v.op_A2_Dy,
                _x=v.op_A2_x,
                _y=v.op_A2_y,
            ))
            pp.append(v.op_A2_pp)
        elif el_name == 'A2e_M4i':
            # A2e_M4i: drift 38.412m
            el.append(srwlib.SRWLOptD(
                _L=v.op_A2e_M4i_L,
            ))
            pp.append(v.op_A2e_M4i_pp)
        elif el_name == 'M4':
            # M4: toroidalMirror 48.74m
            el.append(srwlib.SRWLOptMirTor(
                _rt=v.op_M4_rt,
                _rs=v.op_M4_rs,
                _size_tang=v.op_M4_size_tang,
                _size_sag=v.op_M4_size_sag,
                _x=v.op_M4_horizontalPosition,
                _y=v.op_M4_verticalPosition,
                _ap_shape=v.op_M4_ap_shape,
                _nvx=v.op_M4_nvx,
                _nvy=v.op_M4_nvy,
                _nvz=v.op_M4_nvz,
                _tvx=v.op_M4_tvx,
                _tvy=v.op_M4_tvy,
            ))
            pp.append(v.op_M4_pp)

        elif el_name == 'M4e_A3i':
            # M4e_A3i: drift 48.74m
            el.append(srwlib.SRWLOptD(
                _L=v.op_M4e_A3i_L,
            ))
            pp.append(v.op_M4e_A3i_pp)
        elif el_name == 'A3':
            # A3: aperture 49.74m
            el.append(srwlib.SRWLOptA(
                _shape=v.op_A3_shape,
                _ap_or_ob='a',
                _Dx=v.op_A3_Dx,
                _Dy=v.op_A3_Dy,
                _x=v.op_A3_x,
                _y=v.op_A3_y,
            ))
            pp.append(v.op_A3_pp)
        elif el_name == 'A3e_Samplei':
            # A3e_Samplei: drift 49.74m
            el.append(srwlib.SRWLOptD(
                _L=v.op_A3e_Samplei_L,
            ))
            pp.append(v.op_A3e_Samplei_pp)
            
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
    os.chdir('/user/home/opt_cmd/xl/xl/experiments/SOLEIL_telePtycho/data')
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
    
    

