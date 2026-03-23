
# Specify non-feature data
#  in the df columns... 
#  (1) Radon data and metadata
#   see: jb_eda_validFeatures.ipynb for more information


from .feature_groups import TARGET_COLUMN, METADATA_COLUMNS


# ---------------------------------------------------------------------
# Columns that should NEVER appear in model features
# ---------------------------------------------------------------------

NON_FEATURE_COLUMNS = (
    METADATA_COLUMNS
    + [TARGET_COLUMN]
)

# ---------------------------------------------------------------------
#  There are other columns that we should immediately drop from the data, too
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
# Compositional feature exclusions
#
# Some feature groups represent fractions that sum to 1.
# One member of each group must be removed to avoid
# perfect multicollinearity (dummy variable trap).
# ---------------------------------------------------------------------
COMPOSITIONAL_FEATURE_DROP = [
    # housing type fractions sum to 1
    "hous_frac_type_movable",

    # housing age fractions sum to 1
    "hous_frac_age_1981_2000",

    # housing tenure fractions sum to 1
    "demogr_frac_tenure_rented",
]


# ---------------------------------------------------------------------
# Non-informative Feature Exclusions
#
# Some feature are simply zero at all times.
# We exclude those b/c there is no infomration there.
# ---------------------------------------------------------------------

NONINFORMATIVE_FEATURE_DROP = [
    "geolprov_arctic_continental_shelf",
    "geolprov_arctic_platform",
    "geolprov_bear_province",
    "geolprov_innuitian_orogen",
    "geolprov_oceanic_crust",
    "geolprov_slave_province",
    "sedi_weathered_bedrock_or_regolith",
]


####################################################################
####  BASIC NECESSARY EXCLUSIONS
###################################################################

BASAL_FEATURE_EXCLUDE = (
    NON_FEATURE_COLUMNS
    + COMPOSITIONAL_FEATURE_DROP
    + NONINFORMATIVE_FEATURE_DROP
)

# --------------------------------------------------
# Optional exclusion sets
# --------------------------------------------------

LOW_IMPACT_EXCLUDE = [
    "demogr_num_total_dwellings",
    "demogr_num_occ_dwellings",
]

SPATIAL_EXCLUDE = [
    "latitude",
    "longitude",
]

SOCIOECONOMIC_EXCLUDE = [
    "socioeco_frac_govt_transfers",
    "socioeco_frac_nonlaborer",
]

OPTIONAL_FEATURE_EXCLUDES = {
    "low_impact": LOW_IMPACT_EXCLUDE,
    "spatial": SPATIAL_EXCLUDE,
    "socioeconomic": SOCIOECONOMIC_EXCLUDE,
}
