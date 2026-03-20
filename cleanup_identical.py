"""
XRNF Identical Duplicate Cleanup
==================================
Finds all identical duplicate files (same md5) and removes redundant copies,
keeping the best canonical version of each.

Run with --dry-run first to preview, then run without to apply.

Usage:
    python cleanup_identical.py --dry-run
    python cleanup_identical.py
"""

import os
import re
import hashlib
import argparse
from pathlib import Path
from collections import defaultdict

# === Configuration ===
REPO_ROOT = Path(__file__).parent
SEARCH_DIRS = [
    "scripts/ascicomp",
    "scripts/ascicomp/missing",
    "scripts/homecomp",
    "scripts/homecomp/local/clean",
    "scripts/homecomp/wfactions",
    "scripts/ascicomp2",
    "experiments/ascicomp",
    "experiments/homecomp",
    "loose/homecomp",
]

EXTENSIONS = {'.py', '.csv'}

# Priority order for which copy to keep (lower = higher priority)
# Files matching these patterns are preferred as the canonical copy
KEEP_PRIORITY = [
    # Prefer non-copy, non-missing, non-old versions
    lambda p: 0 if '_copy' not in p.stem and 'missing' not in str(p) else 1,
    # Prefer ascicomp over homecomp over ascicomp2
    lambda p: 0 if 'ascicomp/' in str(p) and 'ascicomp2' not in str(p) else
              1 if 'homecomp' in str(p) else
              2 if 'ascicomp2' in str(p) else 3,
    # Prefer shorter paths (less nested)
    lambda p: len(str(p).split(os.sep)),
]

def md5(filepath):
    h = hashlib.md5()
    with open(filepath, 'rb') as f:
        h.update(f.read())
    return h.hexdigest()

def score(path):
    """Lower score = higher priority = keep this one."""
    return tuple(fn(path) for fn in KEEP_PRIORITY)

def relative(path):
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)

# === Parse args ===
parser = argparse.ArgumentParser()
parser.add_argument('--dry-run', action='store_true',
                    help='Preview changes without deleting anything')
args = parser.parse_args()

dry_run = args.dry_run
if dry_run:
    print("=== DRY RUN MODE — no files will be deleted ===\n")
else:
    print("=== LIVE MODE — files will be deleted ===\n")

# === Collect all files ===
print("Scanning repository...")
all_files = []
for d in SEARCH_DIRS:
    dirpath = REPO_ROOT / d
    if not dirpath.exists():
        continue
    for f in dirpath.rglob('*'):
        if f.is_file() and f.suffix in EXTENSIONS:
            if '__pycache__' not in str(f):
                all_files.append(f)

print(f"Found {len(all_files)} files.\n")

# === Group by filename, then by md5 ===
by_name = defaultdict(list)
for f in all_files:
    by_name[f.name].append(f)

identical_groups = []
for name, files in by_name.items():
    if len(files) < 2:
        continue
    # Group by md5
    by_hash = defaultdict(list)
    for f in files:
        by_hash[md5(f)].append(f)
    for hash_val, dupes in by_hash.items():
        if len(dupes) > 1:
            identical_groups.append((name, hash_val, dupes))

print(f"Found {len(identical_groups)} groups of identical duplicates.\n")
print("=" * 60)

# === Process each group ===
to_delete = []
keep_log = []

for name, hash_val, dupes in sorted(identical_groups):
    # Sort by priority score — lowest score = keep
    sorted_dupes = sorted(dupes, key=score)
    keep = sorted_dupes[0]
    delete = sorted_dupes[1:]

    keep_log.append((name, keep, delete))
    to_delete.extend(delete)

    print(f"\n{name} (md5: {hash_val[:8]})")
    print(f"  KEEP:   {relative(keep)}")
    for d in delete:
        print(f"  DELETE: {relative(d)}")

print("\n" + "=" * 60)
print(f"\nSummary: {len(to_delete)} files to delete across {len(identical_groups)} groups")

if dry_run:
    print("\nDry run complete. Run without --dry-run to apply changes.")
else:
    print("\nProceeding with deletion...")
    deleted = 0
    errors = 0
    for f in to_delete:
        try:
            f.unlink()
            print(f"  Deleted: {relative(f)}")
            deleted += 1
        except Exception as e:
            print(f"  ERROR deleting {relative(f)}: {e}")
            errors += 1
    print(f"\nDone. Deleted {deleted} files. Errors: {errors}")
    print("\nRemember to run:")
    print("  git add -A")
    print("  git commit -m 'Remove identical duplicate files'")
    print("  git push origin main")

# === Write cleanup log ===
log_path = REPO_ROOT / "cleanup_log.md"
with open(log_path, 'w', encoding='utf-8') as f:
    f.write("# Identical Duplicate Cleanup Log\n\n")
    f.write(f"Total groups processed: {len(identical_groups)}\n")
    f.write(f"Total files removed: {len(to_delete)}\n\n")
    f.write("---\n\n")
    for name, keep, deleted in keep_log:
        f.write(f"## `{name}`\n")
        f.write(f"- **Kept:** `{relative(keep)}`\n")
        for d in deleted:
            f.write(f"- **Removed:** `{relative(d)}`\n")
        f.write("\n")

print(f"\nLog written to: cleanup_log.md")
