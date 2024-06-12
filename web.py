import streamlit as st
from streamlit_option_menu import option_menu
import time
import numpy as np
import pandas as pd
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
import requests
import pydeck as pdk

# Function for the Home page
def home():
    st.title("Home")
    st.write("Welcome to the Home page!")

# Function for the About page
def about():

    # Define the data
    data = {
        'cluster_lat': [8.954261, 9.034180, 9.015257, 8.964058, 9.052935, 9.020116, 8.989751, 9.013835, 9.047567, 9.071813, 8.958031, 9.018709, 9.061072, 9.037509, 9.023574, 8.957485],
        'cluster_lon': [38.776901, 38.842568, 38.813750, 38.721902, 38.735117, 38.733379, 38.773653, 38.741334, 38.718242, 38.729929, 38.748086, 38.789997, 38.791779, 38.737811, 38.784249, 38.762128],
        'cons_pc': [30.038594, 23.621166, 20.499866, 20.488550, 18.578238, 18.206968, 17.768381, 14.816839, 14.566923, 13.792394, 12.825229, 12.782309, 12.539863, 11.936232, 11.709447, 10.622940],
        'Economic Position': [
            "Bole is one of the most affluent districts in ...",
            "Economically active with businesses contributi...",
            "Benefits economically from the presence of the...",
            "More affordable area attracting lower to middl...",
            "Economically vibrant with numerous commercial ...",
            "Economically vibrant with businesses and possi...",
            "Economically diverse with both affluent areas ...",
            "Bustling area with a strong economic presence ...",
            "Moderate economic activity with local business...",
            "Developing economy with growing infrastructure...",
            "Growing area with increasing commercial activi...",
            "Moderate economic status with local businesses...",
            "Developing economy with growing infrastructure...",
            "Varied economic status with both affluent and ...",
            "Developing area with growing residential and c...",
            "This area has a developing economy with ongoin..."
        ],
        'Demographics': [
            "Bole is highly populated with a mix of locals ...",
            "Mixed-use area with residential and commercial...",
            "Centered around the International Livestock Re...",
            "Primarily a residential neighborhood with a hi...",
            "Large district with diverse communities, inclu...",
            "Likely to be in a well-regarded area, named af...",
            "An older part of Addis Ababa with a mixed demo...",
            "Known for its commercial establishments and di...",
            "Likely in a mixed residential and commercial a...",
            "Diverse district with various residential and ...",
            "Diverse with a mix of income levels but predom...",
            "Residential area with a mixture of housing typ...",
            "Similar to other areas in Gulele, a mix of low...",
            "Located in Kirkos Sub City with a mix of demog...",
            "Suburban area with a mix of lower and middle-i...",
            "A residential area with a mix of middle and lo..."
        ],
        'area_name': [
            "Bole", "Burkina Faso St", "ILRI campus", "Jomo", "Yeka", "Kenenisa Avenue", "Kirkos",
            "Liberia Street", "Sheh Ojele Street", "Gulele", "Nefassik Lafto", "Geja Sefer", "Guele",
            "Riche Kirkos subcity", "Kotebe", "Nefas Silk Fafto"
        ]
    }

    # Create a DataFrame
    df = pd.DataFrame(data)

    # Function to handle map click events
    def handle_click(map_data):
        if map_data:
            clicked = map_data[0]
            lon, lat = clicked['coordinates']
            place_info = df[(df['cluster_lat'] == lat) & (df['cluster_lon'] == lon)]
            if not place_info.empty:
                info = place_info.iloc[0]
                st.session_state['clicked_info'] = {
                    'area_name': info['area_name'],
                    'Economic Position': info['Economic Position'],
                    'Demographics': info['Demographics']
                }

    # Initial view state of the map
    view_state = pdk.ViewState(
        latitude=8.990161,
        longitude=38.754737,
        zoom=9,
        pitch=50
    )

    # Define the HexagonLayer
    hex_layer = pdk.Layer(
        'HexagonLayer',
        data=df,
        get_position='[cluster_lon, cluster_lat]', 
        radius=300,
        elevation_scale=10000,
        elevation_range=[0, 50000],
        pickable=True,
        extruded=True,
        get_elevation='cons_pc',
        auto_highlight=True
    )

    # Define the ScatterplotLayer
    scatter_layer = pdk.Layer(
        'ScatterplotLayer',
        data=df,
        get_position='[cluster_lon, cluster_lat]',
        get_color='[200, 30, 0, 160]',
        get_radius=100
    )

    # Define the Deck
    deck = pdk.Deck(
        map_style=None,
        initial_view_state=view_state,
        layers=[hex_layer, scatter_layer],
        tooltip={"text": "{area_name}"}
    )

    # Render the map
    st.pydeck_chart(deck)

    # Handle the click event
    map_click_data = st.session_state.get('pydeck_map_click')
    if map_click_data:
        handle_click(map_click_data)

    # Display clicked info
    if 'clicked_info' in st.session_state:
        info = st.session_state['clicked_info']
        st.write(f"### {info['area_name']}")
        st.write(f"**Economic Position:** {info['Economic Position']}")
        st.write(f"**Demographics:** {info['Demographics']}")



# Function for the Contact page
def prediction_map():
    # Dummy function to represent a machine learning prediction
    

    # write requests
    # define day of week and time



    # Function to get place name from coordinates
    def get_place_name(lat, lon):
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.reverse((lat, lon), exactly_one=True)
        return location.address if location else "Unknown location"

    # Set up the Streamlit app
    st.title("Prediction by Location")
    st.write("Click anywhere (read: Nigeria or Ethiopia) on the world map to choose desired location to generate your ✨ bespoke ✨ prediction:")

    # Create a map centered around a specific location
    latitude, longitude = 9.050654, 38.25645  # Example coordinates
    map_center = [latitude, longitude]
    m = folium.Map(location=map_center, zoom_start=3)

    # Add some example points to the map
    # points = [
    #     {"location": [37.7749, -122.4194], "popup": "Point 1", "icon": "cloud"},
    #     {"location": [37.7849, -122.4094], "popup": "Point 2", "icon": "info-sign"},
    #     {"location": [37.7649, -122.4294], "popup": "Point 3", "icon": "ok-sign"},
    # ]

    # Function to add markers to the map
    # def add_marker(map_obj, point):
    #     folium.Marker(
    #         location=point["location"],
    #         popup=point["popup"],
    #         icon=folium.Icon(icon=point["icon"], color="blue")
    #     ).add_to(map_obj)

    # Add markers to the map
    # for point in points:
    #     add_marker(m, point)

    # Add a click handler to the map to get coordinates
    m.add_child(folium.LatLngPopup())

    # Display the map in the Streamlit app and capture click events
    map_data = st_folium(m, width=700, height=500)

    # Check if a point was clicked and get the coordinates
    if map_data['last_clicked']:
        clicked_location = map_data['last_clicked']['lat'], map_data['last_clicked']['lng']
        # Format the coordinates to 6 decimal places
        formatted_lat = f"{clicked_location[0]:.6f}"
        formatted_lng = f"{clicked_location[1]:.6f}"
        place_name = get_place_name(formatted_lat, formatted_lng)
        loc = f"Latitude: {formatted_lat}, Longitude: {formatted_lng}"
        # st.write(f"Location: Latitude {formatted_lat}, Longitude: {formatted_lng}")
        place_name2 = f"Place: {place_name}"
        # st.write(f"Place: {place_name}") 
        
        def make_prediction(location):
        # In a real scenario, replace this with the actual model prediction
        # For example: return model.predict([location])
            return np.random.choice(["Class A", "Class B", "Class C"])
        # Make prediction based on the clicked location
        prediction = make_prediction(clicked_location)
        pred = f"## {prediction}"
        # st.write(f"Prediction: {prediction}")
        
        response = requests.get(url, params=params)
        response.json() #=> {wait: 64}
        params = {'lat': formatted_lat, 'lon': formatted_lng}
    
        def stream_data_loc():
            for char in loc:
                yield char
                time.sleep(0.04)
        
        def stream_data_pn(): 
            for word1 in place_name2.split(" "):
                yield word1 + " "
                time.sleep(0.04)
                
        def stream_data_pred():        
            for char2 in pred:
                yield char2
                time.sleep(0.15)
        
        # def write_stream_with_font_size(data, size='16px'):
        #     st.markdown(f'<p style="font-size:{size};">{data}</p>', unsafe_allow_html=True)
        
        # Custom CSS for button hover effect
        button_css = """
        <style>
        div.stButton > button {
            border-color: initial;
            color: initial;
            transition: border-color 0.2s, color 0.2s;
        }

        div.stButton > button:hover,
        div.stButton > button:focus,
        div.stButton > button:active,
        div.stButton > button:visited {
            border-color: #008753 !important;  /* Change the border color on hover, focus, active, and visited */
            color: #008753 !important;  /* Change the text color on hover, focus, active, and visited */
            background-color: transparent !important;  /* Ensure background remains transparent */
        }
        </style>
        """
        
        st.markdown(button_css, unsafe_allow_html=True)
        
        # spinner_css = """
        # <style>
        # div[role="progressbar"] {
        #     border-top-color: #008753 !important;  /* Change the moving segment color */
        #     border-right-color: #008753 !important;  /* Ensure consistency if other parts are visible */
        # }
        # </style>
        # """

        # st.markdown(spinner_css, unsafe_allow_html=True)
        
        st.write("## Generate your prediction:")
        if st.button("Example Prediction"):
            st.write("### Location:")
            time.sleep(0.3)
            st.write_stream(stream_data_loc)   
            # st.write_stream(stream_data_pn)
            
            st.write("### Prediction:")
            with st.spinner("## Take out below before demo day"):
                time.sleep(4)
            with st.spinner("Creating artificial impression of complex, sophisticated code..."):
                time.sleep(6)
            with st.spinner("... and building suspense..."):
                time.sleep(4)
            with st.spinner("... but mostly the first thing."):
                time.sleep(4)
            # with st.spinner("OK done"):
            #     time.sleep(2)
            # write_stream_with_font_size(stream_data_pred, size='24px')
            st.write_stream(stream_data_pred)
        
        if st.button("Make Prediction"):
            st.write("### Location:")
            time.sleep(0.3)
            st.write_stream(stream_data_loc)   
            st.write_stream(stream_data_pn)
            
            st.write("### Prediction:")
            with st.spinner("Calculating..."):
                time.sleep(1)
            # write_stream_with_font_size(stream_data_pred, size='24px')
            st.write_stream(stream_data_pred)

# Main function to render the app
def main():
    with st.sidebar:
        selected = option_menu(
            menu_title=None,  # required
            options=["Home", "About", "Prediction Map"],  # required
            #icons=["house", "info", "envelope"],  # optional
            menu_icon=None,  # optional
            default_index=0,  # optional
            styles={
            "container": {"padding": "0!important", "background-color": "#fafafa"},
            "icon": {"color": "#FCDD09", "font-size": "16px"}, 
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "rgba(252, 221, 9, 0.5)"},
            "nav-link-selected": {"background-color": "#008753"},
            }
        )

    if selected == "Home":
        home()
    elif selected == "About":
        about()
    elif selected == "Prediction Map":
        prediction_map()

if __name__ == "__main__":
    main()

# #TRYING TO SET CUSTOM FONT WITH CSS
# with open( "style.css" ) as css: 
#     st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html= True)

# # # Main title
# # st.title("Whereas disregard" )

# # # Option menu in the sidebar
# # with st.sidebar:
# #     # 3. CSS style definitions
# #     selected3 = option_menu(None, ["Home", "Machine Learning",  "Predictor Map", 'Settings'], 
# #     icons=['house', 'cloud-upload', "list-task", 'gear'], 
# #     menu_icon="cast", default_index=0, orientation="horizontal",
# #     styles={
# #         "container": {"padding": "0!important", "background-color": "#fafafa"},
# #         "icon": {"color": "orange", "font-size": "25px"}, 
# #         "nav-link": {"font-size": "25px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
# #         "nav-link-selected": {"background-color": "green"},
# #             }
# # )
    
# # # TYPEWRITER EFFECT
# # _LOREM_IPSUM = """
# # Lorem ipsum dolor sit amet, **consectetur adipiscing** elit, sed do eiusmod tempor
# # incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis
# # nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
# # """

# # def stream_data():
# #     for word in _LOREM_IPSUM.split(" "):
# #         yield word + " "
# #         time.sleep(0.02)

# #     yield pd.DataFrame(
# #         np.random.randn(5, 10),
# #         columns=["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"],
# #     )

# #     for word in _LOREM_IPSUM.split(" "):
# #         yield word + " "
# #         time.sleep(0.02)


# # if st.button("Stream data"):
# #     st.write_stream(stream_data)

# # # MAGIC COMMANDS    
# # # Draw a title and some text to the app:
# # '''
# # # This is the document title

# # This is some _markdown_. #italicise
# # '''

# # import pandas as pd
# # df = pd.DataFrame({'col1': [1,2,3]})
# # df  # 👈 Draw the dataframe

# # x = 10
# # 'x', x  # 👈 Draw the string 'x' and then the value of x

# # # Also works with most supported chart types
# # import matplotlib.pyplot as plt

# # arr = np.random.normal(1, 1,  size=100)
# # fig, ax = plt.subplots()
# # ax.hist(arr, bins=20)

# # fig  # 👈 Draw a Matplotlib chart

# Dummy function to represent a machine learning prediction
# def make_prediction(location):
#     # In a real scenario, replace this with the actual model prediction
#     # For example: return model.predict([location])
#     return np.random.choice(["Class A", "Class B", "Class C"])

# # Function to get place name from coordinates
# def get_place_name(lat, lon):
#     geolocator = Nominatim(user_agent="geoapiExercises")
#     location = geolocator.reverse((lat, lon), exactly_one=True)
#     return location.address if location else "Unknown location"

# # Set up the Streamlit app
# st.title("Interactive Map with Predictions")

# # Create a map centered around a specific location
# latitude, longitude = 9.050654, 38.25645  # Example coordinates
# map_center = [latitude, longitude]
# m = folium.Map(location=map_center, zoom_start=3)

# # Add some example points to the map
# # points = [
# #     {"location": [37.7749, -122.4194], "popup": "Point 1", "icon": "cloud"},
# #     {"location": [37.7849, -122.4094], "popup": "Point 2", "icon": "info-sign"},
# #     {"location": [37.7649, -122.4294], "popup": "Point 3", "icon": "ok-sign"},
# # ]

# # Function to add markers to the map
# def add_marker(map_obj, point):
#     folium.Marker(
#         location=point["location"],
#         popup=point["popup"],
#         icon=folium.Icon(icon=point["icon"], color="blue")
#     ).add_to(map_obj)

# # Add markers to the map
# # for point in points:
# #     add_marker(m, point)

# # Add a click handler to the map to get coordinates
# m.add_child(folium.LatLngPopup())

# # Display the map in the Streamlit app and capture click events
# map_data = st_folium(m, width=700, height=500)

# # Check if a point was clicked and get the coordinates
# if map_data['last_clicked']:
#     clicked_location = map_data['last_clicked']['lat'], map_data['last_clicked']['lng']
#     # Format the coordinates to 6 decimal places
#     formatted_lat = f"{clicked_location[0]:.6f}"
#     formatted_lng = f"{clicked_location[1]:.6f}"
#     place_name = get_place_name(formatted_lat, formatted_lng)
#     st.write(f"Location: Latitude {formatted_lat}, Longitude: {formatted_lng}")
#     st.write(f"Place: {place_name}") 
    
#     # Make prediction based on the clicked location
#     prediction = make_prediction(clicked_location)
#     st.write(f"Prediction: {prediction}")
