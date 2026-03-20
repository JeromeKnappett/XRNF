"""
XRNF Codebase Duplicate Audit
==============================
Finds duplicate and near-duplicate scripts across all computer branches.
Groups by: identical names, near-identical names (e.g. _new, _JK, _2 suffixes).
Outputs a report: duplicate_audit_report.md
"""

import os
import re
import hashlib
import difflib
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

# Suffixes/patterns that indicate a variant of another file
VARIANT_PATTERNS = [
    r'_new$',
    r'_old$',
    r'_JK$',
    r'_jk$',
    r'_home$',
    r'_dev$',
    r'_test$',
    r'_TEST$',
    r'_clean$',
    r'_backup$',
    r'_copy\d*$',
    r'_\d+$',
    r'\d+$',
    r'_[A-Z]$',
    r'OLD$',
    r'NEW$',
    r'_TEST\d*$',
]

EXTENSIONS = {'.py', '.csv'}

# === Helpers ===

def md5(filepath):
    h = hashlib.md5()
    with open(filepath, 'rb') as f:
        h.update(f.read())
    return h.hexdigest()

def strip_variant_suffix(stem):
    """Strip known variant suffixes to get a base name."""
    for pattern in VARIANT_PATTERNS:
        stripped = re.sub(pattern, '', stem)
        if stripped != stem and stripped:
            return stripped
    return stem

def count_diff_lines(path1, path2):
    """Return number of differing lines between two text files."""
    try:
        with open(path1, 'r', errors='ignore') as f1:
            lines1 = f1.readlines()
        with open(path2, 'r', errors='ignore') as f2:
            lines2 = f2.readlines()
        diff = list(difflib.unified_diff(lines1, lines2))
        changed = sum(1 for l in diff if l.startswith('+') or l.startswith('-'))
        return changed, len(lines1), len(lines2)
    except Exception:
        return -1, 0, 0

def classify_diff(changed_lines, total_lines):
    if changed_lines == 0:
        return "IDENTICAL"
    if total_lines == 0:
        return "UNKNOWN"
    pct = changed_lines / max(total_lines, 1) * 100
    if pct < 5:
        return "NEARLY IDENTICAL (<5% different)"
    elif pct < 25:
        return "MINOR DIFFERENCES (<25% different)"
    else:
        return "SIGNIFICANTLY DIFFERENT"

def relative(path):
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)

# === Collect all files ===

print("Scanning repository...")
all_files = []
for d in SEARCH_DIRS:
    dirpath = REPO_ROOT / d
    if not dirpath.exists():
        print(f"  Skipping (not found): {d}")
        continue
    for f in dirpath.rglob('*'):
        if f.is_file() and f.suffix in EXTENSIONS:
            if '__pycache__' not in str(f):
                all_files.append(f)

print(f"Found {len(all_files)} files across {len(SEARCH_DIRS)} directories.\n")

# === Group by exact name ===

by_name = defaultdict(list)
for f in all_files:
    by_name[f.name].append(f)

exact_duplicates = {k: v for k, v in by_name.items() if len(v) > 1}

# === Group by base name (after stripping variant suffixes) ===

by_base = defaultdict(list)
for f in all_files:
    base = strip_variant_suffix(f.stem) + f.suffix
    by_base[base].append(f)

# Near-duplicates: same base name but different actual names
near_duplicates = {}
for base, files in by_base.items():
    # Only include if there are files with DIFFERENT names mapping to this base
    names = set(f.name for f in files)
    if len(names) > 1:
        near_duplicates[base] = files

# === Build report ===

report_lines = []
report_lines.append("# XRNF Duplicate Audit Report\n")
report_lines.append(f"Total files scanned: {len(all_files)}\n")
report_lines.append(f"Files with exact name duplicates: {sum(len(v) for v in exact_duplicates.values())}\n")
report_lines.append(f"Near-duplicate groups (variant names): {len(near_duplicates)}\n")
report_lines.append("\n---\n")

# --- Section 1: Exact duplicates ---
report_lines.append("## 1. Exact Name Duplicates\n")
report_lines.append("Same filename found in multiple locations.\n\n")

identical_count = 0
nearly_count = 0
minor_count = 0
significant_count = 0

for name, files in sorted(exact_duplicates.items()):
    hashes = [md5(f) for f in files]
    unique_hashes = set(hashes)

    if len(unique_hashes) == 1:
        status = "[IDENTICAL]"
        identical_count += 1
    else:
        # Compare all pairs
        changed, t1, t2 = count_diff_lines(files[0], files[1])
        classification = classify_diff(changed, max(t1, t2))
        status = f"[!]  {classification}"
        if "NEARLY" in classification:
            nearly_count += 1
        elif "MINOR" in classification:
            minor_count += 1
        else:
            significant_count += 1

    report_lines.append(f"### `{name}` — {status}\n")
    for f, h in zip(files, hashes):
        report_lines.append(f"- `{relative(f)}` (md5: `{h[:8]}`)\n")
    report_lines.append("\n")

# --- Section 2: Near-duplicates (variant names) ---
report_lines.append("\n---\n")
report_lines.append("## 2. Near-Duplicate Names (Variant Suffixes)\n")
report_lines.append("Files with names like `script.py`, `script_new.py`, `script2.py` grouped together.\n\n")

for base, files in sorted(near_duplicates.items()):
    # Skip if all files have the same name (already covered above)
    names = set(f.name for f in files)
    if len(names) == 1:
        continue

    report_lines.append(f"### Base: `{base}`\n")
    
    # Compare all unique pairs
    unique_files = []
    seen_paths = set()
    for f in files:
        if str(f) not in seen_paths:
            unique_files.append(f)
            seen_paths.add(str(f))

    for f in unique_files:
        report_lines.append(f"- `{relative(f)}`\n")

    # Diff each pair
    if len(unique_files) >= 2:
        report_lines.append("\n  **Pairwise comparison:**\n")
        for i in range(len(unique_files)):
            for j in range(i+1, len(unique_files)):
                changed, t1, t2 = count_diff_lines(unique_files[i], unique_files[j])
                classification = classify_diff(changed, max(t1, t2))
                report_lines.append(
                    f"  - `{unique_files[i].name}` vs `{unique_files[j].name}`: "
                    f"**{classification}** ({changed} changed lines)\n"
                )
    report_lines.append("\n")

# --- Summary ---
report_lines.insert(4, f"  - Identical: {identical_count}\n")
report_lines.insert(5, f"  - Nearly identical: {nearly_count}\n")
report_lines.insert(6, f"  - Minor differences: {minor_count}\n")
report_lines.insert(7, f"  - Significantly different: {significant_count}\n")

# === Write report ===
output_path = REPO_ROOT / "duplicate_audit_report.md"
with open(output_path, 'w', encoding='utf-8') as f:
    f.writelines(report_lines)

print(f"Report written to: {output_path}")
print(f"\nSummary:")
print(f"  Exact duplicates found: {len(exact_duplicates)} groups")
print(f"    - Identical:              {identical_count}")
print(f"    - Nearly identical:       {nearly_count}")
print(f"    - Minor differences:      {minor_count}")
print(f"    - Significantly different:{significant_count}")
print(f"  Near-duplicate name groups: {len(near_duplicates)}")
