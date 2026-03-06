import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import sobel
import pickle
from math import e

def calculate_phase(E):
    """
    Calculates the total phase of a complex electric field.
    
    Parameters:
    E (array-like): Complex electric field array with shape (nx, ny, 2)
                    representing the x and y components of the electric field.
    
    Returns:
    phase (array-like): The total phase of the electric field.
    """
    E_x = E[:, :, 0]
    E_y = E[:, :, 1]
    phase = np.angle(E_x + E_y)
    
    # grad = np.gradient(phase, axis=1)
    # grad[abs(grad) > 0.9*np.pi] = 0
    # # sobel(phase, axis=1)
    # # np.gradient(phase, axis=1)
    
    # plt.plot(phase[np.shape(phase)[0]//2,:], '.', label = 'phase profile')
    # plt.plot(grad[np.shape(phase)[0]//2,:], '.', label = 'gradient')
    # plt.title('phase profile')
    # plt.legend()
    # # plt.colorbar()
    # plt.show()
    
    # grad = np.gradient(phase, axis=0)
    # grad[abs(grad) > 0.9*np.pi] = 0
    # # sobel(phase, axis=1)
    # # np.gradient(phase, axis=1)
    
    # plt.plot(phase[:,np.shape(phase)[1]//2], '.', label = 'phase profile')
    # plt.plot(grad[:,np.shape(phase)[1]//2], '.', label = 'gradient')
    # plt.title('phase profile')
    # plt.legend()
    # # plt.colorbar()
    # plt.show()
    
    return phase

def adjust_values_based_on_difference_thresholds(array, threshold, value, axis='x'):
    """
    Adjusts values in the array based on differences with adjacent points exceeding specified thresholds.
    
    Parameters:
    array (2D array-like): Input 2D array of values.
    threshold (float): positive/negative threshold value. Points with differences above/below this threshold will be modified.
    value (float): The value to add/subtract from points where the difference is above/below the positive/negative threshold.
    
    Returns:
    modified_array (2D array-like): Modified array with values adjusted based on the thresholds.
    """
    # Create a copy of the array to modify
    modified_array = np.copy(array)
    
    if axis=='x':
        # Check horizontal differences
        horizontal_diff = np.diff(modified_array, axis=1)
        horizontal_exceed_pos = horizontal_diff > threshold
        horizontal_exceed_neg = horizontal_diff < threshold
        
        # Add value to points exceeding positive horizontal threshold
        modified_array[:, :-1][horizontal_exceed_pos] += value
        modified_array[:, 1:][horizontal_exceed_pos] += value
        
        # Subtract value from points exceeding negative horizontal threshold
        modified_array[:, :-1][horizontal_exceed_neg] -= value
        modified_array[:, 1:][horizontal_exceed_neg] -= value
    
    # for i in range(modified_array.shape[0]):
    #     for j in range(modified_array.shape[1] - 1):
    #         if horizontal_exceed_pos[i, j]:
    #             modified_array[i, j] -= value
    #             modified_array[i, j + 1] -= value
    #         if horizontal_exceed_neg[i, j]:
    #             modified_array[i, j] += value
    #             modified_array[i, j + 1] += value
    
    elif axis == 'y':
        # Check vertical differences
        vertical_diff = np.diff(modified_array, axis=0)
        vertical_exceed_pos = vertical_diff > threshold
        vertical_exceed_neg = vertical_diff < threshold
        
        # Add value to points exceeding positive vertical threshold
        modified_array[:-1, :][vertical_exceed_pos] += value
        modified_array[1:, :][vertical_exceed_pos] += value
        
        # Subtract value from points exceeding negative vertical threshold
        modified_array[:-1, :][vertical_exceed_neg] -= value
        modified_array[1:, :][vertical_exceed_neg] -= value
    
    # for i in range(modified_array.shape[0] - 1):
    #     for j in range(modified_array.shape[1]):
    #         if vertical_exceed_pos[i, j]:
    #             modified_array[i, j] -= value
    #             modified_array[i + 1, j] -= value
    #         if vertical_exceed_neg[i, j]:
    #             modified_array[i, j] += value
    #             modified_array[i + 1, j] += value
    
    return modified_array

def calculate_pixel_differences(pixel_array):
    rows, cols = pixel_array.shape
    # Create an array to store the differences, initialized with zeros
    diff_array = np.zeros((rows, cols), dtype=int)
    
    # Set the initial pixel [0,0] difference as 0
    diff_array[0, 0] = 0
    
    # Fill the first row (horizontal differences)
    for j in range(1, cols):
        diff_array[0, j] = pixel_array[0, j] - pixel_array[0, j - 1]
    
    # Fill the first column (vertical differences)
    for i in range(1, rows):
        diff_array[i, 0] = pixel_array[i, 0] - pixel_array[i - 1, 0]
    
    # Fill the rest of the array, choosing the minimum of horizontal or vertical differences
    for i in range(1, rows):
        for j in range(1, cols):
            vertical_diff = pixel_array[i, j] - pixel_array[i - 1, j]
            horizontal_diff = pixel_array[i, j] - pixel_array[i, j - 1]
            diff_array[i, j] = min(vertical_diff, horizontal_diff)
    
    return diff_array

def calculate_pixel_differences_axis(pixel_array, axis='horizontal'):
    rows, cols = pixel_array.shape
    # Create an array to store the differences, initialized with zeros
    diff_array = np.zeros((rows, cols), dtype=float)
    
    if axis == 'horizontal':
        # Fill the first column with 0 (no previous pixel horizontally for first column)
        # diff_array[:, 0] = 0
        # Calculate horizontal differences for each row
        for i in range(rows):
            for j in range(1, cols):
                diff_array[i, j] = pixel_array[i, j] - pixel_array[i, j - 1]
                # print(diff_array[i,j])
    
    elif axis == 'vertical':
        # Fill the first row with 0 (no previous pixel vertically for first row)
        # diff_array[0, :] = 0
        # Calculate vertical differences for each column
        for j in range(cols):
            for i in range(1, rows):
                diff_array[i, j] = pixel_array[i, j] - pixel_array[i - 1, j]
    
    else:
        raise ValueError("Axis must be 'horizontal' or 'vertical'")
    
    # plt.imshow(diff_array)
    # plt.title('test')
    # plt.show()
    
    return diff_array

def phase_gradient_from_center(phase_array, dx, dy):
    """
    Calculates the phase gradient in x and y directions starting from the center point.
    
    Parameters:
    phase_array (2D array-like): Input 2D array of phase values.
    dx (float): Spatial step size in the x direction.
    dy (float): Spatial step size in the y direction.
    
    Returns:
    gradient_x (2D array-like): Gradient of phase in the x direction.
    gradient_y (2D array-like): Gradient of phase in the y direction.
    """
    # Get the shape of the array
    rows, cols = phase_array.shape
    
    # Calculate the center point indices
    center_row = rows // 2
    center_col = cols // 2
    
    # Initialize arrays for the gradients
    gradient_x = np.zeros_like(phase_array)
    gradient_y = np.zeros_like(phase_array)
    
    # Split the array into four quadrants and calculate the gradients for each quadrant
    quadrants = [
        np.fliplr(np.flipud(phase_array[:center_row+1, :center_col+1])),# 0, 0),  # Top-left
        np.flipud(phase_array[:center_row+1, center_col:]),# 0, center_col),  # Top-right
        np.fliplr(phase_array[center_row:, :center_col+1]),# center_row, 0),  # Bottom-left
        phase_array[center_row:, center_col:],# center_row, center_col)  # Bottom-right
        ]
    
    # Calculate gradients for each quadrant
    # Top-left quadrant
    Q1x = -calculate_pixel_differences_axis(quadrants[0],axis='horizontal') #-np.gradient(quadrants[0],axis=1)# / dx #np.fliplr(phase_array[:center_row+1, :center_col+1]), dx, axis=1)
    Q1y = calculate_pixel_differences_axis(quadrants[0],axis='vertical') #np.gradient(quadrants[0],axis=0)# / dy #np.flipud(phase_array[:center_row+1, :center_col+1]), dy, axis=0)
    gradient_x[:center_row+1, :center_col+1] = np.fliplr(np.flipud(Q1x))
    gradient_y[:center_row+1, :center_col+1] = np.fliplr(np.flipud(Q1y))
    
    # Top-right quadrant
    Q2x = calculate_pixel_differences_axis(quadrants[1],axis='horizontal') #np.gradient(quadrants[1],axis=1)# / dx #phase_array[:center_row+1, center_col:], dx, axis=1)
    Q2y = calculate_pixel_differences_axis(quadrants[1],axis='vertical') #np.gradient(quadrants[1],axis=0)# / dy #np.flipud(phase_array[:center_row+1, center_col:]), dy, axis=0)
    gradient_x[:center_row+1, center_col:] = np.flipud(Q2x)
    gradient_y[:center_row+1, center_col:] = np.flipud(Q2y)
    
    # Bottom-left quadrant
    Q3x = -calculate_pixel_differences_axis(quadrants[2],axis='horizontal') #-np.gradient(quadrants[2],axis=1)# / dx #np.fliplr(phase_array[center_row:, :center_col+1]), dx, axis=1)
    Q3y = -calculate_pixel_differences_axis(quadrants[2],axis='vertical') #-np.gradient(quadrants[2],axis=0)# / dy #phase_array[center_row:, :center_col+1], dy, axis=0)
    gradient_x[center_row:, :center_col+1] = np.fliplr(Q3x)
    gradient_y[center_row:, :center_col+1] = np.fliplr(Q3y)
    
    # Bottom-right quadrant
    Q4x = calculate_pixel_differences_axis(quadrants[3],axis='horizontal') #np.gradient(quadrants[3],axis=1)# / dx #phase_array[center_row:, center_col:], dx, axis=1)
    Q4y = -calculate_pixel_differences_axis(quadrants[3],axis='vertical') #-np.gradient(quadrants[3],axis=0)# / dy #phase_array[center_row:, center_col:], dy, axis=0)
    gradient_x[center_row:, center_col:] = Q4x
    gradient_y[center_row:, center_col:] = Q4y
    
    # print('shape of Q1x: ', np.shape(Q1x))
    
    # plt.imshow(phase_array,aspect='auto')
    # plt.title('unwrapped phase')
    # plt.show()
    
    # fig, ax = plt.subplots(2,2)
    
    # ax[0,0].imshow(quadrants[0],aspect='auto')
    # ax[0,0].set_title('Q1')
    # ax[0,1].imshow(quadrants[1],aspect='auto')
    # ax[0,1].set_title('Q2')
    # ax[1,0].imshow(quadrants[2],aspect='auto')
    # ax[1,0].set_title('Q3')
    # ax[1,1].imshow(quadrants[3],aspect='auto')
    # ax[1,1].set_title('Q4')
    # plt.show()
    
    # # # plt.imshow(phase_array,aspect='auto')
    # # # plt.colorbar()
    # # # plt.show()
    
    # fig, ax = plt.subplots(2,2)
    
    # ax[0,0].imshow(Q1x,aspect='auto')
    # ax[0,0].set_title('Q1x')
    # ax[0,1].imshow(Q2x,aspect='auto')
    # ax[0,1].set_title('Q2x')
    # ax[1,0].imshow(Q3x,aspect='auto')
    # ax[1,0].set_title('Q3x')
    # ax[1,1].imshow(Q4x,aspect='auto')
    # ax[1,1].set_title('Q4x')
    # plt.show()
    
    # # plt.imshow(gradient_x,aspect='auto')
    # # plt.colorbar()
    # # plt.show()
    
    # fig, ax = plt.subplots(2,2)
    
    # ax[0,0].imshow(Q1y,aspect='auto')
    # ax[0,0].set_title('Q1y')
    # ax[0,1].imshow(Q2y,aspect='auto')
    # ax[0,1].set_title('Q2y')
    # ax[1,0].imshow(Q3y,aspect='auto')
    # ax[1,0].set_title('Q3y')
    # ax[1,1].imshow(Q4y,aspect='auto')
    # ax[1,1].set_title('Q4y')
    # plt.show()
    
    # plt.imshow(gradient_y,aspect='auto')
    # plt.colorbar()
    # plt.show()
    
    # for r in range(center_row, rows):
    #     for c in range(center_col, cols):
    #         if r < rows - 1 and c < cols - 1:
    #             gradient_x[r, c] = (phase_array[r, c+1] - phase_array[r, c]) / dx
    #             gradient_y[r, c] = (phase_array[r+1, c] - phase_array[r, c]) / dy
    
    # for r in range(center_row, rows):
    #     for c in range(center_col, -1, -1):
    #         if r < rows - 1 and c > 0:
    #             gradient_x[r, c] = (phase_array[r, c] - phase_array[r, c-1]) / dx
    #             gradient_y[r, c] = (phase_array[r+1, c] - phase_array[r, c]) / dy
    
    # for r in range(center_row, -1, -1):
    #     for c in range(center_col, cols):
    #         if r > 0 and c < cols - 1:
    #             gradient_x[r, c] = (phase_array[r, c+1] - phase_array[r, c]) / dx
    #             gradient_y[r, c] = (phase_array[r, c] - phase_array[r-1, c]) / dy
    
    # for r in range(center_row, -1, -1):
    #     for c in range(center_col, -1, -1):
    #         if r > 0 and c > 0:
    #             gradient_x[r, c] = (phase_array[r, c] - phase_array[r, c-1]) / dx
    #             gradient_y[r, c] = (phase_array[r, c] - phase_array[r-1, c]) / dy
    
    print("Maximum phase gradient (x,y):   ", (np.max(gradient_x),np.max(gradient_y)))
    
    return gradient_x, gradient_y

def calculate_phase_gradient_threshold(E, dx, dy, intensity_threshold):
    """
    Calculates the 2-dimensional phase gradient of a complex electric field for points with intensity over a threshold.
    
    Parameters:
    E (array-like): Complex electric field array with shape (nx, ny, 2) 
                    representing the x and y components of the electric field.
    dx (float): Spatial step size in the x direction.
    dy (float): Spatial step size in the y direction.
    intensity_threshold (float): Threshold value for the intensity to calculate the phase gradient.
    
    Returns:
    gradient_x (array-like): The phase gradient in the x direction for points above the intensity threshold.
    gradient_y (array-like): The phase gradient in the y direction for points above the intensity threshold.
    distance_from_center_x (array-like): Distance from the central x-axis for the points above the intensity threshold.
    distance_from_center_y (array-like): Distance from the central y-axis for the points above the intensity threshold.
    """
    # Separate the x and y components of the electric field
    E_x = E[:, :, 0]
    E_y = E[:, :, 1]
    
    # Calculate the total intensity
    intensity_total = np.abs(E_x)**2 + np.abs(E_y)**2
    
    
    # Calculate the total phase
    phase_total = np.angle(E_x + E_y) + np.pi
    
    # plt.imshow(phase_total)
    # plt.colorbar()
    # plt.show()
    
    phase_total = np.unwrap(phase_total, axis=0,period=np.pi)#,discont=np.pi/10)# period=np.pi)#,discont=np.pi)
    phase_total = np.unwrap(phase_total, axis=1,period=np.pi)#,discont=np.pi/10)# period=np.pi)#,discont=np.pi)
    print('shape of phase: ', np.shape(phase_total))
    
    plt.imshow(phase_total)
    plt.title('Unwrapped phase')
    plt.colorbar()
    plt.show()
    
    # Calculate the phase gradient (partial derivative of the total phase)
    """For two dimensional arrays, the return will be two arrays ordered by
    axis. In this example the first array stands for the gradient in
    rows and the second one in columns direction:"""

    # >>> np.gradient(np.array([[1, 2, 6], [3, 4, 5]], dtype=float))
    # [array([[ 2.,  2., -1.],
    #        [ 2.,  2., -1.]]), array([[1. , 2.5, 4. ],
    #        [1. , 1. , 1. ]])]
                                     
    # gradient_x = sobel(phase_total, axis=0) / dx
    # gradient_y = sobel(phase_total, axis=1) / dy
    # gradient_x = np.gradient(phase_total, axis=0) / dx
    # gradient_y = np.gradient(phase_total, axis=1) / dy
    
    gradient_x, gradient_y = phase_gradient_from_center(phase_total,dx,dy) #np.gradient(phase_total)
    
    
    # grad = gradient_y
    # # grad[grad >= np.pi] -= np.pi
    # # grad[grad <= np.pi] += np.pi
    # # sobel(phase, axis=1)
    # # np.gradient(phase, axis=1)
    
    # plt.plot(phase_total[:,np.shape(phase_total)[1]//2], '.', label = 'phase profile')
    # plt.plot(grad[:,np.shape(phase_total)[1]//2] * np.max(phase_total[:,np.shape(phase_total)[1]//2]), '.', label = 'gradient')
    # plt.title('centered y phase profile')
    # plt.legend()
    # # plt.colorbar()
    # plt.show()
    
    # grad = gradient_x
    # grad[abs(grad) > 0.8*np.pi] = 0
    # # sobel(phase, axis=1)
    # # np.gradient(phase, axis=1)
    
    # plt.plot(phase_total[np.shape(phase_total)[0]//2,:], '.', label = 'phase profile')
    # plt.plot(grad[np.shape(phase_total)[0]//2,:] * np.max(phase_total[np.shape(phase_total)[0]//2,:]), '.', label = 'gradient')
    # plt.title('centered x phase profile')
    # plt.legend()
    # # plt.colorbar()
    # plt.show()
    
    # print('shape of gradient_x: ', np.shape(gradient_x))
    
    # Create the grid for calculating distance from the center
    ny, nx = E_x.shape
    print('here')
    print(nx,ny)
    x = np.linspace(-nx//2, nx//2, nx) * dx
    y = np.linspace(ny//2, -ny//2, ny) * dy
    X, Y = np.meshgrid(x, y)
    
    print(np.shape(X))
    print(np.shape(Y))
    
    # # Apply the intensity threshold
    # mask = intensity_total > intensity_threshold
    # gradient_x = gradient_x[mask]
    # gradient_y = gradient_y[mask]
    # distance_from_center_x = X[mask]
    # distance_from_center_y = Y[mask]
    
    # Set the values outside the threshold to zero
    # intensity_total[np.abs(intensity_total) < intensity_threshold] = 0

    
    # plt.imshow(gradient_x,aspect='auto')
    # plt.colorbar()
    # plt.title('phase gradient (x) - before')
    # plt.show()
    
    # plt.imshow(gradient_y,aspect='auto')
    # plt.colorbar()
    # plt.title('phase gradient (y) - before')
    # plt.show()
    
    # while abs(gradient_x).any() >= np.pi or abs(gradient_y).any() >= np.pi:
    #     gradient_x[gradient_x >= np.pi] -= np.pi
    #     gradient_x[gradient_x <= np.pi] += np.pi
    #     gradient_y[gradient_y >= np.pi] -= np.pi
#     gradient_y[gradient_y <= np.pi] += np.pi
    # for g in [gradient_x,gradient_y]:
    #     # grad[grad >= np.pi] -= np.pi
    #     # print('\n here')
    #     # print(np.shape(g))
    #     # print(g[g >= np.pi])
        
    #     g[g>2*np.pi] -= 2*np.pi
    #     g[g<-2*np.pi] += 2*np.pi
    #     g[g>=np.pi] -= np.pi
    #     g[g<=-np.pi] += np.pi
    #     # g[g=np.pi] -= np.pi
    #     # g[g-np.pi] += np.pi
    # gradient_x = adjust_values_based_on_difference_thresholds(gradient_x, np.pi, np.pi, axis='x')
    # gradient_y = adjust_values_based_on_difference_thresholds(gradient_y, np.pi, np.pi, axis='y')
    # gradient_x[gradient_x >= np.pi] = gradient_x[gradient_x >= np.pi] - np.pi
    # gradient_y[abs(gradient_y) >= np.pi] = 0
    
    gradient_x[np.abs(intensity_total) < intensity_threshold] = 0
    gradient_y[np.abs(intensity_total) < intensity_threshold] = 0
    
    # grad_thresh = 0.45*np.pi
    
    # gradient_x[np.abs(gradient_x) >= grad_thresh] = 0
    # gradient_y[np.abs(gradient_y) >= grad_thresh] = 0
    
    # plt.imshow(gradient_x,aspect='auto')
    # plt.colorbar()
    # plt.title('phase gradient (x) - after')
    # plt.show()
    
    # plt.imshow(gradient_y,aspect='auto')
    # plt.colorbar()
    # plt.title('phase gradient (y) - after')
    # plt.show()
    
    
    X[np.abs(intensity_total) < intensity_threshold] = 0
    Y[np.abs(intensity_total) < intensity_threshold] = 0
    
    # X[np.abs(gradient_x) >= grad_thresh] = 0
    # Y[np.abs(gradient_y) >= grad_thresh] = 0
    
    
    # plt.imshow(X,aspect='auto')
    # plt.colorbar()
    # plt.title('X')
    # plt.show()
    # plt.imshow(Y,aspect='auto')
    # plt.colorbar()
    # plt.title('Y')
    # plt.show()
    
    
    return gradient_x / dx, gradient_y / dy, X, Y #distance_from_center_x, distance_from_center_y

def calculate_phase_gradient(phase, dx, dy):
    """
    Calculates the phase gradient of the phase distribution.
    
    Parameters:
    phase (array-like): Phase distribution of the electric field.
    dx (float): Spatial step size in the x direction.
    dy (float): Spatial step size in the y direction.
    
    Returns:
    gradient_x (array-like): The phase gradient in the x direction.
    gradient_y (array-like): The phase gradient in the y direction.
    """
    
    gradient_y, gradient_x = sobel(phase)
    
    # gradient_x = sobel(phase, axis=0) / dx
    # gradient_y = sobel(phase, axis=1) / dy
    print('shape of gradient_x: ', np.shape(gradient_x))
    # Plot x and y divergence
    # Calculate the grid of positions
    nx, ny = gradient_x.shape
    x = np.linspace(-nx//2, nx//2, nx) * dx
    y = np.linspace(-ny//2, ny//2, ny) * dy
    X, Y = np.meshgrid(x, y)
    
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))
    
    im0 = axs[0].imshow(gradient_x / dx, extent=[x.min(), x.max(), y.min(), y.max()], origin='lower',aspect='auto')
    axs[0].set_title("x phase gradient")
    fig.colorbar(im0, ax=axs[0])
    
    im1 = axs[1].imshow(gradient_y / dy, extent=[x.min(), x.max(), y.min(), y.max()], origin='lower',aspect='auto')
    axs[1].set_title("y phase gradient")
    fig.colorbar(im1, ax=axs[1])
    
    plt.tight_layout()
    plt.show()
    return gradient_x/dx, gradient_y/dy, X, Y


def compute_divergence_from_phase_gradient(wl,gradient_x, gradient_y,dx,dy):
    """
    Computes the divergence of the phase gradient as the tangent of the phase gradient.
    
    Parameters:
    gradient_x (array-like): The phase gradient in the x direction.
    gradient_y (array-like): The phase gradient in the y direction.
    
    Returns:
    divergence_x (array-like): The divergence in the x direction.
    divergence_y (array-like): The divergence in the y direction.
    """    
    # Wave number
    k = 2 * np.pi / wl
    
    # plt.imshow(gradient_y,aspect='auto')
    # plt.title('before')
    # plt.show()
    
    divergence_x = np.arctan(gradient_x / k)
    divergence_y = np.arctan(gradient_y / k)
    
    
    # plt.imshow(divergence_y,aspect='auto')
    # plt.title('before')
    # plt.colorbar()
    # plt.show()
    
    
    # divergence_y = np.unwrap(divergence_y, axis=1,discont=np.max(divergence_y))#, period=8*np.max(divergence_y))
    
    
    # plt.imshow(divergence_y,aspect='auto')
    # plt.title('after')
    # plt.colorbar()
    # plt.show()
    
    print('shape of gradient_x: ', np.shape(gradient_x))
    # Plot x and y divergence
    # Calculate the grid of positions
    ny, nx = np.shape(gradient_x)
    x = np.linspace(-nx//2, nx//2, nx) * dx
    y = np.linspace(-ny//2, ny//2, ny) * dy
    X, Y = np.meshgrid(x, y)
    
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))
    
    im0 = axs[0].imshow(divergence_x, extent=[x.min(), x.max(), y.min(), y.max()],aspect='auto')
    axs[0].set_title("x'")
    fig.colorbar(im0, ax=axs[0])
    
    im1 = axs[1].imshow(divergence_y, extent=[x.min(), x.max(), y.min(), y.max()],aspect='auto')#, origin='lower',aspect='auto')
    axs[1].set_title("y'")
    fig.colorbar(im1, ax=axs[1])
    
    plt.tight_layout()
    plt.show()
    
    return divergence_x, divergence_y

def plot_total_intensity_and_phase(E, dx, dy):
    """
    Plots the total intensity and phase of a complex electric field.
    
    Parameters:
    E (array-like): Complex electric field array with shape (nx, ny, 2) 
                    representing the x and y components of the electric field.
    dx (float): Spatial step size in the x direction.
    dy (float): Spatial step size in the y direction.
    """
    # Separate the x and y components of the electric field
    E_x = E[:, :, 0]
    E_y = E[:, :, 1]
    
    # Calculate the grid of positions
    ny, nx = E_x.shape
    x = np.linspace(-nx//2, nx//2, nx) * dx
    y = np.linspace(-ny//2, ny//2, ny) * dy
    X, Y = np.meshgrid(x, y)
    
    # Calculate the total intensity
    intensity_total = np.abs(E_x)**2 + np.abs(E_y)**2
    
    # Calculate the total phase
    phase_total = np.angle(E_x + E_y)
    
    # Plot intensity and phase
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))
    
    im0 = axs[0].imshow(intensity_total, extent=[x.min(), x.max(), y.min(), y.max()], origin='lower',aspect='auto')
    axs[0].set_title('Total Intensity')
    fig.colorbar(im0, ax=axs[0])
    
    im1 = axs[1].imshow(phase_total, extent=[x.min(), x.max(), y.min(), y.max()], origin='lower',aspect='auto')
    axs[1].set_title('Total Phase')
    fig.colorbar(im1, ax=axs[1])
    
    plt.tight_layout()
    plt.show()
    return intensity_total, phase_total

def plot_divergence_vs_distance(divergence_x, divergence_y, distance_from_center_x, distance_from_center_y,title=None,limit=[[None,None],[None,None]]):
    """
    Plots the y component of the divergence against the distance from the central y-axis
    and the x component of the divergence against the distance from the central x-axis as scatter plots.
    
    Parameters:
    divergence_x (array-like): The divergence in the x direction.
    divergence_y (array-like): The divergence in the y direction.
    distance_from_center_x (array-like): Distance from the central x-axis for the points above the intensity threshold.
    distance_from_center_y (array-like): Distance from the central y-axis for the points above the intensity threshold.
    """
    
    print('shape of divergence_x: ', np.shape(divergence_x))
    print('shape of distance_x: ', np.shape(distance_from_center_x))
    
    maskX = abs(divergence_x) > 0.0
    maskY = abs(divergence_y) > 0.0
    divergence_x = divergence_x[maskX]
    divergence_y = divergence_y[maskY]
    distance_from_center_x = distance_from_center_x[maskX]
    distance_from_center_y = distance_from_center_y[maskY]
    
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))
    
    axs[0].scatter(distance_from_center_x, divergence_x, c='b', marker='o')
    axs[0].set_title('Divergence (x) vs. Distance from Central X-axis')
    axs[0].set_xlabel('Distance from Central X-axis')
    axs[0].set_ylabel('Divergence (x)')
    
    axs[1].scatter(distance_from_center_y, divergence_y, c='r', marker='o')
    axs[1].set_title('Divergence (y) vs. Distance from Central Y-axis')
    axs[1].set_xlabel('Distance from Central Y-axis')
    axs[1].set_ylabel('Divergence (y)')
    
    for ax in axs:
        ax.set_xlim(limit[0])
        ax.set_ylim(limit[1])
    
    print(distance_from_center_y)
    print(divergence_y)
    
    if title:
        fig.suptitle(title)
    
    plt.tight_layout()
    plt.show()


# Example usage with Gaussian beam data
def gaussian_beam(wl,nx, ny, dx, dy, waist_x, waist_y, divergence_x, divergence_y):
    x = np.linspace(-nx//2, nx//2, nx) * dx
    y = np.linspace(-ny//2, ny//2, ny) * dy
    X, Y = np.meshgrid(x, y)
    
    # Gaussian beam parameters
#    waist_x = 1.0  # Beam waist in x direction
#    waist_y = 1.0  # Beam waist in y direction
    k = 2 * np.pi / wl  # Wavenumber for a wavelength of wl
    
    # Amplitude
    amplitude = np.exp(- (X**2 / (2 * waist_x**2) + Y**2 / (2 * waist_y**2)))
    
    # Phase
    phase_x = k * divergence_x * X**2 / 2
    phase_y = k * divergence_y * Y**2 / 2
    
    # Complex field ensuring phase goes from -pi to +pi
    E_x = amplitude * np.exp(1j * (phase_x % (2 * np.pi) - np.pi))
    E_y = amplitude * np.exp(1j * (phase_y % (2 * np.pi) - np.pi))
    # Combine into a single array
    E = np.stack((E_x, E_y), axis=-1)
    
    return E


def testGauss():
    # Parameters
    # # Parameters
    nx, ny = 800, 800
    dx, dy = 0.00125, 0.00125
    divergence_x = 0.020e-6  # 20 mrad
    divergence_y = -1.5e-7  # 10 mrad
    size_x = 0.1
    size_y = 0.25
    # Parameters
    wavelength = 6.7e-9
    wl = wavelength
    # nx, ny = 1000, 1000
    # dx, dy = 0.1, 0.1
    # divergence_x = 10.0e-10  # 20 mrad
    # divergence_y = 5.0e-11  # 10 mrad
    # size_x = 10.0
    # size_y = 1.0
    intensity_threshold = 0.1e12  # Example threshold value
    # 
    # intensity_threshold = 0.1e12 #006e12 #0001e12  # Example threshold value
    
    E = gaussian_beam(wavelength,nx, ny, dx, dy, size_x, size_y, divergence_x, divergence_y)
    
    
    # print(np.shape(E))
    # # Plot total intensity and phase
    I, P = plot_total_intensity_and_phase(E, dx, dy)
    
    intensity_threshold = np.max(I) / 10# (e**2)
    
    print('Threshold I')
    print(intensity_threshold)
    
    # Calculate phase
    phase = calculate_phase(E)
    
    # Calculate phase gradients
    # gradient_x, gradient_y, distance_from_center_x, distance_from_center_y = calculate_phase_gradient(phase, dx, dy)
    
    # Apply intensity threshold and get distances from center
    # intensity_threshold = 0.1  # Example threshold value
    gradient_x, gradient_y, distance_from_center_x, distance_from_center_y = calculate_phase_gradient_threshold(E, dx, dy, intensity_threshold)
    
    # # Plot phase gradient vs distance
    # plot_divergence_vs_distance(gradient_x, gradient_y, distance_from_center_x, distance_from_center_y)
    
    # Compute divergences
    divergence_x, divergence_y = compute_divergence_from_phase_gradient(wl,gradient_x, gradient_y,dx,dy)
    
    # Plot divergence vs distance
    plot_divergence_vs_distance(divergence_x, divergence_y, distance_from_center_x, distance_from_center_y)
    
def testData():
    # path = 'wavefield_1.pkl'
    path = '/user/home/opt/xl/xl/experiments/correctedAngle_coherence/data/'
    #slit sizes]
    wl = 6.7e-9
    # S = 300
    sX = [25,50,75,100,125,150,175,200,225,250,300,350,500]
    sY = np.full_like(sX,200)
    files = [path + 'beforeBDA_efield_sx' + str(sx) + 'sy' + str(sy) + '/beforeBDA_efield_sx' + str(sx) + 'sy' + str(sy) + 'Efields.pkl' for sx,sy in zip(sX,sY)]
    
    picks = [pickle.load(open(f, 'rb')) for f in files]
    EhR = [p[0] for p in picks]
    EhI = [p[1] for p in picks]
    EvR = [p[2] for p in picks]
    EvI = [p[3] for p in picks]
    res = [(p[4],p[5]) for p in picks]
    
    
    Eh = [ExR + ExI*1j for ExR,ExI in zip(EhR,EhI)]
    Ev = [EyR + EyI*1j for EyR,EyI in zip(EvR,EvI)]#EvR + EvI*1j
    
    # E = Eh[0] + Ev[0]    
    # print(np.shape(E))
    # Combine into a single array
    for i,f in enumerate(files):
        E = np.stack((Eh[i], Ev[i]), axis=-1)
        dx,dy = res[i][0],res[i][1]
        
        # print(np.shape(E))
        # # Plot total intensity and phase
        I, P = plot_total_intensity_and_phase(E, dx, dy)
        
        intensity_threshold = np.max(I) / 10# (e**2)
        
        print('Threshold I')
        print(intensity_threshold)
        
        # Calculate phase
        phase = calculate_phase(E)
        
        # Calculate phase gradients
        # gradient_x, gradient_y, distance_from_center_x, distance_from_center_y = calculate_phase_gradient(phase, dx, dy)
        
        # Apply intensity threshold and get distances from center
        # intensity_threshold = 0.1  # Example threshold value
        gradient_x, gradient_y, distance_from_center_x, distance_from_center_y = calculate_phase_gradient_threshold(E, dx, dy, intensity_threshold)
        
        # # Plot phase gradient vs distance
        # plot_divergence_vs_distance(gradient_x, gradient_y, distance_from_center_x, distance_from_center_y)
        
        # Compute divergences
        divergence_x, divergence_y = compute_divergence_from_phase_gradient(wl,gradient_x, gradient_y,dx,dy)
        
        # Plot divergence vs distance
        plot_divergence_vs_distance(divergence_x, divergence_y, distance_from_center_x, distance_from_center_y)

if __name__ == '__main__':
    testGauss()
    # testData()