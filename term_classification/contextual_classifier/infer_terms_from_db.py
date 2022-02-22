from transformers import AutoModelForSequenceClassification, AutoTokenizer,AutoModelForTokenClassification, AutoModel
from transformers import pipeline
import torch 
import numpy as np
import pickle 
import json
import argparse
from tqdm import tqdm
import re 
from subprocess import PIPE, run

parser = argparse.ArgumentParser()
parser.add_argument('--term_clf')
parser.add_argument('--filein')
parser.add_argument('--fileout')
parser.add_argument('--batch_size',type=int, default=4)
parser.add_argument('--kw', default='jobDescription')
args = parser.parse_args()
if args.fileout is None:
    args.fileout = args.filein +'_out'

classifier = pipeline("zero-shot-classification", 
                       model="vicgalle/xlm-roberta-large-xnli-anli",device=0)
tokenizer = AutoTokenizer.from_pretrained('Davlan/bert-base-multilingual-cased-ner-hrl')
model = AutoModel.from_pretrained('Davlan/bert-base-multilingual-cased-ner-hrl',output_attentions=True).cuda()

def cal_tech_prob(sentence):
    outs =[]
    for i in range(0,len(sentence),args.batch_size):
        batch_outs = classifier(sentence[i:i+args.batch_size],['technology','non-technology'])
        if type(batch_outs)==list:
            outs+=batch_outs
        else:
            outs.append(batch_outs)

    return [out['scores'][out['labels'].index('technology')] for out in outs]


def encodings_context(sentence, keywords, tokenizer, model):
    tokens =  tokenizer.encode(sentence,max_length=512, truncation=True)

    extracted_keywords = []
    indices = []
    for keyword in keywords:
        keyword_tokens = tokenizer.encode(keyword)[1:-1]
        index = -1
        for i in range(len(tokens)):
            if tokens[i:i+len(keyword_tokens)] == keyword_tokens:
                index=i
                break
        if index >=0:
            indices.append((i,i+len(keyword_tokens)))
            extracted_keywords.append(keyword)
    out = model(torch.tensor([tokens]).cuda())
    embeddings = []
    for s, e in indices:     
        embeddings.append(out.last_hidden_state[0][s:e].mean(0).detach().cpu().numpy())
    return extracted_keywords, embeddings

clf = pickle.load(open(args.term_clf,'rb'))

n = 0
command = ['wc', '-l', args.fileout]
result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
if result.returncode == 0:
    n = int(result.stdout.split()[0])

result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
print(result.returncode, result.stdout, result.stderr)
with open(args.fileout, 'a') as f:
    for i,line in tqdm(enumerate(open(args.filein))):
        if i < n:
            continue
        threshold=0.5
        extracted_terms = []
        data = json.loads(line.strip())
        # text=data[args.kw]
        if "strings" not in data:
            continue
        text = "\n".join(data["strings"])

        uris = {}
        error = False
        keywords=set()
        # for annot in data['annotations']:
        #     keywords.add(annot['surfaceForm'])
        #     uris[annot['surfaceForm']] = annot['uri'].split('/')[-1]
        if 'Resources' not in data:
            continue

        for annot in data['Resources']:
            keywords.add(annot['@surfaceForm'])
            uris[annot['@surfaceForm']] = annot['@URI'].split('/')[-1]
        sens = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s',text)
        # sens=['. '.join(sens[i:i+args.batch_size]) for i in range(0, len(sens),args.batch_size)]
        tech_probs = cal_tech_prob(sens)
        extracted_keywordss=[]
        embeddingss = []
        tech_probss = []
        for idx, sen in enumerate(sens):
            # tech_prob = cal_tech_prob(sen)
            # term_probs=1
            extracted_keywords = [keyword for keyword in keywords if keyword in sen]
            if len(extracted_keywords)==0:
                continue 

            extracted_keywords, embeddings = encodings_context(sen, extracted_keywords,tokenizer, model)
            if len(extracted_keywords)==0:
                continue 
            extracted_keywordss += extracted_keywords
            embeddingss.append(embeddings)
            tech_probss += [tech_probs[idx]]*len(extracted_keywords)
            # term_probs = clf.predict_proba(np.stack(embeddings))[:,0] * tech_probs[idx]
            # extracted_terms += list(zip(extracted_keywords, [uris[extracted_keyword] for extracted_keyword in extracted_keywords], term_probs.tolist()))
        if len(embeddingss) ==0:
            continue
        try:
            embeddingss = np.vstack(embeddingss)
            tech_probss = np.array(tech_probss)
            term_probs = clf.predict_proba(embeddingss)[:,0] * tech_probss
            extracted_terms += list(zip(extracted_keywordss, [uris[extracted_keyword] for extracted_keyword in extracted_keywordss], term_probs.tolist()))
            data['terms'] =  extracted_terms #= {'id':data.get('id',''),'companyName':data.get('companyName',''),'terms':extracted_terms,'jobDescription':data['jobDescription'],'annotations':data['annotations']}
            # if len(extracted_terms)>0:
            #     print(data)
            f.write(json.dumps(data)+"\n")
            # predictions.append(data)
        except Exception as e:
            print(e)