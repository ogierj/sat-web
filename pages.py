import streamlit as st
import pandas as pd
import pydeck as pdk
from streamlit_folium import st_folium, folium_static
import requests
import numpy as np
import time
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import folium
from utils import load_known_data, create_3d_barchart
from folium.plugins import HeatMap


def home():
    st.title("Predicting Consumption Using Satellite Images")
    st.write("Welcome to our live prediction website using streamlit!")

    st.write("""
    The aim of our final project is to predict an economic outcome, in this case, consumption, from satellite images as an alternative to ground survey data. We used a transfer learning convolutional neural network, VGG16, which is already trained on recognising image features.
    """)
    
    st.write("""
    Participants: Ladislas, Luca, Jacques, and Annabel.
    """)

    st.write("""
    Acknowledgements to LeWagon batch managers and TAs, especially Charlotte and Mischa.
    """)
    
def heatmap_page():
    data = load_known_data()

    # Separate data for Ethiopia and Nigeria
    ethiopia_data = data[data['country'] == 'eth']
    nigeria_data = data[data['country'] == 'ng']

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

def prediction_map():
    st.title("Prediction by Location")
    st.write("Click anywhere (read: Nigeria or Ethiopia) on the map of Africa to choose a location for prediction.")
    
    # Load data
    df = load_known_data()

    # Function to get place name from coordinates, including timeout issues and errors
    def get_place_name(lat, lon):
        geolocator = Nominatim(user_agent="geoapiExercises", timeout=10)  # Set timeout to 10 seconds
        try:
            location = geolocator.reverse((lat, lon), exactly_one=True)
            return location.address if location else "Unknown location"
        except GeocoderTimedOut:
            return "Geocoding service timed out. Please try again later."
        except GeocoderServiceError as e:
            if "403" in str(e):
                return "Access to the geocoding service was denied. Please try again later."
            return f"An error occurred: {str(e)}"
        except Exception as e:
            return f"An error occurred: {str(e)}"
    
    
    # Function to simulate a machine learning prediction
    def make_prediction(lat, lon):
        # In a real scenario, replace this with the actual model prediction
        # For example: return model.predict([lat, lon])
        return np.random.choice(["Class A", "Class B", "Class C"])

    # Handle the click event
    def handle_click(map_data, df):
        try:
            if map_data:
                clicked = map_data[0]
                lon, lat = clicked['coordinates']
                place_name = get_place_name(lat, lon)
                prediction = make_prediction(lat, lon)
                st.write(f"Clicked Location: Latitude {lat}, Longitude {lon}")
                st.write(f"Place Name: {place_name}")
                st.write(f"Prediction: {prediction}")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

    # Create a map centered around Africa
    africa_map = folium.Map(location=[0, 20], zoom_start=3)
    africa_map.add_child(folium.LatLngPopup())
    
    # Display the map in the Streamlit app and capture click events
    map_data = st_folium(africa_map, width=700, height=500)

    # # Check if a point was clicked and handle the event
    if 'last_clicked' in map_data and map_data['last_clicked']:
        handle_click([{'coordinates': [map_data['last_clicked']['lng'], map_data['last_clicked']['lat']]}], df)

def barchart():
    # Load data
    data = load_known_data()

    # Separate data for Ethiopia and Nigeria
    ethiopia_data = data[data['country'] == 'eth']
    nigeria_data = data[data['country'] == 'ng']

    # Create map for Ethiopia
    st.header("Ethiopia Map")
    create_3d_barchart(
        df=ethiopia_data,
        lat_col='cluster_lat',
        lon_col='cluster_lon',
        elevation_col='cons_pc',
        tooltip_col=None,  # No tooltip column
        initial_lat=8.990161,
        initial_lon=38.754737
    )

    # Create map for Nigeria
    st.header("Nigeria Map")
    create_3d_barchart(
        df=nigeria_data,
        lat_col='cluster_lat',
        lon_col='cluster_lon',
        elevation_col='cons_pc',
        tooltip_col=None,  # No tooltip column
        initial_lat=9.082,
        initial_lon=8.6753
    )
