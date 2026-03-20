import optuna
import mlflow

def objective(trial):
    """Optuna calls this function for each trial."""
    # Define the search space
    params = {
        "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.3, log=True),
        "max_depth": trial.suggest_int("max_depth", 3, 8),
        "n_estimators": trial.suggest_int("n_estimators", 100, 500, step=50),
        "subsample": trial.suggest_float("subsample", 0.5, 1.0),
        "min_samples_split": trial.suggest_int("min_samples_split", 2, 20),
    }

    with mlflow.start_run(nested=True):
        mlflow.log_params(params)

        model = GradientBoostingClassifier(**params, random_state=42)
        model.fit(X_train, y_train)

        roc_auc = roc_auc_score(y_val, model.predict_proba(X_val)[:, 1])
        mlflow.log_metric("val_roc_auc", roc_auc)

    return roc_auc  # Optuna maximizes this

# Run 50 trials, pruning poor runs early
with mlflow.start_run(run_name="optuna-sweep"):
    study = optuna.create_study(
        direction="maximize",
        pruner=optuna.pruners.MedianPruner(n_startup_trials=10),
    )
    study.optimize(objective, n_trials=50, n_jobs=4)

    best = study.best_params
    print(f"Best params: {best}")
    print(f"Best ROC-AUC: {study.best_value:.4f}")
    mlflow.log_params({f"best_{k}": v for k, v in best.items()})
    mlflow.log_metric("best_val_roc_auc", study.best_value)
