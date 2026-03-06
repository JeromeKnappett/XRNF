#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 19:19:49 2021

@author: gvanriessen
"""
import srwl_bl as srwl_bl


opNames = [ # COMMENT OUT ANY UNNECESSARY OPTICAL ELEMENTS
            'WBS',
            'After_WBS_Before_Toroidal_Mirror',
            'Toroidal_Mirror',
            'After_Toroidal_Mirror_Before_PGM', 
            'Planar_Mirror', 
            'Planar_Mirror_Grating', 
            'Grating', 
            'Grating_Before_Exit_Aperture', 
            'Exit_Aperture', 
            'After_Exit_Aperture_Before_Cylindrical_Mirror', 
            'Cylindrical_Mirror', 
            'After_Cylindrical_Mirror_Before_Exit_Slit', 
            'Exit_Slits', 
            #'Exit_Slits_Drift',
            #'Exit_Slits_Cleanup', 
            'After_Exit_Slit_Before_BDA',
            'FZP_Aperture',
            'FZP',
            'BDA_Mask_Aperture',
            'BDA',
            'maskObstacle',
######            'maskSubstrate',
            'Mask'  ,
            'Drift_Mask_To_AerialImage'
             ]



varParam = srwl_bl.srwl_uti_ext_options([
    ['name', 's', 'blBeamCoherence2', 'simulation name'],

#---Data Folder
    ['fdir', 's', '', 'folder (directory) name for reading-in input and saving output data files'],

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
    ['ebm_dr', 'f', -1.54, 'electron beam longitudinal drift [m] to be performed before a required calculation'],
    ['ebm_ens', 'f', 0.001021, 'electron beam relative energy spread'],
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
    ['und_bx', 'f', 0.0, 'undulator horizontal peak magnetic field [T]'],
    ['und_by', 'f', 0.46111878, 'undulator vertical peak magnetic field [T]'],
    ['und_phx', 'f', 0.0, 'initial phase of the horizontal magnetic field [rad]'],
    ['und_phy', 'f', 0.0, 'initial phase of the vertical magnetic field [rad]'],
    ['und_b2e', '', '', 'estimate undulator fundamental photon energy (in [eV]) for the amplitude of sinusoidal magnetic field defined by und_b or und_bx, und_by', 'store_true'],
    ['und_e2b', '', '', 'estimate undulator field amplitude (in [T]) for the photon energy defined by w_e', 'store_true'],
    ['und_per', 'f', 0.075, 'undulator period [m]'],
    ['und_len', 'f', 1.875, 'undulator length [m]'],
    ['und_zc', 'f', 0.0, 'undulator center longitudinal position [m]'],
    ['und_sx', 'i', 1, 'undulator horizontal magnetic field symmetry vs longitudinal position'],
    ['und_sy', 'i', 1, 'undulator vertical magnetic field symmetry vs longitudinal position'],
    ['und_g', 'f', 6.72, 'undulator gap [mm] (assumes availability of magnetic measurement or simulation data)'],
    ['und_ph', 'f', 0.0, 'shift of magnet arrays [mm] for which the field should be set up'],
    ['und_mdir', 's', '', 'name of magnetic measurements sub-folder'],
    ['und_mfs', 's', '', 'name of magnetic measurements for different gaps summary file'],



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
    ['ss_ef', 'f', 1000.0, 'final photon energy [eV] for single-e spectrum vs photon energy calculation'],
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
    ['sm_ei', 'f', 0.0, 'initial photon energy [eV] for multi-e spectrum vs photon energy calculation'],
    ['sm_ef', 'f', 1000.0, 'final photon energy [eV] for multi-e spectrum vs photon energy calculation'],
    ['sm_ne', 'i', 10000, 'number of points vs photon energy for multi-e spectrum vs photon energy calculation'],
    ['sm_x', 'f', 0.0, 'horizontal center position [m] for multi-e spectrum vs photon energy calculation'],
    ['sm_rx', 'f', 1e-05, 'range of horizontal position / horizontal aperture size [m] for multi-e spectrum vs photon energy calculation'],
    ['sm_nx', 'i', 1, 'number of points vs horizontal position for multi-e spectrum vs photon energy calculation'],
    ['sm_y', 'f', 0.0, 'vertical center position [m] for multi-e spectrum vs photon energy calculation'],
    ['sm_ry', 'f', 1e-05, 'range of vertical position / vertical aperture size [m] for multi-e spectrum vs photon energy calculation'],
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
    ['si', '', '', 'calculate single-e intensity distribution (without wavefront propagation through a beamline) vs horizontal and vertical position', 'store_true'],
    #Single-Electron Wavefront Propagation
    ['ws', '', '', 'calculate single-electron (/ fully coherent) wavefront propagation', 'store_true'],
    #Multi-Electron (partially-coherent) Wavefront Propagation
    ['wm', '', '1', 'calculate multi-electron (/ partially coherent) wavefront propagation', 'store_true'],

#--- Initial Wavefront Propagation Parameters
    ['w_e', 'f', 184.76, 'photon energy [eV] for calculation of intensity distribution vs horizontal and vertical position'],
    ['w_ef', 'f', -1.0, 'final photon energy [eV] for calculation of intensity distribution vs horizontal and vertical position'],
    ['w_ne', 'i', 1, 'number of points vs photon energy for calculation of intensity distribution'],
    ['w_x', 'f', 0.0, 'central horizontal position [m] for calculation of intensity distribution'],
    ['w_rx', 'f', 0.006, 'range of horizontal position [m] for calculation of intensity distribution'],
    ['w_nx', 'i', 600, 'number of points vs horizontal position for calculation of intensity distribution'],
    ['w_y', 'f', 0.0, 'central vertical position [m] for calculation of intensity distribution vs horizontal and vertical position'],
    ['w_ry', 'f', 0.006, 'range of vertical position [m] for calculation of intensity distribution vs horizontal and vertical position'],
    ['w_ny', 'i', 600, 'number of points vs vertical position for calculation of intensity distribution'],
    ['w_smpf', 'f', 0, 'sampling factor for calculation of intensity distribution vs horizontal and vertical position'],
    ['w_meth', 'i', 1, 'method to use for calculation of intensity distribution vs horizontal and vertical position: 0- "manual", 1- "auto-undulator", 2- "auto-wiggler"'],
    ['w_prec', 'f', 0.01, 'relative precision for calculation of intensity distribution vs horizontal and vertical position'],
    ['w_u', 'i', 1, 'electric field units: 0- arbitrary, 1- sqrt(Phot/s/0.1%bw/mm^2), 2- sqrt(J/eV/mm^2) or sqrt(W/mm^2), depending on representation (freq. or time)'],
    ['si_pol', 'i', 6, 'polarization component to extract after calculation of intensity distribution: 0- Linear Horizontal, 1- Linear Vertical, 2- Linear 45 degrees, 3- Linear 135 degrees, 4- Circular Right, 5- Circular Left, 6- Total'],
    #### PUT 1 FOR MULTI-ELECTRON, 0 FOR SINGLE ####
    ['si_type', 'i', 1, 'type of a characteristic to be extracted after calculation of intensity distribution: 0- Single-Electron Intensity, 1- Multi-Electron Intensity, 2- Single-Electron Flux, 3- Multi-Electron Flux, 4- Single-Electron Radiation Phase, 5- Re(E): Real part of Single-Electron Electric Field, 6- Im(E): Imaginary part of Single-Electron Electric Field, 7- Single-Electron Intensity, integrated over Time or Photon Energy'],
    ['w_mag', 'i', 1, 'magnetic field to be used for calculation of intensity distribution vs horizontal and vertical position: 1- approximate, 2- accurate'],

    #['si_fn', 's', 'res_int_se.dat', 'file name for saving calculated single-e intensity distribution (without wavefront propagation through a beamline) vs horizontal and vertical position'],
    #['si_pl', 's', '', 'plot the input intensity distributions in graph(s): ""- dont plot, "x"- vs horizontal position, "y"- vs vertical position, "xy"- vs horizontal and vertical position'],
#    ['ws_fni', 's', 'res_int_pr_se.dat', 'file name for saving propagated single-e intensity distribution vs horizontal and vertical position'],
    #['ws_pl', 's', '', 'plot the resulting intensity distributions in graph(s): ""- dont plot, "x"- vs horizontal position, "y"- vs vertical position, "xy"- vs horizontal and vertical position'],
    ['si_fn', 's', '', 'file name for saving calculated single-e intensity distribution (without wavefront propagation through a beamline) vs horizontal and vertical position'],
    ['si_pl', 's', '', 'plot the input intensity distributions in graph(s): ""- dont plot, "x"- vs horizontal position, "y"- vs vertical position, "xy"- vs horizontal and vertical position'],
    ['ws_fni', 's', '', 'file name for saving propagated single-e intensity distribution vs horizontal and vertical position'],
    ['ws_pl', 's', '', 'plot the resulting intensity distributions in graph(s): ""- dont plot, "x"- vs horizontal position, "y"- vs vertical position, "xy"- vs horizontal and vertical position'],



    ['wm_nm', 'i', 1000, 'number of macro-electrons (coherent wavefronts) for calculation of multi-electron wavefront propagation'],
    ['wm_na', 'i', 5, 'number of macro-electrons (coherent wavefronts) to average on each node for parallel (MPI-based) calculation of multi-electron wavefront propagation'],
    ['wm_ns', 'i', 5, 'saving periodicity (in terms of macro-electrons / coherent wavefronts) for intermediate intensity at multi-electron wavefront propagation calculation'],
    #### PUT "20" BELLOW TO EXTRACT MULTI-ELECTRON ELECTRIC FIELD ####
    ['wm_ch', 'i', 0, 'type of a characteristic to be extracted after calculation of multi-electron wavefront propagation: #0- intensity (s0); 1- four Stokes components; 2- mutual intensity cut vs x; 3- mutual intensity cut vs y; 40- intensity(s0), mutual intensity cuts and degree of coherence vs X & Y'],
    ['wm_ap', 'i', 0, 'switch specifying representation of the resulting Stokes parameters: coordinate (0) or angular (1)'],
    ['wm_x0', 'f', 0, 'horizontal center position for mutual intensity cut calculation'],
    ['wm_y0', 'f', 0, 'vertical center position for mutual intensity cut calculation'],
    ['wm_ei', 'i', 0, 'integration over photon energy is required (1) or not (0); if the integration is required, the limits are taken from w_e, w_ef'],
    ['wm_rm', 'i', 1, 'method for generation of pseudo-random numbers for e-beam phase-space integration: 1- standard pseudo-random number generator, 2- Halton sequences, 3- LPtau sequences (to be implemented)'],
    ['wm_am', 'i', 0, 'multi-electron integration approximation method: 0- no approximation (use the standard 5D integration method), 1- integrate numerically only over e-beam energy spread and use convolution to treat transverse emittance'],
    ['wm_fni', 's', 'res_int_pr_me.dat', 'file name for saving propagated multi-e intensity distribution vs horizontal and vertical position'],

    ['stokes_fname','s','stokes',''],
    ['res_ipm','','','container for results of multi-electron wavefront propagation.'],


    #to add options
    ['op_r', 'f', 14.3, 'longitudinal position of the first optical element [m]'],

    # Former appParam:
    ['rs_type', 's', 'u', 'source type, (u) idealized undulator, (t), tabulated undulator, (m) multipole, (g) gaussian beam'],

#---Beamline optics:
    # WBS: aperture
    ['op_WBS_shape', 's', 'r', 'shape'],
    ['op_WBS_Dx', 'f', 0.004, 'horizontalSize'],
    ['op_WBS_Dy', 'f', 0.003, 'verticalSize'],
    ['op_WBS_x', 'f', 0.0, 'horizontalOffset'],
    ['op_WBS_y', 'f', 0.0, 'verticalOffset'],

    # After_WBS_Before_Toroidal_Mirror: drift
    ['op_After_WBS_Before_Toroidal_Mirror_L', 'f', 0.82, 'length'],

    # Toroidal_Mirror: toroidalMirror
    ['op_Toroidal_Mirror_hfn', 's', '', 'heightProfileFile'],
    ['op_Toroidal_Mirror_dim', 's', 'x', 'orientation'],
    ['op_Toroidal_Mirror_ap_shape', 's', 'r', 'apertureShape'],
    ['op_Toroidal_Mirror_rt', 'f', 6669.6, 'tangentialRadius'],
    ['op_Toroidal_Mirror_rs', 'f', 5.2619, 'sagittalRadius'],
    ['op_Toroidal_Mirror_size_tang', 'f', 0.42, 'tangentialSize'],
    ['op_Toroidal_Mirror_size_sag', 'f', 0.3, 'sagittalSize'],
    ['op_Toroidal_Mirror_ang', 'f', 0.0174533, 'grazingAngle'],
    ['op_Toroidal_Mirror_horizontalPosition', 'f', 0.0, 'horizontalPosition'],
    ['op_Toroidal_Mirror_verticalPosition', 'f', 0.0, 'verticalPosition'],
    ['op_Toroidal_Mirror_nvx', 'f', -0.999847695026, 'normalVectorX'],
    ['op_Toroidal_Mirror_nvy', 'f', 0.0, 'normalVectorY'],
    ['op_Toroidal_Mirror_nvz', 'f', 0.0174524139162, 'normalVectorZ'],
    ['op_Toroidal_Mirror_tvx', 'f', -0.0174524139162, 'tangentialVectorX'],
    ['op_Toroidal_Mirror_tvy', 'f', 0.0, 'tangentialVectorY'],
    ['op_Toroidal_Mirror_amp_coef', 'f', 0.0, 'heightAmplification'],

    # After_Toroidal_Mirror_Before_PGM: drift
    ['op_After_Toroidal_Mirror_Before_PGM_L', 'f', 3.38, 'length'],

    # Planar_Mirror: mirror
    ['op_Planar_Mirror_hfn', '','/user/home/opt/xl/xl/experiments/beamCoherence2/mirror_1d.dat', 'heightProfileFile'],
    ['op_Planar_Mirror_dim', 's', 'y', 'orientation'],
    ['op_Planar_Mirror_ang', 'f', 0.0349066, 'grazingAngle'],
    ['op_Planar_Mirror_amp_coef', 'f', 0, 'heightAmplification'],
    ['op_Planar_Mirror_size_x', 'f', 0.46, 'horizontalTransverseSize'],
    ['op_Planar_Mirror_size_y', 'f', 0.05, 'verticalTransverseSize'],

    # Planar_Mirror_Grating: drift
    ['op_Planar_Mirror_Grating_L', 'f', 0.2, 'length'],

    # Grating: grating
    ['op_Grating_size_tang', 'f', 0.15, 'tangentialSize'],
    ['op_Grating_size_sag', 'f', 0.02, 'sagittalSize'],
    ['op_Grating_nvx', 'f', 0.0, 'normalVectorX'],
    ['op_Grating_nvy', 'f', 0.9997905128, 'normalVectorY'],
    ['op_Grating_nvz', 'f', -0.0204677921334, 'normalVectorZ'],
    ['op_Grating_tvx', 'f', 0.0, 'tangentialVectorX'],
    ['op_Grating_tvy', 'f', 0.0204677921334, 'tangentialVectorY'],
    ['op_Grating_x', 'f', 0.0, 'horizontalOffset'],
    ['op_Grating_y', 'f', 0.0, 'verticalOffset'],
    ['op_Grating_m', 'f', 1.0, 'diffractionOrder'],
    ['op_Grating_grDen', 'f', 250.0, 'grooveDensity0'],
    ['op_Grating_grDen1', 'f', 0.0, 'grooveDensity1'],
    ['op_Grating_grDen2', 'f', 0.0, 'grooveDensity2'],
    ['op_Grating_grDen3', 'f', 0.0, 'grooveDensity3'],
    ['op_Grating_grDen4', 'f', 0.0, 'grooveDensity4'],

    # Grating_Before_Exit_Aperture: drift
    ['op_Grating_Before_Exit_Aperture_L', 'f', 1.0, 'length'],

    # Exit_Aperture: aperture
    ['op_Exit_Aperture_shape', 's', 'r', 'shape'],
    #['op_Exit_Aperture_Dx', 'f', 0.004, 'horizontalSize'],  GVR
    #['op_Exit_Aperture_Dy', 'f', 8e-05, 'verticalSize'],
    ['op_Exit_Aperture_Dx', 'f', 10.0e-3, 'horizontalSize'], #REDUCED zzzzz
    ['op_Exit_Aperture_Dy', 'f', 20.0e-3, 'verticalSize'],
    ['op_Exit_Aperture_x', 'f', 0.0, 'horizontalOffset'],
    ['op_Exit_Aperture_y', 'f', 0.0, 'verticalOffset'],

    # After_Mask_Aperture_Before_Cylindrical_Mirror: drift
    ['op_After_Exit_Aperture_Before_Cylindrical_Mirror_L', 'f', 0.6, 'length'],

    # Cylindrical_Mirror: toroidalMirror
    ['op_Cylindrical_Mirror_hfn', 's', '', 'heightProfileFile'],
    ['op_Cylindrical_Mirror_dim', 's', 'x', 'orientation'],
    ['op_Cylindrical_Mirror_ap_shape', 's', 'r', 'apertureShape'],
    ['op_Cylindrical_Mirror_rt', 'f', 1000000000000, 'tangentialRadius'],  # was 10,000
    ['op_Cylindrical_Mirror_rs', 'f', 0.24433, 'sagittalRadius'],  # was -.24
    ['op_Cylindrical_Mirror_size_tang', 'f', 0.24, 'tangentialSize'],  #was 0.24
    ['op_Cylindrical_Mirror_size_sag', 'f', 0.04, 'sagittalSize'],  # was 0.04
    ['op_Cylindrical_Mirror_ang', 'f', 0.0261769095412, 'grazingAngle'],  # was 0.0174533
    ['op_Cylindrical_Mirror_horizontalPosition', 'f', 0.0, 'horizontalPosition'],
    ['op_Cylindrical_Mirror_verticalPosition', 'f', 0.0, 'verticalPosition'],
    ['op_Cylindrical_Mirror_nvx', 'f', 0.999657325991, 'normalVectorX'], #was 0.999848623819
    ['op_Cylindrical_Mirror_nvy', 'f', 0.0, 'normalVectorY'],
    ['op_Cylindrical_Mirror_nvz', 'f', -0.0261769095412, 'normalVectorZ'],#was -0.0173991220093
    ['op_Cylindrical_Mirror_tvx', 'f', 0.0261769095412, 'tangentialVectorX'],#was 0.0173991220093
    ['op_Cylindrical_Mirror_tvy', 'f', 0.0, 'tangentialVectorY'],
    ['op_Cylindrical_Mirror_amp_coef', 'f', 0.0, 'heightAmplification'],
    
    # Circular_Cylinder: sphericalMirror
    ['op_Circular_Cylinder_hfn', 's', '', 'heightProfileFile'],
    ['op_Circular_Cylinder_dim', 's', 'x', 'orientation'],
    ['op_Circular_Cylinder_r', 'f', 0.24433, 'radius'],
    ['op_Circular_Cylinder_size_tang', 'f', 0.24, 'tangentialSize'], #was 0.24
    ['op_Circular_Cylinder_size_sag', 'f', 0.04, 'sagittalSize'],    #was 0.04
    ['op_Circular_Cylinder_ang', 'f', 0.034906599999999996, 'grazingAngle'], #was  0.034906599999999996
    ['op_Circular_Cylinder_nvx', 'f', 0.9993908264969952, 'normalVectorX'], #was 0.9993908264969952
    ['op_Circular_Cylinder_nvy', 'f', 0.0, 'normalVectorY'],
    ['op_Circular_Cylinder_nvz', 'f', -0.034899511653501074, 'normalVectorZ'], #was -0.034899511653501074
    ['op_Circular_Cylinder_tvx', 'f', 0.034899511653501074, 'tangentialVectorX'],#was 0.034899511653501074
    ['op_Circular_Cylinder_tvy', 'f', 0.0, 'tangentialVectorY'],
    ['op_Circular_Cylinder_amp_coef', 'f', 0.0, 'heightAmplification'],
    ['op_Circular_Cylinder_x', 'f', 0.0, 'horizontalOffset'],
    ['op_Circular_Cylinder_y', 'f', 0.0, 'verticalOffset'],

    # After_Cylindrical_Mirror_Before_Exit_Slit: drift
    ['op_After_Cylindrical_Mirror_Before_Exit_Slit_L', 'f', 7.0, 'length'],

    # Exit_Slits: aperture
    ['op_Exit_Slits_shape', 's', 'r', 'shape'],
    ['op_Exit_Slits_Dx', 'f', 200e-6, 'horizontalSize'],
    ['op_Exit_Slits_Dy', 'f', 200e-6, 'verticalSize'],
    ['op_Exit_Slits_x', 'f', 0.0, 'horizontalOffset'],
    ['op_Exit_Slits_y', 'f', 0.0, 'verticalOffset'],
    
    # Grating_Before_Exit_Aperture: drift
    ['op_Exit_Slits_Drift_L', 'f', 0.01, 'length'],
    
    # Exit_Slits_Cleanup: aperture
    ['op_Exit_Slits_Cleanup_shape', 's', 'r', 'shape'],
    ['op_Exit_Slits_Cleanup_Dx', 'f', 200e-6, 'horizontalSize'],
    ['op_Exit_Slits_Cleanup_Dy', 'f', 250e-6, 'verticalSize'],
    ['op_Exit_Slits_Cleanup_x', 'f', 0.0, 'horizontalOffset'],
    ['op_Exit_Slits_Cleanup_y', 'f', 0.0, 'verticalOffset'],

    # After_Exit_Slit_Before_BDA: drift
    ['op_After_Exit_Slit_Before_BDA_L', 'f', 9.5, 'length'],
    
    # FZP_Aperture: aperture
    ['op_FZP_Aperture_shape', 'c', 'r', 'shape'],
    ['op_FZP_Aperture_Dx', 'f', 50e-06, 'horizontalSize'],
    ['op_FZP_Aperture_Dy', 'f', 50e-06, 'verticalSize'],
    ['op_FZP_Aperture_x', 'f', 0.0, 'horizontalOffset'],
    ['op_FZP_Aperture_y', 'f', 0.0, 'verticalOffset'],
    
    # FZP: lens
    ['op_FZP_Fx', 'f', 1.0888e-3, 'horizontalFocalLength'],
    ['op_FZP_Fy', 'f', 1.0888e-3, 'verticalFocalLength'],
    ['op_FZP_x', 'f', 0.0, 'horizontalOffset'],
    ['op_FZP_y', 'f', 0.0, 'verticalOffset'],

    # BDA_Mask_Aperture: drift
    ['op_BDA_Mask_Aperture_L', 'f', 0.00021776, 'length'],
    
    # BDA: aperture
    ['op_BDA_shape', 's', 'r', 'shape'],
    #['op_BDA_Dx', 'f', 0.004, 'horizontalSize'], GVRzz
    #['op_BDA_Dy', 'f', 0.0006, 'verticalSize'],
    ['op_BDA_Dx', 'f', 40e-6, 'horizontalSize'],
    ['op_BDA_Dy', 'f', 40e-6, 'verticalSize'],
    ['op_BDA_x', 'f', 0.0, 'horizontalOffset'],
    ['op_BDA_y', 'f', 0.0, 'verticalOffset'],


    # # Mask_Aperture: aperture
    # ['op_Mask_Aperture_shape', 's', 'r', 'shape'],
    # ['op_Mask_Aperture_Dx', 'f', 1e-05, 'horizontalSize'],
    # ['op_Mask_Aperture_Dy', 'f', 4e-05, 'verticalSize'],
    # ['op_Mask_Aperture_x', 'f', 0.0, 'horizontalOffset'],
    # ['op_Mask_Aperture_y', 'f', 0.0, 'verticalOffset'],

 
     # maskObstacle: obstacle [Tantillum?]
    ['op_maskObstacle_file_path', 's', '/user/home/opt/xl/xl/experiments/masks/vert_block.tif', 'imageFile'], #mask1IN
    ['op_maskObstacle_outputImageFormat', 's', 'tif', 'outputImageFormat'],
    ['op_maskObstacle_position', 'f', 37.0, 'position'],
    ['op_maskObstacle_resolution', 'f', 2.5e-09, 'resolution'], 
    ['op_maskObstacle_thick', 'f', 200e-9, 'thickness'],
    ['op_maskObstacle_delta', 'f', 0.0135615645, 'refractiveIndex'], 
    ['op_maskObstacle_atten_len', 'f', 2.753364e-8, 'attenuationLength'], 
    ['op_maskObstacle_horizontalCenterCoordinate', 'f', 0.0, 'horizontalCenterCoordinate'],
    ['op_maskObstacle_verticalCenterCoordinate', 'f', 0.0, 'verticalCenterCoordinate'],
    ['op_maskObstacle_rotateAngle', 'f', 90.0, 'rotateAngle'],
    ['op_maskObstacle_cutoffBackgroundNoise', 'f', 0.001, 'cutoffBackgroundNoise'],
    ['op_maskObstacle_cropArea', 'i', 0, 'cropArea'],
    ['op_maskObstacle_extTransm', 'i', 0, 'transmissionImage'], 
    ['op_maskObstacle_areaXStart', 'i', 0, 'areaXStart'],
    ['op_maskObstacle_areaXEnd', 'i', 17000, 'areaXEnd'], #200
    ['op_maskObstacle_areaYStart', 'i', 0, 'areaYStart'],
    ['op_maskObstacle_areaYEnd', 'i', 17000, 'areaYEnd'], #798
    ['op_maskObstacle_rotateReshape', 'i', 0, 'rotateReshape'],
    ['op_maskObstacle_backgroundColor', 'i', 0, 'backgroundColor'],
    ['op_maskObstacle_tileImage', 'i', 0, 'tileImage'],
    ['op_maskObstacle_tileRows', 'i', 1, 'tileRows'],
    ['op_maskObstacle_tileColumns', 'i', 1, 'tileColumns'],
    ['op_maskObstacle_shiftX', 'i', 0, 'shiftX'],
    ['op_maskObstacle_shiftY', 'i', 0, 'shiftY'],
    ['op_maskObstacle_invert', 'i', 0, 'invert'],
    
    
    #maskSubstrate: Si02
    ['op_maskSubstrate_file_path', 's', '/user/home/opt/xl/xl/experiments/masks/vert_substrate.tif', 'imageFile'], #mask1IN
    ['op_maskSubstrate_outputImageFormat', 's', 'tif', 'outputImageFormat'],
    ['op_maskSubstrate_position', 'f', 37.0, 'position'],
    ['op_maskSubstrate_resolution', 'f', 2.5e-09, 'resolution'], 
    ['op_maskSubstrate_thick', 'f', 40e-9, 'thickness'],
    ['op_maskSubstrate_delta', 'f', 0.0940100942, 'refractiveIndex'], 
    ['op_maskSubstrate_atten_len', 'f', 0.100688e-06, 'attenuationLength'], 
    ['op_maskSubstrate_horizontalCenterCoordinate', 'f', 0.0, 'horizontalCenterCoordinate'],
    ['op_maskSubstrate_verticalCenterCoordinate', 'f', 0.0, 'verticalCenterCoordinate'],
    ['op_maskSubstrate_rotateAngle', 'f', 0.0, 'rotateAngle'],
    ['op_maskSubstrate_cutoffBackgroundNoise', 'f', 0.001, 'cutoffBackgroundNoise'],
    ['op_maskSubstrate_cropArea', 'i', 0, 'cropArea'],
    ['op_maskSubstrate_extTransm', 'i', 0, 'transmissionImage'], 
    ['op_maskSubstrate_areaXStart', 'i', 0, 'areaXStart'],
    ['op_maskSubstrate_areaXEnd', 'i', 17000, 'areaXEnd'], #200
    ['op_maskSubstrate_areaYStart', 'i', 0, 'areaYStart'],
    ['op_maskSubstrate_areaYEnd', 'i', 17000, 'areaYEnd'], #798
    ['op_maskSubstrate_rotateReshape', 'i', 0, 'rotateReshape'],
    ['op_maskSubstrate_backgroundColor', 'i', 0, 'backgroundColor'],
    ['op_maskSubstrate_tileImage', 'i', 0, 'tileImage'],
    ['op_maskSubstrate_tileRows', 'i', 1, 'tileRows'],
    ['op_maskSubstrate_tileColumns', 'i', 1, 'tileColumns'],
    ['op_maskSubstrate_shiftX', 'i', 0, 'shiftX'],
    ['op_maskSubstrate_shiftY', 'i', 0, 'shiftY'],
    ['op_maskSubstrate_invert', 'i', 0, 'invert'],

     # Mask: sample [values for Si3N4]
    ['op_Mask_file_path', 's', '/user/home/opt/xl/xl/experiments/masks/vert_mask.tif', 'imageFile'], #mask1IN
    ['op_Mask_outputImageFormat', 's', 'tif', 'outputImageFormat'],
    ['op_Mask_position', 'f', 37.0, 'position'],
    ['op_Mask_resolution', 'f', 2.5e-09, 'resolution'], 
    ['op_Mask_thick', 'f', 72e-9, 'thickness'],
    ['op_Mask_delta', 'f', 0.0253030726473131, 'refractiveIndex'], #UPDATED -JK
    ['op_Mask_atten_len', 'f', 4.372202275503694e-08, 'attenuationLength'],  #UPDATED -JK
    ['op_Mask_horizontalCenterCoordinate', 'f', 0.0, 'horizontalCenterCoordinate'],
    ['op_Mask_verticalCenterCoordinate', 'f', 0.0, 'verticalCenterCoordinate'],
    ['op_Mask_rotateAngle', 'f', 90.0, 'rotateAngle'],
    ['op_Mask_cutoffBackgroundNoise', 'f', 0.001, 'cutoffBackgroundNoise'],
    ['op_Mask_cropArea', 'i', 0, 'cropArea'],
    ['op_Mask_extTransm', 'i', 0, 'transmissionImage'], 
    ['op_Mask_areaXStart', 'i', 0, 'areaXStart'],
    ['op_Mask_areaXEnd', 'i', 17000, 'areaXEnd'], #200
    ['op_Mask_areaYStart', 'i', 0, 'areaYStart'],
    ['op_Mask_areaYEnd', 'i', 17000, 'areaYEnd'], #798
    ['op_Mask_rotateReshape', 'i', 0, 'rotateReshape'],
    ['op_Mask_backgroundColor', 'i', 0, 'backgroundColor'],
    ['op_Mask_tileImage', 'i', 0, 'tileImage'],
    ['op_Mask_tileRows', 'i', 1, 'tileRows'],
    ['op_Mask_tileColumns', 'i', 1, 'tileColumns'],
    ['op_Mask_shiftX', 'i', 0, 'shiftX'],
    ['op_Mask_shiftY', 'i', 0, 'shiftY'],
    ['op_Mask_invert', 'i', 1, 'invert'],

    # Drift_Mask_To_AerialImage: drift
    ['op_Drift_Mask_To_AerialImage_L', 'f', 0.000170, 'length'], #0.00020443924880224158



#---Propagation parameters
    ['op_WBS_pp', 'f',                                           [0, 0, 1.0, 0, 0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'WBS'],
    ['op_After_WBS_Before_Toroidal_Mirror_pp', 'f',              [0, 0, 1.0, 1, 0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'After_WBS_Before_Toroidal_Mirror'],  
    ['op_Toroidal_Mirror_pp', 'f',                               [0, 0, 1.0, 0, 0, 2.0, 1.0, 2.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'Toroidal_Mirror'],
    ['op_After_Toroidal_Mirror_Before_PGM_pp', 'f',              [0, 0, 1.0, 1, 0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'After_Toroidal_Mirror_Before_PGM'],
    ['op_Planar_Mirror_pp', 'f',                                 [0, 0, 1.0, 0, 0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'Planar_Mirror'],
    ['op_Planar_Mirror_Grating_pp', 'f',                         [0, 0, 1.0, 1, 0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'Planar_Mirror_Grating'],
    ['op_Grating_pp', 'f',                                       [0, 0, 1.0, 0, 0, 2.0, 1.0, 2.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'Grating'],
    ['op_Grating_Before_Exit_Aperture_pp', 'f',                  [0, 0, 1.0, 1, 0, 1.25, 0.8, 1.25, 0.8, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'Grating_Before_Exit_Aperture'],
    ['op_Exit_Aperture_pp', 'f',                                 [0, 0, 1.0, 0, 0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'Exit_Aperture'],
    ['op_After_Exit_Aperture_Before_Cylindrical_Mirror_pp', 'f', [0, 0, 1.0, 1, 0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'After_Mask_Aperture_Before_Cylindrical_Mirror'],
    ['op_Cylindrical_Mirror_pp', 'f',                            [0, 0, 1.0, 0, 0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'Cylindrical_Mirror'], 
    ['op_Circular_Cylinder_pp', 'f',                             [0, 0, 1.0, 0, 0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'Circular_Cylinder'],
    ['op_After_Cylindrical_Mirror_Before_Exit_Slit_pp', 'f',     [0, 0, 1.0, 1, 0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'After_Cylindrical_Mirror_Before_Exit_Slit'],
    ['op_Exit_Slits_pp', 'f',                                    [0, 0, 1.0, 0, 0, 0.1, 32.0, 0.1, 32.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'Exit_Slits'],
    ['op_Exit_Slits_Drift_pp', 'f',                              [0 ,0, 1.0, 1, 0, 1.0, 1.0, 1.0,  1.0,    0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'Exit_Slits_Drift'],
    ['op_Exit_Slits_Cleanup_pp', 'f',                            [0, 0, 1.0, 0, 0, 1.0, 1.0, 1.0,  1.0,    0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  'Exit_Slits_Cleanup'],  
    ['op_After_Exit_Slit_Before_BDA_pp', 'f',                    [0, 0, 1.0, 1, 0, 1.5,  0.5, 1.5, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'After_Exit_Slit_Before_BDA'],  
    ['op_FZP_Aperture_pp', 'f',                                  [0, 0, 1.0, 0, 0, 0.25, 4.0, 0.25, 4.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'BDA_Mask_Aperture'],
    ['op_FZP_pp', 'f',                                           [0, 0, 1.0, 0, 0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'FZP'],
    ['op_BDA_Mask_Aperture_pp', 'f',                             [0, 0, 1.0, 1, 0, 0.25, 34.0, 0.5, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'BDA_Mask_Aperture'],
    ['op_BDA_pp', 'f',                                           [0, 0, 1.0, 0, 0, 0.5, 1.0, 0.5, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'BDA'],  
#    ['op_BDA_pp', 'f',                                           [0, 0, 1.0, 0, 0, 0.05, 150.0, 0.05, 10.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'BDA'],  
     
    # exit slit to bda sampling was set to -- 6(x), 8(y) - changed to 1.5(x), 3.2(y)
    # exit slit to bda range was set to -- 0.3(x), 0.02(y) - changed to 1.2(x), 0.05(y) - by jerome
    
    # bda sampling was -- 42.5(x), 10(y) - changed to 170(x), 25(y)
    # bda range was -- 0.12(x), 0.07(y) - changed to 0.03(x), 0.028(y) 
    # Mask Stack: 
    ['op_maskObstacle_pp', 'f',                                  [0, 0, 1.0, 0, 0, 0.5, 4.0, 0.5, 4.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'Mask obstacle'],    
    # mask obstacle range changed from 0.5 to 0.125(x), 0.2(y) to match previous change - jerome
    ['op_maskSubstrate_pp', 'f',                                 [0, 0, 1.0, 0, 0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'Mask Substrate'],    
    ['op_Mask_pp', 'f',                                          [0, 0, 1.0, 0, 0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'Mask Absorber'],
    ['op_Drift_Mask_To_AerialImage_pp', 'f',                     [0, 0, 1.0, 1, 0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'Drift_Mask_To_AerialImage'],

    #OLD['op_Mask_Mask_pp', 'f',                                 [0, 0, 1.0, 0, 0, 0.6,  1.0, 0.6, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'final post-propagation (resize) parameters'],


    ['op_fin_pp', 'f',                                           [0, 0, 1.0, 0, 0, 1.0,  1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'final post-propagation (resize) parameters'],




    ])
    #[ 0]: Auto-Resize (1) or not (0) Before propagation
    #[ 1]: Auto-Resize (1) or not (0) After propagatio
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
