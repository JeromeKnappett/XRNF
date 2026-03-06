import numpy as np
from scipy.ndimage import sobel

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
    return phase

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
    phase_total = np.angle(E_x + E_y)
    
    # Calculate the phase gradient (partial derivative of the total phase)
    gradient_x = sobel(phase_total, axis=1) / dx
    gradient_y = sobel(phase_total, axis=0) / dy
    
    # Create the grid for calculating distance from the center
    nx, ny = E_x.shape
    x = np.linspace(-nx//2, nx//2, nx) * dx
    y = np.linspace(-ny//2, ny//2, ny) * dy
    X, Y = np.meshgrid(x, y)
    
    # Apply the intensity threshold
    mask = intensity_total > intensity_threshold
    gradient_x = gradient_x[mask]
    gradient_y = gradient_y[mask]
    distance_from_center_x = X[mask]
    distance_from_center_y = Y[mask]
    
    return gradient_x, gradient_y, distance_from_center_x, distance_from_center_y

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
    gradient_x = sobel(phase, axis=1) / dx
    gradient_y = sobel(phase, axis=0) / dy
    return gradient_x, gradient_y


def compute_divergence_from_phase_gradient(wl,gradient_x, gradient_y):
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
    
    divergence_x = np.tan(gradient_x / k)
    divergence_y = np.tan(gradient_y / k)
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
    nx, ny = E_x.shape
    x = np.linspace(-nx//2, nx//2, nx) * dx
    y = np.linspace(-ny//2, ny//2, ny) * dy
    X, Y = np.meshgrid(x, y)
    
    # Calculate the total intensity
    intensity_total = np.abs(E_x)**2 + np.abs(E_y)**2
    
    # Calculate the total phase
    phase_total = np.angle(E_x + E_y)
    
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

def plot_divergence_vs_distance(divergence_x, divergence_y, distance_from_center_x, distance_from_center_y):
    """
    Plots the y component of the divergence against the distance from the central y-axis
    and the x component of the divergence against the distance from the central x-axis as scatter plots.
    
    Parameters:
    divergence_x (array-like): The divergence in the x direction.
    divergence_y (array-like): The divergence in the y direction.
    distance_from_center_x (array-like): Distance from the central x-axis for the points above the intensity threshold.
    distance_from_center_y (array-like): Distance from the central y-axis for the points above the intensity threshold.
    """
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))
    
    axs[0].scatter(distance_from_center_x, divergence_y, c='b', marker='o')
    axs[0].set_title('Divergence (y component) vs. Distance from Central Y-axis')
    axs[0].set_xlabel('Distance from Central Y-axis')
    axs[0].set_ylabel('Divergence (y component)')
    
    axs[1].scatter(distance_from_center_y, divergence_x, c='r', marker='o')
    axs[1].set_title('Divergence (x component) vs. Distance from Central X-axis')
    axs[1].set_xlabel('Distance from Central X-axis')
    axs[1].set_ylabel('Divergence (x component)')
    
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

# Parameters
wavelength = 6.7e-9
nx, ny = 1000, 1000
dx, dy = 0.1, 0.1
divergence_x = 10.0e-10  # 20 mrad
divergence_y = 5.0e-11  # 10 mrad
size_x = 10.0
size_y = 5.0
intensity_threshold = 0.1  # Example threshold value

E = gaussian_beam(wavelength,nx, ny, dx, dy, size_x, size_y, divergence_x, divergence_y)

print(np.shape(E))

# Plot total intensity and phase
plot_total_intensity_and_phase(E, dx, dy)

# Calculate phase
phase = calculate_phase(E)

# Calculate phase gradients
gradient_x, gradient_y = calculate_phase_gradient(phase, dx, dy)

# Apply intensity threshold and get distances from center
intensity_threshold = 0.1  # Example threshold value
gradient_x, gradient_y, distance_from_center_x, distance_from_center_y = calculate_phase_gradient_threshold(E, dx, dy, intensity_threshold)

# Compute divergences
divergence_x, divergence_y = compute_divergence_from_phase_gradient(wavelength,gradient_x, gradient_y)

# Plot divergence vs distance
plot_divergence_vs_distance(divergence_x, divergence_y, distance_from_center_x, distance_from_center_y)
