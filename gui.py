# -*- coding: utf-8 -*-
# !/usr/bin/env python
# ----------------------------------------------------------------------------------------------------------------
# Archivo: gui.py
# Tarea: 2 Arquitecturas Micro Servicios.
# Autor(es):
# Daniel Hernández
# Oscar Oswaldo
# Armando Rodarte
# Alejandro Pinedo 
# Version: 2.0 Mayo 2018
# Descripción:
#
#   Este archivo define la interfaz gráfica del usuario. Recibe dos parámetros que posteriormente son enviados
#   al API Gateway para la comunicación con los servicios utilizados por el sistema.
#   
#   Consume el API Gateway que se comunica con los servicios que
        proporcionan información al usuario.
#
#                                             gui.py
#           +-----------------------+-------------------------+-----------------------------+
#           |  Nombre del elemento  |     Responsabilidad     |          Propiedades        |
#           +-----------------------+-------------------------+-----------------------------+
#           |                       |  - Porporcionar la in-  | - Consume el API Gateway    |
#           |          GUI          |    terfaz gráfica con la|   que se comunica con los   |
#           |                       |    que el usuario hará  |   servicios que proporcionan|
#           |                       |    uso del sistema.     |   información al usuario.   |
#           +-----------------------+-------------------------+-----------------------------+
#

import os
from flask import Flask, render_template, request
import urllib, json
import requests

app = Flask(__name__)


@app.route("/")
def index():
    # Método que muestra el index del GUI
    return render_template("index.html")


@app.route("/information", methods=['GET'])
def sentiment_analysis():
    # Solicitud al servicio sv_information, por medio del API Gateway.
    url = 'http://localhost:8085/api/movie/information'
    response_omdb = requests.get(url, request.args)
    json_result = {'omdb': {}, 'twitter': {}, 'no_results': {}}
    error_omdb = False

    if response_omdb.status_code == 200:
        json_result['omdb'] = response_omdb.json()
        json_result['omdb']['display'] = ''
    else:
        json_result['omdb']['display'] = 'hidden'
        error_omdb = True

    # Solicitud al servicio sv_gestor_tweets, por medio del API Gateway.
    url = 'http://localhost:8085/api/tweet/search'
    response_obtener = requests.get(url, request.args)
    error_tweet = False

    if response_obtener.status_code == 200:
        # Solicitud al servicio sv_analizador_tweets, por medio del API Gateway.
        url = 'http://localhost:8085/api/tweet/analizar'
        response_analizar = requests.post(url, {'tweets': json.dumps(
            response_obtener.json())})
        if response_analizar.status_code == 200:
            json_result['twitter'] = response_analizar.json()
            json_result['twitter']['display'] = ''
        else:
            error_tweet = True
    else:
        error_tweet = True
    error_tweet = error_tweet or response_analizar.json()['totales'] == 0
    if error_tweet:
        json_result['twitter']['display'] = 'hidden'
    json_result['no_results']['display'] = 'hidden'
    if error_omdb and error_tweet:
        json_result['no_results']['display'] = ''
    # Se manda renderizar el template html con los datos que debe cargar
    return render_template("status.html", result=json_result)


if __name__ == '__main__':
    # Se define el puerto del sistema operativo que utilizará el Sistema de Procesamiento de Comentarios (SPC).
    port = int(os.environ.get('PORT', 8088))
    # Se habilita el modo debug para visualizar errores
    app.debug = True
    # Se ejecuta el GUI con un host definido cómo '0.0.0.0' para que pueda ser accedido desde cualquier IP
    app.run(host='0.0.0.0', port=port)

