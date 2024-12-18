import streamlit as st
import pandas as pd
import os
import cv2
from PIL import Image




def informacion_app():
    # Columnas para el logo y el título
    col_img, col_tit = st.columns((0.2, 1.6))

    # Título con logo
    logo = cv2.imread(filename="sources/logo.png")
    logo = cv2.cvtColor(logo, cv2.COLOR_BGR2RGB)
    logo = cv2.resize(logo, (200, 200))
    col_img.image(logo, use_column_width=True)
    col_tit.markdown(
        "<h1 style='margin-top: 15px; color: skyblue; font-size: 3em;'>"
        "Más detalles sobre los creadores</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style=' font-size: 1.2em;'>"
        'En esta sección, podrás conocer a los miembros del equipo detrás de este proyecto. Cada uno de nosotros ha contribuido con sus habilidades y experiencia para hacer realidad este trabajo, y estamos disponibles para cualquier consulta o colaboración futura. <br><br>'
        'Esperamos que esta sección te haya proporcionado una visión más clara sobre quiénes somos y el trabajo que hemos realizado en este proyecto. Nos apasiona seguir avanzando en el campo de la tecnología y la ciencia de datos, y estamos siempre abiertos a nuevas oportunidades de colaboración. Te invitamos a explorar nuestro código, seguir nuestras actualizaciones y no dudes en contactarnos a través de LinkedIn para conversar sobre nuestras experiencias o ideas futuras.',
        unsafe_allow_html=True)

    ###################### Info creadores #########################
    width, height = 300, 300
    col, columna_diego, columna_luis, columna_victorm, columna_joaquin = st.columns((0.15,1,1,1,1))

    with columna_diego:
        st.header(":blue[Diego Díaz]")
        img1 = Image.open('sources/Diego.png')
        st.image(img1)

        # Links:
        linkedin, github = st.columns((1,1))

        linkedin.link_button("Linkedin", "https://www.linkedin.com/in/diegodiazgomez/")
        github.link_button("Github", "https://github.com/diegodiazgomez")


    #############################################
    #### Luis #####
    with columna_luis:
        st.header(":blue[Luis M. Guerrero]")
        img2 = Image.open('sources/luis.png')
        st.image(img2)
        

        #Links:
        linkedin, github = st.columns((1,1))

        linkedin.link_button("Linkedin", "https://www.linkedin.com/in/luismguerrero/")
        github.link_button("Github", "https://github.com/LouieGGG")

#########
    ### Víctor Manuel ###
    with columna_victorm:
        st.header(":blue[Victor M. Harillo]")
        victorm = Image.open("sources/Victor.png")
        st.image(victorm)

        #Links:
        linkedin, github = st.columns((1,1))

        linkedin.link_button("Linkedin", "https://www.linkedin.com/in/victormanuelharilloparra")
        github.link_button("Github", "https://github.com/HarilloP")

    ###############################
    ### Joaquin ############
    with columna_joaquin:
        st.header(":blue[Joaquín Acosta]")
        joaquin = Image.open("sources/joaquin.png")
        st.image(joaquin)

        #Links:
        linkedin, github = st.columns((1,1))

        #linkedin.link_button("Linkedin", )
        linkedin.link_button("Linkedin", "https://www.linkedin.com/in/joaquinacde?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app")
        github.link_button("Github", "https://github.com/AcostaJoaquin" )








if __name__ == "__informacion_app_":
    informacion_app()