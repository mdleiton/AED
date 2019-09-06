# script que obtiene los tweets.se ejecuta 3 veces por cada ciudad(cada una con token de usuario diferente)
from __future__ import absolute_import, print_function
import sys
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import datetime
import syslog
import os

class TweetsListener(StreamListener):
    fecha = ""
    contador = 0
    file = 0
    path = ""
    
    def on_data(self, data):
        json_file = []
        fecha = str(datetime.datetime.now()).split(" ")[0]
        if not os.path.exists(self.path + fecha):
            os.mkdir(self.path + fecha)
        if self.contador > 200:
            self.file = self.file + 1
            self.contador = 0
            self.fecha = self.path + fecha + "/" + fecha + str(self.file) +".json"
            if not os.path.exists(self.fecha):
                data_ = {"data":[]}
                with open(self.fecha, 'w') as outfile:  
                    json.dump(data_, outfile,indent=4)  
        tweet = json.loads(data)
        with open(self.fecha) as f:
            json_file = json.load(f)
            json_file["data"].append(tweet)
        with open(self.fecha, 'w') as f:
            json.dump(json_file, f, indent=4)
        self.contador = self.contador + 1
        #syslog.syslog('tweets:' + str(tweet['text']))
        return True

    def on_error(self, status):
        syslog.syslog('tweets:' + str(status))
        sys.exit()

if __name__ == '__main__':
    args = sys.argv
    if not os.path.exists(args[1]):
        os.mkdir(args[1])
    if not os.path.exists(args[1] + "/" + str(datetime.datetime.now()).split(" ")[0]):
        os.mkdir(args[1] + "/" + str(datetime.datetime.now()).split(" ")[0])
    json_file = {}
    with open("conf_twitter.json") as f:
        json_file = json.load(f)
    coordenadas = json_file[args[1]]["coordenadas"]
    l = TweetsListener()
    l.path = args[1] + "/"
    l.file = 1
    l.contador = 0
    path_ = str(datetime.datetime.now()).split(" ")[0]
    l.fecha = l.path + path_ + "/" +  path_ + str(l.file) +".json"
    if not os.path.exists(l.fecha):
        data = {"data":[]}
        with open(l.fecha, 'w') as outfile:  
            json.dump(data, outfile, indent=4)
    auth = OAuthHandler(json_file[args[1]]["token"]["consumer_key"], json_file[args[1]]["token"]["consumer_secret"])
    auth.set_access_token(json_file[args[1]]["token"]["key"], json_file[args[1]]["token"]["secret"])
    stream = Stream(auth, l)
    stream.filter(locations=coordenadas)
