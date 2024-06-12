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
from utils import load_known_data
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
                place_info = df[(df['cluster_lat'] == lat) & (df['cluster_lon'] == lon)]
                if not place_info.empty:
                    info = place_info.iloc[0]
                    st.session_state['clicked_info'] = {
                        'area_name': info['area_name'],
                        'Economic Position': info['Economic Position'],
                        'Demographics': info['Demographics']
                    }
                else:
                    st.warning("No information available for the clicked location.")
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

    # Display clicked info if available
    if 'clicked_info' in st.session_state:
        info = st.session_state['clicked_info']
        st.write(f"### {info['area_name']}")
        st.write(f"**Economic Position:** {info['Economic Position']}")
        st.write(f"**Demographics:** {info['Demographics']}")

    # # Additional feature: Generate prediction based on button click
    # st.write("## Generate your prediction:")
    
    # def stream_data(text, delay=0.04):
    #     for char in text:
    #         yield char
    #         time.sleep(delay)
    
    # if st.button("Generate Prediction"):
    #     if 'last_clicked' in map_data and map_data['last_clicked']:
    #         clicked_location = map_data['last_clicked']['lat'], map_data['last_clicked']['lng']
    #         formatted_lat = f"{clicked_location[0]:.6f}"
    #         formatted_lng = f"{clicked_location[1]:.6f}"
    #         place_name = get_place_name(formatted_lat, formatted_lng)
    #         loc = f"Latitude: {formatted_lat}, Longitude: {formatted_lng}"
    #         place_name_text = f"Place: {place_name}"
    #         prediction = make_prediction(formatted_lat, formatted_lng)
    #         pred_text = f"## {prediction}"
            
    #         st.write("### Location:")
    #         st.write_stream(lambda: stream_data(loc))
    #         st.write_stream(lambda: stream_data(place_name_text))
            
    #         st.write("### Prediction:")
    #         with st.spinner("Calculating..."):
    #             time.sleep(2)
    #         st.write_stream(lambda: stream_data(pred_text, delay=0.15))