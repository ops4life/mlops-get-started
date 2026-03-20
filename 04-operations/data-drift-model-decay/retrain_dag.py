"""
dags/drift_detection_and_retrain.py
Daily drift monitoring with automated retraining trigger.
"""
from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from datetime import datetime, timedelta

def check_drift(**context):
    """Check if drift exceeds retraining threshold."""
    import pandas as pd
    from evidently.report import Report
    from evidently.metric_preset import DataDriftPreset

    # Load reference and recent production data
    reference_df = pd.read_parquet("s3://your-bucket/reference/training_features.parquet")
    current_df = pd.read_parquet(f"s3://your-bucket/production_logs/{context['ds']}/features.parquet")

    report = Report(metrics=[DataDriftPreset()])
    report.run(reference_data=reference_df, current_data=current_df)
    result = report.as_dict()

    n_drifted = result["metrics"][0]["result"]["n_drifted_features"]
    drift_share = result["metrics"][0]["result"]["share_drifted_features"]

    # Store for downstream tasks
    context["ti"].xcom_push("drift_share", drift_share)
    context["ti"].xcom_push("n_drifted_features", n_drifted)

    # Trigger retraining if >20% of features have drifted
    return "trigger_retraining" if drift_share > 0.20 else "no_action"

with DAG(
    dag_id="drift_detection_and_retrain",
    schedule_interval="0 8 * * *",
    start_date=datetime(2024, 1, 1),
    catchup=False,
) as dag:

    monitor = BranchPythonOperator(
        task_id="check_drift",
        python_callable=check_drift,
    )

    retrain = KubernetesPodOperator(
        task_id="trigger_retraining",
        name="ml-retrain-{{ ds_nodash }}",
        namespace="mlops",
        image="your-registry/ml-trainer:latest",
        arguments=["python", "train.py",
                   "--data-path=s3://your-bucket/curated/latest",
                   "--experiment-name=churn-prediction-retrain"],
        env_vars={"MLFLOW_TRACKING_URI": "http://mlflow.mlops.svc.cluster.local:5000"},
        is_delete_operator_pod=True,
    )

    no_action = PythonOperator(
        task_id="no_action",
        python_callable=lambda: print("No drift detected, no retraining needed"),
    )

    monitor >> [retrain, no_action]
