import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# Load fire CSV
df = pd.read_csv("../data/SUOMI_VIIRS_C2_USA_contiguous_and_Hawaii_24h.csv")

# Create geometry column
geometry = [Point(xy) for xy in zip(df.longitude, df.latitude)]
gdf_fires = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")

# Load US states shapefile
states = gpd.read_file("../data/shapefiles/usa_states/cb_2022_us_state_500k.shp")

# Spatial join: fires + states
states = states.to_crs("EPSG:4326")
fires_with_state = gpd.sjoin(gdf_fires, states, how="inner", predicate="within")

# Group by state name
by_state = fires_with_state.groupby("NAME").size().reset_index(name="fire_count")
by_state = by_state.sort_values("fire_count", ascending=False)

print(by_state.head(10))
