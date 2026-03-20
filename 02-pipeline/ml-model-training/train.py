"""
train.py — Production training script for a churn prediction model.
Designed to run as a CLI, in Airflow, or as a Kubernetes Job.
"""
import argparse
import mlflow
import mlflow.sklearn
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import (
    accuracy_score, f1_score, roc_auc_score,
    precision_score, recall_score, classification_report
)
import joblib
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

def load_data(data_path: str):
    """Load and return train/val splits as numpy arrays."""
    train = pd.read_parquet(f"{data_path}/train.parquet")
    val = pd.read_parquet(f"{data_path}/val.parquet")

    feature_cols = [c for c in train.columns if c not in ("user_id", "churned", "label_date")]
    target_col = "churned"

    return (
        train[feature_cols].values, train[target_col].values,
        val[feature_cols].values, val[target_col].values,
        feature_cols
    )

def train(args):
    mlflow.set_tracking_uri(args.mlflow_uri)
    mlflow.set_experiment(args.experiment_name)

    with mlflow.start_run(run_name=f"gbt-lr{args.learning_rate}-d{args.max_depth}"):
        # Log all hyperparameters
        mlflow.log_params({
            "learning_rate": args.learning_rate,
            "max_depth": args.max_depth,
            "n_estimators": args.n_estimators,
            "subsample": args.subsample,
            "data_path": args.data_path,
        })

        X_train, y_train, X_val, y_val, feature_names = load_data(args.data_path)
        logger.info(f"Loaded {len(X_train)} training, {len(X_val)} validation examples")

        model = GradientBoostingClassifier(
            learning_rate=args.learning_rate,
            max_depth=args.max_depth,
            n_estimators=args.n_estimators,
            subsample=args.subsample,
            random_state=42,
            verbose=0,
        )

        model.fit(X_train, y_train)

        # Evaluate on validation set
        y_pred = model.predict(X_val)
        y_prob = model.predict_proba(X_val)[:, 1]

        metrics = {
            "val_accuracy": accuracy_score(y_val, y_pred),
            "val_f1": f1_score(y_val, y_pred),
            "val_roc_auc": roc_auc_score(y_val, y_prob),
            "val_precision": precision_score(y_val, y_pred),
            "val_recall": recall_score(y_val, y_pred),
        }

        mlflow.log_metrics(metrics)
        logger.info(f"Metrics: {metrics}")

        # Log the model
        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="model",
            registered_model_name=args.model_name,
            input_example=X_val[:3],
        )

        return metrics["val_roc_auc"]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-path", required=True)
    parser.add_argument("--learning-rate", type=float, default=0.1)
    parser.add_argument("--max-depth", type=int, default=4)
    parser.add_argument("--n-estimators", type=int, default=200)
    parser.add_argument("--subsample", type=float, default=0.8)
    parser.add_argument("--mlflow-uri", default="http://mlflow:5000")
    parser.add_argument("--experiment-name", default="churn-prediction")
    parser.add_argument("--model-name", default="churn-predictor")
    args = parser.parse_args()
    train(args)
