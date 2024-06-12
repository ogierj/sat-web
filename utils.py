import numpy as np
from geopy.geocoders import Nominatim
import streamlit as st
import pandas as pd
import pydeck as pdk

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

def create_3d_barchart(df, lat_col, lon_col, elevation_col, tooltip_col, initial_lat, initial_lon, zoom=9, pitch=50):
    """
    Create a 3D bar chart on a map using Pydeck in Streamlit.

    Parameters:
    df (pd.DataFrame): DataFrame containing the data.
    lat_col (str): Column name for latitude.
    lon_col (str): Column name for longitude.
    elevation_col (str): Column name for elevation data.
    tooltip_col (str or None): Column name for tooltip information, or None if not available.
    initial_lat (float): Initial latitude for the map view.
    initial_lon (float): Initial longitude for the map view.
    zoom (int, optional): Initial zoom level for the map. Default is 9.
    pitch (int, optional): Initial pitch for the map. Default is 50.
    """
    # Initial view state of the map
    view_state = pdk.ViewState(
        latitude=initial_lat,
        longitude=initial_lon,
        zoom=zoom,
        pitch=pitch
    )

    # Define the HexagonLayer
    hex_layer = pdk.Layer(
        'HexagonLayer',
        data=df,
        get_position=f'[{lon_col}, {lat_col}]',
        radius=1000,
        elevation_scale=1000,
        elevation_range=[0, 1000],
        pickable=True,
        extruded=True,
        get_elevation=elevation_col,
        auto_highlight=True,
        get_fill_color=[255, 0, 0, 200],
    )

    # Define the ScatterplotLayer
    scatter_layer = pdk.Layer(
        'ScatterplotLayer',
        data=df,
        get_position=f'[{lon_col}, {lat_col}]',
        get_color='[200, 30, 0, 160]',
        get_radius=300,
        elevation_scale=1000,
    )

    # Define the Deck
    deck = pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=view_state,
        layers=[hex_layer, scatter_layer],
        tooltip={"text": f"{{{tooltip_col}}}" if tooltip_col else None}
    )

    # Render the map
    st.pydeck_chart(deck)
