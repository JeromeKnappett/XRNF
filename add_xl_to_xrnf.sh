#!/bin/bash
# Run this from ~/XRNF on computer 2
# Maps:
#   /user/home/opt/xl/xl/experiments/*  --> ~/XRNF/simulations/
#   everything else in /xl/xl/          --> ~/XRNF/scripts/  (preserving subdirs)
# Only .py and .csv files are included; wfactions.nils/ is excluded.

set -e

REPO=~/XRNF
SRC=/user/home/opt/xl/xl

echo "=== Copying simulation experiments ==="
mkdir -p "$REPO/simulations"
rsync -av \
  --include='*/' \
  --include='*.py' \
  --include='*.csv' \
  --exclude='*' \
  "$SRC/experiments/" "$REPO/simulations/"

echo ""
echo "=== Copying all other scripts ==="
mkdir -p "$REPO/scripts"
rsync -av \
  --exclude='__pycache__/' \
  --exclude='experiments/' \
  --exclude='wfactions.nils/' \
  --include='*/' \
  --include='*.py' \
  --include='*.csv' \
  --exclude='*' \
  "$SRC/" "$REPO/scripts/"

echo ""
echo "=== Staging all changes ==="
cd "$REPO"
git add simulations/ scripts/

echo ""
echo "=== Summary ==="
git diff --cached --stat | tail -10

echo ""
echo "Ready to commit. Run:"
echo "  cd ~/XRNF && git commit -m 'Add xl simulations and utility scripts from computer2'"
