#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 13:33:20 2025

@author: -
"""
import numpy as np
import matplotlib.pyplot as plt

#!/usr/bin/env python3

import numpy as np

def generate_uncorrelated_2d_surface(
    rms, size_x, size_y, nx, ny,
    filename="height_profile_matrix.dat",
    plot=False
):
    """
    Generate a 2D uncorrelated height profile and save it to a .dat file 
    in a matrix-style format with each column tab-delimited and each row
    on a new line:
    
      0    y0       y1       y2     ... y_(ny-1)
      x0   h00      h01      h02    ... h0(ny-1)
      x1   h10      h11      h12    ... h1(ny-1)
      ...
      x_(nx-1) ...
    
    Parameters
    ----------
    rms : float
        Desired RMS roughness (standard deviation of heights).
    size_x : float
        Physical size in the x-direction.
    size_y : float
        Physical size in the y-direction.
    nx : int
        Number of points (pixels) along the x-direction.
    ny : int
        Number of points (pixels) along the y-direction.
    filename : str
        Output .dat file name.
    plot : bool
        If True, display the height map using matplotlib.
    """

    # Generate x and y coordinates
    x_vals = np.linspace(-size_x/2, size_x/2, nx)  # shape = (nx,)
    y_vals = np.linspace(-size_y/2, size_y/2, ny)  # shape = (ny,)

    # Generate random heights with mean=0 and std=rms
    # heights[i, j] = height at x_i, y_j
    heights = np.random.normal(loc=0.0, scale=rms, size=(nx, ny))

    # Write to .dat file in the requested format
    with open(filename, "w") as f:
        # First row: 0 followed by y-coordinates
        first_row = ["0"] + [f"{y_vals[j]}" for j in range(ny)]
        f.write("\t".join(first_row) + "\n")

        # Subsequent rows: the first value is x-coordinate, then height values
        for i in range(nx):
            row_data = [f"{x_vals[i]}"] + [f"{heights[i, j]}" for j in range(ny)]
            f.write("\t".join(row_data) + "\n")

    print(f"Height profile saved to '{filename}'")
    print(f"Resolution (x,y): {(size_x/nx,size_y/ny)}")

    # Optionally plot the height map
    if plot:
        import matplotlib.pyplot as plt

        # Create mesh grid for plotting
        # indexing='ij' so that heights[i, j] => (x_i, y_j).
        X, Y = np.meshgrid(x_vals, y_vals, indexing='ij')

        plt.figure(figsize=(6, 5))
        plt.pcolormesh(X, Y, heights, cmap='viridis', shading='auto')
        plt.colorbar(label='Height')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Uncorrelated 2D Surface Height Map')
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    # Example usage:
    rms_roughness = 0.5e-9   # RMS roughness
    size_x = 420.0e-3         # Physical size in x
    size_y = 30.0e-3          # Physical size in y
    nx = 40777//3                # Number of points in x
    ny = 2913//3                # Number of points in y
    output_filename = "/user/home/opt/xl/xl/experiments/heightProfiles/height_profile_M1.dat"

    generate_uncorrelated_2d_surface(
        rms=rms_roughness,
        size_x=size_x,
        size_y=size_y,
        nx=nx,
        ny=ny,
        filename=output_filename,
        plot=True  # Set to False if you do not want a plot
    )