import os 
import json 
import multiprocessing as mp 
import argparse
import langdetect
import random
import requests

parser = argparse.ArgumentParser()
parser.add_argument('--data')
parser.add_argument('--out')
args = parser.parse_args()

lang_to_apis = {
    'en': ['https://api.dbpedia-spotlight.org/en/annotate', 'http://localhost:2222/rest/annotate'],
    'fr': ['https://api.dbpedia-spotlight.org/fr/annotate', 'http://localhost:2223/rest/annotate'],
    'de': ['https://api.dbpedia-spotlight.org/de/annotate', 'http://localhost:2224/rest/annotate'],
    'it': ['https://api.dbpedia-spotlight.org/it/annotate', 'http://localhost:2225/rest/annotate'],

    }
def annotate(line):
    global lang_to_apis
    data = json.loads(line.strip())
    try:
        text = data['jobDescription']
        lang = langdetect.detect(text)
    except:
        return ""
        
    try:
        api_urls = lang_to_apis[lang][1:]
    except:
        api_urls = lang_to_apis['en'][1:]

    #random.shuffle(api_urls)
    for api_url in api_urls:
        response = requests.get(api_url, params={'text':text},headers={'Accept': 'application/json'})
        if response.status_code == 200:
            result = response.json()
            data.update(result)
            break 
    if response.status_code != 200:
        return ''
    else:
        return json.dumps(data)+"\n"

pool = mp.Pool(int(0.8*mp.cpu_count()))
annotated_results = pool.map(annotate, open(args.data).readlines())

n_miss = 0
with open(args.out, 'w') as f:
    for annotated_result in annotated_results:
        if len(annotated_result) == 0:
            n_miss += 1
        else:
            f.write(annotated_result)
