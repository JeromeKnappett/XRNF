#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 10:16:57 2024

@author: -
"""

import ptypy, os
import ptypy.utils as u
import h5py
import numpy as np


# This will import the HDF5Loader class
ptypy.load_ptyscan_module("hdf5_loader")

# # This will import the GPU engines
# ptypy.load_gpu_engines("cuda")

# Root directory of tutorial data
data_home ='/user/home/ptypy-0.5.0/jk/experiments/SOLEIL_telePtycho_91/'
#'/data/xfm/22353/HERMES/data/UP_20242172/2025-09-28/' 
# '/user/home/ptypy-0.5.0/jk/experiments/SOLEIL_telePtycho_91/'


scan_name = 'Image_20250928_048standardized'
#'13x15_20um_1600_pad448_reshape'
#
## Dataset for this tutorial
dataset = f"{scan_name}.h5"

PROBE_FILE = None #'/user/home/ptypy-0.5.0/jk/experiments/SOLEIL_telePtycho_91/standardized/recons/real_data_test/real_data_test_DM_0300.ptyr'
OBJECT_FILE = None

# Absolute path to HDF5 file with raw data
path_to_data = data_home + dataset #os.path.join(data_home, dataset)
# path_to_probe = data_home + probe

# # Load the custom probe
# with h5py.File(path_to_probe, 'r') as f:
#     # List datasets
#     print("Datasets in the probe file:")
#     f.visititems(lambda name, obj: print(name) if isinstance(obj, h5py.Dataset) else None)
    
#     # Replace 'probe_dataset' with your actual dataset name
#     custom_probe = f['probe'][()]


# Create parameter tree
p = u.Param()

# Set verbose level to interactive
p.verbose_level = 3#"interactive"

# Set io settings (no files saved)
p.io = u.Param()
p.io.home = f"{data_home}{scan_name}/"
# p.io.rfile = 'test.h5'

p.io.autosave = u.Param(active=True)
p.io.autosave.interval = 10

# Live-plotting during the reconstruction
p.io.autoplot = u.Param()
p.io.autoplot.active=True
p.io.autoplot.threaded = True
p.io.autoplot.layout = "python"
p.io.autoplot.interval = 1

# Define the scan model
p.scans = u.Param()
p.scans.scan_00 = u.Param()
p.scans.scan_00.name = 'BlockFull'


p.scans.scan_00.sample = u.Param()
if OBJECT_FILE is not None:
    p.scans.scan_00.sample.model = 'recon' #None          # 'stxm', 'recons'
    p.scans.scan_00.sample.recon = u.Param()
    p.scans.scan_00.sample.recon.rfile = OBJECT_FILE #'{0}analysis/eiger/SXDM/{1}'.format(BASE_DIR, OBJECT_FILE)
    p.scans.scan_00.sample.process = None
    p.scans.scan_00.sample.diversity = None
else:
    p.scans.scan_00.sample.model = None

# Define the illumination (probe) parameters
p.scans.scan_00.coherence = u.Param()
p.scans.scan_00.coherence.num_probe_modes = 3
p.scans.scan_00.coherence.num_object_modes = 1

# set up probe, load from file if filename is supplied
p.scans.scan_00.illumination = u.Param()

if PROBE_FILE is not None:
    #p.scans.scan_00.illumination.model = 'file'       # 'stxm', 'recons'
    #f = h5py.File('{0}analysis/eiger/SXDM/{1}'.format(BASE_DIR, PROBE_FILE), 'r')
    #dset = f['/content/probe'] #f['/probe']
    #p.scans.scan_00.illumination.model = dset.value
	p.scans.scan_00.illumination.model = 'recon'
	p.scans.scan_00.illumination.recon = u.Param()
	p.scans.scan_00.illumination.recon.rfile = PROBE_FILE
	p.scans.scan_00.illumination.aperture = u.Param()
	p.scans.scan_00.illumination.aperture.form = None
	p.scans.scan_00.illumination.diversity = None #u.Param()
	#p.scans.scan_00.illumination.diversity.power = 0.1
	#p.scans.scan_00.illumination.diversity.noise = (np.pi, 3.0)
	#p.scans.scan_00.illumination.shape= (400,400)
else:
    p.scans.scan_00.illumination.model = None         #None #custom_probe #'recon'  # No analytical model
    p.scans.scan_00.illumination.aperture = u.Param()
    p.scans.scan_00.illumination.aperture.form = 'circ'
    p.scans.scan_00.illumination.aperture.size = (21.0e-6, 21.0e-6)
    p.scans.scan_00.illumination.aperture.edge = 50
    p.scans.scan_00.illumination.diversity = u.Param()
    p.scans.scan_00.illumination.diversity.power = 0.1
    p.scans.scan_00.illumination.diversity.noise = (np.pi, 3.0)
    # p.scans.scan_00.illumination.diversity.shift = None

# Data loader
p.scans.scan_00.data = u.Param()
p.scans.scan_00.data.name = 'Hdf5Loader'

# Read diffraction data
p.scans.scan_00.data.intensities = u.Param()
p.scans.scan_00.data.intensities.file = path_to_data
p.scans.scan_00.data.intensities.key = "entry/data"

# p.scans.scan_00.data.shape = (2048,2048) #(256,256) #(512,512)#(1024,1024)
p.scans.scan_00.data.rebin = 1
p.scans.scan_00.data.center = (1011.3750912548046, 1034.4123909531513)
 # (1019.4916481923785, 1033.1202001680572) 
# p.scans.scan_00.data.padding = (224,224,224,224)# (2048,2048)
if p.scans.scan_00.data.center == None:
    p.scans.scan_00.data.auto_center = True
else:
    p.scans.scan_00.data.auto_center = False
    
p.scans.scan_00.data.orientation = 3

    # Data frame orientation

    # Choose

    #     None or 0: correct orientation

    #     1: invert columns (numpy.flip_lr)

    #     2: invert rows (numpy.flip_ud)

    #     3: invert columns, invert rows

    #     4: transpose (numpy.transpose)

    #     4+i: tranpose + other operations from above

    # Alternatively, a 3-tuple of booleans may be provided (do_transpose, do_flipud, do_fliplr)

    # default = None


# Read positions data
p.scans.scan_00.data.positions = u.Param()
p.scans.scan_00.data.positions.file = path_to_data
p.scans.scan_00.data.positions.slow_key = "entry/pos_y"
p.scans.scan_00.data.positions.slow_multiplier = 1.0
p.scans.scan_00.data.positions.fast_key = "entry/pos_x"
p.scans.scan_00.data.positions.fast_multiplier = 1.0

# Read meta data: photon energy
p.scans.scan_00.data.recorded_energy = u.Param()
p.scans.scan_00.data.recorded_energy.file = path_to_data
p.scans.scan_00.data.recorded_energy.key = "entry/energy_eV"
p.scans.scan_00.data.recorded_energy.multiplier = 1e-3

# # Read meta data: detector distance
# p.scans.scan_00.data.recorded_distance = u.Param()
# p.scans.scan_00.data.recorded_distance.file = path_to_data
# p.scans.scan_00.data.recorded_distance.key = "entry/det_distance_m"
# p.scans.scan_00.data.recorded_distance.multiplier = 1.0

# # Read meta data: detector pixelsize
# p.scans.scan_00.data.recorded_psize = u.Param()
# p.scans.scan_00.data.recorded_psize.file = path_to_data
# p.scans.scan_00.data.recorded_psize.key = "entry/det_pixelsize_m"
# p.scans.scan_00.data.recorded_psize.multiplier = 1.0

# # load parameters from data file
# f = h5py.File(path_to_data,'r')

p.scans.scan_00.data.psize = 11.0e-6#f['entry/det_pixelsize_m'][()] # 1.0884810724605152e-05
p.scans.scan_00.data.distance = 0.0549#f['entry/det_distance_m'][()] #0.0147700437245549 #z2
#0.0147720437245549 #z1
p.scans.scan_00.data.energy = 0.091# f['entry/energy_eV'][()]*1e-3 #0.185

# # Define reconstruction engine (using DM)
p.engines = u.Param()
p.engines.engine00 = u.Param()
p.engines.engine00.name = "DM"
p.engines.engine00.numiter = 300
p.engines.engine00.numiter_contiguous = 10
p.engines.engine00.record_local_error = False
p.engines.engine00.alpha = 0.99 #0.99
p.engines.engine00.probe_support = 0.8
p.engines.engine00.probe_fourier_support = None
p.engines.engine00.overlap_converge_factor = 0.001
p.engines.engine00.probe_update_start = 25
p.engines.engine00.update_object_first = True
p.engines.engine00.obj_smooth_std = None
p.engines.engine00.probe_inertia = 1.0e-3
p.engines.engine00.object_inertia = 1.0e-4
p.engines.engine00.fourier_power_bound = 0.25
p.engines.engine00.fourier_relax_factor = 0.03
p.engines.engine00.clip_object = (0.0001, 1.)

##initializing position corrections
# p.engines.engine00.position_refinement = u.Param()
# p.engines.engine00.position_refinement.method = 'Annealing'
# p.engines.engine00.position_refinement.start = 35
# p.engines.engine00.position_refinement.stop = 300
# p.engines.engine00.position_refinement.interval = 10
# p.engines.engine00.position_refinement.nshifts = 10
# # p.engines.engine00.position_refinement.amplitude = 5.0e-8
# # p.engines.engine00.position_refinement.max_shift = 1.0e-7
# p.engines.engine00.position_refinement.amplitude = p.scans.scan_00.data.psize/110
# p.engines.engine00.position_refinement.max_shift = p.scans.scan_00.data.psize/50

p.engines.engine01 = u.Param()
p.engines.engine01.name = 'ML'
p.engines.engine01.ML_type = 'Gaussian'
p.engines.engine01.numiter = 200
p.engines.engine01.numiter_contiguous = 10
#p.engines.engine01.reg_del2 = True
#p.engines.engine01.reg_del2_amplitude = .01
p.engines.engine01.scale_precond = True
p.engines.engine01.scale_probe_object = 1.
p.engines.engine01.probe_update_start = 15
p.engines.engine01.probe_support = None

#initializing position corrections
p.engines.engine01.position_refinement = u.Param()
p.engines.engine01.position_refinement.method = 'Annealing'
p.engines.engine01.position_refinement.start = 50
p.engines.engine01.position_refinement.stop = 200
p.engines.engine01.position_refinement.interval = 10
p.engines.engine01.position_refinement.nshifts = 8
p.engines.engine01.position_refinement.amplitude = 5.0e-8
p.engines.engine01.position_refinement.max_shift = 1.0e-7

# print(p.scans.scan_00.data.psize)
# print(p.scans.scan_00.data.distance)

# Run reconstruction
P = ptypy.core.Ptycho(p,level=5)

# # Step 1: Load only data (no model yet)
# P = ptypy.core.Ptycho(p, level=4)

# # Step 2: Downsample positions and data
# sample_rate = 10
# scan = P.scans.scan_00
# scan.data.positions = scan.data.positions[::sample_rate]
# scan.data.intensities = scan.data.intensities[::sample_rate]
# print(f"Using {len(scan.data.positions)} positions")

# # Step 3: Initialize models and run engines (equivalent to level=5)
# P.model_init()
# P.engine_iterate()

