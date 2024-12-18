import pandas as pd
import numpy as np
import mysql.connector
import configparser

import requests

from datetime import datetime, timedelta
from pprint import pprint


lang = "es"
restaDia = 30
input_año = 2024


headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Host": "apidatos.ree.es"
}

##    ---OBTENCIÓN DE DATOS DE BALANCE---

def create_database():
    # Leer el archivo de configuración
    config = configparser.ConfigParser()
    config.read('../../Notebooks/SQL/config.ini')

    # Obtener los valores del archivo de configuración
    host = config['mysql']['host']
    user = config['mysql']['user']
    password = config['mysql']['password']

    try:
        # Establecer conexión con MySQL
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )

        cursor = conn.cursor()

        # Crear la base de datos si no existe
        cursor.execute("CREATE DATABASE IF NOT EXISTS red_electrica")
        conn.commit()

        print("Base de datos 'red_electrica' creada con éxito si existía.")


    finally:
        # Cerrar la conexión
        if conn.is_connected():
            cursor.close()
            conn.close()

# Llamar a la función

    
import requests
import pandas as pd
import mysql.connector
import configparser
from datetime import datetime, timedelta

def balance_datos(lang, input_año, restaDia):

    now = datetime.now()
    ultima_fecha = (now - timedelta(days=restaDia)).replace(year=input_año).strftime('%Y-%m-%d')
    hoy = now.replace(year=input_año).strftime('%Y-%m-%d')
    
    query = f"start_date={ultima_fecha}T00:00&end_date={hoy}T23:59&time_trunc=day"
    endpoint = f"https://apidatos.ree.es/{lang}/datos/balance/balance-electrico?{query}"
    response = requests.get(url=endpoint)
    data = response.json()

    lista_nombres = []
    lista_tipos = []
    lista_valores = []
    lista_porcentajes = []
    lista_fechas = []

    for dato in data['included']: 
        for info in dato['attributes']['content']:
            nombre = info['type']
            tipo = info['groupId']

            for i in info['attributes']['values']:
                valor = i['value']
                porcentaje = i['percentage']
                fecha = pd.to_datetime(i['datetime']).strftime("%d/%m/%Y")
                lista_nombres.append(nombre)
                lista_tipos.append(tipo)
                lista_valores.append(valor)
                lista_porcentajes.append(porcentaje)
                lista_fechas.append(fecha)

    df_balance = pd.DataFrame({
        'nombre': lista_nombres,
        'tipo de energía': lista_tipos,
        'Valores': lista_valores,
        'Porcentaje': lista_porcentajes,
        'Fecha actualización': lista_fechas
    })
    df_balance.to_csv('../../Notebooks/Obtencion datos/balance_electrico.csv', index=False)
    
    config = configparser.ConfigParser()
    config.read('../../Notebooks/SQL/config.ini')

    host = config['mysql']['host']
    user = config['mysql']['user']
    password = config['mysql']['password']
    
    
    df = pd.read_csv('../../Notebooks/Obtencion datos//balance_electrico.csv', sep=',', 
                    parse_dates=['Fecha actualización'], dayfirst=True)

    df['id'] = df.index + 1 

    df.rename(columns={'tipo de energía': 'tipo_energia'}, inplace=True)

    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database='red_electrica'
    )

    cursor = conn.cursor()

    for index, row in df.iterrows():
        cursor.execute(""" 
            INSERT INTO balance (id, nombre, tipo_energia, valores, porcentaje, fecha_actualizacion)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
            nombre = VALUES(nombre),
            tipo_energia = VALUES(tipo_energia),
            valores = VALUES(valores),
            porcentaje = VALUES(porcentaje),
            fecha_actualizacion = VALUES(fecha_actualizacion)
        """, (row['id'], row['nombre'], row['tipo_energia'], row['Valores'], row['Porcentaje'], row['Fecha actualización']))

    conn.commit()


    cursor.close()
    conn.close()

    
    print("Datos insertados o actualizados en la tabla 'balance' con éxito.")


    return df_balance



    #df_balance  = balance_datos(lang)


    ###    ---OBTENCIÓN DE DATOS DE DEMANDA--- 


def demanda_datos(lang, input_año, restaDia):
    now = datetime.now()
    ultima_fecha = (now - timedelta(days=restaDia)).replace(year=input_año).strftime('%Y-%m-%d')
    hoy = now.replace(year=input_año).strftime('%Y-%m-%d')

    query = f"start_date={ultima_fecha}T00:00&end_date={hoy}T23:59&time_trunc=day"
    endpoint = f"https://apidatos.ree.es/{lang}/datos/demanda/evolucion?{query}"
    response = requests.get(url=endpoint)
    data = response.json()

    datetime_lista = []
    value_lista = []
    percentage_lista = []

    for value in data['included']:
        for content in value['attributes']['values']:
            valor = content['value']
            fecha = content['datetime']
            fecha = pd.to_datetime(fecha).strftime("%d/%m/%Y")
            datetime_lista.append(fecha)
            value_lista.append(valor)

    df_demanda = pd.DataFrame({
        'Fecha actualización': datetime_lista,
        'Energía_consumida': value_lista,
    })

    df_demanda.to_csv('../../Notebooks/Obtencion datos/demanda_evolucion.csv', index=False)

    # Leer el archivo de configuración
    config = configparser.ConfigParser()
    config.read('../../Notebooks/SQL/config.ini')

    # Obtener los valores del archivo de configuración
    host = config['mysql']['host']
    user = config['mysql']['user']
    password = config['mysql']['password']

    # Cargar el CSV y mostrar las primeras filas para depuración
    df_raw = pd.read_csv('../../Notebooks/Obtencion datos/demanda_evolucion.csv', sep=',')

    # Cargar el CSV con el nombre correcto de la columna para la fecha
    # Ajustamos el formato de la fecha a 'dd/mm/yyyy' al cargar el CSV
    df = pd.read_csv('../../Notebooks/Obtencion datos/demanda_evolucion.csv', sep=',', 
                    parse_dates=['Fecha actualización'], 
                    dayfirst=True)  # Asegurarse de que se interprete correctamente

    # Renombrar las columnas adecuadamente
    df.rename(columns={'Fecha actualización': 'fecha', 'Energía_consumida': 'valor'}, inplace=True)

    # Crear una columna 'id' usando el índice del DataFrame
    df['id'] = df.index + 1  # Genera un id único basado en el índice

    # Conectar a la base de datos
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database='red_electrica'
    )

    # Crear cursor
    cursor = conn.cursor()

    # Insertar o actualizar datos en la tabla usando el id como clave única
    for index, row in df.iterrows():
        cursor.execute(""" 
            INSERT INTO demanda (id, fecha, valor)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE
            fecha = VALUES(fecha),
            valor = VALUES(valor)
        """, (row['id'], row['fecha'], row['valor']))  # Se eliminó 'porcentaje'

    # Confirmar los cambios
    conn.commit()

    # Cerrar conexión
    cursor.close()
    conn.close()

    print("Datos insertados o actualizados en la tabla 'demanda' con éxito.")

    return df_demanda


####  ----OBTENCIÓN DE DATOS DE GENERACIÓN---- 


def generacion_datos(lang,input_año, restaDia):

    now = datetime.now()
    ultima_fecha = (now - timedelta(days = restaDia)).replace(year = input_año).strftime('%Y-%m-%d')
    
    hoy = now.replace(year = input_año).strftime('%Y-%m-%d')
    
    query = f'start_date={ultima_fecha}T00:00&end_date={hoy}T23:59&time_trunc=day'


    endpoint = f"https://apidatos.ree.es/{lang}/datos/generacion/estructura-generacion?{query}"
    response = requests.get(url= endpoint, headers= headers)
    data = response.json()

    lista_nombres = list()
    lista_tipos = list()
    lista_valores = list()
    lista_porcentajes = list()
    lista_fechas = list()
    



    for dato in data['included']:
        nombre = dato['attributes']['title']
        tipo = dato['attributes']['type']


        for i in dato['attributes']['values']:
            valor = i['value']

            porcentaje = i['percentage']

            fecha = i['datetime']
            fecha = pd.to_datetime(fecha)
            

            fecha =  fecha.strftime("%d/%m/%Y")

            lista_nombres.append(nombre)
            lista_tipos.append(tipo)
            lista_valores.append(valor)
            lista_porcentajes.append(porcentaje)
            lista_fechas.append(fecha)
            

    df_generacion = pd.DataFrame()
    df_generacion['nombre']               = lista_nombres
    df_generacion['tipo de energía']      = lista_tipos
    df_generacion['Valores']              = lista_valores
    df_generacion["Porcentaje"]           = lista_porcentajes
    df_generacion["Fecha actualización"]  = lista_fechas
    
    df_generacion.to_csv('../../Notebooks/Obtencion datos/generacion_estructura.csv')

    # Leer el archivo de configuración
    config = configparser.ConfigParser()
    config.read('../../Notebooks/SQL/config.ini')

    # Obtener los valores del archivo de configuración
    host = config['mysql']['host']
    user = config['mysql']['user']
    password = config['mysql']['password']

    # Cargar el CSV
    df = pd.read_csv('../../Notebooks/Obtencion datos/generacion_estructura.csv', sep=',', parse_dates=['Fecha actualización'])

    # Renombrar las columnas para que coincidan con la estructura de la tabla
    df.rename(columns={
    'tipo de energía': 'tipo_energia', 
    'Valores': 'valores', 
    'Porcentaje': 'porcentaje', 
    'Fecha actualización': 'fecha_actualizacion'
    }, inplace=True)

    # Crear una columna 'id' usando el índice del DataFrame
    df['id'] = df.index + 1  # Genera un id único basado en el índice

    # Conectar a la base de datos
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database='red_electrica'
    )

    # Crear cursor
    cursor = conn.cursor()

    # Insertar o actualizar datos en la tabla usando el id como clave única
    for index, row in df.iterrows():
        cursor.execute("""
            INSERT INTO generacion (id, nombre, tipo_energia, valores, porcentaje, fecha_actualizacion)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
            nombre = VALUES(nombre),
            tipo_energia = VALUES(tipo_energia),
            valores = VALUES(valores),
            porcentaje = VALUES(porcentaje),
            fecha_actualizacion = VALUES(fecha_actualizacion)
            """, (row['id'], row['nombre'], row['tipo_energia'], row['valores'], row['porcentaje'], row['fecha_actualizacion']))

    # Confirmar los cambios
    conn.commit()

    # Cerrar conexión
    cursor.close()
    conn.close()

    print("Datos insertados o actualizados en la tabla 'generacion' con éxito.")

    return df_generacion


#  --- OBTENCIÓN DE DATOS DE INTERCAMBIO ---

def intercambio_datos(lang,input_año, restaDia):
    now = datetime.now()
    ultima_fecha = (now - timedelta(days = restaDia)).replace(year = input_año).strftime('%Y-%m-%d')
    hoy = now.replace(year = input_año).strftime('%Y-%m-%d')

    query = f"start_date={ultima_fecha}T00:00&end_date={hoy}T23:59&time_trunc=day"


    endpoint = f"https://apidatos.ree.es/{lang}/datos/intercambios/todas-fronteras-programados?{query}"
    response = requests.get(url = endpoint, headers = headers)
    data = response.json()


    lista_nombres = list()
    lista_tipos = list()
    lista_valores = list()
    lista_porcentajes = list()
    lista_fechas = list()
   


    for dato in data['included']: 
        for info in dato['attributes']['content']:
            tipo = info['type']

            nombre = info['groupId']


            for i in info['attributes']['values']:
                valor = i['value']

                porcentaje = i['percentage']

                fecha = i['datetime']
                fecha = pd.to_datetime(fecha)
                

                fecha =  fecha.strftime("%d/%m/%Y")

                
                lista_nombres.append(nombre)
                lista_tipos.append(tipo)
                lista_valores.append(valor)
                lista_porcentajes.append(porcentaje)
                lista_fechas.append(fecha)
               


    df_intercambio = pd.DataFrame()
    df_intercambio['nombre']               = lista_nombres
    df_intercambio['tipo de intercambio']      = lista_tipos
    df_intercambio['Valores']              = lista_valores
    df_intercambio["Porcentaje"]           = lista_porcentajes
    df_intercambio["Fecha actualización"]  = lista_fechas

    df_intercambio.to_csv('../../Notebooks/Obtencion datos/intercambio_electrico.csv')
             
    # Leer el archivo de configuración
    config = configparser.ConfigParser()
    config.read('../../Notebooks/SQL/config.ini')

    # Obtener los valores del archivo de configuración
    host = config['mysql']['host']
    user = config['mysql']['user']
    password = config['mysql']['password']

    # Cargar el CSV
    df = pd.read_csv('../../Notebooks/Obtencion datos/intercambio_electrico.csv', sep=',', parse_dates=['Fecha actualización'])

    # Renombrar las columnas para que coincidan con la estructura de la tabla
    df.rename(columns={
    'tipo de intercambio': 'tipo_intercambio', 
    'Valores': 'valores', 
    'Porcentaje': 'porcentaje', 
    'Fecha actualización': 'fecha_actualizacion'
    }, inplace=True)

    # Crear una columna 'id' usando el índice del DataFrame
    df['id'] = df.index + 1  # Genera un id único basado en el índice

    # Conectar a la base de datos
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database='red_electrica'
        )

    # Crear cursor
    cursor = conn.cursor()

    # Insertar o actualizar datos en la tabla usando el id como clave única
    for index, row in df.iterrows():
        cursor.execute("""
        INSERT INTO intercambio (id, nombre, tipo_intercambio, valores, porcentaje, fecha_actualizacion)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        nombre = VALUES(nombre),
        tipo_intercambio = VALUES(tipo_intercambio),
        valores = VALUES(valores),
        porcentaje = VALUES(porcentaje),
        fecha_actualizacion = VALUES(fecha_actualizacion)
        """, (row['id'], row['nombre'], row['tipo_intercambio'], row['valores'], row['porcentaje'], row['fecha_actualizacion']))

    # Confirmar los cambios
    conn.commit()

    # Cerrar conexión
    cursor.close()
    conn.close()

    print("Datos insertados o actualizados en la tabla 'intercambio' con éxito.")

    return df_intercambio 
    
if __name__ == "__main__":
    balance_datos(lang,input_año, restaDia)
    demanda_datos(lang, input_año, restaDia)
    generacion_datos(lang,input_año, restaDia)
    intercambio_datos(lang,input_año, restaDia)