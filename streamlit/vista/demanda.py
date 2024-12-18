import streamlit as st
import pandas as pd
import os
from datetime import timedelta

import plotly.express as px

def get_demanda_data():
    script_dir = os.path.dirname(__file__)
    data_path = os.path.join(script_dir, '..', '..', 'Notebooks', 'Obtencion datos', 'demanda_evolucion.csv')
    print(f"Data path: {data_path}")
    return pd.read_csv(data_path)

def demanda_app(selected_time, selected_year):
    st.markdown("<h1 style='color: skyblue; font-size: 2rem;'>Datos de la demanda eléctrica a nivel nacional</h1>", unsafe_allow_html=True)

    demanda_data = get_demanda_data()

    demanda_data['Fecha actualización'] = pd.to_datetime(demanda_data['Fecha actualización'], format='%d/%m/%Y').dt.tz_localize(None)
    
    today = pd.to_datetime(demanda_data['Fecha actualización'].iloc[-1]).replace(year=selected_year)
    demanda_data = demanda_data[demanda_data['Fecha actualización'].dt.year == selected_year]

    if selected_time == '7 días':
        fecha_limite = today - timedelta(days=7)
    elif selected_time == '14 días':
        fecha_limite = today - timedelta(days=14)
    elif selected_time == '30 días':
        fecha_limite = today - timedelta(days=30)

    

    #fecha_limite = fecha_limite.tz_localize(None)

    filtered_data = demanda_data[(demanda_data['Fecha actualización'] >= fecha_limite) & (demanda_data['Fecha actualización'] <= today)]

    st.markdown("<h1 style='color: skyblue; font-size: 1.3rem;'>Muestras de gráficas</h1>", unsafe_allow_html=True)

    st.markdown(
        body="""<p style='font-size: 1.2em; margin: 10px 0;'>
                La demanda energética hace referencia a la cantidad de energía que se requiere para satisfacer las necesidades de una población, de un sector económico o de una región en particular. Este concepto es clave en la planificación y gestión de los recursos energéticos, ya que ayuda a prever y satisfacer la demanda según las características de consumo de cada área. En nuestro país, esta energía puede proceder de diversas fuentes, como fuentes renovables y no renovables, que juntas contribuyen a la generación de la energía necesaria para el funcionamiento de la sociedad.
                 </p>"""
                 """<p style='font-size: 1.2em; margin: 10px 0;'>
                En el gráfico, se observa cómo la demanda energética varía a lo largo de los días seleccionados en la barra lateral, lo que permite identificar patrones de consumo en días específicos. Estos cambios se reflejan en momentos de alta demanda, conocidos como "picos", que suelen coincidir con horas de gran actividad, y en momentos de baja demanda, denominados "valles", que suelen ocurrir en horarios nocturnos o durante periodos de menor actividad. Este análisis de picos y valles es fundamental para la administración eficiente de la energía y la optimización de los recursos energéticos en nuestro país.
               </p>""",
        unsafe_allow_html=True
    )

    fig_demanda = px.line(data_frame=filtered_data,
                           x='Fecha actualización',
                           y='Energia_consumida',
                           title='Evolución de demanda energética diaría',
                           markers=True)

    st.plotly_chart(fig_demanda, use_container_width=True)

if __name__ == "__main__":
    demanda_app()
