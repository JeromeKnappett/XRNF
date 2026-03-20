import h5py
import shutil
import ptypy
from ptypy.utils import ortho, rmphaseramp
import numpy as np

def remove_phase_ramp(
    filePath, 
    savePath,
    obj=True,
    probe=False
):
    """
    1. Copies the file from 'filePath' to 'savePath'.
    2. Optionally removes the phase ramp for the object (/content/obj/Sscan00G00/data).
    3. Optionally removes the phase ramp for the probe (/content/probe/Sscan00G00/data).
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
            ob = f_orig['/content/obj/Sscan00G00/data'][()]
            # Remove the phase ramp
            ob_corrected = rmphaseramp(ob)
            # Overwrite the dataset in the new file
            f_new['/content/obj/Sscan00G00/data'][...] = ob_corrected

        # =========== If removing phase ramp from the probe ===========
        if probe:
            # Read the probe dataset
            pr = f_orig['/content/probe/Sscan00G00/data'][()]

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
            f_new['/content/probe/Sscan00G00/data'][...] = pr_corrected

    print(f"Phase ramp removal is complete.\nNew file saved at: {savePath}")

def test():
    # Example usage:

    # Path to original file
    original_path = (
        "/data/xfm/22353/analysis/eiger/SXDM/tele_fzp/173674_46/dumps/"
        "ptypy_173674_46_256_roi_9995_gpu/ptypy_173674_46_256_roi_9995_gpu_DM_0300.ptyr"
    )
    # Where to save the corrected file
    new_path = (
        "/data/xfm/22353/analysis/eiger/SXDM/tele_fzp/173674_46/dumps/"
        "ptypy_173674_46_256_roi_9995_gpu/ptypy_173674_46_256_roi_9995_gpu_DM_0300_corrected.ptyr"
    )

    # Example: remove phase ramp from both object and probe
    remove_phase_ramp(
        filePath=original_path,
        savePath=new_path,
        obj=False,
        probe=False
    )    
if __name__ == '__main__':
    pass
    #test()
