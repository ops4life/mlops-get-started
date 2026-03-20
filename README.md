# mlops-get-started

Code snippets for [LearnMLOps](https://learnmlops.ops4life.com) guides — practical MLOps examples for DevOps engineers.

## Structure

```
mlops-get-started/
├── 01-foundation/
│   ├── devops-to-mlops/       # 90-day learning plan
│   └── ml-basics/             # Python ML setup and first model
├── 02-pipeline/
│   ├── data-preparation/      # Preprocessing, feature engineering, splits, feature stores
│   ├── dataset-pipeline/      # Ingestion, S3 structure, validation, Airflow DAGs, DVC
│   └── ml-model-training/     # Training scripts, MLflow, Optuna, Kubernetes Jobs
├── 03-kubernetes/
│   ├── kubernetes-for-ml/     # Node affinity, taints, PVCs, Jobs, resource quotas
│   ├── kubernetes-gpu-workloads/  # NVIDIA device plugin, GPU Operator, MIG, DCGM
│   └── deploying-with-kserve/ # InferenceService, canary, autoscaling, monitoring
└── 04-operations/
    └── data-drift-model-decay/ # Drift detection, Evidently AI, DVC versioning, retraining
```

## Usage

Clone and explore:

```bash
git clone https://github.com/ops4life/mlops-get-started.git
cd mlops-get-started
```

Each file corresponds to a code block in the LearnMLOps guides at [learnmlops.ops4life.com](https://learnmlops.ops4life.com).
