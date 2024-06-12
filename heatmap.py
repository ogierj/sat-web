import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import folium_static
from folium.plugins import HeatMap

# Load data
@st.cache_data
def load_data():
    data = pd.read_csv('eth_cons_pp_clust.csv')
    return data

data = load_data()

st.title("Ethiopia Consumption Heatmap")
st.write("This heatmap shows the consumption data in Ethiopia.")

m = folium.Map(location=[9.145, 40.4897], zoom_start=6)

heat_data = [[row['lat_dd_mod'], row['lon_dd_mod'], row['cons_pp']] for index, row in data.iterrows()]

HeatMap(heat_data, radius=15, blur=10, max_zoom=1).add_to(m)

folium_static(m)

