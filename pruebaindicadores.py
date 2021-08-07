# -*- coding: utf-8 -*-
"""
Created on Thu Jul  1 11:30:22 2021

@author: aferrelli
"""
import pandas as pd
import calculosBonos as cb

# d1= pd.to_datetime("30/01/2021", format='%d/%m/%Y')
# d2= pd.to_datetime("01/02/2020", format="%d/%m/%Y")





# d = cb.calcularInteresCorrido(fechad, fechah, 1, 360)

# print(d)


d1 = pd.to_datetime("04/09/2020", format='%d/%m/%Y')
d2 = pd.to_datetime("9/7/2021", format='%d/%m/%Y')

d = cb.days360(d1, d2)
interescorrido = round(cb.calcularInteresCorrido(d1, d2, 1, 360),4)

valorresidual = 100
precio = 36.50
tasa = 1
paridad = round(cb.calcularParidad(d1, d2, precio, valorresidual, tasa), 2)