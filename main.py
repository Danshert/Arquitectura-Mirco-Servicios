# -*- coding: utf-8 -*-
# !/usr/bin/env python
# ----------------------------------------------------------------------------------------------------------------
# Archivo: sv_analizador_tweets.py
#Tarea: 2 Arquitecturas Micro Servicios.
# Autor(es):
# Daniel Hernández
# Oscar Oswaldo
# Armando Rodarte
# Alejandro Pinedo 
# Version: 2.0 Mayo 2018
# Descripción:
#
#   Este archivo inicializa los servicios y elementos necesarios para
#	el funcionamiento del sistema
#

import os
import webbrowser

def run_python_program(program_name):
    os.system("gnome-terminal -e 'bash -c \"python " + program_name + "\"'")

# Se levantan los microservicios.
run_python_program('servicios/sv_gestor_tweets.py')
run_python_program('servicios/sv_analizador_tweets.py')
run_python_program('servicios/sv_information.py')

# Se levanta el API Gateway.
run_python_program('api_gateway.py')

# Se levanta la GUI.
run_python_program('gui.py')


webbrowser.open('http://localhost:8088', new=0)
