
  

# Data Annotation

Directory containing sample data and relevent scripts to extract terms from sentences. This is the first step of the whole process.

## File structure

-  `indeed`: Directory containing sample data crawled from indeed. Beside indeed, we have other data sources like twitter, website (of the companies), ... 
Normally, the data are saved in the form of json but each data source has its own set of fields so the scripts should be modified to handle them appropirately.

-  `lang_classify.py`: Split the data into several parts based on their languages. We only take the major languages including en, fr, de, it into consideration.
	- `--datain`: Input data directory like `indeed`
	- `--dataout`: Output data directory
	- This script has been integrated into below annotate scripts.
- `annotate_website.py`,`annotate_twitter.py`: Script to annotate text using dbpedia spotlight.
	- `--data`: Input file where each line is a dictionary. This file is expected to be in output directory of `lang_classify.py`
	- `--out`: Output file where each line is the annotated result in json format.
## How to run
- Step 1: Split the data based on the language for each data source by running `lang_classify.py`
- Step 2 (optional): Run dbpedia spotlight locally. See more at [this](https://github.com/dbpedia-spotlight/dbpedia-spotlight-model)
- Step 3: Run `annotate_*.py` to extract terms from text

## What's next?

After annotating, we will classify these extracted terms as tech or non-tech using the combination of two classifiers:
	- Zeroshot classification using abstracts
	- Classifer using contextual embeddings of these terms  
