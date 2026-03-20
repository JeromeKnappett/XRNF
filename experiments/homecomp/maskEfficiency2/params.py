#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 19:19:49 2021

@author: gvanriessen
"""
import srwl_bl as srwl_bl


opNames = [ # COMMENT OUT ANY UNNECESSARY OPTICAL ELEMENTS
            'zero_drift', 
            'Mask_Aperture',   # Aperture to block wavefield at mask edges (Should be size of mask)
#            'maskObstacle',
#            'maskSubstrate',
#            'Mask',
#            'Farfield_Propagation'  #GVR: note that naming consistency preferred, e.g. driftFarfield (camel case, noun)
             ]



varParam = srwl_bl.srwl_uti_ext_options([
    ['name', 's', 'MaskTest', 'simulation name'],

#---Data Folder
    ['fdir', 's', '', 'folder (directory) name for reading-in input and saving output data files'],

#--- Gaussian Beam Properties (If energy is changed here it must also be changed for Wavefront Propagation (~line 300))
    ['gbm_x', 'f', 0.0, 'average horizontal coordinates of waist [m]'],
    ['gbm_y', 'f', 0.0, 'average vertical coordinates of waist [m]'],
    ['gbm_z', 'f', 0.0, 'average longitudinal coordinate of waist [m]'],
    ['gbm_xp', 'f', 0.0, 'average horizontal angle at waist [rad]'],
    ['gbm_yp', 'f', 0.0, 'average verical angle at waist [rad]'],
    ['gbm_ave', 'f', 184.76, 'average photon energy [eV]'],           # CHANGE INCIDENT ENERGY HERE (184.76 eV ~ 6.7 nm, 90.44 eV ~ 13.5 nm)
    ['gbm_pen', 'f', 0.001, 'energy per pulse [J]'],
    ['gbm_rep', 'f', 1, 'rep. rate [Hz]'],
    ['gbm_pol', 'f', 1, 'polarization 1- lin. hor., 2- lin. vert., 3- lin. 45 deg., 4- lin.135 deg., 5- circ. right, 6- circ. left'],
    ['gbm_sx', 'f', 0.01, 'rms beam size vs horizontal position [m] at waist (for intensity)'],
    ['gbm_sy', 'f', 0.01, 'rms beam size vs vertical position [m] at waist (for intensity)'],#9.787229999999999e-06
    ['gbm_st', 'f', 1e-13, 'rms pulse duration [s] (for intensity)'],
    ['gbm_mx', 'f', 0, 'transverse Gauss-Hermite mode order in horizontal direction'],
    ['gbm_my', 'f', 0, 'transverse Gauss-Hermite mode order in vertical direction'],
    ['gbm_ca', 's', 'c', 'treat _sigX, _sigY as sizes in [m] in coordinate representation (_presCA="c") or as angular divergences in [rad] in angular representation (_presCA="a")'],
    ['gbm_ft', 's', 't', 'treat _sigT as pulse duration in [s] in time domain/representation (_presFT="t") or as bandwidth in [eV] in frequency domain/representation (_presFT="f")'],

#---Calculation Types
# MOST OF THESE CAN BE IGNORED IF USING A SIMPLE GAUSSIAN - ONLY NEEDED FOR UNDULATOR SOURCE
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
    ['ss_ei', 'f', 30.0, 'initial photon energy [eV] for single-e spectrum vs photon energy calculation'],
    ['ss_ef', 'f', 700.0, 'final photon energy [eV] for single-e spectrum vs photon energy calculation'],
    ['ss_ne', 'i', 10000, 'number of points vs photon energy for single-e spectrum vs photon energy calculation'],
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
    ['sm_ei', 'f', 30.0, 'initial photon energy [eV] for multi-e spectrum vs photon energy calculation'],
    ['sm_ef', 'f', 700.0, 'final photon energy [eV] for multi-e spectrum vs photon energy calculation'],
    ['sm_ne', 'i', 10000, 'number of points vs photon energy for multi-e spectrum vs photon energy calculation'],
    ['sm_x', 'f', 0.0, 'horizontal center position [m] for multi-e spectrum vs photon energy calculation'],
    ['sm_rx', 'f', 0.001, 'range of horizontal position / horizontal aperture size [m] for multi-e spectrum vs photon energy calculation'],
    ['sm_nx', 'i', 1, 'number of points vs horizontal position for multi-e spectrum vs photon energy calculation'],
    ['sm_y', 'f', 0.0, 'vertical center position [m] for multi-e spectrum vs photon energy calculation'],
    ['sm_ry', 'f', 0.001, 'range of vertical position / vertical aperture size [m] for multi-e spectrum vs photon energy calculation'],
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
    ['pw_rx', 'f', 0.0025, 'range of horizontal position [m] for calculation of power density distribution vs horizontal and vertical position'],
    ['pw_nx', 'i', 400, 'number of points vs horizontal position for calculation of power density distribution'],
    ['pw_y', 'f', 0.0, 'central vertical position [m] for calculation of power density distribution vs horizontal and vertical position'],
    ['pw_ry', 'f', 0.00025, 'range of vertical position [m] for calculation of power density distribution vs horizontal and vertical position'],
    ['pw_ny', 'i', 400, 'number of points vs vertical position for calculation of power density distribution'],
    ['pw_pr', 'f', 1.0, 'precision factor for calculation of power density distribution'],
    ['pw_meth', 'i', 1, 'power density computation method (1- "near field", 2- "far field")'],
    ['pw_zst', 'f', 0., 'initial longitudinal position along electron trajectory of power density distribution (effective if pow_sst < pow_sfi)'],
    ['pw_zfi', 'f', 0., 'final longitudinal position along electron trajectory of power density distribution (effective if pow_sst < pow_sfi)'],
    ['pw_mag', 'i', 1, 'magnetic field to be used for power density calculation: 1- approximate, 2- accurate'],
    ['pw_fn', 's', 'res_pow.dat', 'file name for saving calculated power density distribution'],
    ['pw_pl', 's', '', 'plot the resulting power density distribution in a graph: ""- dont plot, "x"- vs horizontal position, "y"- vs vertical position, "xy"- vs horizontal and vertical position'],

    #Single-Electron Intensity distribution vs horizontal and vertical position
    ['si', '', '', 'calculate single-e intensity distribution (without wavefront propagation through a beamline) vs horizontal and vertical position', 'store_true'],
    #Single-Electron Wavefront Propagation
    ['ws', '', '', 'calculate single-electron (/ fully coherent) wavefront propagation', 'store_true'],
    #Multi-Electron (partially-coherent) Wavefront Propagation
    ['wm', '', '', 'calculate multi-electron (/ partially coherent) wavefront propagation', 'store_true'],


#--- Initial Wavefront Propagation Parameters
    ['w_e', 'f', 184.76, 'photon energy [eV] for calculation of intensity distribution vs horizontal and vertical position'],
    ['w_ef', 'f', -1.0, 'final photon energy [eV] for calculation of intensity distribution vs horizontal and vertical position'],
    ['w_ne', 'i', 1, 'number of points vs photon energy for calculation of intensity distribution'],
    ['w_x', 'f', 0.0, 'central horizontal position [m] for calculation of intensity distribution'],
    ['w_rx', 'f', 0.003, 'range of horizontal position [m] for calculation of intensity distribution'],
    ['w_nx', 'i', 1000, 'number of points vs horizontal position for calculation of intensity distribution'], # CHANGE INITIAL RESOLUTION HERE
    ['w_y', 'f', 0.0, 'central vertical position [m] for calculation of intensity distribution vs horizontal and vertical position'],
    ['w_ry', 'f', 0.003, 'range of vertical position [m] for calculation of intensity distribution vs horizontal and vertical position'],
    ['w_ny', 'i', 1000, 'number of points vs vertical position for calculation of intensity distribution'],   # CHANGE INITIAL RESOLUTION HERE
    ['w_smpf', 'f', 0, 'sampling factor for calculation of intensity distribution vs horizontal and vertical position'],
    ['w_meth', 'i', 2, 'method to use for calculation of intensity distribution vs horizontal and vertical position: 0- "manual", 1- "auto-undulator", 2- "auto-wiggler"'], # CHANGE TO AUTO-UNDULATOR IF USING UNDULATOR SOURCE
    ['w_prec', 'f', 0.01, 'relative precision for calculation of intensity distribution vs horizontal and vertical position'],
    ['w_u', 'i', 1, 'electric field units: 0- arbitrary, 1- sqrt(Phot/s/0.1%bw/mm^2), 2- sqrt(J/eV/mm^2) or sqrt(W/mm^2), depending on representation (freq. or time)'],
    ['si_pol', 'i', 6, 'polarization component to extract after calculation of intensity distribution: 0- Linear Horizontal, 1- Linear Vertical, 2- Linear 45 degrees, 3- Linear 135 degrees, 4- Circular Right, 5- Circular Left, 6- Total'],
    ['si_type', 'i', 0, 'type of a characteristic to be extracted after calculation of intensity distribution: 0- Single-Electron Intensity, 1- Multi-Electron Intensity, 2- Single-Electron Flux, 3- Multi-Electron Flux, 4- Single-Electron Radiation Phase, 5- Re(E): Real part of Single-Electron Electric Field, 6- Im(E): Imaginary part of Single-Electron Electric Field, 7- Single-Electron Intensity, integrated over Time or Photon Energy'],
    ['w_mag', 'i', 1, 'magnetic field to be used for calculation of intensity distribution vs horizontal and vertical position: 1- approximate, 2- accurate'],

    ['si_fn', 's', 'res_int_se.dat', 'file name for saving calculated single-e intensity distribution (without wavefront propagation through a beamline) vs horizontal and vertical position'],
    ['si_pl', 's', '', 'plot the input intensity distributions in graph(s): ""- dont plot, "x"- vs horizontal position, "y"- vs vertical position, "xy"- vs horizontal and vertical position'],
    ['ws_fni', 's', 'res_int_pr_se.dat', 'file name for saving propagated single-e intensity distribution vs horizontal and vertical position'],
    ['ws_pl', 's', '', 'plot the resulting intensity distributions in graph(s): ""- dont plot, "x"- vs horizontal position, "y"- vs vertical position, "xy"- vs horizontal and vertical position'],

#--- Multi Electron Propagation Parameters
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
    ['wm_fbk', '', '', 'create backup file(s) with propagated multi-e intensity distribution vs horizontal and vertical position and other radiation characteristics', 'store_true'],

    #to add options
    ['op_r', 'f', 3.0, 'longitudinal position of the first optical element [m]'], # 1st OPTICAL ELEMENT POSITION (CANNOT BE 0)
    
    # Former appParam:
    # CHANGE SOURCE TYPE HERE (MAY NOT BE NECESSARY) - USE IDEALISED UNDULATOR (u) FOR UNDULATOR SOURCE
    ['rs_type', 's', 'g', 'source type, (u) idealized undulator, (t), tabulated undulator, (m) multipole, (g) gaussian beam'],

#---Beamline optics:
#---CHANGE THESE PROPERTIES FOR TESTS
    # zero_drift: drift
    ['op_zero_drift_L', 'f', 0, 'length'],   # INITIAL DRIFT AFTER 1st OPTICAL ELEMENT POSITION (CAN BE 0)

    # Mask_Aperture: aperture
    ['op_Mask_Aperture_shape', 's', 'r', 'shape'], # CHANGE 'r' TO 'c' FOR CIRCULAR APERTURE
    ['op_Mask_Aperture_Dx', 'f', 10e-6, 'horizontalSize'],
    ['op_Mask_Aperture_Dy', 'f', 10e-6, 'verticalSize'],
    ['op_Mask_Aperture_x', 'f', 0.0, 'horizontalOffset'],
    ['op_Mask_Aperture_y', 'f', 0.0, 'verticalOffset'],

    # Obstacle: obstacle
    ['op_Obstacle_shape', 's', 'r', 'shape'],
    ['op_Obstacle_Dx', 'f', 20e-6, 'horizontalSize'],
    ['op_Obstacle_Dy', 'f', 33.75e-6, 'verticalSize'],
    ['op_Obstacle_x', 'f', 0.0, 'horizontalOffset'],
    ['op_Obstacle_y', 'f', -10e-6, 'verticalOffset'],    #-10e-6
    
    # maskObstacle: Photon Block Layer [
    ['op_maskObstacle_file_path', 's', '/opt/xl/xl/experiments/maskEfficiency/masks/vert_block.tif', 'imageFile'], # MAKE SURE FILE PATH IS CORRECT
    ['op_maskObstacle_outputImageFormat', 's', 'tif', 'outputImageFormat'],
    ['op_maskObstacle_position', 'f', 3.0, 'position'],                        # ABSOLUTE POSITION ALONG BEAMLINE
    ['op_maskObstacle_resolution', 'f', 2.5e-08, 'resolution'],                # CHECK PIXEL SIZE OF TIFF VS MASK SIZE TO GET RESOLUTION
    ['op_maskObstacle_thick', 'f', 200e-9, 'thickness'],                       # PHOTON BLOCK LAYER THICKNESS
    ['op_maskObstacle_delta', 'f', 0.0135615645, 'refractiveIndex'],           # REFRACTIVE INDEX OF PHOTON BLOCK MATERIAL
    ['op_maskObstacle_atten_len', 'f', 2.753364e-8, 'attenuationLength'],      # ATTENUATION LENGTH
    ['op_maskObstacle_horizontalCenterCoordinate', 'f', 0.0, 'horizontalCenterCoordinate'],
    ['op_maskObstacle_verticalCenterCoordinate', 'f', 0.0, 'verticalCenterCoordinate'],
    ['op_maskObstacle_rotateAngle', 'f', 0.0, 'rotateAngle'],
    ['op_maskObstacle_cutoffBackgroundNoise', 'f', 0.001, 'cutoffBackgroundNoise'],
    ['op_maskObstacle_cropArea', 'i', 0, 'cropArea'],
    ['op_maskObstacle_extTransm', 'i', 0, 'transmissionImage'], 
    ['op_maskObstacle_areaXStart', 'i', 0, 'areaXStart'],
    ['op_maskObstacle_areaXEnd', 'i', 1408, 'areaXEnd'],                       # NUMBER OF PIXELS IN TIFF FILE (HORIZONTAL)
    ['op_maskObstacle_areaYStart', 'i', 0, 'areaYStart'],
    ['op_maskObstacle_areaYEnd', 'i', 1408, 'areaYEnd'],                       # NUMBER OF PIXELS IN TIFF FILE (VERTICAL)
    ['op_maskObstacle_rotateReshape', 'i', 0, 'rotateReshape'],
    ['op_maskObstacle_backgroundColor', 'i', 0, 'backgroundColor'],
    ['op_maskObstacle_tileImage', 'i', 0, 'tileImage'],
    ['op_maskObstacle_tileRows', 'i', 1, 'tileRows'],
    ['op_maskObstacle_tileColumns', 'i', 1, 'tileColumns'],
    ['op_maskObstacle_shiftX', 'i', 0, 'shiftX'],
    ['op_maskObstacle_shiftY', 'i', 0, 'shiftY'],
    ['op_maskObstacle_invert', 'i', 1, 'invert'],                              # INVERT BLACK/WHITE (BLACK = EMPTY SPACE, WHITE = SOLID SURFACE)
    
    
    #maskSubstrate: Si02
    ['op_maskSubstrate_file_path', 's', '/opt/xl/xl/experiments/maskEfficiency/masks/vert_substrate.tif', 'imageFile'], # MAKE SURE FILE PATH IS CORRECT
    ['op_maskSubstrate_outputImageFormat', 's', 'tif', 'outputImageFormat'],
    ['op_maskSubstrate_position', 'f', 3.0, 'position'],                       # ABSOLUTE POSITION ALONG BEAMLINE
    ['op_maskSubstrate_resolution', 'f', 2.5e-08, 'resolution'],               # CHECK PIXEL SIZE OF TIFF VS MASK SIZE TO GET RESOLUTION
    ['op_maskSubstrate_thick', 'f', 40e-9, 'thickness'],                       # SUBSTRATE LAYER THICKNESS
    ['op_maskSubstrate_delta', 'f', 0.0940100942, 'refractiveIndex'],          # REFRACTIVE INDEX OF SUBSTRATE MATERIAL
    ['op_maskSubstrate_atten_len', 'f', 0.100688e-06, 'attenuationLength'],    # ATTENUATION LENGTH
    ['op_maskSubstrate_horizontalCenterCoordinate', 'f', 0.0, 'horizontalCenterCoordinate'],
    ['op_maskSubstrate_verticalCenterCoordinate', 'f', 0.0, 'verticalCenterCoordinate'],
    ['op_maskSubstrate_rotateAngle', 'f', 0.0, 'rotateAngle'],
    ['op_maskSubstrate_cutoffBackgroundNoise', 'f', 0.001, 'cutoffBackgroundNoise'],
    ['op_maskSubstrate_cropArea', 'i', 0, 'cropArea'],
    ['op_maskSubstrate_extTransm', 'i', 0, 'transmissionImage'], 
    ['op_maskSubstrate_areaXStart', 'i', 0, 'areaXStart'],
    ['op_maskSubstrate_areaXEnd', 'i', 1408, 'areaXEnd'],                      # NUMBER OF PIXELS IN TIFF FILE (HORIZONTAL)
    ['op_maskSubstrate_areaYStart', 'i', 0, 'areaYStart'],
    ['op_maskSubstrate_areaYEnd', 'i', 1408, 'areaYEnd'],                      # NUMBER OF PIXELS IN TIFF FILE (VERTICAL)
    ['op_maskSubstrate_rotateReshape', 'i', 0, 'rotateReshape'],
    ['op_maskSubstrate_backgroundColor', 'i', 0, 'backgroundColor'],
    ['op_maskSubstrate_tileImage', 'i', 0, 'tileImage'],
    ['op_maskSubstrate_tileRows', 'i', 1, 'tileRows'],
    ['op_maskSubstrate_tileColumns', 'i', 1, 'tileColumns'],
    ['op_maskSubstrate_shiftX', 'i', 0, 'shiftX'],
    ['op_maskSubstrate_shiftY', 'i', 0, 'shiftY'],
    ['op_maskSubstrate_invert', 'i', 1, 'invert'],                             # INVERT BLACK/WHITE (BLACK = EMPTY SPACE, WHITE = SOLID SURFACE)


     # Mask: sample [values for Si3N4]
    ['op_Mask_file_path', 's', '/opt/xl/xl/experiments/maskEfficiency/masks/testGrating_1-2.tif', 'imageFile'], # MAKE SURE FILE PATH IS CORRECT
    ['op_Mask_outputImageFormat', 's', 'tif', 'outputImageFormat'],
    ['op_Mask_position', 'f', 3.0, 'position'],                               # ABSOLUTE POSITION ALONG BEAMLINE
    ['op_Mask_resolution', 'f', 6.25e-09, 'resolution'],                        # CHECK PIXEL SIZE OF TIFF VS MASK SIZE TO GET RESOLUTION
    ['op_Mask_thick', 'f', 500e-9, 'thickness'],                                # ABSORBER LAYER THICKNESS
    ['op_Mask_delta', 'f', 0.020682307, 'refractiveIndex'],                    # REFRACTIVE INDEX OF ABSORBER MATERIAL
    ['op_Mask_atten_len', 'f', 3.265140e-08, 'attenuationLength'],             # ATTENUATION LENGTH
    ['op_Mask_horizontalCenterCoordinate', 'f', 0.0, 'horizontalCenterCoordinate'],
    ['op_Mask_verticalCenterCoordinate', 'f', 0.0, 'verticalCenterCoordinate'],
    ['op_Mask_rotateAngle', 'f', 0.0, 'rotateAngle'],
    ['op_Mask_cutoffBackgroundNoise', 'f', 0.001, 'cutoffBackgroundNoise'],
    ['op_Mask_cropArea', 'i', 0, 'cropArea'],
    ['op_Mask_extTransm', 'i', 0, 'transmissionImage'], 
    ['op_Mask_areaXStart', 'i', 0, 'areaXStart'],
    ['op_Mask_areaXEnd', 'i', 1600, 'areaXEnd'],                               # NUMBER OF PIXELS IN TIFF FILE (HORIZONTAL)
    ['op_Mask_areaYStart', 'i', 0, 'areaYStart'],
    ['op_Mask_areaYEnd', 'i', 1600, 'areaYEnd'],                               # NUMBER OF PIXELS IN TIFF FILE (VERTICAL)
    ['op_Mask_rotateReshape', 'i', 0, 'rotateReshape'],
    ['op_Mask_backgroundColor', 'i', 0, 'backgroundColor'],
    ['op_Mask_tileImage', 'i', 0, 'tileImage'],
    ['op_Mask_tileRows', 'i', 1, 'tileRows'],
    ['op_Mask_tileColumns', 'i', 1, 'tileColumns'],
    ['op_Mask_shiftX', 'i', 0, 'shiftX'],
    ['op_Mask_shiftY', 'i', 0, 'shiftY'],
    ['op_Mask_invert', 'i', 1, 'invert'],                                      # INVERT BLACK/WHITE (BLACK = EMPTY SPACE, WHITE = SOLID SURFACE)
    
    # Farfield_Propagation: drift
    # (For double slit with preset geometry, farfield propagation is 1m) 
    # (For binary grating mask with dimensions given in Jerome's honours thesis, theoretical image plane distance is 176.56 microns)
    ['op_Farfield_Propagation_L', 'f', 0.003, 'length'], # PROPAGATION DISTANCE AFTER MASK - 

#---Propagation parameters - - - -CHANGE THESE TO ALTER RESOLUTION (Rx,Ry) AND SAMPLE RANGE (Sx,Sy)
# R=1 means no change, R>1 increases resolution (more pixels), R<1 decreases resolution (less pixels)
# S=1 means no change, S>1 increases sampled area, S<1 decreases sampled area
# Make sure to change resolution appropriately if changing range as increasing range will increase number of pixels
#                                                              Sx,  Rx,  Sy,  Ry
    ['op_zero_drift_pp', 'f',                [0, 0, 1.0, 0, 0, 0.25, 4.0, 0.25, 4.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'zero_drift'],
    ['op_Mask_Aperture_pp', 'f',             [0, 0, 1.0, 0, 0, 0.125, 100.0, 0.125, 100.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'Mask_Aperture'],
   # ['op_Obstacle_pp', 'f',                  [0, 0, 1.0, 0, 0, 0.125, 50.0, 0.125, 50.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'Obstacle'], # current res at obstacle = 375x375 nm
    ['op_maskObstacle_pp', 'f',              [0, 0, 1.0, 0, 0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'maskObstacle'],
    ['op_maskSubstrate_pp', 'f',             [0, 0, 1.0, 0, 0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'Substrate'],    
    ['op_Mask_pp', 'f',                      [0, 0, 1.0, 0, 0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'Mask'],
    ['op_Farfield_Propagation_pp', 'f',      [0, 0, 1.0, 1, 0, 2.0, 0.5, 2.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'Farfield_Propagation'],
    ['op_fin_pp', 'f',                       [0, 0, 1.0, 0, 0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'final post-propagation (resize) parameters'],



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
])
    
        


    
options = [              
    # # Option to save wavefield after each element for inspection (0 - Don't save, 1 - Save)
    # ['op_zero_drift_cache', 'f',                                               0, 'Cache wavefront after zero_drift'],
    # ['op_Mask_Aperture_cache', 'f',                                            0, 'Cache wavefront after Mask Aperture'],
    # ['op_Obstacle_cache', 'f',                                                 0, 'Cache wavefront after Obstacle'],
    # ['op_maskObstacle_cache', 'f',                                             0, 'Cache wavefront after maskObstacle'],
    # ['op_maskSubstrate_cache', 'f',                                            0, 'Cache wavefront after maskSubstrate'],
    # ['op_Mask_cache', 'f',                                                     0, 'Cache wavefront after Mask'],
    # ['op_Far_Field_cache', 'f',                                                0, 'Cache wavefront after Far_Field'],

    #list copied from above
    ['opList','s', opNames, 'List of names of optical elements'],

    # Specify source type (use g)
    # override source type, optionally using a new option 'r' (you probably won't want to do this for first run...)
    ['rs_type', 's', 'g', 'source type, (u) idealized undulator, \
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
