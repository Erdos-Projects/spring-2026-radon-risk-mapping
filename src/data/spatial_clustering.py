import pandas as pd
import geopandas as gpd
from spatialkfold.clusters import spatial_kfold_clusters


# ---------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------

CANADA_ALBERS_EPSG = "EPSG:3347"
DEFAULT_N_CLUSTERS = 200
RANDOM_STATE = 42


def create_spatial_clusters(
    df,
    n_clusters=DEFAULT_N_CLUSTERS
):
    """
    Generate spatial clusters using KMeans for spatial cross-validation.

    Parameters
    ----------
    df : pandas.DataFrame
        this is the main dataset that is a pandas df containing 
            latitude and longitude in Canada as columns
    n_clusters : int
        Number of spatial clusters.

    Returns
    -------
    GeoDataFrame with new 'spatial_cluster' column
    """
    
    # validate data
    required_columns = {"longitude", "latitude"}

    missing = required_columns - set(df.columns)

    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    # sort data to keep kmeans behavior reproducible
    df_sorted = df.sort_values(["longitude", "latitude"]).reset_index(drop=True)

    # create our GeoDF
    gdf = gpd.GeoDataFrame(
        df_sorted,
        geometry=gpd.points_from_xy(df_sorted.longitude, df_sorted.latitude),
        crs="EPSG:4326"
    )

    # Project to metric CRS for Canada
    # Need this for meaningful spatial kmeans calculation
    gdf = gdf.to_crs(CANADA_ALBERS_EPSG)

    # create unique id column for spatial-kfold function
    gdf["spkf_id"] = range(len(gdf))

    gdf_clusters = spatial_kfold_clusters(
        gdf=gdf,
        name="spkf_id",
        nfolds=n_clusters,
        algorithm="kmeans",
        random_state=RANDOM_STATE
    )

    gdf_clusters = gdf_clusters.rename(
        columns={"folds": "spatial_cluster"}
    )

    return gdf_clusters