#!/bin/bash
# Run this from ~/XRNF on computer 2
# Maps:
#   ptypy-0.5.0/jk/experiments/SOLEIL_telePtycho/    --> reconstructions/SOLEIL_telePtycho/185/experiment/
#   ptypy-0.5.0/jk/experiments/SOLEIL_telePtycho_91/ --> reconstructions/SOLEIL_telePtycho/91/experiment/
#   ptypy-0.5.0/jk/*.py                              --> scripts/
#   HERMES/.../scripts/ (excl. pysync-master)        --> scripts/
#   HERMES/.../results/recon_scripts/                --> reconstructions/HERMES_22353/

set -e

REPO=~/XRNF
PTYPY=/user/home/ptypy-0.5.0/jk
HERMES=/data/xfm/22353/HERMES/data/UP_20242172

echo "=== Copying ptypy recon scripts (185 - experiment) ==="
mkdir -p "$REPO/reconstructions/SOLEIL_telePtycho/185/experiment"
rsync -av \
  --include='*/' \
  --include='*.py' \
  --include='*.csv' \
  --exclude='*' \
  "$PTYPY/experiments/SOLEIL_telePtycho/" "$REPO/reconstructions/SOLEIL_telePtycho/185/experiment/"

echo ""
echo "=== Copying ptypy recon scripts (91 - experiment) ==="
mkdir -p "$REPO/reconstructions/SOLEIL_telePtycho/91/experiment"
rsync -av \
  --include='*/' \
  --include='*.py' \
  --include='*.csv' \
  --exclude='*' \
  "$PTYPY/experiments/SOLEIL_telePtycho_91/" "$REPO/reconstructions/SOLEIL_telePtycho/91/experiment/"

echo ""
echo "=== Creating simulation placeholders ==="
touch "$REPO/reconstructions/SOLEIL_telePtycho/185/simulation/.gitkeep"
touch "$REPO/reconstructions/SOLEIL_telePtycho/91/simulation/.gitkeep"

echo ""
echo "=== Copying ptypy root utility scripts ==="
find "$PTYPY" -maxdepth 1 \( -name "*.py" -o -name "*.csv" \) | while read f; do
  cp -v "$f" "$REPO/scripts/"
done

echo ""
echo "=== Copying HERMES processing scripts ==="
rsync -av \
  --exclude='pysync-master/' \
  --exclude='__pycache__/' \
  --include='*/' \
  --include='*.py' \
  --include='*.csv' \
  --exclude='*' \
  "$HERMES/scripts/" "$REPO/scripts/"

echo ""
echo "=== Copying HERMES recon scripts ==="
mkdir -p "$REPO/reconstructions/HERMES_22353"
rsync -av \
  --include='*/' \
  --include='*.py' \
  --include='*.csv' \
  --exclude='*' \
  "$HERMES/results/recon_scripts/" "$REPO/reconstructions/HERMES_22353/"

echo ""
echo "=== Staging all changes ==="
cd "$REPO"
git add reconstructions/ scripts/

echo ""
echo "=== Summary ==="
git diff --cached --stat | tail -10

echo ""
echo "Ready to commit. Run:"
echo "  cd ~/XRNF && git commit -m 'Add ptypy and HERMES reconstructions and scripts from computer2'"
