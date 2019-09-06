#!iApp/views.py
from django.shortcuts import render
from keras.models import model_from_json
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras import backend as K
import tweepy as tw
from sentic import SenticPhrase
import requests, json
from dateutil import tz
import numpy as np
from textblob import TextBlob
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
from sklearn import feature_extraction
import nltk
import matplotlib.pyplot as plt
from sklearn import preprocessing
from scipy import sparse
from sklearn import linear_model
import tensorflow as tf
import keras

auth=tw.OAuthHandler("LLENAR CON TUS CREDENTIALES DE TWITTER. TOKENS","LLENAR CON TUS CREDENTIALES DE TWITTER. TOKENS")
auth.set_access_token("LLENAR CON TUS CREDENTIALES DE TWITTER. TOKENS","LLENAR CON TUS CREDENTIALES DE TWITTER. TOKENS")
api = tw.API(auth)

# Tweepy api credentials config
def getxy(row_s, row_f, feature_cols=['content',"sin_stopwords", 'followers', 'following', 'retweet',"n_mentioned","n_hashtags"], label_col=['troll']):
    return df[feature_cols][row_s:row_f], df[label_col][row_s:row_f]

df = pd.read_csv('alldataset_sentimental.csv', sep=",", encoding='utf-8')
df = df[['content',"sin_stopwords", 'followers', 'following', 'retweet',"n_mentioned","n_hashtags","troll"]].dropna()
users_copy = df[df["troll"] == False].copy()
trolls_copy =  df[df["troll"] == True].copy()

X_train, y_train = getxy(0,299802)
X_test, y_test = getxy(299803,316119)

stopwords_set = stopwords.words('spanish')
stopwords_set.extend(stopwords.words('english'))
stopwords_set = set(stopwords_set)
vocab_size=5000
tokenizer=feature_extraction.text.CountVectorizer(stop_words=stopwords_set, max_features=vocab_size)
tokenizer=tokenizer.fit(df['sin_stopwords'])

bool_to_bin = lambda x: 1 if x else 0
y_train['troll'] = y_train['troll'].apply(bool_to_bin)
y_test['troll'] = y_test['troll'].apply(bool_to_bin)

# binarize retweet colum
X_train['retweet'] = X_train['retweet'].apply(bool_to_bin)
X_test['retweet'] = X_test['retweet'].apply(bool_to_bin)

X_train_tok=tokenizer.transform(X_train['content'])
X_test_tok=tokenizer.transform(X_test['content'])

scaler = preprocessing.StandardScaler().fit(X_train[['followers','following',"n_mentioned","n_hashtags"]])

col_to_std = ['followers', 'following',"n_mentioned","n_hashtags"]
X_train[col_to_std]=scaler.transform(X_train[col_to_std])
X_test[col_to_std]=scaler.transform(X_test[col_to_std])

def concatenate_features(tok_matrix, data_df):
    """ concatenate the tokenized matrix (scipy.sparse) with other features """
    sparse_cols = sparse.csr_matrix(data_df[['followers', 'following', 'retweet',"n_mentioned","n_hashtags"]])
    combined = sparse.hstack([tok_matrix, sparse_cols])
    return combined

X_train_combined = concatenate_features(X_train_tok, X_train)
X_test_combined = concatenate_features(X_test_tok, X_test)

def tweets(user):
    global api, tokenizer, scaler_training, scaler
    result = []
    try:
        for status in tw.Cursor(api.user_timeline, screen_name=user.strip("\n"), tweet_mode="extended").items(50):
            tweet = status.full_text
            name = "modelLSTM"
            json_file = open('iApp/'+ name + '.json', 'r')
            loaded_model_json = json_file.read()
            json_file.close()
            loaded_model = model_from_json(loaded_model_json)
            loaded_model._make_predict_function()
            loaded_model.load_weights("iApp/" + name + ".h5")
            mini_df = {}
            mini_df['content'] = [str(tweet)]
            mini_df['followers'] = [int(status.user.followers_count)]
            mini_df['following'] = [int(status.user.friends_count)]
            mini_df['retweet'] = [1 if status.retweeted else 0]
            mini_df["polarity"] = [TextBlob(str(tweet)).sentiment.polarity]
            user_mentioned = ';'.join(i['screen_name'] for i in status.entities["user_mentions"])
            hashtags = ';'.join(i['text'] for i in status.entities["hashtags"])
            mini_df["n_mentioned"] = [len(user_mentioned)]
            mini_df["n_hashtags"] = [len(hashtags)]
            mini_df = pd.DataFrame.from_dict(mini_df)
            tweet_tok=tokenizer.transform(mini_df['content']) 
            mini_df[col_to_std]=scaler.transform(mini_df[col_to_std])  # normalize followers/following
            mini_df_combined = concatenate_features(tweet_tok, mini_df)
            mini_df_numpy_vector = mini_df_combined.todense()
            pred = loaded_model.predict(mini_df_numpy_vector)
            K.clear_session()
            result.append(pred[0])
        promedio = np.mean(result)
        print(promedio)
        data = {}
        if promedio >= 0.73:
            data = {"data": user, "result": "troll"}
        else:
            data = {"data": user, "result": "No eres troll"}
        return data    
    except:
        data = {"data": user, "result": "No existe dicho usuario"}
        return data    

def clasificador(request):
    """View para clasificar un texto"""
    if request.method == 'POST':
        user = request.POST["data"]
        data = tweets(user)
        return render(request, "clasificador.html", data)
    return render(request, "clasificador.html",)
