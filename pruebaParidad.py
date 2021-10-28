# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 14:53:30 2021

@author: Adrian
"""

# Public Function myParidad(fecha1 As Date, fecha2 As Date, precio As Double, valorResidual As Double, tasa As Double) '(fecha ultimo pago, fecha calculo, precio, valor residual, tasa int)
# Dim p As Double
# Dim ic As Double
    
#     ic = interesesCorridos(fecha1, fecha2, tasa)
#     p = precio / (valorResidual + ic)
  

# myParidad = p
# End Function

import sqlite3
import pandas as pd
import calculosBonos as cbiol
from datetime import datetime


simbolo = 'AL29D'
url_base = "C:/Users/Adrian/Documents/Adrian/Python/Base de datos/Bd Bonos/bdbonos.db"

db_conexion = sqlite3.connect(url_base)
                

fechaCalculo = "2021-8-27 00:00:00"

query_idbono = "select * from tflujodefondos \
                WHERE idbono = 1 and \
                fecha < '{}' order by fecha desc \
                limit 1".format(fechaCalculo)
df_flujofondos = pd.read_sql(query_idbono, db_conexion)

fechaDesde = df_flujofondos.iloc[0,2]
fechaHasta = fechaCalculo

fechaD = datetime.strptime(fechaDesde, "%Y-%m-%d 00:00:00")
fechaH = datetime.strptime(fechaHasta, "%Y-%m-%d 00:00:00")


valor_residual = 100
precio = 36.70
tasa = 0.5

paridad = cbiol.calcularParidad(fechaD,fechaH,precio,valor_residual,tasa)