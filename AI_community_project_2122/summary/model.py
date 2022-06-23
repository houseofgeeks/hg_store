import pandas as pd
import numpy as np
import nltk
import string
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import PunktSentenceTokenizer
import re
import joblib
import gensim
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from gensim.models import Word2Vec
from gensim.models import KeyedVectors
import pickle
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix
from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score
from tqdm import tqdm
import os

class text_summarization:
    def __init__(self,text,stop_words=None):
        
        self.text = text
        
#         self.Kmeans_cluster = KMeans(n_clusters=10)
        self.Kmeans_cluster = None
        
        self.required_sentences = None 
        
        self.sentences = None
        
        self.punk = PunktSentenceTokenizer()
        
        self.st = PorterStemmer()
        
        self.tf_idf_vect = TfidfVectorizer(min_df = 2)
        
        if stop_words == None:
            
            self.stop_words = set(['br', 'the', 'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've",\
            "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', \
            'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their',\
            'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', \
            'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', \
            'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', \
            'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after',\
            'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further',\
            'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more',\
            'most', 'other', 'some', 'such', 'only', 'own', 'same', 'so', 'than', 'too', 'very', \
            's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', \
            've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn',\
            "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn',\
            "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", \
            'won', "won't", 'wouldn', "wouldn't"])
        else:
            
            self.stop_words = stop_words
            
            
            
            
            
    def cleanhtml(self,sentence):
        
        clean_text = ""
        
        cleanr = re.compile('<.*?>')
        
        clean_text = (re.sub(cleanr,' ',sentence))
        
        return clean_text
    
    
    def remove_stopwords(self,text):
        filtered_text = ""
        
        filtered_words = [word for word in nltk.word_tokenize(text) if word not in self.stop_words and word.isalpha()]
        
        filtered_text = ' '.join(filtered_words)
        
        return filtered_text
    
    
    
    def remove_special_characters(self,text):
        filtered_text = ""
        
        pattern = re.compile('[{}]'.format(re.escape(string.punctuation)))
        
        filtered_tokens = filter(None, [pattern.sub('', word) for word in nltk.word_tokenize(text)])
        
        filtered_text = ' '.join(filtered_tokens)
        
        return filtered_text
    
    
    
    def stemming_words(self,sentence):
        words_stemming = []
        
        word_tokens = word_tokenize(sentence)
        
        word_tokens = map(lambda k: self.st.stem(k), word_tokens)
        
        words_stemming.append(' '.join(word_tokens))
        
        return words_stemming[0]
    
    
    
    
    def normalize_corpus(self):
        normalized_text =[]
        
        if(isinstance(self.sentences,list)):
            
            for sentence in self.sentences:
                
                sentence = self.cleanhtml(sentence)
                
                sentence = self.remove_stopwords(sentence)
                
                sentence = self.stemming_words(sentence)
                
                sentence = self.remove_special_characters(sentence)
                
                normalized_text.append(sentence)
                
            return normalized_text
        else:
            text = self.remove_stopwords(text)
            
            text = self.stemming_words(text)
            
            text = self.remove_special_characters(text)
            
            return text
        
    def get_tfidf_matrix(self,clustersentences):
        
        tfidf_matrix = np.array([],dtype = np.float64).reshape(0,50)
        
        for key,value in clustersentences:
            
            tfidf_matrix =  np.vstack([tfidf_matrix,self.sent_vectors[value]])
            
            return tfidf_matrix
        
  
        
        
        
    def summary(self):
        self.sentences = self.punk.tokenize(self.text)
        
        for i in range(len(self.sentences)):
            
            self.sentences[i] = self.sentences[i].strip()
            
        self.required_sentences = self.normalize_corpus()
        
        self.final_tf_idf  = self.tf_idf_vect.fit_transform(self.required_sentences)
        
        list_of_sentences = []
        
        for i in self.required_sentences:
            
            list_of_sentences.append(i.split())
            
        w2v_model = gensim.models.Word2Vec(list_of_sentences,min_count=2,vector_size = 50,workers = 4)
        
        w2v_words = list(w2v_model.wv.key_to_index)
        
        self.sent_vectors = []; # the avg-w2v for each sentence/review is stored in this list
        
        for sent in tqdm(list_of_sentences): 
            
            sent_vec = np.zeros(50) # 50 dimensions
            
            cnt_words =0; # num of words with a valid vector in the sentence/review
            
            for word in sent: # for each word in a review/sentence
                
                if word in w2v_words:
                    
                    vec = w2v_model.wv[word]
                    
                    sent_vec += vec
                    
                    cnt_words += 1
                    
            if cnt_words != 0:
                
                sent_vec /= cnt_words
                
            self.sent_vectors.append(sent_vec)
            
        if "models" not in os.listdir("."):
            
            os.mkdir('models')
            
        self.Kmeans_cluster = KMeans(n_clusters=10,random_state = 42) if "model.pkl" not in os.listdir("./summary/models") else joblib.load("./summary/models/model.pkl")
        
        joblib.dump(self.Kmeans_cluster,'./summary/models/model.pkl')
        
        self.Kmeans_cluster.fit(self.sent_vectors)
        
        clusters = self.Kmeans_cluster.labels_.tolist()


        
        
        sent_dict = {}
        
        for idx, sentence in enumerate(self.sentences):
            
            sent_dict[idx] = {}
            
            sent_dict[idx]['text'] = sentence
            
            sent_dict[idx]['cluster'] = clusters[idx]
            
            sent_dict[idx]['stemmed'] = self.required_sentences[idx]
            
        
        clusterDictionary = {}
        
        for key, sentence in sent_dict.items():
            
            if sentence['cluster'] not in clusterDictionary:
                
                clusterDictionary[sentence['cluster']] = []
                
            clusterDictionary[sentence['cluster']].append((sentence['stemmed'],key))
            
            sentence['idx'] = len(clusterDictionary[sentence['cluster']]) - 1 
        
        
        
        cosine_score = {}
        
        for key, clusterSentences in clusterDictionary.items():
            
            cosine_score[key] = {}
            
            cosine_score[key]['similarity_score'] = 0
            
            cos_sim_matrix = cosine_similarity(self.get_tfidf_matrix(clusterSentences))
            
            for idx, row in enumerate(cos_sim_matrix):
                
                score = 0
                
                for col in row:
                    
                    score += col
                    
                if score >= cosine_score[key]['similarity_score']:
                    
                    cosine_score[key]['similarity_score'] = score
                    
                    cosine_score[key]['idx'] = idx   
        
        Indexes = []
        
        i = 0
        
        for key, value in cosine_score.items():
            
            cluster = key
            
            idx = value['idx']
            
            #stemmedSentence = clusterDictionary[cluster][idx][0]
            
            stemmedSentence = clusterDictionary[cluster][idx][0]
            
            # key corresponds to the sentences index of the original document
            # we will use this key to sort our results in order of original document
            for key, value in sent_dict.items():
                
                if value['cluster'] == cluster and value['idx'] == idx:
                    
                    Indexes.append(key)

        Indexes.sort()
        # Iterate over sentences and construct summary output
        summary = ''
        
        for i in Indexes:
            
            summary += self.sentences[i] + ' '
            
        return summary
