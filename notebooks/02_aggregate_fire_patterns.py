import pandas as pd

# Load file
df = pd.read_csv("../data/SUOMI_VIIRS_C2_USA_contiguous_and_Hawaii_24h.csv")

# Convert to datetime
df['acq_datetime'] = pd.to_datetime(df['acq_date'].astype(str) + df['acq_time'].astype(str).str.zfill(4), format='%Y-%m-%d%H%M')

# 🔢 Daily fire counts
daily_counts = df.groupby(df['acq_date']).size().reset_index(name='fire_count')
print(daily_counts.head())

# Optionally: filter to "daytime" or brightness above threshold

# Define a grid resolution
lat_bin = (df['latitude'] * 2).round() / 2   # 0.5° bins
lon_bin = (df['longitude'] * 2).round() / 2

df['lat_bin'] = lat_bin
df['lon_bin'] = lon_bin

grid_counts = df.groupby(['acq_date', 'lat_bin', 'lon_bin']).size().reset_index(name='fire_count')
print(grid_counts.head())
