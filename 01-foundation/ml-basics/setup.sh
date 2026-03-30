#!/bin/bash
# Set up a Python ML environment
python3 -m venv mlenv
source mlenv/bin/activate

# Core ML stack
pip install numpy pandas scikit-learn matplotlib

# Deep learning (CPU-only for dev)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

# MLOps tooling
pip install mlflow dvc
