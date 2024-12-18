import streamlit as st
import pandas as pd
import numpy as np
import os
from datetime import timedelta
import plotly.express as px

def get_balance_data():
    script_dir = os.path.dirname(__file__)
    data_path = os.path.join(script_dir, '..', '..', 'Notebooks', 'Obtencion datos', 'balance_electrico.csv')
    print(f"Data path: {data_path}")
    return pd.read_csv(data_path)

def balance_app(selected_time, selected_year):
    st.markdown("<h1 style=' color: skyblue; font-size: 2rem;'>Balance de energía eléctrica</h1>", unsafe_allow_html=True)

    df_bal = get_balance_data()

    st.markdown("<p style='font-size: 1.2em;'>En esta sección se muestra el informe diario de balance.</p>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 1.2em;'>El balance energético diario es el detalle de producción y consumo energético en los sistemas penilsulares y no penilsulares de la red eléctrica española, así como de Ceuta y Melilla.</p>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 1.2em;'>Incluidos en este apartado, encontramos datos y gráficas que nos muestran la estructura necesaria para la cobertura de la demanda energética. Ésta misma se encuentra distribuida en diferentes tipos de energías renovables y no renovables.</p>", unsafe_allow_html=True)

    df_bal['Fecha actualización'] = pd.to_datetime(df_bal['Fecha actualización'])

    today = pd.to_datetime(df_bal['Fecha actualización'].iloc[-1], format='%d/%m/%Y').replace(year=selected_year)
    df_bal = df_bal[df_bal['Fecha actualización'].dt.year == selected_year]

    if selected_time == '7 días':
        date_limit = today - timedelta(days=7)
    elif selected_time == '14 días':
        date_limit = today - timedelta(days=14)
    elif selected_time == '30 días':
        date_limit = today - timedelta(days=30)

    #date_limit = date_limit.tz_localize(None)
    
    filtered_data = df_bal[(df_bal['Fecha actualización'] >= date_limit) & (df_bal['Fecha actualización'] <= today)]

    colores_personalizados = px.colors.qualitative.Plotly + px.colors.qualitative.Pastel + px.colors.qualitative.Set1
    colores_personalizados = colores_personalizados[:30]

    st.markdown("<h1 style=' color: skyblue; font-size: 1.2rem;'>Muestras de gráficas</h1>", unsafe_allow_html=True)

    col_1, col_2 = st.columns((1, 1))

    col_1.markdown("<p style='font-size: 1.2em;'>La gráfica principal ilustra el balance energético, segmentado por tipo de energía, con la producción diaria asignada según el combustible principal utilizado.</p>", unsafe_allow_html=True)
    col_1.markdown("<p style='font-size: 1.2em;'>Para proporcionar una visión más detallada, se han elaborado tres gráficas lineales adicionales que comparan la producción diaria específica de cada tipo de energía, permitiendo así un análisis individualizado. Así mismo, también puedes comparar el trazo del combustible individual comparado con la traza de la generación total (la suma de todos los combustibles por tipo de energía) a la que pertenece.</p>", unsafe_allow_html=True)
    col_1.markdown("<p style='font-size: 1.2em;'>La última representación es un boxplot, que muestra la mediana como la línea central de la caja, indicando el valor central de los datos. Los bordes de la caja reflejan los cuartiles: el límite izquierdo representa el 25% de los valores y el derecho el 75%.</p>", unsafe_allow_html=True)
    col_1.markdown("<p style='font-size: 1.2em;'>Además, los bigotes del boxplot indican los valores más extremos, con los outliers señalando aquellos valores atípicos que se encuentran fuera del rango normal. Este conjunto de visualizaciones permite una comprensión integral y comparativa de la producción energética.</p>", unsafe_allow_html=True)

    # Gráficas
    fig_all = px.line(data_frame=filtered_data,
                      x='Fecha actualización',
                      y='Valores',
                      color='nombre',
                      color_discrete_sequence=colores_personalizados)
    fig_all.update_layout(title='Evolución de energía diaria')

    for i, trace in enumerate(fig_all.data):
        if trace.name not in ['Carbón', 'Hidráulica', 'Consumos en bombeo']:
            fig_all.data[i].visible = 'legendonly'

    col_2.plotly_chart(figure_or_data=fig_all, use_container_width=True)

    fig_reno = px.line(data_frame=filtered_data[filtered_data['tipo de energía'] == 'Renovable'],
                       x='Fecha actualización',
                       y='Valores',
                       color='nombre',
                       color_discrete_sequence=colores_personalizados)
    fig_reno.update_layout(title='Evolución de energía diaria renovable')

    for i, trace in enumerate(fig_reno.data):
        if trace.name in ['Generación renovable']:
            fig_reno.data[i].visible = 'legendonly'

    col_1.plotly_chart(figure_or_data=fig_reno, use_container_width=True)

    fig_no_reno = px.line(data_frame=filtered_data[filtered_data['tipo de energía'] == 'No-Renovable'],
                           x='Fecha actualización',
                           y='Valores',
                           color='nombre',
                           color_discrete_sequence=colores_personalizados)
    fig_no_reno.update_layout(title='Evolución de energía diaria no renovable')

    for i, trace in enumerate(fig_no_reno.data):
        if trace.name in ['Generación no renovable']:
            fig_no_reno.data[i].visible = 'legendonly'

    col_2.plotly_chart(figure_or_data=fig_no_reno, use_container_width=True)

    fig_dbc = px.line(data_frame=filtered_data[filtered_data['tipo de energía'] == 'Demanda en b.c.'],
                       x='Fecha actualización',
                       y='Valores',
                       color='nombre',
                       color_discrete_sequence=colores_personalizados)
    fig_dbc.update_layout(title='Evolución de energía diaria de demanda en barra central')

    for i, trace in enumerate(fig_dbc.data):
        if trace.name in ['Demanda en b.c.']:
            fig_dbc.data[i].visible = 'legendonly'

    col_1.plotly_chart(figure_or_data=fig_dbc, use_container_width=True)

    fig_box2 = px.box(data_frame=filtered_data,
                      x='Valores',
                      y='tipo de energía',
                      color='tipo de energía',
                      color_discrete_sequence=colores_personalizados)
    fig_box2.update_layout(title='Boxplot con outliers')
    col_2.plotly_chart(figure_or_data=fig_box2, use_container_width=True)

if __name__ == "__main__":
    balance_app()
