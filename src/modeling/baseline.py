import pandas as pd
import numpy as np
from pathlib import Path
import sys

# project root = two levels above notebooks
PROJECT_ROOT = Path.cwd().parent.parent
sys.path.append(str(PROJECT_ROOT))

from src.data.data_loading import (
    load_full_dataset,
    load_full_training_pool,
    load_test_data,
    load_training_data,
    load_validation_data
)

CUTOFF_THRESHOLD = 0.5

## Approach: add a binary column with condition "Radon concentration >200"
## so that each FSA has a bunch of rows with 1s and 0s. Corresponding to each FSA, take 
## mean of the binary column (gives us the fraction of measurements that exceed 200).
## Finally classify the FSA as 1 if the mean is more than `threshold`

def baseline_using_measurement_proportion(threshold = CUTOFF_THRESHOLD):
    df = load_full_dataset()
    df['y_binary'] = (df['concentration'] >200).astype(int)
    fsa_features = df.drop(columns="y_binary").drop_duplicates("FSA")
    y_mean = df.groupby("FSA")["y_binary"].mean().reset_index(name="y_mean")
    df = pd.merge(y_mean, fsa_features, on= 'FSA')
    df['classification'] = (df['y_mean'] > threshold).astype(int)
    return df[['FSA', 'classification']]

## Approach 2: Corresponding to each FSA, take the mean of all the measurements in 
## that particular FSA. Classify the FSA as 1 if the mean radon is more than 200, else 0.

def baseline_using_mean_radon_level():
    df = load_full_dataset()
    fsa_features = df.drop(columns="concentration").drop_duplicates("FSA")
    fsa_mean = df.groupby("FSA")["concentration"].mean().reset_index(name="mean_concentration")
    df = pd.merge(fsa_mean, fsa_features, on= 'FSA')
    df['classification'] = (df['mean_concentration'] > 200).astype(int)
    return df[['FSA', 'classification']]

