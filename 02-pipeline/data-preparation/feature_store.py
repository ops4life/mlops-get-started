# feature_repo/features.py — Define features once, use everywhere
from feast import Entity, FeatureView, Field, FileSource
from feast.types import Float32, Int64
from datetime import timedelta

user = Entity(name="user_id", description="A user in the system")

user_stats_source = FileSource(
    path="s3://your-bucket/curated/user_features.parquet",
    timestamp_field="event_timestamp",
)

user_activity_features = FeatureView(
    name="user_activity",
    entities=[user],
    ttl=timedelta(days=90),
    schema=[
        Field(name="session_count_7d", dtype=Int64),
        Field(name="session_count_30d", dtype=Int64),
        Field(name="purchase_count_30d", dtype=Int64),
        Field(name="days_since_last_event", dtype=Int64),
        Field(name="purchase_rate_30d", dtype=Float32),
    ],
    source=user_stats_source,
)

# Training: fetch historical features at label time (prevents leakage)
from feast import FeatureStore
store = FeatureStore(repo_path="feature_repo/")
training_df = store.get_historical_features(
    entity_df=labels_df,   # has user_id + event_timestamp columns
    features=["user_activity:session_count_7d", "user_activity:purchase_rate_30d"],
).to_df()

# Serving: fetch latest features for a live user_id
features = store.get_online_features(
    features=["user_activity:session_count_7d", "user_activity:purchase_rate_30d"],
    entity_rows=[{"user_id": "abc-123"}],
).to_dict()
