# -*- coding: utf-8 -*-
"""
Created on Sat Sep 25 18:54:59 2021

@author: Adrian
"""

import pandas as pd

df = pd.read_json("gd30.json")


df=df[['fechaHora','ultimoPrecio']]

df['fechaHora']=  pd.to_datetime(df['fechaHora']).dt.strftime("%d/%m/%Y")

df.to_excel("gd30d.xlsx",index=False)