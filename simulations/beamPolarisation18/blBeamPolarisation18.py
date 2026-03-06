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
            # maskObtacle: sample 37.0m
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
            # maskSubstrate: sample
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
            
        elif el_name == 'Farfield_Propagation':
            # Farfield_Propagation: drift 15.0m
            el.append(srwlib.SRWLOptD(
                _L=v.op_Farfield_Propagation_L,
            ))
            pp.append(v.op_Farfield_Propagation_pp)
    pp.append(v.op_fin_pp)
    return srwlib.SRWLOptC(el, pp)


    
from wpg.srw.srwl_bl import srwl_uti_merge_options
varParam = srwl_uti_merge_options(varParam, options)

def main():
    import os
    os.chdir('/user/home/opt/xl/xl/experiments/beamPolarisation18/data')
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
