import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer

# Load curated dataset
df = pd.read_parquet("s3://your-bucket/curated/training_datasets/v20240115/raw.parquet")

# 1. Drop rows with too many missing values (>50% missing)
threshold = len(df.columns) * 0.5
df = df.dropna(thresh=threshold)

# 2. Separate feature types
numeric_features = ["age", "days_since_login", "total_purchases", "session_duration_s"]
categorical_features = ["plan_type", "acquisition_channel", "country"]

# 3. Build sklearn preprocessing pipelines
numeric_pipeline = Pipeline([
    ("impute", SimpleImputer(strategy="median")),
    ("scale", StandardScaler()),
])

categorical_pipeline = Pipeline([
    ("impute", SimpleImputer(strategy="most_frequent")),
    ("encode", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
])

preprocessor = ColumnTransformer([
    ("num", numeric_pipeline, numeric_features),
    ("cat", categorical_pipeline, categorical_features),
])

# IMPORTANT: Fit ONLY on training data, then transform all splits
X_train_processed = preprocessor.fit_transform(X_train)
X_val_processed = preprocessor.transform(X_val)    # Never fit_transform on val/test!
X_test_processed = preprocessor.transform(X_test)
