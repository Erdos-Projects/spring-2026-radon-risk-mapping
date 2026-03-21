from pathlib import Path

# --------------------------------------------------
# Project root
# --------------------------------------------------

# config.py should be in /root/config/paths.py
PROJECT_ROOT = Path(__file__).resolve().parents[1]


# --------------------------------------------------
# Core directories
# --------------------------------------------------

DATA_DIR = PROJECT_ROOT / "data"

RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
FINAL_DATASET_DIR = DATA_DIR / "final_dataset"
FIGURES_DIR = PROJECT_ROOT / "figures"
MAPS_DIR = FIGURES_DIR / "maps"

NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"

SRC_DIR = PROJECT_ROOT / "src"


# --------------------------------------------------
# Raw datasets
# --------------------------------------------------

# Directories
CENSUS_RAW_DIR = RAW_DATA_DIR / "census_canada_2016" / "98-401-X2016046_eng_CSV"

RADON_RAW = RAW_DATA_DIR / "radon" / "radon-concentration.csv"

FSA_BOUNDARY_SHAPEFILE = RAW_DATA_DIR / "fsa_boundary" / "gfsa000a11a_e.shp"

URANIUM_RASTER = RAW_DATA_DIR / "uranium" / "Canada - 250m - RAD - Equivalent Uranium eU - 2025_Aug.ERS"

# Files
CENSUS_RAW_FILENAME = "98-401-X2016046_English_CSV_data.csv"
CENSUS_RAW = CENSUS_RAW_DIR / CENSUS_RAW_FILENAME
# # census data is stored locally b/c of size limits. 
# # gitignore hides this from the repo
# # download & unzip contents (census data files) to:    RAW_DATA_DIR / "census_canada_2016"
# # final intended filepath is: RAW_DATA_DIR / "census_canada_2016" / "98-401-X2016046_eng_CSV" / "98-401-X2016046_English_CSV_data.csv"
# #  ie CENSUS_RAW_DIR / CENSUS_RAW_FILENAME

# --------------------------------------------------
# Processed datasets
# --------------------------------------------------

# Files
RADON_CLEANED = PROCESSED_DATA_DIR / "radon-concentration-cleaned.csv"

CENSUS_FSA = PROCESSED_DATA_DIR / "fsa_census.csv"

FSA_CENTROIDS = PROCESSED_DATA_DIR / "fsa_centroids.csv"

URANIUM_FSA = PROCESSED_DATA_DIR / "fsa_uranium.csv"

GEOLOGY_FSA = PROCESSED_DATA_DIR / "geology_fsa_radon.csv"

SURFICIAL_FSA = PROCESSED_DATA_DIR / "surficial_fsa_radon.csv"

HEATING_DAYS = PROCESSED_DATA_DIR / "average_heating_days_cleaned.csv"


# --------------------------------------------------
# Modeling datasets
#   !!!  ACCESS WITH HELPER FUNCTIONS  !!!
#   !!!  (see: src/data/data_loading ) !!!
# --------------------------------------------------

# Directories
MODEL_DATA_DIR = DATA_DIR / "modeling"

SPATIAL_CV_DIR = MODEL_DATA_DIR / "spatial_cv"

# Files
SPATIAL_CV_DATASET = SPATIAL_CV_DIR / "dataset_with_spatial_cv_splits.csv"


# --------------------------------------------------
# Main aggregated dataset
# --------------------------------------------------

MAIN_DATASET = FINAL_DATASET_DIR / "main_dataset.csv"
