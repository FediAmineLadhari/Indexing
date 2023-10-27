import nltk
#nltk.download('punkt')
#nltk.download('stopwords')
from nltk.tokenize import word_tokenize
from math import log
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import os


def raciner(l):
  ps = PorterStemmer()
  a=[]
  for i in l:
    a.append(ps.stem(i))
  return a

def filter(l):
  s=set(stopwords.words("english"))
  a=[]
  for i in l:
    if not i in s:
      a.append(i)
  return a

def nb_occ(x,l):
  all_words=nltk.FreqDist(l)
  return all_words[x]

def poid(x,l,nb_doc,y):
  return (1+log(nb_occ(x,l)))*log(nb_doc/y)

def doc_retourne(x,l):
  res={}
  for k,v in l.items():
    if nb_occ(x,v)>0:
      res[k]=v
  return res

def best_doc(x,l,nb_doc,y):
  doc_poid={}
  for i in l.keys():
    doc_poid[i]=poid(x,l[i],nb_doc,y)
  maxv=max(doc_poid.values())
  for key, val in doc_poid.items():
    if val==maxv:
      return key

def contien(l,x):
  cont=0
  for i in l.values():
    if x in i:
      cont+=1
  return cont

def tf_idf(word_tokens,x):
  filtered_sentence=filter(word_tokens)
  mytexts = nltk.TextCollection([filtered_sentence, word_tokens])
  if len(mytexts)==0:
    return 0
  return mytexts.tf_idf(x, word_tokens)


l=os.listdir('.')
f_txt=[]
for i in l:
  if i[-3:]=="txt":
    f_txt.append(i)
nb_doc=len(f_txt)
x=input("donner un mot a chercher: ")
x1=x
ps1 = PorterStemmer()
x=ps1.stem(x)
txt={}
txt1={}
for i in f_txt:
  f=open(i,'r')
  txt[i]=word_tokenize(f.read())
  txt1[i]=word_tokenize(f.read())
for i in txt.keys():
  l1=filter(txt[i])
  txt[i]=raciner(txt[i])
txt=doc_retourne(x,txt)
if len(txt)>0:
  y=contien(txt,x)
  for i in txt.keys():
     print("documen {} nombre d occurance du mot {} avec un poid de {} et tf_idf {}".format(i,nb_occ(x,txt[i]),poid(x,txt[i],nb_doc,y),tf_idf(txt1[i],x1)))
  print("document le plus pertinent: {}".format(best_doc(x,txt,nb_doc,y)))
else:
  print("n'existe pas")
input("type enter to exit")
