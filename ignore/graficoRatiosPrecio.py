# -*- coding: utf-8 -*-
"""
Created on Thu Sep 30 17:19:55 2021

@author: Adrian
"""

import pandas as pd

import matplotlib.pyplot as plt 

wb = pd.read_excel('Bonos en dolares.xlsm',
                   sheet_name="Paridad usd",
                   engine="openpyxl")




fig, ax = plt.subplots(figsize=(11,6))


wb['Fecha']=pd.to_datetime(
      wb["Fecha"]
     ).dt.strftime("%Y/%m/%d")

wb.sort_values(by=['Fecha'], ascending=True, inplace=True)

media = (wb['GD30D']/wb['AL30D']).mean()
desvio = (wb['GD30D']/wb['AL30D']).std()
masdesvio = media + desvio
menosdesvio = media - desvio

masdosdesvio = media + (2*desvio)
menosdosdesvio = sdosdesvio = media - (2*desvio)


plt.axhline(y=media,color='r')
plt.axhline(y=masdesvio,color='b')
plt.axhline(y=menosdesvio,color='b')


plt.axhline(y=masdosdesvio,color='b')
plt.axhline(y=menosdosdesvio,color='b')



plt.plot(wb['Fecha'],(wb['GD30D']/wb['AL30D']))


plt.show()
