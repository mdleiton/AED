#concatena dos archivos con informacion de geolocalizacion obtenidos del API de LocationIQ. Verifica duplicados
import csv
import pandas as pandaExport
import numpy as np
data_array =[]
def filter_sucess(finalResult, originData, i):
    write = open(finalResult,"a")
    read = open(originData, "r")
    for x in read:
        data = x.split(",")
        log = data[-1]
        lat = data[-2]
        id = data[i]
        if len(id) > 10:
            id = data[i-1]
        if id not in data_array:
            data_array.append(id)
            data_write = str(id) +"," + str(lat) +"," + str(log) 
            write.write(data_write)
    read.close()
    write.close()

CITY="CUENCA" 
filter_sucess("Location"+ CITY +".csv", "success_cuenca.csv", 0)