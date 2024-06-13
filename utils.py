import numpy as np
from geopy.geocoders import Nominatim
import streamlit as st
import pandas as pd
import pydeck as pdk
import math
import requests
import matplotlib.pyplot as plt
from requests.auth import HTTPBasicAuth
import json
from io import BytesIO
from shapely.geometry import Polygon

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

class PlanetDownloader:
    def __init__(self, api_key, item_type='PSScene'):
        self.api_key = api_key
        self.item_type = item_type
    
    def create_cords(lat, lon, zoom):
        xtile, ytile = deg_to_tile(lat, lon, zoom)

        coords = [tilexy_to_deg(xtile, ytile, zoom, a, b) for a,b in [(0,0), (0,255), (255,255), (255,0)]]
        return [[b,a] for a,b in coords]
    
    def download_image(self, lat, lon, min_year, min_month, max_year, max_month, zoom=14, cloud_max=0.05):
        '''
        Use this method to download an image at a lat, lon in some time range
        If multiple images are available, the latest is downloaded
        
        I would not increase zoom
        cloud_max is the maximum cloud filter, defaulting to 5%
        '''
        assert 0 <= cloud_max <= 1.0
        if min_month < 10:
            min_month = '0' + str(min_month)

        if max_month < 10:
            max_month = '0' + str(max_month)
        
        cords = PlanetDownloader.create_cords(lat, lon, zoom)
        geo_json_geometry = {
          "type": "Polygon",
          "coordinates": [
              cords
          ],

        }

        # filter for items the overlap with our chosen geometry
        geometry_filter = {
          "type": "GeometryFilter",
          "field_name": "geometry",
          "config": geo_json_geometry,
        }

        # filter images acquired in a certain date range
        date_range_filter = {
          "type": "DateRangeFilter",
          "field_name": "acquired",
          "config": {
            "gte": "{}-{}-01T00:00:00.000Z".format(min_year, min_month),
            "lte": "{}-{}-01T00:00:00.000Z".format(max_year, max_month)
          }
        }

        # filter any images which are more than 50% clouds
        cloud_cover_filter = {
          "type": "RangeFilter",
          "field_name": "cloud_cover",
          "config": {
            "lte": cloud_max
          }
        }

        # create a filter that combines our geo and date filters
        # could also use an "OrFilter"
        reservoir = {
          "type": "AndFilter",
          "config": [geometry_filter, date_range_filter, cloud_cover_filter]
        }
        
        # Search API request object
        search_endpoint_request = {
          "item_types": [self.item_type],
          "filter": reservoir
        }

        result = \
          requests.post(
            'https://api.planet.com/data/v1/quick-search',
            auth=HTTPBasicAuth(self.api_key, ''),
            json=search_endpoint_request)
        
        res = json.loads(result.text)
        x, y = deg_to_tile(lat, lon, zoom)
        item_id = None
        

        if len(res['features']) == 0:
            # print('No image found, try widening your search or using a different satellite')
            return None
        else:
            # planet for some reason will return results that don't even contain the requested geometry -_-
            # this will look for the LATEST (closest to the max time) match that actually contains our geometry
            polya = Polygon(cords) 
            b_cords = [tilexy_to_deg(x,y,zoom,a,b) for a,b in [(0,0), (1,0), (1,1), (0,1)]]
            polyb = Polygon([(b,a) for (a,b) in b_cords])

            for idx in range(len(res['features']) - 1, -1, -1):
                polyc = Polygon(res['features'][idx]['geometry']['coordinates'][0])
                
                if polyc.contains(polya) and polyc.contains(polyb):
                    item_id = res['features'][idx]['id']
                    break
        
        if item_id is None:
            # print('No good images found')
            return None
        
        url = 'https://tiles0.planet.com/data/v1/{}/{}/{}/{}/{}.png?api_key={}'.format(self.item_type, item_id, zoom, x, y, self.api_key)
        
        res = requests.get(url)
        if res.status_code >= 400:
            # print('download error')
            return None
        
        return plt.imread(BytesIO(res.content))

def tilexy_to_deg(xtile, ytile, zoom, x, y):
    """Converts a specific location on a tile (x,y) to geocoordinates."""
    decimal_x = xtile + x / 256
    decimal_y = ytile + y / 256
    n = 2.0 ** zoom
    lon_deg = decimal_x / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * decimal_y / n)))
    lat_deg = math.degrees(lat_rad)
    return (lat_deg, lon_deg)

def deg_to_tilexy(lat_deg, lon_deg, zoom):
    """Converts geocoordinates to an x,y position on a tile."""
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    x = ((lon_deg + 180.0) / 360.0 * n)
    y = ((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad)))
        / math.pi) / 2.0 * n)
    return (int((x % 1) * 256), int((y % 1) * 256))

def tile_to_deg(xtile, ytile, zoom):
    """Returns the coordinates of the northwest corner of a Slippy Map
    x,y tile"""
    n = 2.0 ** zoom
    lon_deg = xtile / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
    lat_deg = math.degrees(lat_rad)
    return (lat_deg, lon_deg)

def deg_to_tile(lat_deg, lon_deg, zoom):
    """Converts coordinates into the nearest x,y Slippy Map tile"""
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad)))
                 / math.pi) / 2.0 * n)
    return (xtile, ytile)
