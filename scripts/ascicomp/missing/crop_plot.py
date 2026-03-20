#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 15 11:43:27 2025

@author: -
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import tifffile
from matplotlib.colors import LogNorm

import numpy as np
import matplotlib.pyplot as plt

def crop_and_display(images, crop_size, layout=(1,1), center=None, pixel_size=1.0, cmap='viridis',
                     save_path=None, colorbar_label="Intensity", image_labels=None,
                     label_color='white', scalebar_length=100.0, show_scalebar=True,
                     fig_scaling=4, auto_log=True, adjustBC=False,colourbar=False,
                     lineProf=False,analyse=False,convert=False,dwell=1.0):
    """
    Crop and display multiple images in a flexible grid with a shared vertical colorbar.
    Automatic logarithmic normalization is applied if auto_log=True and image dynamic range is high.
    Images with negative values are shifted to ≥ 0 before log scaling.
    Figure size automatically scales with the grid layout.

    Parameters
    ----------
    images : array-like
        List or numpy array of 2D images with shape (n, y, x) or (y, x).
    crop_size : tuple
        Desired crop size in pixels as (crop_y, crop_x).
    layout : tuple
        Tuple of (n_rows, n_cols) specifying the grid layout.
    center : tuple or None
        Center position for cropping as (y, x). If None, the image center is used.
    pixel_size : float
        Size of a pixel in micrometres (µm).
    cmap : str
        Matplotlib colormap for display.
    save_path : str or None
        Path to save the displayed figure.
    colorbar_label : str
        Label for the shared colorbar.
    image_labels : list of str or None
        Optional list of labels for each image.
    label_color : str
        Color for image labels.
    scalebar_length : float
        Real-space length of the scalebar in micrometres (µm).
    show_scalebar : bool
        If True, displays the scalebar on each image.
    fig_scaling : float
        Scaling factor for figure size per image (default 4 inches per image).
    auto_log : bool
        If True, automatically applies log scaling to high dynamic range images.
    """

    # Convert to numpy array and ensure 3D
    images = np.array(images)
    if images.ndim == 2:
        images = images[np.newaxis, :, :]
    n_images, ydim, xdim = images.shape

    n_rows, n_cols = layout
    if n_rows * n_cols < n_images:
        raise ValueError("Layout does not have enough spaces for all images.")

    crop_y, crop_x = crop_size

    if center is None:
        center = (xdim // 2, ydim // 2)
    cx, cy = center

    # Crop boundaries
    y1 = max(cy - crop_y // 2, 0)
    y2 = min(cy + crop_y // 2, ydim)
    x1 = max(cx - crop_x // 2, 0)
    x2 = min(cx + crop_x // 2, xdim)

    cropped_images = [img[y1:y2, x1:x2] for img in images]
    
    if convert:
        HPCE = 3.66
        conversion = 1.27  
        energy = 91
        cropped_images = [i*10000*(pixel_size**2) for i in cropped_images]
        cropped_images = [(i)/(HPCE*conversion*energy*dwell) for i in cropped_images]
        print('Total ph/s in cropped image:')
        print([np.sum(i) for i in cropped_images])
        print([np.min(i) for i in cropped_images])
        print([np.max(i) for i in cropped_images])
    else:        
        print('Total counts in cropped image:')
        print([np.sum(i) for i in cropped_images])

    if analyse:
        import analyse_variation
        analyse_variation.analyse_variation(cropped_images)
    else:
        pass

    # Handle auto_log: shift images to >=0 if negative
    if auto_log:
        for i, img in enumerate(cropped_images):
            min_val = img.min()
            if min_val <= 0:
                cropped_images[i] = img - min_val + 1e-9  # shift and avoid log(0)
    # Coordinate extents in µm
    y_extent = (-(cy - y1) * pixel_size, (y2 - cy) * pixel_size)
    x_extent = (-(cx - x1) * pixel_size, (x2 - cx) * pixel_size)
    extent = [x_extent[0], x_extent[1], y_extent[0], y_extent[1]]

    # Global color limits
    vmin = min(img.min() for img in cropped_images)
    vmax = max(img.max() for img in cropped_images)

    # Determine if log scaling is appropriate
    use_log = auto_log and (vmin > 0) and (vmax / vmin > 100)

    if use_log:
        # Prevent log(0) or negative
        cropped_images = [np.clip(img, 1e-10, None) for img in cropped_images]
        

        print([np.min(i) for i in cropped_images])
        print([np.max(i) for i in cropped_images])
        # Take logarithm
        cropped_images = [np.log(img)  / np.log(10) for img in cropped_images]
        
        cropped_images = [np.clip(img, 1e-10, None) for img in cropped_images]

        print([np.min(i) for i in cropped_images])
        print([np.max(i) for i in cropped_images])
        vmin = min(img.min() for img in cropped_images)
        vmax = max(img.max() for img in cropped_images)
        
        

    print([np.min(i) for i in cropped_images])
    print([np.max(i) for i in cropped_images])
    if adjustBC: 
        vmin, vmax = np.percentile(cropped_images[0], adjustBC)
        # from skimage import exposure

        # Stretch contrast to full range
        # img = exposure.rescale_intensity(img, in_range='image', out_range=(0, 1))
        # img = exposure.equalize_hist(img)
        # plt.imshow(image_rescaled, cmap='gray')
        # plt.colorbar()

    # Auto figure size
    fig_width = fig_scaling * n_cols
    fig_height = fig_scaling * n_rows
    fig, axes = plt.subplots(
        n_rows, n_cols,
        figsize=(fig_width, fig_height),
        sharex=True, sharey=True,
        gridspec_kw={'hspace': 0.0, 'wspace': 0.0}  # remove extra spacing
    )
    axes = np.array(axes).reshape(-1)  # flatten
  
    ims = []
    for i, ax in enumerate(axes):
        if i < n_images:
            ax.set_aspect('auto')  # allow non-square images to fill vertical space
            img = cropped_images[i]
            # if use_log:
                # print('using log scale')
                # im = ax.imshow(img, cmap=cmap, extent=extent, norm=LogNorm(vmin=vmin, vmax=vmax), origin='lower')
            # else:
            im = ax.imshow(img, cmap=cmap, extent=extent, vmin=vmin, vmax=vmax, origin='lower')
            ims.append(im)
            ax.set_xlabel(f"X (\u03bcm)")
            ax.set_ylabel(f"Y (\u03bcm)")

            # Image label
            if image_labels is not None and i < len(image_labels):
                ax.text(0.02, 0.95, image_labels[i], transform=ax.transAxes,
                        color=label_color, fontsize=12, fontweight='bold',
                        va='top', ha='left', bbox=dict(facecolor='black', alpha=0.3, edgecolor='none'))

            # Scalebar
            if show_scalebar and scalebar_length > 0:
                ax.axis('off')
                x_min, x_max = x_extent
                y_min, y_max = y_extent
                bar_x = x_max - scalebar_length * 1.5
                bar_y = y_min + (y_max - y_min) * 0.05
                bar_height = (y_max - y_min) * 0.015
                ax.add_patch(Rectangle(
                    (bar_x, bar_y), scalebar_length, bar_height,
                    facecolor='white', edgecolor='black', lw=0.5
                ))
                ax.text(bar_x + scalebar_length / 2, bar_y + bar_height * 2,
                        f"{int(scalebar_length)} µm",
                        color='white', ha='center', va='bottom', fontsize=10, fontweight='bold')
        else:
            ax.axis('off')

    if colourbar:
        # Shared vertical colorbar
        fig.subplots_adjust(right=0.85)
        cbar_ax = fig.add_axes([0.99, 0.44, 0.05, 0.12])
        cbar = fig.colorbar(ims[0], cax=cbar_ax)
        cbar.set_label(colorbar_label)

    plt.tight_layout()#rect=[0, 0, 0.85, 1])

    if save_path is not None:
        fig.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Figure saved to: {save_path}")

    plt.show()


if __name__ == '__main__':
    
    date = '28'
    dir_path = f"/data/xfm/22353/HERMES/data/UP_20242172/2025-09-{date}/"
    nums = ['40'] 
    scan_nums =  [f"202509{date}_0{n}" for n in nums]#['09']]#,'26']]#,24,25,29,30,31,26,27,28]] 
                 # [23,24,25,29,30,31,26,27,28]]#range(23,32)]# range(23,32)]
    # ['20250927_009']
    # [f"20250927_0{n}" for n in [25,31,28]] 
                 # [23,24,25,29,30,31,26,27,28]]#range(23,32)]# range(23,32)]
    h5file = '/user/home/ptypy-0.5.0/jk/experiments/SOLEIL_telePtycho_91/Image_20250928_040standardized_5/dumps/recon_28_40_large_5/recon_28_40_large_5_DM_0130_propz1120.ptyr'
    
    import h5py
    f = h5py.File(h5file,'r')
    
    imgs = [np.abs(f["my_array"][:])**2]
    
    print(np.shape(imgs[0]))
    # [np.flipud(tifffile.imread(f"{dir_path}Time_{n}_processed.tif")) for n in scan_nums] 
    # imgs = np.log(imgs / np.max([i.max() for i in imgs]))
    
    # plt.imshow(imgs[0],aspect='auto')
    # plt.colorbar()
    # plt.show()
    # print(np.max(imgs))
    # print([np.max(i) for i in imgs])
    # imgs = [i / np.max(imgs) for i in imgs]
    # # print(np.shape(imgs))
    
    
    labels = [None]
    # ['G3: small SLH #1', 'G3: small SLH #2', 'G3: smal SLV']
    labels = [ ''
                # "G3: small SLH #1", "G3: small SLH #2", "G3: small SLV",
                # "G1: small SLH #1", "G2: small SLH #1", "G3: small SLH #1",
                # "G1: small SLH #2", "G2: small SLH #2", "G3: small SLH #2",
                # "G1: small SLV", "G2: small SLV", "G3: small SLV",
              ]



    crop_and_display(
                      imgs,
                      crop_size=(3000, 10000),#1600),
                      center= (np.shape(imgs[0])[1]//2,np.shape(imgs[0])[0]//2), 
                      # (476,790), # zero order
                      # (800,800), # zero order
                      # (476,790), # left order
                      # (1125,810),# right order
                      layout=(1,1),
                      pixel_size=11.0,
                      cmap='gray',
                      # 'nipy_spectral',
                      #'rainbow',
                      #'coolwarm',#'viridis',#'gray',
                      colorbar_label="[log$_{10}$(ph/s)]",##"Signal (a.u.)",
                      image_labels=labels,
                      label_color='white',
                      scalebar_length=1000.0,    # 100 µm scale bar
                      show_scalebar=True,
                      # save_path=f"{dir_path}_farfield_both.svg",
                       # None,#"farfield_grating_SLV.png",
                      # fig_scaling=10,
                      # adjustBC=(68,100),
                       # (70,100),#(78.33,100),
                      colourbar=True,
                      analyse=False,
                      # convert=True,
                        # auto_log=False
                      )
    
    