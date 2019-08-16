ciudad_x.to_csv("ULocation" + FILE_NAME,header=True,encoding="utf-8",index=False)
data_array =[]
def filter_sucess(finalResult, originData):
    global data_array
    write = open(finalResult,"a")
    read = open(originData, "r")
    for x in read:
        data = x.split(",")
        id = data[3]
        if id not in data_array:
            print(id)
            data_array.append(id)
            data_write = str( data[0]) +"," + str( data[1]) +"," + str( data[2]) 
            write.write(data_write)
    read.close()
    write.close()

CITY="GUAYAQUIL" 

filter_sucess("U1Location"+ CITY +".csv", "ULocation"+ CITY +".csv")
