import numpy as np
import tifffile
from scipy.ndimage import zoom
from skimage.transform import resize
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import h5py

from usefulWavefield_old import EtoWL

def create_complex_wavefield(intensity_path, phase_path,
                             original_pixel_size=(1.0, 1.0),
                             final_real_size=None,
                             new_pixel_size=None,
                             new_array_size=None,
                             autoCentre = False):
    """
    Create a complex wavefield from intensity and phase TIFF images, with optional center cropping 
    and resampling based on specified real sizes and pixel sizes.
    
    Parameters:
    -----------
    intensity_path : str
        Path to the TIFF file containing the intensity data of the wavefield.
    phase_path : str
        Path to the TIFF file containing the phase data of the wavefield.
    original_pixel_size : tuple of floats, optional
        The original pixel size of the input data in (pixel_size_x, pixel_size_y) format (in physical units).
        Defaults to (1.0, 1.0).
    final_real_size : tuple of floats, optional
        The desired physical size (width, height) of the final wavefield area in the same units as original_pixel_size.
        This parameter is used to crop the arrays to this physical size before resampling.
    new_pixel_size : tuple of floats, optional
        The desired pixel size for the final wavefield array in (pixel_size_x, pixel_size_y) format (in physical units).
        If provided after cropping, the wavefield will be resampled to match this new pixel size.
        
    Returns:
    --------
    complex_wavefield : numpy.ndarray
        A 2D complex-valued numpy array representing the cropped and resampled complex wavefield.
    
    Notes:
    ------
    - The amplitude of the wavefield is derived as sqrt(intensity).
    - The complex wavefield is constructed as amplitude * exp(i * phase).
    - If `final_real_size` is provided, the array is first cropped to center pixels corresponding to this physical size.
    - If `new_pixel_size` is provided, after cropping, the array is resampled so that the final pixel size matches `new_pixel_size`.
    - Pixel sizes and real sizes are tuples representing values along x and y dimensions.
    - The resampling uses bilinear interpolation (order=1) by default.
    """
    
    # Load intensity and phase data from TIFF files
    intensity = tifffile.imread(intensity_path)
    phase = tifffile.imread(phase_path)
    
    # Ensure that intensity and phase have the same shape
    if intensity.shape != phase.shape:
        raise ValueError("Intensity and phase images must have the same shape.")
    
    # Convert intensity and phase into a complex wavefield
    amplitude = np.sqrt(intensity)
    complex_wavefield = amplitude * np.exp(1j * phase)
        
    original_height, original_width = complex_wavefield.shape
    
    # Step 1: Cropping based on final_real_size
    if final_real_size is not None:
        if len(final_real_size) != 2:
            raise ValueError("final_real_size must be a tuple of two floats (width, height).")
        if len(original_pixel_size) != 2:
            raise ValueError("original_pixel_size must be a tuple of two floats (pixel_size_x, pixel_size_y).")
        
        final_real_width, final_real_height = final_real_size
        pixel_size_x, pixel_size_y = original_pixel_size
        
        if autoCentre:            
            # Find the position of the maximum intensity
            max_position = np.unravel_index(np.argmax(intensity), intensity.shape)
            max_y, max_x = max_position
        else:
            # Find the center of the array
            cen_array = intensity.shape[0] // 2, intensity.shape[1] // 2
            max_y,max_x = cen_array
        
        # Calculate the number of pixels that correspond to the desired physical size
        # in the original array
        width_in_pixels = int(final_real_width / pixel_size_x)
        height_in_pixels = int(final_real_height / pixel_size_y)
        
        # Ensure the crop sizes are not larger than the original sizes
        if width_in_pixels > original_width or height_in_pixels > original_height:
            raise ValueError("Specified final_real_size is larger than the original image size.")
        
        # Calculate start and end indices for cropping around the maximum intensity location
        start_x = max_x - width_in_pixels // 2
        start_y = max_y - height_in_pixels // 2
        end_x = start_x + width_in_pixels
        end_y = start_y + height_in_pixels
        
        # Adjust if the cropping window goes out of bounds
        if start_x < 0:
            start_x = 0
            end_x = width_in_pixels
        if start_y < 0:
            start_y = 0
            end_y = height_in_pixels
        if end_x > original_width:
            end_x = original_width
            start_x = original_width - width_in_pixels
        if end_y > original_height:
            end_y = original_height
            start_y = original_height - height_in_pixels
        
        # Crop the wavefield
        complex_wavefield = complex_wavefield[start_y:end_y, start_x:end_x]
        print(np.shape(complex_wavefield))
        
    # Step 2: Resampling based on new_pixel_size
    if new_pixel_size is not None:
        if len(new_pixel_size) != 2:
            raise ValueError("new_pixel_size must be a tuple of two floats (new_pixel_size_x, new_pixel_size_y).")
        if final_real_size is None:
            raise ValueError("final_real_size must be specified when new_pixel_size is provided.")

        # After cropping, the wavefield's shape corresponds to final_real_size physically
        current_height, current_width = complex_wavefield.shape
        final_real_width, final_real_height = final_real_size  # same as used for cropping
        new_pixel_size_x, new_pixel_size_y = new_pixel_size
        
        # Calculate the desired number of pixels in the final array
        final_width_in_pixels = int(final_real_width / new_pixel_size_x)
        final_height_in_pixels = int(final_real_height / new_pixel_size_y)
        
        # Calculate zoom factors
        # The current number of pixels is the cropped one, and we want to achieve final_width_in_pixels, final_height_in_pixels
        zoom_factor_y = final_height_in_pixels / current_height
        zoom_factor_x = final_width_in_pixels / current_width
        
        # Resample the wavefield using the zoom factors
        complex_wavefield = zoom(complex_wavefield, (zoom_factor_y, zoom_factor_x), order=1)
    
    if new_array_size is not None:
        print(np.shape(complex_wavefield))
        complex_wavefield = resize(complex_wavefield, new_array_size,preserve_range=True)# order=1)#, preserve_range=True, anti_aliasing=True)
    #     # After cropping, the wavefield's shape corresponds to final_real_size physically
    #     current_height, current_width = complex_wavefield.shape
    #     final_real_width, final_real_height = final_real_size  # same as used for cropping
    #     new_pixel_size_x, new_pixel_size_y = new_pixel_size
        
    #     # Calculate the desired number of pixels in the final array
    #     final_width_in_pixels = int(final_real_width / new_pixel_size_x)
    #     final_height_in_pixels = int(final_real_height / new_pixel_size_y)
        
    #     # Calculate zoom factors
    #     # The current number of pixels is the cropped one, and we want to achieve final_width_in_pixels, final_height_in_pixels
    #     zoom_factor_y = final_height_in_pixels / current_height
    #     zoom_factor_x = final_width_in_pixels / current_width
        
    #     # Resample the wavefield using the zoom factors
    #     complex_wavefield = zoom(complex_wavefield, (zoom_factor_y, zoom_factor_x), order=1)
    
    # print('')
    
    return complex_wavefield


def plot_complex_wavefield(complex_wavefield, dx,dy, phase_range=(-np.pi, np.pi)):
    """
    Plot a complex-valued 2D wavefield image.
    The hue represents the phase, and the brightness represents the amplitude.
    A colorbar for the phase is included.
    
    Parameters:
    -----------
    complex_wavefield : numpy.ndarray
        A 2D complex-valued NumPy array representing the wavefield.
    phase_range : tuple of floats, optional
        The range of phase values (in radians) mapped to the hue range [0, 1].
        Default is (-À, À).
        
    Returns:
    --------
    fig, ax : matplotlib.figure.Figure, matplotlib.axes.Axes
        The figure and axis objects of the plot.
        
    Notes:
    ------
    - The amplitude is represented by the brightness (value in HSV), normalized to [0, 1].
    - The phase is represented by the hue in HSV, mapped from phase_range to [0, 1].
    - The saturation is fixed to 1.
    - A colorbar is added to interpret the phase values.
    """
    
    # Extract amplitude and phase from the complex wavefield
    amplitude = np.abs(complex_wavefield)
    phase = np.angle(complex_wavefield)
    
    (Ny,Nx) = np.shape(amplitude)
    
    # Normalize amplitude to [0, 1] for brightness
    amplitude_normalized = amplitude / amplitude.max() if amplitude.max() != 0 else amplitude
    
    # Map the phase to hue in the range [0, 1]
    phase_min, phase_max = phase_range
    phase_mapped = (phase - phase_min) / (phase_max - phase_min)
    phase_mapped = np.mod(phase_mapped, 1)  # Ensures values wrap around the range [0, 1]
    
    # Construct the HSV image:
    # H = phase_mapped, S = 1 (full saturation), V = amplitude_normalized
    hsv_image = np.zeros((*complex_wavefield.shape, 3))
    hsv_image[..., 0] = phase_mapped
    hsv_image[..., 1] = 1.0
    hsv_image[..., 2] = amplitude_normalized
    
    # Convert HSV image to RGB
    rgb_image = mcolors.hsv_to_rgb(hsv_image)
    
    # Plot the image
    fig, ax = plt.subplots()
    cax = ax.imshow(rgb_image, origin='lower', extent=[-dx*(Nx/2),dx*(Nx/2),-dy*(Ny/2),dy*(Ny/2)], aspect='auto')
    ax.set_title('Complex Wavefield: Hue = Phase, Brightness = Amplitude')
    ax.set_xlabel('X-axis (pixels)')
    ax.set_ylabel('Y-axis (pixels)')
    
    # Create a custom colormap for the phase colorbar
    # The colormap will cycle through hues [0,1] in HSV with full saturation and value = 1
    phase_colormap = plt.cm.hsv
    
    # Create a norm for the phase range to map to the colorbar
    phase_norm = mcolors.Normalize(vmin=phase_min, vmax=phase_max)
    
    # Add a colorbar for the phase
    cbar = fig.colorbar(plt.cm.ScalarMappable(norm=phase_norm, cmap=phase_colormap), ax=ax)
    cbar.set_label('Phase (radians)')
    
    plt.show()
    return fig, ax

def resample_complex_array(input_array, new_shape):
    """
    Resamples a complex 2D array to a new shape.

    Parameters:
    input_array (numpy.ndarray): The input complex 2D array.
    new_shape (tuple): Desired output shape as (rows, columns).

    Returns:
    numpy.ndarray: The resampled complex 2D array.
    """
    # Separate the real and imaginary parts
    real_part = np.real(input_array)
    imag_part = np.imag(input_array)
    
    # Resample the real and imaginary parts separately
    real_resampled = resize(real_part, new_shape, preserve_range=True)
    imag_resampled = resize(imag_part, new_shape, preserve_range=True)
    
    # Recombine the real and imaginary parts
    resampled_array = real_resampled + 1j * imag_resampled
    return resampled_array

def prepare_probe_for_ptypy(complex_probe, output_filename):
    """
    Prepare a complex probe array for ptypy reconstruction as initial probe.
    Ensures it is in the correct format (modes, y, x) and saves as an HDF5 file.

    Parameters:
    -----------
    complex_probe : np.ndarray
        Complex numpy array representing the probe.
        This array must have shape: (y, x) or (modes, y, x).
    output_filename : str
        Path for the output HDF5 file that ptypy can read as the initial probe.

    Returns:
    --------
    None
    """
    # Ensure the probe array has shape (modes, y, x)
    if complex_probe.ndim == 2:
        # Single mode, one 2D array
        complex_probe = np.expand_dims(complex_probe, axis=0)
    elif complex_probe.ndim == 3:
        # Already in (modes, y, x) shape
        pass
    else:
        raise ValueError("Probe array must be 2D (y, x) or 3D (modes, y, x).")

    # Save complex probe data to an HDF5 file
    with h5py.File(output_filename, 'w') as hf:
        hf.create_dataset('probe', data=complex_probe)

    print(f"Probe data saved to {output_filename} in the shape {complex_probe.shape}.")

def reconstructedResolution(wl,Zsd,N,px):
    dXs = (wl * Zsd) / (N * px)
    return dXs

def test():
    dirPath = '/user/home/opt_cmd/xl/xl/experiments/SOLEIL_telePtycho/data/test_scan_2um/probe/'
    # '/user/home/opt/xl/xl/experiments/XFM_teleptycho/data/testPhaseSpace/atPinhole/'
    # '/user/home/opt/xl/xl/experiments/XFM_ptycho/data/phaseSpace/samplePinhole_in/'
    savePath = dirPath
    # '/user/home/ptypy-0.5.0/jk/experiments/XFM_ptycho/'
    
    energy = 185.0 #8340  # Photon energy in eV
    det_z = 6.52e-3  # Detector distance in m
    det_n = 128 #512
    det_px = 11.0e-6
    
    mePR = 'IntensityDist_SE.dat'
    # 'res_int_pr_se.dat'
    print("Loading probe file")
    nx = str(np.loadtxt(dirPath+mePR, dtype=str, comments=None, skiprows=6, max_rows=1, usecols=(0)))[1:]#[1:3]
    ny = str(np.loadtxt(dirPath+mePR, dtype=str, comments=None, skiprows=9, max_rows=1, usecols=(0)))[1:]#[1:3]
    xMin = str(np.loadtxt(dirPath+mePR, dtype=str, comments=None, skiprows=4, max_rows=1, usecols=(0)))[1:]#[1:3]
    xMax = str(np.loadtxt(dirPath+mePR, dtype=str, comments=None, skiprows=5, max_rows=1, usecols=(0)))[1:]#[1:3]
    rx = float(xMax)-float(xMin)
    dx = np.divide(rx,float(nx))
    yMin = str(np.loadtxt(dirPath+mePR, dtype=str, comments=None, skiprows=7, max_rows=1, usecols=(0)))[1:]#[1:3]
    yMax = str(np.loadtxt(dirPath+mePR, dtype=str, comments=None, skiprows=8, max_rows=1, usecols=(0)))[1:]#[1:3]
    ry = float(yMax)-float(yMin)
    dy = np.divide(ry,float(ny))
    
    numC = 1 #int(str(np.loadtxt(dirPath+mePR, dtype=str, comments=None, skiprows=10, max_rows=1, usecols=(0)))[1:])#[1:3]
    print("------ Probe parameters -------")
    print("Resolution (x,y): {}".format((nx,ny)))
    print("xRange: {}".format(rx))
    print("xMax: {}".format(xMax))
    print("xMin: {}".format(xMin))
    print("yRange: {}".format(ry))
    print("yMax: {}".format(yMax))
    print("yMin: {}".format(yMin))
    print("Dx, Dy : {}".format((dx,dy)))
    
    I = np.reshape(np.loadtxt(dirPath+mePR,skiprows=10), (numC, int(ny),int(nx)))         # Propagated multi-electron intensity
    # Iflat = I.flatten()
    # # conventional ptycho simulation
    # xi = -9.39929384314256e-05 #Initial Horizontal Position [m]
    # xf = 9.143431758962083e-05 #Final Horizontal Position [m]
    # Nx = 18720 #Number of points vs Horizontal Position
    # yi = -9.400271489561359e-05 #Initial Vertical Position [m]
    # yf = 9.146155389686803e-05 #Final Vertical Position [m]
    # Ny = 18720 #Number of points vs Vertical Position
    # Rx = xf-xi
    # Ry = yf-yi
    # dx = Rx/Nx
    # dy = Ry/Ny
    
    # print('(dx,dy): ', (dx,dy))
    """
    original_pixel_size : tuple of floats, optional
        The original pixel size of the input data in (pixel_size_x, pixel_size_y) format (in physical units).
        Defaults to (1.0, 1.0).
    final_real_size : tuple of floats, optional
        The desired physical size (width, height) of the final wavefield area in the same units as original_pixel_size.
        This parameter is used to crop the arrays to this physical size before resampling.
    new_pixel_size : tuple of floats, optional
        The desired pixel size for the final wavefield array in (pixel_size_x, pixel_size_y) format (in physical units).
        If provided after cropping, the wavefield will be resampled to match this new pixel size.
        """
    pr = reconstructedResolution(EtoWL(energy), det_z, det_n, det_px)
    
    finalSize =  (det_n*pr,det_n*pr)#(3.35354043904e-06,3.35354043904e-06)# for 1024
    # (6.71e-6,6.71e-6) # for 1024
    pixelSize = (pr,pr)#(6.54988367e-09,6.54988367e-09) #(15.e-09/2,15.e-09/2)# (6.54988367e-09, 6.54988367e-09)#(15.e-09,15.e-09) #(3.27494183e-09*2,3.27494183e-09*2)#(15.e-09,15.e-09)#(10.23e-6,10.23e-6)#(7.7e-6,7.7e-6)
    arraySize = (det_n,det_n)
    
    # # tele ptycho simulation
    # xi = -0.00012869358965143972 #Initial Horizontal Position [m]
    # xf = 0.00012613493977386305 #Final Horizontal Position [m]
    # Nx = 25480 #Number of points vs Horizontal Position
    # yi = -0.00015574296140587597 #Initial Vertical Position [m]
    # yf = 0.00015320177767720242 #Final Vertical Position [m]
    # Ny = 12150 #Number of points vs Vertical Position
    # Rx = xf-xi
    # Ry = yf-yi
    # dx = Rx/Nx
    # dy = Ry/Ny
    
    # print('(dx,dy): ', (dx,dy))
    # finalSize = (10.0e-6,10.0e-6) # for 1024
    # # (6.71e-6,6.71e-6) # for 1024
    # pixelSize = None#(6.e-09,6.e-09)# (6.54988367e-09, 6.54988367e-09)#(15.e-09,15.e-09) #(3.27494183e-09*2,3.27494183e-09*2)#(15.e-09,15.e-09)#(10.23e-6,10.23e-6)#(7.7e-6,7.7e-6)
    # arraySize = (720,720)#(512,512)
    
    # C = create_complex_wavefield(dirPath + 'intensity.tif', dirPath + 'phase.tif',
    #                              # new_pixel_size=2.0e-8,original_pixel_size=(dx,dy),
    #                              new_shape = (512,512)
    C = create_complex_wavefield(dirPath + 'intensity.tif', dirPath + 'phase.tif',
                                 original_pixel_size=(dx,dy),final_real_size=finalSize,
                                 new_pixel_size=pixelSize, new_array_size = arraySize, autoCentre=False) #(5.12e-6,5.12e-6))
    plot_complex_wavefield(C,dx,dy)
    prepare_probe_for_ptypy(C,savePath + 'probe_128.h5' )

if __name__ == '__main__':
    test()