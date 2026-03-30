# Setup

Two ways to use the tools in this repo — pick whichever fits your situation.

---

## Option A — Online Sandbox (no install)

The easiest way to get started. Everything is pre-installed and the starter notebooks from this repo are already loaded.

| Tool | URL |
|------|-----|
| Jupyter Notebook | https://sandbox.learnmlops.ops4life.com |
| MLflow UI | https://mlflow.learnmlops.ops4life.com |
| Airflow UI | https://airflow.learnmlops.ops4life.com |

Open Jupyter, navigate to `starter/`, and run any notebook. MLflow and Airflow are already running and connected.

> **Note:** The sandbox is shared. Don't store sensitive data or credentials in notebooks.

---

## Option B — Run locally with Docker Compose

**Prerequisites:** [Docker](https://docs.docker.com/get-docker/) with the Compose plugin.

```bash
git clone https://github.com/ops4life/mlops-get-started.git
cd mlops-get-started
docker compose -f docker-compose.local.yml up -d
```

| Tool | URL |
|------|-----|
| Jupyter Notebook | http://localhost:8888 |
| MLflow UI | http://localhost:5000 |
| Airflow UI | http://localhost:8080 |

Stop everything:

```bash
docker compose -f docker-compose.local.yml down
```

---

## Tools

### Jupyter Notebook

An interactive Python environment for running and editing notebooks.

- In the online sandbox, starter notebooks are in the `starter/` folder
- Locally, your full repo clone is mounted at `/workspace`
- Run cells with `Shift+Enter`; the kernel persists between cells

The notebooks in this repo connect to MLflow using `http://mlflow:5000` — this works in both the sandbox and the local Docker setup without any changes.

### MLflow

Tracks experiments: parameters, metrics, and model artifacts across training runs.

- Open the UI to compare runs and register models
- Notebooks log to MLflow automatically via the tracking URI set at the top of each notebook
- Locally, run data is stored in a `mlruns/` Docker volume

Key concepts:
- **Experiment** — a named group of runs (e.g. `employee-attrition`)
- **Run** — one training execution with logged params and metrics
- **Model Registry** — promotes a run's model artifact to `Staging` or `Production`

### Airflow

Orchestrates ML pipelines as DAGs (Directed Acyclic Graphs).

- Runs in standalone mode: scheduler, webserver, and a single worker in one process
- DAG files placed in `02-pipeline/` are auto-discovered every 30 seconds
- Log in to the UI with the credentials printed during startup:
  ```bash
  docker compose logs airflow | grep "standalone_admin_password"
  # or check: docker exec learnmlops-airflow cat /airflow/standalone_admin_password.txt
  ```
- Trigger a DAG manually from the UI or via CLI:
  ```bash
  docker exec learnmlops-airflow airflow dags trigger <dag_id>
  ```

### DVC

Versions datasets and pipeline stages without storing large files in git.

DVC is a CLI tool — no server required.

Install:

```bash
pip install dvc

# With S3 support
pip install "dvc[s3]"

# With GCS support
pip install "dvc[gs]"
```

> DVC is already installed in both the online sandbox and the local Docker Compose environment.

Key commands:

```bash
# Initialize in a repo
dvc init

# Track a data file (adds to .dvc/ and creates a .dvc pointer file)
dvc add datasets/HR-Employee-Attrition.csv

# Define pipeline stages and run them
dvc repro

# Push data to a remote (S3, GCS, SSH, etc.)
dvc remote add -d myremote s3://your-bucket/dvc-cache
dvc push

# Reproduce the exact dataset/model from a past git commit
git checkout <commit>
dvc checkout
```

The `dvc_setup.sh` scripts in each section show the full setup for that guide's pipeline.
