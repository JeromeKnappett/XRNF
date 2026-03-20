#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 13 15:10:44 2025

@author: -
"""

import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations
from skimage.metrics import structural_similarity as ssim
import tifffile
# ---------------- Metric Functions ----------------

def compute_mse(img1, img2):
    return np.mean((img1 - img2) ** 2)

def compute_ssim(img1, img2):
    return ssim(img1, img2, data_range=img2.max() - img2.min())

def compute_fidelity(img1, img2):
    img1_flat = img1.flatten()
    img2_flat = img2.flatten()
    numerator = np.dot(img1_flat, img2_flat)
    denominator = np.linalg.norm(img1_flat) * np.linalg.norm(img2_flat)
    return numerator / denominator if denominator != 0 else 0

# ---------------- Normalize MSE ----------------

def normalize_mse(mse_vals):
    arr = np.array(mse_vals)
    min_val = np.min(arr)
    max_val = np.max(arr)
    if max_val == min_val:
        return [1.0] * len(arr)
    norm = (arr - min_val) / (max_val - min_val)
    return (1 - norm).tolist()  # Inverted: higher = better

# ---------------- Main Function ----------------

def analyse_variation(images):
    """
    Show intra- and inter-condition variation using MSE (normalized), SSIM, and Fidelity.
    Each plot has lines for each grating/condition and points for each pairwise comparison.
    """

    if len(images) != 9:
        raise ValueError("Expected 9 images (3 conditions × 3 gratings)")

    images_by_condition = [
        images[0:3],  # small SLH #1
        images[3:6],  # small SLV
        images[6:9],  # small SLH #2
    ]

    condition_labels = ['small SLH #1', 'small SLV', 'small SLH #2']
    grating_labels = ['G1', 'G2', 'G3']
    pair_labels = ['Pair 1', 'Pair 2', 'Pair 3']  # Used for consistent x-axis

    metric_funcs = {
        'MSE': compute_mse,
        'SSIM': compute_ssim,
        # 'Fidelity': compute_fidelity
    }

    similarity_metrics = {
        'MSE': False,
        'SSIM': True,
        # 'Fidelity': True
    }

    # Store all results for final combined plot
    all_metrics = {
        'MSE': {'intra': [], 'inter': []},
        'SSIM': {'intra': [], 'inter': []},
        # 'Fidelity': {'intra': [], 'inter': []}
    }

    fig, axs = plt.subplots(2, 2, figsize=(14, 12))
    fig.suptitle("Variation in Diffraction Patterns (Similarity Metrics)", fontsize=18)

    for row_idx, (metric_name, func) in enumerate(metric_funcs.items()):
        is_similarity = similarity_metrics[metric_name]

        # ---- Intra-condition (same condition, diff gratings) ----
        intra_lines = []
        for cond in range(3):
            triplet = images_by_condition[cond]
            vals = []
            for i, j in combinations(range(3), 2):
                val = func(triplet[i], triplet[j])
                vals.append(val)
            intra_lines.append(vals)

        # ---- Inter-condition (same grating, diff conditions) ----
        inter_lines = []
        for g in range(3):
            triplet = [images_by_condition[cond][g] for cond in range(3)]
            vals = []
            for i, j in combinations(range(3), 2):
                val = func(triplet[i], triplet[j])
                vals.append(val)
            inter_lines.append(vals)

        # ---- Normalize MSE ----
        if metric_name == 'MSE':
            all_vals = sum(intra_lines + inter_lines, [])
            norm_vals = normalize_mse(all_vals)
            intra_lines = [norm_vals[i*3:(i+1)*3] for i in range(3)]
            inter_lines = [norm_vals[9 + i*3:9 + (i+1)*3] for i in range(3)]

        # ---- Store for later ----
        all_metrics[metric_name]['intra'] = intra_lines
        all_metrics[metric_name]['inter'] = inter_lines

        # ---- Plot Intra ----
        ax_intra = axs[row_idx, 0]
        for idx, vals in enumerate(intra_lines):
            ax_intra.plot(range(3), vals, marker='o', label=condition_labels[idx])
        ax_intra.set_title(f"Intra-Condition Variation: {metric_name}")
        ax_intra.set_xticks(range(3))
        ax_intra.set_xticklabels(['G1-G2', 'G1-G3', 'G2-G3'])
        ax_intra.set_ylabel("Similarity" if is_similarity else "Normalized Distance")
        ax_intra.grid(True)
        ax_intra.legend()

        # ---- Plot Inter ----
        ax_inter = axs[row_idx, 1]
        for idx, vals in enumerate(inter_lines):
            ax_inter.plot(range(3), vals, marker='s', label=grating_labels[idx])
        ax_inter.set_title(f"Inter-Condition Variation: {metric_name}")
        ax_inter.set_xticks(range(3))
        ax_inter.set_xticklabels(['C1-C2', 'C1-C3', 'C2-C3'])
        ax_inter.set_ylabel("Similarity" if is_similarity else "Normalized Distance")
        ax_inter.grid(True)
        ax_inter.legend()

        # ax_intra.set_yscale('log')
        # ax_inter.set_yscale('log')
        
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()

    # ---------------- Combined Plots ----------------

    fig2, axs2 = plt.subplots(1, 2, figsize=(14, 5))
    fig2.suptitle("Comparison of All Metrics", fontsize=16)

    colors = {
        'MSE': 'tab:red',
        'SSIM': 'tab:green',
        'Fidelity': 'tab:blue'
    }

    # ---- Intra combined ----
    for metric_name, data in all_metrics.items():
        # Average across conditions for each pair
        intra_vals = np.array(data['intra'])  # shape (3, 3)
        means = np.mean(intra_vals, axis=0)
        stds = np.std(intra_vals, axis=0)
        axs2[0].errorbar(range(3), means, yerr=stds, fmt='-o', label=metric_name, color=colors[metric_name])
    axs2[0].set_title("Intra-Condition Comparison")
    axs2[0].set_xticks(range(3))
    axs2[0].set_xticklabels(['G1-G2', 'G1-G3', 'G2-G3'])
    axs2[0].set_ylabel("Similarity (Normalized for MSE)")
    axs2[0].legend()
    axs2[0].grid(True)

    # ---- Inter combined ----
    for metric_name, data in all_metrics.items():
        inter_vals = np.array(data['inter'])  # shape (3, 3)
        means = np.mean(inter_vals, axis=0)
        stds = np.std(inter_vals, axis=0)
        axs2[1].errorbar(range(3), means, yerr=stds, fmt='-s', label=metric_name, color=colors[metric_name])
    axs2[1].set_title("Inter-Condition Comparison")
    axs2[1].set_xticks(range(3))
    axs2[1].set_xticklabels(['C1-C2', 'C1-C3', 'C2-C3'])
    axs2[1].set_ylabel("Similarity (Normalized for MSE)")
    axs2[1].legend()
    axs2[1].grid(True)

    plt.tight_layout()
    plt.show()

    
if __name__ == '__main__':
    dir_path = '/data/xfm/22353/HERMES/data/UP_20242172/2025-09-27/'
    scan_nums = [f"20250927_0{n}" for n in range(23,32)]
    imgs = [tifffile.imread(f"{dir_path}Time_{n}_processed.tif") for n in scan_nums] 
    # print(np.shape(imgs))
    analyse_variation(imgs)