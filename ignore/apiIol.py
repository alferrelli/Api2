# -*- coding: utf-8 -*-
"""
Created on Thu Jul  8 15:50:13 2021

@author: aferrelli
"""

import requests
import pandas as pd

username = 'kempestw'
password= 'halcon148'
grant_type = 'password'

# Datos para pedir el token
data = {
  'grant_type': grant_type,
  'username': username,
  'password': password
}

response_auth = requests.post('https://api.invertironline.com/token', data=data, verify=True)

if (response_auth.status_code == 200):
                json_data = response_auth.json()
                
                #aca tengo los dos tokens que necesito
                access_token = json_data['access_token']
                refresh_token = json_data['refresh_token']
                
                headers = {'Authorization': 'Bearer ' + access_token}
                
                # pongo los parametros para pedir precio de un tiulo
                # /api/v2/{Mercado}/Titulos/{Simbolo}/Cotizacion
                simbolo = 'AL29D'
                
                mercado = 'bCBA'
                plazo ='t2'
                
                parametros = {
                    'simbolo': simbolo,
                    'mercado': mercado,
                    'model.simbolo': simbolo,
                    'model.mercado': mercado,
                    'model.plazo' : plazo
                    }
                
                
                # Hacemos un Get Request con el Encabezado, que contiene el token de acceso
                # y los parametros de busqueda
                # devuelve el precio actual y fecha (lo que a mi me importa) entre otras cosas
                response = requests.get('https://api.invertironline.com/api/v2/{Mercado}/Titulos/{Simbolo}/Cotizacion',                                                
                                        headers=headers,
                                        params=parametros, 
                                        verify=True)
                if (response.status_code == 200):
                        #pedimos los datos en formato JSON
                        api_response = response.json()
                        
                        df_response = pd.json_normalize(data=api_response)
                        datosUtiles = df_response[['ultimoPrecio','fechaHora']]
                        datosUtiles = datosUtiles.append(df_response['montoOperado'])
                        print (datosUtiles)
                else :
                        print ('Error al obtener contizaciones')
else:   
    print ('Error al logearse')