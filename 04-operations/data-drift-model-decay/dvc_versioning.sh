# Tag dataset versions at milestone points
git tag -a "dataset-v1.0.0" -m "Initial training dataset: 6 months of events"
git tag -a "dataset-v1.1.0" -m "Added Q4 2023 data after drift detection"
git push origin --tags

# In MLflow, record which dataset version trained each model
import mlflow
with mlflow.start_run():
    mlflow.log_param("dataset_git_tag", "dataset-v1.1.0")
    mlflow.log_param("dataset_dvc_rev", subprocess.check_output(
        ["git", "rev-parse", "HEAD"]
    ).decode().strip())
    # ... training code ...

# To reproduce training with the exact dataset from 3 months ago:
git checkout dataset-v1.0.0
dvc pull   # Downloads the exact dataset state

# Alternatively, use DVC's data registry pattern:
# dvc get https://github.com/your-org/ml-project data/curated/ \
#   --rev dataset-v1.0.0 \
#   -o data/reproduced/
