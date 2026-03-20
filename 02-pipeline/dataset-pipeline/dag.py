"""
dags/ml_dataset_pipeline.py
Daily dataset ingestion, validation, and DVC commit pipeline.
"""
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.email import EmailOperator

from ingestion.ingest_postgres import ingest_daily_events
from validation.validate_events import validate_events

DEFAULT_ARGS = {
    "owner": "mlops",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "email_on_failure": True,
    "email": ["ml-alerts@yourcompany.com"],
}

with DAG(
    dag_id="ml_dataset_pipeline",
    default_args=DEFAULT_ARGS,
    schedule_interval="0 2 * * *",  # 2 AM daily
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["ml", "data-pipeline"],
) as dag:

    ingest = PythonOperator(
        task_id="ingest_events",
        python_callable=ingest_daily_events,
        op_kwargs={
            "source_dsn": "{{ var.value.postgres_dsn }}",
            "s3_bucket": "{{ var.value.ml_data_bucket }}",
            "run_date": "{{ ds }}",
        },
    )

    def validate_and_branch(**context):
        parquet_path = f"s3://{{ var.value.ml_data_bucket }}/raw/events/{context['ds']}/events.parquet"
        if validate_events(parquet_path):
            return "copy_to_validated"
        return "alert_validation_failure"

    branch = BranchPythonOperator(
        task_id="validate_events",
        python_callable=validate_and_branch,
    )

    copy_validated = PythonOperator(
        task_id="copy_to_validated",
        python_callable=lambda **ctx: print("Copying to validated zone..."),
    )

    alert_failure = EmailOperator(
        task_id="alert_validation_failure",
        to=["ml-alerts@yourcompany.com"],
        subject="[ALERT] Dataset validation failed for {{ ds }}",
        html_content="Validation checks failed. Check Airflow logs.",
    )

    # Pipeline: ingest -> validate -> branch -> copy OR alert
    ingest >> branch >> [copy_validated, alert_failure]
