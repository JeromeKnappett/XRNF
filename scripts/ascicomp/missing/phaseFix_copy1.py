import numpy as np

def fit_plane(phase_map, mask):
    """
    Fit a plane z(x, y) = a*x + b*y + c to data in phase_map[mask].
    
    Returns a, b, c.
    """
    # Indices (row -> y, column -> x)
    y_idx, x_idx = np.where(mask)
    z = phase_map[mask]
    
    # Convert to float
    x_idx = x_idx.astype(np.float64)
    y_idx = y_idx.astype(np.float64)
    
    # Design matrix for a plane
    A = np.column_stack([x_idx, y_idx, np.ones_like(x_idx)])
    
    # Least-squares solve: A [a, b, c]^T = z
    coeffs, residuals, rank, s = np.linalg.lstsq(A, z, rcond=None)
    a, b, c = coeffs
    return a, b, c

def subtract_plane_from_entire_map(phase_map, a, b, c):
    """
    Subtract z(x, y) = a*x + b*y + c from every point in phase_map.
    """
    # Build a coordinate grid matching phase_map
    ny, nx = phase_map.shape
    x_grid, y_grid = np.meshgrid(np.arange(nx), np.arange(ny))
    
    # Compute the plane for the entire map
    plane = a*x_grid + b*y_grid + c
    
    # Subtract it
    return phase_map - plane

def remove_gradient_of_specified_region(phase_map, region_labels, region_id):
    """
    1) Fits a plane to 'phase_map' *within* a specified region (region_id).
    2) Subtracts that plane from the entire phase_map, preserving boundary jumps.
    
    Parameters
    ----------
    phase_map : 2D numpy array
        The input phase map.
    region_labels : 2D numpy array of int
        Same shape as phase_map. Each pixel labeled by a region ID (e.g. 0, 1, 2...).
    region_id : int
        The specific region ID we want to fit the gradient to.
    
    Returns
    -------
    corrected_phase : 2D numpy array
        The phase map after globally subtracting the plane
        fitted within the chosen region.
    """
    # Create a boolean mask for the specified region
    mask = (region_labels == region_id)
    
    # Fit a plane only within that region
    a, b, c = fit_plane(phase_map, mask)
    
    # Subtract that plane from the entire map
    corrected_phase = subtract_plane_from_entire_map(phase_map, a, b, c)
    
    return corrected_phase
