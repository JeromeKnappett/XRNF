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
from tqdm import tqdm
from tifffile import imread
from usefulWavefield_old import EtoWL



def reconstructedResolution(wl,Zsd,N,px):
    dXs = (wl * Zsd) / (N * px)
    return dXs

def center_crop(image, target_shape):
    """Crop the center of the image to match target_shape."""
    y, x = image.shape
    target_y, target_x = target_shape

    startx = x // 2 - target_x // 2
    starty = y // 2 - target_y // 2

    return image[starty:starty + target_y, startx:startx + target_x]

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

def scanFromCSV(path,xc,yc,zc,Ic,Iname,num='all'):    
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
        data = pd.read_csv(path, usecols=[xc,yc,zc,Ic])
        if num == 'all':
            x_pos = data[xc]
            y_pos = data[yc]
            z = data[zc]
            Ifiles = [f'{c}{Iname}' for c in data[Ic]]
        else:
            try:
                x_pos = data[xc][0:num]
                y_pos = data[yc][0:num]
                z = data[zc][0:num]
                Ifiles = [f'{c}{Iname}' for c in data[Ic][0:num]]
            except:
                x_pos = data[xc][num[0]:num[1]]
                y_pos = data[yc][num[0]:num[1]]
                z = data[zc][0:num]
                Ifiles = [f'{c}{Iname}' for c in data[Ic][num[0]:num[1]]]
                
        print(Ifiles[0:2])
        return x_pos,y_pos,z,Ifiles
    except FileNotFoundError:
        print("The specified file was not found.")
    except pd.errors.EmptyDataError:
        print("The file is empty.")
    except pd.errors.ParserError:
        print("There was an error parsing the file.")
    except ValueError as e:
        print(f"Error: {e}")

        
def test():
    data_dir = '/user/home/opt/xl/xl/experiments/SOLEIL_telePtycho_92/data/5x5_twopins/'  # Update this with the path to your files
    probe_dir = '/user/home/opt/xl/xl/experiments/SOLEIL_telePtycho_92/data/5x5_twopins/'# '/user/home/opt/xl/xl/experiments/XFM_ptycho/data/phaseSpace/samplePinhole_in/intensity.tif'
    
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
    data_dir = '/user/home/opt/xl/xl/experiments/SOLEIL_telePtycho_92/' 
    # '/user/home/opt/xl/xl/experiments/XFM_teleptycho/' 
    # '/user/home/opt/xl/xl/experiments/XFM_ptycho/' # Update this with the path to your files
    # probe_dir = '/user/home/opt/xl/xl/experiments/XFM_ptycho/data/phaseSpace/samplePinhole_in/intensity.tif'
    # '/user/home/opt/xl/xl/experiments/XFM_teleptycho/data/testPhaseSpace/atPinhole/intensity.tif'
    # '/user/home/opt/xl/xl/experiments/XFM_ptycho/data/phaseSpace/samplePinhole_in/intensity.tif'
    save_dir = data_dir#'/user/home/ptypy-0.5.0/jk/experiments/SOLEIL_ptycho/'
    scan_name = '13x15_20um_highT'
    # '5x5_test'
    # 'test_scan_4um_longZ'
     # 'SOLEIL_test_4um_z2_256.h5'
    # 'SOLEIL_5x5_twopins_128.h5'
    # 

    showPositions = True
    invertX = False # for when positions are in reference to sample instead of probe
    invertY = True
    IfromTIFFS = True
    pad = 448#//2
    probe_size = 20.0e-6
    asize =  (1600,1600)
    # (2048,2048)
    # (1600,1600)
    # (512,512)
    #(128,128)#(256,256)

    energy_ev = 91  #  photon energy in eV
    # det_distance_m = 0.014772043724554977 # detector distance in m
    
    if pad:
        saveName = f"SOLEIL_{scan_name}_{int(asize[0])}_pad{pad}.h5"
    else:
        saveName = f"SOLEIL_{scan_name}_{int(asize[0])}.h5"
    # 'SOLEIL_test_4um_256.h5'
    
    # Load scan info from CSV
    x, y, z, I = scanFromCSV(
        f"{data_dir}{scan_name}.csv",
        xc='op_pinhole_x',
        yc='op_pinhole_y',
        zc='op_prop2detector_L',
        Ic='fdir',
        Iname='IntensityDist_SE.dat',
        num='all'
    )

    print("Loaded scan positions:", len(I))
    print("First .dat path:", I[0])
    
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
    
    print("Detector size (x,y): {}".format((nx,ny)))
    print("xRange: {}".format(rx))
    # print("xMax: {}".format(xMax))
    # print("xMin: {}".format(xMin))
    print("yRange: {}".format(ry))
    # print("yMax: {}".format(yMax))
    # print("yMin: {}".format(yMin))
    print("Dx, Dy : {}".format((dx,dy)))
    
    if IfromTIFFS:
        # --- Load TIFFs instead of .dat diffraction data ---
        diffraction_patterns = []
        print(f"Loading {len(I)} TIFF files...")
        for dat_path in tqdm(I, desc="Loading TIFFs", unit="file"):
            base_dir = os.path.dirname(dat_path)
            folder_name = os.path.basename(base_dir)
            tif_path = f"{base_dir}/{folder_name}intensity.tif" #os.path.join(base_dir, f"{folder_name}.tif")
        
            if not os.path.exists(tif_path):
                raise FileNotFoundError(f"TIFF file not found: {tif_path}")
        
            img = imread(tif_path)
        
            # Crop if needed
            if img.shape != asize:
                if pad:
                    _asize = (asize[0]-pad, asize[1]-pad)
                    img = center_crop(img, _asize)
                    img = np.pad(img, (pad,pad))
                else:
                    img = center_crop(img, asize)
        
            diffraction_patterns.append(img)
    else:
        diffraction_patterns = []
        for i in tqdm(I, desc="Loading and reshaping .dat files", unit="file"):
            img = [np.reshape(np.loadtxt(i,skiprows=10), (1, int(ny),int(nx)))[0,:,:] for i in I]  
            if int(nx) != asize[0]:
                img = center_crop(img, asize)#[resize(d, asize, preserve_range=False) for d in diffraction_patterns]
            diffraction_patterns.append(img)

    # --- Visual check ---
    fig, ax = plt.subplots(1, 2)
    ax[0].imshow(diffraction_patterns[0], cmap='gray')
    ax[0].set_title('Scan #1')
    ax[1].imshow(np.log1p(diffraction_patterns[0]), cmap='gray')
    ax[1].set_title('Scan #1 (log)')
    plt.tight_layout()
    plt.show()

    print('Final diffraction shape:', diffraction_patterns[0].shape)
    print(f"Resolution of reconstruction: {1e9*reconstructedResolution(EtoWL(energy_ev),z[0],asize[0],dx)} nm")
    # --- Process positions ---
    positions_x = [-a if invertX else a for a in x]
    positions_y = [-b if invertY else b for b in y]

    det_pixelsize_um = dx  # assuming square pixels

    if showPositions:
        # print('First position (x, y):', (positions_x[0], positions_y[0]))
        fig, ax = plt.subplots()
        for xx, yy in zip(positions_x, positions_y):
            circle = plt.Circle((xx, yy), probe_size / 2, color='red', alpha=0.1)
            ax.add_patch(circle)
        ax.plot(positions_x, positions_y, ':x', label='Probe positions')
        ax.set_xlabel('x [m]')
        ax.set_ylabel('y [m]')
        plt.legend()
        plt.show()

    # --- Save to HDF5 ---
    create_hdf5_file(
        os.path.join(save_dir, saveName),
        diffraction_patterns,
        (positions_x, positions_y),
        energy_ev,
        z[0],
        det_pixelsize_um
    )
    print(f"H5 file saved to:    {os.path.join(save_dir, saveName)}")
    
    

if __name__ == '__main__':
    # test()
    testFromCSV()