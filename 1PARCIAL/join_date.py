import sys
import json
import datetime
import syslog
import os
data = {}
for r, d, f in os.walk("../quito/"):
    for file in f:
        if '.json' in file:
            if file[:10] not in data:
                data[file[:10]] = []
            with open(os.path.join(r, file)) as json_f:
                json_file = json.load(json_f)
            data[file[:10]] = data[file[:10]] + json_file["data"]
total = 0
for k, v in data.items():
    with open(k + ".json", 'w') as outfile:  
        json.dump({"data":v}, outfile, indent=4)
    cantidad = len(v)
    total = total + cantidad
    print("final guardado: " + k + " tamano: " + str(cantidad))
print("total: " + str(total))
#cuenca: 58522
#guayaquil: 197486
#quito 140265
#total 396273
