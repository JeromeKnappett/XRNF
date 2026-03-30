#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
aerial_image_spatial_metrics.py
================================
Computes ptychography aerial-image quality metrics:
  - over the whole array (global summary)
  - as a 2-D spatial map via a sliding real-space window

For each window position the script records:
  michelson, rms_contrast, composite_C, NILS, dH, period_mean, period_sdev, STD_ph

From these per-window scalar maps it produces:
  • mean-map  and  variance-map  of every metric   (metric_maps.svg)
  • distribution (histogram) of each metric        (metric_distributions.svg)
  • per-array comparison of global vs window-mean  (global_vs_window.svg)
  • pairwise metric comparison across arrays        (metric_comparison.svg)

Usage
-----
Populate `arrays` with your 2-D numpy arrays and set the configuration
block below, then run the script.
"""

import h5py
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
from scipy.signal import find_peaks

import interferenceGratingModelsJK
from calc_metrics import crop_center, rotate_complex_array, estimate_periodicity, print_peak_metrics

# ──────────────────────────────────────────────────────────────────────────────
# CONFIGURATION
# ──────────────────────────────────────────────────────────────────────────────
dir_path  = '/user/home/ptypy-0.5.0/jk/experiments/SOLEIL_telePtycho_91/'
date      = '28'
engine    = 'ML'
iteration = '800'
folder    = 'recons'
area      = 'large'        # used in filenames, e.g. 'large', '5x5', etc.

nums  = ['01', #'07', 
         '29', '38', 
         '39', '40']
names = [f"a1_hc_{area}_zerocenter", #f"a2_hc_{area}_zerocenter", 
         f"a3_hc_{area}_zerocenter",
         f"a1_lc_{area}_zerocenter", f"a2_lc_{area}_zerocenter", f"a3_lc_{area}_5_zerocenter"]

files    = [f"Image_202509{date}_0{nu}_{na}"  for nu, na in zip(nums, names)]
recons   = [f"recon_{date}_{nu}_{na}"         for nu, na in zip(nums, names)]
h5_files = [f"{dir_path}{fi}/{folder}/{re}/{re}_{engine}_0{iteration}.ptyr"
            for fi, re in zip(files, recons)]

dataset_path  = '/content/obj/Sscan_00G00/data'
psize_path    = '/content/obj/Sscan_00G00/_psize'

SAVE          = True

# ── Pre-processing parameters (mirror the batch script) ─────────────────────
central_size  = 833         # initial crop size [pixels]
ex            = 50          # secondary trim [pixels]  → final size = central_size - ex
center_offset = (0, 0)     # (x, y) offset from array centre for first crop
ROTATE        = False       # set to angle in degrees to rotate, or False
RMPHASE       = False       # True → remove phase ramp with ptypy

# Grating pitch in metres
pitch         = 100e-9      # [m]

# Which modality to analyse: 'I' (intensity), 'P' (phase), or 'both'
analyse       = 'both'

# ── Window parameters ────────────────────────────────────────────────────────
# Size of the sliding window in nanometres (real space).
# Should contain enough grating periods to measure contrast reliably.
window_nm     = 5000.0       # [nm]

# Step between successive window centres in nanometres.
# Smaller → finer map but slower.  Typically window_nm / 4 is a good start.
stride_nm     = 1000.0       # [nm]

# Which metric to use for selecting best region: 'michelson', 'rms_contrast', 'composite_C', 'NILS', or 'all' (average of NILS, composite_C, rms_contrast)
best_metric   = 'all'

# When True, skip the expensive bootstrap (RMS) and Monte-Carlo (composite-C)
# uncertainty estimates *inside each window*.  The global computation always
# runs the full estimators.  Recommended True unless you have few windows.
FAST_WINDOW   = True

# ── Plotting style ────────────────────────────────────────────────────────────
FS        = 13
I_COLOR   = 'black'
P_COLOR   = 'red'
CMAP_MEAN = 'viridis'
CMAP_VAR  = 'plasma'


# ──────────────────────────────────────────────────────────────────────────────
# LOAD AND PRE-PROCESS ALL WAVEFIELDS
# Produces the `arrays` dict consumed by the analysis engine below.
# ──────────────────────────────────────────────────────────────────────────────

def _load_wavefield(h5_file: str, label: str) -> dict:
    """
    Load one .ptyr HDF5 file, crop, optionally rotate/remove phase ramp,
    align phase, and return {'I', 'P', 'pixel_size', 'label'}.
    Mirrors the pre-processing in aerial_image_metrics_batch.py exactly.
    """
    print(f"\n{'='*60}")
    print(f"  Loading: {label}")

    with h5py.File(h5_file, 'r') as f:
        img  = f[dataset_path][()]
        pix  = float(f[psize_path][()].ravel()[0])

    print(f"  Raw shape  : {img.shape},  pixel size = {pix*1e9:.4f} nm")

    # ── crop to centre ────────────────────────────────────────────────────────
    if center_offset:
        ny_r, nx_r   = np.squeeze(img).shape[-2:]
        define_center = (nx_r // 2 + center_offset[0],
                         ny_r // 2 + center_offset[1])
    else:
        define_center = False

    img = crop_center(np.squeeze(img), central_size, define_center)

    if ROTATE:
        img = rotate_complex_array(img, ROTATE)
        img = crop_center(img, central_size - ex)
    else:
        img = crop_center(img, central_size - ex)

    if RMPHASE:
        import ptypy
        img = ptypy.utils.rmphaseramp(img, weight='abs')

    print(f"  Final shape: {img.shape}")

    if img.ndim != 2:
        raise ValueError(f"Expected 2-D complex image after crop, got {img.shape}")

    # ── intensity ─────────────────────────────────────────────────────────────
    I_arr = np.abs(img) ** 2

    # ── phase: initial wrap/shift ─────────────────────────────────────────────
    P = np.angle(img)
    P -= P.mean()
    P[P < -np.pi] += 2 * np.pi
    P[P >  np.pi] -= 2 * np.pi
    P -= P.mean()
    Pmin = np.min(P)
    P = (P + np.abs(Pmin)) if Pmin < 0 else (P - Pmin)

    # ── phase alignment: lift wrapped minima if separation > 2π ──────────────
    cy      = P.shape[0] // 2
    profile = P[cy, :]
    peaks,   _ = find_peaks( profile, distance=5)
    troughs, _ = find_peaks(-profile, distance=5)
    if len(peaks) > 0 and len(troughs) > 0:
        separation = np.mean(profile[peaks]) - np.mean(profile[troughs])
        if separation > 2 * np.pi:
            P[P < np.mean(P)] += 2 * np.pi
            print(f"  Phase wrap detected (sep={separation:.3f} rad) → +2π applied to minima")
        else:
            print(f"  Phase wrap OK (sep={separation:.3f} rad)")
    else:
        print(f"  Phase wrap check: insufficient peaks, skipping lift")

    P -= np.mean(P)

    return {'I': I_arr, 'P': P, 'pixel_size': pix, 'label': label}


arrays = {}
for h5f, name in zip(h5_files, names):
    try:
        entry = _load_wavefield(h5f, name)
        arrays[name] = entry
    except Exception as exc:
        print(f"  WARNING: could not load {name}: {exc}")

# ──────────────────────────────────────────────────────────────────────────────
# METRIC DEFINITIONS  (used to drive generic plotting loops)
# ──────────────────────────────────────────────────────────────────────────────
METRIC_DEFS = [
    # (key,              label,                    unit,   cmap)
    ('michelson',        'Michelson C',            '',     'viridis'),
    ('rms_contrast',     '$C_{\\mathrm{RMS}}$',    '',     'viridis'),
    ('composite_C',      '$C_{\\mathrm{C}}$',      '',     'viridis'),
    ('NILS',             'NILS / π',               '',     'cividis'),
    ('dH',               r'$\bar{\Delta}$',        '',     'magma'),
    ('period_mean',      r'$\bar{p}$',             'nm',   'plasma'),
    ('period_sdev',      'Period σ/μ',             '',     'hot'),
    ('STD_ph',           'Peak σ',                 '',     'inferno'),
]
METRIC_KEYS = [m[0] for m in METRIC_DEFS]


# ══════════════════════════════════════════════════════════════════════════════
# CORE METRIC ENGINE
# ══════════════════════════════════════════════════════════════════════════════

def _effective_n(series: np.ndarray) -> float:
    """Integrated autocorrelation effective sample size."""
    a = np.asarray(series, dtype=float)
    n = len(a)
    if n < 4 or np.std(a) == 0:
        return float(n)
    a_norm = (a - a.mean()) / a.std()
    tau = 0.0
    for k in range(1, n // 2):
        rk = np.mean(a_norm[:n - k] * a_norm[k:])
        if rk <= 0:
            break
        tau += rk
    return max(1.0, n / (2 * tau + 1))


def _sem(series) -> float:
    a = np.asarray(series, dtype=float)
    return float(np.std(a, ddof=1) / np.sqrt(_effective_n(a)))


def compute_metrics(arr: np.ndarray,
                    pix: float,
                    pitch_m: float,
                    fast: bool = False) -> dict:
    """
    Compute all aerial-image quality metrics for a 2-D array.

    Parameters
    ----------
    arr     : 2-D numpy array (intensity or phase)
    pix     : pixel size [m]
    pitch_m : grating pitch [m]
    fast    : if True, skip bootstrap and MC uncertainty estimates

    Returns
    -------
    dict with scalar metric values and their uncertainties.
    """
    ny, nx   = arr.shape
    xP       = (np.arange(nx) - nx // 2) * pix

    M2D_list, NILS_list = [], []
    PH_rows, TH_rows, SPACING_list = [], [], []

    for n in range(ny):
        iP     = arr[n, :]
        iP_pos = iP - iP.min()
        try:
            _, _, sp, ph, th = estimate_periodicity(
                iP, pix, distance=pitch_m / (2 * pix), show=False)
            nils = interferenceGratingModelsJK.NILS(iP_pos, xP, pitch_m, show=False)
            m2d  = interferenceGratingModelsJK.gratingContrastMichelson(iP_pos)
        except Exception:
            continue

        M2D_list.append(m2d)
        NILS_list.append(nils[0])
        PH_rows.append(list(ph))
        TH_rows.append(list(th))
        SPACING_list.append(sp)

    if not M2D_list:
        return {k: np.nan for k in METRIC_KEYS + [k + '_sem' for k in METRIC_KEYS]
                          + ['NILS_dist']}

    PH_list = [v for row in PH_rows for v in row]
    TH_list = [v for row in TH_rows for v in row]

    # ── per-row aggregates ────────────────────────────────────────────────────
    dH_per_row = []
    for ph_row, th_row in zip(PH_rows, TH_rows):
        if ph_row and th_row:
            dH_per_row.append(np.mean([p - t
                                        for p, t in zip(ph_row, th_row)]))
    dH     = float(np.mean(dH_per_row)) if dH_per_row else np.nan
    dH_sem = _sem(dH_per_row)           if dH_per_row else np.nan

    S_per_row   = [np.mean(sp) for sp in SPACING_list if len(sp) > 0]
    S_flat      = [s for sp in SPACING_list for s in sp]
    period_mean = float(np.mean(S_per_row)) * 1e9 if S_per_row else np.nan
    period_sem  = _sem(S_per_row)             * 1e9 if S_per_row else np.nan
    period_sdev = (np.std(S_flat) / np.mean(S_flat)) if S_flat else np.nan
    STD_ph      = float(np.std(PH_list))

    # ── 2-D contrast ─────────────────────────────────────────────────────────
    arr_pos = arr - arr.min()

    rmsC = interferenceGratingModelsJK.gratingContrastRMS(arr_pos)
    if fast:
        rmsC_std = np.nan
    else:
        rms_boot = np.array([
            interferenceGratingModelsJK.gratingContrastRMS(
                arr_pos[np.random.choice(ny, ny, replace=True), :])
            for _ in range(500)])
        rmsC_std = float(np.std(rms_boot, ddof=1))

    if fast:
        compC     = rmsC          # lightweight stand-in
        compC_std = np.nan
    else:
        _c = interferenceGratingModelsJK.meanDynamicRange_with_uncertainty(
            arr_pos, bins=256, n_mc=2000, resample_mode='poisson')
        compC     = _c['C']
        compC_std = _c['C_std']

    return dict(
        michelson         = float(np.mean(M2D_list)),
        michelson_sem     = _sem(M2D_list),
        rms_contrast      = rmsC,
        rms_contrast_sem  = rmsC_std,
        composite_C       = compC,
        composite_sem     = compC_std,
        NILS              = float(np.mean(NILS_list)) / np.pi,
        NILS_sem          = _sem(NILS_list) / np.pi,
        NILS_dist         = [v / np.pi for v in NILS_list],
        dH                = dH,
        dH_sem            = dH_sem,
        period_mean       = period_mean,
        period_sem        = period_sem,
        period_sdev       = period_sdev,
        STD_ph            = STD_ph,
    )


# ══════════════════════════════════════════════════════════════════════════════
# SLIDING-WINDOW MAP ENGINE
# ══════════════════════════════════════════════════════════════════════════════

def compute_metric_maps(arr: np.ndarray,
                        pix: float,
                        pitch_m: float,
                        window_nm: float,
                        stride_nm: float) -> dict:
    """
    Slide a real-space window across `arr` and compute metrics at each position.

    The window moves in steps of `stride_nm` nm in both y and x.
    Each window must contain at least 3 rows; positions with too few rows
    are marked NaN.

    Returns
    -------
    dict with keys:
        'map_<metric>'  – 2-D array (n_y_steps × n_x_steps) of metric values
        'y_centres_nm'  – 1-D array of window y-centre positions [nm]
        'x_centres_nm'  – 1-D array of window x-centre positions [nm]
        'window_nm'     – (wy, wx) actual window size used [nm]
    """
    ny, nx = arr.shape

    # convert nm → pixels
    win_px  = max(3, int(round(window_nm  / (pix * 1e9))))
    step_px = max(1, int(round(stride_nm  / (pix * 1e9))))

    half_y = win_px // 2
    half_x = win_px // 2

    y_starts = np.arange(half_y, ny - half_y, step_px)
    x_starts = np.arange(half_x, nx - half_x, step_px)

    n_y = len(y_starts)
    n_x = len(x_starts)

    # Pre-allocate output maps (NaN)
    maps = {k: np.full((n_y, n_x), np.nan) for k in METRIC_KEYS}

    total = n_y * n_x
    done  = 0
    for iy, cy in enumerate(y_starts):
        for ix, cx in enumerate(x_starts):
            sub = arr[cy - half_y: cy + half_y,
                      cx - half_x: cx + half_x]
            if sub.shape[0] < 3 or sub.shape[1] < 3:
                done += 1
                continue
            m = compute_metrics(sub, pix, pitch_m, fast=FAST_WINDOW)
            for k in METRIC_KEYS:
                maps[k][iy, ix] = m.get(k, np.nan)
            done += 1
        pct = 100 * done / total
        print(f"  Window map: {pct:5.1f}%  ({done}/{total})", end='\r', flush=True)

    print()  # newline after progress

    y_centres_nm = (y_starts - ny // 2) * pix * 1e9
    x_centres_nm = (x_starts - nx // 2) * pix * 1e9

    result = {'y_centres_nm': y_centres_nm,
              'x_centres_nm': x_centres_nm,
              'window_nm':    (win_px * pix * 1e9, win_px * pix * 1e9)}
    for k in METRIC_KEYS:
        result[f'map_{k}'] = maps[k]

    return result


# ══════════════════════════════════════════════════════════════════════════════
# RUN ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════

if not arrays:
    raise RuntimeError(
        "The `arrays` dict is empty. "
        "Populate it with your 2-D numpy arrays before running.")

results = {}   # label → {'global_I', 'global_P', 'maps_I', 'maps_P', ...}

for label, entry in arrays.items():
    print(f"\n{'='*60}")
    print(f"  Processing: {label}")
    print(f"{'='*60}")

    pix     = entry['pixel_size']#.get('pixel_size', pixel_size)
    p_m     = entry.get('pitch',      pitch)

    res = {'label': label, 'pixel_size': pix, 'pitch': p_m}

    for mod in (['I', 'P'] if analyse == 'both' else [analyse]):
        arr = entry[mod]
        print(f"\n  ── {mod} global metrics ──")
        g = compute_metrics(arr, pix, p_m, fast=False)
        res[f'global_{mod}'] = g

        print(f"\n  ── {mod} window map  "
              f"(window={window_nm:.0f} nm, stride={stride_nm:.0f} nm) ──")
        wm = compute_metric_maps(arr, pix, p_m, window_nm, stride_nm)
        res[f'maps_{mod}'] = wm
        res[f'arr_{mod}']  = arr

    results[label] = res

labels = list(results.keys())
print(f"\nDone. {len(labels)} array(s) processed.")

# ── Find best 5x5 um regions ────────────────────────────────────────────────
best_regions = {}
for label in labels:
    res = results[label]
    for mod in mods:
        maps = res[f'maps_{mod}']
        if best_metric == 'all':
            score_map = (maps['map_NILS'] + maps['map_composite_C'] + maps['map_rms_contrast']) / 3
        else:
            score_map = maps[f'map_{best_metric}']
        if np.all(np.isnan(score_map)):
            continue
        max_idx = np.unravel_index(np.nanargmax(score_map), score_map.shape)
        iy, ix = max_idx
        y_center_nm = maps['y_centres_nm'][iy]
        x_center_nm = maps['x_centres_nm'][ix]
        arr = res[f'arr_{mod}']
        pix = res['pixel_size']
        win_px = int(round(window_nm / (pix * 1e9)))
        half = win_px // 2
        cy_pixel = arr.shape[0] // 2 + int(round(y_center_nm / (pix * 1e9)))
        cx_pixel = arr.shape[1] // 2 + int(round(x_center_nm / (pix * 1e9)))
        sub_arr = arr[cy_pixel - half: cy_pixel + half, cx_pixel - half: cx_pixel + half]
        metrics = compute_metrics(sub_arr, pix, pitch, fast=False)
        best_regions[f'{label}_{mod}'] = {
            'metrics': metrics,
            'center_nm': (x_center_nm, y_center_nm),
            'center_pixel': (cx_pixel, cy_pixel)
        }


# ══════════════════════════════════════════════════════════════════════════════
# PLOTTING HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def _label_fmt(key):
    for k, lbl, unit, _ in METRIC_DEFS:
        if k == key:
            return lbl + (f'  [{unit}]' if unit else '')
    return key


def _cmap_for(key):
    for k, _, _, cm in METRIC_DEFS:
        if k == key:
            return cm
    return 'viridis'


def _add_colorbar(fig, ax, im, label):
    cb = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cb.set_label(label, fontsize=FS - 1)
    cb.ax.tick_params(labelsize=FS - 2)


def _plot_map_pair(ax_mean, ax_var, maps, key, label, pix):
    """Draw mean-map and variance-map for one metric."""
    m = maps[f'map_{key}']
    xc = maps['x_centres_nm']
    yc = maps['y_centres_nm']
    extent = [xc[0], xc[-1], yc[-1], yc[0]]

    mean_m = np.nanmean(m)
    var_m  = np.nanvar(m)
    std_m  = np.nanstd(m)

    cmap = _cmap_for(key)

    # mean map — colour limits ± 3σ around mean, clipped to data range
    vmin = np.nanpercentile(m, 2)
    vmax = np.nanpercentile(m, 98)
    im1  = ax_mean.imshow(m, extent=extent, origin='upper',
                           aspect='equal', cmap=cmap, vmin=vmin, vmax=vmax)
    ax_mean.set_title(f'{label}  (mean={mean_m:.3g})', fontsize=FS)
    ax_mean.set_xlabel('x  [nm]', fontsize=FS - 1)
    ax_mean.set_ylabel('y  [nm]', fontsize=FS - 1)
    ax_mean.tick_params(labelsize=FS - 2)
    _add_colorbar(ax_mean.get_figure(), ax_mean, im1, _label_fmt(key))

    # variance map
    im2 = ax_var.imshow(m ** 2, extent=extent, origin='upper',
                         aspect='equal', cmap=CMAP_VAR)
    ax_var.set_title(f'{label}  variance  (σ={std_m:.3g})', fontsize=FS)
    ax_var.set_xlabel('x  [nm]', fontsize=FS - 1)
    ax_var.set_ylabel('y  [nm]', fontsize=FS - 1)
    ax_var.tick_params(labelsize=FS - 2)
    _add_colorbar(ax_var.get_figure(), ax_var, im2, f'({_label_fmt(key)})²')


def _plot_map_mean(ax, maps, key, label, pix):
    """Draw mean-map for one metric."""
    m = maps[f'map_{key}']
    xc = maps['x_centres_nm']
    yc = maps['y_centres_nm']
    extent = [xc[0], xc[-1], yc[-1], yc[0]]

    mean_m = np.nanmean(m)
    cmap = _cmap_for(key)

    vmin = np.nanpercentile(m, 2)
    vmax = np.nanpercentile(m, 98)
    im = ax.imshow(m, extent=extent, origin='upper',
                   aspect='equal', cmap=cmap, vmin=vmin, vmax=vmax)
    ax.set_title(f'{label}  (mean={mean_m:.3g})', fontsize=FS)
    ax.set_xlabel('x  [nm]', fontsize=FS - 1)
    ax.set_ylabel('y  [nm]', fontsize=FS - 1)
    ax.tick_params(labelsize=FS - 2)
    _add_colorbar(ax.get_figure(), ax, im, _label_fmt(key))


# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 1 – METRIC MAPS  (mean only, per array, per modality)
# ══════════════════════════════════════════════════════════════════════════════
selected_keys = ['NILS', 'composite_C', 'period_mean']

mods = ['I', 'P'] if analyse == 'both' else [analyse]

for label in labels:
    res = results[label]
    for mod in mods:
        maps = res[f'maps_{mod}']
        n_metrics = len(selected_keys)

        fig, axes = plt.subplots(n_metrics, 1,
                                  figsize=(6, 4 * n_metrics))
        fig.suptitle(
            f'{label}  –  {"Intensity" if mod=="I" else "Phase"}  '
            f'metric maps\n'
            f'window = {window_nm:.0f} nm,  stride = {stride_nm:.0f} nm',
            fontsize=FS + 1)

        for row, key in enumerate(selected_keys):
            lbl = _label_fmt(key).split('  [')[0]  # remove unit
            _plot_map_mean(axes[row] if n_metrics > 1 else axes, maps, key,
                           lbl + (f' [{_label_fmt(key).split("  [")[1]}' if '  [' in _label_fmt(key) else ''),
                           res['pixel_size'])

        plt.tight_layout()
        fname = f'metric_maps_{label}_{mod}.svg'
        if SAVE:
            plt.savefig(dir_path + fname, bbox_inches='tight')
            print(f"Saved → {fname}")
        plt.show()


# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 2 – WAVEFIELD PLOTS WITH BEST REGION CENTER
# ══════════════════════════════════════════════════════════════════════════════

for label in labels:
    res = results[label]
    for mod in mods:
        if f'{label}_{mod}' not in best_regions:
            continue
        arr = res[f'arr_{mod}']
        cx, cy = best_regions[f'{label}_{mod}']['center_pixel']
        x_nm, y_nm = best_regions[f'{label}_{mod}']['center_nm']
        fig, ax = plt.subplots(figsize=(8,6))
        im = ax.imshow(arr, cmap='viridis' if mod=='I' else 'plasma', origin='upper')
        ax.plot(cx, cy, 'rx', markersize=15, markeredgewidth=3)
        ax.set_title(f'{label} - {mod} wavefield with best region center\nCenter: x={x_nm:.1f} nm, y={y_nm:.1f} nm')
        ax.set_xlabel('x [pixels]')
        ax.set_ylabel('y [pixels]')
        plt.colorbar(im, ax=ax)
        fname = f'wavefield_{label}_{mod}.png'
        if SAVE:
            plt.savefig(dir_path + fname, bbox_inches='tight')
            print(f"Saved → {fname}")
        plt.show()
        print(f"Best region center for {label} {mod}: x={x_nm:.1f} nm, y={y_nm:.1f} nm")


# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 3 – COMPARISON OF METRICS IN BEST REGIONS
# ══════════════════════════════════════════════════════════════════════════════

labels_mod = [lm for lm in best_regions.keys()]
n_labels = len(labels_mod)
for key in selected_keys:
    values = [best_regions[lm]['metrics'][key] for lm in labels_mod]
    errors = [best_regions[lm]['metrics'].get(key + '_sem', 0) for lm in labels_mod]
    fig, ax = plt.subplots(figsize=(10,6))
    x = np.arange(n_labels)
    ax.bar(x, values, yerr=errors, capsize=5, color='skyblue', edgecolor='black')
    ax.set_xticks(x)
    ax.set_xticklabels(labels_mod, rotation=45, ha='right')
    ax.set_title(f'{_label_fmt(key)} in best 5x5 μm regions')
    ax.set_ylabel(_label_fmt(key))
    plt.tight_layout()
    fname = f'metric_comparison_{key}.png'
    if SAVE:
        plt.savefig(dir_path + fname, bbox_inches='tight')
        print(f"Saved → {fname}")
    plt.show()


# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 4 – METRIC DISTRIBUTIONS  (histograms from window values)
# ══════════════════════════════════════════════════════════════════════════════

# One figure per modality, one subplot per metric.
# Overlays all arrays as separate histogram traces.
COLORS_ARRAYS = plt.cm.tab10(np.linspace(0, 0.9, max(len(labels), 1)))

for mod in mods:
    n_metrics = len(METRIC_KEYS)
    ncols = 4
    nrows = int(np.ceil(n_metrics / ncols))
    fig, axes = plt.subplots(nrows, ncols,
                              figsize=(5 * ncols, 4 * nrows))
    axes = axes.flatten()
    fig.suptitle(
        f'Metric distributions from sliding windows  –  '
        f'{"Intensity" if mod=="I" else "Phase"}',
        fontsize=FS + 1)

    for ax_idx, (key, lbl, unit, _) in enumerate(METRIC_DEFS):
        ax = axes[ax_idx]
        ax.set_title(lbl + (f'  [{unit}]' if unit else ''), fontsize=FS)
        ax.set_xlabel(_label_fmt(key), fontsize=FS - 1)
        ax.set_ylabel('Count', fontsize=FS - 1)
        ax.tick_params(labelsize=FS - 2)

        all_vals = []
        for label, color in zip(labels, COLORS_ARRAYS):
            m  = results[label][f'maps_{mod}'][f'map_{key}']
            v  = m[np.isfinite(m)].ravel()
            all_vals.extend(v)
            if len(v) > 1:
                ax.hist(v, bins=30, alpha=0.55, color=color,
                        edgecolor='white', linewidth=0.4, label=label)
                ax.axvline(np.nanmean(v), color=color, linewidth=1.8,
                           linestyle='--')

        ax.legend(fontsize=FS - 3, ncol=1)
        ax.grid(axis='y', linestyle='--', alpha=0.35)

    # hide unused panels
    for ax in axes[n_metrics:]:
        ax.set_visible(False)

    plt.tight_layout()
    fname = f'metric_distributions_{mod}.svg'
    if SAVE:
        plt.savefig(dir_path + fname, bbox_inches='tight')
        print(f"Saved → {fname}")
    plt.show()


# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 3 – GLOBAL  vs  WINDOW-MEAN  COMPARISON
# One panel per metric, arrays on x-axis, global=filled circle, window=square.
# Error bar for global = SEM from compute_metrics.
# Error bar for window = std of the window-map values.
# ══════════════════════════════════════════════════════════════════════════════

x_pos = np.arange(len(labels))

for mod in mods:
    color = I_COLOR if mod == 'I' else P_COLOR
    n_metrics = len(METRIC_KEYS)
    ncols = 4
    nrows = int(np.ceil(n_metrics / ncols))

    fig, axes = plt.subplots(nrows, ncols,
                              figsize=(5 * ncols, 4 * nrows))
    axes = axes.flatten()
    fig.suptitle(
        f'Global (●) vs window-mean (■)  –  '
        f'{"Intensity" if mod=="I" else "Phase"}',
        fontsize=FS + 1)

    for ax_idx, (key, lbl, unit, _) in enumerate(METRIC_DEFS):
        ax   = axes[ax_idx]
        sem_key = key + '_sem'

        glob_vals, glob_errs = [], []
        win_means, win_stds  = [], []

        for label in labels:
            g = results[label][f'global_{mod}']
            m = results[label][f'maps_{mod}'][f'map_{key}']
            v = m[np.isfinite(m)].ravel()

            glob_vals.append(g.get(key,     np.nan))
            glob_errs.append(g.get(sem_key, np.nan))
            win_means.append(float(np.nanmean(v)) if len(v) else np.nan)
            win_stds.append( float(np.nanstd(v))  if len(v) else np.nan)

        ax.errorbar(x_pos - 0.1, glob_vals, yerr=glob_errs,
                    fmt='o', color=color, ecolor=color,
                    mfc=color, capsize=5, markersize=8,
                    linewidth=1.5, label='Global')
        ax.errorbar(x_pos + 0.1, win_means, yerr=win_stds,
                    fmt='s', color=color, ecolor=color,
                    mfc='none', capsize=5, markersize=8,
                    linewidth=1.5, label='Window mean ± σ')

        ax.set_xticks(x_pos)
        ax.set_xticklabels(labels, rotation=30, ha='right', fontsize=FS - 2)
        ax.set_title(lbl + (f'  [{unit}]' if unit else ''), fontsize=FS)
        ax.set_ylabel(_label_fmt(key), fontsize=FS - 1)
        ax.tick_params(labelsize=FS - 2)
        ax.legend(fontsize=FS - 3)
        ax.grid(axis='y', linestyle='--', alpha=0.35)

    for ax in axes[n_metrics:]:
        ax.set_visible(False)

    plt.tight_layout()
    fname = f'global_vs_window_{mod}.svg'
    if SAVE:
        plt.savefig(dir_path + fname, bbox_inches='tight')
        print(f"Saved → {fname}")
    plt.show()


# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 4 – PAIRWISE METRIC SCATTER  (scatter of window values between arrays)
# For every pair of arrays, plot window_metric_A vs window_metric_B.
# ══════════════════════════════════════════════════════════════════════════════

from itertools import combinations

pairs = list(combinations(labels, 2))

for mod in mods:
    for (la, lb) in pairs:
        n_metrics = len(METRIC_KEYS)
        ncols = 4
        nrows = int(np.ceil(n_metrics / ncols))

        fig, axes = plt.subplots(nrows, ncols,
                                  figsize=(5 * ncols, 4 * nrows))
        axes = axes.flatten()
        color = I_COLOR if mod == 'I' else P_COLOR
        fig.suptitle(
            f'Window metric comparison:  {la}  vs  {lb}  '
            f'({"I" if mod=="I" else "φ"})',
            fontsize=FS + 1)

        for ax_idx, (key, lbl, unit, _) in enumerate(METRIC_DEFS):
            ax = axes[ax_idx]
            ma = results[la][f'maps_{mod}'][f'map_{key}'].ravel()
            mb = results[lb][f'maps_{mod}'][f'map_{key}'].ravel()

            # align (same grid assumed; if arrays differ in size, skip)
            if len(ma) != len(mb):
                ax.text(0.5, 0.5, 'Grid mismatch', transform=ax.transAxes,
                        ha='center', va='center', fontsize=FS - 2)
                ax.set_visible(True)
                continue

            mask = np.isfinite(ma) & np.isfinite(mb)
            ax.scatter(ma[mask], mb[mask], s=12, alpha=0.4, color=color)

            # 1:1 line
            lo = min(np.nanmin(ma), np.nanmin(mb))
            hi = max(np.nanmax(ma), np.nanmax(mb))
            ax.plot([lo, hi], [lo, hi], 'k--', linewidth=0.8, alpha=0.5)

            # Pearson r
            if mask.sum() > 2:
                r = np.corrcoef(ma[mask], mb[mask])[0, 1]
                ax.text(0.05, 0.93, f'r = {r:.3f}',
                        transform=ax.transAxes, fontsize=FS - 2,
                        verticalalignment='top')

            ax.set_xlabel(f'{la}  {_label_fmt(key)}', fontsize=FS - 2)
            ax.set_ylabel(f'{lb}  {_label_fmt(key)}', fontsize=FS - 2)
            ax.set_title(lbl + (f'  [{unit}]' if unit else ''), fontsize=FS)
            ax.tick_params(labelsize=FS - 2)
            ax.grid(linestyle='--', alpha=0.3)

        for ax in axes[n_metrics:]:
            ax.set_visible(False)

        plt.tight_layout()
        fname = f'metric_comparison_{la}_vs_{lb}_{mod}.svg'
        if SAVE:
            plt.savefig(dir_path + fname, bbox_inches='tight')
            print(f"Saved → {fname}")
        plt.show()


# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 5 – SUMMARY TABLE  (global mean ± SEM, and window mean ± σ)
# ══════════════════════════════════════════════════════════════════════════════

for mod in mods:
    print(f"\n{'='*80}")
    print(f"  SUMMARY  –  {'Intensity' if mod=='I' else 'Phase'}")
    print(f"{'='*80}")
    header = f"{'Metric':<22}" + "".join(f"  {lb:<26}" for lb in labels)
    print(header)
    print('-' * len(header))

    for key, lbl, unit, _ in METRIC_DEFS:
        sem_key = key + '_sem'
        row = f"{lbl + (' [' + unit + ']' if unit else ''):<22}"
        for label in labels:
            g  = results[label][f'global_{mod}']
            m  = results[label][f'maps_{mod}'][f'map_{key}']
            v  = m[np.isfinite(m)].ravel()
            gv = g.get(key, float('nan'))
            ge = g.get(sem_key, float('nan'))
            wm = float(np.nanmean(v)) if len(v) else float('nan')
            ws = float(np.nanstd(v))  if len(v) else float('nan')
            row += f"  G:{gv:.4f}±{ge:.4f}  W:{wm:.4f}±{ws:.4f}"
        print(row)