def engineer_user_features(events_df: pd.DataFrame, as_of_date: pd.Timestamp) -> pd.DataFrame:
    """
    Create ML-ready features from raw event log.
    'as_of_date' prevents future leakage in time-series data.
    """
    events = events_df[events_df["event_ts"] <= as_of_date].copy()

    # Window aggregations
    windows = {
        "7d": as_of_date - pd.Timedelta(days=7),
        "30d": as_of_date - pd.Timedelta(days=30),
        "90d": as_of_date - pd.Timedelta(days=90),
    }

    features = {}
    for window_name, window_start in windows.items():
        window_events = events[events["event_ts"] >= window_start]
        grouped = window_events.groupby("user_id")

        features[f"session_count_{window_name}"] = grouped["event_ts"].count()
        features[f"purchase_count_{window_name}"] = (
            grouped["event_type"].apply(lambda x: (x == "purchase").sum())
        )

    user_features = pd.DataFrame(features).fillna(0)

    # Recency feature
    last_event = events.groupby("user_id")["event_ts"].max()
    user_features["days_since_last_event"] = (
        as_of_date - last_event
    ).dt.days

    # Derived ratio feature
    user_features["purchase_rate_30d"] = (
        user_features["purchase_count_30d"] /
        (user_features["session_count_30d"] + 1)  # +1 to avoid division by zero
    )

    return user_features
