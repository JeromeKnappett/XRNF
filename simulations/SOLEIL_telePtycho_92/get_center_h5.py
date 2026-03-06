import h5py
import numpy as np
import matplotlib.pyplot as plt

from skimage import io

def reject_outliers(data, m=2):
    med = np.nanmedian(data)
    std = np.nanstd(data)
    output = np.where((abs(data - med) < m * std), data, med)
    return output


def replace_outliers_with_median(err_arr):
    a = err_arr
    med = np.nanmedian(a)
    outlierConstant = 1.5
    upper_quartile = np.percentile(a, 80)
    lower_quartile = np.percentile(a, 20)
    IQR = (upper_quartile - lower_quartile) * outlierConstant
    quartileSet = (lower_quartile - IQR, upper_quartile + IQR)
    output = np.where((a >= quartileSet[0]) & (a <= quartileSet[1]), a, med)
    return output


def extract_by_roi(data_array, roi_array, x_min, x_max, y_min, y_max):
    """
    Extract values from data_array based on ROI bounds using positions in roi_array.
    """
    data = []
    for i, r in enumerate(roi_array):
        if (x_min <= r[0] < x_max) and (y_min <= r[1] <= y_max):
            data.append((data_array[0][i], data_array[1][i]))
    return data


def calculate_com(image):
    """
    Compute the center of mass of a 2D array (image).
    """
    total = np.sum(image)
    if total == 0:
        return (np.nan, np.nan)

    indices = np.indices(image.shape)
    x_center = np.sum(indices[1] * image) / total
    y_center = np.sum(indices[0] * image) / total
    return (x_center, y_center)


# --- PARAMETERS ---
data_dir = '/user/home/opt/xl/xl/experiments/SOLEIL_telePtycho_92/' 

# '/user/home/ptypy-0.5.0/jk/experiments/SOLEIL_telePtycho_91/'
# '/user/home/opt/xl/xl/experiments/SOLEIL_telePtycho_92/' 
scan_name = '13x15_20um_highT_1600_pad448'
 # '6x6_twopins_256'
# 'test_scan_4um_512'
# '6x6_twopins_256'
# '5x5_twopins_256'
# 'test_scan_4um_longZ_256'
# 'test_scan_4um_512'
#'5x5_twopins_256'
h5_file_path = f"{data_dir}SOLEIL_{scan_name}.h5"   # 🔁 Change to your actual HDF5 file path
define_roi = None  # Set to (x_min, x_max, y_min, y_max) in meters, or None for full dataset
asize = 2048#1600#512 #256  # Size of the overlay box in plot (in pixels)

save_path = f"{data_dir}SOLEIL_{scan_name}.tif"

# --- LOAD HDF5 FILE ---
with h5py.File(h5_file_path, 'r') as f:
    data_stack = f['data'][:]  # Shape: (N, H, W)
    pixel_size = f['det_pixelsize_m'][()]  # [dx, dy]

# --- PIXEL SIZE & IMAGE SHAPE ---
# Handle single value or 2-element pixel size
if np.isscalar(pixel_size) or len(pixel_size) == 1:
    dx = dy = float(pixel_size) if np.isscalar(pixel_size) else float(pixel_size[0])
else:
    dx, dy = pixel_size

num_images, img_h, img_w = data_stack.shape

# --- SYNTHETIC RASTER SCAN POSITIONS (in meters) ---
x_pixels = int(np.sqrt(num_images))
y_pixels = int(np.ceil(num_images / x_pixels))

x_pos = np.arange(x_pixels) * img_w * dx
y_pos = np.arange(y_pixels) * img_h * dy
xx, yy = np.meshgrid(x_pos, y_pos)
positions = np.vstack([xx.ravel(), yy.ravel()]).T[:num_images]

# --- COMPUTE CoM FOR EACH IMAGE ---
MX, MY = [], []
for img in data_stack:
    x_cen, y_cen = calculate_com(img)
    MX.append(x_cen)
    MY.append(y_cen)

# --- APPLY ROI FILTERING IF DEFINED ---
if define_roi is not None:
    M = [MX, MY]
    M = extract_by_roi(M, positions,
                       define_roi[0], define_roi[1],
                       define_roi[2], define_roi[3])
    MX = [m[0] for m in M]
    MY = [m[1] for m in M]

# --- PLOT RAW CENTERS ---
plt.scatter(MX, MY)
plt.title("Raw Centers of Mass")
plt.xlabel("X [pixels]")
plt.ylabel("Y [pixels]")
plt.show()

# --- OUTLIER REJECTION ---
MXc = reject_outliers(np.array(MX), m=3)
MYc = reject_outliers(np.array(MY), m=3)

# --- MEAN & MEDIAN CENTER POSITIONS ---
xm = np.nanmean(MX)
ym = np.nanmean(MY)
xmx = np.nanmedian(MX)
ymx = np.nanmedian(MY)

# --- PLOTTING RESULTS ---
plt.figure(figsize=(8, 6))
plt.scatter(MX, MY, color='red', label='Raw')
plt.scatter(MXc, MYc, color='blue', label='Cleaned (3σ outliers removed)')
plt.scatter(xm, ym, marker='x', color='black', label=f'Mean = ({int(xm)}, {int(ym)})')
plt.scatter(xmx, ymx, marker='x', color='yellow', label=f'Median = ({int(xmx)}, {int(ymx)})')

plt.hlines(ym - asize // 2, xm - asize // 2, xm + asize // 2, colors='black', linestyles='--')
plt.hlines(ym + asize // 2, xm - asize // 2, xm + asize // 2, colors='black', linestyles='--')
plt.vlines(xm - asize // 2, ym - asize // 2, ym + asize // 2, colors='black', linestyles='--')
plt.vlines(xm + asize // 2, ym - asize // 2, ym + asize // 2, colors='black', linestyles='--')

plt.xlabel('X center [pixels]')
plt.ylabel('Y center [pixels]')
plt.title("Center of Mass Summary")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# --- FINAL OUTPUT ---
print("Center position (x, y):", (xm, ym))


if save_path:
    img = np.mean(data_stack,axis=0)
    if np.max(np.abs(img)) > 2147483647:
        img = img*(2147483647 / np.max(np.abs(img)))
    # Save the summed images with subtracted darkfield
    if save_path:
        print(f'Saving processed image to: {save_path}')
        io.imsave(save_path,  np.int32(img))#.astype(np.uint16))