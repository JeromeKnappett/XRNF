#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 11:45:22 2026

@author: -
"""

import h5py
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

import interferenceGratingModelsJK
from calc_metrics import (crop_center, rotate_complex_array,
                          estimate_periodicity, print_peak_metrics)

# ==============================================================================
# CONFIGURATION
# ==============================================================================
dir_path  = '/user/home/ptypy-0.5.0/jk/experiments/SOLEIL_telePtycho_91/'
date      = '28'
engine    = 'ML'
iteration = '800'
folder    = 'recons'
area = '5x5'
# 'large'
# '5x5'

nums  = ['01', '07', '29', '38', '39', '40']
names = [f"a1_hc_{area}_zerocenter", f"a2_hc_{area}_zerocenter", f"a3_hc_{area}_zerocenter",
         f"a1_lc_{area}_zerocenter", f"a2_lc_{area}_zerocenter", f"a3_lc_{area}_zerocenter"]

# ['a1_hc_5x5_zerocenter', 'a2_hc_5x5_zerocenter', 'a3_hc_5x5_zerocenter',
#          'a1_lc_5x5_zerocenter', 'a2_lc_5x5_zerocenter', 'a3_lc_5x5_zerocenter']

files  = [f"Image_202509{date}_0{nu}_{na}"  for nu, na in zip(nums, names)]
recons = [f"recon_{date}_{nu}_{na}"         for nu, na in zip(nums, names)]
h5_files = [
    f"{dir_path}{fi}/{folder}/{re}/{re}_{engine}_0{iteration}.ptyr"
    for fi, re in zip(files, recons)
]

dataset_path  = '/content/obj/Sscan_00G00/data'
ex            = 50
if area == 'large':
    central_size  = 833
elif area == '5x5':
    central_size  = 200
det_dist      = 0.0549
wavelength    = 13.6246e-9
pitch         = 100e-9
edge_taper    = False
taper_w       = ex // 2
unwrap        = False
plotRange     = 3000
center_offset = (0, 0)
analyse       = 'I'   # 'I', 'P', or 'both'
ROTATE        = False
RMPHASE       = False
SAVE          = True
PLOT_IMAGES   = True


# ==============================================================================
# HELPER – process a single h5 file and return a dict of metrics
# ==============================================================================
def process_single_image(h5_file: str, label: str = '') -> dict:
    """
    Load one ptyr file, compute quality metrics for intensity and/or phase,
    and return them in a dict.

    Return keys are always prefixed I_ (intensity) and P_ (phase) so that
    'both' mode can use both sets without ambiguity.
    """

    with h5py.File(h5_file, 'r') as f:
        img        = f[dataset_path][()]
        pixel_size = f['/content/obj/Sscan_00G00/_psize'][()][0]

    print(f"\n{'='*60}")
    print(f"Processing: {label or h5_file}")
    print(f"  Loaded shape : {img.shape}")

    if center_offset:
        ny, nx        = img[0].shape
        define_center = (nx // 2 + center_offset[0],
                         ny // 2 + center_offset[1])
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

    print(f"  Cropped shape: {img.shape}")

    if img.ndim != 2:
        raise ValueError(f"Expected 2-D complex image, got shape {img.shape}")

    H, W = img.shape

    # ── intensity & phase arrays ───────────────────────────────────────────────
    I_raw = np.abs(img) ** 2

    P = np.angle(img)
    P -= P.mean()
    P[P < -np.pi] += 2 * np.pi
    P[P >  np.pi] -= 2 * np.pi
    P -= P.mean()
    Pmin = np.min(P)
    P = P + np.abs(Pmin) if Pmin < 0 else P - Pmin

    # ── phase alignment: fix wrapped minima before any metric is computed ──────
    cy      = P.shape[0] // 2
    profile = P[cy, :]
    peaks,   _ = find_peaks( profile, distance=5)
    troughs, _ = find_peaks(-profile, distance=5)
    if len(peaks) > 0 and len(troughs) > 0:
        separation = np.mean(profile[peaks]) - np.mean(profile[troughs])
        if separation > 2 * np.pi:
            P[P < np.mean(P)] += 2 * np.pi
            print(f"  [{label}] phase wrap detected (sep={separation:.3f} rad) → +2π applied to minima")
        else:
            print(f"  [{label}] phase wrap check OK (sep={separation:.3f} rad)")
    else:
        print(f"  [{label}] phase wrap check: insufficient peaks found, skipping lift")
    P -= np.mean(P)

    xP     = np.linspace(-(W / 2) * pixel_size, (W / 2) * pixel_size, W)
    _pitch = pitch * 1.5 if analyse == 'P' else pitch

    # ── inner helper: compute all row-wise + 2D metrics for one array ──────────
    def _row_metrics(arr: np.ndarray, pitch_m: float) -> dict:
        M2D_list     = []
        NILS_list    = []
        PH_rows      = []
        TH_rows      = []
        SPACING_list = []

        for n in range(arr.shape[0]):
            iP     = arr[n, :]
            if iP.min() < 0:
                iP_pos = iP - iP.min()   # shift to min=0 for contrast functions 
            else:
                iP_pos = iP
            p, sdev, sp, ph, th = estimate_periodicity(
                iP, pixel_size, distance=pitch_m / (2 * pixel_size), show=False)
            NILS2d = interferenceGratingModelsJK.NILS(iP_pos, xP, pitch_m, show=False)
            m2D    = interferenceGratingModelsJK.gratingContrastMichelson(iP_pos)
            
            # m2D = interferenceGratingModelsJK.gratingContrastMichelson(iP)
    
            print_peak_metrics(ph)

            M2D_list.append(m2D)
            # print(f"Michelson:    {M2D_list}")
            NILS_list.append(NILS2d[0])
            PH_rows.append(list(ph))
            TH_rows.append(list(th))
            SPACING_list.append(sp)

        PH_list = [v for row in PH_rows for v in row]
        TH_list = [v for row in TH_rows for v in row]

        def _effective_n(series):
            a = np.asarray(series, dtype=float)
            n = len(a)
            if n < 4 or np.std(a) == 0:
                return float(n)
            a_norm = (a - a.mean()) / a.std()
            tau = 0.0
            for k in range(1, n // 2):
                rk = np.mean(a_norm[:n-k] * a_norm[k:])
                if rk <= 0:
                    break
                tau += rk
            return max(1.0, n / (2 * tau + 1))

        def _sem(series):
            a = np.asarray(series, dtype=float)
            return float(np.std(a, ddof=1) / np.sqrt(_effective_n(series)))

        avNILS   = np.mean(NILS_list)
        NILS_sem = _sem(NILS_list)

        m2D_mean = np.mean(M2D_list)
        m_sem    = _sem(M2D_list)

        dH_per_row = []
        for ph_row, th_row in zip(PH_rows, TH_rows):
            if ph_row and th_row:
                dH_per_row.append(np.mean([p - t for p, t in zip(ph_row, th_row)]))
        dH     = np.mean(dH_per_row) if dH_per_row else np.nan
        dH_sem = _sem(dH_per_row)    if dH_per_row else np.nan

        S_per_row   = [np.mean(sp) for sp in SPACING_list if len(sp) > 0]
        S_flat      = [s for sp in SPACING_list for s in sp]
        period_mean = np.mean(S_per_row) * 1e9 if S_per_row else np.nan
        period_sem  = _sem(S_per_row)    * 1e9 if S_per_row else np.nan
        sdev_s      = (np.std(S_flat) / np.mean(S_flat)) if S_flat else np.nan
        STD_ph      = np.std(PH_list)

        arr_pos    = arr - arr.min()   # shift whole array to min=0 for 2D contrast
        rmsC2d     = interferenceGratingModelsJK.gratingContrastRMS(arr_pos)
        rms_samples = np.array([
            interferenceGratingModelsJK.gratingContrastRMS(
                arr_pos[np.random.choice(arr_pos.shape[0], arr_pos.shape[0], replace=True), :])
            for _ in range(500)
        ])
        rmsC2d_std  = float(np.std(rms_samples, ddof=1))

        compC = interferenceGratingModelsJK.meanDynamicRange_with_uncertainty(
            arr_pos, bins=256, n_mc=2000, resample_mode='poisson')

        return dict(
            michelson        = m2D_mean,
            michelson_sem    = m_sem,
            rms_contrast     = rmsC2d,
            rms_contrast_sem = rmsC2d_std,
            composite_C      = compC['C'],
            composite_sem    = compC['C_std'],
            NILS             = avNILS / np.pi,
            NILS_sem         = NILS_sem / np.pi,
            NILS_dist        = [n / np.pi for n in NILS_list],
            dH               = dH,
            dH_sem           = dH_sem,
            period_mean      = period_mean,
            period_sem       = period_sem,
            period_sdev      = sdev_s,
            STD_ph           = STD_ph,
        )

    # ── compute metrics for both I and P ──────────────────────────────────────
    print(f"  Computing intensity metrics...")
    I_m = _row_metrics(I_raw, pitch)

    print(f"  Computing phase metrics...")
    P_m = _row_metrics(P, pitch * 1.5)# if analyse == 'P' else pitch)

    # ── print summary ──────────────────────────────────────────────────────────
    for tag, m in [('Intensity', I_m), ('Phase', P_m)]:
        print(f"  [{tag}]")
        print(f"    Mean periodicity : {m['period_mean']:.4f} ± {m['period_sem']:.4f} nm")
        print(f"    Δ(peak-trough)   : {m['dH']:.4f} ± {m['dH_sem']:.4f}")
        print(f"    Michelson C      : {m['michelson']:.4f} ± {m['michelson_sem']:.4f}")
        print(f"    RMS Contrast     : {m['rms_contrast']:.4f} ± {m['rms_contrast_sem']:.4f}")
        print(f"    Composite C      : {m['composite_C']:.4f} ± {m['composite_sem']:.4f}")
        print(f"    NILS             : {m['NILS']:.4f} ± {m['NILS_sem']:.4f}")
        print(f"    Period σ/μ       : {m['period_sdev']:.4f}")

    # prefix and merge
    out = dict(label=label, I_arr=I_raw, P=P, xP=xP, pixel_size=pixel_size)
    for k, v in I_m.items():
        out[f'I_{k}'] = v
    for k, v in P_m.items():
        out[f'P_{k}'] = v
    return out


# ==============================================================================
# IMAGE + LINE-PROFILE PLOT
# ==============================================================================
def plot_image_comparison(r: dict, save: bool = False) -> None:
    I_arr  = r['I_arr']
    P      = r['P']
    xP     = r['xP']
    label  = r['label']
    H, W   = I_arr.shape
    cy     = H // 2
    xP_nm  = xP * 1e9

    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle(label, fontsize=13, fontweight='bold')

    ax = axes[0, 0]
    im = ax.imshow(I_arr, origin='upper',
                   extent=[xP_nm[0], xP_nm[-1], xP_nm[-1], xP_nm[0]],
                   cmap='gray', aspect='equal')
    ax.axhline(xP_nm[cy], color='tomato', linestyle='--', linewidth=1)
    ax.set_title('Intensity')
    ax.set_xlabel('x  (nm)')
    ax.set_ylabel('y  (nm)')
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

    ax = axes[0, 1]
    ax.plot(xP_nm, I_arr[cy, :], color='steelblue', linewidth=1.2)
    ax.axvline(0, color='gray', linestyle=':', linewidth=0.8)
    ax.set_title(f'Intensity – centre row (row {cy})')
    ax.set_xlabel('x  (nm)')
    ax.set_ylabel('Intensity  (arb. u.)')
    ax.set_xlim(xP_nm[0], xP_nm[-1])
    ax.grid(axis='y', linestyle='--', alpha=0.4)

    ax = axes[1, 0]
    im2 = ax.imshow(P, origin='upper',
                    extent=[xP_nm[0], xP_nm[-1], xP_nm[-1], xP_nm[0]],
                    cmap='RdBu_r', aspect='equal')
    ax.axhline(xP_nm[cy], color='gold', linestyle='--', linewidth=1)
    ax.set_title('Phase')
    ax.set_xlabel('x  (nm)')
    ax.set_ylabel('y  (nm)')
    fig.colorbar(im2, ax=ax, fraction=0.046, pad=0.04, label='Phase  (rad)')

    ax = axes[1, 1]
    ax.plot(xP_nm, P[cy, :], color='mediumseagreen', linewidth=1.2)
    ax.axvline(0, color='gray', linestyle=':', linewidth=0.8)
    ax.set_title(f'Phase – centre row (row {cy})')
    ax.set_xlabel('x  (nm)')
    ax.set_ylabel('Phase  (rad)')
    ax.set_xlim(xP_nm[0], xP_nm[-1])
    ax.grid(axis='y', linestyle='--', alpha=0.4)

    plt.tight_layout()

    if save:
        fname = f"image_{label}.svg"
        plt.savefig(dir_path + fname, bbox_inches='tight')
        print(f"  Saved → {fname}")

    plt.show()


# ==============================================================================
# BATCH LOOP
# ==============================================================================
results = []
for h5f, name in zip(h5_files, names):
    try:
        r = process_single_image(h5f, label=name)
        results.append(r)
        if PLOT_IMAGES:
            plot_image_comparison(r, save=SAVE)
    except Exception as exc:
        print(f"  [SKIP] {name}: {exc}")

if not results:
    raise RuntimeError("No images processed successfully.")

labels = [r['label'] for r in results]

# ==============================================================================
# GROUPING
# ==============================================================================
group_labels = ['a1', 'a2', 'a3']
x            = np.arange(len(group_labels))

hc = results[0:3]   # High C  (a1_hc, a2_hc, a3_hc)
lc = results[3:6]   # Low C   (a1_lc, a2_lc, a3_lc)

OFFSET = 0.00

# ==============================================================================
# GLOBAL STYLE
# ==============================================================================
FS         = 14           # base font size
I_COLOR    = 'black'      # intensity
P_COLOR    = 'red'        # phase
HC_MARKER  = 'o'          # High C  (metrics plots)
LC_MARKER  = 'x'          # Low C   (metrics plots)
AP_MARKERS = ['o','x','^']# a1,a2,a3 (final SSA plot only)
AP_LABELS  = ['a1','a2','a3']
MS         = 9            # marker size

# Line-connection options for the metrics plots.
# Set CONNECT_LINES = True to draw lines between the a1,a2,a3 points.
# HC_LS / LC_LS control the line style for High C and Low C respectively.
CONNECT_LINES = True
HC_LS  = '-'    # High C line style
LC_LS  = '--'   # Low C  line style
P_HC_LS = ':'   # Phase High C line style  (only used when analyse == 'both')
P_LC_LS = '-.'  # Phase Low C  line style


def _get(results_list, key):
    return [r[key] for r in results_list]


def _tight_ylim(ax, margin=0.15):
    """Set y-limits with a fractional margin around the actual data range."""
    all_y = []
    for line in ax.get_lines():
        all_y.extend([v for v in line.get_ydata() if np.isfinite(v)])
    for container in ax.containers:
        try:
            for seg in container[2]:
                all_y.extend([v for v in seg.get_ydata() if np.isfinite(v)])
        except (IndexError, TypeError, AttributeError):
            pass
    if not all_y:
        return
    lo, hi = min(all_y), max(all_y)
    span = hi - lo if hi != lo else abs(hi) * 0.1 or 0.1
    ax.set_ylim(lo - margin * span, hi + margin * span)


def _make_metrics_legend():
    """
    Legend for the metrics plots:
      High C (circle), Low C (cross), Intensity (black), Phase (red).
    """
    from matplotlib.lines import Line2D
    return [
        Line2D([0],[0], marker=HC_MARKER, color='grey', linestyle='None',
               markersize=MS, label='High C'),
        Line2D([0],[0], marker=LC_MARKER, color='grey', linestyle='None',
               markersize=MS, label='Low C'),
        Line2D([0],[0], marker='s', color=I_COLOR, linestyle='None',
               markersize=MS, markerfacecolor=I_COLOR, label='Intensity'),
        Line2D([0],[0], marker='s', color=P_COLOR, linestyle='None',
               markersize=MS, markerfacecolor=P_COLOR, label='Phase'),
    ]


def _make_ssa_legend():
    """
    Legend for the final SSA-size plot:
      a1/a2/a3 (o,x,^), Intensity (black), Phase (red).
    """
    from matplotlib.lines import Line2D
    handles = []
    for mk, lbl in zip(AP_MARKERS, AP_LABELS):
        handles.append(Line2D([0],[0], marker=mk, color='grey', linestyle='None',
                               markersize=MS, label=lbl))
    handles.append(Line2D([0],[0], marker='s', color=I_COLOR, linestyle='None',
                           markersize=MS, markerfacecolor=I_COLOR, label='Intensity'))
    handles.append(Line2D([0],[0], marker='s', color=P_COLOR, linestyle='None',
                           markersize=MS, markerfacecolor=P_COLOR, label='Phase'))
    return handles


def _plot_series(ax, x_vals, y_vals, err_vals, color, marker, ls):
    """
    Plot a single errorbar series and optionally connect the points.
    Connecting line is drawn separately so it sits behind the error bars.
    """
    if CONNECT_LINES:
        ax.plot(x_vals, y_vals, color=color, linestyle=ls,
                linewidth=1.2, zorder=1)
    ax.errorbar(x_vals, y_vals, yerr=err_vals,
                fmt=marker, color=color, ecolor=color,
                mfc=color if marker != 'x' else 'none',
                capsize=5, markersize=MS, linewidth=1.5, zorder=2)


def _scatter_ap(ax, hc_list, lc_list, key, err_key, ylabel, title, color):
    """
    Single-modality panel: x-axis = a1,a2,a3.
    Marker encodes coherence: o = High C, x = Low C.
    Colour encodes modality (passed in).
    """
    xv = list(range(len(group_labels)))
    hc_vals = [r[key]     for r in hc_list]
    hc_errs = [r[err_key] for r in hc_list]
    lc_vals = [r[key]     for r in lc_list]
    lc_errs = [r[err_key] for r in lc_list]
    _plot_series(ax, xv, hc_vals, hc_errs, color, HC_MARKER, HC_LS)
    _plot_series(ax, xv, lc_vals, lc_errs, color, LC_MARKER, LC_LS)
    ax.set_xticks(xv)
    ax.set_xticklabels(group_labels, fontsize=FS)
    ax.set_ylabel(ylabel, fontsize=FS)
    ax.set_title(title,  fontsize=FS)
    ax.tick_params(labelsize=FS - 1)
    ax.grid(axis='y', linestyle='--', alpha=0.4)


def _scatter_both_ap(ax, hc_list, lc_list,
                     I_key, I_err, P_key, P_err,
                     ylabel, title):
    """
    Both-modality panel: x-axis = a1,a2,a3.
    Colour = modality (black=I, red=P).
    Marker = coherence (o=High C, x=Low C).
    """
    xv = list(range(len(group_labels)))
    _plot_series(ax, xv, [r[I_key] for r in hc_list],
                 [r[I_err] for r in hc_list], I_COLOR, HC_MARKER, HC_LS)
    _plot_series(ax, xv, [r[I_key] for r in lc_list],
                 [r[I_err] for r in lc_list], I_COLOR, LC_MARKER, LC_LS)
    _plot_series(ax, xv, [r[P_key] for r in hc_list],
                 [r[P_err] for r in hc_list], P_COLOR, HC_MARKER, P_HC_LS)
    _plot_series(ax, xv, [r[P_key] for r in lc_list],
                 [r[P_err] for r in lc_list], P_COLOR, LC_MARKER, P_LC_LS)
    ax.set_xticks(xv)
    ax.set_xticklabels(group_labels, fontsize=FS)
    ax.set_ylabel(ylabel, fontsize=FS)
    ax.set_title(title,  fontsize=FS)
    ax.tick_params(labelsize=FS - 1)
    ax.grid(axis='y', linestyle='--', alpha=0.4)



# ==============================================================================
# CONTRAST METRICS FIGURE
# ==============================================================================
fig, axes = plt.subplots(2, 2, figsize=(11, 9))
fig.suptitle('Aerial image quality metrics – High C vs Low C', fontsize=FS + 2)

if analyse == 'both':
    _scatter_both_ap(axes[0, 0], hc, lc,
                     'I_michelson', 'I_michelson_sem',
                     'P_michelson', 'P_michelson_sem',
                     'Michelson C', 'Michelson Contrast ± SEM')
    _scatter_both_ap(axes[0, 1], hc, lc,
                     'I_rms_contrast', 'I_rms_contrast_sem',
                     'P_rms_contrast', 'P_rms_contrast_sem',
                     '$C_{\mathrm{RMS}}$', 'RMS Contrast ± SEM')
    _scatter_both_ap(axes[1, 0], hc, lc,
                     'I_NILS', 'I_NILS_sem',
                     'P_NILS', 'P_NILS_sem',
                     'NILS / π', 'Normalised Image Log-Slope ± SEM')
    _scatter_both_ap(axes[1, 1], hc, lc,
                     'I_composite_C', 'I_composite_sem',
                     'P_composite_C', 'P_composite_sem',
                     '$C_{\mathrm{C}}$', 'Composite Contrast ± SEM')
else:
    pfx   = 'I_' if analyse == 'I' else 'P_'
    color = I_COLOR if analyse == 'I' else P_COLOR
    _scatter_ap(axes[0, 0], hc, lc, f'{pfx}michelson',    f'{pfx}michelson_sem',
                'Michelson C',          'Michelson Contrast ± SEM',     color)
    _scatter_ap(axes[0, 1], hc, lc, f'{pfx}rms_contrast', f'{pfx}rms_contrast_sem',
                '$C_{\mathrm{RMS}}$',   'RMS Contrast ± SEM',           color)
    _scatter_ap(axes[1, 0], hc, lc, f'{pfx}NILS',         f'{pfx}NILS_sem',
                'NILS / π',             'Normalised Image Log-Slope ± SEM', color)
    _scatter_ap(axes[1, 1], hc, lc, f'{pfx}composite_C',  f'{pfx}composite_sem',
                '$C_{\mathrm{C}}$',     'Composite Contrast ± SEM',     color)

# tight y-limits on Michelson panel
_tight_ylim(axes[0, 0])

fig.legend(handles=_make_metrics_legend(), fontsize=FS - 1,
           loc='lower center', ncol=4, bbox_to_anchor=(0.5, -0.04))
plt.tight_layout(rect=[0, 0.05, 1, 1])
if SAVE:
    plt.savefig(dir_path + 'contrast_metrics.svg', bbox_inches='tight')
    print("Saved → contrast_metrics.svg")
plt.show()


# ==============================================================================
# FRINGE METRICS FIGURE
# ==============================================================================
if analyse == 'both':
    fig2, axes2 = plt.subplots(3, 2, figsize=(11, 13))
    fig2.suptitle('Fringe metrics – High C vs Low C', fontsize=FS + 2)

    _scatter_ap(axes2[0, 0], hc, lc, 'I_period_mean', 'I_period_sem',
                r'$\bar{p}$  (nm)', r'Mean Periodicity $\bar{p}$ – Intensity ± SEM',
                I_COLOR)
    _scatter_ap(axes2[0, 1], hc, lc, 'P_period_mean', 'P_period_sem',
                r'$\bar{p}$  (nm)', r'Mean Periodicity $\bar{p}$ – Phase ± SEM',
                P_COLOR)
    _scatter_ap(axes2[1, 0], hc, lc, 'I_dH', 'I_dH_sem',
                r'$\bar{\Delta}I$', r'$\bar{\Delta}I$ – Intensity ± SEM',
                I_COLOR)
    _scatter_ap(axes2[1, 1], hc, lc, 'P_dH', 'P_dH_sem',
                r'$\bar{\Delta}\phi$', r'$\bar{\Delta}\phi$ – Phase ± SEM',
                P_COLOR)
    _scatter_both_ap(axes2[2, 0], hc, lc,
                     'I_period_sdev', 'I_period_sdev',   # no error: plot at 0
                     'P_period_sdev', 'P_period_sdev',
                     'σ / μ', 'Relative Period Std Dev')
    _scatter_both_ap(axes2[2, 1], hc, lc,
                     'I_STD_ph', 'I_STD_ph',
                     'P_STD_ph', 'P_STD_ph',
                     'σ', 'Peak Height Std Dev')

else:
    pfx      = 'I_' if analyse == 'I' else 'P_'
    color    = I_COLOR if analyse == 'I' else P_COLOR
    dH_label = r'$\bar{\Delta}I$' if analyse == 'I' else r'$\bar{\Delta}\phi$'

    fig2, axes2 = plt.subplots(2, 2, figsize=(11, 9))
    fig2.suptitle('Fringe metrics – High C vs Low C', fontsize=FS + 2)

    _scatter_ap(axes2[0, 0], hc, lc, f'{pfx}period_mean', f'{pfx}period_sem',
                r'$\bar{p}$  (nm)', r'Mean Periodicity $\bar{p}$ ± SEM', color)
    _scatter_ap(axes2[0, 1], hc, lc, f'{pfx}period_sdev', f'{pfx}period_sdev',
                'σ / μ', 'Relative Period Std Dev', color)
    _scatter_ap(axes2[1, 0], hc, lc, f'{pfx}dH', f'{pfx}dH_sem',
                dH_label, f'{dH_label} ± SEM', color)
    _scatter_ap(axes2[1, 1], hc, lc, f'{pfx}STD_ph', f'{pfx}STD_ph',
                'σ', 'Peak Height Std Dev', color)

fig2.legend(handles=_make_metrics_legend(), fontsize=FS - 1,
            loc='lower center', ncol=4, bbox_to_anchor=(0.5, -0.04))
plt.tight_layout(rect=[0, 0.05, 1, 1])
if SAVE:
    plt.savefig(dir_path + 'fringe_metrics.svg', bbox_inches='tight')
    print("Saved → fringe_metrics.svg")
plt.show()


# ==============================================================================
# NILS DISTRIBUTION – histogram per aperture
# ==============================================================================
pfx_nils = 'P_' if analyse == 'P' else 'I_'

fig3, axes3 = plt.subplots(1, 3, figsize=(14, 5), sharey=True)
fig3.suptitle('NILS / π  distribution – High C vs Low C', fontsize=FS + 2)

for i, (hc_r, lc_r, gl, ax) in enumerate(zip(hc, lc, group_labels, axes3)):
    hd = hc_r[f'{pfx_nils}NILS_dist']
    ld = lc_r[f'{pfx_nils}NILS_dist']
    bins = np.linspace(min(min(hd), min(ld)), max(max(hd), max(ld)), 30)
    ax.hist(hd, bins=bins, color=I_COLOR,
            alpha=0.5, label='High C', edgecolor='white', linewidth=0.5)
    ax.hist(ld, bins=bins, color=P_COLOR,
            alpha=0.5, label='Low C',  edgecolor='white', linewidth=0.5)
    ax.axvline(hc_r[f'{pfx_nils}NILS'], color=I_COLOR, linestyle='-',  linewidth=1.8)
    ax.axvline(lc_r[f'{pfx_nils}NILS'], color=P_COLOR, linestyle='--', linewidth=1.8)
    ax.set_title(gl, fontsize=FS)
    ax.set_xlabel('NILS / π', fontsize=FS)
    ax.tick_params(labelsize=FS - 1)
    ax.grid(axis='y', linestyle='--', alpha=0.4)

axes3[0].set_ylabel('Count (rows)', fontsize=FS)
from matplotlib.lines import Line2D as _L2D
_nils_handles = [
    _L2D([0],[0], color=I_COLOR, linewidth=8, alpha=0.5, label='High C'),
    _L2D([0],[0], color=P_COLOR, linewidth=8, alpha=0.5, label='Low C'),
]
fig3.legend(handles=_nils_handles, fontsize=FS - 1,
            loc='lower center', ncol=2, bbox_to_anchor=(0.5, -0.06))
plt.tight_layout(rect=[0, 0.06, 1, 1])
if SAVE:
    plt.savefig(dir_path + 'nils_distributions.svg', bbox_inches='tight')
    print("Saved → nils_distributions.svg")
plt.show()


# ==============================================================================
# COMBINED LINE PROFILES – per-aperture panels, High C vs Low C overlaid
# ==============================================================================
hc_colors = ['#2166ac', '#4393c3', '#92c5de']
lc_colors = ['#b2182b', '#d6604d', '#f4a582']

fig4, axes4 = plt.subplots(2, 3, figsize=(15, 8), sharey='row')
fig4.suptitle('Centre-row line profiles: High C vs Low C', fontsize=FS + 2)

for i, (hc_r, lc_r, gl) in enumerate(zip(hc, lc, group_labels)):
    xP_nm_hc = hc_r['xP'] * 1e9
    xP_nm_lc = lc_r['xP'] * 1e9
    cy_hc = hc_r['I_arr'].shape[0] // 2
    cy_lc = lc_r['I_arr'].shape[0] // 2

    ax = axes4[0, i]
    ax.plot(xP_nm_hc, hc_r['I_arr'][cy_hc, :],
            color=hc_colors[i], linewidth=1.4, label='High C')
    ax.plot(xP_nm_lc, lc_r['I_arr'][cy_lc, :],
            color=lc_colors[i], linewidth=1.4, label='Low C', linestyle='--')
    ax.set_title(f'Intensity: {gl}', fontsize=FS)
    ax.set_xlabel('x  (nm)', fontsize=FS)
    ax.set_xlim(min(xP_nm_hc[0], xP_nm_lc[0]), max(xP_nm_hc[-1], xP_nm_lc[-1]))
    ax.axvline(0, color='gray', linestyle=':', linewidth=0.8)
    ax.tick_params(labelsize=FS - 1)
    ax.grid(axis='y', linestyle='--', alpha=0.4)

    ax = axes4[1, i]
    ax.plot(xP_nm_hc, hc_r['P'][cy_hc, :],
            color=hc_colors[i], linewidth=1.4, label='High C')
    ax.plot(xP_nm_lc, lc_r['P'][cy_lc, :],
            color=lc_colors[i], linewidth=1.4, label='Low C', linestyle='--')
    ax.set_title(f'Phase: {gl}', fontsize=FS)
    ax.set_xlabel('x  (nm)', fontsize=FS)
    ax.set_xlim(min(xP_nm_hc[0], xP_nm_lc[0]), max(xP_nm_hc[-1], xP_nm_lc[-1]))
    ax.axvline(0, color='gray', linestyle=':', linewidth=0.8)
    ax.tick_params(labelsize=FS - 1)
    ax.grid(axis='y', linestyle='--', alpha=0.4)

axes4[0, 0].set_ylabel('Intensity  (arb. u.)', fontsize=FS)
axes4[1, 0].set_ylabel('Phase  (rad)', fontsize=FS)

from matplotlib.lines import Line2D
lp_handles = [
    Line2D([0], [0], color=hc_colors[0], linewidth=1.5, label='High C'),
    Line2D([0], [0], color=lc_colors[0], linewidth=1.5, linestyle='--', label='Low C'),
]
fig4.legend(handles=lp_handles, fontsize=FS, loc='lower center',
            ncol=2, bbox_to_anchor=(0.5, -0.03))
plt.tight_layout(rect=[0, 0.04, 1, 1])
if SAVE:
    plt.savefig(dir_path + 'line_profiles_hc_vs_lc.svg', bbox_inches='tight')
    print("Saved → line_profiles_hc_vs_lc.svg")
plt.show()


# ==============================================================================
# COMBINED LINE PROFILES – all images on two panels
# ==============================================================================
fig5, axes5 = plt.subplots(1, 2, figsize=(14, 5))
fig5.suptitle('Centre-row line profiles – all images', fontsize=FS + 2)

ax_I = axes5[0]
ax_P = axes5[1]
ax_I.set_title('Intensity', fontsize=FS)
ax_P.set_title('Phase', fontsize=FS)
ax_I.set_xlabel('x  (nm)', fontsize=FS)
ax_P.set_xlabel('x  (nm)', fontsize=FS)
ax_I.set_ylabel('Intensity  (arb. u.)', fontsize=FS)
ax_P.set_ylabel('Phase  (rad)', fontsize=FS)

for i, (hc_r, lc_r, gl) in enumerate(zip(hc, lc, group_labels)):
    cy_hc    = hc_r['I_arr'].shape[0] // 2
    cy_lc    = lc_r['I_arr'].shape[0] // 2
    xP_nm_hc = hc_r['xP'] * 1e9
    xP_nm_lc = lc_r['xP'] * 1e9

    ax_I.plot(xP_nm_hc, hc_r['I_arr'][cy_hc, :],
              color=hc_colors[i], linewidth=1.4, label=f'{gl} High C')
    ax_I.plot(xP_nm_lc, lc_r['I_arr'][cy_lc, :],
              color=lc_colors[i], linewidth=1.4, label=f'{gl} Low C', linestyle='--')

    ax_P.plot(xP_nm_hc, hc_r['P'][cy_hc, :],
              color=hc_colors[i], linewidth=1.4, label=f'{gl} High C')
    ax_P.plot(xP_nm_lc, lc_r['P'][cy_lc, :],
              color=lc_colors[i], linewidth=1.4, label=f'{gl} Low C', linestyle='--')

for ax in axes5:
    ax.axvline(0, color='gray', linestyle=':', linewidth=0.8)
    ax.tick_params(labelsize=FS - 1)
    ax.grid(axis='y', linestyle='--', alpha=0.4)

fig5.legend(handles=ax_I.get_legend_handles_labels()[0],
            labels=ax_I.get_legend_handles_labels()[1],
            fontsize=FS - 1, loc='lower center', ncol=3,
            bbox_to_anchor=(0.5, -0.06))
plt.tight_layout(rect=[0, 0.07, 1, 1])
if SAVE:
    plt.savefig(dir_path + 'line_profiles_all.svg', bbox_inches='tight')
    print("Saved → line_profiles_all.svg")
plt.show()


# ==============================================================================
# FINAL FIGURE – all datasets, x-axis = SSA size
# x positions: 0 = '45×35 μm²' (High C), 1 = '200×200 μm²' (Low C)
# Marker = aperture (a1/a2/a3), Colour = modality (black/red)
# One figure-level legend
# ==============================================================================
SSA_LABELS = ['45×35', '200×200']
SSA_X      = [0, 1]

if analyse == 'both':
    metric_defs_final = [
        ('I_michelson',    'I_michelson_sem',    'P_michelson',    'P_michelson_sem',
         'Michelson C',        'Michelson Contrast ± SEM'),
        ('I_NILS',         'I_NILS_sem',         'P_NILS',         'P_NILS_sem',
         'NILS / π',           'NILS ± SEM'),
        ('I_rms_contrast', 'I_rms_contrast_sem', 'P_rms_contrast', 'P_rms_contrast_sem',
         '$C_{\mathrm{RMS}}$', 'RMS Contrast ± SEM'),
        ('I_composite_C',  'I_composite_sem',    'P_composite_C',  'P_composite_sem',
         '$C_{\mathrm{C}}$',   'Composite Contrast ± SEM'),
    ]
    n_panels = len(metric_defs_final)
    fig6, axes6 = plt.subplots(1, n_panels, figsize=(5 * n_panels, 6))
    fig6.suptitle('All datasets – SSA size comparison', fontsize=FS + 2)

    for ax, (Im, Ie, Pm, Pe, ylabel, title) in zip(axes6, metric_defs_final):
        for i, (hc_r, lc_r) in enumerate(zip(hc, lc)):
            mk = AP_MARKERS[i]
            ax.errorbar(SSA_X[0], hc_r[Im], yerr=hc_r[Ie],
                        fmt=mk, color=I_COLOR, ecolor=I_COLOR,
                        mfc=I_COLOR, capsize=5, markersize=MS, linewidth=1.5)
            ax.errorbar(SSA_X[1], lc_r[Im], yerr=lc_r[Ie],
                        fmt=mk, color=I_COLOR, ecolor=I_COLOR,
                        mfc=I_COLOR, capsize=5, markersize=MS, linewidth=1.5)
            ax.errorbar(SSA_X[0], hc_r[Pm], yerr=hc_r[Pe],
                        fmt=mk, color=P_COLOR, ecolor=P_COLOR,
                        mfc=P_COLOR, capsize=5, markersize=MS, linewidth=1.5)
            ax.errorbar(SSA_X[1], lc_r[Pm], yerr=lc_r[Pe],
                        fmt=mk, color=P_COLOR, ecolor=P_COLOR,
                        mfc=P_COLOR, capsize=5, markersize=MS, linewidth=1.5)
            # if i == 0:
            #     ax.set_ylim([0.999,1.0])
        ax.set_xticks(SSA_X)
        ax.set_xticklabels(SSA_LABELS, fontsize=FS)
        ax.set_xlabel(r'SSA size  [μm]', fontsize=FS)
        ax.set_ylabel(ylabel, fontsize=FS)
        ax.set_title(title, fontsize=FS)
        ax.tick_params(labelsize=FS - 1)
        ax.grid(axis='y', linestyle='--', alpha=0.4)
        # if 'ichelson' in title:
            # _tight_ylim(ax)

else:
    pfx   = 'I_' if analyse == 'I' else 'P_'
    color = I_COLOR if analyse == 'I' else P_COLOR
    metric_defs_final = [
        (f'{pfx}michelson',    f'{pfx}michelson_sem',    'Michelson C',        'Michelson Contrast ± SEM'),
        (f'{pfx}NILS',         f'{pfx}NILS_sem',         'NILS / π',           'NILS ± SEM'),
        (f'{pfx}rms_contrast', f'{pfx}rms_contrast_sem', '$C_{\mathrm{RMS}}$', 'RMS Contrast ± SEM'),
        (f'{pfx}composite_C',  f'{pfx}composite_sem',    '$C_{\mathrm{C}}$',   'Composite Contrast ± SEM'),
    ]
    n_panels = len(metric_defs_final)
    fig6, axes6 = plt.subplots(1, n_panels, figsize=(5 * n_panels, 6))
    fig6.suptitle('All datasets – SSA size comparison', fontsize=FS + 2)

    for ax, (metric, err, ylabel, title) in zip(axes6, metric_defs_final):
        for i, (hc_r, lc_r) in enumerate(zip(hc, lc)):
            mk = AP_MARKERS[i]
            ax.errorbar(SSA_X[0], hc_r[metric], yerr=hc_r[err],
                        fmt=mk, color=color, ecolor=color,
                        mfc=color, capsize=5, markersize=MS, linewidth=1.5)
            ax.errorbar(SSA_X[1], lc_r[metric], yerr=lc_r[err],
                        fmt=mk, color=color, ecolor=color,
                        mfc=color, capsize=5, markersize=MS, linewidth=1.5)
        ax.set_xticks(SSA_X)
        ax.set_xticklabels(SSA_LABELS, fontsize=FS)
        ax.set_xlabel(r'SSA size  [μm]', fontsize=FS)
        ax.set_ylabel(ylabel, fontsize=FS)
        ax.set_title(title, fontsize=FS)
        ax.tick_params(labelsize=FS - 1)
        ax.grid(axis='y', linestyle='--', alpha=0.4)
        if 'ichelson' in title:
            _tight_ylim(ax)

fig6.legend(handles=_make_ssa_legend(), fontsize=FS,
            loc='lower center', ncol=5, bbox_to_anchor=(0.5, -0.06))
plt.tight_layout(rect=[0, 0.08, 1, 1])
if SAVE:
    plt.savefig(dir_path + 'metrics_all_datasets.svg', bbox_inches='tight')
    print("Saved → metrics_all_datasets.svg")
plt.show()