import streamlit as st
from streamlit_option_menu import option_menu
from pages import home, prediction_map, heatmap_page

def main():
    with st.sidebar:
        selected = option_menu(
            menu_title=None,  
            options=["Home", "Prediction Map", "Heatmaps"],  
            default_index=0
        )

    if selected == "Home":
        home()
    elif selected == "Prediction Map":
        prediction_map()
    elif selected == "Heatmaps":
        heatmap_page()

if __name__ == "__main__":
    main()
