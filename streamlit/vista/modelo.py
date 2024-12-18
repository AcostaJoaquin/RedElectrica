import streamlit as st
import numpy as np
import pandas as pd

import plotly.express as px
from datetime import datetime, date, timedelta

import pickle
import tensorflow as tf
from tensorflow.keras.models import load_model
import os

from PIL import Image


def get_demanda_data():
    script_dir = os.path.dirname(__file__)
    data_path = os.path.join(script_dir, '..', '..', 'Notebooks', 'Obtencion datos', 'demanda_evolucion.csv')
    
    demanda_data = pd.read_csv(data_path)

    if 'Fecha actualización' in demanda_data.columns:
        demanda_data['datetime'] = pd.to_datetime(demanda_data['Fecha actualización'], format='%d/%m/%Y')
    else:
        st.error("La columna 'Fecha actualización' no se encontró en el CSV.")
        return pd.DataFrame()

    return demanda_data


def modelo():
    
    demanda_data = get_demanda_data()

    script_dir_1 = os.path.dirname(__file__)
    data_path_1 = os.path.join(script_dir_1, '..', '..', 'Notebooks', 'ML', 'modelo_LSTM_msle.keras')
    modelo = load_model(data_path_1)
    
    script_dir_2 = os.path.dirname(__file__)
    data_path_2 = os.path.join(script_dir_2, '..', '..', 'Notebooks', 'ML', 'scaler.pkl')
    with open(data_path_2, 'rb') as file:
        escalador = pickle.load(file)


    st.markdown("<h1 style=' color: skyblue; font-size: 3rem;'>Modelo de Machine Learning </h1>", unsafe_allow_html=True)

    st.markdown(body = """<p style='font-size: 1.2em; text-align: justify; margin: 10px 0;'>En este apartado explicaremos las decisiones tomadas para construir nuestro modelo de
                          Machine Learning y veremos las predicciones realizadas por este.""", unsafe_allow_html=True)
    
    st.markdown(body = """<p style='font-size: 1.2em; text-align: justify; margin: 10px 0;'>Vistas las operaciones que componen el flujo principal de actividades de la red eléctrica 
                          española, la que suscita mayor interés a la hora de intentar predecir su evolución es la 
                          demanda, ya que indica cuanta electricidad se consume o se va a consumir en nuestro país.""", unsafe_allow_html=True)
    
    st.markdown(body = """<p style='font-size: 1.2em; text-align: justify; margin: 10px 0;'>Es por ello que hemos desarrollado una herramienta que ofrece una aproximación a la que
                          será la demanda energética de los próximos días. Dicha herramienta se basa en un modelo
                          de Machine learning (cuyos detalles se especifican más adelante) entrenado con datos
                          extraidos de la API REData, que permite extraer datos en bruto de los movimientos de 
                          la red eléctrica española. [Para ver más en detalle la API.](https://www.ree.es/es/apidatos)""",
                          unsafe_allow_html=True)


    st.markdown(body = """<p style='font-size: 1.2em; text-align: justify; margin: 10px 0;'>A continuación puedes conocer en mayor profundidad el modelo 
                          o utilizarlo para predecir la evolución de la demanda eléctrica.""", unsafe_allow_html=True)

    tabs1, tabs2 = st.tabs(["📘:blue[Explicación técnica del modelo]", "⚡:blue[Evolución de la demanda eléctrica]"])
    with tabs1:
        
        st.markdown("<h1 style=' color: skyblue; font-size: 2rem;'>Explicación técnica del modelo </h1>", unsafe_allow_html=True)

        st.markdown("<h1 style='text-align: left; color: skyblue; font-size: 1rem;'>Obtención de datos y preparación de los mismos para su uso en el modelo </h1>", unsafe_allow_html=True)

        st.markdown(body = """<p style='font-size: 1.2em; text-align: justify; margin: 10px 0;'>Los datos utilizados para entrenar el modelo han sido extraídos, 
                           como ya se ha mencionado, de la API de REData. En concreto, como las predicciones del
                           modelo debían centrarse en la demanda eléctrica a futuro, se reaprovechó el código
                           utilizado para obtener el histórico de la demanda hasta el momento, utilizando los 
                           mismos datos que aquellos empleados para mostrar este.""", unsafe_allow_html=True)
        
        st.markdown(body = """<p style='font-size: 1.2em; text-align: justify; margin: 10px 0;'>Una vez obtenidos los datos, se revisó la posible existencia de NaN's y/o outliers.
                           Al no haber ninguno, no hubo necesidad de hacer más limpieza de datos.""", unsafe_allow_html=True)

        st.markdown(body = """<p style='font-size: 1.2em; text-align: justify; margin: 10px 0;'>Para el preprocesado, se eliminó la columna de las fechas, dejando solo la de los valores,
                            que es la que nos interesa de cara al entrenamiento del modelo. Para evitar el data leakage,
                            antes de crear las ventanas de tamaño T, se dividió el total de datos en conjuntos de train y 
                            test, dejando en el conjunto de test los datos únicamente del último mes y en el de train
                            el resto del histórico. Tras esto, se escalaron los datos de ambos conjuntos y se organizaron 
                            en ventanas de tamaño T=10 para darles el formato más adecuado de cara al entrenamiento
                            del modelo.""", unsafe_allow_html=True)

        st.markdown("<h1 style='text-align: left; color: skyblue; font-size: 1rem;'>Creación del modelo </h1>", unsafe_allow_html=True)

        st.markdown(body = """<p style='font-size: 1.2em; text-align: justify; margin: 10px 0;'>Tras la realización de múltiples pruebas, en las que se cambiaron la capa
                            recurrente, el tipo de pérdida y el learning rate, finalmente la arquitectura que vimos
                            que daba mejores resultados fue la siguiente:""", unsafe_allow_html=True)
        
        code = '''  model = Sequential()

            model.add(Input(shape = (T, 1)))

            model.add(LSTM(units = 200, activation = "relu"))

            model.add(Dense(units = 64, activation = "relu")) 
            model.add(Dense(units = 32, activation = "relu")) 
            model.add(Dense(units = 16, activation = "relu")) 
            model.add(Dense(units = 1))

            model.compile(optimizer = "adam", loss = "msle")'''

        st.code(code, language='python')

        st.markdown(body = """<p style='font-size: 1.2em; text-align: justify; margin: 10px 0;'>Como se puede observar, la capa recurrente es una LSTM, ya que al tratarse 
                           de un modelo de series temporales, es importante que el modelo sea capaz de recordar 
                           a largo plazo; el tipo de activación es relu, ya que no va a haber en principio valores negativos;
                           el optimizador es adam, ya que queríamos probar con él diferentes learning rates, pero 
                           finalmente vimos que el que mejor funcionaba era el que viene por defecto, por eso no viene especificado; 
                           por último, la pérdida que utilizamos fue msle.""", unsafe_allow_html=True)


        st.markdown(body = """<p style='font-size: 1.2em; text-align: justify; margin: 10px 0;'>Una vez escogida la arquitectura a utilizar se entrenó al modelo utilizando para ello 100 épocas, 
                           dando como resultado la siguiente pérdida:""", unsafe_allow_html=True)
        st.markdown(body = """ """)

        #st.image("../sources/perdida_modelo.png", width=450)
        img = Image.open('sources/perdida_modelo.png')
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(img, width=500)


        st.markdown(body = """ """)
        st.markdown(body = """<p style='font-size: 1.2em; text-align: justify; margin: 10px 0;'>Viendo que los resultados obtenidos eran satisfactorios, se hizo el 1-step y el 
                            multiple step como comprobación de un caso de aplicación del modelo. Tras esto, 
                            considerando al modelo lo suficientemente bueno, se exportó para su uso en la web. """, unsafe_allow_html=True)
        st.markdown(body = """ """)

        col_1,col_2 = st.columns((1,1))

        col_1.markdown(body = """**Predicciones 1-step**""")
        
        img1 = Image.open("sources/1-step_modelo.png")
        col_1.image(img1, width=400)

        col_2.markdown(body = """**Predicciones multiple step**""")
        
        img2 = Image.open("sources/multiple_step_modelo.png")
        col_2.image(img2, width=400)


    with tabs2:
        st.markdown("<h1 style=' color: skyblue; font-size: 2rem;'>Evolución de la demanda eléctrica </h1>", unsafe_allow_html=True)

        st.markdown(body = """<p style='font-size: 1.2em; text-align: justify; margin: 10px 0;'>Aquí se mostrará la predicción de tantos días como se indique a continuación del último día 
                        de actualización de la página, o de sus equivalentes en años anteriores 
                        si se ha seleccionado otro año.""", unsafe_allow_html=True)
        st.markdown(body = """<p style='font-size: 1.2em; text-align: justify; margin: 10px 0;'>En la segunda gráfica se mostrará esa misma predicción, 
                           pero integrada en la evolución de la demanda hasta ese momento""", unsafe_allow_html=True)
        st.markdown(body = """<p style='font-size: 1.2em; text-align: justify; margin: 10px 0;'>Tarda unos segundo en cargar, y si se cambian los parámetros 
                              hay que volver a esperar unos segundos.""", unsafe_allow_html=True)


        años = [2024, 2023, 2022]
        año = st.selectbox(label = "Elige año para la proyección de datos", options = años)

        días = [2,3,4,5,6,7,8,9,10,11,12,13,14]
        n_días = st.selectbox(label  = "Di cuántos días quieres predecir",
                                options = días) 


        #demanda_fechas = demanda_data[demanda_data['datetime'].dt.year==año]
        primera_fecha = pd.to_datetime(demanda_data['datetime'].iloc[-1], format='%d/%m/%Y').replace(year=año)
        ultima_fecha = primera_fecha + timedelta(days=n_días)
        lista_fechas = pd.date_range(start=primera_fecha, end=ultima_fecha, freq='D')
        lista_fechas = lista_fechas [1:]
        lista_fechas = pd.DataFrame(lista_fechas, columns = ["fechas"])
        #lista_fechas['fechas'] = lista_fechas['fechas'].dt.strftime('%d/%m')

        demanda_filtrado = demanda_data[demanda_data['datetime'].dt.year==año]
        demanda_filtrado = demanda_filtrado.reset_index()
        indice = demanda_filtrado[demanda_filtrado['datetime'] == primera_fecha].index
        valor_indice = indice[0]
        #demanda_filtrado = demanda_filtrado[demanda_filtrado['Energia_consumida'][:valor_indice]]
        #demanda_filtrado = demanda_filtrado.drop (['Fecha actualización', 'datetime'],axis = 1)

        X = pd.DataFrame(demanda_filtrado["Energia_consumida"][:valor_indice])
        X = escalador.transform(X)

        # "Multiple - Step Predictions"
        # Toma el último valor de una serie y predice el siguiente
        # Usa esa predicción para seguir haciendo predicciones.


        validation_predictions = list()

        last_x = X

        while len(validation_predictions) < n_días:
            
            # En la primera iteración predice el siguiente valor usando X
            # En las siguientes iteraciones usa el valor predicho anterior para predecir el siguiente
            p = modelo.predict(last_x.reshape(1, -1, 1))[0, 0]
            
            validation_predictions.append(p)
            # Desplaza los elementos en last_x hacia atras, dejando el primer elemento al final
            last_x = np.roll(last_x, -1)
            
            # Cambia el último elemento a la predicción
            last_x[-1] = p

        validation_predictions = pd.DataFrame(validation_predictions)
        validation_predictions = escalador.inverse_transform(validation_predictions)
        validation_predictions = pd.DataFrame(validation_predictions, columns = ["valores"])

        #Graficamos las predicciones    
        fig_pred = px.line(
                x = lista_fechas ["fechas"], 
                y = validation_predictions["valores"],
                labels = {'x': 'Fecha', 'y': 'Valores'})
        fig_pred.update_layout(title = 'Predicción de la evolución de la demanda')
        st.plotly_chart(figure_or_data = fig_pred,
                    use_container_width = True)


        #Graficamos las predicciones integradas en el histórico
        demanda_grafica = demanda_data[demanda_data['datetime'].dt.year==año]
        demanda_grafica = demanda_grafica.reset_index()
        indice_grafica = demanda_grafica[demanda_grafica['datetime'] == primera_fecha].index
        valor_indice_grafica = indice_grafica[0]+1
        demanda_grafica = demanda_grafica.iloc[:valor_indice_grafica]

        fig_hist = px.line(demanda_grafica,
                x = "datetime", 
                y = "Energia_consumida",
                labels = {'x': 'Fecha', 'y': 'Valores'}
                )
        fig_hist.add_scatter(
                x = lista_fechas ["fechas"], 
                y = validation_predictions["valores"],
                name = "Predicción")
        fig_hist.update_layout(title = 'Predicción integrada en el recorrido previo')
        st.plotly_chart(figure_or_data = fig_hist,
                    use_container_width = True)



if __name__ == "__main__":
    modelo()