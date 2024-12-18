import streamlit as st
import pandas as pd
import os
from datetime import timedelta

import plotly.express as px

def get_generacion_data():
    script_dir = os.path.dirname(__file__)
    data_path = os.path.join(script_dir, '..', '..', 'Notebooks', 'Obtencion datos', 'generacion_estructura.csv')
    print(f"Data path: {data_path}")
    return pd.read_csv(data_path)

def generacion_app(selected_time, selected_year):

    st.markdown("<h1 style='color: skyblue; font-size: 2rem;'>Datos de Generación Eléctrica</h1>", unsafe_allow_html=True)

    st.markdown(body="""<p style='font-size: 1.2em; text-align: justify; margin: 10px 0;'>
                        En esta sección se muestra el informe diario de generación eléctrica.
                        </p>""", unsafe_allow_html=True)

    st.markdown(body="""<p style='font-size: 1.2em; text-align: justify; margin: 10px 0;'>
                        Los datos de generación energética diaria registra la cantidad de energía eléctrica que se produce en un momento dado a través de diferentes fuentes
                        o combustibles, sean renovables, no renovables, o demandas en barra central en los sistemas penilsulares
                        y no penilsulares de la red eléctrica española.
                        </p>""", unsafe_allow_html=True)

    st.markdown(body="""<p style='font-size: 1.2em; text-align: justify; margin: 10px 0;'>
                        Estos datos son fundamentales para comprender cómo se suministra la energía eléctrica a la población y a la industria, y para analizar la evolución del sistema energético.
                        </p>""", unsafe_allow_html=True)

    generacion_data = get_generacion_data()

    generacion_data['Fecha actualización'] = pd.to_datetime(generacion_data['Fecha actualización'], format='%d/%m/%Y').dt.tz_localize(None)
    
    today = pd.to_datetime(generacion_data['Fecha actualización'].iloc[-1]).replace(year=selected_year)
    generacion_data = generacion_data[generacion_data['Fecha actualización'].dt.year == selected_year]

    if selected_time == '7 días':
        date_limit = today - timedelta(days=7)
    elif selected_time == '14 días':
        date_limit = today - timedelta(days=14)
    elif selected_time == '30 días':
        date_limit = today - timedelta(days=30)

    #date_limit = date_limit.tz_localize(None)

    filtered_data = generacion_data[(generacion_data['Fecha actualización'] >= date_limit) & (generacion_data['Fecha actualización'] <= today)]

    st.markdown("<h1 style='color: skyblue; font-size: 1rem;'>Muestras de gráficas</h1>", unsafe_allow_html=True)

    st.markdown(body="""<p style='font-size: 1.2em; text-align: justify; margin: 10px 0;'>
                        En esta sección se muestra el informe diario de la generación energética.
                        El gráfico te está mostrando cómo la generación de energía según su tipo de combustible cambia a lo largo del día, con momentos en que se usa más energía (picos) y momentos en que se usa menos (valles).
                        </p>""", unsafe_allow_html=True)

    st.markdown(body="""<p style='font-size: 1.2em; text-align: justify; margin: 10px 0;'>
                        En esta gráfica, podrás encontrar todos los tipos de combustible que es generado incluyendo las trazas totales de cada energía,
                        esto es, generación renovable, generación no renovable, y generación total.
                        </p>""", unsafe_allow_html=True)

    fig = px.line(data_frame=filtered_data, x='Fecha actualización', y='Valores', color='nombre',
                  line_group='tipo de energía',
                  title='Tipo de energía',
                  markers=True)

    for i, trace in enumerate(fig.data):
        if trace.name not in ['Solar fotovoltaica', 'Eólica', 'Turbina de vapor']:
            fig.data[i].visible = 'legendonly'

    st.plotly_chart(fig, use_container_width=True)

    st.markdown(body="""<p style='font-size: 1.2em; text-align: justify; margin: 10px 0;'>
                        A continuación, podemos contemplar tres histogramas divididos por tipos de energías. En estas podemos ver que las energías renovables no suelen llegar a valores altos.
                        Por otro lado, las energías no renovables pueden tener valores similares a excepción de cuando llegamos a los 180k-200k.
                        </p>""", unsafe_allow_html=True)

    fig2 = px.histogram(data_frame=filtered_data,
                         x='Valores',
                         y='Porcentaje',
                         color='tipo de energía',
                         title='Histograma por su tipo de energía',
                         facet_col='tipo de energía',
                         nbins=50)

    st.plotly_chart(fig2, use_container_width=True)

    st.markdown(body="""<p style='font-size: 1.2em; text-align: justify; margin: 10px 0;'>
                        Para finalizar, los valores energéticos, sean que estén divididos por combustible energético como por tipo de energía, en forma de boxplot
                        nos permiten ver la mediana, cuartiles y outliers. Podemos ver en el boxplot dividido por tipo de energía (última gráfica), que los valores percibidos tienen una mediana similar, pero su tercer cuartil y bigote superior son diferentes
                        siendo los valores de generación renovables más que los de no renovables.
                        </p>""", unsafe_allow_html=True)

    fig3 = px.box(data_frame=filtered_data,
                   x='Valores',
                   y='nombre',
                   color='nombre')

    for i, trace in enumerate(fig3.data):
        if trace.name not in ['Solar fotovoltaica', 'Eólica', 'Hidráulica']:
            fig3.data[i].visible = 'legendonly'

    fig3.update_layout(title='Box por tipo de energía')

    st.plotly_chart(fig3, use_container_width=True)

    fig4 = px.box(data_frame=filtered_data,
                   x='Valores',
                   y='tipo de energía',
                   title='Box tipo de energía Renovables, No Renovables y Generación total',
                   color='tipo de energía')

    st.plotly_chart(fig4, use_container_width=True)

if __name__ == "__main__":
    generacion_app()
