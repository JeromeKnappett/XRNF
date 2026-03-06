#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 19:19:49 2021

@author: gvanriessen
"""
import srwl_bl as srwl_bl


opNames = [ # COMMENT OUT ANY UNNECESSARY OPTICAL ELEMENTS
            # 'zero_drift1', 
            'M1A', 
            'M1Ae_M1Bi', 
            'M1B', 
            'M1Be_A1i', 
            'A1', 
            # 'A1e_PGMi', 
            # 'VDG1', 
            # 'VDG1_M2A', 
            # 'M2A', 
            # 'M2A_M3', 
            # 'M3', 
            # 'PGMe_A2i', 
            # 'A2', 
            # 'A2e_M4i', 
            # 'M4', 
            # 'M4e_A3i', 
            # 'A3', 
            # 'A3e_Samplei',
            # 'Sample',    # FZP
            # 'SampleBalls',
            'prop2pinhole',
            'pinhole',
            'prop2detector',
            'resample',
            ]



varParam = [
    ['name', 's', 'SOLEIL-HERMES', 'simulation name'],

#---Data Folder
    ['fdir', 's', 'SOLEIL-HERMES/', 'folder (directory) name for reading-in input and saving output data files'],

#---Electron Beam
    ['ebm_nm', 's', '', 'standard electron beam name'],
    ['ebm_nms', 's', '', 'standard electron beam name suffix: e.g. can be Day1, Final'],
    ['ebm_i', 'f', 0.5, 'electron beam current [A]'],
    ['ebm_e', 'f', 2.75, 'electron beam avarage energy [GeV]'],
    ['ebm_de', 'f', 0.0, 'electron beam average energy deviation [GeV]'],
    ['ebm_x', 'f', 0.0, 'electron beam initial average horizontal position [m]'],
    ['ebm_y', 'f', 0.0, 'electron beam initial average vertical position [m]'],
    ['ebm_xp', 'f', 0.0, 'electron beam initial average horizontal angle [rad]'],
    ['ebm_yp', 'f', 0.0, 'electron beam initial average vertical angle [rad]'],
    ['ebm_z', 'f', 0., 'electron beam initial average longitudinal position [m]'],
    ['ebm_dr', 'f', -0.930952, 'electron beam longitudinal drift [m] to be performed before a required calculation'],
    ['ebm_ens', 'f', 0.001025, 'electron beam relative energy spread'],
    ['ebm_emx', 'f', 3.9e-09, 'electron beam horizontal emittance [m]'],
    ['ebm_emy', 'f', 3.9e-09, 'electron beam vertical emittance [m]'],
    # Definition of the beam through Twiss:
    ['ebm_betax', 'f', 4.598, 'horizontal beta-function [m]'],
    ['ebm_betay', 'f', 2.236, 'vertical beta-function [m]'],
    ['ebm_alphax', 'f', -0.008, 'horizontal alpha-function [rad]'],
    ['ebm_alphay', 'f', 0.001, 'vertical alpha-function [rad]'],
    ['ebm_etax', 'f', 0.165, 'horizontal dispersion function [m]'],
    ['ebm_etay', 'f', 0.0, 'vertical dispersion function [m]'],
    ['ebm_etaxp', 'f', -0.003, 'horizontal dispersion function derivative [rad]'],
    ['ebm_etayp', 'f', 0.0, 'vertical dispersion function derivative [rad]'],
    # Definitition of the beam size and divergence - added by JK to fix error 13/08/25
    ['ebm_sigx', 'f', 0.00021572080480333837, 'horizontal RMS size [m]'],
    ['ebm_sigxp', 'f', 2.9123785250781248e-05, 'horizontal RMS divergence [rad]'],
    ['ebm_mxxp', 'f', 0, "<(x-<x>)(x'-<x'>)> [m]"],
    ['ebm_sigy', 'f', 9.338308197955346e-05, 'vertical RMS size [m]'],
    ['ebm_sigyp', 'f', 4.176345347922784e-05, 'vertical RMS divergence [rad]'],
    ['ebm_myyp', 'f', 0, "<(y-<y>)(y'-<y'>)> [m]"],
    
#---Undulator
#---idealized params
    ['und_bx', 'f', 0.0, 'undulator horizontal peak magnetic field [T]'],
    ['und_by', 'f', 1.096592196256, 'undulator vertical peak magnetic field [T]'],
    ['und_phx', 'f', 0.0, 'initial phase of the horizontal magnetic field [rad]'],
    ['und_phy', 'f', 0.0, 'initial phase of the vertical magnetic field [rad]'],
    ['und_sx', 'i', 1, 'undulator horizontal magnetic field symmetry vs longitudinal position'],
    ['und_sy', 'i', -1, 'undulator vertical magnetic field symmetry vs longitudinal position'],
    ['und_b2e', '', '', 'estimate undulator fundamental photon energy (in [eV]) for the amplitude of sinusoidal magnetic field defined by und_b or und_bx, und_by', 'store_true'],
    ['und_e2b', '', '', 'estimate undulator field amplitude (in [T]) for the photon energy defined by w_e', 'store_true'],
#---tabulated params
    ['und_g', 'f', 6.72, 'undulator gap [mm] (assumes availability of magnetic measurement or simulation data)'],
    ['und_ph', 'f', 0.0, 'shift of magnet arrays [mm] for which the field should be set up'],
    ['und_mfz', 's', '', 'name of zip-file of directory with magnetic measurement files for different gaps + summary file (if it is defined, it overrides the values of und_mdir and und_mfs)'],
#---both  params
    ['und_zc', 'f', 0.0, 'undulator center longitudinal position [m]'],
    ['und_per', 'f', 0.040476, 'undulator period [m]'],
    ['und_len', 'f', 1.7, 'undulator length [m]'],

    ['ut', '', '', 'calculate undulator "operation table", i.e. dependence of gap (and phase) on photon energy (for a given polarization)'],
    ['mf', 'i', 0, 'specify whether or not to calculate magnetic field'],
    
    #Coherent Gaussian Beam Wavefront Propagation
    ['wg', '', '', 'calculate coherent Gaussian beam wavefront propagation (has priority over "si" if both Gaussian beam and e-beam + magnetic field are defined)', 'store_true'],
    ['gs', '', '', 'calculate gaussian spectrum vs photon energy', 'store_true'],
    #Coherent Gaussian Beam Intensity distribution vs horizontal and vertical position
    ['gi', '', '', 'calculate coherent Gaussian beam intensity distribution (without wavefront propagation through a beamline) vs horizontal and vertical position (has priority over "si" if both Gaussian beam and e-beam + magnetic field are defined)', 'store_true'],

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
    ['sm_ei', 'f', 100.0, 'initial photon energy [eV] for multi-e spectrum vs photon energy calculation'],
    ['sm_ef', 'f', 20000.0, 'final photon energy [eV] for multi-e spectrum vs photon energy calculation'],
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
    ['wm', '', '', 'calculate multi-electron (/ partially coherent) wavefront propagation', 'store_true'],


#--- Initial Wavefront Propagation Parameters
    ['w_e', 'f', 185.0, 'photon energy [eV] for calculation of intensity distribution vs horizontal and vertical position'],
    ['w_ef', 'f', -1.0, 'final photon energy [eV] for calculation of intensity distribution vs horizontal and vertical position'],
    ['w_ne', 'i', 1, 'number of points vs photon energy for calculation of intensity distribution'],
    ['w_x', 'f', 0.0, 'central horizontal position [m] for calculation of intensity distribution'],
    ['w_rx', 'f', 0.006, 'range of horizontal position [m] for calculation of intensity distribution'],
    ['w_nx', 'i', 300, 'number of points vs horizontal position for calculation of intensity distribution'],
    ['w_y', 'f', 0.0, 'central vertical position [m] for calculation of intensity distribution vs horizontal and vertical position'],
    ['w_ry', 'f', 0.006, 'range of vertical position [m] for calculation of intensity distribution vs horizontal and vertical position'],
    ['w_ny', 'i', 300, 'number of points vs vertical position for calculation of intensity distribution'],
    ['w_smpf', 'f', 0, 'sampling factor for calculation of intensity distribution vs horizontal and vertical position'],
    ['w_meth', 'i', 1, 'method to use for calculation of intensity distribution vs horizontal and vertical position: 0- "manual", 1- "auto-undulator", 2- "auto-wiggler"'],
    ['w_prec', 'f', 0.01, 'relative precision for calculation of intensity distribution vs horizontal and vertical position'],
    ['w_u', 'i', 1, 'electric field units: 0- arbitrary, 1- sqrt(Phot/s/0.1%bw/mm^2), 2- sqrt(J/eV/mm^2) or sqrt(W/mm^2), depending on representation (freq. or time)'],
    
    ['si_pol', 'i', 6, 'polarization component to extract after calculation of intensity distribution: 0- Linear Horizontal, 1- Linear Vertical, 2- Linear 45 degrees, 3- Linear 135 degrees, 4- Circular Right, 5- Circular Left, 6- Total'],
    #### PUT 1 FOR MULTI-ELECTRON, 0 FOR SINGLE ####
    ['si_type', 'i', 0, 'type of a characteristic to be extracted after calculation of intensity distribution: 0- Single-Electron Intensity, 1- Multi-Electron Intensity, 2- Single-Electron Flux, 3- Multi-Electron Flux, 4- Single-Electron Radiation Phase, 5- Re(E): Real part of Single-Electron Electric Field, 6- Im(E): Imaginary part of Single-Electron Electric Field, 7- Single-Electron Intensity, integrated over Time or Photon Energy'],
    ['w_mag', 'i', 1, 'magnetic field to be used for calculation of intensity distribution vs horizontal and vertical position: 1- approximate, 2- accurate'],

    ['w_zi', 'f', 0., 'initial longitudinal position [m] along electron trajectory for SR calculation (effective if w_zi < w_zf)'],
    ['w_zf', 'f', 0., 'final longitudinal position [m] along electron trajectory for SR calculation (effective if w_zi < w_zf)'],
    #['si_fn', 's', 'res_int_se.dat', 'file name for saving calculated single-e intensity distribution (without wavefront propagation through a beamline) vs horizontal and vertical position'],
    #['si_pl', 's', '', 'plot the input intensity distributions in graph(s): ""- dont plot, "x"- vs horizontal position, "y"- vs vertical position, "xy"- vs horizontal and vertical position'],
#    ['ws_fni', 's', 'res_int_pr_se.dat', 'file name for saving propagated single-e intensity distribution vs horizontal and vertical position'],
    #['ws_pl', 's', '', 'plot the resulting intensity distributions in graph(s): ""- dont plot, "x"- vs horizontal position, "y"- vs vertical position, "xy"- vs horizontal and vertical position'],
    ['si_fn', 's', 'InitialIntensity.dat', 'file name for saving calculated single-e intensity distribution (without wavefront propagation through a beamline) vs horizontal and vertical position'],
    ['si_pl', 's', '', 'plot the input intensity distributions in graph(s): ""- dont plot, "x"- vs horizontal position, "y"- vs vertical position, "xy"- vs horizontal and vertical position'],
    # ['ws_fni', 's', '', 'file name for saving propagated single-e intensity distribution vs horizontal and vertical position'],
    # ['ws_pl', 's', '', 'plot the resulting intensity distributions in graph(s): ""- dont plot, "x"- vs horizontal position, "y"- vs vertical position, "xy"- vs horizontal and vertical position'],


    #changed by GVR for compatibility with new SRW 
    ['ws_fni', 's', 'IntensityDist_SE.dat', 'file name for saving propagated single-e intensity distribution vs horizontal and vertical position'],
    ['ws_pl', 's', '', 'plot the resulting intensity distributions in graph(s): ""- dont plot, "x"- vs horizontal position, "y"- vs vertical position, "xy"- vs horizontal and vertical position'],
    ['ws_fne', 's', '', 'file name for saving initial electric field wavefront (before propagation)'],
    
    #added by GVR for compatibility with new SRW 
    ['ws_fnep', 's', 'EField.dat', 'file name for saving electric field wavefront after propagation'],

    ['wm_nm', 'i', 4000, 'number of macro-electrons (coherent wavefronts) for calculation of multi-electron wavefront propagation'],
    ['wm_na', 'i', 10, 'number of macro-electrons (coherent wavefronts) to average on each node for parallel (MPI-based) calculation of multi-electron wavefront propagation'],
    ['wm_ns', 'i', 1000, 'saving periodicity (in terms of macro-electrons / coherent wavefronts) for intermediate intensity at multi-electron wavefront propagation calculation'],
    #### PUT "20" BELLOW TO EXTRACT MULTI-ELECTRON ELECTRIC FIELD ####
    ['wm_ch', 'i', 61, 'type of a characteristic to be extracted after calculation of multi-electron wavefront propagation: #0- intensity (s0); 1- four Stokes components; 2- mutual intensity cut vs x; 3- mutual intensity cut vs y; 40- intensity(s0), mutual intensity cuts and degree of coherence vs X & Y'],
    ['wm_ap', 'i', 0, 'switch specifying representation of the resulting Stokes parameters: coordinate (0) or angular (1)'],
    ['wm_x0', 'f', 0, 'horizontal center position for mutual intensity cut calculation'],
    ['wm_y0', 'f', 0, 'vertical center position for mutual intensity cut calculation'],
    ['wm_ei', 'i', 0, 'integration over photon energy is required (1) or not (0); if the integration is required, the limits are taken from w_e, w_ef'],
    ['wm_rm', 'i', 1, 'method for generation of pseudo-random numbers for e-beam phase-space integration: 1- standard pseudo-random number generator, 2- Halton sequences, 3- LPtau sequences (to be implemented)'],
    ['wm_am', 'i', 0, 'multi-electron integration approximation method: 0- no approximation (use the standard 5D integration method), 1- integrate numerically only over e-beam energy spread and use convolution to treat transverse emittance'],
    # ['wm_fni', 's', 'res_int_pr_me.dat', 'file name for saving propagated multi-e intensity distribution vs horizontal and vertical position'],
    #added by JK 16/05/25
    ['wm_pol', 'i', 6, 'polarization component to extract after calculation of intensity distribution: 0- Linear Horizontal, 1- Linear Vertical, 2- Linear 45 degrees, 3- Linear 135 degrees, 4- Circular Right, 5- Circular Left, 6- Total'],

    ['stokes_fname','s','stokes',''],
    ['res_ipm','','','container for results of multi-electron wavefront propagation.'],

    ['wm_nmm', 'i', 1, 'number of MPI masters to use'],
    ['wm_ncm', 'i', 30, 'number of Coherent Modes to calculate'],

    ['wm_nop', '', '1', 'switch forcing to do calculations ignoring any optics defined (by set_optics function)', 'store_true'],

    ['wm_fni', 's', 'test_cmd', 'file name for saving propagated multi-e intensity distribution vs horizontal and vertical position'],
    #['wm_fni', 's', 'ex20_res_pr.h5', 'file name for saving propagated multi-e intensity distribution vs horizontal and vertical position'],

    ['wm_fnmi', 's', '', 'file name of input cross-spectral density / mutual intensity; if this file name is supplied, the initial cross-spectral density (for such operations as coherent mode decomposition) will not be calculated, but rathre it will be taken from that file.'],
    ['wm_fncm', 's', '', 'file name of input cross-spectral density / mutual intensity; if this file name is supplied, the initial cross-spectral density (for such operations as coherent mode decomposition) will not be calculated, but rather it will be taken from that file.'],
    ['wm_ff', 's', 'h5', 'format of data file for saving propagated multi-e intensity distribution vs horizontal and vertical position (ascii and hdf5 supported)'],

    #to add options
    ['op_r', 'f', 20.0, 'longitudinal position of the first optical element [m]'],

    # Former appParam:
    ['rs_type', 's', 'u', 'source type, (u) idealized undulator, (t), tabulated undulator, (m) multipole, (g) gaussian beam'],
    ['op_rv','l', [[1,2,3,4,5,6,7,8,9],#,8,9,10,11,12]
                   [1],[1],[1],[1],[1],[1],[1],[1],[1],[1],
                   [1],[1],[1],[1],[1],[1],[1],[1],[1],
                   [1],[1],[1],[1],[1],[1],[1],[1],[1],
                   [1],[1],[1],[1],[1],[1],[1],[1],[1],
                   [1],[1],[1],[1],[1],[1],[1],[1],[1],
                   [1],[1],[1],[1],[1],[1],[1],[1],[1],
                   [1],[1],[1],[1],[1]], 'list of optical element indexes (1-based) after which intensity or other characteristics should be extracted'], #added - JK 11/05/23
    # 16,17,18,19,20,21
                 # # [[1,2,3,4,5,6,7,8,9,10,11,12,13,14],
                 #  # [1,2,3,4,5,6,7,8,9,10,11,12,13,14],
                 #  # [1,2,3,4,5,6,7,8,9,10,11,12,13,14],
                 #  # [1,2,3,4,5,6,7,8,9,10,11,12,13,14],
                 #  # [1,2,3,4,5,6,7,8,9,10,11,12,13,14],
                 #  # [1,2,3,4,5,6,7,8,9,10,11,12,13,14],
                 #  # [1,2,3,4,5,6,7,8,9,10,11,12,13,14]]
                 #  , 'list of optical element indexes (1-based) after which intensity or other characteristics should be extracted'], #added - JK 11/05/23

    ['ws_fnei', 's', '', 'file name to load custom wavefront to propagate'],
    ['om', 'i', 0, 'perform beamline optimisation and possibly source parameters'],
    ['op_dp', 'f', 0., 'length of drift space to be applied after propagation through a beamline [m]'],
    ['op_fno', 's', '', 'file name for saving orientations of optical elements in the lab frame'],
    
    ['w_wr', 'f', 0., 'wavefront radius to set (is taken into account if != 0) [m]; this parameter may be important for subsequent wavefront propagation simulations; by default, it is set by a function calculating the initial wavefront; however, it can also be set manually using this variable'],
    ['w_wre', 'f', 0., 'wavefront radius error (is taken into account if != 0) [m]; this parameter may be important for subsequent wavefront propagation simulations; by default, it is set by a function calculating the initial wavefront; however, it can also be set manually using this variable'],
    ['ws_ap', 'i', 0, 'switch specifying representation of the resulting Stokes parameters (/ Intensity distribution): coordinate (0) or angular (1)'],
    
    
#---Beamline optics:
    # zero_drift1: drift
    ['op_zero_drift1_L', 'f', 0, 'length'],

    # M1A: mirror
    ['op_M1A_hfn', 's', '/user/home/opt_cmd/xl/xl/experiments/SOLEIL_telePtycho/mirror_1d.dat', 'heightProfileFile'],
    ['op_M1A_dim', 's', 'x', 'orientation'],
    ['op_M1A_ang', 'f', 0.04363323129985824, 'grazingAngle'],
    ['op_M1A_amp_coef', 'f', 1.0, 'heightAmplification'],
    ['op_M1A_size_x', 'f', 0.001, 'horizontalTransverseSize'],
    ['op_M1A_size_y', 'f', 0.001, 'verticalTransverseSize'],

    # M1Ae_M1Bi: drift
    ['op_M1Ae_M1Bi_L', 'f', 0.978, 'length'],

    # M1B: toroidalMirror
    ['op_M1B_hfn', 's', '', 'heightProfileFile'],
    ['op_M1B_dim', 's', 'x', 'orientation'],
    ['op_M1B_ap_shape', 's', 'r', 'apertureShape'],
    ['op_M1B_rt', 'f', 126.7, 'tangentialRadius'],
    ['op_M1B_rs', 'f', 0.887, 'sagittalRadius'],
    ['op_M1B_size_tang', 'f', 1.0, 'tangentialSize'],
    ['op_M1B_size_sag', 'f', 1.0, 'sagittalSize'],
    ['op_M1B_ang', 'f', 0.04363323129985824, 'grazingAngle'],
    ['op_M1B_horizontalPosition', 'f', 0.0, 'horizontalPosition'],
    ['op_M1B_verticalPosition', 'f', 0.0, 'verticalPosition'],
    ['op_M1B_nvx', 'f', 0.9990482215818578, 'normalVectorX'],
    ['op_M1B_nvy', 'f', 0.0, 'normalVectorY'],
    ['op_M1B_nvz', 'f', -0.043619387365336, 'normalVectorZ'],
    ['op_M1B_tvx', 'f', 0.043619387365336, 'tangentialVectorX'],
    ['op_M1B_tvy', 'f', 0.0, 'tangentialVectorY'],
    ['op_M1B_amp_coef', 'f', 1.0, 'heightAmplification'],

    # M1Be_A1i: drift
    ['op_M1Be_A1i_L', 'f', 1.022, 'length'],

    # A1: aperture
    ['op_A1_shape', 's', 'r', 'shape'],
    ['op_A1_Dx', 'f', 1.0e-6, 'horizontalSize'], # was 1.0e-3 - changed to represent single slit from YDS
    ['op_A1_Dy', 'f', 5.0e-6, 'verticalSize'],   # was 1.0e-3
    ['op_A1_x', 'f', 0.0, 'horizontalOffset'],
    ['op_A1_y', 'f', 0.0, 'verticalOffset'],

    # A1e_PGMi: drift
    ['op_A1e_PGMi_L', 'f', 3.256, 'length'],

    # VDG1: grating
    ['op_VDG1_hfn', 's', '', 'heightProfileFile'],
    ['op_VDG1_dim', 's', 'y', 'orientation'],
    ['op_VDG1_size_tang', 'f', 0.2, 'tangentialSize'],
    ['op_VDG1_size_sag', 'f', 0.2, 'sagittalSize'],
    ['op_VDG1_nvx', 'f', 0.0, 'nvx'],
    ['op_VDG1_nvy', 'f', 0.99899674389, 'nvy'],
    ['op_VDG1_nvz', 'f', -0.044782872816, 'nvz'],
    ['op_VDG1_tvx', 'f', 0.0, 'tvx'],
    ['op_VDG1_tvy', 'f', 0.044782872816, 'tvy'],
    ['op_VDG1_x', 'f', 0.0, 'horizontalOffset'],
    ['op_VDG1_y', 'f', 0.0, 'verticalOffset'],
    ['op_VDG1_m', 'f', 1, 'diffractionOrder'],
    ['op_VDG1_grDen', 'f', 450.0, 'grooveDensity0'],
    ['op_VDG1_grDen1', 'f', 0.0, 'grooveDensity1'],
    ['op_VDG1_grDen2', 'f', 0.0, 'grooveDensity2'],
    ['op_VDG1_grDen3', 'f', 0.0, 'grooveDensity3'],
    ['op_VDG1_grDen4', 'f', 0.0, 'grooveDensity4'],
    ['op_VDG1_e_avg', 'f', 185.0, 'energyAvg'],
    ['op_VDG1_cff', 'f', 2.0, 'cff'],
    ['op_VDG1_ang', 'f', 0.044797855058534175, 'grazingAngle'],
    ['op_VDG1_rollAngle', 'f', 0.0, 'rollAngle'],
    ['op_VDG1_outoptvx', 'f', 0.0, 'outoptvx'],
    ['op_VDG1_outoptvy', 'f', 0.134078774762, 'outoptvy'],
    ['op_VDG1_outoptvz', 'f', 0.99097067674, 'outoptvz'],
    ['op_VDG1_outframevx', 'f', 1.0, 'outframevx'],
    ['op_VDG1_outframevy', 'f', 0.0, 'outframevy'],
    ['op_VDG1_computeParametersFrom', 'f', 1, 'computeParametersFrom'],
    ['op_VDG1_amp_coef', 'f', 0.001, 'heightAmplification'],

    # VDG1_M2A: drift
    ['op_VDG1_M2A_L', 'f', 0.5, 'length'],

    # M2A: mirror
    ['op_M2A_hfn', 's', '', 'heightProfileFile'],
    ['op_M2A_dim', 's', 'x', 'orientation'],
    ['op_M2A_ang', 'f', 0.020943951023931952, 'grazingAngle'],
    ['op_M2A_amp_coef', 'f', 1.0, 'heightAmplification'],
    ['op_M2A_size_x', 'f', 0.001, 'horizontalTransverseSize'],
    ['op_M2A_size_y', 'f', 0.001, 'verticalTransverseSize'],

    # M2A_M3: drift
    ['op_M2A_M3_L', 'f', 4.327999999999999, 'length'],

    # M3: toroidalMirror
    ['op_M3_hfn', 's', '', 'heightProfileFile'],
    ['op_M3_dim', 's', 'x', 'orientation'],
    ['op_M3_ap_shape', 's', 'r', 'apertureShape'],
    ['op_M3_rt', 'f', 0.146, 'tangentialRadius'],
    ['op_M3_rs', 'f', 83.0, 'sagittalRadius'],
    ['op_M3_size_tang', 'f', 0.96, 'tangentialSize'],
    ['op_M3_size_sag', 'f', 0.8, 'sagittalSize'],
    ['op_M3_ang', 'f', 0.020943951023931952, 'grazingAngle'],
    ['op_M3_horizontalPosition', 'f', 0.0, 'horizontalPosition'],
    ['op_M3_verticalPosition', 'f', 0.0, 'verticalPosition'],
    ['op_M3_nvx', 'f', 0.9997806834748455, 'normalVectorX'],
    ['op_M3_nvy', 'f', 0.0, 'normalVectorY'],
    ['op_M3_nvz', 'f', -0.020942419883356957, 'normalVectorZ'],
    ['op_M3_tvx', 'f', 0.020942419883356957, 'tangentialVectorX'],
    ['op_M3_tvy', 'f', 0.0, 'tangentialVectorY'],
    ['op_M3_amp_coef', 'f', 1.0, 'heightAmplification'],

    # PGMe_A2i: drift
    ['op_PGMe_A2i_L', 'f', 8.328, 'length'],

    # A2: aperture
    ['op_A2_shape', 's', 'r', 'shape'],
    ['op_A2_Dx', 'f', 0.001, 'horizontalSize'],
    ['op_A2_Dy', 'f', 2e-05, 'verticalSize'],
    ['op_A2_x', 'f', 0.0, 'horizontalOffset'],
    ['op_A2_y', 'f', 0.0, 'verticalOffset'],

    # A2e_M4i: drift
    ['op_A2e_M4i_L', 'f', 10.328000000000003, 'length'],

    # M4: toroidalMirror
    ['op_M4_hfn', 's', '', 'heightProfileFile'],
    ['op_M4_dim', 's', 'x', 'orientation'],
    ['op_M4_ap_shape', 's', 'r', 'apertureShape'],
    ['op_M4_rt', 'f', 0.0396, 'tangentialRadius'],
    ['op_M4_rs', 'f', 79.0, 'sagittalRadius'],
    ['op_M4_size_tang', 'f', 0.96, 'tangentialSize'],
    ['op_M4_size_sag', 'f', 0.8, 'sagittalSize'],
    ['op_M4_ang', 'f', 0.02356194490192345, 'grazingAngle'],
    ['op_M4_horizontalPosition', 'f', 0.0, 'horizontalPosition'],
    ['op_M4_verticalPosition', 'f', 0.0, 'verticalPosition'],
    ['op_M4_nvx', 'f', 0.9997224302180006, 'normalVectorX'],
    ['op_M4_nvy', 'f', 0.0, 'normalVectorY'],
    ['op_M4_nvz', 'f', -0.023559764833610154, 'normalVectorZ'],
    ['op_M4_tvx', 'f', 0.023559764833610154, 'tangentialVectorX'],
    ['op_M4_tvy', 'f', 0.0, 'tangentialVectorY'],
    ['op_M4_amp_coef', 'f', 1.0, 'heightAmplification'],

    # M4e_A3i: drift
    ['op_M4e_A3i_L', 'f', 1.0, 'length'],

    # A3: aperture
    ['op_A3_shape', 's', 'r', 'shape'],
    ['op_A3_Dx', 'f', 0.0002, 'horizontalSize'],
    ['op_A3_Dy', 'f', 0.0002, 'verticalSize'],
    ['op_A3_x', 'f', 0.0, 'horizontalOffset'],
    ['op_A3_y', 'f', 0.0, 'verticalOffset'],

    # A3e_Samplei: drift
    ['op_A3e_Samplei_L', 'f', 14.26, 'length'],
        
    #  # maskObstacle: obstacle [Tantillum?]
    # ['op_maskObstacle_file_path', 's', '/user/home/opt/xl/xl/experiments/maskLER_retry2/masks/restest_vert_block.tif', 'imageFile'], #mask1IN
    # ['op_maskObstacle_outputImageFormat', 's', 'tif', 'outputImageFormat'],
    # ['op_maskObstacle_position', 'f', 37.0, 'position'],
    # ['op_maskObstacle_resolution', 'f', 1.0e-09, 'resolution'], 
    # ['op_maskObstacle_thick', 'f', 1000e-9, 'thickness'], # changed from 200.0e-9 to block more photons for LER simulation
    # ['op_maskObstacle_delta', 'f', 0.0135615645, 'refractiveIndex'], 
    # ['op_maskObstacle_atten_len', 'f', 2.753364e-8, 'attenuationLength'], 
    # ['op_maskObstacle_horizontalCenterCoordinate', 'f', 0.0, 'horizontalCenterCoordinate'],
    # ['op_maskObstacle_verticalCenterCoordinate', 'f', 0.0, 'verticalCenterCoordinate'],
    # ['op_maskObstacle_rotateAngle', 'f', 90.0, 'rotateAngle'],
    # ['op_maskObstacle_cutoffBackgroundNoise', 'f', 0.001, 'cutoffBackgroundNoise'],
    # ['op_maskObstacle_cropArea', 'i', 0, 'cropArea'],
    # ['op_maskObstacle_extTransm', 'i', 0, 'transmissionImage'], 
    # ['op_maskObstacle_areaXStart', 'i', 0, 'areaXStart'],
    # ['op_maskObstacle_areaXEnd', 'i', 18027, 'areaXEnd'], #200
    # ['op_maskObstacle_areaYStart', 'i', 0, 'areaYStart'],
    # ['op_maskObstacle_areaYEnd', 'i', 18027, 'areaYEnd'], #798
    # ['op_maskObstacle_rotateReshape', 'i', 0, 'rotateReshape'],
    # ['op_maskObstacle_backgroundColor', 'i', 0, 'backgroundColor'],
    # ['op_maskObstacle_tileImage', 'i', 0, 'tileImage'],
    # ['op_maskObstacle_tileRows', 'i', 1, 'tileRows'],
    # ['op_maskObstacle_tileColumns', 'i', 1, 'tileColumns'],
    # ['op_maskObstacle_shiftX', 'i', 0, 'shiftX'],
    # ['op_maskObstacle_shiftY', 'i', 0, 'shiftY'],
    # ['op_maskObstacle_invert', 'i', 0, 'invert'],
    
      # Sample: sample [values for Si3N4]
    ['op_Sample_file_path', 's','/user/home/opt_cmd/xl/xl/experiments/SOLEIL_telePtycho/masks/SLS_37.5rBlock.tif', 'imageFile'], #mask1IN
    ['op_Sample_outputImageFormat', 's', 'tif', 'outputImageFormat'],
    ['op_Sample_position', 'f', 36.26, 'position'],
    ['op_Sample_resolution', 'f', 10.0e-9, 'resolution'], 
    ['op_Sample_thick', 'f', 1.0e-6, 'thickness'], 
    ['op_Sample_delta', 'f', 0.0135615645, 'refractiveIndex'],
    ['op_Sample_atten_len', 'f', 2.753364e-8, 'attenuationLength'],
    ['op_Sample_xc', 'f', 0.0, 'horizontalCenterCoordinate'],
    ['op_Sample_yc', 'f', 0.0, 'verticalCenterCoordinate'],
    ['op_Sample_rotateAngle', 'f', 90.0, 'rotateAngle'],
    ['op_Sample_cutoffBackgroundNoise', 'f', 0.001, 'cutoffBackgroundNoise'],
    # ['op_Sample_rx', 'f', 1e-05, 'rx'],
    # ['op_Sample_ry', 'f', 1e-05, 'ry'],
    # ['op_Sample_dens', 'f', 20000000.0, 'dens'],
    # ['op_Sample_r_min_bw_obj', 'f', 1e-09, 'r_min_bw_obj'],
    # ['op_Sample_edge_frac', 'f', 0.02, 'edge_frac'],
    # ['op_Sample_obj_size_min', 'f', 1e-07, 'obj_size_min'],
    # ['op_Sample_ang_min', 'f', 0.0, 'ang_min'],
    # ['op_Sample_obj_size_max', 'f', 1.2e-07, 'obj_size_max'],
    # ['op_Sample_ang_max', 'f', 45.0, 'ang_max'],
    # ['op_Sample_obj_size_ratio', 'f', 0.5, 'obj_size_ratio'],
    ['op_Sample_cropArea', 'i', 0, 'cropArea'],
    ['op_Sample_extTransm', 'i', 0, 'transmissionImage'], 
    ['op_Sample_areaXStart', 'i', 0, 'areaXStart'],
    ['op_Sample_areaXEnd', 'i', 8732, 'areaXEnd'],  #17000 #200
    ['op_Sample_areaYStart', 'i', 0, 'areaYStart'],
    ['op_Sample_areaYEnd', 'i',8732, 'areaYEnd'], #17000 #798
    ['op_Sample_rotateReshape', 'i', 0, 'rotateReshape'],
    ['op_Sample_backgroundColor', 'i', 0, 'backgroundColor'],
    ['op_Sample_tileImage', 'i', 0, 'tileImage'],
    ['op_Sample_tileRows', 'i', 1, 'tileRows'],
    ['op_Sample_tileColumns', 'i', 1, 'tileColumns'],
    ['op_Sample_shiftX', 'i', 0, 'shiftX'],
    ['op_Sample_shiftY', 'i', 0, 'shiftY'],
    ['op_Sample_invert', 'i', 0, 'invert'],
    # ['op_Sample_nx', 'i', 1001, 'nx'],
    # ['op_Sample_ny', 'i', 1001, 'ny'],
    # ['op_Sample_obj_type', 'i', 1, 'obj_type'],
    # ['op_Sample_size_dist', 'i', 1, 'size_dist'],
    # ['op_Sample_ang_dist', 'i', 1, 'ang_dist'],
    # ['op_Sample_rand_alg', 'i', 1, 'rand_alg'],
    # ['op_Sample_poly_sides', 'i', 6, 'poly_sides'],
    # ['op_Sample_rand_shapes', 'i', [1, 2, 3, 4], 'rand_shapes'],
    # ['op_Sample_rand_obj_size', 'b', False, 'rand_obj_size'],
    # ['op_Sample_rand_poly_side', 'b', False, 'rand_poly_side'],
    
    # SampleBalls: sample [values for Si3N4]
    ['op_SampleBalls_file_path', 's','/user/home/opt_cmd/xl/xl/experiments/SOLEIL_telePtycho/masks/SLS_200.0p37.5rMask.tif', 'imageFile'], #mask1IN
    ['op_SampleBalls_outputImageFormat', 's', 'tif', 'outputImageFormat'],
    ['op_SampleBalls_position', 'f', 36.26, 'position'],
    ['op_SampleBalls_resolution', 'f', 10.0e-09, 'resolution'], 
    ['op_SampleBalls_thick', 'f', 2.5e-6, 'thickness'], # thickness for pi phase shift @ 185 eV: 0.4746102860553121e-06
    ['op_SampleBalls_delta', 'f', 0.014120740235449956, 'refractiveIndex'], #UPDATED -JK
    ['op_SampleBalls_atten_len', 'f', 4.831876577964474e-07, 'attenuationLength'],  #UPDATED -JK
    ['op_SampleBalls_xc', 'f', 0.0, 'horizontalCenterCoordinate'], # change here for FZP movement!!!
    ['op_SampleBalls_yc', 'f', 0.0, 'verticalCenterCoordinate'],
    ['op_SampleBalls_rotateAngle', 'f', 90.0, 'rotateAngle'],
    ['op_SampleBalls_cutoffBackgroundNoise', 'f', 0.1, 'cutoffBackgroundNoise'], 
    ['op_SampleBalls_cropArea', 'i', 0, 'cropArea'],
    ['op_SampleBalls_extTransm', 'i', 1, 'transmissionImage'],
    ['op_SampleBalls_areaXStart', 'i', 0, 'areaXStart'],
    ['op_SampleBalls_areaXEnd', 'i', 8732, 'areaXEnd'],  #17000 #200
    ['op_SampleBalls_areaYStart', 'i', 0, 'areaYStart'],
    ['op_SampleBalls_areaYEnd', 'i', 8732, 'areaYEnd'], #17000 #798
    ['op_SampleBalls_rotateReshape', 'i', 0, 'rotateReshape'],
    ['op_SampleBalls_backgroundColor', 'i', 0, 'backgroundColor'],
    ['op_SampleBalls_tileImage', 'i', 0, 'tileImage'],
    ['op_SampleBalls_tileRows', 'i', 0, 'tileRows'],
    ['op_SampleBalls_tileColumns', 'i', 0, 'tileColumns'],
    ['op_SampleBalls_shiftX', 'i', 0, 'shiftX'],
    ['op_SampleBalls_shiftY', 'i', 0, 'shiftY'],
    ['op_SampleBalls_invert', 'i', 1, 'invert'],

    
    
    # #maskSubstrate: Si02
    # ['op_maskSubstrate_file_path', 's', '/user/home/opt/xl/xl/test/vert_substrate.tif', 'imageFile'], #mask1IN
    # ['op_maskSubstrate_outputImageFormat', 's', 'tif', 'outputImageFormat'],
    # ['op_maskSubstrate_position', 'f', 37.0, 'position'],
    # ['op_maskSubstrate_resolution', 'f', 2.5e-09, 'resolution'], 
    # ['op_maskSubstrate_thick', 'f', 40e-9, 'thickness'],
    # ['op_maskSubstrate_delta', 'f', 0.0940100942, 'refractiveIndex'], 
    # ['op_maskSubstrate_atten_len', 'f', 0.100688e-06, 'attenuationLength'], 
    # ['op_maskSubstrate_horizontalCenterCoordinate', 'f', 0.0, 'horizontalCenterCoordinate'],
    # ['op_maskSubstrate_verticalCenterCoordinate', 'f', 0.0, 'verticalCenterCoordinate'],
    # ['op_maskSubstrate_rotateAngle', 'f', 0.0, 'rotateAngle'],
    # ['op_maskSubstrate_cutoffBackgroundNoise', 'f', 0.001, 'cutoffBackgroundNoise'],
    # ['op_maskSubstrate_cropArea', 'i', 0, 'cropArea'],
    # ['op_maskSubstrate_extTransm', 'i', 0, 'transmissionImage'], 
    # ['op_maskSubstrate_areaXStart', 'i', 0, 'areaXStart'],
    # ['op_maskSubstrate_areaXEnd', 'i', 17000, 'areaXEnd'], #200
    # ['op_maskSubstrate_areaYStart', 'i', 0, 'areaYStart'],
    # ['op_maskSubstrate_areaYEnd', 'i', 17000, 'areaYEnd'], #798
    # ['op_maskSubstrate_rotateReshape', 'i', 0, 'rotateReshape'],
    # ['op_maskSubstrate_backgroundColor', 'i', 0, 'backgroundColor'],
    # ['op_maskSubstrate_tileImage', 'i', 0, 'tileImage'],
    # ['op_maskSubstrate_tileRows', 'i', 1, 'tileRows'],
    # ['op_maskSubstrate_tileColumns', 'i', 1, 'tileColumns'],
    # ['op_maskSubstrate_shiftX', 'i', 0, 'shiftX'],
    # ['op_maskSubstrate_shiftY', 'i', 0, 'shiftY'],
    # ['op_maskSubstrate_invert', 'i', 0, 'invert'],


    #  # Mask: sample [values for Si3N4]
    # ['op_Mask_file_path', 's', '/user/home/opt/xl/xl/experiments/maskLER_retry2/masks/restest_vert_mask.tif', 'imageFile'], #mask1IN
    # ['op_Mask_outputImageFormat', 's', 'tif', 'outputImageFormat'],
    # ['op_Mask_position', 'f', 37.0, 'position'],
    # ['op_Mask_resolution', 'f', 1.0e-09, 'resolution'], 
    # ['op_Mask_thick', 'f', 20e-9, 'thickness'],
    # ['op_Mask_delta', 'f', 0.0253030726473131, 'refractiveIndex'], #UPDATED -JK
    # ['op_Mask_atten_len', 'f', 4.372202275503694e-08, 'attenuationLength'],  #UPDATED -JK
    # ['op_Mask_horizontalCenterCoordinate', 'f', 0.0, 'horizontalCenterCoordinate'],
    # ['op_Mask_verticalCenterCoordinate', 'f', 0.0, 'verticalCenterCoordinate'],
    # ['op_Mask_rotateAngle', 'f', 90.0, 'rotateAngle'],
    # ['op_Mask_cutoffBackgroundNoise', 'f', 0.001, 'cutoffBackgroundNoise'],
    # ['op_Mask_cropArea', 'i', 0, 'cropArea'],
    # ['op_Mask_extTransm', 'i', 0, 'transmissionImage'], 
    # ['op_Mask_areaXStart', 'i', 0, 'areaXStart'],
    # ['op_Mask_areaXEnd', 'i', 18027, 'areaXEnd'], #200
    # ['op_Mask_areaYStart', 'i', 0, 'areaYStart'],
    # ['op_Mask_areaYEnd', 'i', 18027, 'areaYEnd'], #798
    # ['op_Mask_rotateReshape', 'i', 0, 'rotateReshape'],
    # ['op_Mask_backgroundColor', 'i', 0, 'backgroundColor'],
    # ['op_Mask_tileImage', 'i', 0, 'tileImage'],
    # ['op_Mask_tileRows', 'i', 1, 'tileRows'],
    # ['op_Mask_tileColumns', 'i', 1, 'tileColumns'],
    # ['op_Mask_shiftX', 'i', 0, 'shiftX'],
    # ['op_Mask_shiftY', 'i', 0, 'shiftY'],
    # ['op_Mask_invert', 'i', 1, 'invert'],
    
    # prop2pinhole: drift   # f = 30.33 cm
    ['op_prop2pinhole_L', 'f', 0.0011187746837473512, 'length'],
    
    # pinhole: aperture
    ['op_pinhole_shape', 's', 'c', 'shape'],
    ['op_pinhole_Dx', 'f', 4.0e-06, 'horizontalSize'],
    ['op_pinhole_Dy', 'f', 4.0e-06, 'verticalSize'],
    ['op_pinhole_x', 'f', 0.0, 'horizontalOffset'],
    ['op_pinhole_y', 'f', 0.0, 'verticalOffset'],
    
    # prop2detector: drift
    ['op_prop2detector_L', 'f', 6.52e-3, 'length'],
    
    # resample: zero drift
    ['op_resample_L', 'f', 0.0, 'length'],

    # detector parameters - added by JK to fix errors for new SRW version
    ['d_x', 'f', 0.0, 'horizontal center position of active area [m]'],
    ['d_rx', 'f', 0.022528, 'horizontal size of active area [m]'],
    ['d_nx', 'i', 2048, 'number of pixels in horizontal direction'],
    ['d_dx', 'f', 11.0e-6, 'horizontal pixel size [m]'],
    ['d_y', 'f', 0.0, 'vertical center position of active area [m]'],
    ['d_ry', 'f', 0.022528, 'vertical size of active area [m]'],
    ['d_ny', 'i', 2048, 'number of pixels in vertical direction'],
    ['d_dy', 'f', 11.0e-6, 'vertical pixel size [m]'],
    ['d_or', 'i', 1, 'interpolation order (i.e. order of polynomials to be used at 2D interpolation)'],
    ['d_ifn', 's', '', 'file name with detector spectral efficiency data'],
    # ['wm_fnei', 's', '', 'file name to load custom wavefront to propagate'],

#---Propagation parameters
    ['op_zero_drift1_pp', 'f', [0, 0, 1.0, 0, 0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'zero_drift1'],
    ['op_M1A_pp', 'f',         [0, 0, 1.0, 0, 0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'M1A'],
    ['op_M1Ae_M1Bi_pp', 'f',   [0, 0, 1.0, 1, 0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'M1Ae_M1Bi'],
    ['op_M1B_pp', 'f',         [0, 0, 1.0, 0, 0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'M1B'],
    ['op_M1Be_A1i_pp', 'f',    [0, 0, 1.0, 1, 0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'M1Be_A1i'],
    # ['op_A1_pp', 'f',          [0, 0, 1.0, 0, 0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'A1'], # for grating mask ptycho (1mm aperture)
    ['op_A1_pp', 'f',          [0, 0, 1.0, 0, 0, 0.02, 4250.0, 0.004, 250.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'A1'], # for pinhole ptycho (1x5 um aperture)
    
    # ['op_A1e_PGMi_pp', 'f',    [0, 0, 1.0, 1, 0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'A1e_PGMi'],
    # ['op_VDG1_pp', 'f',        [0, 0, 1.0, 0, 0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'VDG1'],
    # ['op_VDG1_M2A_pp', 'f',    [0, 0, 1.0, 1, 0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'VDG1_M2A'],
    # ['op_M2A_pp', 'f',         [0, 0, 1.0, 0, 0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'M2A'],
    # ['op_M2A_M3_pp', 'f',      [0, 0, 1.0, 1, 0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'M2A_M3'],
    # ['op_M3_pp', 'f',          [0, 0, 1.0, 0, 0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'M3'],
    # ['op_PGMe_A2i_pp', 'f',    [0, 0, 1.0, 1, 0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'PGMe_A2i'],
    # ['op_A2_pp', 'f',          [0, 0, 1.0, 0, 0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'A2'],
    # ['op_A2e_M4i_pp', 'f',     [0, 0, 1.0, 1, 0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'A2e_M4i'],
    # ['op_M4_pp', 'f',          [0, 0, 1.0, 0, 0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'M4'],
    # ['op_M4e_A3i_pp', 'f',     [0, 0, 1.0, 1, 0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'M4e_A3i'],
    # ['op_A3_pp', 'f',          [0, 0, 1.0, 0, 0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'A3'],

    ['op_A3e_Samplei_pp', 'f',   [0, 0, 1.0, 1, 0, 1.0, 85.0, 0.2, 5.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'A3e_Samplei'],
    ['op_Sample_pp', 'f',          [0, 0, 1.0, 0, 0, 0.02, 50.0, 0.02, 50.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'Sample'],
    ['op_SampleBalls_pp', 'f',     [0, 0, 1.0, 0, 0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'Sample'],
    # ['op_Sample_pp', 'f',          [0, 0, 1.0, 0, 0, 1.0, 61.12 / 2, 1.0, 4.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'Sample'],
    # ['op_prop2pinhole_pp', 'f',   [0, 0, 1.0, 0, 0, 100.0, 0.002, 20.0, 0.05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'prop2pinhole'],
    ['op_prop2pinhole_pp', 'f',    [0, 0, 1.0, 1, 0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'prop2pinhole'],
    ['op_pinhole_pp', 'f',         [0, 0, 1.0, 0, 0, 0.2, 5.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'pinhole'],
    # ['op_prop2detector_pp', 'f',   [0, 0, 1.0, 0, 0, 86.46694748806735, 0.00321606117624494, 271.42015822870775, 0.0010678436721095097, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'afterAp2_Sample'],
    # ['op_prop2detector_pp', 'f',   [0, 0, 1.0, 0, 0, 2.5, 0.00013333333333333334, 2.5, 0.00013280000000000003, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'afterAp2_Sample'],
    ['op_prop2detector_pp', 'f',  [0, 0, 1.0, 3, 0, 0.16, 2.0, 0.16, 85.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'afterAp2_Sample'],
    # ['op_prop2detector_pp', 'f',  [0, 0, 1.0, 0, 0, 200.0, 0.00025, 200.0, 0.016, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'afterAp2_Sample'],
    # ['op_resample_pp', 'f',        [0, 0, 1.0, 0, 0, 0.5123, 0.488, 0.41, 1.22, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'resample'], # FOR GRATING MASK PTYCHO
    ['op_resample_pp', 'f',        [0, 0, 1.0, 0, 0, 0.5123/3, 0.488*3, 0.41, 1.22, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'resample'], # FOR PINHOLE PTYCHO
    ['op_fin_pp', 'f',         [0, 0, 1.0, 0, 0, 0.1, 0.002, 0.1, 0.06, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'final post-propagation (resize) parameters'],

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
