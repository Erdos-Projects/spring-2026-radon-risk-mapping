from config.feature_filters import BASAL_FEATURE_EXCLUDE, OPTIONAL_FEATURE_EXCLUDES
from config.feature_groups import ALL_FEATURE_COLUMNS

def get_feature_columns(
    df,
    optional_excludes=None,
    extra_drop=None,
):

    cols = list(ALL_FEATURE_COLUMNS)

    # remove basal exclusions
    cols = [c for c in cols if c not in BASAL_FEATURE_EXCLUDE]

    # apply optional exclusion sets
    if optional_excludes is not None:

        optional_cols = []

        for name in optional_excludes:
            optional_cols += OPTIONAL_FEATURE_EXCLUDES.get(name, [])

        cols = [c for c in cols if c not in optional_cols]

    # remove experiment-specific drops
    if extra_drop is not None:
        cols = [c for c in cols if c not in extra_drop]

    # remove columns missing from dataframe
    cols = [c for c in cols if c in df.columns]

    return cols