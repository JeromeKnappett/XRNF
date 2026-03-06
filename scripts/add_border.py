#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 10 14:04:12 2025

@author: -
"""

import tifffile as tiff
import numpy as np

def add_white_border(input_path, output_path, border_thickness,rotate=False):
    # Open the image
    image = tiff.imread(input_path)
    if rotate:
        image = np.rot90(image)
    
    # Get image dimensions
    height, width = image.shape[:2]
    
    # Create new image with border
    new_height = height + 2 * border_thickness
    new_width = width + 2 * border_thickness
    
    if image.ndim == 2:
        bordered_image = np.full((new_height, new_width), 255, dtype=image.dtype)  # Grayscale
    else:
        bordered_image = np.full((new_height, new_width, image.shape[2]), 255, dtype=image.dtype)  # RGB or RGBA
    
    # Insert original image into the center
    bordered_image[border_thickness:border_thickness+height, border_thickness:border_thickness+width] = image
    
    # Save the new image
    tiff.imwrite(output_path, bordered_image)

# Example usage
# input_image = '/user/home/opt/xl/xl/experiments/CDSAXS/masks/50p/largeCsingle_20000000.00000_2.00000_200.00000_mask.tif'  # Change to your input file path
# output_image = '/user/home/opt/xl/xl/experiments/CDSAXS/masks/50p/largeCsingle_20000000.00000_2.00000_200.00000_mask_withBorder.tif'  # Change to your desired output file path
border_size = 10  # Change to your desired border thickness in pixels

# add_white_border(input_image, output_image, border_size)

dirPath = '/user/home/opt/xl/xl/experiments/CDSAXS2/masks/'
C = [10,20,30,40,50]
R = [30,40,50,60,70,80,100,150,200,250,300,350,400,450,500]

# name = '/largeCsingle_vert_mask.tif'
# mask = dirPath + name
# savePath = dirPath + name[0:-4] + '_withBorder.tif'
# add_white_border(mask, savePath, border_size, rotate=True)

for c in C:
    for r in R:
        mask = dirPath + 'largeCsingle_20000000.00000_' + str(c) + '.00000_' + str(r) + '.00000_mask.tif'
        savePath = dirPath + 'largeCsingle_20000000.00000_' + str(c) + '.00000_' + str(r) + '.00000_mask_withBorder.tif'
        try:
            add_white_border(mask, savePath, border_size, rotate=True)
        except:
            print(mask + '... not found')
            