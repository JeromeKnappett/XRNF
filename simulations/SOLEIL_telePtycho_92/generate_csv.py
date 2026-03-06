#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 09:29:10 2024

@author: -
"""

import csv
import numpy as np
# import usefulWavefield_old as UW
import matplotlib.pyplot as plt
showPositions = True

scan_name = '13x15_20um'
# '5x5_twopins'
# '5x5_twopins'
# 'test_scan_4um_longZ'

output_csv_file = f"/user/home/opt/xl/xl/experiments/SOLEIL_telePtycho_92/{scan_name}.csv"
# 5x5_twopins_z2.csv'
#5x5_twopins.csv'

# Base file location path (modify as needed)
base_file_location = f"/user/home/opt/xl/xl/experiments/SOLEIL_telePtycho_92/data/{scan_name}/"
# 5x5_twopins_z2/'
#5x5_twopins/'

titles = ['name','fdir','op_pinhole_x','op_pinhole_y','op_prop2pinhole_L','op_prop2detector_L']
# ['name','fdir','op_prop2pinhole_L','op_Sample_xc','op_Sample_yc','op_SampleBalls_xc','op_SampleBalls_yc']

dx,dy =1.996037395959178e-09, 3.4653742299792975e-07

dz = 0.0
# -80.0e-6

z_pin =  0.0007322594383165418
#0.0011187746837473512 + dz
z_det = [0.05447438735576681 - z_pin]
# [0.014772043724554977-dz] # aerial image - 200nm pitch - longZ
# [0.014770043724554977] # aerial image - 200nm pitch - z2
# [0.014772043724554977] # aerial image - 200nm pitch - z1
# [1] #[0.01,0.012]

ap_size = 20.0e-6
overlap = 0.90
Nx, Ny = 13,15 #14,14
# Define scanning parameters
# x_step =26*dx # Step size in x direction
x_step_n = int(((1-overlap)*ap_size) / dx)
x_step = x_step_n * dx
xmin = -(Nx//2)*x_step   # Minimum x position
xmax = (Nx//2)*x_step    # Maximum x position


y_step_n = int(((1-overlap)*ap_size) / dy)
y_step = y_step_n * dy
ymin = -(Ny//2)*y_step   # Minimum y position
ymax = (Ny//2)*y_step    # Maximum y position


# Generate x and y positions
x_positions = np.arange(xmin, xmax + x_step, x_step)
y_positions = np.arange(ymin, ymax + y_step, y_step)
# print(x_positions)
print(f"Scan size (x,y):           {(Nx*x_step, Ny*y_step)}")
print(f"Step size (x,y):           {(x_step, y_step)}")
print(f"Number of positions (x,y): {(len(x_positions),len(y_positions))}")
print(f"Total number of positions: {len(x_positions)*len(y_positions)}")
print(f"First position (x,y):      {(x_positions[0], y_positions[0])}")

# fig, ax = plt.subplots()   
# Open CSV file for writing
with open(output_csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write header with additional columns
    writer.writerow(titles)#['x', 'y', 'file_location', 'position_name'])  

    for i,z in enumerate(z_det):
        # Generate scanning pattern
        for ii,y in enumerate(y_positions):
            for iii,x in enumerate(x_positions):
                # Define file location and position name strings
                file_location = f"{base_file_location}pos_z{i}_x{iii}_y{ii}/"
                position_name = f"pos_z{i}_x{iii}_y{ii}"
                
                # if abs(x) < 9.0e-9:
                #     x = 0.0
                # else:
                #     x = UW.round_sig(x,3)            
                
                # if abs(y) < 9.0e-9:
                #     y = 0.0
                # else:
                #     y = UW.round_sig(y,3)      
                # Write row to CSV file
                writer.writerow([position_name, file_location, x, y, z_pin, z])
                
                # ax.plot(x,y,':x')#,label='Sample positions')np.deg2rad(15))

print(f"CSV file written to: {output_csv_file}")
if showPositions:
    fig, ax = plt.subplots()
    for xx in x_positions:
        for yy in y_positions:
            circle = plt.Circle((xx, yy), ap_size / 2, color='red', alpha=0.1)
            ax.add_patch(circle)
            ax.plot(xx, yy, ':x',color='black')
    aperture = plt.Circle((0,0), ap_size / 2, ls=':', edgecolor='black', facecolor='red', alpha = 1.0)
    ax.add_patch(aperture)
    ax.set_xlabel('x [m]')
    ax.set_ylabel('y [m]')
    plt.legend()
    plt.show()
        

