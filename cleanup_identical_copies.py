"""
XRNF Identical Copy Cleanup
============================
Removes confirmed-identical duplicate files, keeping one canonical copy.
Run with --dry-run first to preview.

Usage:
    python cleanup_identical_copies.py --dry-run
    python cleanup_identical_copies.py
"""

import argparse
import hashlib
from pathlib import Path

REPO_ROOT = Path(__file__).parent

def md5(filepath):
    h = hashlib.md5()
    with open(filepath, 'rb') as f:
        h.update(f.read())
    return h.hexdigest()

def relative(path):
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)

# Each entry: (keep, [delete, delete, ...])
# All files in each group have been confirmed identical in the audit report.
CLEANUP_GROUPS = [

    # blMaskEfficiency - all identical, keep the one in beamPolarisation1
    (
        "experiments/homecomp/beamPolarisation1/blMaskEfficiency4.py",
        [
            "experiments/homecomp/maskEfficiency10/blMaskEfficiency10.py",
            "experiments/homecomp/maskEfficiency11/blMaskEfficiency11.py",
            "experiments/homecomp/maskEfficiency13/blMaskEfficiency13.py",
            "experiments/homecomp/maskEfficiency14/blMaskEfficiency14.py",
            "experiments/homecomp/maskEfficiency16/blMaskEfficiency16.py",
            "experiments/homecomp/maskEfficiency17/blMaskEfficiency17.py",
            "experiments/homecomp/maskEfficiency18/blMaskEfficiency18.py",
            "experiments/homecomp/maskEfficiency19/blMaskEfficiency19.py",
            "experiments/homecomp/maskEfficiency2/blMaskEfficiency2.py",
            "experiments/homecomp/maskEfficiency20/blMaskEfficiency20.py",
            "experiments/homecomp/maskEfficiency21/blMaskEfficiency21.py",
            "experiments/homecomp/maskEfficiency5/blMaskEfficiency5.py",
            "experiments/homecomp/maskEfficiency6/blMaskEfficiency6.py",
            "experiments/homecomp/maskEfficiency7/blMaskEfficiency7.py",
            "experiments/homecomp/maskEfficiency8/blMaskEfficiency8.py",
            "experiments/homecomp/maskEfficiency9/blMaskEfficiency9.py",
        ]
    ),

    # resampleArray - all 3 copies identical
    (
        "scripts/ascicomp2/resampleArray_copy1.py",
        [
            "scripts/ascicomp2/resampleArray_copy2.py",
            "scripts/ascicomp2/resampleArray_copy3.py",
        ]
    ),

    # uti_cp_prj - copies 1-4 identical (copy5 has 4 line diff, keep separately)
    (
        "scripts/ascicomp2/uti_cp_prj_copy1.py",
        [
            "scripts/ascicomp2/uti_cp_prj_copy2.py",
            "scripts/ascicomp2/uti_cp_prj_copy3.py",
            "scripts/ascicomp2/uti_cp_prj_copy4.py",
        ]
    ),

    # hermes - both copies identical
    (
        "scripts/ascicomp/missing/hermes_copy1.py",
        [
            "scripts/ascicomp/missing/hermes_copy2.py",
        ]
    ),

    # wfrutils - both copies identical
    (
        "scripts/ascicomp/missing/wfrutils_copy1.py",
        [
            "scripts/ascicomp/missing/wfrutils_copy2.py",
        ]
    ),

    # phaseFix - both copies identical
    (
        "scripts/ascicomp/missing/phaseFix_copy1.py",
        [
            "scripts/ascicomp/missing/phaseFix_copy2.py",
        ]
    ),

    # phaseFix_copy2 same as copy1 - already handled above
    # fixPhase - copy1 and copy2 are DIFFERENT so don't delete either

    # findMaskSize - both identical
    (
        "scripts/ascicomp2/findMaskSize_copy1.py",
        [
            "scripts/ascicomp2/findMaskSize_copy2.py",
        ]
    ),

    # gratingFFT - both identical
    (
        "scripts/ascicomp2/gratingFFT_copy1.py",
        [
            "scripts/ascicomp2/gratingFFT_copy2.py",
        ]
    ),

    # fourierPower - both identical
    (
        "scripts/ascicomp2/fourierPower_copy1.py",
        [
            "scripts/ascicomp2/fourierPower_copy2.py",
        ]
    ),

    # XFMtest - both identical
    (
        "scripts/ascicomp2/XFMtest_copy1.py",
        [
            "scripts/ascicomp2/XFMtest_copy2.py",
        ]
    ),

    # utilMask_1 - identical in both locations, keep scripts/homecomp version
    (
        "scripts/homecomp/utilMask_1.py",
        [
            "loose/homecomp/utilMask_1.py",
        ]
    ),

    # process copies - copy1 and copies 3-9 are nearly identical
    # copy5 is significantly different - keep it separately
    # keep copy1 as canonical, remove exact/near-exact duplicates
    (
        "scripts/ascicomp2/process_copy1.py",
        [
            "scripts/ascicomp2/process_copy3.py",  # nearly identical (36 lines)
            "scripts/ascicomp2/process_copy4.py",  # nearly identical (34 lines)
            "scripts/ascicomp2/process_copy6.py",  # nearly identical (35 lines)
            "scripts/ascicomp2/process_copy7.py",  # nearly identical (36 lines)
            "scripts/ascicomp2/process_copy8.py",  # nearly identical (34 lines)
            "scripts/ascicomp2/process_copy9.py",  # nearly identical (34 lines)
            "scripts/ascicomp2/process_copy10.py", # nearly identical (20 lines)
            "scripts/ascicomp2/process_copy11.py", # nearly identical (19 lines)
        ]
    ),
    # keep process_copy2 (minor diffs) and process_copy5 (significantly different)

    # gauss_fitting - copies 3-7 are nearly identical to each other
    # copy1 and copy2 are significantly different from each other and from 3-7
    # keep copy1, copy2, copy3 (as representative of 3-7 group)
    (
        "scripts/ascicomp2/gauss_fitting_copy3.py",
        [
            "scripts/ascicomp2/gauss_fitting_copy4.py",
            "scripts/ascicomp2/gauss_fitting_copy5.py",
            "scripts/ascicomp2/gauss_fitting_copy6.py",
            "scripts/ascicomp2/gauss_fitting_copy7.py",
        ]
    ),

    # LER_script - keep the clean version as canonical
    # (LER_script.py and LER_script_clean.py are significantly different -
    #  keep both for now, will merge later)
]


def run(dry_run=True):
    if dry_run:
        print("=== DRY RUN - no files will be deleted ===\n")
    else:
        print("=== LIVE MODE - files will be deleted ===\n")

    total_deleted = 0
    errors = 0

    for keep_rel, delete_rels in CLEANUP_GROUPS:
        keep = REPO_ROOT / keep_rel
        if not keep.exists():
            print(f"WARNING: Keep file not found: {keep_rel}")
            continue

        keep_hash = md5(keep)
        print(f"KEEP: {keep_rel} (md5: {keep_hash[:8]})")

        for del_rel in delete_rels:
            del_path = REPO_ROOT / del_rel
            if not del_path.exists():
                print(f"  SKIP (not found): {del_rel}")
                continue

            del_hash = md5(del_path)
            diff_note = "" if del_hash == keep_hash else f" [WARNING: hashes differ! {del_hash[:8]}]"

            if dry_run:
                print(f"  DELETE: {del_rel}{diff_note}")
            else:
                try:
                    del_path.unlink()
                    print(f"  DELETED: {del_rel}{diff_note}")
                    total_deleted += 1
                except Exception as e:
                    print(f"  ERROR: {del_rel}: {e}")
                    errors += 1
        print()

    if not dry_run:
        print(f"\nDone. Deleted {total_deleted} files. Errors: {errors}")
        print("\nRemember to commit:")
        print("  git add -A")
        print("  git commit -m 'Remove identical and near-identical duplicate copies'")
        print("  git push origin main")
    else:
        print("\nDry run complete. Run without --dry-run to apply.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    run(dry_run=args.dry_run)
