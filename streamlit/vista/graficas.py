import streamlit as st
from datetime import datetime, timedelta
from vista.balance import balance_app as balance_page
from vista.demanda import demanda_app as demanda_page
from vista.generacion import generacion_app as generacion_page
from vista.intercambio import intercambio_app as intercambio_page


def graficas_app():
    #Titulo
    st.title('  Explora datos visualmente  ')

    #Barra lateral
    sidebar_opciones = ['Balance', 'Demanda', 'Generación', 'Intercambio']
    selected_option = st.sidebar.selectbox('Datos a consultar', sidebar_opciones)

    #selección del perido de tiempo
    tiempo_opciones = ['7 días','14 días', '30 días']
    selected_time= st.sidebar.selectbox('Periodo de tiempo', tiempo_opciones)

    #Selección del año
    años = [2024, 2023, 2022]
    selected_year= st.sidebar.selectbox("Periodo de años ", años)


    #Llamar a la función de la página seleccionada

    if selected_option == 'Balance':
        balance_page(selected_time, selected_year)
    elif selected_option == 'Demanda':
        demanda_page(selected_time, selected_year)
    elif selected_option == 'Generación':
        generacion_page(selected_time,selected_year)
    elif selected_option == 'Intercambio':
        intercambio_page(selected_time,selected_year)

if __name__ == "__graficas_app__":
    graficas_app()