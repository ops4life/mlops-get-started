import numpy as np
import pandas as pd
from scipy import stats
from typing import Dict

def detect_feature_drift(
    reference: pd.DataFrame,
    current: pd.DataFrame,
    numeric_features: list,
    categorical_features: list,
    significance_level: float = 0.05,
) -> Dict[str, dict]:
    """
    Detect drift in feature distributions using statistical tests.
    Returns per-feature drift report.
    """
    results = {}

    # KS test for numeric features
    for feature in numeric_features:
        ref_vals = reference[feature].dropna().values
        cur_vals = current[feature].dropna().values

        stat, p_value = stats.ks_2samp(ref_vals, cur_vals)

        # Calculate Population Stability Index (PSI)
        psi = calculate_psi(ref_vals, cur_vals)

        results[feature] = {
            "test": "ks",
            "statistic": round(stat, 4),
            "p_value": round(p_value, 4),
            "drifted": p_value < significance_level,
            "psi": round(psi, 4),
            "psi_severity": "none" if psi < 0.1 else "minor" if psi < 0.2 else "major",
        }

    # Chi-squared test for categorical features
    for feature in categorical_features:
        ref_counts = reference[feature].value_counts(normalize=True)
        cur_counts = current[feature].value_counts(normalize=True)

        # Align categories
        all_cats = set(ref_counts.index) | set(cur_counts.index)
        ref_freq = np.array([ref_counts.get(c, 0) for c in all_cats])
        cur_freq = np.array([cur_counts.get(c, 0) for c in all_cats])

        # Chi-squared expects counts, not proportions
        n_current = len(current)
        expected = ref_freq * n_current
        observed = cur_freq * n_current

        # Avoid zero expected values
        expected = np.where(expected < 1, 1, expected)
        stat, p_value = stats.chisquare(observed, expected)

        results[feature] = {
            "test": "chi2",
            "statistic": round(stat, 4),
            "p_value": round(p_value, 4),
            "drifted": p_value < significance_level,
        }

    return results

def calculate_psi(reference: np.ndarray, current: np.ndarray, bins: int = 10) -> float:
    """Population Stability Index — values >0.2 indicate significant drift."""
    ref_hist, bin_edges = np.histogram(reference, bins=bins)
    cur_hist, _ = np.histogram(current, bins=bin_edges)

    ref_pct = ref_hist / len(reference) + 1e-10
    cur_pct = cur_hist / len(current) + 1e-10

    psi = np.sum((cur_pct - ref_pct) * np.log(cur_pct / ref_pct))
    return psi
