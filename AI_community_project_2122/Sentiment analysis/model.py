import string
import re
import pickle
import spacy
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding
import numpy as np
import re


class sentiment:
	def __init__(self):
		self.model =  load_model('./sentiment/Model.h5')
		self.tokenizer = Tokenizer()
		self.nlp = spacy.load("en_core_web_sm")
		self.stopwords = list(self.nlp.Defaults.stop_words)
		
	def clean_text(self,sentences):
		docs = self.nlp(sentences)
		sentence_list = [sentence.text for sentence in docs.sents]
		return sentence_list
		
	def encoding(self,sentences):
		training_sentences = self.clean_text(sentences)
		print(training_sentences)
		self.tokenizer.fit_on_texts(training_sentences)
		word_index = self.tokenizer.word_index
		training_sequences = self.tokenizer.texts_to_sequences(training_sentences)
		training_padded = pad_sequences(training_sequences,padding = "post")
		return training_padded
	def score(self,sentences):
		padded = self.encoding(sentences)
		sent = self.model.predict(padded)
		return str({"sentiment score : ": sent[0][0]})
