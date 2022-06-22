# &emsp;&emsp;&emsp; _AUTO CAPTIONING_ 
For the extraction of keywords and Keyphrases , we have used the ```KeyBert```
and Data reguler expressions (```regex```) to extract a valid date format from the string.
## _About  KeyBert :_
- KeyBert is minimal and easy to use *keyword extraction technique.*
- It is leverage ```BERT``` embeddings to create keywords and keyphrases that are most similer to a documents

### _Working of Model :_
- For the installation of KeyBert we have started with
``` pip install keybert ```
- Used _keyphrase_ngram_range_ to set the length of the resulting keywords/keyphrases.
- We checked for all the possible ranges and diversities and Set the range (2,2) , ,diversity (0.6) for the efficient result in this model.
```
tag = kw_model.extract_keywords(s, keyphrase_ngram_range=(2,2 ), stop_words='english',use_mmr=True, diversity=0.6,top_n=1)
[('algorithm generalize training', 0.7727),
 ('supervised learning algorithm', 0.7502),
 ('learning machine learning', 0.7577),
 ('learning algorithm analyzes', 0.7587),
 ('learning algorithm generalize', 0.7514)]
```
- To validate and extract date in correct manner used regex -
```
new_lst=re.findall(r"([\w]{1,2}-[\w]{1,2}-[\w]{2,4})|([\w]+-[\w]+)|([\d]{1,2}:[\d]{2})",s)
```

- To store object data to the files we can use ```pickle.dump``` 
  - The first argument is the object that you want to store.
  - The second argument is the file object you get by opening the desired file in ```write-binary (wb)``` mode. 
  - The third argument is the ```key-value argument```. This argument defines the protocol. There are two type of protocol _pickle.HIGHEST_PROTOCOL and pickle.DEFAULT_PROTOCOL_
   (As we are using pretrained model here so this step is optional)
```
pickle_out=open("Auto_Captioning.pickle","wb")
pickle.dump(Auto_Caption,pickle_out)
pickle_out.close()
```
## _Contributers_
&emsp;&emsp;[Abhishek Mishra](https://github.com/abhishekiiitr) &emsp; &emsp; &emsp;&nbsp;[Anjaney Srinivas](https://github.com/branch-electronics)
&emsp;&emsp;[Ishan Jaiswal](https://github.com/hackerishan-123) &emsp; &emsp; &emsp; &emsp; [Ayush Kumar singh](https://github.com/ayushksingh28)

## *Resources*
&emsp;&emsp;Blog - [ Maarten Grootendorst](https://pypi.org/project/keybert/) &emsp; Paper -[ Sharma, P., & Li, Y. (2019)](https://www.preprints.org/manuscript/201908.0073/download/final_file)
