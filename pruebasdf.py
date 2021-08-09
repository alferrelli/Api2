# -*- coding: utf-8 -*-
"""
Created on Sun Aug  8 19:54:11 2021

@author: Adrian
"""

import pandas as pd

al29 = [['2021-08-06T17:00:11.833', 35.40]]
al30 = [['2021-08-06T17:00:11.833', 40.40]]


df1 = pd.DataFrame(al29, columns=('Fecha', 'Precio'))
df2 = pd.DataFrame(al30, columns=('Fecha', 'Precio'))



micolumna = df1['Precio']


df2 = df2.append(df1)


print (df2.index[0])

df2.to_excel('kk.xlsx')
df1.to_excel('kk21.xlsx')

