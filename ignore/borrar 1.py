# -*- coding: utf-8 -*-
"""
Created on Sat Oct 16 12:53:33 2021

@author: Adrian
"""

# from datetime import datetime

# date_string = "21 June, 2018"

# print("date_string =", date_string)
# print("type of date_string =", type(date_string))

# date_object = datetime.strptime(date_string, "%d %B, %Y")

# print("date_object =", date_object)
#print("type of date_object =", type(date_object))



from datetime import datetime

now = datetime.now() # current date and time

print("type of date_string =", type(now))

year = now.strftime("%Y")
print("year:", year)

month = now.strftime("%m")
print("month:", month)

day = now.strftime("%d")
print("day:", day)

time = now.strftime("%H:%M:%S")
print("time:", time)

date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
print("date and time:",date_time)	