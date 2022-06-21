import re
import pickle

from keybert import KeyBERT
kw_model = KeyBERT()

class Auto_Caption:

  def __init__(self, doc):  
        self.doc = doc 

  def fun(self):
    lst=doc.split("\n")   #Split the sentence from newline characters
    k=(len(lst))
    for i in range(k):
      if(lst[i].find(".")>0):     #If a character other than the first character is a dot.
        if(lst[i][lst[i].find(".")-1].islower()):  
          new_lst=lst[i].split(".")
          for s in new_lst:
            self.caption(s)  
      else:
        self.caption(lst[i])

  def caption(self,s):
    tag=kw_model.extract_keywords(s, keyphrase_ngram_range=(2,2 ), stop_words='english', 
                                use_mmr=True, diversity=0.6,top_n=1)
    if(len(tag)!=0):
      tag1=tag[0][0]
      tag2=re.split(" ",tag1)
      
    new_lst=re.findall(r"([\w]{1,2}-[\w]{1,2}-[\w]{2,4})|([\w]+-[\w]+)|([\d]{1,2}:[\d]{2})",s) 

    if len(new_lst)==0:
      if(len(tag)!=0):
        print(tag[0][0])
    else:
      for j in new_lst[0]:
        if j.find(tag2[0])!=-1:
          j+=" "
          j+=tag2[1]
          print(j)
        elif j.find(tag2[1])!=-1:
          tag2[0]+=" "
          tag2[0]+=j
          print(tag2[0])


pickle_out=open("Auto_Captioning.pickle","wb")
pickle.dump(Auto_Caption,pickle_out)
pickle_out.close()
