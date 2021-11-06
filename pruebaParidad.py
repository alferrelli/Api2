# -*- coding: utf-8 -*-
"""
Created on Fri Oct 29 08:24:56 2021

@author: aferrelli
"""

# -- coding: utf-8 --
"""
Created on Fri Oct 29 08:24:56 2021

@author: aferrelli
"""

# -- coding: utf-8 --
"""
Created on Thu Oct 28 14:53:30 2021
@author: Adrian
"""
import sqlite3
import pandas as pd
import calculosBonos as cbiol
from datetime import datetime


simbolo = 'AL29D'
url_base = "C:/Users/Adrian/Documents/Adrian/Python/Base de datos/Bd Bonos/bdbonos.db"
            
db_conexion = sqlite3.connect(url_base)
                
#obtener datos calculo
def get_idbono(simbolo):
    q_idbono = "select idbono from tbono where ticker = '{}'".format(simbolo)
    
    df_idbono=pd.read_sql(q_idbono, db_conexion)
    return df_idbono.iloc[0,0]


def get_tasa(idbono, fechaCalculo):
    
    q_tasa = "select tasa from ttasasbonos where idbono={} and fechadesde<'{}'and fechahasta>='{}'".format(idbono, fechaCalculo, fechaCalculo)
    df_tasa = pd.read_sql(q_tasa, db_conexion)

    return df_tasa.iloc[0,0]


def get_flujo_fondos(idbono):
        # Obtengo el flujo de fondos total del simbolo que busco
        q_flujodefondos = "select tflujodefondos.* from tflujodefondos \
                            	where idbono = '{}'".format(idbono)
        
        
        df_flujofondos = pd.read_sql(q_flujodefondos, db_conexion)
        return df_flujofondos
    
    

def get_valor_residual(df_flujodefondos, fechaCalculo):
 
    # Saco el flujo de fondos desde el inicio hasta la fecha de calculo
    df_flujopagado = df_flujofondos[df_flujofondos['fecha']<fechaCalculo]
    v = 100 - df_flujopagado['amortizacion'].sum()
    return v


def get_precio(idbono, fechaCalculo):
    
    q_precio = "select * from tcotizaciones where idbono= {} and fechaHora = '{}' ".format(idbono,fechaCalculo)
    df_precio = pd.read_sql(q_precio, db_conexion)
    precio = df_precio.loc[0,'ultimoPrecio']
    return precio

def get_fecha_emision(idbono):
    q_emision = "select * from tbono where idbono= {}".format(idbono)
    df_emision = pd.read_sql(q_emision, db_conexion)
    femision = df_emision.loc[0,'femision']
    return femision

def set_paridad(fecha,idbono,valor_paridad):
    
    df = pd.DataFrame(columns=('fecha', 'idbono', 'idindicador', 'valorindicador'))
    df.loc[len(df)]=['2021-10-22',1,1,0.5] 
    df.to_sql('tindicadoresbonos', db_conexion, if_exists='append',index=False)



## Programa principal


df_cotizaciones = pd.read_sql("select * from tcotizaciones order by fechaHora", db_conexion)
fila = 0
for fecha in df_cotizaciones['fechaHora']:


    fechaCalculo = fecha

    idbono = df_cotizaciones.loc[fila,'idbono']
    df_flujofondos = get_flujo_fondos(idbono)
    valor_residual = get_valor_residual(df_flujofondos, fechaCalculo)
    
    
    # Obtengo el periodo de fechas menor que el de la fecha de calculo
    # y de ese periodo el ultimo, que seria la fecha de ultimo pago
    
    df_ultimos_pagos = df_flujofondos[df_flujofondos['fecha'] < fechaCalculo]
    if df_ultimos_pagos.empty:
        # si entra aca es porque aun no pago renta, voy a la fecha de emision
        # como inicio del calculo de intereses, paridad, etc
        fechaUltimoPago = get_fecha_emision(idbono)
    else:   
        fechaUltimoPago = df_ultimos_pagos.iloc[-1,2]
    
    
    
    fechaD = datetime.strptime(fechaUltimoPago, "%Y-%m-%d")
    fechaH = datetime.strptime(fechaCalculo, "%Y-%m-%d")
    
    
    precio = df_cotizaciones.loc[fila,'ultimoPrecio']
    tasa = get_tasa(idbono, fechaCalculo)
    
    paridad = cbiol.calcularParidad(fechaD,fechaH,precio,valor_residual,tasa)
    fila = fila + 1
    # Guardo el valor de paridad en la BD
    set_paridad(fechaH, idbono, paridad)

# db_conexion.commit()
# db_conexion.close()