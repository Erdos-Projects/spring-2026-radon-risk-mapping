import pandas as pd
import numpy as np



# ============================================
# Feature name standardization
# ============================================
COLUMN_REMAP = {

    # FSA
    "FSA": "fsa",

    # dwelling composition (compositional group: type)
    "frac_single_detached": "hous_frac_type_single_detached",
    "frac_highrise": "hous_frac_type_highrise",
    "frac_other_attached": "hous_frac_type_other_attached",
    "frac_movable": "hous_frac_type_movable",

    # structure
    "avg_rooms": "hous_avg_rooms",
    "frac_major_repair": "hous_frac_major_repair",

    # construction age (compositional group: age)
    "frac_pre_1980": "hous_frac_age_pre_1980",
    "frac_1981_2000": "hous_frac_age_1981_2000",
    "frac_post_2001": "hous_frac_age_post_2001",

    # housing value
    "median_home_value": "hous_median_value",

    # demographics
    "pop_2016": "demogr_pop_2016",
    "num_dwellings": "demogr_num_total_dwellings",
    "occ_dwellings": "demogr_num_occ_dwellings",
    "median_age": "demogr_median_age",
    "avg_household_size": "demogr_avg_household_size",

    # housing tenure (compositional group: tenure)
    "frac_owned": "demogr_frac_tenure_owned",
    "frac_rented": "demogr_frac_tenure_rented",
    "frac_band": "demogr_frac_tenure_band",

    # income
    "frac_low_income": "socioeco_frac_low_income",
    "med_income": "socioeco_median_income",
    "frac_high_income": "socioeco_frac_high_income",
    "frac_govt_transfers": "socioeco_frac_govt_transfers",

    # labor
    "unemployment_rate": "socioeco_frac_unemployment_rate",
    "frac_non_laborer": "socioeco_frac_nonlaborer",

    # education
    "frac_bachelor_plus": "socioeco_frac_bachelor_plus",

    # housing stress
    "frac_overcrowded": "socioeco_frac_overcrowded",
    "frac_unsuitable_housing": "socioeco_frac_unsuitable_housing",
    "frac_housing_poor_owners": "socioeco_frac_housing_burden",
}


# ============================================
# Helper fucntions
# ============================================

def _clean_census_column_names(df):
    df = df.copy()

    # Remove stray quotes
    df.columns = df.columns.str.replace('"', '', regex=False)

    return df


def _filter_census_fsa(raw_census_df):
    """
    Filter Census Profile data to FSA level only.
    Removes national aggregate row.
    """
    df = raw_census_df.copy()

    # Keep only FSA geography
    #df = df[df["GEO_LEVEL"] == "Forward Sortation Area"]
    df = df[df["GEO_LEVEL"] == 2]

    # Remove Canada aggregate
    df = df[df["GEO_CODE (POR)"] != "01"]

    return df


def _pivot_census_long_to_wide(df):
    """
    Convert Census Profile long format to wide format.
    Rows: FSA
    Columns: Member ID
    Values: Total - Sex column
    """

    value_col = "Dim: Sex (3): Member ID: [1]: Total - Sex"
    member_col = "Member ID: Profile of Forward Sortation Areas (2247)"
    geo_col = "GEO_CODE (POR)"

    # Convert values to numeric
    df[value_col] = pd.to_numeric(df[value_col], errors="coerce")

    # Pivot
    df_wide = (
        df.pivot_table(
            index=geo_col,
            columns=member_col,
            values=value_col,
            aggfunc="first"
        )
        .reset_index()
    )

    # Rename GEO column to simple name
    df_wide = df_wide.rename(columns={geo_col: "FSA"})
    # Remove extra header
    df_wide.columns.name = None

    return df_wide


# ============================================
# Structural Features
# ============================================

def _build_dwelling_type_features(df_wide):
    """
    Compute dwelling structure proportions at FSA level.
    """
# ============================================
# Census Member ID Constants
# Structural Type of Dwelling (100% data)
# Source: 2016 Census Profile (98-401-X2016046)

    # Important:
    # Census counts are (sometimes) rounded to the nearest 5... cprrelated with small N
    # As a result, the published total (Member ID 41)
    # may not exactly equal the sum of top-level categories.
    # Instead, we compute the total ourselves...
# ============================================

    MEMBER_IDS = {
        # Parent total
        "total_occupied_private_dwellings": 41,

        # Top-level categories
        "single_detached": 42,
        "highrise_apartment_5plus": 43,
        "other_attached_total": 44,
        "movable_dwelling": 50,

        # Subcategories of "other_attached_total"
        "semi_detached": 45,
        "row_house": 46,
        "duplex": 47,
        "lowrise_apartment_lt5": 48,
        "other_single_attached": 49,
    }

    ids = MEMBER_IDS

    # Extract raw counts
    single_detached = df_wide[ids["single_detached"]]
    highrise = df_wide[ids["highrise_apartment_5plus"]]
    other_attached = df_wide[ids["other_attached_total"]]
    movable = df_wide[ids["movable_dwelling"]]

    # Recompute structural total from components
    structural_total = (
        single_detached +
        highrise +
        other_attached +
        movable
    )

    # Avoid divide-by-zero
    structural_total = structural_total.replace(0, np.nan)

    return pd.DataFrame({
        "FSA": df_wide["FSA"],
        "frac_single_detached": single_detached / structural_total,
        "frac_highrise": highrise / structural_total,
        "frac_other_attached": other_attached / structural_total,
        "frac_movable": movable / structural_total,
    })

def _build_avg_rooms_feature(df_wide):
    """
    Compute average number of rooms per dwelling.

    Source:
    2016 Census Profile (98-401-X2016046)
    Number of rooms (25% sample data)

    We use Member ID 1636, which is the precomputed
    average number of rooms per dwelling. 
    We don't use the categorical breakdown of room counts that is available...
    """

    MEMBER_IDS = {
        "avg_rooms": 1636
    }

    avg_rooms = df_wide[MEMBER_IDS["avg_rooms"]]

    return pd.DataFrame({
        "FSA": df_wide["FSA"],
        "avg_rooms": avg_rooms
    })

def _build_repair_status_feature(df_wide):
    """
    Compute proportion of dwellings requiring major repairs.

    Source:
    2016 Census Profile (98-401-X2016046)
    Condition of dwelling (25% sample data)

    Member IDs:
        1651 = Total occupied private dwellings (condition table)
        1653 = Major repairs needed

    Notes:
    - 25% sample data.
    - Counts are rounded to nearest 5 for some (all?) FSA's
    - Small FSAs may contain NaN values and weird rounding stuff...
    """

    MEMBER_IDS = {
        "total_condition": 1651,
        "major_repair": 1653,
    }

    total = df_wide[MEMBER_IDS["total_condition"]]
    major = df_wide[MEMBER_IDS["major_repair"]]

    # Avoid divide-by-zero
    total = total.replace(0, np.nan)

    return pd.DataFrame({
        "FSA": df_wide["FSA"],
        "frac_major_repair": major / total
    })

def _build_building_age_features(df_wide):
    """
    Compute building age composition features.

    Source:
    2016 Census Profile (98-401-X2016046)
    Period of construction (25% sample data)

    Member IDs:
        1644 to 1650 = construction year bins
        1643 = total (not used due to rounding artifacts)

    We aggregate bins into:
        - pre_1980
        - 1981_2000
        - post_2001

    Denominator is recomputed from bin counts to avoid rounding drift.
    """

    MEMBER_IDS = {
        "pre_1960": 1644,
        "1961_1980": 1645,
        "1981_1990": 1646,
        "1991_2000": 1647,
        "2001_2005": 1648,
        "2006_2010": 1649,
        "2011_2016": 1650,
    }

    ids = MEMBER_IDS

    # Extract counts
    pre_1960 = df_wide[ids["pre_1960"]]
    y1961_1980 = df_wide[ids["1961_1980"]]
    y1981_1990 = df_wide[ids["1981_1990"]]
    y1991_2000 = df_wide[ids["1991_2000"]]
    y2001_2005 = df_wide[ids["2001_2005"]]
    y2006_2010 = df_wide[ids["2006_2010"]]
    y2011_2016 = df_wide[ids["2011_2016"]]

    # Recompute total
    construction_total = (
        pre_1960 +
        y1961_1980 +
        y1981_1990 +
        y1991_2000 +
        y2001_2005 +
        y2006_2010 +
        y2011_2016
    )

    construction_total = construction_total.replace(0, np.nan)

    # Aggregate bins
    frac_pre_1980 = (pre_1960 + y1961_1980) / construction_total
    frac_1981_2000 = (y1981_1990 + y1991_2000) / construction_total
    frac_post_2001 = (y2001_2005 + y2006_2010 + y2011_2016) / construction_total

    return pd.DataFrame({
        "FSA": df_wide["FSA"],
        "frac_pre_1980": frac_pre_1980,
        "frac_1981_2000": frac_1981_2000,
        "frac_post_2001": frac_post_2001,
    })

def _build_home_value_feature(df_wide):
    """
    Extract median dwelling value (Member ID 1676).

    Source:
    2016 Census Profile (98-401-X2016046)
    Table: Value of dwelling (25% sample data)

    Defensive handling:
    - Convert to numeric.
    - Replace impossible values (<= 0) with NaN.
    """

    MEMBER_ID = 1676

    # Convert to numeric safely
    median_value = pd.to_numeric(
        df_wide[MEMBER_ID],
        errors="coerce"
    )

    # Sanity enforcement:
    # Median home value cannot be <= 0
    median_value = median_value.mask(median_value <= 0)

    return pd.DataFrame({
        "FSA": df_wide["FSA"],
        "median_home_value": median_value
    })

def _build_tenure_features(df_wide):
    """
    Build tenure-based housing proportions at FSA level.

    Uses 25% sample data:
        1617 - Total - Private households by tenure - 25% sample data (156)
        1618 - Owner
        1619 - Renter
        1620 - Band housing

    Denominator is recomputed as sum of the three components
    to avoid rounding inconsistencies in census totals.
    """

    MEMBER_IDS = {
        "owner": 1618,
        "renter": 1619,
        "band": 1620,
    }

    # Extract counts
    owner = pd.to_numeric(df_wide[MEMBER_IDS["owner"]], errors="coerce")
    renter = pd.to_numeric(df_wide[MEMBER_IDS["renter"]], errors="coerce")
    band = pd.to_numeric(df_wide[MEMBER_IDS["band"]], errors="coerce")

    # Recompute total from components (avoid census rounding artifacts)
    total = owner + renter + band

    # Prevent divide-by-zero
    total = total.mask(total == 0)

    return pd.DataFrame({
        "FSA": df_wide["FSA"],
        "frac_owned": owner / total,
        "frac_rented": renter / total,
        "frac_band": band / total,
    })

def _build_income_features(df_wide):
    """
    Build income-related socioeconomic features.

    Member IDs:
        857  - Prevalence of low income (LIM-AT) (%)
        742  - Median total income of households ($)
        693  - Population with total income
        707  - Population with income >= $150,000
        690  - Government transfers (%)

    frac_high_income is computed as:
        (count >=150k) / (count with total income)
    """

    MEMBER_IDS = {
        "pct_low_income": 857,
        "med_income": 742,
        "with_income": 693,
        "high_income_count": 707,
        "pct_govt_transfers": 690,
    }

    # Extract raw values
    frac_low_income = pd.to_numeric(df_wide[MEMBER_IDS["pct_low_income"]], errors="coerce") / 100
    med_income = pd.to_numeric(df_wide[MEMBER_IDS["med_income"]], errors="coerce")
    with_income = pd.to_numeric(df_wide[MEMBER_IDS["with_income"]], errors="coerce")
    high_income_count = pd.to_numeric(df_wide[MEMBER_IDS["high_income_count"]], errors="coerce")
    frac_govt_transfers = pd.to_numeric(df_wide[MEMBER_IDS["pct_govt_transfers"]], errors="coerce") / 100

    # Compute high income share safely
    denominator = with_income.mask(with_income == 0)
    frac_high_income = (high_income_count / denominator) 

    # Sanity enforcement
    frac_low_income = frac_low_income.mask((frac_low_income < 0) | (frac_low_income > 1))
    frac_govt_transfers = frac_govt_transfers.mask((frac_govt_transfers < 0) | (frac_govt_transfers > 1))

    med_income = med_income.mask(med_income <= 0)
    frac_high_income = frac_high_income.mask((frac_high_income < 0) | (frac_high_income > 1))

    return pd.DataFrame({
        "FSA": df_wide["FSA"],
        "frac_low_income": frac_low_income,
        "med_income": med_income,
        "frac_high_income": frac_high_income,
        "frac_govt_transfers": frac_govt_transfers,
    })

def _build_labor_features(df_wide):
    """
    Build labor force related features.

    Member IDs:
        1871 - Employment rate (%)
        1872 - Unemployment rate (%)
        1865 - Total population aged 15+
        1869 - Not in the labour force
    """

    MEMBER_IDS = {
        "employment_rate": 1871,
        "unemployment_rate": 1872,
        "total_15plus": 1865,
        "not_in_labor_force": 1869,
    }

    frac_employment_rate = pd.to_numeric(
        df_wide[MEMBER_IDS["employment_rate"]],
        errors="coerce"
    ) / 100

    frac_unemployment_rate = pd.to_numeric(
        df_wide[MEMBER_IDS["unemployment_rate"]],
        errors="coerce"
    ) / 100

    total_15plus = pd.to_numeric(
        df_wide[MEMBER_IDS["total_15plus"]],
        errors="coerce"
    )

    not_in_labor_force = pd.to_numeric(
        df_wide[MEMBER_IDS["not_in_labor_force"]],
        errors="coerce"
    )

    # Compute non-labor force percentage
    denominator = total_15plus.mask(total_15plus == 0)
    frac_non_laborer = (not_in_labor_force / denominator) 

    # Sanity enforcement
    frac_employment_rate = frac_employment_rate.mask(
        (frac_employment_rate < 0) | (frac_employment_rate > 1)
    )

    frac_unemployment_rate = frac_unemployment_rate.mask(
        (frac_unemployment_rate < 0) | (frac_unemployment_rate > 1)
    )

    frac_non_laborer = frac_non_laborer.mask(
        (frac_non_laborer < 0) | (frac_non_laborer > 1)
    )

    return pd.DataFrame({
        "FSA": df_wide["FSA"],
        "unemployment_rate": frac_unemployment_rate,
        "frac_non_laborer": frac_non_laborer,
    })

def _build_education_features(df_wide):
    """
    Build education-related features.

    Computes:
        frac_bachelor_plus
            = population aged 25–64 with bachelor's degree or higher
              divided by total population aged 25–64

    Member IDs:
        1698 - Total population aged 25–64
        1707 - Bachelor's degree or higher
    """

    MEMBER_IDS = {
        "total_25_64": 1698,
        "bachelor_plus": 1707,
    }

    total_25_64 = pd.to_numeric(
        df_wide[MEMBER_IDS["total_25_64"]],
        errors="coerce"
    )

    bachelor_plus = pd.to_numeric(
        df_wide[MEMBER_IDS["bachelor_plus"]],
        errors="coerce"
    )

    # Safe division
    denominator = total_25_64.mask(total_25_64 == 0)
    frac_bachelor_plus = (bachelor_plus / denominator) 

    # Sanity enforcement
    frac_bachelor_plus = frac_bachelor_plus.mask(
        (frac_bachelor_plus < 0) | (frac_bachelor_plus > 1)
    )

    return pd.DataFrame({
        "FSA": df_wide["FSA"],
        "frac_bachelor_plus": frac_bachelor_plus,
    })

def _build_overcrowding_feature(df_wide):
    """
    Build overcrowding feature.

    Computes:
        frac_overcrowded_households
            = households with >1 person per room
              divided by total households

    Member IDs:
        1637 - Total households (persons per room)
        1639 - More than 1 person per room
    """

    MEMBER_IDS = {
        "total_households": 1637,
        "overcrowded_households": 1639,
    }

    total_households = pd.to_numeric(
        df_wide[MEMBER_IDS["total_households"]],
        errors="coerce"
    )

    overcrowded_households = pd.to_numeric(
        df_wide[MEMBER_IDS["overcrowded_households"]],
        errors="coerce"
    )

    # Safe division
    denominator = total_households.mask(total_households == 0)
    frac_overcrowded = (overcrowded_households / denominator)

    # Sanity enforcement
    frac_overcrowded = frac_overcrowded.mask(
        (frac_overcrowded < 0) | (frac_overcrowded > 1)
    )

    return pd.DataFrame({
        "FSA": df_wide["FSA"],
        "frac_overcrowded": frac_overcrowded,
    })

def _build_housing_suitability_feature(df_wide):
    """
    Build housing suitability feature.

    Computes:
        frac_unsuitable_housing
            = households classified as "Not suitable"
              divided by total households

    Member IDs:
        1640 - Total households (housing suitability)
        1642 - Not suitable
    """

    MEMBER_IDS = {
        "total_households": 1640,
        "not_suitable": 1642,
    }

    total_households = pd.to_numeric(
        df_wide[MEMBER_IDS["total_households"]],
        errors="coerce"
    )

    not_suitable = pd.to_numeric(
        df_wide[MEMBER_IDS["not_suitable"]],
        errors="coerce"
    )

    # Safe division
    denominator = total_households.mask(total_households == 0)
    frac_unsuitable_housing = (not_suitable / denominator)

    # Sanity enforcement
    frac_unsuitable_housing = frac_unsuitable_housing.mask(
        (frac_unsuitable_housing < 0) | (frac_unsuitable_housing > 1)
    )

    return pd.DataFrame({
        "FSA": df_wide["FSA"],
        "frac_unsuitable_housing": frac_unsuitable_housing,
    })

def _build_housing_cost_burden_feature(df_wide):
    """
    Build housing cost burden feature for owner households.

    Computes:
        frac_housing_poor_owners
            = fraction of owner households spending >=30% of income on shelter

    Member ID:
        1673 - % of owner households spending 30%+ on shelter costs

        1671. Total - Owner households in non-farm, non-reserve private dwellings - 25% sample data
        1672.   % of owner households with a mortgage (168)
        1673.   % of owner households spending 30% or more of its income on shelter costs (169)
        1674.   Median monthly shelter costs for owned dwellings ($) (170)
        1675.   Average monthly shelter costs for owned dwellings ($) (171)
    """

    MEMBER_IDS = {
        "pct_housing_cost_burden": 1673
    }

    frac_housing_poor_owners = pd.to_numeric(
        df_wide[MEMBER_IDS["pct_housing_cost_burden"]],
        errors="coerce"
    ) / 100

    # Sanity enforcement
    frac_housing_poor_owners = frac_housing_poor_owners.mask(
        (frac_housing_poor_owners < 0) |
        (frac_housing_poor_owners > 1)
    )

    return pd.DataFrame({
        "FSA": df_wide["FSA"],
        "frac_housing_poor_owners": frac_housing_poor_owners,
    })


def _build_structural_features(df_wide):
    """
    Compose all structural (physical housing) features.
    """

    feature_blocks = []

    # Dwelling composition proportions
    feature_blocks.append(
        _build_dwelling_type_features(df_wide)
    )
    # Average number of rooms
    feature_blocks.append(_build_avg_rooms_feature(df_wide))
    # Proportion of hoouses in need of major repair
    feature_blocks.append(_build_repair_status_feature(df_wide))
    # Building age
    feature_blocks.append(_build_building_age_features(df_wide))
    # Median home value
    feature_blocks.append(_build_home_value_feature(df_wide))

    # Future additions:
    # feature_blocks.append(_build_housing_age_features(df_wide))
    # feature_blocks.append(_build_housing_condition_features(df_wide))

    # Iteratively merge all structural blocks
    structural = feature_blocks[0]

    for block in feature_blocks[1:]:
        structural = structural.merge(block, on="FSA", how="left")

    return structural

def _build_demographic_features(df_wide):
    """
    Build basic demographic and geographic control variables.

    These variables describe:
        - Population 
        - Density
        - Household structure
        - Age 
        - FSA size
        - number of houses
    
    Note that Member IDs 2,3,6, and 7 seem to not exist at the FSA level. 
    These correspond with 2011 population, population change, population density and land area.
    """

    MEMBER_IDS = {
        "pop_2016": 1,
        "num_dwellings": 4,
        "occ_dwellings": 5,
        "median_age": 40,
        "avg_household_size": 58,
    }

    # Extract and coerce to numeric
    pop_2016 = pd.to_numeric(df_wide[MEMBER_IDS["pop_2016"]], errors="coerce")
    num_dwellings = pd.to_numeric(df_wide[MEMBER_IDS["num_dwellings"]], errors="coerce")
    occ_dwellings = pd.to_numeric(df_wide[MEMBER_IDS["occ_dwellings"]], errors="coerce")
    median_age = pd.to_numeric(df_wide[MEMBER_IDS["median_age"]], errors="coerce")
    avg_household_size = pd.to_numeric(df_wide[MEMBER_IDS["avg_household_size"]], errors="coerce")
    
    # Minimal sanity enforcement
    pop_2016 = pop_2016.mask(pop_2016 < 0)
    num_dwellings = num_dwellings.mask(num_dwellings < 0)
    occ_dwellings = occ_dwellings.mask(occ_dwellings < 0)
    median_age = median_age.mask(median_age <= 0)
    avg_household_size = avg_household_size.mask(avg_household_size <= 0)

    return pd.DataFrame({
        "FSA": df_wide["FSA"],
        "pop_2016": pop_2016,
        "num_dwellings": num_dwellings,
        "occ_dwellings": occ_dwellings,
        "median_age": median_age,
        "avg_household_size": avg_household_size
    })


def _build_socioeconomic_features(df_wide):
    """
    Compose all socioeconomic features.

    Includes:
        - Tenure
        - Income
        - Labor force
        - Education
        - Housing stress
    """

    feature_blocks = []

    # Tenure proportions
    feature_blocks.append(_build_tenure_features(df_wide))
    feature_blocks.append(_build_income_features(df_wide))
    feature_blocks.append(_build_labor_features(df_wide))
    feature_blocks.append(_build_education_features(df_wide))
    feature_blocks.append(_build_overcrowding_feature(df_wide))
    feature_blocks.append(_build_housing_suitability_feature(df_wide))
    feature_blocks.append(_build_housing_cost_burden_feature(df_wide))

    # Iteratively merge all socioeconomic blocks
    socioeconomic = feature_blocks[0]

    for block in feature_blocks[1:]:
        socioeconomic = socioeconomic.merge(block, on="FSA", how="left")

    return socioeconomic



def build_census_fsa_matrix(raw_census_df):
    """
    Takes raw Census Profile dataframe.
    Returns clean FSA-level feature matrix.
    """
    
    # Clean column names
    df = _clean_census_column_names(raw_census_df)

    # Filter to FSA level
    df = _filter_census_fsa(df)

    # Pivot to wide format
    df_wide = _pivot_census_long_to_wide(df)

    # Build feature blocks
    structural = _build_structural_features(df_wide)
    demographic = _build_demographic_features(df_wide)
    socioeconomic = _build_socioeconomic_features(df_wide)

    # Merge all blocks
    features = structural.merge(
        demographic,
        on="FSA",
        how="left"
    )

    features = features.merge(
        socioeconomic,
        on="FSA",
        how="left"
    )

    # Optional: enforce consistent column order
    features = features.sort_values("FSA").reset_index(drop=True)

    # Rename columns so that they play nicely with other datasets
    features = features.rename(columns=COLUMN_REMAP)

    return features