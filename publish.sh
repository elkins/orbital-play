#!/bin/bash

# OrbitalPlay PyPI Publication Script
# Automates building and uploading the package to PyPI.

# Exit on error
set -e

echo "🚀 Starting OrbitalPlay publication process..."

# 1. Clean up old build artifacts
echo "🧹 Cleaning up old builds..."
rm -rf dist/ build/ *.egg-info/

# 2. Build the package
echo "📦 Building source and wheel distributions..."
python3 -m build

# 3. Verify the build
echo "🔍 Verifying the package with twine..."
python3 -m twine check dist/*

# 4. Upload to PyPI
echo "⬆️ Uploading to PyPI..."
echo "Note: You will need your PyPI credentials/token."
python3 -m twine upload dist/*

echo "✅ OrbitalPlay successfully published to PyPI!"
