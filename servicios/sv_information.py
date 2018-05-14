# -*- coding: utf-8 -*-
# !/usr/bin/env python
# ----------------------------------------------------------------------------------------------------------------
# Archivo: sv_information.py
#Tarea: 2 Arquitecturas Micro Servicios.
# Autor(es):
# Daniel Hernández
# Oscar Oswaldo
# Armando Rodarte
# Alejandro Pinedo 
# Version: 2.0 Mayo 2018
# Descripción:
#
#   Este archivo define el rol de un servicio. Su función general es porporcionar en un objeto JSON
#   información detallada acerca de una pelicula o una serie en particular haciendo uso del API proporcionada
#   por IMDb ('https://www.imdb.com/').
#
#
#
#                                        sv_information.py
#           +-----------------------+-------------------------+------------------------+
#           |  Nombre del elemento  |     Responsabilidad     |      Propiedades       |
#           +-----------------------+-------------------------+------------------------+
#           |                       |  - Ofrecer un JSON que  | - Utiliza el API de    |
#           |    Procesador de      |    contenga información |   IMDb.                |
#           |     comentarios       |    detallada de pelí-   | - Devuelve un JSON con |
#           |       de IMDb         |    culas o series en    |   datos de la serie o  |
#           |                       |    particular.          |   pelicula en cuestión.|
#           +-----------------------+-------------------------+------------------------+
#

import os
from flask import Flask, abort, render_template, request
from flask.ext.api import FlaskAPI, status
import urllib, json

app = Flask(__name__)


@app.route("/api/v1/information")
def get_information():
    """
    Este método obtiene información acerca de una película o serie
    específica.
    :return: JSON con la información de la película o serie
    """
    # Se lee el parámetro 't' que contiene el título de la película o serie que se va a consultar
    
    if 'title' in request.args.keys():
        title = request.args['title']
        url_base = 'http://www.omdbapi.com/?t=' + title + '&plot=full&r=json'
        # Se conecta con el servicio de IMDb a través de su API
        response_omdb = requests.get(url_base, request.args)
        if 'Error' in response_omdb.json():
            error_response = {'message': response_omdb.json()['Error']}
            return error_response, status.HTTP_404_NOT_FOUND
        # Se regresa el JSON de la respuesta
        return response_omdb.json(), response_omdb.status_code
    else:
        error_response = {'message': 'Parámetros incompletos'}
        # Se regresa un mensaje de error
        return  error_response, status.HTTP_400_BAD_REQUEST

if __name__ == '__main__':
    # Se define el puerto del sistema operativo que utilizará el servicio
    port = int(os.environ.get('PORT', 8087))
    # Se habilita la opción de 'debug' para visualizar los errores
    app.debug = True
    # Se ejecuta el servicio definiendo el host '0.0.0.0' para que se pueda acceder desde cualquier IP
    app.run(host='0.0.0.0', port=port)
