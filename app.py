import streamlit as st
from streamlit_option_menu import option_menu
from pages import home, prediction_map, heatmap_page, barchart

api_key = st.secrets['api_key']

# st.write(api_key)

def main():
    with st.sidebar:
        selected = option_menu(
            menu_title=None,  
            options=["Home", "Prediction Map", "Heatmaps"],
            # options=["Home", "Prediction Map", "Heatmaps", "3D Bar Charts"],  
            default_index=0
        )

    if selected == "Home":
        home()
    elif selected == "Prediction Map":
        prediction_map(api_key)
    elif selected == "Heatmaps":
        heatmap_page()
    # elif selected == "3D Bar Charts":
    #     barchart()

if __name__ == "__main__":
    main()
