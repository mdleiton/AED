# script que recibe un csv con los datos de establecimientos y genera un grafo
import csv
import pandas as pandaExport
import numpy as np
TIPO = "ABIERTOS"
CIUDADES = ['GUAYAQUIL.csv', "CUENCA.csv", "QUITO.csv"]
FILE_NAME = CIUDADES[2]
valido = pandaExport.read_csv('actualizado'+TIPO + FILE_NAME,sep=",",encoding ="utf-8",error_bad_lines=False)
valido = valido.sort_values(by=["NUMERO_RUC","NUMERO_ESTABLECIMIENTO"],ascending=[True,True])

factor = pandaExport.read_csv("factorNormalizacion" + FILE_NAME, sep=",",encoding ="utf-8",error_bad_lines=False)
prev_ruc = None
prev_id = None
prev_parroquia = None
contador = 0

def get_factor(parroquia):
    for index, row in factor.iterrows():
        if row["DESCRIPCION_PARROQUIA"] == parroquia:
            return row["FACTOR"]

def validar(row):
    global prev_ruc, prev_id, prev_parroquia, contador
    if prev_ruc != row["NUMERO_RUC"]:
        if prev_ruc:
            row["origin"] = None
        prev_ruc = row["NUMERO_RUC"]
        prev_id = int(row["ID"])
        prev_parroquia = row["DESCRIPCION_PARROQUIA"]
        contador = 0
    else:
        if prev_id!= int(row["ID"]):
            row["origin"] = prev_id
            row["origin_p"] = prev_parroquia
            row["peso"] = get_factor(row["DESCRIPCION_PARROQUIA"])
            prev_id = int(row["ID"])
            contador += 1
            row["secuencia"] = contador
    return row
    
valido = valido.apply(validar, axis=1)
valido = valido[valido["origin"].notnull()]
valido = valido[valido["origin"]!=valido["ID"]]
valido["origin"] = valido["origin"].astype(int)
valido.to_csv("grafo"+TIPO+ FILE_NAME,header=True,encoding="utf-8",index=False)