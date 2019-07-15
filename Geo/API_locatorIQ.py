# coding: utf-8

import requests
import json
import time
import pandas as pandaExport
import datetime


# Initial values
URL = "https://us1.locationiq.com/v1/search.php"

KEYS = [
    #Byron
    '42e21cf0c2eb57',
    #Mauricio
    '679e8ce7ebef3d',
    '682ff2322d6870',
    'f2453ef379d738',
    '28315e9c4f5a69',
    '66f24e7bf9fe3c',
    # GeanCarlo
    '7d3f9e46790faa'
    ]

FILES = [('GUAYAQUIL.csv',992150),('QUITO.csv',1284051),('CUENCA.csv',218315)]
MAX_RATE = 10000



# load initial data
data = pandaExport.read_csv('GUAYAQUIL.csv',sep=",",encoding ="ISO-8859-1",error_bad_lines=False, skiprows=range(1,200000),nrows=270000)


for i in range(0,70000):
    
    # current row
    row = data.iloc[i]
    
    
    # Time to avoid more than 2 requests per second
    time.sleep(1)
    

    
    

