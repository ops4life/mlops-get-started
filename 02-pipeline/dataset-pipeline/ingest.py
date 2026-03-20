"""
ingestion/ingest_postgres.py
Reads from a PostgreSQL source table, writes partitioned Parquet to S3.
"""
import boto3
import pandas as pd
import sqlalchemy
from datetime import date
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def ingest_daily_events(
    source_dsn: str,
    s3_bucket: str,
    run_date: date,
) -> int:
    """Ingest one day of events from PostgreSQL to S3 Parquet."""
    engine = sqlalchemy.create_engine(source_dsn)
    s3 = boto3.client("s3")

    query = """
        SELECT user_id, event_type, event_ts, properties
        FROM events
        WHERE DATE(event_ts) = :run_date
    """

    logger.info(f"Fetching events for {run_date}")
    df = pd.read_sql(query, engine, params={"run_date": run_date})
    row_count = len(df)
    logger.info(f"Fetched {row_count} rows")

    if row_count == 0:
        logger.warning(f"No data for {run_date} — possible upstream issue")
        return 0

    # Write partitioned Parquet: raw/events/year=2024/month=01/day=15/
    s3_key = (
        f"raw/events/"
        f"year={run_date.year}/"
        f"month={run_date.month:02d}/"
        f"day={run_date.day:02d}/"
        f"events.parquet"
    )

    # Write to temp file, upload to S3
    local_path = f"/tmp/events_{run_date}.parquet"
    df.to_parquet(local_path, index=False, compression="snappy")
    s3.upload_file(local_path, s3_bucket, s3_key)
    logger.info(f"Uploaded to s3://{s3_bucket}/{s3_key}")

    return row_count
