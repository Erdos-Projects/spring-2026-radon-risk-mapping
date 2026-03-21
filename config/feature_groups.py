# Dataset & project constants
RADON_HIGH_CONCENTRATION = 200
RANDOM_STATE = 42

#--------------------------------------
# Specify all the column names and put into groups

TARGET_COLUMN = "concentration"

METADATA_COLUMNS = [
"FSA",
"cv_fold",
"spatial_cluster",
"geometry",
"n_days",
"is_test",
"provinceterritory",
]

SPATIAL_FEATURES = [
"latitude",
"longitude",
]

WEATHER_FEATURES = [
    "average_heating_days",
]

GEOLOGY_FEATURES = [
    "geolprov_appalachian_orogen",
    "geolprov_arctic_continental_shelf",
    "geolprov_arctic_platform",
    "geolprov_atlantic_continental_shelf",
    "geolprov_bear_province",
    "geolprov_churchill_province",
    "geolprov_cordilleran_orogen",
    "geolprov_grenville_province",
    "geolprov_hudson_bay_lowlands",
    "geolprov_innuitian_orogen",
    "geolprov_interior_platform",
    "geolprov_nain_province",
    "geolprov_oceanic_crust",
    "geolprov_pacific_continental_shelf",
    "geolprov_slave_province",
    "geolprov_southern_province",
    "geolprov_st_lawrence_platform",
    "geolprov_superior_province",
    "geolprov_unknown",
    "rxtp_intrusive_rocks",
    "rxtp_metamorphic_rocks",
    "rxtp_sedimentary_and_volcanic_rocks",
    "rxtp_sedimentary_rocks",
    "rxtp_unknown",
    "rxtp_volcanic_rocks",
    "sedi_alluvial_sediments",
    "sedi_bedrock",
    "sedi_colluvial_and_mass-wasting_deposits",
    "sedi_eolian_sediments",
    "sedi_glacial_ice_or_snowpack",
    "sedi_glacial_sediments",
    "sedi_glaciofluvial_sediments",
    "sedi_glaciolacustrine_sediments",
    "sedi_glaciomarine_sediments",
    "sedi_lacustrine_sediments",
    "sedi_marine_sediments",
    "sedi_organic_deposits",
    "sedi_volcanic_deposits",
    "sedi_weathered_bedrock_or_regolith",
]

URANIUM_FEATURES = [
    "max_uranium",
    "mean_uranium",
]

HOUSING_FEATURES = [
    "hous_avg_rooms",
    "hous_frac_age_1981_2000",
    "hous_frac_age_post_2001",
    "hous_frac_age_pre_1980",
    "hous_frac_major_repair",
    "hous_frac_type_highrise",
    "hous_frac_type_movable",
    "hous_frac_type_other_attached",
    "hous_frac_type_single_detached",
    "hous_median_value",
]

DEMOGRAPHIC_FEATURES = [
    "demogr_avg_household_size",
    "demogr_frac_tenure_band",
    "demogr_frac_tenure_owned",
    "demogr_frac_tenure_rented",
    "demogr_median_age",
    "demogr_num_occ_dwellings",
    "demogr_num_total_dwellings",
    "demogr_pop_2016",
]

SOCIOECONOMIC_FEATURES = [
    "socioeco_frac_bachelor_plus",
    "socioeco_frac_govt_transfers",
    "socioeco_frac_high_income",
    "socioeco_frac_housing_burden",
    "socioeco_frac_low_income",
    "socioeco_frac_nonlaborer",
    "socioeco_frac_overcrowded",
    "socioeco_frac_unemployment_rate",
    "socioeco_frac_unsuitable_housing",
    "socioeco_median_income",
]


ALL_FEATURE_COLUMNS = (
    SPATIAL_FEATURES
    + WEATHER_FEATURES
    + GEOLOGY_FEATURES
    + URANIUM_FEATURES
    + HOUSING_FEATURES
    + DEMOGRAPHIC_FEATURES
    + SOCIOECONOMIC_FEATURES
)


##############################
#############################
# make it easy to access this stuff later...

FEATURE_GROUPS = {
    "spatial": SPATIAL_FEATURES,
    "weather": WEATHER_FEATURES,
    "geology": GEOLOGY_FEATURES,
    "uranium": URANIUM_FEATURES,
    "housing": HOUSING_FEATURES,
    "demographic": DEMOGRAPHIC_FEATURES,
    "socioeconomic": SOCIOECONOMIC_FEATURES,
}

