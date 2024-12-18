import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from .demanda import demanda_app
from .modelo import get_demanda_data
from datetime import datetime, timedelta
import pickle
from tensorflow.keras.models import load_model
import os
import cv2
from PIL import Image

selected_time = '30 días'
selected_year = 2024

def inicio_app():

    # Columnas para el logo y el título
    col_img, col_tit = st.columns((0.2, 1.6))

    # Título con logo
    #logo = cv2.imread(r"../sources/logo.png")
    #logo = cv2.cvtColor(logo, cv2.COLOR_BGR2RGB)
    #logo = cv2.resize(logo, (200, 200))
    img = Image.open('sources/logo.png')
    #col_img.image('../sources/logo.png')
    col_img.image(img, use_column_width=True)
    col_tit.markdown(
        "<h1 style='margin-top: 15px; color: skyblue; font-size: 3em;'>"
        "Proyecto cuadro de mando de la red eléctrica de España</h1>",
        unsafe_allow_html=True
    )

    # Imagen de banner con espaciado adicional
    st.markdown("<br>", unsafe_allow_html=True)
    img1 = Image.open('sources/Banner_4.png')
    st.image(img1)

    # Columnas para el texto introductorio
    col_1, col_2 = st.columns((1, 0.2))

    col_1.markdown(
        "<h2 style='color: skyblue;'>Funcionalidades de la plataforma</h2>"
        "<p style=' font-size: 1.2em;'>"
        "En esta plataforma interactiva se ofrece un análisis detallado sobre el balance, la demanda, la generación y el intercambio en el mercado energético español, "
        "así como una predicción de la evolución de la demanda energética para los próximos días. Para ello, se ha obtenido información principalmente de la API de REData, "
        "que ofrece un amplio registro de los distintos movimientos que se realizan a diario en dicho mercado. Además, para la parte de la predicción, se ha entrenado un "
        "modelo de aprendizaje automático que permite, con el histórico de datos, conocer aproximadamente cuáles serán los valores de la demanda para los siguientes días.<br><br>"

        "Este es el resultado de nuestro proyecto final del curso de <span style='font-weight: bold; color: skyblue'>Data Science e Inteligencia Artificial</span> "
        "de la escuela <span style='font-weight: bold; color: skyblue'>HACK A BOSS</span>. Aquí se muestra la aplicación de diferentes conceptos y "
        "tareas relacionados con el manejo de datos y los modelos de inteligencia artificial, como la recopilación y limpieza de datos, la creación "
        "de gráficas interactivas o el uso de modelos de aprendizaje automático.<br><br>"

        "Este proyecto refleja nuestro esfuerzo conjunto para generar una herramienta útil e interesante, que además muestre nuestras habilidades "
        "y lo aprendido durante el curso.<br><br>"

        "Fue desarrollado por Diego Díaz Gómez, Luis Miguel Guerrero Albalat, Joaquín Acosta y Víctor Manuel Harillo Parra.<br><br>"

        "Las principales funcionalidades de la plataforma son: <br>"
        "</p>",
        unsafe_allow_html=True
    )

    # Espaciado antes de las pestañas
    st.markdown("<br>", unsafe_allow_html=True)

    # Pestañas de la aplicación
    tabs1, tabs2 = st.tabs(["📈:blue[Gráficas interactivas] 📉", ":blue[Modelo de Machine Learning]🤖 "])

    # Contenido de la primera pestaña
    with tabs1:
        st.header("Gráficas interactivas")
        st.markdown(
            "<p style='font-size: 1.2em;'>"
            "A través de ellas visualizamos los datos relativos al balance, la demanda, la generación y los intercambios de energía en el mercado español. Estas gráficas ayudan a comprender la situación actual del mercado, así como a comparar los diferentes componentes de cada tipo de activo energético.<br><br>"
            "En el subapartado 'intercambio' se incluye un mapa dinámico que permite explorar geográficamente los datos de intercambio de energía entre las principales fronteras de España.<br><br>"
            "Para una exploración más detallada, visite la sección de gráficas interactivas, donde podrá filtrar datos por fecha o tipo de energía, y analizar tendencias y patrones.<br><br>"
            "Aquí tiene un adelanto:"
            "</p>",
            unsafe_allow_html=True
        )
        demanda_app(selected_time, selected_year)

    # Contenido de la segunda pestaña
    with tabs2:
        st.header("Modelo de Machine Learning")
        st.markdown(
             "<p style='font-size: 1.2em;'>"
            "Hemos implementado un modelo de aprendizaje automático que predice el comportamiento futuro de la demanda en el sistema energético español. "
            "En esta pestaña puede visualizar una muestra de los resultados obtenidos con el modelo, y en su sección correspondiente, se muestra su funcionamiento en detalle."
            "</p>",
            unsafe_allow_html=True
        )

        # Preparación y visualización de la predicción
        demanda_data = get_demanda_data()

        script_dir_1 = os.path.dirname(__file__)
        data_path_1 = os.path.join(script_dir_1, '..', '..', 'Notebooks', 'ML', 'modelo_LSTM_msle.keras')
        modelo = load_model(data_path_1)
        
        script_dir_2 = os.path.dirname(__file__)
        data_path_2 = os.path.join(script_dir_2, '..', '..', 'Notebooks', 'ML', 'scaler.pkl')
        with open(data_path_2, 'rb') as file:
            escalador = pickle.load(file)

        primera_fecha = pd.to_datetime(demanda_data['datetime'].iloc[-1], format='%d/%m/%Y')
        ultima_fecha = primera_fecha + timedelta(days=6)
        lista_fechas = pd.date_range(start=primera_fecha, end=ultima_fecha, freq='D')
        lista_fechas = pd.DataFrame(lista_fechas[1:], columns=["fechas"])

        demanda_filtrado = demanda_data[demanda_data['datetime'].dt.year == 2024].reset_index()
        valor_indice = demanda_filtrado[demanda_filtrado['datetime'] == primera_fecha].index[0]

        X = pd.DataFrame(demanda_filtrado["Energia_consumida"][:valor_indice])
        X = escalador.transform(X)

        validation_predictions = []
        last_x = X

        while len(validation_predictions) < 6:
            p = modelo.predict(last_x.reshape(1, -1, 1))[0, 0]
            validation_predictions.append(p)
            last_x = np.roll(last_x, -1)
            last_x[-1] = p

        validation_predictions = pd.DataFrame(escalador.inverse_transform(pd.DataFrame(validation_predictions)), columns=["valores"])

        demanda_grafica = demanda_filtrado.iloc[:valor_indice + 1].iloc[-30:]
        fig_hist = px.line(demanda_grafica, x="datetime", y="Energia_consumida", labels={'datetime': 'Fecha', 'Energia_consumida': 'Valores'})
        fig_hist.add_scatter(x=lista_fechas["fechas"], y=validation_predictions["valores"], name="Predicción", mode="lines")
        fig_hist.update_layout(title="Predicción integrada en el recorrido previo")
        fig_hist.update_traces(connectgaps=True)

        st.plotly_chart(fig_hist, use_container_width=True)

if __name__ == "__inicio_app__":
    inicio_app()
