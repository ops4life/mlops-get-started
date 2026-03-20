from evidently import ColumnMapping
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, DataQualityPreset, TargetDriftPreset
from evidently.metrics import *

# Define column roles
column_mapping = ColumnMapping(
    target="churned",
    prediction="prediction",
    numerical_features=["session_count_30d", "days_since_last_event", "purchase_rate_30d"],
    categorical_features=["plan_type", "acquisition_channel"],
)

# Build a comprehensive monitoring report
report = Report(metrics=[
    DataDriftPreset(),          # Feature distribution drift
    DataQualityPreset(),        # Missing values, outliers, duplicates
    TargetDriftPreset(),        # Output/prediction drift
    ClassificationPreset(),     # Accuracy, F1, precision, recall
])

# reference_df: data from model training period
# current_df: last 7 days of production data
report.run(
    reference_data=reference_df,
    current_data=current_df,
    column_mapping=column_mapping,
)

# Save HTML report
report.save_html("drift_report_2024_01_15.html")

# Or extract as dictionary for programmatic use
report_dict = report.as_dict()
dataset_drift = report_dict["metrics"][0]["result"]["dataset_drift"]
n_drifted_features = report_dict["metrics"][0]["result"]["n_drifted_features"]

if dataset_drift:
    print(f"DRIFT DETECTED: {n_drifted_features} features have drifted!")
    # Trigger retraining pipeline...
