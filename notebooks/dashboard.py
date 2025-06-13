import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
import json
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
import plotly.express as px


# ----------------------------
# 🌟 Page Setup
# ----------------------------

st.set_page_config(
    page_title="Wildfire Detection Dashboard",
    layout="wide"
)


st.title("🔥 Wildfire Detection Dashboard")
st.markdown("An interactive tool to visualize near-real-time wildfire activity in the U.S. using VIIRS satellite data.")

# ----------------------------
# 📦 Load Data
# ----------------------------
@st.cache_data
def load_fire_data():
    df = pd.read_csv("data/SUOMI_VIIRS_C2_USA_contiguous_and_Hawaii_24h.csv")
    df["acq_date"] = pd.to_datetime(df["acq_date"]).dt.date
    return df

@st.cache_data
def load_state_shapes():
    shp = gpd.read_file("data/shapefiles/usa_states/cb_2022_us_state_500k.shp").to_crs("EPSG:4326")
    return shp

fires = load_fire_data()
states = load_state_shapes()

# ----------------------------
# 🛠️ Preprocess
# ----------------------------
geometry = gpd.points_from_xy(fires.longitude, fires.latitude)
gdf = gpd.GeoDataFrame(fires, geometry=geometry, crs="EPSG:4326")
joined = gpd.sjoin(gdf, states, how="inner", predicate="within")
fire_by_state = joined.groupby("NAME").size().reset_index(name="fire_count").sort_values("fire_count", ascending=False)

# ----------------------------
# 🗺️ Tabs
# ----------------------------
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📍 Overview", "🗺️ Fire Map", "🗺️ Choropleth",
    "📈 Time Series", "🌡️ Climate", "🤖 ML Predictions"
])

# ----------------------------
# 📍 Overview Tab
# ----------------------------
with tab1:
    st.header("📍 Overview")
    st.markdown("""
    This dashboard provides a near real-time view of wildfire activity across the United States, using satellite data from **NASA FIRMS (Fire Information for Resource Management System)**.  
    Fires are detected by the **VIIRS instrument onboard the Suomi NPP satellite**, based on thermal anomalies captured in Band 4 (TI4).
    """)

    st.markdown("### 📆 Data Source")
    st.markdown("""
    - [NASA FIRMS](https://firms.modaps.eosdis.nasa.gov/)
    - Dataset: SUOMI VIIRS C2 – USA Contiguous & Hawaii – 24h
    - Format: CSV with latitude, longitude, brightness, date/time, confidence, satellite ID
    """)

    col1, col2 = st.columns(2)
    col1.metric("Total Detections", len(fires))
    col2.metric("Latest Date", str(fires["acq_date"].max()))

    st.markdown("### 📊 Detection Summary")
    col3, col4, col5 = st.columns(3)
    col3.metric("Night Detections", (fires["daynight"] == "N").sum())
    col4.metric("Day Detections", (fires["daynight"] == "D").sum())
    col5.metric("Brightness Range", f"{fires['bright_ti4'].min():.1f}K – {fires['bright_ti4'].max():.1f}K")

    st.markdown("### 🌍 Top 5 States by Detections")
    st.dataframe(fire_by_state.head(5), use_container_width=True)

# ----------------------------
# 🗺️ Fire Map Tab
# ----------------------------
with tab2:
    st.header("🗺️ Fire Detection Map")

    st.markdown("""
    **Brightness (TI4):** Thermal band brightness temperature (K). Higher means hotter fire.
    **Day/Night:** Choose day or night satellite pass.
    """)

    col1, col2 = st.columns([3, 1])
    with col1:
        min_bright = st.slider("Minimum Brightness (TI4)", 300.0, 350.0, 310.0)
    with col2:
        daynight_filter = st.selectbox("Detection Time", ["All", "Day Only", "Night Only"])

    filtered = fires[fires["bright_ti4"] >= min_bright]
    if daynight_filter == "Day Only":
        filtered = filtered[filtered["daynight"] == "D"]
    elif daynight_filter == "Night Only":
        filtered = filtered[filtered["daynight"] == "N"]

    m = folium.Map(location=[39.8283, -98.5795], zoom_start=4.5, tiles="CartoDB positron")
    cluster = MarkerCluster().add_to(m)
    for _, row in filtered.iterrows():
        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=3,
            popup=f"{row['acq_date']} | Brightness: {row['bright_ti4']}",
            color='red', fill=True, fill_opacity=0.6
        ).add_to(cluster)
    folium_static(m, width=1150, height=650)

# ----------------------------
# 🗺️ Choropleth
# ----------------------------
with tab3:
    st.header("\U0001f5fa️ Fire Counts by State (Choropleth)")
    merged = states.merge(fire_by_state, on="NAME", how="left").fillna(0)
    merged = merged[~merged["STUSPS"].isin(["AK", "HI", "PR"])]
    merged_json = json.loads(merged.to_json())

    fig = px.choropleth(
        merged,
        geojson=merged_json,
        locations="NAME",
        featureidkey="properties.NAME",
        color="fire_count",
        color_continuous_scale="YlOrRd",
        projection="albers usa",
        labels={"fire_count": "Fire Count"},
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, height=600)
    st.plotly_chart(fig, use_container_width=True)

# ----------------------------
# 📈 Time Series
# ----------------------------
with tab4:
    st.header("\U0001f4c8 Fire Trends Over Time")
    ts = fires.groupby("acq_date").size().reset_index(name="fire_count")
    ts["acq_date"] = pd.to_datetime(ts["acq_date"])
    fig = px.line(ts, x="acq_date", y="fire_count", title="Daily Fire Detections")
    fig.update_layout(xaxis_title="Date", yaxis_title="Fire Count", height=400)
    st.plotly_chart(fig, use_container_width=True)

# ----------------------------
# 🌡️ Climate
# ----------------------------
with tab5:
    st.header("🌡️ Climate Overlay (Coming Soon)")
    st.info("Temperature, wind, and humidity overlays will be added here.")

# ----------------------------
# 🤖 ML Placeholder
# ----------------------------
with tab6:
    st.header("🤖 Fire Risk Prediction (Coming Soon)")
    st.info("Model-predicted risk zones based on climate and satellite features.")

# ----------------------------
# 🔿️ Footer
# ----------------------------
st.markdown("---")
st.caption("Built by Ayushi Joshi | Powered by NASA FIRMS, GeoPandas, and Streamlit")