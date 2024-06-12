import numpy as np
from geopy.geocoders import Nominatim
import streamlit as st
import pandas as pd

def make_prediction(location):
    # Dummy function for making predictions
    return np.random.choice(["Class A", "Class B", "Class C"])

def get_place_name(lat, lon):
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.reverse((lat, lon), exactly_one=True)
    return location.address if location else "Unknown location"

def stream_data(data, delay=0.04):
    for char in data:
        yield char
        time.sleep(delay)
        
@st.cache_data
def load_known_data():
    return pd.read_csv('data/nig_eth.csv')

# def handle_click(map_data, df):
#     try:
#         if map_data:
#             clicked = map_data[0]
#             lon, lat = clicked['coordinates']
#             place_name = get_place_name(lat, lon)
#             prediction = make_prediction(lat, lon)
#             st.write(f"Clicked Location: Latitude {lat}, Longitude {lon}")
#             st.write(f"Place Name: {place_name}")
#             st.write(f"Prediction: {prediction}")
            
#             place_info = df[(df['cluster_lat'] == lat) & (df['cluster_lon'] == lon)]
#             if not place_info.empty:
#                 info = place_info.iloc[0]
#                 st.session_state['clicked_info'] = {
#                     'area_name': info['area_name'],
#                     'Economic Position': info['Economic Position'],
#                     'Demographics': info['Demographics']
#                 }
#             else:
#                 st.warning("No information available for the clicked location.")
#     except Exception as e:
#         st.error(f"An error occurred: {str(e)}")