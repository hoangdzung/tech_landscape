#!/usr/bin/env python
# coding: utf-8

# In[19]:


import requests
import string
from bs4 import BeautifulSoup
from tqdm import tqdm
import json 
import multiprocessing as mp 
import sys 


def crawl(term):
    term=term.strip()
    page = requests.get("https://www.wordhippo.com/what-is/sentences-with-the-word/{}.html".format(term.replace(" ","+")))

    soup = BeautifulSoup(page.content, 'html.parser')
    sentences=[]
    for row in tqdm((soup.find_all('tr',class_='exv2row1')+soup.find_all('tr',class_='exv2row2'))[:50]):
        sentence = row.text.strip()
        sentences.append(sentence)
    return term, sentences

pool = mp.Pool(int(0.5*mp.cpu_count()))
results = pool.map(crawl, open(sys.argv[1]).readlines() )
results = dict(results)
with open(sys.argv[2],'w') as f:
    json.dump(results, f)
