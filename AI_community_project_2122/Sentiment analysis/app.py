import string
import re
import pickle
from flask import Flask
import requests
from ast import literal_eval
from flask import send_file, request
from flask_cors import CORS
#import tensorflow as tf
import keras
from keras.models import load_model
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras import Sequential
from keras.layers import Embedding
import numpy as np
import re




model = load_model('./model.h5')

class sentiment():
    def stop_words_remove(self,sentences):
        list = []
        for text in sentences:
            clean_1 = " ".join([w for w in text.lower().split() if w not in my_stopwords])
            list.append(clean_1)
        return list
    def clean_text(self,sentences):
        list = []
        data = self.stop_words_remove(sentences)
        for text in data:
            clean_1 = re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z\t])|(\w+:\/\/\S+)"," ",text)
            list.append(clean_1)
        return list
    def encoding(self,sentences):
        tokenizer = Tokenizer()
        training_sentences = self.clean_text(sentences)
        tokenizer.fit_on_texts(training_sentences)
        word_index = tokenizer.word_index
        training_sequences = tokenizer.texts_to_sequences(training_sentences)
        training_padded = pad_sequences(training_sequences,padding = "post")
        return training_padded
    def score(self,sentences,model):
      padded = self.encoding(sentences)
      sent = model.predict(padded)
      data = []
      for i in range(len(sentences)):
        value = []
        if sent[[i]] <= 0.5:
          value.append(sentences[i])
          value.append(sent[[i]])
          value.append("positive")
        elif sent[[i]] > 0.7 :
          value.append(sentences[i])
          value.append(sent[[i]])
          value.append("negative")
        else:
          value.append(sentences[i])
          value.append(sent[[i]])
          value.append("neutral")

        data.append(value)
      return data
obj = sentiment()
#result = obj.score(sentences,model)



app = Flask(__name__)
CORS(app)



my_stopwords = ["aaj","aap","aapne","aata","aati","aaya","aaye","ab","abbe","abbey","abe","abhi","aisa","aise","aisi","andar","apan","apnaa","apne","apni","are","aur",
              "arre","aya","baar","bas","batao","banaya","banaye", "banayi","bhi","bola","bole","boli","bolo","bolta","bolte","bolti","chal","chalega","chahiye","dega",
               "degi","dekh","dekha","dekhe","dekhi","dekho","denge","dijiye","diya","diyaa","diye","dono","doosra", "dusra","dusre","dusri","dvaara","dvara", "dwaara",
                "dwara","ek","fir","gaya","gaye","gayi","hamara","hai","hamare","hamari","hamne","har","hoga","hm","hmm","hogi","hona","honaa","hone","honge","hongi",
                "hota","hotaa","hote","hoti","hoyenge","hua","hue","hui","hum","humne","humara","humara","humari","huye","huyi"," inhe","inhi","inho","inka","inkaa","inke",
                "inki","is","ise","iski","iska","isse","iske","isme","isne","itna","itne","itni","ityadi","ityaadi","jab","jahaan","jahan","jaha","jaise","jaisa","jaisi",
                "jidhar","jin","jinhe","jinhi","jinhone","jinka","jinki","jinke","jiska","jiski","jiski","jise","jisse","jisme","jitna","jitne","jitni","jo","ka","ki","k",
                "ko","kab","kyu","kaun","kabhi","kaha","kahaa","kahi","kahin","kaise","kaisa","kaisi","kar","kara","kare","karke","karna","karni","karo","karta","karte",
                "karti","karu","karun","kaunsa","kinhe","kitna","kinka","kinko","kise","kitne","kitni","kisliye", "koi","kuch","kuchh","kya","kyaa","kyuki","kyunki","lekin",
                "magar","mai","main","maine","mera","meri", "mere","mereko","mujhe","oh","phla","phle","phli","pahle","pahli","pura","puri","sabhi","sabse", "sabne","sabka",
                "sabko","sabne","sabka","sabse","sabko","tera","teri","tere","tereko","tumko","tumne","tumhara","tumhari","tumse","tumlog","tumhare","tune","unka","unki","unko",
               "unke","unse","usne","usse","uska","vahi","vaisa","vaisi","waisa","waise","wale","wha","whan","wahi","wahan","waisa","wo","whi","yadi","yaha","yha","yhan","ye",
               "pahla","ne","ke","hi","he","arey","thi","yeh","h","bahut",'i', 'me', 'my', 'myself', 'we', 'our',"yahan", 'ours', 'ourselves', 'you', "you're", "you've",
                "you'll","you'd", 'your', 'yours', 'yourself','yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its',
                'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that',"that'll", 'these', 'those', 'am', 'is', 'are', 'was',
                 'were', 'be', 'been', 'being', 'have', 'has', 'had','having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as',
                 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through','until', 'while', 'of', 'at','during', 'before', 'after', 'above', 'below', 'to',
                'up', 'down', 'in', 'out', 'on', 'off', 'over','under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any',
                'from' 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just',
                 'don', "don't", 'should', "should've", 'now','d', 'll', 'm', 'o', 're', 've', 'y','needn','shan',]



@app.route('/sentiment/v1/analyze', methods=["POST"])
def get_senti():
    data = eval(request.data.decode())
    data_list = [item["text"] for item in data["data"]]
    result = obj.score(data_list,model)
    for i in range(len(result)):
        data["data"][i]['score'] = float(result[i][1][0][0])
        data["data"][i]['sentiment'] = result[i][2]

    return data

@app.route('/')
def getStatus():
    return "<p>{Status: 1}</p>"


if __name__ == "__main__":
    print("[root]: starting app")
    app.run(debug=False, host='0.0.0.0')
