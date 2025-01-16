import streamlit as st
from streamlit_option_menu import option_menu
from views.seasonality import run as seasonality_run
from views.dashboard_euro import run as dashboard_euro_run
from views.dashboard_gbp import run as dashboard_gbp_run
from views.dashboard_usd import run as dashboard_usd_run

# --- PAGE SETUP ---
pages = {
    "Main page": seasonality_run,
    "Euro": dashboard_euro_run,
    "Pound": dashboard_gbp_run,
    "Dollar": dashboard_usd_run,
}

with st.sidebar:
    st.title("Main")
    page_selection = option_menu(
        menu_title=None,  
        options=list(pages.keys()),
        icons=["Home","currency-euro","currency-pound","currency-dollar"], 
        menu_icon="cast", 
        default_index=0, 
        styles={
            "container": {"padding": "5px", "background-color": "#f0f2f6"},
            "icon": {"color": "black", "font-size": "18px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "0px",
                "color": "black",
            },  
            "nav-link-selected": {"background-color": "#007bff", "color": "white"}, 
        },
    )

# --- RUN SELECTED PAGE ---
pages[page_selection]()

