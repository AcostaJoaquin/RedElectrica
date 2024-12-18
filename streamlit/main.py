import streamlit as st

from vista.informacion import informacion_app
from vista.home import inicio_app
from vista.graficas import graficas_app
from vista.modelo import modelo
from datetime import datetime, timedelta

st.set_page_config(layout="wide")

page_gb_img = """
<style>
[data-testid="stSidebar"] {
background-image: url("https://cdn.prod.website-files.com/5ff3273633e29c2a7c8b6c80/62162087f33cd1ae31e1b121_blog_REE%20(1)%20(1)%20(1)%20(2).png");
background-size: cover;
}

[data-testid="stAppViewBlockContainer"] {
background-color: #111111;
}

[data-testid="stHeader"] {
background-color: #202020;
}

</style>


"""
st.markdown(page_gb_img, unsafe_allow_html=True)

def main():
   
    menu = [
    [' Inicio','🔎'],
    [' Gráficas Interactivas', '📊'],
    [' Modelo de Machine Learning', '🤖'],
    [' Información', '📘']
    ]
    menu_options = [item[0] for item in menu]
    # Mostrar nombre y icono con estilo
    selected_option = st.sidebar.selectbox(
        '🏡  MENU',
        menu_options,
        format_func=lambda x: f"{(menu[menu_options.index(x)][1])}{x}",
    )

    # Llamar a la función de la página seleccionada
    if selected_option == ' Inicio':
        inicio_app()
    elif selected_option == ' Gráficas Interactivas':
        graficas_app()
    elif selected_option == ' Modelo de Machine Learning':
        modelo()
    elif selected_option == ' Información':
        informacion_app()


if __name__ == "__main__":
    main()
