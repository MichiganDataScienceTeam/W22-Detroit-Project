from cmath import nan
from curses.ascii import isdigit
from xml.dom import ValidationErr
from zlib import Z_DEFAULT_COMPRESSION
from idna import valid_label_length
import numpy as np
import pandas as pd

#returns true if a string is a number
def isNum(str) -> bool:
    for c in str:
        if not isdigit(c):
            return False
    return True


#noise filtering
noise_list = ["is", "a", "this", "...", "of", "the",
                "and", "to", "of", "on", "is", "in",
                "at", "was", "this", "-", "has", "into",
                "for", "are", "it", "from"] 

def removeNoise(input_text) -> str:
    words = input_text.split() 
    noise_free_words = [word for word in words if word.lower() not in noise_list] 
    noise_free_text = " ".join(noise_free_words) 
    return noise_free_text


#read in csv file to list:[id, description]
def getDescriptions() -> list:
    df = pd.read_csv('../data/Improve_Detroit_Issues.csv', dtype = {'reopened_at':'str', 'neighborhood':'str'})
    print(df.shape)
    df = df.drop_duplicates(subset = 'id')
    lst = df.values.tolist()
    des = []
    for l in lst:
        if l[5] != "Redacted" and l[5] == l[5] and len(l[5]) != 0:
            des.append([l[2],l[5]])
    return des

    
#added a dictionary of frequency to every description (with cleaning)
#download these if error occurs
# nltk.download('wordnet')
# nltk.download('omw-1.4')
from nltk.stem.wordnet import WordNetLemmatizer
lem = WordNetLemmatizer()
meaningless_punc = [".", ",","-","/","@","#","%","&","\"","\'"]

def genFreq(des) -> list:
    freq = {}
    for l in des:
        clean_des = removeNoise(l[1])
        words = clean_des.split()
        for w in words:
            if w[-1] in meaningless_punc:
                w = w[:-1]
            if isNum(w):
                continue
            w = lem.lemmatize(w).lower()
            if w in freq:
                freq[w] += 1
            else:
                freq[w] = 1
        l.append(freq)
        freq = {}
    return des


#main
des = getDescriptions()
des = genFreq(des)
for l in des:
    print(l)



        