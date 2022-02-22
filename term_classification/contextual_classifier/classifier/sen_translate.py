import json 
import pandas as pd 
import argparse
from tqdm import tqdm 

def translate_text(text, target="fr"):
    """Translates text into the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """
    import six
    from google.cloud import translate_v2 as translate

    translate_client = translate.Client()

    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(text, target_language=target)

    return result["translatedText"]

parser = argparse.ArgumentParser()
parser.add_argument('--filein')
parser.add_argument('--fileout')
parser.add_argument('--to')
args = parser.parse_args()

data = json.load(open(args.filein))
rows = []

for kw, sentences in tqdm(data.items()):
    if len(sentences)==0:
        continue
    for sentence in sentences[:10]:
        index = sentence.lower().find(kw.lower())
        sentence = sentence[:index+len(kw)]+" </p>"+sentence[index+len(kw):]
        sentence = sentence[:index]+"<p> "+sentence[index:]
        translated_text = translate_text(sentence, target=args.to)
        
        s_idx = translated_text.find("<p>")
        e_idx = translated_text.find("</p>")

        translated_kw = translated_text[s_idx+3:e_idx].strip()
        translated_text = translated_text.replace("<p>","").replace("</p>","")
        rows.append([translated_kw, translated_text])
df = pd.DataFrame(rows, columns=['kw','sentence'])
df.to_csv(args.fileout, index=False)