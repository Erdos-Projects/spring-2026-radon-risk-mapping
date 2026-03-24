#parameters for initial spatial (outer) cv fold
N_SPATIAL_CLUSTERS = 200 # number of k-means clusters that we use to spatially divide Canada
# 200 nicely separates Toronto and Missasauga without overly subdividing

NUM_TEST_SPLITS = 5  # KFOLD SPLITTING NEEDS AN INTEGER: 1/N gives the fractional size of the test split
NUM_CV_SPLITS = 5  # Number of folds for kfold splitting

OUTER_FOLD_COLUMN = "cv_fold"

# parameters for the nested cv 

INNER_CV_GROUP_COLUMN = "spatial_cluster"
INNER_CV_STRATIFY_COLUMN = "provinceterritory"
TEST_FLAG_COLUMN = "is_test"
N_INNER_SPLITS = 3
