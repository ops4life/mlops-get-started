#!/usr/bin/env bash
# ML environment setup — installs the core Python packages used across all guides.
# Run inside a virtual environment: python -m venv .venv && source .venv/bin/activate

set -euo pipefail

pip install --upgrade pip

# Core data stack
pip install pandas numpy scipy

# ML framework
pip install scikit-learn

# Experiment tracking & model registry
pip install mlflow

# Hyperparameter tuning
pip install optuna

# Data validation
pip install pandera

# Monitoring & drift detection
pip install evidently

# Feature store
pip install feast

# Data versioning
pip install dvc

# Orchestration (standalone mode — no database needed)
pip install "apache-airflow==2.9.0" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.9.0/constraints-3.11.txt"

echo "Setup complete. All packages installed."
