#!/usr/bin/env bash
# Render.com build script

set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

echo "Build completed successfully!"