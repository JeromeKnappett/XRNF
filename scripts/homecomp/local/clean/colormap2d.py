#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 13:43:49 2022

@author: jerome
"""
import matplotlib.pyplot as plt
import numpy as np
class ColorMap2D():
    def __init__(self, filename, transpose=False, reverse_x=False, reverse_y=False, xclip=None, yclip=None):
        """
        Maps two 2D array to an RGB color space based on a given reference image.
        Args:
            filename (str): reference image to read the x-y colors from
            rotate (bool): if True, transpose the reference image (swap x and y axes)
            reverse_x (bool): if True, reverse the x scale on the reference
            reverse_y (bool): if True, reverse the y scale on the reference
            xclip (tuple): clip the image to this portion on the x scale; (0,1) is the whole image
            yclip  (tuple): clip the image to this portion on the y scale; (0,1) is the whole image
        """
        self._colormap_file = filename or COLORMAP_FILE
        self._img = plt.imread(self._colormap_file)
        if transpose:
            self._img = self._img.transpose()
        if reverse_x:
            self._img = self._img[::-1,:,:]
        if reverse_y:
            self._img = self._img[:,::-1,:]
        if xclip is not None:
            imin, imax = map(lambda x: int(self._img.shape[0] * x), xclip)
            self._img = self._img[imin:imax,:,:]
        if yclip is not None:
            imin, imax = map(lambda x: int(self._img.shape[1] * x), yclip)
            self._img = self._img[:,imin:imax,:]
        if issubclass(self._img.dtype.type, np.integer):
            self._img = self._img / 255.0

        self._width = len(self._img)
        self._height = len(self._img[0])

        self._range_x = (0, 1)
        self._range_y = (0, 1)


    def __call__(self, val_x, val_y):
        """
        Take val_x and val_y, and associate the RGB values 
        from the reference picture to each item. val_x and val_y 
        must have the same shape.
        """
        if val_x.shape != val_y.shape:
            pass
            # raise ValueError(f'x and y array must have the same shape, but have {val_x.shape} and {val_y.shape}.')
        self._range_x = (np.amin(val_x), np.amax(val_x))
        self._range_y = (np.amin(val_y), np.amax(val_y))
        # i_xy = np.stack((x_indices, y_indices), axis=-1)
        rgb = np.zeros((np.shape(val_x)[0], 3))
        # for indices in np.ndindex(val_x.shape):
        #     img_indices = tuple(i_xy[indices])
        #     rgb[indices] = self._img[img_indices]
        return rgb

    def generate_cbar(self, nx=100, ny=100):
        "generate an image that can be used as a 2D colorbar"
        x = np.linspace(0, 1, nx)
        y = np.linspace(0, 1, ny)
        return self.__call__(*np.meshgrid(x, y))

