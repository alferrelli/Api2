# -*- coding: utf-8 -*-
"""
Created on Fri Sep 24 19:34:16 2021

@author: Adrian
"""
import requests

username = 'kempestw'
password= 'halcon148'
grant_type = 'password'

data = {
  'grant_type': grant_type,
  'username': username,
  'password': password
}

headers = {'Authorization': 'Bearer ' }

def pedir_token():
    
    token = requests.post('https://api.invertironline.com/token', data=data, verify=True)
    return token


# pido el token y me conecto
def conect_Iol():
    
    response_auth = pedir_token()
    if (response_auth.status_code == 200):
        json_data = response_auth.json()

        #aca tengo los dos tokens que necesito
        access_token = json_data['access_token']
        refresh_token = json_data['refresh_token']
        headers.update({'Authorization': 'Bearer ' + access_token})
        

    return response_auth.status_code


def iolRequestCotizacionActual(m, p,s):
        parametros = {
                        'simbolo': s,
                        'mercado': m,
                        'model.simbolo': s,
                        'model.mercado': m,
                        'model.plazo': p
                      }
      
    
        response = requests.get('https://api.invertironline.com/api/v2/{Mercado}/Titulos/{Simbolo}/Cotizacion',
                                     headers=headers,
                                     params=parametros,
                                     verify=True)
        return response
    
def iolRequestCotizacionHistorica(m, p, s,fd, fh):
    parametros = {
                'mercado': m,    
                'simbolo': s,
                'fechaDesde': fd,
                'fechaHasta': fh,
                'ajustada': 'sinAjustar' 
            }
    response = requests.get('https://api.invertironline.com/api/v2/{mercado}/Titulos/{simbolo}/Cotizacion/seriehistorica/{fechaDesde}/{fechaHasta}/{ajustada',
                                     headers=headers,
                                     params=parametros,
                                     verify=True)
    return response