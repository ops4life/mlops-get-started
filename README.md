# mlops-get-started

Code snippets for [LearnMLOps](https://learnmlops.ops4life.com) guides — practical MLOps examples for DevOps engineers.

## Structure

```
mlops-get-started/
├── employee_attrition.csv         # Dataset used across pipeline notebooks
├── 01-foundation/
│   ├── devops-to-mlops/           # 90-day learning plan
│   └── ml-basics/                 # Python ML setup and first model
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

## Usage

Clone and explore:

```bash
git clone https://github.com/ops4life/mlops-get-started.git
cd mlops-get-started
```

Each notebook corresponds to a code block in the LearnMLOps guides at [learnmlops.ops4life.com](https://learnmlops.ops4life.com). The pipeline notebooks (`02-pipeline/`) are runnable end-to-end in [Google Colab](https://colab.research.google.com) — each includes `!pip install` and dataset fetch cells.

The full production MLOps project these notebooks are based on is available at [github.com/techiescamp/mlops-for-devops](https://github.com/techiescamp/mlops-for-devops).

## License

The licenses below apply to the files in **this repository** (`mlops-get-started`) only.

**Code** (all `.ipynb`, `.yaml`, `.sh`, and `.py` files) — Apache License 2.0

> Copyright 2025 TechiesCamp / DevOpsCube (contact@devopscube.com)
>
> Licensed under the Apache License, Version 2.0. You may obtain a copy at:
> http://www.apache.org/licenses/LICENSE-2.0

**Content** (README files, guides, documentation, and explanatory text) — All Rights Reserved

> Copyright (c) 2025 TechiesCamp / DevOpsCube (contact@devopscube.com)
>
> You may read and study this content for personal learning, and link to this repository. Brief excerpts (up to 50 words) may be quoted with clear attribution. Copying, republishing, creating derivative works, or using this content in any course or training material — whether free or paid — requires prior written consent.
>
> Contact: contact@devopscube.com

For the license terms of the upstream project, see [techiescamp/mlops-for-devops](https://github.com/techiescamp/mlops-for-devops).
