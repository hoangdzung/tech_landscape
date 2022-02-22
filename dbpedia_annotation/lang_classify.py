from langdetect import detect
import multiprocessing as mp 
import os 
import json 
import argparse
from tqdm import tqdm 

parser = argparse.ArgumentParser()
parser.add_argument("--datain")
parser.add_argument("--dataout")
args = parser.parse_args()

def groupbylang(srcdir, dstdir=args.dataout):
    dstdir = os.path.join(dstdir, os.path.basename(srcdir))
    if not os.path.isdir(dstdir):
        os.makedirs(dstdir)

    lang_to_file = {}
    for lang in ['en','de','fr','it','other']:
        lang_to_file[lang] = open(os.path.join(dstdir, lang),'w')

    for root, dirnames, filenames in os.walk(srcdir):
        for filename in tqdm(filenames, desc=srcdir):
            if not filename.startswith('part'):
                continue
            for line in open(os.path.join(root, filename)):
                data = json.loads(line.strip())
                try:
                    lang = detect(data['jobDescription'])
                except:
                    #print(data['jobDescription'])
                    lang = 'other'
                try:
                    lang_to_file[lang].write(line)
                except:
                    lang_to_file[lang] = open(os.path.join(dstdir, lang),'w')
                    lang_to_file[lang].write(line)

    for lang in lang_to_file:
        lang_to_file[lang].close()



pool = mp.Pool(int(0.8*mp.cpu_count()))
pool.map(groupbylang, [os.path.join(args.datain, i) for i in os.listdir(args.datain)])

