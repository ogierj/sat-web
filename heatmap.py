import pandas as pd
import streamlit as st
import folium
from streamlit_folium import folium_static
from folium.plugins import HeatMap

# Load data
@st.cache_data
def load_data():
    return pd.read_csv('data/nig_eth.csv')

# Load the combined data
data = load_data()

# Separate data for Ethiopia and Nigeria
ethiopia_data = data[data['country'] == 'eth']
nigeria_data = data[data['country'] == 'ng']

st.write("Sample of Ethiopia Data:")
st.write(ethiopia_data.head())

# Title and description for the heatmaps
st.title("Consumption Heatmaps")
st.write("This application shows consumption heatmaps for Ethiopia and Nigeria.")

# Ethiopia heatmap
st.header("Ethiopia Consumption Heatmap")
st.write("This heatmap shows the consumption data in Ethiopia.")

eth_map = folium.Map(location=[9.145, 40.4897], zoom_start=6)
eth_heat_data = [[row['cluster_lat'], row['cluster_lon'], row['cons_pc']] for index, row in ethiopia_data.iterrows()]
HeatMap(eth_heat_data, radius=15, blur=10, max_zoom=1).add_to(eth_map)
folium_static(eth_map)

# Nigeria heatmap
st.header("Nigeria Consumption Heatmap")
st.write("This heatmap shows the consumption data in Nigeria.")

nig_map = folium.Map(location=[9.0820, 8.6753], zoom_start=6)
nig_heat_data = [[row['cluster_lat'], row['cluster_lon'], row['cons_pc']] for index, row in nigeria_data.iterrows()]
HeatMap(nig_heat_data, radius=15, blur=10, max_zoom=1).add_to(nig_map)
folium_static(nig_map)


