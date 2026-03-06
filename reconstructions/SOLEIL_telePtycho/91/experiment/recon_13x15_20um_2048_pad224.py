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
tutorial_data_home = '/user/home/ptypy-0.5.0/jk/experiments/SOLEIL_telePtycho_91/'


scan_name = '13x15_20um_1600_pad448'
#
## Dataset for this tutorial
dataset = f"SOLEIL_{scan_name}.h5"
PROBE_FILE = None #'/user/home/ptypy-0.5.0/jk/experiments/SOLEIL_telePtycho/15x5_4um_256/recons/best/ExampleRec_ML_0500.ptyr'

reconfile = None #'/user/home/ptypy-0.5.0/jk/experiments/XFM_ptycho/multi_distance/recons/ExampleRec_multiZ_singleZ/ExampleRec_multiZ_singleZ_ML_0500.ptyr'

# Absolute path to HDF5 file with raw data
path_to_data = tutorial_data_home + dataset #os.path.join(tutorial_data_home, dataset)
# path_to_probe = tutorial_data_home + probe

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
p.io.home = f"{tutorial_data_home}{scan_name}/"
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
p.scans.scan_00.data.intensities.key = "data"

#p.scans.scan_00.data.shape = (256,256) #(256,256) #(512,512)#(1024,1024)
#p.scans.scan_00.data.rebin = 1
p.scans.scan_00.data.center = () 
if p.scans.scan_00.data.center == None:
    p.scans.scan_00.data.auto_center = True
else:
    p.scans.scan_00.data.auto_center = False

# Read positions data
p.scans.scan_00.data.positions = u.Param()
p.scans.scan_00.data.positions.file = path_to_data
p.scans.scan_00.data.positions.slow_key = "posy_m"
p.scans.scan_00.data.positions.slow_multiplier = 1.0
p.scans.scan_00.data.positions.fast_key = "posx_m"
p.scans.scan_00.data.positions.fast_multiplier = 1.0

# Read meta data: photon energy
p.scans.scan_00.data.recorded_energy = u.Param()
p.scans.scan_00.data.recorded_energy.file = path_to_data
p.scans.scan_00.data.recorded_energy.key = "energy_ev"
p.scans.scan_00.data.recorded_energy.multiplier = 1e-3

# Read meta data: detector distance
p.scans.scan_00.data.recorded_distance = u.Param()
p.scans.scan_00.data.recorded_distance.file = path_to_data
p.scans.scan_00.data.recorded_distance.key = "det_distance_m"
p.scans.scan_00.data.recorded_distance.multiplier = 1.0

# Read meta data: detector pixelsize
p.scans.scan_00.data.recorded_psize = u.Param()
p.scans.scan_00.data.recorded_psize.file = path_to_data
p.scans.scan_00.data.recorded_psize.key = "det_pixelsize_m"
p.scans.scan_00.data.recorded_psize.multiplier = 1.0

# load parameters from data file
f = h5py.File(path_to_data,'r')

p.scans.scan_00.data.psize = f['det_pixelsize_m'][()] # 1.0884810724605152e-05
p.scans.scan_00.data.distance = f['det_distance_m'][()] #0.0147700437245549 #z2
#0.0147720437245549 #z1
p.scans.scan_00.data.energy = f['energy_ev'][()]*1e-3 #0.185

# Define reconstruction engine (using DM)
p.engines = u.Param()
p.engines.engine00 = u.Param()
p.engines.engine00.name = "DM"
p.engines.engine00.numiter = 300
p.engines.engine00.numiter_contiguous = 10
p.engines.engine00.record_local_error = False
p.engines.engine00.alpha = 0.99 #0.99
p.engines.engine00.probe_support = 0.7
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

# p.engines.engine01 = u.Param()
# p.engines.engine01.name = 'ML'
# p.engines.engine01.ML_type = 'Gaussian'
# p.engines.engine01.numiter = 200
# p.engines.engine01.numiter_contiguous = 10
# #p.engines.engine01.reg_del2 = True
# #p.engines.engine01.reg_del2_amplitude = .01
# p.engines.engine01.scale_precond = True
# p.engines.engine01.scale_probe_object = 1.
# p.engines.engine01.probe_update_start = 15
# p.engines.engine01.probe_support = None

# #initializing position corrections
# p.engines.engine01.position_refinement = u.Param()
# p.engines.engine01.position_refinement.method = 'Annealing'
# p.engines.engine01.position_refinement.start = 50
# p.engines.engine01.position_refinement.stop = 200
# p.engines.engine01.position_refinement.interval = 10
# p.engines.engine01.position_refinement.nshifts = 8
# p.engines.engine01.position_refinement.amplitude = 5.0e-8
# p.engines.engine01.position_refinement.max_shift = 1.0e-7

print(p.scans.scan_00.data.psize)
print(p.scans.scan_00.data.distance)

# Run reconstruction
P = ptypy.core.Ptycho(p,level=5)
