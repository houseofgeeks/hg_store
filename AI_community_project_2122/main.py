from autocaptioning.model import Auto_Caption
from sentiment.model import sentiment
import uuid
from summary.model import text_summarization
from PIL import Image
from io import BytesIO
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from fastapi import FastAPI,Request, File, UploadFile
from nsfw.model import Nsfw
from pydantic import BaseModel 
import os
import json

app = FastAPI()
nsfw_model = Nsfw()
autocaption_model = Auto_Caption("")
sentiment_model = sentiment()

class Item(BaseModel):
    text: list
    
@app.post("/captioning")
def return_caption(item: Item):
	text = item.text
	final = {}
	cnt = 0
	for texts in text:
		autocaption_model.update_data(texts)
		final[cnt] = {'captions': autocaption_model.fun()}
		cnt += 1
	return str(final)

@app.post("/summary")
def return_summary(item: Item):
	text = item.text
	final = {}
	cnt = 0
	for texts in text:
		model1= text_summarization(texts)
		final[cnt] = {'summarization_text': model1.summary()}
		cnt += 1
	return str(final)

@app.post("/sentiment")
def know_sentiment(item: Item):
	text = item.text
	final = {}
	cnt = 0
	for texts in text:
		final[cnt] = {'sentiment': sentiment_model.score(texts)}
		cnt += 1
	return str(final)

IMAGEDIR = "./images/"
@app.post("/NSFW")
async def predict_image(file:UploadFile = File(...)):
	file.filename = f"{uuid.uuid4()}.jpg"
	contents = await file.read()
	with open(f"{IMAGEDIR}{file.filename}", "wb") as f:
		f.write(contents)
	file.close()
	image = plt.imread(f"{IMAGEDIR}{file.filename}")
	image = tf.keras.preprocessing.image.smart_resize(image,size=(250,250),interpolation='nearest')
	image = image.reshape(1,250,250,3)
	predictions = nsfw_model.predict(image)
	os.remove(f"{IMAGEDIR}{file.filename}")
	return "SFW" if(predictions[0][0] != 0) else "NSFW" 
