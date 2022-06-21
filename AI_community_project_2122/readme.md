### The community project for the session :  2021 - 2022

This repository contains the code for :
	1. Auto captioning/keyword extraction of text
	2. Summarization of text
	3. Sentiment analysis of text
	4. NSFW classifier for images
	
To run the app run the following commands: 

```
pip install -r requirements
```

Then run

```
python3
import nltk
nltk.download('popular')
exit()
``` 
```
python3 -m spacy download en_core_web_sm
```

```
uvicorn main:app --reload
```

Redirect to the address 
```
http://127.0.0.1:8000/docs#/
```

Call for the services which you want
