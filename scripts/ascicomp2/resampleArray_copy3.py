#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  2 10:05:02 2025

@author: -
"""

import numpy as np
from scipy.ndimage import zoom

def resample_2d_array(array, input_res, target_res):
    """
    Resamples a 2D array based on real-world resolution in meters.

    Parameters:
        array (np.ndarray): Input 2D array of shape (H, W).
        input_res (tuple): Current resolution (y_res, x_res) in meters per pixel.
        target_res (tuple): Desired resolution (y_res, x_res) in meters per pixel.

    Returns:
        np.ndarray: Resampled 2D array with resolution approximately matching target_res.
    """
    if len(array.shape) != 2:
        raise ValueError("Input array must be 2D.")
    if not all(isinstance(r, (int, float)) for r in input_res + target_res):
        raise ValueError("Resolutions must be numbers.")

    input_height, input_width = array.shape
    input_y_res, input_x_res = input_res
    target_y_res, target_x_res = target_res

    # Calculate the size in meters
    height_m = input_height * input_y_res
    width_m = input_width * input_x_res

    # Calculate the new shape in pixels
    new_height = int(round(height_m / target_y_res))
    new_width = int(round(width_m / target_x_res))

    zoom_factors = (
        new_height / input_height,
        new_width / input_width
    )

    resampled_array = zoom(array, zoom_factors, order=1)  # bilinear interpolation

    return resampled_array