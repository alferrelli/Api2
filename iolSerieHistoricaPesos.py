# -*- coding: utf-8 -*-
"""
Created on Sun Oct 24 16:17:51 2021

@author: Adrian
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Sep 15 20:48:03 2021

Opbtengo la cotizacion historica segun fechaDesde y fechaHasta de un conjunto de simbolos
utilizando la API de Iol

@author: Adrian
"""

import pandas as pd
import funcionesIol as fiol
import sqlite3




# de estos tickers voy a pedir la cotizacion
simbolos = ['AL29','GD29', 'AL30', 'GD30', 'AL35', 'AE38','AL41']
url_base = "C:/Users/Adrian/Documents/Adrian/Python/Base de datos/Bd Bonos/bdbonosPesos.db"
camposBase = ['ultimoPrecio','variacion','apertura','maximo','minimo',
                          'fechaHora','cierreAnterior','montoOperado','volumenNominal',
                          'cantidadOperaciones']
mercado = 'bCBA'
plazo = 't2'
fechaDesde =  pd.to_datetime('2020-09-01')
fechaHasta = pd.to_datetime('2021-11-01')
response_auth = fiol.pedir_token()

# Pide el token y conecta
status = fiol.conect_Iol()
guardoEnExcel=True

if (status == 200):
    
    for simbolo in simbolos:
        resp = fiol.iolRequestCotizacionHistorica(mercado, plazo, simbolo,fechaDesde, fechaHasta)
    
        if (resp.status_code == 200):       
            # pedimos los datos en formato JSON
                api_response = resp.json()
                df_response = pd.json_normalize(data=api_response)
                df_response = df_response[camposBase]
                
                
                db_conexion = sqlite3.connect(url_base)
                
                query_idbono = "select idbono from tbono where ticker = '{}'".format(simbolo)
                
                # Busco el id del tiker
                df_idbono = pd.read_sql(query_idbono, db_conexion)
                # lo agrego al df
                idbono = df_idbono.iloc[0,0]
                
                df_response['fechaHora'] = pd.to_datetime(df_response["fechaHora"], infer_datetime_format=True)
                df_response['fechaHora']=df_response['fechaHora'].apply(lambda x : x.date())
                
                
                df_response['idbono'] = idbono

                if guardoEnExcel==True:
                    writer=pd.ExcelWriter("Bonos Pesos.xlsx")
                    df_response.to_excel(writer, sheet_name='Bonos',index=False,engine='xlsxwriter')
                
                df_response.to_sql("tcotizaciones", con = db_conexion, if_exists='append', index = False)
                
                db_conexion.commit()
                db_conexion.close()
                
        else:
                print('Error al obtener contizaciones de: ' + simbolo)
         
else:
    print ('Error al logearse en la API de IOL')
    