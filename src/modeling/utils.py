import pandas as pd
import numpy as np
from pathlib import Path
import sys

def add_y_binary(df):
    if 'concentration' not in df.columns:
        raise ValueError("Dataframe must have the column `concentration`")
    df['y_binary'] = (df['concentration'] >200).astype(int)
    return df

def fsa_grouped_features_and_proportion_above200(df):
    if 'y_mean' in df.columns: ## in this case, this functin is already used in the dataframe
        return df
    if "y_binary" not in df.columns:
        df = add_y_binary(df)
    drop_columns = ['provinceterritory', 'geometry','spatial_cluster', 'is_test', 
                    'cv_fold', "y_binary", "concentration" ]
    fsa_features = df.drop(columns=drop_columns, errors = 'ignore').drop_duplicates("FSA")
    y_mean = df.groupby("FSA")["y_binary"].mean().reset_index(name="y_mean")
    return fsa_features.merge(y_mean, on="FSA")

def fsa_features_only(df):
    return fsa_grouped_features_and_proportion_above200(df).drop(columns = ['y_mean'])

def fsa_proportion_above200(df):
    df = fsa_grouped_features_and_proportion_above200(df).rename(columns = {'y_mean':'proportion'})
    return df[['FSA', 'proportion']]

def no_of_measurements_per_fsa(df):
    counts = df.value_counts('FSA')
    df = df.drop_duplicates('FSA')
    df = df.merge(counts, on = 'FSA')
    df = df.rename(columns = {'count':'no_of_measurements'})
    return df[['FSA', 'no_of_measurements']]