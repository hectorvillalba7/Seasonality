import streamlit as st
from streamlit_option_menu import option_menu
from views.seasonality import run as seasonality_run
#from views.dashboard_euro import run as dashboard_euro_run
from views.dashboard_euro import run as dashboard_euro_run
from views.dashboard_gbp import run as dashboard_gbp_run
from views.dashboard_usd import run as dashboard_usd_run

# --- PAGE SETUP ---
pages = {
    "Inicio": seasonality_run,
    "Euro": dashboard_euro_run,
    "Libra": dashboard_gbp_run,
    "Dólar": dashboard_usd_run,
}

with st.sidebar:
    st.title("Navegación")
    page_selection = option_menu(
        menu_title=None,  # No se muestra un título adicional
        options=list(pages.keys()),
        icons=["Home","currency-euro","currency-pound","currency-dollar"],  # iconos paginas
        menu_icon="cast",  # Ícono del menú
        default_index=0,  # Índice por defecto
        styles={
            "container": {"padding": "5px", "background-color": "#f0f2f6"},  # Fondo del menú
            "icon": {"color": "black", "font-size": "18px"},  # Color y tamaño de los íconos
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "0px",
                "color": "black",
            },  # Estilo de los enlaces
            "nav-link-selected": {"background-color": "#007bff", "color": "white"},  # Página seleccionada
        },
    )

#st.logo("assets/logo.png")
# --- RUN SELECTED PAGE ---
pages[page_selection]()

