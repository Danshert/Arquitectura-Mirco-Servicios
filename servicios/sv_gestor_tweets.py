# -*- coding: utf-8 -*-
# !/usr/bin/env python
# ----------------------------------------------------------------------------------------------------------------
# Archivo: sv_gestor_tweets.py
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
#   los comentarios obtenidos de una película o serie de netflix por medio de la API de Twitter.
#
#
#
#                                        sv_gestor_tweets.py
#           +-----------------------+-------------------------+------------------------+
#           |  Nombre del elemento  |     Responsabilidad     |      Propiedades       |
#           +-----------------------+-------------------------+------------------------+
#           |                       |  - Representar el       | - Contiene los         |
#           |                       |    modelo de un tweet   |   atributos            |
#           |                       |    en la base de datos  |   - user_name          |
#           |         Tweet         |                         |   - tweet_hashtag      |
#           |                       |                         |   - tweet_body         |
#           |                       |                         |   - tweet_date         |
#           +-----------------------+-------------------------+------------------------+
#           |                       |  - Obtener Tweets y     | - Realiza la peticion  | 
#           |                       |    devolverlos cono     |   a la API de twitter  |
#           |                       |    intancias de la      |   y obtener los        | 
#           |     BuscadorTweets    |    clase tweet.         |   comentarios.         |
#           |                       |                         | - Devolver instancias  |
#           |                       |                         |   de la clase Tweet a  |
#           |                       |                         |   partir de los        |
#           |                       |                         |   resultados           | 
#           +-----------------------+-------------------------+------------------------+  
#           |                       |  - Manejar              | - Utiliza SQLite para  |
#           |   PersistenciaTweets  |    la persistencia de   |   la persistencia      |  
#           |                       |    tweets.              |   de tweets.           |
#           |                       |                         | - Inserta y devuelve   |              
#           |                       |                         |   los tweets           |
#           +-----------------------+-------------------------+------------------------+ 
#           |                       | - Devuelve un JSON con  | - Utiliza la clase     |
#           |                       |   con los tweets de una |   BuscadorTweets para  |
#           |       Gestor de       |   serie o película.     |   obtener los tweets   |
#           |      comentarios      |                         |   de la API de Twitter |   
#           |       de Twitter      |                         | - Utiliza la clase     |
#           |                       |                         |   persistenciaTweets   |
#           |                       |                         |   para persistir los   |
#           |                       |                         |   datost y obtenerlos  |
#           +-----------------------+-------------------------+------------------------+ 

import os
from flask import request
from flask.ext.api import FlaskAPI, status
from twython import Twython
import sys
import requests.packages.urllib3
import sqlite3

class PersistenciaTweets:
    def __init__(self):
        self.open_connection()
        self.cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS tweets(
                user_name TEXT,
                tweet_hashtag TEXT,
                tweet_body TEXT,
                tweet_date DATETIME,
                PRIMARY KEY (user_name, tweet_date)
            )
            ''')
        self.conn.commit()
        self.conn.close()

    def open_connection(self):
        self.conn = sqlite3.connect('tweets.db')
        self.cursor = self.conn.cursor()

    def insert_tweet(self, tweet):
        self.open_connection()
        self.cursor.execute(
            'INSERT OR IGNORE INTO tweets (tweet_body, tweet_date, '
            'user_name, tweet_hashtag) VALUES (?, '
            '?, ?, ?)', tweet)
        self.conn.commit()
        self.conn.close()

    def insert_tweets(self, tweets):
        self.open_connection()
        self.cursor.executemany(
            'INSERT OR IGNORE INTO tweets (tweet_body, tweet_date, '
            'user_name, tweet_hashtag) VALUES (?, '
            '?, ?, ?)', tweets)
        self.conn.commit()
        self.conn.close()

    def get_all_tweets(self):
        self.open_connection()
        tweets = self.cursor.execute('SELECT * FROM tweets').fetchall()
        self.conn.commit()
        self.conn.close()
        return tweets

    def get_tweets_by_hashtag(self, hashtag):
        self.open_connection()
        tweets = self.cursor.execute('SELECT * FROM tweets WHERE '
                                     'tweet_hashtag=?', [hashtag])
        data = tweets.fetchall()
        self.conn.commit()
        self.conn.close()
        return [{'user_name': row[0], 'tweet_hashtag': row[1],
                 'tweet_body': row[2], 'tweet_date': row[3]} for row in data]



reload(sys)
requests.packages.urllib3.disable_warnings()
sys.setdefaultencoding("utf-8")


class Tweet:
    def __init__(self, screen_name, hashtag, text, created_at):
        self.screen_name = screen_name
        self.hashtag = hashtag
        self.text = text
        self.created_at = created_at


class BuscadorTweets:
    def __init__(self):
        self.ConsumerKey = "jfij525430WHSqo46VCXiTA95"
        self.ConsumerSecret = "BfFZ6iSPTj7u699apBGY3Yu4RHMLOVR61QGASVenGVLdjh6lRb"
        self.AccessToken = "3290922366-kDNgrRkVLYnVQXDTtKbJqH1wCj0fkVKJy3PotjV"
        self.AccessTokenSecret = "Ulb7EPn9VQ4rWa8wIXflzGvMuNrZ1yBtVYQ6MSTvtl1We"
        self.twitter = Twython(self.ConsumerKey, self.ConsumerSecret,
                               self.AccessToken, self.AccessTokenSecret)

    def to_hashtag(self, text):
        return '#' + ''.join(c for c in text.title() if not c.isspace())

    def search_tweets(self, title):
        search_query = '@netflix ' + self.to_hashtag(title)
        result = self.twitter.search(q=search_query, count=20)
        tweets = []
        for status in result["statuses"]:
            screen_name = status["user"]['screen_name']
            hashtag = self.to_hashtag(title)
            text = status['text']
            created_at = status['created_at']
            tweets.append(Tweet(screen_name, hashtag, text, created_at)
                          .__dict__)
        return tweets

app = FlaskAPI(__name__)


@app.route("/api/tweet/search", methods=['GET'])
def buscar_tweets():
    # Se verifica que el parámetro 'titulo' venga en la request
    if 'titulo' in request.args.keys():
        # Obtiene el valor del parámetro
        titulo = request.args['titulo']
        # Crea la instancia del buscador de tweets
        buscador = BuscadorTweets()
        # Busca y obtiene los tweets por medio del título
        tweets = buscador.search_tweets(titulo)
        # Crea la instancia del manejador de sqlite
        persistencia = PersistenciaTweets()
        # Manda insertar los tweets en la base de datos
        persistencia.insert_tweets(tweet.values() for tweet in tweets)
        # devuelve un JSON con los tweets y el código de la solicitud
        tweets_bd = persistencia.get_tweets_by_hashtag(
            buscador.to_hashtag(titulo))
        if len(tweets_bd) > 0:
            return tweets_bd, status.HTTP_200_OK
        else:
            return {'message': 'No tweets found'}, status.HTTP_404_NOT_FOUND
    else:
        # Mensaje de error
        error_response = {'message': 'Parámetros incompletos'}
        # Devuelve el mensaje de error y el código de la solicitud
        return error_response, status.HTTP_400_BAD_REQUEST

if __name__ == '__main__':
    print '--------------------------------------------------------------------'
    print 'Servicio sv_gestor_tweets'
    print '--------------------------------------------------------------------'
    port = int(os.environ.get('PORT', 8084))
    app.debug = True
    app.run(host='0.0.0.0', port=port)
