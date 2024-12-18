import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta
import pytz
import plotly.express as px
from IPython.display import display

## MAPAS ##
import folium
from streamlit_folium import st_folium
from folium.plugins import AntPath

def get_intercambio_data():
    script_dir = os.path.dirname(__file__)
    data_path = os.path.join(script_dir, '..', '..', 'Notebooks', 'Obtencion datos', 'intercambio_electrico.csv')
    print(f"Data path: {data_path}")
    return pd.read_csv(data_path)

def intercambio_app(selected_time,selected_year):
    st.markdown("<h1 style=' color: skyblue; font-size: 2rem;'>Datos de Intercambio Eléctrico </h1>", unsafe_allow_html=True)

    intercambio_data = get_intercambio_data()

    intercambio_data['Fecha actualización'] = pd.to_datetime(intercambio_data['Fecha actualización'], format='%d/%m/%Y').dt.tz_localize(None)
    
    today = pd.to_datetime(intercambio_data['Fecha actualización'].iloc[-1]).replace(year=selected_year)
    intercambio_data = intercambio_data[intercambio_data['Fecha actualización'].dt.year == selected_year]

    if selected_time == '7 días':
        date_limit = today - timedelta(days=7)
    elif selected_time == '14 días':
        date_limit = today - timedelta(days=14)
    elif selected_time == '30 días':
        date_limit = today - timedelta(days=30)

    date_limit = date_limit.tz_localize(None)

    filtered_data = intercambio_data[(intercambio_data['Fecha actualización'] >= date_limit) & (intercambio_data['Fecha actualización'] <= today)]

    ##IMPUT DEL TIPO DE INFORMACIÓN DESEADA.
    bar_opciones = ['Importación', 'Exportación', 'Saldo']
    selected_option = st.selectbox('Tipo de energía', bar_opciones)


    #Creamos mapa base:
    españa_alt = 40.4637
    españa_lat = -3.7492

    #Creacion del mapa

    

    spain_map = folium.Map(location = [españa_alt, españa_lat],
                       zoom_start= 5,
                       tiles = 'CartoDB Dark_Matter',
                       width='600px',
                       height='600px'
                       )

    bounds =   [[51.1242, -17.0000],[20.0000, 9.6625]]

    spain_map.fit_bounds(bounds)


    #Coordenadas de los paises donde existe un intercambio energetico.
    lista_paises = ['Marruecos', 'Francia', 'Portugal', 'Andorra', 'España']
    lista_altitudes = [31.83999, 46.57771, 39.68023, 42.5462, 40.4637]
    lista_latitudes = [-6.19721, 2.78159, -8.80606, 1.5034, -3.7492]

    df_coordenadas = pd.DataFrame()
    df_coordenadas['nombre'] = lista_paises
    df_coordenadas['altitud'] = lista_altitudes
    df_coordenadas['latitud'] = lista_latitudes


    #Creacion de variables con sus coordenadas
    marruecos = [df_coordenadas['altitud'][0], df_coordenadas['latitud'][0]]
    francia = [df_coordenadas['altitud'][1], df_coordenadas['latitud'][1]]
    portugal = [df_coordenadas['altitud'][2], df_coordenadas['latitud'][2]]
    andorra = [df_coordenadas['altitud'][3], df_coordenadas['latitud'][3]]
    españa = [df_coordenadas['altitud'][4], df_coordenadas['latitud'][4]]


    #Unión de df_coordenadas y df incluido en la función - en nuestro caso, df_intercambio.
    df_unido = pd.merge(filtered_data, df_coordenadas, how = 'left', on = 'nombre')


    #Creación de iconos por país
    españa_url = "https://upload.wikimedia.org/wikipedia/en/9/9a/Flag_of_Spain.svg"
    españa_icon = folium.CustomIcon(españa_url, icon_size=(50, 30))

    marruecos_url = "https://upload.wikimedia.org/wikipedia/commons/2/2c/Flag_of_Morocco.svg"
    marruecos_icon = folium.CustomIcon(marruecos_url, icon_size=(40, 20))

    andorra_url = "https://upload.wikimedia.org/wikipedia/commons/1/19/Flag_of_Andorra.svg"
    andorra_icon = folium.CustomIcon(andorra_url, icon_size=(40, 20))

    francia_url = "https://upload.wikimedia.org/wikipedia/en/c/c3/Flag_of_France.svg"
    francia_icon = folium.CustomIcon(francia_url, icon_size=(40, 20))

    portugal_url = "https://upload.wikimedia.org/wikipedia/commons/5/5c/Flag_of_Portugal.svg"
    portugal_icon = folium.CustomIcon(portugal_url, icon_size=(40, 20))


    ## df_filtrado es el df resultante del tipo de intercambio deseado.
    df_filtrado = df_unido[df_unido['tipo de intercambio'] == selected_option]

    #CREACIÓN DEL MAPA CON INFORMACIÓN
    intercambios = folium.map.FeatureGroup(name='Intercambios')


    for lat, lng, pais, valores, porcentaje, fecha in zip(df_filtrado['altitud'],
                           df_filtrado['latitud'],
                           df_filtrado['nombre'],
                           df_filtrado['Valores'],
                           df_filtrado['Porcentaje'],
                           df_filtrado['Fecha actualización']):

            contenido_label = f'''<b> Pais: {pais} </b><br>
                            <b>Tipo de intercambio: {selected_option} </b><br>
                            <b>Valores: {valores} </b><br>
                            <b>Porcentaje: {porcentaje} </b><br>
                            <b>Fecha actualización: {fecha} </b>'''
            intercambios.add_child(folium.Marker(location=[lat, lng],
                                                 popup=contenido_label))



    spain_map.add_child(intercambios)



    folium.Marker(
          location= españa,
          icon=españa_icon,
          popup = 'España'
          ).add_to(spain_map)

    folium.Marker(
          location= portugal,
          icon=portugal_icon,
          popup = 'Portugal'
          ).add_to(spain_map)
    folium.Marker(
          location= francia,
          icon=francia_icon,
          popup = 'Francia'
          ).add_to(spain_map)
    folium.Marker(
          location= marruecos,
          icon=marruecos_icon,
          popup = 'Marruecos'
          ).add_to(spain_map)
    folium.Marker(
          location= andorra,
          icon=andorra_icon,
          popup = 'Andorra'
          ).add_to(spain_map)


    for i, v in df_filtrado[df_filtrado['nombre'] == 'Francia'].iterrows():
        if v['Valores'] < 0:
                AntPath(locations = [españa, francia],
                color = 'blue',
                delay = 2000,
                weight = 5).add_to(spain_map)
        elif v['Valores'] > 0:
                AntPath(locations = [francia,españa],
                color = 'blue',
                delay = 2000,
                weight = 5).add_to(spain_map)
        else:
                pass

    for i, v in df_filtrado[df_filtrado['nombre'] == 'Andorra'].iterrows():
        if v['Valores'] < 0:
                AntPath(locations = [españa, andorra],
                color = 'orange',
                delay = 2000,
                weight = 5).add_to(spain_map)
        elif v['Valores'] > 0:
                AntPath(locations = [andorra,españa],
                color = 'orange',
                delay = 2000,
                weight = 5).add_to(spain_map)
        else:
                pass

    for i, v in df_filtrado[df_filtrado['nombre'] == 'Marruecos'].iterrows():
        if v['Valores'] < 0:
                AntPath(locations = [españa, marruecos],
                color = 'red',
                delay = 2000,
                weight = 5).add_to(spain_map)
        elif v['Valores'] > 0:
                AntPath(locations = [marruecos, españa],
                color = 'red',
                delay = 2000,
                weight = 5).add_to(spain_map)
        else:
                pass

    for i, v in df_filtrado[df_filtrado['nombre'] == 'Portugal'].iterrows():
        if v['Valores'] < 0:
                AntPath(locations = [españa, portugal],
                color = 'green',
                delay = 2000,
                weight = 5).add_to(spain_map)
        elif v['Valores'] > 0:
                AntPath(locations = [portugal, españa],
                color = 'green',
                delay = 2000,
                weight = 5).add_to(spain_map)
        else:
                pass




    col_1,col_2 = st.columns((1,1))

    with col_1:
        st_folium(spain_map,
                  width  = 800,
                  height = 400)

    with col_2:

        st.markdown(body = """<p style='font-size: 1.2em; text-align: justify; margin: 10px 0;'>En esta sección se muestra el último informe de intercambio energético con nuestros países vecinos.
                    El mapa te ofrece ver los datos de importación y exportación energética de otros países así como el saldo el cual es la diferencia entre la importación y exportación. En el caso de que no hubiera ninguna información,
                    no mostraría ninguna etiqueta tras la bandera de cada país.</p>""", unsafe_allow_html=True)


        st.markdown(body = """<p style='font-size: 1.2em; text-align: justify; margin: 10px 0;'>El intercambio energético también demuestra una linea que va de España hacia afuera, lo cual significa que esta exportando energía o, en cuanto a saldo energético con el país vecino se trata, habla de una deuda energética a pagar.</p>""", unsafe_allow_html=True)



        st.markdown(body = """<p style='font-size: 1.2em; text-align: justify; margin: 10px 0;'>De la misma manera, si la linea va desde el país vecino hacia adentro, significa que esta importando energía o, en cuanto a saldo energético con el país vecino se trata, habla de una deuda energética en el que el país vecino sale deudor con España.</p>""", unsafe_allow_html=True)



    st.markdown("<h1 style=' color: skyblue; font-size: 1.3rem;'>Muestras de gráficas</h1>",
                unsafe_allow_html=True)

    st.markdown(body = """<p style='font-size: 1.2em; text-align: justify; margin: 10px 0;'>A continuación vemos una gráfica lineal en la que se ve el tipo de categoría energética seleccionada dividido por países.
                    Los valores más altos representan valores energéitcos superiores, mientras que los valores más bajos representan valores energéticos inferiores. Algo que
                    se podrá apreciar es que en algunos países los valores saltan dos o tres fechas, o incluso que paran en algúna fecha en concreto,
                    porque no se toma o extrae energía de esos países.""",
                unsafe_allow_html=True)

    st.markdown(body = """<p style='font-size: 1.2em; text-align: justify; margin: 10px 0;'>También ofrecemos una vista de la traza de manera individual por país debajo de la gráfica principal.""",
                unsafe_allow_html=True)


    fig = px.line(df_filtrado, x = 'Fecha actualización', y = 'Valores', color= 'nombre',
              line_group='tipo de intercambio',
              title= 'Evolucion de los valores de intercambio por País y Tipo',
              line_dash='tipo de intercambio',
              markers= True)

    st.plotly_chart(fig,use_container_width= True)

    col_3,col_4 = st.columns((1,1))


    fig_francia = px.line(df_filtrado[df_filtrado['nombre'] == 'Francia'], x = 'Fecha actualización', y = 'Valores', color= 'tipo de intercambio',
              line_group='tipo de intercambio',
              title= 'Evolucion de los valores de intercambio Francia',
              line_dash='tipo de intercambio',
              markers= True)
    col_3.plotly_chart(fig_francia,use_container_width= True)


    fig_portugal = px.line(df_filtrado[df_filtrado['nombre'] == 'Portugal'], x = 'Fecha actualización', y = 'Valores', color= 'tipo de intercambio',
              line_group='tipo de intercambio',
              title= 'Evolucion de los valores de intercambio por Portugal',
              line_dash= 'tipo de intercambio',
              markers= True)
    col_4.plotly_chart(fig_portugal,use_container_width=True)


    fig_marruecos = px.line(df_filtrado[df_filtrado['nombre'] == 'Marruecos'], x = 'Fecha actualización', y = 'Valores', color= 'tipo de intercambio',
              line_group='tipo de intercambio',
              title= 'Evolucion de los valores de intercambio por Marruecos',
              line_dash= 'tipo de intercambio',
              markers= True)
    col_3.plotly_chart(fig_marruecos,use_container_width=True)


    fig_andorra = px.line(df_filtrado[df_filtrado['nombre'] == 'Andorra'],
              x='Fecha actualización', y='Valores', color='tipo de intercambio',
              line_group='tipo de intercambio',
              title='Evolución de los valores de intercambio por Andorra',
              markers=True,
              line_dash='tipo de intercambio')
    col_4.plotly_chart(fig_andorra,use_container_width=True)


    st.markdown(body = """<p style='font-size: 1.2em; text-align: justify; margin: 10px 0;'>En la gráfica de barras podemos ver de una manera simple qué países exportan o importan más o menos energía entre ellos en el tiempo seleccionado.
                Si lo que se quiere ver es el saldo de intercambio internacional (saldo), se podrá ver qué países deben a España cuando están por encíma del valor 0
                y viceversa cuando se trata de una deuda de parte de España.</p>""", unsafe_allow_html=True)


    fig1 = px.bar(df_filtrado, x = 'nombre', y = 'Valores', color = 'tipo de intercambio',
             title= 'Valor del intercambio por País y Tipo',
             labels= {'Valores' : 'Valor de intercambio', 'nombre' : 'nombre'},
             barmode= 'group')

    st.plotly_chart(fig1,use_container_width= True)

    st.markdown(body = """<p style='font-size: 1.2em; text-align: justify; margin: 10px 0;'>Esta gráfica de dispersión (scatterplot) esta gráfica te permitiría visualizar la dinámica entre cómo cambia el valor nominal de un activo
                y la rapidez (o lentitud) con la que varía, representada por el porcentaje de cambio. Esto te puede ayudar a identificar patrones de comportamiento del mercado,
                tendencias futuras o momentos clave de compra/venta energética.""", unsafe_allow_html=True)

    fig2 = px.scatter(df_filtrado, x = 'Valores', y = 'Porcentaje', color = 'nombre',
                 size= 'Porcentaje', hover_name= 'tipo de intercambio',
                 title = 'Relación entre el valor del intercambio y el porcentaje de cambio',
                 size_max= 10)

    st.plotly_chart(fig2,use_container_width= True)




    if __name__ == "__main__":
        intercambio_app(selected_time)
