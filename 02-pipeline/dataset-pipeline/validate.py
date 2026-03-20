"""
validation/validate_events.py
Run data quality checks on the ingested events dataset.
"""
import great_expectations as gx
import pandas as pd

def validate_events(parquet_path: str) -> bool:
    """Return True if data passes all quality checks."""
    context = gx.get_context()
    df = pd.read_parquet(parquet_path)

    # Create a validator from a pandas dataframe
    validator = context.sources.pandas_default.read_dataframe(df)

    # Schema checks
    validator.expect_column_to_exist("user_id")
    validator.expect_column_to_exist("event_type")
    validator.expect_column_to_exist("event_ts")

    # Nullability checks
    validator.expect_column_values_to_not_be_null("user_id")
    validator.expect_column_values_to_not_be_null("event_ts")

    # Value range / format checks
    validator.expect_column_values_to_be_in_set(
        "event_type",
        ["page_view", "click", "purchase", "signup", "logout"]
    )
    validator.expect_column_values_to_match_regex(
        "user_id",
        r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
    )

    # Volume check — alert if fewer than 1000 rows (likely upstream issue)
    validator.expect_table_row_count_to_be_between(1000, None)

    results = validator.validate()
    if not results.success:
        failed = [r for r in results.results if not r.success]
        for r in failed:
            print(f"FAILED: {r.expectation_config.expectation_type} — {r.result}")
        return False

    print(f"All {len(results.results)} expectations passed")
    return True
