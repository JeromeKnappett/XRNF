import h5py
import numpy as np
import matplotlib.pyplot as plt
import re

from tqdm import tqdm

# -------------------------------
# User-defined parameters
# -------------------------------
dataset_path = '/content/obj/Sscan_00G00/data'
dir_path = '/user/home/ptypy-0.5.0/jk/experiments/SOLEIL_telePtycho_91/'
date = '28'
num ='40'
# '01'
#'40'
name = 'a3_lc_5x5_retest'
# 'a3_lc_5x5_zerocenter'
file = f"Image_202509{date}_0{num}_{name[0:-7]}"
# f"Image_202509{date}_0{num}standardized_5"
recon = f"recon_{date}_{num}_{name}"
# f"recon_{date}_{num}_large_5"
engine1 = 'DM'
iterations1 = ['010','020','030','040','050','060','070','080','090','100',
                '110','120','130','140','150','160','170','180','190','200',
                '210','220','230','240','250','260','270','280','290','300',
                '310','320','330','340','350','360','370','380','390','400',
                '410','420','430','440','450','460','470','480','490'#,'500'
               ]
 # ['010','020','030','040','050','060','070','080','090','100','110','120']
# h5_files = [f"{dir_path}{file}/dumps/{recon}/original/{recon}_{engine}_0{i}.ptyr" for i in iterations]
h5_files = [f"{dir_path}{file}/dumps/{recon}/{recon}_{engine1}_0{i}.ptyr" for i in iterations1]
h5_files.append(f"{dir_path}{file}/recons/{recon}/{recon}_{engine1}_0500.ptyr")

engine2 = 'ML'
iterations2 = ['510','520','530','540','550','560','570','580','590','600',
                '610','620','630','640','650','660','670','680','690','700',
                '710','720','730','740','750','760','770','780','790'#,'800']
               ]

# for i in ['510','520','530','540','550','560','570','580','590','600',
          # '610','620','630','640','650','660','670','680','690','700',
          # '710','720']:#,'730','740','750','760','770','780','790','800']:
# h5_files.append([f"{dir_path}{file}/dumps/{recon}/original/{recon}_ML_0{i}.ptyr")
for i in iterations2:
    h5_files.append(f"{dir_path}{file}/dumps/{recon}/{recon}_{engine2}_0{i}.ptyr")
h5_files.append(f"{dir_path}{file}/recons/{recon}/{recon}_{engine2}_0800.ptyr")


# for i in ['010','020','030','040','050','060','070','080','090','100']:
        # h5_files.append(f"{dir_path}{file}/dumps/{recon}/second/{recon}_DM_0{i}.ptyr")
    

# for i in ['010','020','030','040','050','060','070','080','090','100',
          # '110','120','130','140','150','160','170','180','190','200',
          # '210','220','230','240','250','260','270','280','290','300',
          # ]:
    # h5_files.append(f"{dir_path}{file}/dumps/{recon}/{recon}_DM_0{i}.ptyr")

dataset_path = '/content/obj/Sscan_00G00/data'
central_size = 150#212#100#212     # crop size around center to reduce memory load
roi_size = 150#212#100#212         # region in cropped data for mean std computation

# choose which modes to analyse: 'amp', 'phase', 'comp'
modes_to_analyse = ['amp', 'phase', 'comp']

SAVE = True

# -------------------------------
# Helper functions
# -------------------------------

def crop_center(arr, size):
    """Return a central crop of the given 2D array."""
    ny, nx = arr.shape
    cy, cx = ny // 2, nx // 2
    half = size // 2
    return arr[cy - half:cy + half, cx - half:cx + half]

def extract_number_from_filename(fname):
    """Extract iteration number from filename if possible."""
    nums = re.findall(r'\d+', fname)
    return int(nums[-1]) if nums else None

def extract_central_region(arr, size):
    """Extract central square region of given size from 2D or 3D array."""
    ny, nx = arr.shape[-2:]
    cy, cx = ny // 2, nx // 2
    half = size // 2
    return arr[..., cy - half:cy + half, cx - half:cx + half]

# -------------------------------
# Load and crop data once
# -------------------------------

cropped_data = []
for fpath in h5_files:
    print(fpath)
    with h5py.File(fpath, "r") as f:
        data = f[dataset_path][()]
    data = np.squeeze(np.array(data, dtype=np.complex128))
    cropped_data.append(crop_center(data, central_size))

cropped_data = np.stack(cropped_data, axis=0)  # (n_iters, h, w)
n_iters = cropped_data.shape[0]

# -------------------------------
# Prepare amplitude, phase, complex datasets
# -------------------------------

available_modes = {
    'amp': ('Amplitude', np.abs(cropped_data)),
    'phase': ('Phase', np.angle(cropped_data)),
    'comp': ('Complex', cropped_data)
}

# Filter to user-selected modes
selected_modes = {k: v for k, v in available_modes.items() if k in modes_to_analyse}

# -------------------------------
# Compute per-pixel std maps and evolution curves
# -------------------------------

std_maps = {}
mean_std_vs_iter = {}        # cumulative evolution
frame_to_frame_change = {}   # per-step difference evolution

for mode_key, (mode_name, vals) in selected_modes.items():
    print(f"Processing {mode_name}...")

    # --- Per-pixel std across all iterations ---
    if np.iscomplexobj(vals):
        pixel_std = np.sqrt(
            np.std(np.real(vals), axis=0)**2 +
            np.std(np.imag(vals), axis=0)**2
        )
    else:
        pixel_std = np.std(vals, axis=0)

    std_maps[mode_name] = pixel_std

    # --- Cumulative std evolution ---
    mean_std_vs_iter[mode_name] = []
    for i in range(2, n_iters + 1):
        if np.iscomplexobj(vals):
            std_up_to_i = np.sqrt(
                np.std(np.real(vals[:i]), axis=0)**2 +
                np.std(np.imag(vals[:i]), axis=0)**2
            )
        else:
            std_up_to_i = np.std(vals[:i], axis=0)

        central_region = extract_central_region(std_up_to_i, roi_size)
        mean_std_vs_iter[mode_name].append(np.mean(central_region))

    # --- Frame-to-frame difference ---
    diffs = vals[1:] - vals[:-1]   # per-pixel change between successive iterations
    if np.iscomplexobj(diffs):
        diff_mag = np.sqrt(np.real(diffs)**2 + np.imag(diffs)**2)
    else:
        diff_mag = np.abs(diffs)

    frame_to_frame_change[mode_name] = []
    for d in diff_mag:
        central = extract_central_region(d, roi_size)
        frame_to_frame_change[mode_name].append(np.mean(np.abs(central)))

# -------------------------------
# Extract iteration numbers for plotting
# -------------------------------

# iteration_numbers = [i*10 for i in range(0,len(h5_files))]#[extract_number_from_filename(f) for f in h5_files]
# if None in iteration_numbers:
iteration_numbers = list(range(10, 10 * len(h5_files) + 1, 10))

# -------------------------------
# Plot per-pixel std maps
# -------------------------------

fig, axes = plt.subplots(1, len(selected_modes), figsize=(5 * len(selected_modes), 5))
if len(selected_modes) == 1:
    axes = [axes]
for ax, (key, stdmap) in zip(axes, std_maps.items()):
    im = ax.imshow(stdmap, cmap='inferno')
    ax.set_title(f"{key} Std. Across Iterations")
    ax.axis("off")
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04, label="Std. over iterations")

plt.tight_layout()
if SAVE:
    plt.savefig(f"{dir_path}{file}/figures/{date}_{num}_{name}_2DmeanSTD.pdf")
plt.show()

# -------------------------------
# Plot cumulative std evolution
# -------------------------------

plt.figure(figsize=(8, 6))
colors = {'Amplitude': 'blue', 'Phase': 'red', 'Complex': 'black'}
for key, curve in mean_std_vs_iter.items():
    plt.plot(iteration_numbers[1:], curve,linestyle='', marker='o', mfc='none', color=colors.get(key, None), label=f"{key} (cumulative)")
# plt.title(f"Cumulative Mean Std in Central {roi_size}×{roi_size} Region")
plt.xlabel("Iteration Number")
plt.ylabel("Mean Std (log)")
plt.yscale('log')
plt.grid(True)
plt.legend()
plt.tight_layout()
if SAVE:
    plt.savefig(f"{dir_path}{file}/figures/{date}_{num}_{name}_meanSTD.pdf")
plt.show()

# -------------------------------
# Plot frame-to-frame mean change
# -------------------------------

plt.figure(figsize=(8, 6))
for key, curve in frame_to_frame_change.items():
    plt.plot(iteration_numbers[1:], curve, linestyle='', marker='o', mfc='none', color=colors.get(key, None), label=f"{key}")
# plt.title(f"Frame-to-Frame Mean Change in Central {roi_size}×{roi_size} Region")
plt.xlabel("Iteration Number")
plt.ylabel("Mean pixel std.")
plt.yscale('log')
plt.grid(True)
plt.legend()
# plt.ylim(0,0.05)
plt.tight_layout()
if SAVE:
    plt.savefig(f"{dir_path}{file}/figures/{date}_{num}_{name}_iterativeSTD.pdf")
plt.show()