# 🔥 Wildfire Detection Dashboard

An interactive, satellite-powered dashboard to monitor near real-time wildfire activity across the United States.

## 📍 About

This dashboard visualizes active fire data from the **NASA FIRMS VIIRS** (Visible Infrared Imaging Radiometer Suite) satellite. It provides insights into wildfire detections by:
- Date and time of acquisition
- Fire brightness (thermal intensity)
- Day vs. night detection
- Geographic distribution (point map and choropleth)

Built for researchers, analysts, emergency responders, and policymakers to monitor fire risk and emerging hotspots.

## 🛰️ Data Source

- **NASA FIRMS**: [https://firms.modaps.eosdis.nasa.gov/](https://firms.modaps.eosdis.nasa.gov/)
- **Dataset**: SUOMI VIIRS C2 – USA Contiguous & Hawaii – Last 24 Hours
- **Update frequency**: Multiple times a day
- **Format**: CSV (includes lat/lon, brightness, FRP, satellite, day/night, confidence)

## 🚀 Features

- 🔧 Interactive filters by brightness and day/night
- 🗺️ Folium-based fire detection map with clustering
- 🗺️ Choropleth map by U.S. state
- 📈 Daily fire detection trends
- 🌡️ Climate and 🔮 ML prediction tabs (coming soon!)
- 🔥 Themed dark-mode UI with blurred background image

## 📦 Tech Stack

- **Frontend**: Streamlit, Plotly, Folium, Leaflet.js
- **Backend**: Python, Pandas, GeoPandas
- **Deployment**: (Coming soon) Streamlit Community Cloud or AWS

## 🛠️ Setup Instructions

1. **Clone this repo**

   ```bash
   git clone git@github.com:your-username/wildfire-detection.git
   cd wildfire-detection```

2. **Create Virtual Environment**

    ```python3 -m venv env
    source env/bin/activate```

3. **Install Dependencies**

    ```pip install -r requirements.txt

4. **Run Streamlit app**

    ```streamlit run notebooks/dashboard.py

## 📁 File Structure

    wildfire-detection/
    ├── data/
    │   ├── SUOMI_VIIRS_C2_USA_contiguous_and_Hawaii_24h.csv
    │   └── shapefiles/
    ├── notebooks/
    │   ├── dashboard.py
    │   ├── 01_explore_viirs_fires.py
    │   ├── 02_aggregate_fire_patterns.py
    │   └── 03_fire_by_state.py
    ├── static/
    │   ├── wildfire_bg.png
    │   └── screenshot.png
    ├── .gitignore
    ├── requirements.txt
    └── README.md

## 🙋‍♀️ Author

    Ayushi Joshi
    Built with 💻 in VSCode and ☁️ powered by NASA FIRMS.


