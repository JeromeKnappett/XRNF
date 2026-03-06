#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 10:15:51 2024

@author: -
"""

import h5py
import numpy as np
import matplotlib.pyplot as plt
import tifffile as tiff
import os
from skimage.transform import resize

def create_hdf5_file(filename, diffraction_patterns, positions, energy_ev, det_distance_m, det_pixelsize_um):
    """
    Create an HDF5 file with the necessary structure for ptychographic reconstruction.

    Parameters:
    - filename: Name of the HDF5 file to create.
    - diffraction_patterns: NumPy array of diffraction patterns.
    - positions: Tuple of (posx_mm, posy_mm) arrays indicating the beam positions.
    - energy_ev: Photon energy in electron volts.
    - det_distance_mm: Detector distance from the sample in millimeters.
    - det_pixelsize_um: Detector pixel size in micrometers.
    """
    with h5py.File(filename, 'w') as f:
        # Save diffraction patterns
        f.create_dataset("data", data=diffraction_patterns)
        
        # Save positions
        posx_mm, posy_mm = positions
        f.create_dataset("posx_m", data=posx_mm)
        f.create_dataset("posy_m", data=posy_mm)
        
        f.create_dataset("energy_ev",data=energy_ev)
        f.create_dataset("det_distance_m",data=det_distance_m)
        f.create_dataset("det_pixelsize_m",data=det_pixelsize_um)
        


def listDataSets(file_path):
    with h5py.File(file_path, 'r') as f:
        def printname(name):
            print(name)
        f.visit(printname)


# # Root directory of tutorial data
# tutorial_data_home = "/user/home/opt/xl/xl/experiments/XFM_ptycho/data/PtychoTest/"

# # Dataset for this tutorial
# dataset = "tutorial_data.h5"

# # Absolute path to HDF5 file with raw data
# file_path = os.path.join(tutorial_data_home, dataset)

# listDataSets(file_path)

def scanFromCSV(path,xc,yc,Ic,Iname,num='all'):    
    """
    Reads data from a CSV file and returns specified columns as a DataFrame.
    
    Parameters:
    - file_path (str): The path to the CSV file.
    - columns (list): List of column headers to read. If None, reads all columns.
    - Isize: Size of intensity files (x,y)
    - num: Number of intensity files to extract. 'all' for all.
    Returns:
    - DataFrame with specified columns or all columns if not specified.
    """
    # import csv    
    import pandas as pd
    
    # if num=='all':
        # num = len(data[xc])
    try:
        data = pd.read_csv(path, usecols=[xc,yc,Ic])
        if num == 'all':
            x_pos = data[xc]
            y_pos = data[yc]
            Ifiles = [f'{c}{Iname}' for c in data[Ic]]
        else:
            try:
                x_pos = data[xc][0:num]
                y_pos = data[yc][0:num]
                Ifiles = [f'{c}{Iname}' for c in data[Ic][0:num]]
            except:
                x_pos = data[xc][num[0]:num[1]]
                y_pos = data[yc][num[0]:num[1]]
                Ifiles = [f'{c}{Iname}' for c in data[Ic][num[0]:num[1]]]
                
        print(Ifiles[0:2])
        return x_pos,y_pos,Ifiles
    except FileNotFoundError:
        print("The specified file was not found.")
    except pd.errors.EmptyDataError:
        print("The file is empty.")
    except pd.errors.ParserError:
        print("There was an error parsing the file.")
    except ValueError as e:
        print(f"Error: {e}")

        
def test():
    data_dir = '/user/home/opt_cmd/xl/xl/experiments/SOLEIL_telePtycho/data/test_scan_2um/'  # Update this with the path to your files
    probe_dir = '/user/home/opt_cmd/xl/xl/experiments/SOLEIL_telePtycho/data/test_scan_2um/' '/user/home/opt/xl/xl/experiments/XFM_ptycho/data/phaseSpace/samplePinhole_in/intensity.tif'
    
    numIntensities = 9

    # Load your 9 far-field intensity TIFF files
    intensity_files = [f'pos{i}/intensity.tif' for i in range(1, numIntensities + 1)]
    intensities = [tiff.imread(f'{data_dir}/{file}') for file in intensity_files]
    
    # Load your probe intensity array (assuming it's still a numpy array; adjust if it's also a TIFF)
    probe_intensity = tiff.imread(probe_dir)#f'{data_dir}/probe/intensity.tif')  # If probe is a TIFF, use tiff.imread
    
    # Example usage:
    # Generate synthetic data for demonstration
    diffraction_patterns = intensities #np.random.rand(10, 256, 256)  # 10 patterns of 256x256 pixels
    positions_x = np.linspace(-0.25, 0.25, 3)  # 3 positions in um
    positions_y = np.linspace(-0.25, 0.25, 3)  # 3 positions in um
    energy_ev = 8340  # Example photon energy in eV
    det_distance_m = 3.88  # Example detector distance in mm
    det_pixelsize_um = 75  # Example detector pixel size in um
    
    # Create the HDF5 file
    create_hdf5_file(f'{data_dir}tutorial_data.h5', diffraction_patterns, (positions_x, positions_y), energy_ev, det_distance_m, det_pixelsize_um)

def testFromCSV():
    data_dir = '/user/home/opt_cmd/xl/xl/experiments/SOLEIL_telePtycho/' 
    # '/user/home/opt/xl/xl/experiments/XFM_teleptycho/' 
    # '/user/home/opt/xl/xl/experiments/XFM_ptycho/' # Update this with the path to your files
    # probe_dir = '/user/home/opt/xl/xl/experiments/XFM_ptycho/data/phaseSpace/samplePinhole_in/intensity.tif'
    # '/user/home/opt/xl/xl/experiments/XFM_teleptycho/data/testPhaseSpace/atPinhole/intensity.tif'
    # '/user/home/opt/xl/xl/experiments/XFM_ptycho/data/phaseSpace/samplePinhole_in/intensity.tif'
    save_dir = data_dir#'/user/home/ptypy-0.5.0/jk/experiments/SOLEIL_ptycho/'

    saveName = 'SOLEIL_test_2um_128.h5'

    showPositions = True
    inverPositions = False # for when positions are in reference to sample instead of probe
    probe_size = 2.0e-6
    asize = (128,128)

    # Example usage
    x,y,I = scanFromCSV(data_dir + 'test_scan_2um.csv',# 'scan_positions_med_wballs.csv', 
                        xc='op_pinhole_x', 
                        # 'op_pinhole_x',
                        #'op_Sample_xc', 
                        yc= 'op_pinhole_y', 
                        # 'op_pinhole_y',
                        #'op_Sample_yc', 
                        Ic='fdir', 
                        Iname='IntensityDist_SE.dat',
                        num='all' # [225,450]#'all'
                        )
    print(I[0])
    
    print(x)
    print(y)
    print(np.shape(I))
    
    nx = str(np.loadtxt(I[0], dtype=str, comments=None, skiprows=6, max_rows=1, usecols=(0)))[1:]#[1:3]
    ny = str(np.loadtxt(I[0], dtype=str, comments=None, skiprows=9, max_rows=1, usecols=(0)))[1:]#[1:3]
    xMin = str(np.loadtxt(I[0], dtype=str, comments=None, skiprows=4, max_rows=1, usecols=(0)))[1:]#[1:3]
    xMax = str(np.loadtxt(I[0], dtype=str, comments=None, skiprows=5, max_rows=1, usecols=(0)))[1:]#[1:3]
    rx = float(xMax)-float(xMin)
    dx = np.divide(rx,float(nx))
    yMin = str(np.loadtxt(I[0], dtype=str, comments=None, skiprows=7, max_rows=1, usecols=(0)))[1:]#[1:3]
    yMax = str(np.loadtxt(I[0], dtype=str, comments=None, skiprows=8, max_rows=1, usecols=(0)))[1:]#[1:3]
    ry = float(yMax)-float(yMin)
    dy = np.divide(ry,float(ny))
    
    numC = 1 #int(str(np.loadtxt(I, dtype=str, comments=None, skiprows=10, max_rows=1, usecols=(0)))[1:])#[1:3]
    
    print("Resolution (x,y): {}".format((nx,ny)))
    print("xRange: {}".format(rx))
    # print("xMax: {}".format(xMax))
    # print("xMin: {}".format(xMin))
    print("yRange: {}".format(ry))
    # print("yMax: {}".format(yMax))
    # print("yMin: {}".format(yMin))
    print("Dx, Dy : {}".format((dx,dy)))
    
    diffraction_patterns = [np.reshape(np.loadtxt(i,skiprows=10), (numC, int(ny),int(nx)))[0,:,:] for i in I]  
    # intensities = [i[0,:,:] for i in intensities]
    
    if int(nx) != asize[0]:
        diffraction_patterns = [resize(d, asize, preserve_range=False) for d in diffraction_patterns]
        
    print('New diffraction data shape:   ', np.shape(diffraction_patterns[0]))
    # # Load your probe intensity array (assuming it's still a numpy array; adjust if it's also a TIFF)
    # probe_intensity = tiff.imread(probe_dir)#f'{data_dir}/probe/intensity.tif')  # If probe is a TIFF, use tiff.imread
    
    if inverPositions:
        positions_x = [-a for a in x] #np.linspace(-0.25, 0.25, 3)  # 3 positions in um
        positions_y = [-b for b in y] #np.linspace(-0.25, 0.25, 3)  # 3 positions in um
    else:
        positions_x = [a for a in x] #np.linspace(-0.25, 0.25, 3)  # 3 positions in um
        positions_y = [b for b in y] #np.linspace(-0.25, 0.25, 3)  # 3 positions in um
    energy_ev = 185  #  photon energy in eV
    det_distance_m = 6.52e-3  # detector distance in m
    det_pixelsize_um = dx  # detector pixel size in m
    
    
    if showPositions:
        try:
            print('First position (x,y): ', (x[0],y[0]))
        except:
            x = [_x for _x in x]
            y = [_y for _y in y]
            print('First position (x,y): ', (x[0],y[0]))
        fig, ax = plt.subplots()
        for xx in x:
            for yy in y:
                circle = plt.Circle((xx,yy),probe_size/2,color='red',alpha=0.1,facecolor=None)
                ax.add_patch(circle)
        ax.plot(x,y,':x',label='Sample positions')
        ax.plot(positions_x,positions_y,':x',label='Probe positions')
        ax.set_xlabel('x [m]')
        ax.set_ylabel('y [m]')
        plt.legend()
        plt.show()

    
    # Create the HDF5 file
    create_hdf5_file(f'{save_dir}{saveName}', diffraction_patterns, (positions_x, positions_y), energy_ev, det_distance_m, det_pixelsize_um)

if __name__ == '__main__':
    # test()
    testFromCSV()