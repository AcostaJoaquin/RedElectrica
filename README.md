<div align="center">

# Proyecto cuadro de mando de la red eléctrica de España

</div>

<div align="center">

  <img src="https://github.com/AcostaJoaquin/PFB-Grupo-B/blob/main/sources/logo.png" alt="logo" width="100%">

</div>
# VISUALIZACIÓN DEL PROYECTO EN LA NUBE

[Análisis de la red eléctrica española](https://cuadrodemandoree.streamlit.app/)

# 1- TECNOLGÍAS USADAS:

<div align="center"> </div>

Lenguaje: Python, SQL.

Librerias: numpy, pandas, plotly, folium, tensorflow, sklearn, pickle, datetime, PIL, requests, cv2, streamlit.

# 2- INTEGRANTES:

<div align="center"> </div>
Diego Díaz Gómez, Luís Miguel Guerrero Albalat, Joaquín Acosta Desalvo, Victor Manuel Harillo Parra

# 3- INTRODUCCIÓN DEL PROYECTO:

<div align="center"> </div>

Nuestro proyecto se trata de las Redes Electricas Españolas, presentado en una plataforma de Streamlit. En esta plataforma interactiva se ofrece un análisis detallado sobre el balance, la demanda, la generación y el intercambio energético español de los ultimos 7, 14 y 30 días, así como una predicción de la evolución de la demanda energética de futuros días, abarcando los próximos 2 a 14 días. Para ello, se ha obtenido información principalmente de la API de REData, que ofrece un amplio registro de los distintos movimientos que se realizan a diario en dicho mercado. Además, para la parte de la predicción, se ha entrenado un modelo de aprendizaje automático que permite, con el histórico de datos, conocer aproximadamente cuáles serán los valores de la demanda para los siguientes días.

Este es el resultado de nuestro proyecto final del curso de Data Science e Inteligencia Artificial de la escuela HACK A BOSS. Es por ello que aquí se muestra la aplicación de diferentes conceptos y tareas relacionados con el mundo del manejo de datos y los modelos de inteligencia artificial, como puedan ser la recopilación y limpieza de datos, la creación de gráficas interactivas o el uso de los ya mencionados modelos, entre otras cosas.

Por tanto, este proyecto refleja nuestro esfuerzo conjunto con el objetivo de generar una herrramienta útil e interesante, que además muestre nuestras habilidades y sirva para reflejar lo haprendido durante el curso.

Las principales funcionalidades de la plataforma son:

-<u>_Gráficas interactivas_</u>:<br> A través de ellas visualizamos los datos relativos al balance, la demanda, la generación y los intercambios de energía en el mercado español. Estas nos ayudarán a comprender mejor la situación actual del mismo, así como a poder comparar los diferentes componentes de cada tipo de activo energético.

En el subapartado "intercambio" integramos además un mapa dinámico que permite explorar geográficamente los datos de intercambio de energía entre las principales fronteras de España.

Para una exploración más detallada y personalizada, le invitamos a visitar la sección de gráficas interactivas. Allí podrá filtrar los datos por fecha o tipo de energía, y analizar tendencias, patrones y relaciones entre los diferentes componentes del sistema.

-<u>_Modelo de Machine Learning_</u>:<br> Hemos implementado un modelo de aprendizaje automático que realiza predicciones sobre el comportamiento futuro de la demanda en el sistema energético español. En esta pestaña se puede visualizar una muestra de los resultados obtenidos con el modelo, y en su sección correspondiente se puede ver lo que ofrece con mayor detalle, así como una explicación técnica del propio modelo.

# 3.1 EXPLICACIÓN DE CADA PÁGINA:

<div align="center"> </div>

-<u>_Balance_</u>:<br> En esta sección se muestra el informe diario de balance. El balance energético diario es el detalle de producción y consumo energético en los sistemas penilsulares y no penilsulares de la red eléctrica española, así como de Ceuta y Melilla.

Incluidos en este apartado, encontramos datos y gráficas que nos muestran la estructura necesaria para la cobertura de la demanda energética. Ésta misma se encuentra distribuida en diferentes tipos de energías renovables y no renovables.

-<u>_Demanda_</u>:<br> La demanda energética hace referencia a la cantidad de energía que se requiere para satisfacer las necesidades de una población, de un sector económico o de una región en particular. Este concepto es clave en la planificación y gestión de los recursos energéticos, ya que ayuda a prever y satisfacer la demanda según las características de consumo de cada área. En nuestro país, esta energía puede proceder de diversas fuentes, como fuentes renovables y no renovables, que juntas contribuyen a la generación de la energía necesaria para el funcionamiento de la sociedad.

En el gráfico, se observa cómo la demanda energética varía a lo largo de los días seleccionados en la barra lateral, lo que permite identificar patrones de consumo en días específicos. Estos cambios se reflejan en momentos de alta demanda, conocidos como "picos", que suelen coincidir con horas de gran actividad, y en momentos de baja demanda, denominados "valles", que suelen ocurrir en horarios nocturnos o durante periodos de menor actividad. Este análisis de picos y valles es fundamental para la administración eficiente de la energía y la optimización de los recursos energéticos en nuestro país.

-<u>_Generación_</u>:<br> En esta sección se muestra el informe diario de generación eléctrica.

Los datos de generación energética diaria registra la cantidad de energía eléctrica que se produce en un momento dado a través de diferentes fuentes o combustibles, sean renovables, no renovables, o demandas en barra central en los sistemas penilsulares y no penilsulares de la red eléctrica española.

Estos datos son fundamentales para comprender cómo se suministra la energía eléctrica a la población y a la industria, y para analizar la evolución del sistema energético.

-<u>_Intercambio_</u>:<br> En esta sección se muestra el último informe de intercambio energético con nuestros países vecinos. El mapa te ofrece ver los datos de importación y exportación energética de otros países así como el saldo el cual es la diferencia entre la importación y exportación. En el caso de que no hubiera ninguna información, no mostraría ninguna etiqueta tras la bandera de cada país.

El intercambio energético también demuestra una linea que va de España hacia afuera, lo cual significa que esta exportando energía o, en cuanto a saldo energético con el país vecino se trata, habla de una deuda energética a pagar.

De la misma manera, si la linea va desde el país vecino hacia adentro, significa que esta importando energía o, en cuanto a saldo energético con el país vecino se trata, habla de una deuda energética en el que el país vecino sale deudor con España.

# 3.2 EXPLICACION DEL MODELO:

<div align="center"> </div>

-<u>_Modelo de machine learning_</u>:<br> En este apartado explicaremos las decisiones tomadas para construir nuestro modelo de Machine Learning y veremos las predicciones realizadas por este.

Vistas las operaciones que componen el flujo principal de actividades de la red eléctrica española, la que suscita mayor interés a la hora de intentar predecir su evolución es la demanda, ya que indica cuanta electricidad se consume o se va a consumir en nuestro país.

Es por ello que hemos desarrollado una herramienta que ofrece una aproximación a la que será la demanda energética de los próximos días. Dicha herramienta se basa en un modelo de Machine learning (cuyos detalles se especifican más adelante) entrenado con datos extraidos de la API REData, que permite extraer datos en bruto de los movimientos de la red eléctrica española.

# 4- CONCLUSIONES:

<div align="center"> </div>
En definitiva, este proyecto no solo refleja nuestro aprendizaje y habilidades técnicas, sino también el potencial del análisis de datos en la optimización de sectores tan cruciales como el energético, demostrando la relevancia y el impacto que la ciencia de datos y el aprendizaje automático pueden tener en áreas de gran importancia económica y social.

De cara al futuro algo que podríamos mejorar o añadir sería hacer predicciones sobre el resto de categorías (balance, generación, intercambio) e incluso perfeccionar la demanda por comunidades autónomas al mostrar gráficas comparativa mensual de la demanda energética por comunidades autónomas españolas.
