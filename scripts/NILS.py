
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

def calculate_mean_nils(profile, w=1.0, dx=1.0, debug_plot=True, distance_tolerance=1.5):
    """
    Calculate mean NILS and average peak-trough distance from a 1D intensity profile,
    ensuring proper peak-trough alternation and reasonable spacing.

    Parameters:
        profile (array-like): 1D intensity profile
        w (float): Physical width of peak (e.g., in microns)
        dx (float): Pixel size (same units as w)
        debug_plot (bool): Show debug plot with annotations
        distance_tolerance (float): Acceptable multiple of w for peak-trough spacing

    Returns:
        mean_nils (float): Mean NILS across all peak sides
        mean_distance (float): Mean peak-to-trough distance (in physical units)
    """
    profile = np.asarray(profile, dtype=np.float64)

    # Replace non-positive values to avoid log issues
    min_positive = np.min(profile[profile > 0])
    profile[profile <= 0] = min_positive * 1e-3

    log_I = np.log(profile)
    dlogI_dx = np.gradient(log_I, dx)

    # Find peaks and troughs
    peaks, _ = find_peaks(profile)
    troughs, _ = find_peaks(-profile)

    # Sanity check: ensure alternating sequence
    sequence = [(pos, 'peak') for pos in peaks] + [(pos, 'trough') for pos in troughs]
    sequence.sort()
    bad_sequence_found = False
    for i in range(1, len(sequence)):
        if sequence[i][1] == sequence[i - 1][1]:
            print(f"⚠️ Warning: Found two consecutive {sequence[i][1]}s at indices {sequence[i - 1][0]}, {sequence[i][0]}")
            bad_sequence_found = True
            break

    nils_values = []
    distances = []
    midpoint_indices = []
    skipped = 0

    for peak in peaks:
        # Find nearest left and right troughs
        left_troughs = troughs[troughs < peak]
        right_troughs = troughs[troughs > peak]

        valid = False

        if len(left_troughs) > 0:
            left = left_troughs[-1]
            dist = (peak - left) * dx
            if dist < distance_tolerance * w:
                mid_left = int(round((peak + left) / 2))
                if 1 <= mid_left < len(profile) - 1:
                    slope_left = dlogI_dx[mid_left]
                    nils_values.append(w * slope_left)
                    distances.append(dist)
                    midpoint_indices.append(mid_left)
                    valid = True

        if len(right_troughs) > 0:
            right = right_troughs[0]
            dist = (right - peak) * dx
            if dist < distance_tolerance * w:
                mid_right = int(round((peak + right) / 2))
                if 1 <= mid_right < len(profile) - 1:
                    slope_right = dlogI_dx[mid_right]
                    nils_values.append(w * slope_right)
                    distances.append(dist)
                    midpoint_indices.append(mid_right)
                    valid = True

        if not valid:
            skipped += 1

    if debug_plot:
        x = np.arange(len(profile)) * dx
        plt.figure(figsize=(10, 4))
        plt.plot(x, profile, label='Intensity Profile', color='blue')
        plt.scatter(x[peaks], profile[peaks], color='red', marker='^', label='Peaks')
        plt.scatter(x[troughs], profile[troughs], color='green', marker='v', label='Troughs')
        plt.scatter(x[midpoint_indices], profile[midpoint_indices], color='orange', marker='x', label='Midpoints')
        plt.xlabel('Position')
        plt.ylabel('Intensity')
        plt.title('NILS Debug Plot')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()
        
        plt.plot(x, log_I, label='Intensity Profile (log)', color='blue')
        plt.plot(x, dlogI_dx/np.max(dlogI_dx), label='Intensity gradient (log)', color='blue')
        plt.scatter(x[peaks], log_I[peaks], color='red', marker='^', label='Peaks')
        plt.scatter(x[troughs], log_I[troughs], color='green', marker='v', label='Troughs')
        plt.scatter(x[midpoint_indices], log_I[midpoint_indices], color='orange', marker='x', label='Midpoints')
        plt.xlabel('Position')
        plt.ylabel('Intensity')
        plt.title('NILS Debug Plot')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    mean_nils = np.mean(np.abs(nils_values)) if nils_values else np.nan
    mean_distance = np.mean(distances) if distances else np.nan

    print(f"✅ Processed {len(peaks)} peaks | Skipped: {skipped} | Valid NILS values: {len(nils_values)}")
    if bad_sequence_found:
        print("⚠️ Note: Peak/trough sequence inconsistency found — consider pre-filtering.")

    return mean_nils, mean_distance

