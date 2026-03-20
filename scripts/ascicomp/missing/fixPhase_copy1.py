import h5py
import shutil
import ptypy
from ptypy.utils import ortho, rmphaseramp
import numpy as np

def remove_phase_ramp(
    filePath, 
    savePath,
    crop=None,
    obj=True,
    probe=False,
    show=False
):
    """
    1. Copies the file from 'filePath' to 'savePath'.
    2. Optionally removes the phase ramp for the object (/content/obj/Sscan_00G00/data).
    3. Optionally removes the phase ramp for the probe (/content/probe/Sscan_00G00/data).
       This includes the orthogonalization step for multi-mode probes.
    4. Writes the corrected data to 'savePath'.
    """

    # 1) Copy the original file to the new file so we keep the original intact
    shutil.copy2(filePath, savePath)

    # 2) Open original file in read-only mode, new file in read+write mode
    with h5py.File(filePath, 'r') as f_orig, \
         h5py.File(savePath, 'r+') as f_new:

        # =========== If removing phase ramp from the object =========== 
        if obj:
            
            # Read the object dataset
            ob = f_orig['/content/obj/Sscan_00G00/data'][()]
            ob = np.squeeze(ob)
            print(f"Object shape:   {np.shape(np.squeeze(ob))}")
            NY,NX = np.shape(np.squeeze(ob))
            if crop:
                ob_crop = ob[NY//2 - crop//2: NY//2 + crop//2, NX//2 - crop//2: NX//2 + crop//2]
                print(f"Cropped object shape:   {np.shape(ob_crop)}")
                # Obtain the phase ramp of cropped area
                ob_corrected,PR = rmphaseramp(ob_crop,return_phaseramp=True)#,weight='abs')
                PR_scaled = extend_complex_phase_ramp(PR, (NY, NX))
                ob_corrected = np.squeeze(ob)*PR_scaled
            else:
                # Remove the phase ramp
                ob_corrected = rmphaseramp(np.squeeze(ob))
            if show:
                import matplotlib.pyplot as plt
                plt.figure()
                plt.imshow(np.angle(PR))
                plt.colorbar()
                plt.show()
                plt.figure()
                plt.imshow(np.angle(PR_scaled))
                plt.colorbar()
                plt.show()
                from plot_complex_colourbar import plotComplexWithColorbar
                px = f_orig['/content/obj/Sscan_00G00/_psize'][()][0]
                plotComplexWithColorbar(ob,px=[px,px],title='before',save_path=None)
                plotComplexWithColorbar(ob_corrected,px=[px,px],title='after',save_path=None)
            # Overwrite the dataset in the new file
            f_new['/content/obj/Sscan_00G00/data'][...] = ob_corrected

        # =========== If removing phase ramp from the probe ===========
        if probe:
            # Read the probe dataset
            pr = f_orig['/content/probe/Sscan_00G00/data'][()]

            # Decompose into amplitude + orthonormal modes
            # `ortho()` returns (amplitudes, list_of_modes)
            amp, mode_list = ortho(pr)

            # Remove phase ramp from each mode individually
            #corrected_modes = []
            pr_corrected = np.zeros_like(pr,dtype=complex)
            for i,mode in enumerate(pr):
                pr_corrected[i] = rmphaseramp(mode)#,weight=amp[i]) 
                #corrected_modes.append(rmphaseramp(mode),weight=amp[)

            # Manually reassemble the corrected modes back into the original shape:
            #   pr_corrected[i] = amp[i] * corrected_modes[i]
            #pr_corrected = np.zeros_like(pr, dtype=complex)  # ensure complex dtype
            #for i, m in enumerate(corrected_modes):
            #    print(amp[i])
            #    print(m)
            #    pr_corrected[i] = (amp[i], m)

            # Overwrite the probe dataset in the new file
            f_new['/content/probe/Sscan_00G00/data'][...] = pr_corrected

    print(f"Phase ramp removal is complete.\nNew file saved at: {savePath}")

def extend_complex_phase_ramp(phase_small, new_shape):
    """
    Extend a complex-valued phase ramp to a larger array while
    preserving the center region exactly.

    Parameters
    ----------
    phase_small : 2D complex ndarray
        exp(1j * phase) array containing a phase ramp
    new_shape : tuple (Ny, Nx)
        Desired output shape

    Returns
    -------
    phase_large : 2D complex ndarray
        Extended phase ramp, same gradient, larger size
    """

    Ny_s, Nx_s = phase_small.shape
    Ny, Nx = new_shape

    # unwrap phase before differentiation
    phi = np.unwrap(np.unwrap(np.angle(phase_small), axis=0), axis=1)

    # estimate average gradients (rad / pixel)
    gy, gx = np.gradient(phi)
    gx = gx.mean()
    gy = gy.mean()

    # coordinate grid centered at zero
    y = np.arange(Ny) - Ny // 2
    x = np.arange(Nx) - Nx // 2
    X, Y = np.meshgrid(x, y)

    # reconstruct phase ramp
    phi_large = gx * X + gy * Y

    # align phase so center matches exactly
    sy, sx = Ny_s // 2, Nx_s // 2
    cy, cx = Ny // 2, Nx // 2
    phi_large += phi[sy, sx] - phi_large[cy, cx]

    # return complex field
    return np.exp(1j * phi_large)

def test():
    # Example usage:

    # Path to original file
    original_path = ('/user/home/ptypy-0.5.0/jk/experiments/SOLEIL_telePtycho/15x5_4um_512/dumps/recon_15x5_4um_512_DM_0140.ptyr')
    # Where to save the corrected file
    new_path = ('/user/home/ptypy-0.5.0/jk/experiments/SOLEIL_telePtycho/15x5_4um_512/best/recon_15x5_4um_512_DM_0140_correctedObj.ptyr')

    # Example: remove phase ramp from both object and probe
    remove_phase_ramp(
        filePath=original_path,
        savePath=new_path,
        obj=True,
        probe=False
    )    
if __name__ == '__main__':
    pass
    # test()
