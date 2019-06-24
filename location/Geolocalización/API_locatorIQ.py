# coding: utf-8

import requests
import json
import time
import pandas as pandaExport
import datetime


# Initial values
URL = "https://us1.locationiq.com/v1/search.php"
VIEWBOX_GUAYAQUIL = '-79.95912,-2.287573,-79.856351,-2.053362'
KEYS = [
    #Byron
    #'42e21cf0c2eb57',
    #Mauricio
    #'679e8ce7ebef3d',
   # '682ff2322d6870',
  #  'f2453ef379d738',
 #   '28315e9c4f5a69',
    '66f24e7bf9fe3c',
    # GeanCarlo
    '7d3f9e46790faa'
    ]

FILES = [('faltantes.csv',992150),('QUITO.csv',1284051),('CUENCA.csv',218315)]
MAX_RATE = 10000

file_id = open('next_id.txt','r+')
file_origin = open('origin.txt','r+')
file_success = open('success.csv','a')
file_fail = open('fail.csv','a')
file_log = open('log.txt','a')
file_count = open('counter.txt','r+')
counter = int(file_count.read())
id = int(file_id.read())
file_id.seek(0)
file_count.seek(0)
file_count.write(str(counter+1))
file_count.close()
num_origin = int(file_origin.read())
origin,max_ids = FILES[num_origin]
file_origin.seek(0)
print(counter)
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
        'viewbox' = VIEWBOX_GUAYAQUIL,
        'bounded' = 1
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

id=10855
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
        
    
# Update next_id per next_day
if id > max_ids:    
    file_id.write('0')
    file_id.close()
    num_origin+=1
    file_origin.write(str(num_origin))
    file_origin.close()
else:
    file_id.write(str(id))
    file_id.close()
    file_origin.close()
    
file_log.close()
file_success.close()
file_fail.close()

    
    

