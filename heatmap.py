import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import folium_static
from folium.plugins import HeatMap

#Create a new .csv df for Nigeria
cons_agg = pd.read_csv('data/cons_agg_wave3_visit1.csv')
household_geo = pd.read_csv('data/nga_householdgeovars_y3.csv')

merged_df = pd.merge(cons_agg, household_geo, on='hhid')

final_df = merged_df[['hhid', 'totcons', 'LAT_DD_MOD', 'LON_DD_MOD']]

final_df.to_csv('data/final_nga_data.csv', index=False)

# Plot heatmaps for Ethiopia and Nigeria
# Load data
@st.cache_data
def load_ethiopia_data():
    return pd.read_csv('data/eth_cons_pp_clust.csv')

@st.cache_data
def load_nigeria_data():
    return pd.read_csv('data/final_nga_data.csv')

# Load Ethiopia data
ethiopia_data = load_ethiopia_data()

# Load Nigeria data
nigeria_data = load_nigeria_data()

# Title and description for Ethiopia heatmap
st.title("Consumption Heatmaps")
st.write("This application shows consumption heatmaps for Ethiopia and Nigeria.")

# Ethiopia heatmap
st.header("Ethiopia Consumption Heatmap")
st.write("This heatmap shows the consumption data in Ethiopia.")

eth_map = folium.Map(location=[9.145, 40.4897], zoom_start=6)
eth_heat_data = [[row['lat_dd_mod'], row['lon_dd_mod'], row['cons_pp']] for index, row in ethiopia_data.iterrows()]
HeatMap(eth_heat_data, radius=15, blur=10, max_zoom=1).add_to(eth_map)
folium_static(eth_map)

# Nigeria heatmap
st.header("Nigeria Consumption Heatmap")
st.write("This heatmap shows the consumption data in Nigeria.")

nig_map = folium.Map(location=[9.0820, 8.6753], zoom_start=6)
nig_heat_data = [[row['LAT_DD_MOD'], row['LON_DD_MOD'], row['totcons']] for index, row in nigeria_data.iterrows()]
HeatMap(nig_heat_data, radius=15, blur=10, max_zoom=1).add_to(nig_map)
folium_static(nig_map)

