# -*- coding: utf-8 -*-
"""
Created on Wed Sep 15 20:48:03 2021

Opbtengo la cotizacion historica segun fechaDesde y fechaHasta de un determinado simbolo. ej gd30d
utilizando la API de Iol

@author: Adrian
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
        
        fechaDesde =  pd.to_datetime('2021-10-22')
        fechaHasta = pd.to_datetime('2021-10-23')
        ajustada = 'sinAjustar'
        mercado='bCBA'
        simbolo='GD30D'
        
        parametros = {
                'mercado': mercado,    
                'simbolo': simbolo,
                'fechaDesde': fechaDesde,
                'fechaHasta': fechaHasta,
                'ajustada': ajustada 
            }
        response = requests.get('https://api.invertironline.com/api/v2/{mercado}/Titulos/{simbolo}/Cotizacion/seriehistorica/{fechaDesde}/{fechaHasta}/{ajustada',
                                     headers=headers,
                                     params=parametros,
                                     verify=True)
            
        if (response.status_code == 200):
                # pedimos los datos en formato JSON
                api_response = response.json()
                df_response = pd.json_normalize(data=api_response)
                respuesta = df_response[['fechaHora','ultimoPrecio']]
                
                respuesta.to_excel('historicoGD30D.xls', index=False)
        else:
                print('Error al obtener contizaciones de: ' + str( response.status_code))
    
                
     