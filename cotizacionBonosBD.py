# -*- coding: utf-8 -*-
"""
Created on Tue Oct 19 21:03:09 2021

@author: Adrian
"""

import pandas as pd
import sqlite3
import requests
import funcionesIol as fiol

# de estos tickers voy a pedir la cotizacion
simbolos = ['AL29D', 'GD29D', 'AL30D', 'GD30D', 'AL35D', 'AE38D','AL41D']
url_base = "C:/Users/Adrian/Documents/Adrian/Python/Base de datos/Bd Bonos/bdbonos.db"


response_auth = fiol.pedir_token()


if (response_auth.status_code == 200):
        json_data = response_auth.json()

        #aca tengo los dos tokens que necesito
        access_token = json_data['access_token']
        refresh_token = json_data['refresh_token']

        headers = {'Authorization': 'Bearer ' + access_token}

        # pongo los parametros para pedir precio de un tiulo
        # /api/v2/{Mercado}/Titulos/{Simbolo}/Cotizacion
        # simbolo = 'AL29D'
       
 
    
        for simbolo in simbolos:
                
            mercado = 'bCBA'
            plazo = 't2'
   
            parametros = {
                'simbolo': simbolo,
                'mercado': mercado,
                'model.simbolo': simbolo,
                'model.mercado': mercado,
                'model.plazo': plazo
            }

            # Hacemos un Get Request con el Encabezado, que contiene el token de acceso
            # y los parametros de busqueda
            # devuelve el precio actual y fecha (lo que a mi me importa) entre otras cosas
            
            response = requests.get('https://api.invertironline.com/api/v2/{Mercado}/Titulos/{Simbolo}/Cotizacion',
                                     headers=headers,
                                     params=parametros,
                                     verify=True)
            
            camposBase = ['ultimoPrecio','variacion','apertura','maximo','minimo',
                          'fechaHora','cierreAnterior','montoOperado','volumenNominal',
                          'cantidadOperaciones']

            if (response.status_code == 200):
                # pedimos los datos en formato JSON
                api_response = response.json()
                df_response = pd.json_normalize(data=api_response)
                df_response = df_response[camposBase]
                
                
                db_conexion = sqlite3.connect(url_base)
                # db_cursor = db_conexion.cursor()
                
                # for row in db_cursor.execute("select * from tbono"):
                #     print(row)
                query_idbono = "select idbono from tbono where ticker = '{}'".format(simbolo)
                
                
                # Busco el id del tiker
                idbono = pd.read_sql(query_idbono, db_conexion)
                
                # lo agrego al df
                df_response['idbono']=idbono
                
                df_response.to_sql("tcotizaciones", con = db_conexion, if_exists='append', index = False)
                
                db_conexion.commit()
                db_conexion.close()
                
            else:
                print('Error al obtener contizaciones de: ' + simbolo)
         
            

else:
    print ('Error al logearse en la API de IOL')
