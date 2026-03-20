def temporal_split(df: pd.DataFrame, date_col: str, val_start: str, test_start: str):
    """
    Split dataset by time to prevent future leakage.
    train: everything before val_start
    val:   val_start to test_start
    test:  test_start onwards
    """
    val_start = pd.Timestamp(val_start)
    test_start = pd.Timestamp(test_start)

    train = df[df[date_col] < val_start]
    val = df[(df[date_col] >= val_start) & (df[date_col] < test_start)]
    test = df[df[date_col] >= test_start]

    print(f"Train: {len(train)} rows ({train[date_col].min()} to {val_start})")
    print(f"Val:   {len(val)} rows ({val_start} to {test_start})")
    print(f"Test:  {len(test)} rows ({test_start} to {test[date_col].max()})")

    return train, val, test

# Example usage
train, val, test = temporal_split(
    df=user_features,
    date_col="label_date",
    val_start="2024-10-01",
    test_start="2024-11-01",
)
