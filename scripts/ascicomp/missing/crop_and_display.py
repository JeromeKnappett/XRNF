#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 17 14:56:50 2025

@author: -
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib import gridspec
from mpl_toolkits.axes_grid1 import make_axes_locatable

def crop_and_display(images, crop_size, layout=(1,1), center=None, pixel_size=1.0, cmap='viridis',
                     save_path=None, colorbar_label="Intensity", image_labels=None,
                     label_color='white', scalebar_length=100.0, show_scalebar=True,
                     fig_scaling=4, auto_log=True, adjustBC=False, colourbar=False,
                     lineProf=False):
    """
    Crop and display multiple images in a flexible grid with optional line profiles.
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

    if auto_log:
        for i, img in enumerate(cropped_images):
            min_val = img.min()
            if min_val <= 0:
                cropped_images[i] = img - min_val + 1e-9  # shift and avoid log(0)

    y_extent = (-(cy - y1) * pixel_size, (y2 - cy) * pixel_size)
    x_extent = (-(cx - x1) * pixel_size, (x2 - cx) * pixel_size)
    extent = [x_extent[0], x_extent[1], y_extent[0], y_extent[1]]

    # Global color limits
    vmin = min(img.min() for img in cropped_images)
    vmax = max(img.max() for img in cropped_images)

    # Log scaling if needed
    use_log = auto_log and (vmin > 0) and (vmax / vmin > 100)
    if use_log:
        cropped_images = [np.clip(img, 5e-2, None) for img in cropped_images]
        cropped_images = [np.log(img) / np.log(10) for img in cropped_images]
        vmin = min(img.min() for img in cropped_images)
        vmax = max(img.max() for img in cropped_images)

    if adjustBC: 
        vmin, vmax = np.percentile(cropped_images[0], adjustBC)

    # === Start Figure ===
    fig_width = fig_scaling * n_cols
    fig_height = fig_scaling * n_rows
    fig = plt.figure(figsize=(fig_width, fig_height))

    outer_gs = gridspec.GridSpec(n_rows, n_cols, wspace=0.0, hspace=0.0)
    ims = []

    for idx in range(n_rows * n_cols):
        if idx >= n_images:
            continue

        img = cropped_images[idx]
        row = idx // n_cols
        col = idx % n_cols

        if lineProf:
            # Create nested GridSpec for each image+profiles
            gs_cell = gridspec.GridSpecFromSubplotSpec(2, 2, width_ratios=[4, 1.2], height_ratios=[4, 1.2],
                                                       subplot_spec=outer_gs[row, col], wspace=0.0, hspace=0.0)
            ax_img = fig.add_subplot(gs_cell[0, 0])
            # ax_yprof = fig.add_subplot(gs_cell[0, 1], sharey=ax_img)
            # ax_xprof = fig.add_subplot(gs_cell[1, 0], sharex=ax_img)
            
            # Inside the loop, after ax_img is defined:
            divider = make_axes_locatable(ax_img)
            if lineProf == 'y' or lineProf == 'both':
                ax_yprof = divider.append_axes("right", size="20%", pad=0.1, sharey=ax_img)  # =' sharey fixes vertical scaling
                # Turn off tick labels to prevent overlap
                plt.setp(ax_yprof.get_yticklabels(), visible=False)
            if lineProf == 'x' or lineProf == 'both':
                ax_xprof = divider.append_axes("bottom", size="20%", pad=0.1, sharex=ax_img)  # Already aligned
                # Turn off tick labels to prevent overlap
                plt.setp(ax_xprof.get_xticklabels(), visible=False)
        else:
            # Single axis per image
            ax_img = fig.add_subplot(outer_gs[row, col])

        # --- Plot image ---
        im = ax_img.imshow(img, cmap=cmap, extent=extent, origin='lower', vmin=vmin, vmax=vmax)
        ims.append(im)

        if image_labels is not None and idx < len(image_labels) and type(image_labels)==list:
            ax_img.text(0.02, 0.95, image_labels[idx], transform=ax_img.transAxes,
                        color=label_color, fontsize=12, fontweight='bold',
                        va='top', ha='left', bbox=dict(facecolor='black', alpha=0.3, edgecolor='none'))
        elif type(image_labels)==str:
            ax_img.text(0.02, 0.95, image_labels, transform=ax_img.transAxes,
                        color=label_color, fontsize=12, fontweight='bold',
                        va='top', ha='left', bbox=dict(facecolor='black', alpha=0.3, edgecolor='none'))
            

        if show_scalebar and scalebar_length > 0:
            ax_img.axis('off')
            x_min, x_max = x_extent
            y_min, y_max = y_extent
            bar_x = x_max - scalebar_length * 2.0
            bar_y = y_min + (y_max - y_min) * 0.05
            bar_height = (y_max - y_min) * 0.015
            ax_img.add_patch(Rectangle(
                (bar_x, bar_y), scalebar_length, bar_height,
                facecolor='white', edgecolor='black', lw=0.5
            ))
            ax_img.text(bar_x + scalebar_length / 2, bar_y + bar_height * 2,
                        f"{int(scalebar_length)} µm",
                        color='white', ha='center', va='bottom', fontsize=10, fontweight='bold')

        ax_img.set_xlabel("X (µm)")
        ax_img.set_ylabel("Y (µm)")

        # --- Plot profiles ---
        if lineProf:
            # X and Y coordinates
            x = np.linspace(x_extent[0], x_extent[1], img.shape[1])
            y = np.linspace(y_extent[0], y_extent[1], img.shape[0])
            center_x = img.shape[1] // 2
            center_y = img.shape[0] // 2
            Ix = img[center_y, :]
            Iy = img[:, center_x]
        
            if lineProf == 'x' or lineProf == 'both':
                # --- Horizontal profile (bottom) ---
                ax_xprof.plot(x, Ix, color='tab:blue')
                ax_xprof.set_xlim(x_extent)
                ax_xprof.set_ylim(-0.1, np.max(Ix)*1.1)
                # ax_xprof.set_ylabel("Counts")
                ax_xprof.set_xlabel("$x$-profile ($y=0$) [µm]")
                # ax_xprof.set_xticks([])
                ax_xprof.yaxis.tick_right()
                ax_xprof.yaxis.set_label_position("right")
                # ax_xprof.set_yticks([0, 0.5, 1])
                # ax_xprof.set_yticklabels(["0", "0.5", "1"])
                # ax_xprof.tick_params(axis='x', labelrotation=45)
                if lineProf == 'x':                    
                    ax_xprof.set_ylabel("Counts \n(log)")

            if lineProf == 'y' or lineProf == 'both':
                # --- Vertical profile (right) ---
                ax_yprof.plot(Iy, y, color='tab:red')
                ax_yprof.set_ylim(y_extent)
                ax_yprof.set_xlim(-0.1, np.max(Iy)*1.1)
                ax_yprof.set_xlabel("            Counts \n        (log)")
                ax_yprof.set_ylabel("$y$-profile ($x=0$) [µm]")
                # ax_yprof.set_yticks([])
                ax_yprof.yaxis.tick_right()
                ax_yprof.yaxis.set_label_position("right")
                # ax_yprof.set_xticks([0, 0.5, 1])
                ax_yprof.invert_xaxis()
                ax_xprof.tick_params(labelbottom=True)
                # # Optional: clean up tick label density
                # ax_xprof.xaxis.set_tick_params(labelsize=8)
                # ax_yprof.yaxis.set_tick_params(labelsize=8)


            # ax_xprof.set_yticklabels([])
            # ax_yprof.set_xticklabels([])

    # --- Shared colorbar ---
    if colourbar and ims:
        cbar_ax = fig.add_axes([0.99, 0.44, 0.05, 0.12])
        cbar = fig.colorbar(ims[0], cax=cbar_ax)
        cbar.set_label(colorbar_label)

    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Figure saved to: {save_path}")

    plt.show()
    
if __name__ == '__main__':
    import tifffile
    dir_path = '/data/xfm/22353/HERMES/data/UP_20242172/2025-09-27/'
    scan_nums = [f"20250927_0{n}" for n in range(23,32)]
                 # [25,31,28]] 
                 # [23,24,25,29,30,31,26,27,28]]#range(23,32)]# range(23,32)]
    imgs = [tifffile.imread(f"{dir_path}Time_{n}_processed.tif") for n in scan_nums] 
    # imgs = np.log(imgs / np.max([i.max() for i in imgs]))
    
    scan_nums = ['20250927_031']
    # [f"20250927_0{n}" for n in [25,31,28]] 
                 # [23,24,25,29,30,31,26,27,28]]#range(23,32)]# range(23,32)]
    imgs = [tifffile.imread(f"{dir_path}Time_{n}_processed.tif") for n in scan_nums] 
    # plt.imshow(imgs[0],aspect='auto')
    # plt.colorbar()
    # plt.show()
    # print(np.max(imgs))
    # print([np.max(i) for i in imgs])
    # imgs = [i / np.max(imgs) for i in imgs]
    # # print(np.shape(imgs))
    
    
    # labels = ['G3: small SLH #1', 'G3: small SLH #2', 'G3: smal SLV']
    labels = ["G1: small SLH #1", "G2: small SLH #1", "G3: small SLH #1",
              "G1: small SLV", "G2: small SLV", "G3: small SLV",
              "G1: small SLH #2", "G2: small SLH #2", "G3: small SLH #2"
              ]
    
    cen = [(800,800),(478,810),(1123,790)]
    imglabels = ["G1_smallSLH1", "G2_smallSLH1", "G3_smallSLH1",
                 "G1_smallSLV", "G2_smallSLV", "G3_smallSLV",
                 "G1_smallSLH2", "G2_smallSLH2", "G3_smallSLH2"]
    
    Glabels = ['G1', 'G2', 'G3','G1', 'G2', 'G3','G1', 'G2', 'G3']
    Clabels = ['smallSLH1','smallSLH1','smallSLH1','smallSLV','smallSLH2']
    Olabels = ['zero','left','right']
    
    BClims = [(60,100)]

    # for i,im in enumerate(imgs):
    #     for c, order in zip(cen,Olabels):
    #         print(i)
    #         print(labels[i])
    #         label=labels[i]
    #         print(label)
    #         crop_and_display(
    #                           im,
    #                           crop_size=(200, 200),
    #                           center=c,
    #                           layout=(1,1),
    #                           pixel_size=11.0,
    #                           cmap='gray',
    #                           colorbar_label="Signal (a.u.)",
    #                           image_labels=label,
    #                           label_color='white',
    #                           scalebar_length=200.0,    # 100 µm scale bar
    #                           show_scalebar=True,
    #                            save_path=f"{dir_path}figures/{imglabels[i]}_{order}_order.png",
    #                           # None,#"farfield_grating_SLV.png",
    #                           fig_scaling=5,
    #                           # adjustBC=(78,100),
    #                            # (70,100),#(78.33,100),
    #                           colourbar=False,
    #                           lineProf=True
    #                           )
    crop_and_display(
                      imgs,
                      crop_size=(200, 1600),
                      center=(800,800),# right order
                      # (800,800), # zero order
                      # (476,810), # left order
                      # (1125,790),# right order
                      layout=(1,1),
                      pixel_size=11.0,
                      cmap='gray',
                      # 'nipy_spectral',
                      #'rainbow',
                      #'coolwarm',#'viridis',#'gray',
                      colorbar_label="Signal (a.u.)",
                      image_labels=None,#labels,
                      label_color='white',
                      scalebar_length=1000.0,    # 100 µm scale bar
                      show_scalebar=True,
                        save_path=f"{dir_path}farfield_pinhole_wCB.pdf",
                      # G3_right_orders.png",
                      # None,#"farfield_grating_SLV.png",
                      fig_scaling=10,
                      # adjustBC=(35,100),
                        # (70,100),#(78.33,100),
                      colourbar=True,
                      lineProf=None,#'x'
                      # auto_log=False
                      )