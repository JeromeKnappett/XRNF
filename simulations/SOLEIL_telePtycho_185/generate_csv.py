#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 09:29:10 2024

@author: -
"""

import csv
import numpy as np
import usefulWavefield_old as UW
import matplotlib.pyplot as plt

output_csv_file = '/user/home/opt_cmd/xl/xl/experiments/SOLEIL_telePtycho/5x5_twopins.csv'
titles = ['name','fdir','op_pinhole_x','op_pinhole_y']
# ['name','fdir','op_prop2pinhole_L','op_Sample_xc','op_Sample_yc','op_SampleBalls_xc','op_SampleBalls_yc']

dx,dy = 6.598205942093138e-10, 7.956005531338945e-08  # 2 PINHOLES

z_pos = [1] #[0.01,0.012]

ap_size = 4.0e-6
overlap = 0.90
Nx, Ny = 5,5 #14,14
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

# Base file location path (modify as needed)
base_file_location = '/user/home/opt_cmd/xl/xl/experiments/SOLEIL_telePtycho/data/5x5_twopins/'

# Generate x and y positions
x_positions = np.arange(xmin, xmax + x_step, x_step)
y_positions = np.arange(ymin, ymax + y_step, y_step)
# print(x_positions)
print("Number of positions: ", len(x_positions)*len(y_positions))

# fig, ax = plt.subplots()   
# Open CSV file for writing
with open(output_csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write header with additional columns
    writer.writerow(titles)#['x', 'y', 'file_location', 'position_name'])  

    for i,z in enumerate(z_pos):
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
                writer.writerow([position_name, file_location, x, y])
                
                # ax.plot(x,y,':x')#,label='Sample positions')np.deg2rad(15))
                    
# ax.plot(x_positions,y_positions,':x',label='Probe positions')
# ax.set_xlabel('x [m]')
# ax.set_ylabel('y [m]')
# # plt.legend()
# plt.show()
            

