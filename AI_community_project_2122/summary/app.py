from model import text_summarization
from fastapi import FastAPI,Request
from typing import Optional
from pydantic import BaseModel
import json

app = FastAPI()

class Item(BaseModel):
    text: list
    
@app.post("/text")
def create_item(item: Item):
	text = item.text
	model1= text_summarization(text)	
	output = {'summarization_text': model1.summary()}
	return output

