# -*- coding: utf-8 -*-
"""
Created on Tue Oct 19 21:03:09 2021

@author: Adrian
"""
# FUNCIONA
import pandas as pd
import sqlite3
#import requests
import funcionesIol as fiol

# de estos tickers voy a pedir la cotizacion
simbolos = ['AL29D', 'GD29D', 'AL30D', 'GD30D', 'AL35D', 'AE38D','AL41D']
url_base = "C:/Users/Adrian/Documents/Adrian/Python/Base de datos/Bd Bonos/bdbonos.db"
camposBase = ['ultimoPrecio','variacion','apertura','maximo','minimo',
                          'fechaHora','cierreAnterior','montoOperado','volumenNominal',
                          'cantidadOperaciones']


# Pide el token y conecta
status = fiol.conect_Iol()

if (status == 200):

     for simbolo in simbolos:
                
            mercado = 'bCBA'
            plazo = 't2'
            
            resp = fiol.iolRequestCotizacionActual(mercado, plazo, simbolo)
                       
            

            if (resp.status_code == 200):
                # pedimos los datos en formato JSON
                api_response = resp.json()
                df_response = pd.json_normalize(data=api_response)
                df_response = df_response[camposBase]
                
                
                db_conexion = sqlite3.connect(url_base)
               
                query_idbono = "select idbono from tbono where ticker = '{}'".format(simbolo)
                
                
                # Busco el id del tiker
                df_idbono = pd.read_sql(query_idbono, db_conexion)
                idbono = df_idbono.iloc[0,0]
                # lo agrego al df
                df_response['idbono'] = idbono
                
                df_response.to_sql("tcotizaciones", con = db_conexion, if_exists='append', index = False)
                
                db_conexion.commit()
                db_conexion.close()
                
            else:
                print('Error al obtener contizaciones de: ' + simbolo)
         
else:
    print ('Error al logearse en la API de IOL')
