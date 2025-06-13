# 📦 Load libraries
import pandas as pd
import folium
from folium.plugins import MarkerCluster

# 📁 Load your file
df = pd.read_csv("../data/SUOMI_VIIRS_C2_USA_contiguous_and_Hawaii_24h.csv")
df.head()

# Choose center of map
map_center = [df['latitude'].mean(), df['longitude'].mean()]
m = folium.Map(location=map_center, zoom_start=5)

# Cluster markers
cluster = MarkerCluster().add_to(m)

# Add detections
for _, row in df.iterrows():
    color = 'red' if row['bright_ti4'] > 330 else 'orange'
    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=3,
        popup=f"FRP: {row['frp']}, Brightness: {row['bright_ti4']}",
        color=color,
        fill=True,
        fill_opacity=0.6
    ).add_to(cluster)

# Save map
m.save("../data/viirs_fire_map.html")
