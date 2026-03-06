#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 19:19:49 2021

@author: gvanriessen
"""
import srwl_bl as srwl_bl


opNames = [ # COMMENT OUT ANY UNNECESSARY OPTICAL ELEMENTS
           # 'zero_drift', 
            'Aperture', 
            'afterAp1_atAp2', 
            'Aperture2', 
            # 'afterAp2_Mask', 
           # 'Block',
            'Mask', 
            # 'Mask_Block', 
            # 'Pinhole',
           # 'Block', 
           # 'Block_detector'
            ]


varParam = [
    ['name', 's', 'XFM', 'simulation name'],

#---Data Folder
    ['fdir', 's', 'XFM/', 'folder (directory) name for reading-in input and saving output data files'],

#---Electron Beam
    ['ebm_nm', 's', '', 'standard electron beam name'],
    ['ebm_nms', 's', '', 'standard electron beam name suffix: e.g. can be Day1, Final'],
    ['ebm_i', 'f', 0.2, 'electron beam current [A]'],
    ['ebm_e', 'f', 3.01, 'electron beam avarage energy [GeV]'],
    ['ebm_de', 'f', 0.0, 'electron beam average energy deviation [GeV]'],
    ['ebm_x', 'f', 0.0, 'electron beam initial average horizontal position [m]'],
    ['ebm_y', 'f', 0.0, 'electron beam initial average vertical position [m]'],
    ['ebm_xp', 'f', 0.0, 'electron beam initial average horizontal angle [rad]'],
    ['ebm_yp', 'f', 0.0, 'electron beam initial average vertical angle [rad]'],
    ['ebm_z', 'f', 0., 'electron beam initial average longitudinal position [m]'],
    ['ebm_dr', 'f', -1.034, 'electron beam longitudinal drift [m] to be performed before a required calculation'],
    ['ebm_ens', 'f', 0.1021, 'electron beam relative energy spread'],
    ['ebm_emx', 'f', 1e-08, 'electron beam horizontal emittance [m]'],
    ['ebm_emy', 'f', 9e-12, 'electron beam vertical emittance [m]'],
    # Definition of the beam through Twiss:
    ['ebm_betax', 'f', 9.0, 'horizontal beta-function [m]'],
    ['ebm_betay', 'f', 3.0, 'vertical beta-function [m]'],
    ['ebm_alphax', 'f', 0.0, 'horizontal alpha-function [rad]'],
    ['ebm_alphay', 'f', 0.0, 'vertical alpha-function [rad]'],
    ['ebm_etax', 'f', 0.0, 'horizontal dispersion function [m]'],
    ['ebm_etay', 'f', 0.0, 'vertical dispersion function [m]'],
    ['ebm_etaxp', 'f', 0.0, 'horizontal dispersion function derivative [rad]'],
    ['ebm_etayp', 'f', 0.0, 'vertical dispersion function derivative [rad]'],

#---Undulator
#---idealized params
    ['und_bx', 'f', 0.0, 'undulator horizontal peak magnetic field [T]'],
    ['und_by', 'f', 1.04, 'undulator vertical peak magnetic field [T]'],
    ['und_phx', 'f', 0.0, 'initial phase of the horizontal magnetic field [rad]'],
    ['und_phy', 'f', 0.0, 'initial phase of the vertical magnetic field [rad]'],
    ['und_sx', 'i', 1, 'undulator horizontal magnetic field symmetry vs longitudinal position'],
    ['und_sy', 'i', 1, 'undulator vertical magnetic field symmetry vs longitudinal position'],
    ['und_b2e', '', '', 'estimate undulator fundamental photon energy (in [eV]) for the amplitude of sinusoidal magnetic field defined by und_b or und_bx, und_by', 'store_true'],
    ['und_e2b', '', '', 'estimate undulator field amplitude (in [T]) for the photon energy defined by w_e', 'store_true'],
# #---tabulated params
#     ['und_g', 'f', 6.72, 'undulator gap [mm] (assumes availability of magnetic measurement or simulation data)'],
#     ['und_ph', 'f', 0.0, 'shift of magnet arrays [mm] for which the field should be set up'],
#     ['und_mdir', 's', '', 'name of magnetic measurements sub-folder'],
#     ['und_mfs', 's', '', 'name of magnetic measurements for different gaps summary file'],
# #---both  params
    ['und_zc', 'f', 0.0, 'undulator center longitudinal position [m]'],
    ['und_per', 'f', 0.022, 'undulator period [m]'],
    ['und_len', 'f', 1.98, 'undulator length [m]'],



#---Calculation Types
    # Electron Trajectory
    ['tr', '', '', 'calculate electron trajectory', 'store_true'],
    ['tr_cti', 'f', 0.0, 'initial time moment (c*t) for electron trajectory calculation [m]'],
    ['tr_ctf', 'f', 0.0, 'final time moment (c*t) for electron trajectory calculation [m]'],
    ['tr_np', 'f', 10000, 'number of points for trajectory calculation'],
    ['tr_mag', 'i', 1, 'magnetic field to be used for trajectory calculation: 1- approximate, 2- accurate'],
    ['tr_fn', 's', 'res_trj.dat', 'file name for saving calculated trajectory data'],
    ['tr_pl', 's', '', 'plot the resulting trajectiry in graph(s): ""- dont plot, otherwise the string should list the trajectory components to plot'],

    #Single-Electron Spectrum vs Photon Energy
    ['ss', '', '', 'calculate single-e spectrum vs photon energy', 'store_true'],
    ['ss_ei', 'f', 100.0, 'initial photon energy [eV] for single-e spectrum vs photon energy calculation'],
    ['ss_ef', 'f', 20000.0, 'final photon energy [eV] for single-e spectrum vs photon energy calculation'],
    ['ss_ne', 'i', 5000, 'number of points vs photon energy for single-e spectrum vs photon energy calculation'],
    ['ss_x', 'f', 0.0, 'horizontal position [m] for single-e spectrum vs photon energy calculation'],
    ['ss_y', 'f', 0.0, 'vertical position [m] for single-e spectrum vs photon energy calculation'],
    ['ss_meth', 'i', 1, 'method to use for single-e spectrum vs photon energy calculation: 0- "manual", 1- "auto-undulator", 2- "auto-wiggler"'],
    ['ss_prec', 'f', 0.01, 'relative precision for single-e spectrum vs photon energy calculation (nominal value is 0.01)'],
    ['ss_pol', 'i', 6, 'polarization component to extract after spectrum vs photon energy calculation: 0- Linear Horizontal, 1- Linear Vertical, 2- Linear 45 degrees, 3- Linear 135 degrees, 4- Circular Right, 5- Circular Left, 6- Total'],
    ['ss_mag', 'i', 1, 'magnetic field to be used for single-e spectrum vs photon energy calculation: 1- approximate, 2- accurate'],
    ['ss_ft', 's', 'f', 'presentation/domain: "f"- frequency (photon energy), "t"- time'],
    ['ss_u', 'i', 1, 'electric field units: 0- arbitrary, 1- sqrt(Phot/s/0.1%bw/mm^2), 2- sqrt(J/eV/mm^2) or sqrt(W/mm^2), depending on representation (freq. or time)'],
    ['ss_fn', 's', 'res_spec_se.dat', 'file name for saving calculated single-e spectrum vs photon energy'],
    ['ss_pl', 's', '', 'plot the resulting single-e spectrum in a graph: ""- dont plot, "e"- show plot vs photon energy'],

    #Multi-Electron Spectrum vs Photon Energy (taking into account e-beam emittance, energy spread and collection aperture size)
    ['sm', '', '', 'calculate multi-e spectrum vs photon energy', 'store_true'],
    ['sm_ei', 'f', 100.0, 'initial photon energy [eV] for multi-e spectrum vs photon energy calculation'],
    ['sm_ef', 'f', 20000.0, 'final photon energy [eV] for multi-e spectrum vs photon energy calculation'],
    ['sm_ne', 'i', 10000, 'number of points vs photon energy for multi-e spectrum vs photon energy calculation'],
    ['sm_x', 'f', 0.0, 'horizontal center position [m] for multi-e spectrum vs photon energy calculation'],
    ['sm_rx', 'f', 0.0001, 'range of horizontal position / horizontal aperture size [m] for multi-e spectrum vs photon energy calculation'],
    ['sm_nx', 'i', 1, 'number of points vs horizontal position for multi-e spectrum vs photon energy calculation'],
    ['sm_y', 'f', 0.0, 'vertical center position [m] for multi-e spectrum vs photon energy calculation'],
    ['sm_ry', 'f', 0.0001, 'range of vertical position / vertical aperture size [m] for multi-e spectrum vs photon energy calculation'],
    ['sm_ny', 'i', 1, 'number of points vs vertical position for multi-e spectrum vs photon energy calculation'],
    ['sm_mag', 'i', 1, 'magnetic field to be used for calculation of multi-e spectrum spectrum or intensity distribution: 1- approximate, 2- accurate'],
    ['sm_hi', 'i', 1, 'initial UR spectral harmonic to be taken into account for multi-e spectrum vs photon energy calculation'],
    ['sm_hf', 'i', 15, 'final UR spectral harmonic to be taken into account for multi-e spectrum vs photon energy calculation'],
    ['sm_prl', 'f', 1.0, 'longitudinal integration precision parameter for multi-e spectrum vs photon energy calculation'],
    ['sm_pra', 'f', 1.0, 'azimuthal integration precision parameter for multi-e spectrum vs photon energy calculation'],
    ['sm_meth', 'i', -1, 'method to use for spectrum vs photon energy calculation in case of arbitrary input magnetic field: 0- "manual", 1- "auto-undulator", 2- "auto-wiggler", -1- dont use this accurate integration method (rather use approximate if possible)'],
    ['sm_prec', 'f', 0.01, 'relative precision for spectrum vs photon energy calculation in case of arbitrary input magnetic field (nominal value is 0.01)'],
    ['sm_nm', 'i', 1, 'number of macro-electrons for calculation of spectrum in case of arbitrary input magnetic field'],
    ['sm_na', 'i', 5, 'number of macro-electrons to average on each node at parallel (MPI-based) calculation of spectrum in case of arbitrary input magnetic field'],
    ['sm_ns', 'i', 5, 'saving periodicity (in terms of macro-electrons) for intermediate intensity at calculation of multi-electron spectrum in case of arbitrary input magnetic field'],
    ['sm_type', 'i', 1, 'calculate flux (=1) or flux per unit surface (=2)'],
    ['sm_pol', 'i', 6, 'polarization component to extract after calculation of multi-e flux or intensity: 0- Linear Horizontal, 1- Linear Vertical, 2- Linear 45 degrees, 3- Linear 135 degrees, 4- Circular Right, 5- Circular Left, 6- Total'],
    ['sm_rm', 'i', 1, 'method for generation of pseudo-random numbers for e-beam phase-space integration: 1- standard pseudo-random number generator, 2- Halton sequences, 3- LPtau sequences (to be implemented)'],
    ['sm_fn', 's', 'res_spec_me.dat', 'file name for saving calculated milti-e spectrum vs photon energy'],
    ['sm_pl', 's', '', 'plot the resulting spectrum-e spectrum in a graph: ""- dont plot, "e"- show plot vs photon energy'],
    #to add options for the multi-e calculation from "accurate" magnetic field

    #Power Density Distribution vs horizontal and vertical position
    ['pw', '', '', 'calculate SR power density distribution', 'store_true'],
    ['pw_x', 'f', 0.0, 'central horizontal position [m] for calculation of power density distribution vs horizontal and vertical position'],
    ['pw_rx', 'f', 0.015, 'range of horizontal position [m] for calculation of power density distribution vs horizontal and vertical position'],
    ['pw_nx', 'i', 100, 'number of points vs horizontal position for calculation of power density distribution'],
    ['pw_y', 'f', 0.0, 'central vertical position [m] for calculation of power density distribution vs horizontal and vertical position'],
    ['pw_ry', 'f', 0.015, 'range of vertical position [m] for calculation of power density distribution vs horizontal and vertical position'],
    ['pw_ny', 'i', 100, 'number of points vs vertical position for calculation of power density distribution'],
    ['pw_pr', 'f', 1.0, 'precision factor for calculation of power density distribution'],
    ['pw_meth', 'i', 1, 'power density computation method (1- "near field", 2- "far field")'],
    ['pw_zst', 'f', 0., 'initial longitudinal position along electron trajectory of power density distribution (effective if pow_sst < pow_sfi)'],
    ['pw_zfi', 'f', 0., 'final longitudinal position along electron trajectory of power density distribution (effective if pow_sst < pow_sfi)'],
    ['pw_mag', 'i', 1, 'magnetic field to be used for power density calculation: 1- approximate, 2- accurate'],
    ['pw_fn', 's', 'res_pow.dat', 'file name for saving calculated power density distribution'],
    ['pw_pl', 's', '', 'plot the resulting power density distribution in a graph: ""- dont plot, "x"- vs horizontal position, "y"- vs vertical position, "xy"- vs horizontal and vertical position'],

    #Single-Electron Intensity distribution vs horizontal and vertical position
    ['si', '', '1', 'calculate single-e intensity distribution (without wavefront propagation through a beamline) vs horizontal and vertical position', 'store_true'],
    #Single-Electron Wavefront Propagation
    ['ws', '', '1', 'calculate single-electron (/ fully coherent) wavefront propagation', 'store_true'],
    #Multi-Electron (partially-coherent) Wavefront Propagation
    ['wm', '', '', 'calculate multi-electron (/ partially coherent) wavefront propagation', 'store_true'],

    ['w_e', 'f', 8340.0, 'photon energy [eV] for calculation of intensity distribution vs horizontal and vertical position'],
    ['w_ef', 'f', -1.0, 'final photon energy [eV] for calculation of intensity distribution vs horizontal and vertical position'],
    ['w_ne', 'i', 1, 'number of points vs photon energy for calculation of intensity distribution'],
    ['w_x', 'f', 0.0, 'central horizontal position [m] for calculation of intensity distribution'],
    ['w_rx', 'f', 0.0004, 'range of horizontal position [m] for calculation of intensity distribution'],
    ['w_nx', 'i', 100, 'number of points vs horizontal position for calculation of intensity distribution'],
    ['w_y', 'f', 0.0, 'central vertical position [m] for calculation of intensity distribution vs horizontal and vertical position'],
    ['w_ry', 'f', 0.0006, 'range of vertical position [m] for calculation of intensity distribution vs horizontal and vertical position'],
    ['w_ny', 'i', 100, 'number of points vs vertical position for calculation of intensity distribution'],
    ['w_smpf', 'f', 2.0, 'sampling factor for calculation of intensity distribution vs horizontal and vertical position'],
    ['w_meth', 'i', 1, 'method to use for calculation of intensity distribution vs horizontal and vertical position: 0- "manual", 1- "auto-undulator", 2- "auto-wiggler"'],
    ['w_prec', 'f', 0.01, 'relative precision for calculation of intensity distribution vs horizontal and vertical position'],
    ['w_mag', 'i', 1, 'magnetic field to be used for calculation of intensity distribution vs horizontal and vertical position: 1- approximate, 2- accurate'],
    ['w_u', 'i', 1, 'electric field units: 0- arbitrary, 1- sqrt(Phot/s/0.1%bw/mm^2), 2- sqrt(J/eV/mm^2) or sqrt(W/mm^2), depending on representation (freq. or time)'],

    ['si_pol', 'i', 6, 'polarization component to extract after calculation of intensity distribution: 0- Linear Horizontal, 1- Linear Vertical, 2- Linear 45 degrees, 3- Linear 135 degrees, 4- Circular Right, 5- Circular Left, 6- Total'],
    ['si_type', 'i', 0, 'type of a characteristic to be extracted after calculation of intensity distribution: 0- Single-Electron Intensity, 1- Multi-Electron Intensity, 2- Single-Electron Flux, 3- Multi-Electron Flux, 4- Single-Electron Radiation Phase, 5- Re(E): Real part of Single-Electron Electric Field, 6- Im(E): Imaginary part of Single-Electron Electric Field, 7- Single-Electron Intensity, integrated over Time or Photon Energy'],
    ['si_fn', 's', 'res_int_se.dat', 'file name for saving calculated single-e intensity distribution (without wavefront propagation through a beamline) vs horizontal and vertical position'],
    ['si_pl', 's', '', 'plot the input intensity distributions in graph(s): ""- dont plot, "x"- vs horizontal position, "y"- vs vertical position, "xy"- vs horizontal and vertical position'],
    ['ws_fni', 's', 'res_int_pr_se.dat', 'file name for saving propagated single-e intensity distribution vs horizontal and vertical position'],
    ['ws_pl', 's', '', 'plot the resulting intensity distributions in graph(s): ""- dont plot, "x"- vs horizontal position, "y"- vs vertical position, "xy"- vs horizontal and vertical position'],

    ['wm_nm', 'i', 1000, 'number of macro-electrons (coherent wavefronts) for calculation of multi-electron wavefront propagation'],
    ['wm_na', 'i', 5, 'number of macro-electrons (coherent wavefronts) to average on each node for parallel (MPI-based) calculation of multi-electron wavefront propagation'],
    ['wm_ns', 'i', 5, 'saving periodicity (in terms of macro-electrons / coherent wavefronts) for intermediate intensity at multi-electron wavefront propagation calculation'],
    ['wm_ch', 'i', 0, 'type of a characteristic to be extracted after calculation of multi-electron wavefront propagation: #0- intensity (s0); 1- four Stokes components; 2- mutual intensity cut vs x; 3- mutual intensity cut vs y; 40- intensity(s0), mutual intensity cuts and degree of coherence vs X & Y'],
    ['wm_ap', 'i', 0, 'switch specifying representation of the resulting Stokes parameters: coordinate (0) or angular (1)'],
    ['wm_x0', 'f', 0.0, 'horizontal center position for mutual intensity cut calculation'],
    ['wm_y0', 'f', 0.0, 'vertical center position for mutual intensity cut calculation'],
    ['wm_ei', 'i', 0, 'integration over photon energy is required (1) or not (0); if the integration is required, the limits are taken from w_e, w_ef'],
    ['wm_rm', 'i', 1, 'method for generation of pseudo-random numbers for e-beam phase-space integration: 1- standard pseudo-random number generator, 2- Halton sequences, 3- LPtau sequences (to be implemented)'],
    ['wm_am', 'i', 0, 'multi-electron integration approximation method: 0- no approximation (use the standard 5D integration method), 1- integrate numerically only over e-beam energy spread and use convolution to treat transverse emittance'],
    ['wm_fni', 's', 'res_int_pr_me.dat', 'file name for saving propagated multi-e intensity distribution vs horizontal and vertical position'],
    ['wm_ff', 's', 'ascii', 'format of file name for saving propagated multi-e intensity distribution vs horizontal and vertical position (ascii and hdf5 supported)'],

    ['wm_nmm', 'i', 1, 'number of MPI masters to use'],
    ['wm_ncm', 'i', 100, 'number of Coherent Modes to calculate'],
    ['wm_acm', 's', 'SP', 'coherent mode decomposition algorithm to be used (supported algorithms are: "SP" for SciPy, "SPS" for SciPy Sparse, "PM" for Primme, based on names of software packages)'],
    ['wm_nop', '', '', 'switch forcing to do calculations ignoring any optics defined (by set_optics function)', 'store_true'],

    ['wm_fnmi', 's', '', 'file name of input cross-spectral density / mutual intensity; if this file name is supplied, the initial cross-spectral density (for such operations as coherent mode decomposition) will not be calculated, but rathre it will be taken from that file.'],
    ['wm_fncm', 's', '', 'file name of input coherent modes; if this file name is supplied, the eventual partially-coherent radiation propagation simulation will be done based on propagation of the coherent modes from that file.'],

    ['wm_fbk', '', '', 'create backup file(s) with propagated multi-e intensity distribution vs horizontal and vertical position and other radiation characteristics', 'store_true'],

    # Optics parameters
    ['op_r', 'f', 20.0, 'longitudinal position of the first optical element [m]'],
    # Former appParam:
    ['rs_type', 's', 'u', 'source type, (u) idealized undulator, (t), tabulated undulator, (m) multipole, (g) gaussian beam'],

    #added by GVR for compatibility with new SRW 
    ['ws_fnei', 's', '', 'file name for loading initial electric field wavefront for propagation'], # added by jk
    ['ws_fnep', 's', 'EField.dat', 'file name for saving electric field wavefront after propagation'],
    
    ['op_rv','l',[[1,2,3,4,5,6,7,8,9],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1]], 'list of optical element indexes (1-based) after which intensity or other characteristics should be extracted'], #added - JK 11/05/23

    ['stokes_fname','s','stokes',''],
    ['res_ipm','','','container for results of multi-electron wavefront propagation.'],
    
    ['und_b2e', '', False,'estimate undulator fundamental photon energy (in [eV]) for the amplitude of sinusoidal magnetic field defined by und_b or und_bx, und_by', 'store_true'],
    ['und_e2b', '', False,'estimate undulator field amplitude (in [T]) for the photon energy defined by w_e', 'store_true'],
    ['si_res', '', '', 'extra parameter to stop crashing'],
    
    # ['om','','','extra parameter to stop crashing'],

#---Beamline optics:
    # # zero_drift: drift
    # ['op_zero_drift_L', 'f', 0, 'length'],

    # Aperture: aperture
    ['op_Aperture_shape', 's', 'r', 'shape'],
    ['op_Aperture_Dx', 'f', 5e-05, 'horizontalSize'],
    ['op_Aperture_Dy', 'f', 5e-05, 'verticalSize'],
    ['op_Aperture_x', 'f', 0.0, 'horizontalOffset'],
    ['op_Aperture_y', 'f', 0.0, 'verticalOffset'],

    # afterAp1_atAp2: drift
    ['op_afterAp1_atAp2_L', 'f', 10.0, 'length'],

    # Aperture2: aperture
    ['op_Aperture2_shape', 's', 'r', 'shape'],
    ['op_Aperture2_Dx', 'f', 80.0e-6, 'horizontalSize'],
    ['op_Aperture2_Dy', 'f', 80.0e-6, 'verticalSize'],
    ['op_Aperture2_x', 'f', 0.0, 'horizontalOffset'],
    ['op_Aperture2_y', 'f', 0.0, 'verticalOffset'],

    # afterAp2_Mask: drift
    ['op_afterAp2_Mask_L', 'f', 1.0, 'length'],

    # # Mask: Mask
    # ['op_Mask_file_path', 's', '/user/home/opt/xl/xl/FZP_100um_80offX0offY.tif', 'imageFile'], # '/user/home/opt/xl/xl/experiments/masks3/SLS_200p30.0r_Mask.tif' 'XFM/masks/single_grating_40pixelpitch.tif', 'imageFile'],
    # ['op_Mask_outputImageFormat', 's', 'tif', 'outputImageFormat'],
    # ['op_Mask_position', 'f', 30.0, 'position'],
    # ['op_Mask_resolution', 'f', 5.0e-09, 'resolution'],
    # ['op_Mask_thick', 'f', 7.803397518091064e-2, 'thickness'], #44.0e-09 #  7.803397518091064e-6
    # ['op_Mask_delta', 'f', 1.9050946469820692e-05, 'refractiveIndex'], # Modelled as pure SiO2 as in Wang et al, Nanotechnology 22 065301 delta =  1.2871318526133276E-05
    # ['op_Mask_atten_len', 'f', 3.4196326767582247e-06, 'attenuationLength'],  # 5.671221134882591e-05
    # ['op_Mask_horizontalCenterCoordinate', 'f', 0.0, 'horizontalCenterCoordinate'],
    # ['op_Mask_verticalCenterCoordinate', 'f', 0.0, 'verticalCenterCoordinate'],
    # ['op_Mask_rotateAngle', 'f', 0.0, 'rotateAngle'],
    # ['op_Mask_cutoffBackgroundNoise', 'f', 0.001, 'cutoffBackgroundNoise'],
    # # ['op_Mask_rx', 'f', 30.0e-06, 'rx'],
    # # ['op_Mask_ry', 'f', 100.0e-06, 'ry'],
    # # ['op_Mask_dens', 'f', 2.2, 'dens'],
    # # ['op_Mask_r_min_bw_obj', 'f', 1e-09, 'r_min_bw_obj'],
    # # ['op_Mask_edge_frac', 'f', 0.02, 'edge_frac'],
    # # ['op_Mask_obj_size_min', 'f', 1e-07, 'obj_size_min'],
    # # ['op_Mask_ang_min', 'f', 0.0, 'ang_min'],
    # # ['op_Mask_obj_size_max', 'f', 1.2e-07, 'obj_size_max'],
    # # ['op_Mask_ang_max', 'f', 45.0, 'ang_max'],
    # # ['op_Mask_obj_size_ratio', 'f', 0.5, 'obj_size_ratio'],
    # ['op_Mask_cropArea', 'i', 0, 'cropArea'],
    # ['op_Mask_extTransm', 'i', 0, 'transmissionImage'],
    # ['op_Mask_areaXStart', 'i', 0, 'areaXStart'],
    # ['op_Mask_areaXEnd', 'i', 20000, 'areaXEnd'],
    # ['op_Mask_areaYStart', 'i', 0, 'areaYStart'],
    # ['op_Mask_areaYEnd', 'i', 20000, 'areaYEnd'],
    # ['op_Mask_rotateReshape', 'i', 0, 'rotateReshape'],
    # ['op_Mask_backgroundColor', 'i', 0, 'backgroundColor'],
    # ['op_Mask_tileImage', 'i', 0, 'tileImage'],
    # ['op_Mask_tileRows', 'i', 0, 'tileRows'],
    # ['op_Mask_tileColumns', 'i', 0, 'tileColumns'],
    # ['op_Mask_shiftX', 'i', 0, 'shiftX'],
    # ['op_Mask_shiftY', 'i', 0, 'shiftY'],
    # ['op_Mask_invert', 'i', 0, 'invert'],
    # # ['op_Mask_nx', 'i', 4000, 'nx'],
    # # ['op_Mask_ny', 'i', 4000, 'ny'],
    # # ['op_Mask_obj_type', 'i', 1, 'obj_type'],
    # # ['op_Mask_size_dist', 'i', 1, 'size_dist'],
    # # ['op_Mask_ang_dist', 'i', 1, 'ang_dist'],
    # # ['op_Mask_rand_alg', 'i', 1, 'rand_alg'],
    # # ['op_Mask_poly_sides', 'i', 6, 'poly_sides'],
    # # ['op_Mask_rand_shapes', 'i', 0, 'rand_shapes'],
    # # ['op_Mask_rand_obj_size', 'b', False, 'rand_obj_size'],
    # ['op_Mask_rand_poly_side', 'b', False, 'rand_poly_side'],

    # Mask_Block: drift
    ['op_Mask_Block_L', 'f', 0.10, 'length'],

    # Block: Mask
    ['op_Block_file_path', 's', '/user/home/opt/xl/xl/experiments/masks3/SLS_200p30.0r_Block.tif', 'imageFile'],
    ['op_Block_outputImageFormat', 's', 'tif', 'outputImageFormat'],
    ['op_Block_position', 'f', 10.0, 'position'],
    ['op_Block_resolution', 'f', 2.5e-08, 'resolution'],
    ['op_Block_thick', 'f', 50.0e-06, 'thickness'],
    ['op_Block_delta', 'f', 2.970837201294633e-5, 'refractiveIndex'], # - JK 07/11/23  # gold is ~8.0e-5 values obtained from Lu, Ming, et al. "Fabrication of high-aspect-ratio hard x-ray zone plates with HSQ plating molds."
    ['op_Block_atten_len', 'f', 4.52932e-6, 'attenuationLength'], # was 1.17437e-6
    ['op_Block_xc', 'f', 0.0, 'horizontalCenterCoordinate'],
    ['op_Block_yc', 'f', 0.0, 'verticalCenterCoordinate'],
    ['op_Block_rotateAngle', 'f', 0.0, 'rotateAngle'],
    ['op_Block_cutoffBackgroundNoise', 'f', 0.0, 'cutoffBackgroundNoise'],
    # ['op_Block_rx', 'f', 1e-05, 'rx'],
    # ['op_Block_ry', 'f', 1e-05, 'ry'],
    # ['op_Block_dens', 'f', 20000000.0, 'dens'],
    # ['op_Block_r_min_bw_obj', 'f', 1e-09, 'r_min_bw_obj'],
    # ['op_Block_edge_frac', 'f', 0.02, 'edge_frac'],
    # ['op_Block_obj_size_min', 'f', 1e-07, 'obj_size_min'],
    # ['op_Block_ang_min', 'f', 0.0, 'ang_min'],
    # ['op_Block_obj_size_max', 'f', 1.2e-07, 'obj_size_max'],
    # ['op_Block_ang_max', 'f', 45.0, 'ang_max'],
    # ['op_Block_obj_size_ratio', 'f', 0.5, 'obj_size_ratio'],
    ['op_Block_cropArea', 'i', 1, 'cropArea'],
    ['op_Block_extTransm', 'i', 0, 'transmissionImage'],
    ['op_Block_areaXStart', 'i', 0, 'areaXStart'],
    ['op_Block_areaXEnd', 'i', 4326, 'areaXEnd'],
    ['op_Block_areaYStart', 'i', 0, 'areaYStart'],
    ['op_Block_areaYEnd', 'i', 4326, 'areaYEnd'],
    ['op_Block_rotateReshape', 'i', 0, 'rotateReshape'],
    ['op_Block_backgroundColor', 'i', 0, 'backgroundColor'],
    ['op_Block_tileImage', 'i', 0, 'tileImage'],
    ['op_Block_tileRows', 'i', 0, 'tileRows'],
    ['op_Block_tileColumns', 'i', 0, 'tileColumns'],
    ['op_Block_shiftX', 'i', 0, 'shiftX'],
    ['op_Block_shiftY', 'i', 0, 'shiftY'],
    ['op_Block_invert', 'i', 0, 'invert'],
    # ['op_Block_nx', 'i', 1001, 'nx'],
    # ['op_Block_ny', 'i', 1001, 'ny'],
    # ['op_Block_obj_type', 'i', 1, 'obj_type'],
    # ['op_Block_size_dist', 'i', 1, 'size_dist'],
    # ['op_Block_ang_dist', 'i', 1, 'ang_dist'],
    # ['op_Block_rand_alg', 'i', 1, 'rand_alg'],
    # ['op_Block_poly_sides', 'i', 6, 'poly_sides'],
    # ['op_Block_rand_shapes', 'i', 0, 'rand_shapes'],
    # ['op_Block_rand_obj_size', 'b', False, 'rand_obj_size'],
    # ['op_Block_rand_poly_side', 'b', False, 'rand_poly_side'],
    
    # Sample: sample
    ['op_Sample_file_path', 's', '/user/home/opt/xl/xl/FZP_10um_10offX0offY.tif', 'imageFile'],
    ['op_Sample_outputImageFormat', 's', 'tif', 'outputImageFormat'],
    ['op_Sample_position', 'f', 70.0, 'position'],
    ['op_Sample_resolution', 'f', 1e-08, 'resolution'],
    ['op_Sample_thick', 'f', 1e-05, 'thickness'],
    ['op_Sample_delta', 'f', 0.014120740235449956, 'refractiveIndex'],
    ['op_Sample_atten_len', 'f', 4.831876577964474e-07, 'attenuationLength'],
    ['op_Sample_xc', 'f', 0.0, 'horizontalCenterCoordinate'],
    ['op_Sample_yc', 'f', 0.0, 'verticalCenterCoordinate'],
    ['op_Sample_rotateAngle', 'f', 0.0, 'rotateAngle'],
    ['op_Sample_cutoffBackgroundNoise', 'f', 0.0, 'cutoffBackgroundNoise'],
    ['op_Sample_rx', 'f', 1e-05, 'rx'],
    ['op_Sample_ry', 'f', 1e-05, 'ry'],
    ['op_Sample_dens', 'f', 20000000.0, 'dens'],
    ['op_Sample_r_min_bw_obj', 'f', 1e-09, 'r_min_bw_obj'],
    ['op_Sample_edge_frac', 'f', 0.02, 'edge_frac'],
    ['op_Sample_obj_size_min', 'f', 1e-07, 'obj_size_min'],
    ['op_Sample_ang_min', 'f', 0.0, 'ang_min'],
    ['op_Sample_obj_size_max', 'f', 1.2e-07, 'obj_size_max'],
    ['op_Sample_ang_max', 'f', 45.0, 'ang_max'],
    ['op_Sample_obj_size_ratio', 'f', 0.5, 'obj_size_ratio'],
    ['op_Sample_cropArea', 'i', 1, 'cropArea'],
    ['op_Sample_extTransm', 'i', 0, 'transmissionImage'],
    ['op_Sample_areaXStart', 'i', 0, 'areaXStart'],
    ['op_Sample_areaXEnd', 'i', 800, 'areaXEnd'],
    ['op_Sample_areaYStart', 'i', 0, 'areaYStart'],
    ['op_Sample_areaYEnd', 'i', 800, 'areaYEnd'],
    ['op_Sample_rotateReshape', 'i', 0, 'rotateReshape'],
    ['op_Sample_backgroundColor', 'i', 0, 'backgroundColor'],
    ['op_Sample_tileImage', 'i', 0, 'tileImage'],
    ['op_Sample_tileRows', 'i', 1, 'tileRows'],
    ['op_Sample_tileColumns', 'i', 1, 'tileColumns'],
    ['op_Sample_shiftX', 'i', 0, 'shiftX'],
    ['op_Sample_shiftY', 'i', 0, 'shiftY'],
    ['op_Sample_invert', 'i', 0, 'invert'],
    ['op_Sample_nx', 'i', 1001, 'nx'],
    ['op_Sample_ny', 'i', 1001, 'ny'],
    ['op_Sample_obj_type', 'i', 1, 'obj_type'],
    ['op_Sample_size_dist', 'i', 1, 'size_dist'],
    ['op_Sample_ang_dist', 'i', 1, 'ang_dist'],
    ['op_Sample_rand_alg', 'i', 1, 'rand_alg'],
    ['op_Sample_poly_sides', 'i', 6, 'poly_sides'],
    ['op_Sample_rand_shapes', 'i', [1, 2, 3, 4], 'rand_shapes'],
    ['op_Sample_rand_obj_size', 'b', False, 'rand_obj_size'],
    ['op_Sample_rand_poly_side', 'b', False, 'rand_poly_side'],
    
    #  # Mask: sample [values for Si3N4]
    # ['op_Mask_file_path', 's', '/user/home/opt/xl/xl/FZP_100um_80offX0offY.tif', 'imageFile'], #mask1IN
    # ['op_Mask_outputImageFormat', 's', 'tif', 'outputImageFormat'],
    # ['op_Mask_position', 'f', 37.0, 'position'],
    # ['op_Mask_resolution', 'f', 5.0e-09, 'resolution'], 
    # ['op_Mask_thick', 'f', 5.0e-6, 'thickness'], # thickness for pi phase shift @ 185 eV: 0.4746102860553121e-06
    # ['op_Mask_delta', 'f', 0.014120740235449956, 'refractiveIndex'], #UPDATED -JK
    # ['op_Mask_atten_len', 'f', 4.831876577964474e-07, 'attenuationLength'],  #UPDATED -JK
    # ['op_Mask_horizontalCenterCoordinate', 'f', 0.0, 'horizontalCenterCoordinate'],
    # ['op_Mask_verticalCenterCoordinate', 'f', 0.0, 'verticalCenterCoordinate'],
    # ['op_Mask_rotateAngle', 'f', 0.0, 'rotateAngle'],
    # ['op_Mask_cutoffBackgroundNoise', 'f', 0.001, 'cutoffBackgroundNoise'],
    # ['op_Mask_cropArea', 'i', 0, 'cropArea'],
    # ['op_Mask_extTransm', 'i', 0, 'transmissionImage'], 
    # ['op_Mask_areaXStart', 'i', 0, 'areaXStart'],
    # ['op_Mask_areaXEnd', 'i', 20000, 'areaXEnd'],  #17000 #200
    # ['op_Mask_areaYStart', 'i', 0, 'areaYStart'],
    # ['op_Mask_areaYEnd', 'i', 20000, 'areaYEnd'], #17000 #798
    # ['op_Mask_rotateReshape', 'i', 0, 'rotateReshape'],
    # ['op_Mask_backgroundColor', 'i', 0, 'backgroundColor'],
    # ['op_Mask_tileImage', 'i', 0, 'tileImage'],
    # ['op_Mask_tileRows', 'i', 0, 'tileRows'],
    # ['op_Mask_tileColumns', 'i', 0, 'tileColumns'],
    # ['op_Mask_shiftX', 'i', 0, 'shiftX'],
    # ['op_Mask_shiftY', 'i', 0, 'shiftY'],
    # ['op_Mask_invert', 'i', 0, 'invert'],

    # Pinhole: aperture
    ['op_Pinhole_shape', 's', 'c', 'shape'],
    ['op_Pinhole_Dx', 'f', 2.0e-6, 'horizontalSize'],
    ['op_Pinhole_Dy', 'f', 2.0e-6, 'verticalSize'],
    ['op_Pinhole_x', 'f', 0.0, 'horizontalOffset'],
    ['op_Pinhole_y', 'f', 0.0, 'verticalOffset'],



    # Block_detector: drift
    ['op_Block_detector_L', 'f', 0.5, 'length'],

#---Propagation parameters
    ['op_zero_drift_pp', 'f',       [0, 0, 1.0, 0, 0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'zero_drift'],
    ['op_Aperture_pp', 'f',         [0, 0, 1.0, 0, 0, 0.1, 10.0, 0.1, 10.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'Aperture'],
    ['op_afterAp1_atAp2_pp', 'f',   [0, 0, 1.0, 1, 0, 50.0, 1.5, 50.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'afterAp1_atAp2'],
    ['op_Aperture2_pp', 'f',        [0, 0, 1.0, 0, 0, 0.1, 120.0, 0.1, 10.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'Aperture2'],
    # ['op_afterAp2_Mask_pp', 'f',  [0, 0, 1.0, 1, 0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'afterAp2_Mask'],
    ['op_Mask_pp', 'f',             [0, 0, 1.0, 0, 0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'Mask'],
    ['op_Mask_Block_pp', 'f',       [0, 0, 1.0, 0, 0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'Mask_Block'],
    ['op_Block_pp', 'f',            [0, 0, 1.0, 0, 0, 0.1, 10.0, 0.1, 75.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'Block'],
    ['op_Pinhole_pp', 'f',          [0, 0, 1.0, 0, 0, 0.2, 5.0, 0.2, 5.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'Pinhole'],
    ['op_Block_detector_pp', 'f',   [0, 0, 1.0, 0, 0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'Block_detector'],
    ['op_fin_pp', 'f',              [0, 0, 1.0, 0, 0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'final post-propagation (resize) parameters'],

    #[ 0]: Auto-Resize (1) or not (0) Before propagation
    #[ 1]: Auto-Resize (1) or not (0) After propagation
    #[ 2]: Relative Precision for propagation with Auto-Resizing (1. is nominal)
    #[ 3]: Allow (1) or not (0) for semi-analytical treatment of the quadratic (leading) phase terms at the propagation
    #[ 4]: Do any Resizing on Fourier side, using FFT, (1) or not (0)
    #[ 5]: Horizontal Range modification factor at Resizing (1. means no modification)
    #[ 6]: Horizontal Resolution modification factor at Resizing
    #[ 7]: Vertical Range modification factor at Resizing
    #[ 8]: Vertical Resolution modification factor at Resizing
    #[ 9]: Type of wavefront Shift before Resizing (not yet implemented)
    #[10]: New Horizontal wavefront Center position after Shift (not yet implemented)
    #[11]: New Vertical wavefront Center position after Shift (not yet implemented)
    #[12]: Optional: Orientation of the Output Optical Axis vector in the Incident Beam Frame: Horizontal Coordinate
    #[13]: Optional: Orientation of the Output Optical Axis vector in the Incident Beam Frame: Vertical Coordinate
    #[14]: Optional: Orientation of the Output Optical Axis vector in the Incident Beam Frame: Longitudinal Coordinate
    #[15]: Optional: Orientation of the Horizontal Base vector of the Output Frame in the Incident Beam Frame: Horizontal Coordinate
    #[16]: Optional: Orientation of the Horizontal Base vector of the Output Frame in the Incident Beam Frame: Vertical Coordinate
]

        


    
options = [              
    # Option to save wavefield after each element for inspection
    ['op_WBS_cache', 'f',                                               0, 'Cache wavefront after WBS'],
    ['op_After_WBS_Before_Toroidal_Mirror_cache', 'f',                  0, 'Cache wavefront after After_WBS_Before_Toroidal_Mirror'],
    ['op_Toroidal_Mirror_cache', 'f',                                   0, 'Cache wavefront after Toroid'],
    ['op_After_Toroidal_Mirror_Before_PGM_cache', 'f',                  0, 'Cache wavefront after After_Toroidal_Mirror_Before_PGM'],
    ['op_Planar_Mirror_cache', 'f',                                     0, 'Cache wavefront after Planar'],
    ['op_Planar_Mirror_Grating_cache', 'f',                             0, 'Cache wavefront after Planar_Grating'],
    ['op_Grating_cache', 'f',                                           0, 'Cache wavefront after Grating'],
    ['op_Grating_Before_Exit_Aperture_cache', 'f',                      0, 'Cache wavefront after Grating_Before_Exit_Aperture'],
    ['op_Exit_Aperture_cache', 'f',                                     0, 'Cache wavefront after Exit Aperture'],
    ['op_After_Mask_Aperture_Before_Cylindrical_Mirror_cache', 'f',     0, 'Cache wavefront after After_Mask_Aperture_Before_Cylindrical_Mirror'],
    ['op_Cylindrical_Mirror_cache', 'f',                                0, 'Cache wavefront after Toroid_turned_into_a_Cylinder'],
    ['op_After_Cylindrical_Mirror_Before_Exit_Slit_cache', 'f',         0, 'Cache wavefront after After_Cylindrical_Mirror_Before_Exit_Slit'],
    ['op_Exit_Slits_cache', 'f',                                        0, 'Cache wavefront after Exit Slits'],
    ['op_After_Exit_Slit_Before_BDA_cache', 'f',                        0, 'Cache wavefront after After_Exit_Slit_Before_BDA'],
    ['op_BDA_cache', 'f',                                               0, 'Cache wavefront after BDA'],
    ['op_Mask_Aperture_cache', 'f',                                     0, 'Cache wavefront after Mask Aperture'],
    ['op_BDA_Mask_Aperture_cache', 'f',                                 0, 'Cache wavefront after BDA MAsk Aperture Drift'],
    ['op_fin', 'f',                                                     0, 'Cache final wavefront'],
    #['op_After_BDA_Before_FZP_cache', 'f',                             0, 'Cache wavefront after After_BDA_Before_FZP'],
    #['op_FZP_cache', 'f',                                              0, 'Cache wavefront after FZP'],
    #['op_After_FZP_Before_OSA_cache', 'f',                             0, 'Cache wavefront after After_FZP_Before_OSA'],
    #['op_OSA_cache', 'f',                                              0, 'Cache wavefront after OSA'],
    #['op_After_OSA_Before_Grating_cache', 'f',                         0, 'Cache wavefront after After_OSA_Before_Grating'], 

    #list copied from above
    ['opList','s', opNames, 'List of names of optical elements'],

    # Specify source type (use g)
    # override source type, optionally using a new option 'r' (you probably won't want to do this for first run...)
    ['rs_type', 's', 'u', 'source type, (u) idealized undulator, \
                                        (t), tabulated undulator, \
                                        (m) multipole, \
                                        (g) gaussian beam, \
                                        (r) restore from file'],
                                        
    # specify a saved wavefield to load instead of simulating source
    # uses same file path for saving when source is not 'r'
    ['wfr_file', 's', '', 'file name for saved wavefront.  Used to continue simulation from existing source.'],
    ['op_MaskResolutionX', 'f', 1.25e-08, 'horizontalPixelSize'],
    ['op_MaskResolutionY', 'f', 1.25e-08, 'verticalPixelSize']
    ]
