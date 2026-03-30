# mlops-get-started

Code snippets for [LearnMLOps](https://learnmlops.ops4life.com) guides — practical MLOps examples for DevOps engineers.

## Structure

```
mlops-get-started/
├── datasets/HR-Employee-Attrition.csv  # Dataset used across pipeline notebooks
├── 01-foundation/
│   ├── devops-to-mlops/           # 90-day learning plan
│   └── ml-basics/                 # First model notebook
├── 02-pipeline/
│   ├── dataset-pipeline/          # Ingestion, Pandera validation, Airflow DAGs, DVC
│   ├── data-preparation/          # Feature engineering, preprocessing, splits
│   └── ml-model-training/         # Training, MLflow tracking, Optuna, Kubernetes Jobs
├── 03-kubernetes/
│   ├── kubernetes-for-ml/         # Node affinity, taints, PVCs, Jobs, resource quotas
│   ├── kubernetes-gpu-workloads/  # NVIDIA device plugin, GPU Operator, MIG, DCGM
│   └── deploying-with-kserve/     # InferenceService, canary, autoscaling, monitoring
└── 04-operations/
    └── data-drift-model-decay/    # Drift detection, Evidently AI, DVC versioning, retraining
```

## Dataset

The pipeline notebooks use the [IBM HR Analytics Employee Attrition & Performance](https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset) dataset from Kaggle.

## Setup

→ [SETUP.md](./SETUP.md) — use the online sandbox or run locally with Docker Compose

| Tool | Online sandbox | Local |
|------|---------------|-------|
| Jupyter | https://sandbox.learnmlops.ops4life.com | http://localhost:8888 |
| MLflow | https://mlflow.learnmlops.ops4life.com | http://localhost:5000 |
| Airflow | https://airflow.learnmlops.ops4life.com | http://localhost:8080 |

## Usage

Clone and explore:

```bash
git clone https://github.com/ops4life/mlops-get-started.git
cd mlops-get-started
```

Each notebook corresponds to a code block in the LearnMLOps guides at [learnmlops.ops4life.com](https://learnmlops.ops4life.com). The pipeline notebooks (`02-pipeline/`) are runnable end-to-end in [Google Colab](https://colab.research.google.com) — each includes `!pip install` and dataset fetch cells.
