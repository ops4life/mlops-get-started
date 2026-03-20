def evaluate_and_promote(new_run_id: str, model_name: str, thresholds: dict):
    """
    Compare new model to current production model.
    Promote to Staging if it passes thresholds and beats current model.
    """
    client = mlflow.tracking.MlflowClient()

    # Get metrics for new model
    new_run = client.get_run(new_run_id)
    new_metrics = new_run.data.metrics

    # Check absolute thresholds
    if new_metrics["val_roc_auc"] < thresholds["min_roc_auc"]:
        raise ValueError(f"ROC-AUC {new_metrics['val_roc_auc']:.4f} < minimum {thresholds['min_roc_auc']}")
    if new_metrics["val_f1"] < thresholds["min_f1"]:
        raise ValueError(f"F1 {new_metrics['val_f1']:.4f} < minimum {thresholds['min_f1']}")

    # Compare to current production model
    prod_versions = client.get_latest_versions(model_name, stages=["Production"])
    if prod_versions:
        prod_run_id = prod_versions[0].run_id
        prod_metrics = client.get_run(prod_run_id).data.metrics
        if new_metrics["val_roc_auc"] <= prod_metrics.get("val_roc_auc", 0):
            raise ValueError(
                f"New model ({new_metrics['val_roc_auc']:.4f}) "
                f"is not better than production ({prod_metrics['val_roc_auc']:.4f})"
            )

    # Register and promote to Staging
    model_version = client.create_model_version(
        name=model_name,
        source=f"runs:/{new_run_id}/model",
        run_id=new_run_id,
    )
    client.transition_model_version_stage(
        name=model_name,
        version=model_version.version,
        stage="Staging",
    )
    print(f"Promoted {model_name} v{model_version.version} to Staging")
