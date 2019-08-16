# coding: utf-8

import requests
import json
import time
import pandas as pandaExport
import datetime


# Initial values
URL = "https://us1.locationiq.com/v1/search.php"

KEYS = [
"4fdda333d431f6",
"85e253a9703278",
"f1fee08f51d685",
"c9c8998bcff6f1",
"9c9dd37184575f"
    ]

FILES = [('finalMayorIgual3_1QUITO.csv',992150),('QUITO.csv',1284051),('CUENCA.csv',218315)]
MAX_RATE = 10000

file_success = open('success.csv','a')
file_fail = open('fail.csv','a')
file_log = open('log.txt','a')
id = 0
origin,max_ids = FILES[0]
VIEWBOX_QUITO = '-78.619545,-0.365889,-78.441315,-0.047208'
# load initial data
data = pandaExport.read_csv(origin,sep=",",encoding ="UTF-8",error_bad_lines=False)

def create_query(row):
    query = ''
    if row.loc['DESCRIPCION_PROVINCIA']:
        query += row.loc['DESCRIPCION_PROVINCIA']
    if row.loc['DESCRIPCION_CANTON']:
        query += ', '+row.loc['DESCRIPCION_CANTON']
    if row.loc['DESCRIPCION_PARROQUIA']:
        query += ', '+row.loc['DESCRIPCION_PARROQUIA']
    if str(row.loc['CALLE']) != 'S/N':
        query += ', '+str(row.loc['CALLE'])
    if str(row.loc['INTERSECCION']) != 'S/N':
        query += ' y '+str(row.loc['INTERSECCION'])
    return query

def get_response(key,query):
    data = {
        'key':key,
        'q': query,
        'format': 'json',
        'viewbox' :VIEWBOX_QUITO,
        'bounded' : 1
    }
    return requests.get(URL, params=data)


def create_error_log(row,status):
    dat = row.tolist()
    dat.append(status)
    return ','.join(str(x) for x in dat)+'\n'


def create_success_log(response,row):
    dat = row.tolist()
    j_response = json.loads(response.text).pop()
    lat = j_response.get('lat')
    lon = j_response.get('lon')
    dat.append(lat)
    dat.append(lon)
    return ','.join(str(x) for x in dat)+'\n'
id = 27981
for i in range(0,MAX_RATE*len(KEYS)):
    
    # current row
    row = data.iloc[id]
    
    # Key selection
    key = KEYS[i // MAX_RATE]
    
    # Query format
    try:
        query = create_query(row)
    except:
        print("An exception occurred")
        error = create_error_log(row,1000)
        file_fail.write(error) 
        id+=1
        continue
    # Request and json response
    response = get_response(key,query)
    
    # validate response
    type = ''
    if response.status_code == 200:
        # Success
        success = create_success_log(response,row)
        file_success.write(success)
        type = 'ok'
    else:
        # Error
        error = create_error_log(row,response.status_code)
        file_fail.write(error)
        type = 'error'

    # Log file
    log_message = str(datetime.datetime.now())+' | '+key+' | Iteration '+str(i)+' | '+type+' \n'
    file_log.write(log_message)
    
    # Time to avoid more than 2 requests per second
    time.sleep(0.7)
    
    # Next id
    id += 1
    if id > max_ids:
        file_log.write('-------------------------End file----------------------')
        break

else:
    file_id.write(str(id))
    file_id.close()
    file_origin.close()
    
file_log.close()
file_success.close()
file_fail.close()


    
    

