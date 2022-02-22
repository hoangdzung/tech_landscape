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

lang_to_api = {
    'en': 'http://localhost:2222/rest/annotate',
    'fr': 'http://localhost:2223/rest/annotate',
    'de': 'http://localhost:2224/rest/annotate',
    'it': 'http://localhost:2225/rest/annotate',

    }
def annotate(line):
    global lang_to_apis
    data = json.loads(line.strip())
    try:
        text = ". ".join(data['strings'])
        lang = langdetect.detect(text)
    except:
        return ""
        
    try:
        api_url = lang_to_api[lang][:]
    except:
        api_url = lang_to_api['en'][:]
    try:
        response = requests.get(api_url, params={'text':text},headers={'Accept': 'application/json'})
        if response.status_code == 200:
            result = response.json()
            data.update(result)
            return json.dumps(data)+"\n"
    except:
        pass
    return ''

pool = mp.Pool(int(0.8*mp.cpu_count()))
annotated_results = pool.map(annotate, open(args.data).readlines())

n_miss = 0
with open(args.out, 'w') as f:
    for annotated_result in annotated_results:
        if len(annotated_result) == 0:
            n_miss += 1
        else:
            f.write(annotated_result)
