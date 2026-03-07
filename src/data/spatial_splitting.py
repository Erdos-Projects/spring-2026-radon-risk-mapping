"""
Utilities for building spatially-aware train/test splits
and cross-validation folds for the radon dataset.
"""

import pandas as pd
from sklearn.model_selection import StratifiedGroupKFold


# ---------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------

CANADA_ALBERS_EPSG = "EPSG:3347"
DEFAULT_N_TEST_SPLITS = 5
DEFAULT_N_CV_SPLITS = 5
DEFAULT_RANDOM_STATE = 42


def create_spatial_test_split(
    df,
    n_test_splits=DEFAULT_N_TEST_SPLITS,
    random_state=DEFAULT_RANDOM_STATE
):
    """
    Create a spatially grouped, stratified test split.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataset containing 'spatial_cluster' and 'provinceterritory'.

    test_fraction : float
        Desired fraction of observations in the test set.

    n_candidates : int
        Number of candidate splits to evaluate.

    random_state : int
        Random seed.

    Returns
    -------
    pandas.DataFrame
        Dataset with boolean column 'is_test'.
    """
    
    # ensure df has the columns we need
    required_columns = {"spatial_cluster", "provinceterritory"}

    missing = required_columns - set(df.columns)

    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    # ensure df doesn't have any assignments already
    df = df.copy()
    df["is_test"] = False

    # set up the split conditions
    sgkf = StratifiedGroupKFold(
        n_splits=n_test_splits,
        shuffle=True,
        random_state=random_state
    )

    X = df 
    y = df["provinceterritory"]
    groups = df["spatial_cluster"]

    # generate  candidate splits
    splits = list(sgkf.split(X, y, groups))

    # choose split most even split of dataset
    target_fraction = 1 / n_test_splits

    best_split = min(
        splits,
        key=lambda split: abs(len(split[1]) / len(df) - target_fraction)
    )

    train_idx, test_idx = best_split

    df.loc[test_idx, "is_test"] = True

    return df


def create_spatial_cv_folds(
        df,
        n_cv_splits=DEFAULT_N_CV_SPLITS,
        random_state=DEFAULT_RANDOM_STATE,
):
    """
    Create cross-validation folds inside the training pool.

    Test rows are excluded.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataset containing 'spatial_cluster', 'provinceterritory', and 'is_test'.

    Returns
    -------
    pandas.DataFrame
        Dataset with a new column 'cv_fold'.
    """

    required_columns = {"spatial_cluster", "provinceterritory", "is_test"}

    missing = required_columns - set(df.columns)

    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df = df.copy()
    df["cv_fold"] = -1

    train_df = df[df["is_test"] == False]

    sgkf = StratifiedGroupKFold(
        n_splits=n_cv_splits,
        shuffle=True,
        random_state=random_state
    )

    X = train_df
    y = train_df["provinceterritory"]
    groups = train_df["spatial_cluster"]

    for fold, (_, val_idx) in enumerate(sgkf.split(X, y, groups)):

        df.loc[train_df.index[val_idx], "cv_fold"] = fold

    return df


def create_spatial_test_and_cv_splits(
    df,
    n_test_splits=DEFAULT_N_TEST_SPLITS,
    n_cv_splits=DEFAULT_N_CV_SPLITS,
    random_state=DEFAULT_RANDOM_STATE
):
    """
    Generate both test split and cross-validation folds.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataset containing spatial clusters and province labels.

    Returns
    -------
    pandas.DataFrame
        Dataset with 'is_test' and 'cv_fold' columns added.
    """

    df = create_spatial_test_split(
        df,
        n_test_splits=n_test_splits, 
        random_state=random_state)

    df = create_spatial_cv_folds(
        df,
        n_cv_splits=n_cv_splits, 
        random_state=random_state
        )

    return df
