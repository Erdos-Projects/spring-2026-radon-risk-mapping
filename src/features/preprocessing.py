from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Optional

import pandas as pd


# =========================================================
# 1. Rules from feature-reduction notebook
# =========================================================

NON_FEATURE_COLUMNS = [
    "FSA",
    "n_days",
    "concentration",
    "provinceterritory",
    "geometry",
    "spatial_cluster",
    "is_test",
    "cv_fold",
    #"radon_danger_conc",
]

# Optional drops: keep as switches
HIGH_CORR_DROP_OPTIONAL = [
    "demogr_pop_2016",
    "demogr_num_total_dwellings",
    "socioeco_frac_unsuitable_housing",
    "socioeco_frac_high_income",
    "socioeco_frac_nonlaborer",
    "geolprov_grenville_province",
]

LOW_MI_DROP_OPTIONAL = [
    "hous_avg_rooms",
]

# One feature removed from each compositional group
# to avoid perfect multicollinearity
COMPOSITIONAL_DROP = [
    "hous_frac_type_other_attached",
    "hous_frac_age_post_2001",
    "demogr_frac_tenure_rented",
    "rxtp_sedimentary_and_volcanic_rocks",
    "geolprov_unknown",
    "geolprov_hudson_bay_lowlands",
]


@dataclass
class PreprocessingResult:
    X: pd.DataFrame
    kept_features: list[str]
    dropped_features: list[str]
    drop_reasons: dict[str, list[str]]


# =========================================================
# 2. Helper functions
# =========================================================

def _existing_columns(columns: Iterable[str], df: pd.DataFrame) -> list[str]:
    """Return only columns that exist in df."""
    return [col for col in columns if col in df.columns]


def get_all_zero_columns(df: pd.DataFrame) -> list[str]:
    """Columns whose values are all zero."""
    return df.columns[(df == 0).all()].tolist()


def get_constant_columns(df: pd.DataFrame) -> list[str]:
    """Columns with only one unique value (including NaN pattern)."""
    return df.columns[df.nunique(dropna=False) == 1].tolist()


def build_feature_list(
    df: pd.DataFrame,
    *,
    drop_high_corr: bool = False,
    drop_low_mi: bool = False,
    extra_drop: Optional[Iterable[str]] = None,
    target_col: Optional[str] = None,
) -> tuple[list[str], dict[str, list[str]]]:
    """
    Build the final feature list based on fixed and optional drop rules.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe.
    drop_high_corr : bool
        Whether to drop manually flagged high-correlation features.
    drop_low_mi : bool
        Whether to drop manually flagged low-MI features.
    extra_drop : iterable of str, optional
        Any extra columns to drop for a particular model run.
    target_col : str, optional
        If provided, force-remove target_col from features.

    Returns
    -------
    kept_features : list[str]
        Final list of kept features.
    drop_reasons : dict[str, list[str]]
        Mapping of drop-reason -> dropped columns.
    """
    df = df.copy()

    drop_reasons: dict[str, list[str]] = {}

    # 1) non-features
    non_feature_cols = _existing_columns(NON_FEATURE_COLUMNS, df)
    if target_col is not None and target_col in df.columns and target_col not in non_feature_cols:
        non_feature_cols.append(target_col)
    drop_reasons["non_feature"] = sorted(set(non_feature_cols))

    # 2) all-zero / constant
    all_zero_cols = get_all_zero_columns(df)
    drop_reasons["all_zero"] = sorted(set(all_zero_cols))

    constant_cols = [c for c in get_constant_columns(df) if c not in all_zero_cols]
    drop_reasons["constant"] = sorted(set(constant_cols))

    # 3) compositional drop (fixed)
    compositional_drop = _existing_columns(COMPOSITIONAL_DROP, df)
    drop_reasons["compositional_reference"] = sorted(set(compositional_drop))

    # 4) optional drops
    if drop_high_corr:
        high_corr_drop = _existing_columns(HIGH_CORR_DROP_OPTIONAL, df)
        drop_reasons["high_corr_optional"] = sorted(set(high_corr_drop))
    else:
        drop_reasons["high_corr_optional"] = []

    if drop_low_mi:
        low_mi_drop = _existing_columns(LOW_MI_DROP_OPTIONAL, df)
        drop_reasons["low_mi_optional"] = sorted(set(low_mi_drop))
    else:
        drop_reasons["low_mi_optional"] = []

    # 5) user-specified extra drops
    extra_drop = list(extra_drop) if extra_drop is not None else []
    drop_reasons["extra_drop"] = sorted(set(_existing_columns(extra_drop, df)))

    # Combine all drops
    all_drop_cols = sorted(
        set(col for cols in drop_reasons.values() for col in cols)
    )

    kept_features = [col for col in df.columns if col not in all_drop_cols]

    return kept_features, drop_reasons


def preprocess_features(
    df: pd.DataFrame,
    *,
    drop_high_corr: bool = False,
    drop_low_mi: bool = False,
    extra_drop: Optional[Iterable[str]] = None,
    target_col: Optional[str] = None,
    return_metadata: bool = True,
) -> PreprocessingResult | pd.DataFrame:
    """
    Apply feature dropping rules and return processed X.

    Note:
    -----
    This function only selects/drops columns.
    Missing-value imputation should usually be done later inside a
    train-only sklearn Pipeline to avoid leakage.
    """
    df = df.copy()

    kept_features, drop_reasons = build_feature_list(
        df,
        drop_high_corr=drop_high_corr,
        drop_low_mi=drop_low_mi,
        extra_drop=extra_drop,
        target_col=target_col,
    )

    X = df[kept_features].copy()
    dropped_features = sorted(set(df.columns) - set(kept_features))

    if return_metadata:
        return PreprocessingResult(
            X=X,
            kept_features=kept_features,
            dropped_features=dropped_features,
            drop_reasons=drop_reasons,
        )

    return X