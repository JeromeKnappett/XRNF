import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import sobel

def calculate_phase_gradient(E, dx, dy):
    """
    Calculates the 2-dimensional phase gradient of a complex electric field.
    
    Parameters:
    E (array-like): Complex electric field array with shape (nx, ny, 2) 
                    representing the x and y components of the electric field.
    dx (float): Spatial step size in the x direction.
    dy (float): Spatial step size in the y direction.
    
    Returns:
    gradient_x (array-like): The phase gradient in the x direction.
    gradient_y (array-like): The phase gradient in the y direction.
    """
    # Separate the x and y components of the electric field
    E_x = E[:, :, 0]
    E_y = E[:, :, 1]
    
    # Calculate the total phase
    phase_total = np.angle(E_x + E_y)
    
    # Calculate the phase gradient (partial derivative of the total phase)
    gradient_x = sobel(phase_total, axis=1) / dx
    gradient_y = sobel(phase_total, axis=0) / dy
    
    return gradient_x, gradient_y

def plot_phase_gradient(gradient_x, gradient_y, dx, dy):
    """
    Plots the magnitude, x component, and y component of the phase gradient.
    
    Parameters:
    gradient_x (array-like): The phase gradient in the x direction.
    gradient_y (array-like): The phase gradient in the y direction.
    dx (float): Spatial step size in the x direction.
    dy (float): Spatial step size in the y direction.
    """
    # Calculate the magnitude of the phase gradient
    magnitude = np.sqrt(gradient_x**2 + gradient_y**2)
    
    # Create the grid for plotting
    nx, ny = gradient_x.shape
    x = np.linspace(-nx//2, nx//2, nx) * dx
    y = np.linspace(-ny//2, ny//2, ny) * dy
    X, Y = np.meshgrid(x, y)
    
    # Plot the magnitude, x component, and y component
    fig, axs = plt.subplots(1, 3, figsize=(18, 6))
    
    im0 = axs[0].imshow(magnitude, extent=[x.min(), x.max(), y.min(), y.max()], origin='lower')
    axs[0].set_title('Magnitude of Phase Gradient')
    fig.colorbar(im0, ax=axs[0])
    
    im1 = axs[1].imshow(gradient_x, extent=[x.min(), x.max(), y.min(), y.max()], origin='lower')
    axs[1].set_title('Phase Gradient (x component)')
    fig.colorbar(im1, ax=axs[1])
    
    im2 = axs[2].imshow(gradient_y, extent=[x.min(), x.max(), y.min(), y.max()], origin='lower')
    axs[2].set_title('Phase Gradient (y component)')
    fig.colorbar(im2, ax=axs[2])
    
    plt.tight_layout()
    plt.show()
    
def plot_phase_gradient_vs_distance(gradient_x, gradient_y, dx, dy):
    """
    Plots the y component of the phase gradient against the distance from the central y-axis
    and the x component of the phase gradient against the distance from the central x-axis.
    
    Parameters:
    gradient_x (array-like): The phase gradient in the x direction.
    gradient_y (array-like): The phase gradient in the y direction.
    dx (float): Spatial step size in the x direction.
    dy (float): Spatial step size in the y direction.
    """
    # Create the grid for plotting
    nx, ny = gradient_x.shape
    x = np.linspace(-nx//2, nx//2, nx) * dx
    y = np.linspace(-ny//2, ny//2, ny) * dy
    
    # Calculate the mean phase gradient along the central axes
    gradient_x_center = gradient_x[:, ny//2]
    gradient_y_center = gradient_y[nx//2, :]
    
    # Plot the phase gradient components against distance
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))
    
    axs[0].scatter(x, gradient_y_center, c='b', marker='o')
    axs[0].set_title('Phase Gradient (y component) vs. Distance from Central Y-axis')
    axs[0].set_xlabel('Distance from Central Y-axis')
    axs[0].set_ylabel('Phase Gradient (y component)')
    
    axs[1].scatter(y, gradient_x_center, c='r', marker='o')
    axs[1].set_title('Phase Gradient (x component) vs. Distance from Central X-axis')
    axs[1].set_xlabel('Distance from Central X-axis')
    axs[1].set_ylabel('Phase Gradient (x component)')
    
    plt.tight_layout()
    plt.show()

def plot_intensity_phase_phase_space(E, dx, dy):
    """
    Plots the 2-dimensional intensity and phase of a photon beam, along with the phase space.
    
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
    nx, ny = E_x.shape
    x = np.linspace(-nx//2, nx//2, nx) * dx
    y = np.linspace(-ny//2, ny//2, ny) * dy
    X, Y = np.meshgrid(x, y)
    
    # Calculate the total intensity
    intensity_total = np.abs(E_x)**2 + np.abs(E_y)**2
    
    # Calculate the total phase
    phase_total = np.angle(E_x + E_y)
    
    # Calculate the divergence (gradient of the phase)
    
    dfy = np.gradient(phase_total, y, axis=0)
    dfxy = np.gradient(dfy, x, axis=1)
    divergence_x = np.gradient(phase_total, dx, axis=1)
    divergence_y = np.gradient(phase_total, dy, axis=0)
    
    # Plot intensity and phase
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))
    
    im0 = axs[0].imshow(intensity_total, extent=[x.min(), x.max(), y.min(), y.max()], origin='lower')
    axs[0].set_title('Total Intensity')
    fig.colorbar(im0, ax=axs[0])
    
    im1 = axs[1].imshow(phase_total, extent=[x.min(), x.max(), y.min(), y.max()], origin='lower')
    axs[1].set_title('Total Phase')
    fig.colorbar(im1, ax=axs[1])
    
    plt.tight_layout()
    plt.show()
#    
    # Plot phase space
    fig, ax = plt.subplots(1, 2, figsize=(12, 6))
    
    ax[0].scatter(X, divergence_x, c='b', marker='o')
    ax[0].set_title('Horizontal Phase Space (x component)')
    ax[0].set_xlabel('Position')
    ax[0].set_ylabel('Divergence')
    
    ax[1].scatter(Y, divergence_y, c='r', marker='o')
    ax[1].set_title('Vertical Phase Space (y component)')
    ax[1].set_xlabel('Position')
    ax[1].set_ylabel('Divergence')
    
    plt.tight_layout()
    plt.show()

# Example usage with Gaussian beam data
def gaussian_beam(nx, ny, dx, dy, waist_x, waist_y, divergence_x, divergence_y):
    x = np.linspace(-nx//2, nx//2, nx) * dx
    y = np.linspace(-ny//2, ny//2, ny) * dy
    X, Y = np.meshgrid(x, y)
    
    # Gaussian beam parameters
#    waist_x = 1.0  # Beam waist in x direction
#    waist_y = 1.0  # Beam waist in y direction
    k = 2 * np.pi / 0.8  # Wavenumber for a wavelength of 0.8 units
    
    # Amplitude
    amplitude = np.exp(- (X**2 / (2 * waist_x**2) + Y**2 / (2 * waist_y**2)))
    
    # Phase
    phase_x = k * divergence_x * X**2 / 2
    phase_y = k * divergence_y * Y**2 / 2
    
    # Complex field
    E_x = amplitude * np.exp(1j * phase_x)
    E_y = amplitude * np.exp(1j * phase_y)
    
    # Combine into a single array
    E = np.stack((E_x, E_y), axis=-1)
    
    return E

# Parameters
nx, ny = 1000, 1000
dx, dy = 0.1, 0.1
divergence_x = 0.05  # 20 mrad
divergence_y = 0.01  # 10 mrad
size_x = 10.0
size_y = 5.0

E = gaussian_beam(nx, ny, dx, dy, size_x, size_y, divergence_x, divergence_y)

plot_intensity_phase_phase_space(E, dx, dy)

dpx,dpy = calculate_phase_gradient(E,dx,dy)
#
plot_phase_gradient(dpx,dpy,dx,dy)
#
plot_phase_gradient_vs_distance(dpx,dpy,dx,dy)

