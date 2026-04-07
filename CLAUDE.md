# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

Educational MLOps training repository for DevOps engineers learning ML engineering. Provides 4 progressive modules: ML fundamentals, a full data pipeline, Kubernetes deployment patterns, and production operations (drift detection, retraining).

## Local Development

```bash
# Start all services locally
cp .env.example .env
docker compose -f docker-compose.local.yml up -d

# Access points
# Jupyter:   http://localhost:8888
# MLflow:    http://localhost:5000
# Airflow:   http://localhost:8080
```

All three services run from the same Docker image (`ops4life/learnmlops-sandbox`) and share a `sandbox-net` network. Notebooks reach the tracking server at `http://mlflow:5000` and Airflow at `http://airflow:8080` by hostname.

There is no build step, test suite, or linter. Notebooks are the primary deliverable and are validated manually in the sandbox.

## Architecture

The repository is structured as a learning progression, not a monolithic application:

```
01-foundation/     # ML basics — train_iris.ipynb is the entry point
02-pipeline/       # Full pipeline: ingest → validate → engineer → train → promote
03-kubernetes/     # K8s manifests for training jobs, GPU, KServe serving
04-operations/     # Drift detection DAG, Evidently reports, DVC versioning
datasets/          # IBM HR Employee Attrition CSV (1,470 rows × 34 cols)
```

### Service roles

| Service | Role |
|---------|------|
| Jupyter | Interactive development; notebooks log to MLflow |
| MLflow  | Experiment tracking, model registry, artifact storage (S3/MinIO) |
| Airflow | Pipeline orchestration; watches `/workspace/dags/`, rescans every 30s |

### Data flow

Raw CSV → (ingest) → S3 `raw/` → (validate, Pandera) → `validated/` → (feature engineer) → `curated/` → (train, MLflow) → Model Registry → (KServe) → REST endpoint

Drift detection runs daily (PSI on MonthlyIncome). If PSI > 0.20 a `BranchPythonOperator` triggers retraining and auto-promotes to Staging.

### Storage

- **Local**: MLflow uses a `mlruns` Docker volume.
- **Production**: MinIO at `s3.ops4life.com`; buckets `mlflow` and `dvc`. Credentials come from `.env` (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `MLFLOW_S3_ENDPOINT_URL`).
- **Production MLflow backend**: PostgreSQL (see `02-pipeline/ml-model-training/docker-compose.yml`).

## Module Details

### 02-pipeline — run notebooks in this order

1. `dataset-pipeline/ingest.ipynb` — generates synthetic HR attrition data
2. `dataset-pipeline/validate.ipynb` — Pandera schema validation
3. `data-preparation/feature_engineering.ipynb` — derived features (PromotionStagnation, CareerVelocity, OverallSatisfaction)
4. `ml-model-training/train.ipynb` — Logistic Regression baseline, MLflow experiment `employee-attrition`
5. `ml-model-training/tune.ipynb` — Optuna hyperparameter search (20 trials, GradientBoostingClassifier)
6. `ml-model-training/promote.ipynb` — gate on min_roc_auc=0.50 / min_f1=0.10, register to MLflow Staging

DAG definitions (`dag.ipynb`, `attrition_pipeline.py`) schedule the full pipeline `@daily`.

### 03-kubernetes — apply manifests to a cluster

- `kubernetes-for-ml/` — PVCs (500GB RWX for data, 100GB RWO for models), parallel jobs, pod affinity, resource quotas
- `kubernetes-gpu-workloads/` — NVIDIA device plugin, GPU Operator, MIG partitioning, DCGM metrics
- `deploying-with-kserve/` — KServe `InferenceService` (sklearn runtime, s3:// or mlflow-artifacts://), canary traffic splitting, HPA

### 04-operations

- `drift_detection.ipynb` — PSI calculation on MonthlyIncome
- `evidently_report.ipynb` — Evidently AI data quality report
- `retrain_dag.py` (`drift_retrain_dag`) — BranchPythonOperator: check drift → retrain → promote, or no_action
- `dvc_versioning.sh` — DVC push/pull against MinIO remote

## Colab Compatibility

Notebooks include a Colab-compatible header that installs missing packages and sets `MLFLOW_TRACKING_URI` to a local file path when not running in the Docker sandbox. Do not remove these guards.

## Deployment Context

This repo lives inside the `learnmlops/` service of the parent VPS monorepo. The sandbox services (`sandbox.learnmlops.ops4life.com`, `mlflow.learnmlops.ops4life.com`, `airflow.learnmlops.ops4life.com`) are the production equivalents of the local Docker Compose setup. MinIO credentials are shared from `minio/.env` in the parent repo.
