
# Data Crawling
Directory containing data (technology terms and corresponding sentences) and downloading scripts  
## File structure
- `crawl tech terms.ipynb`: Crawl technology terms from [techopedia](https://www.techopedia.com/) and economy terms from [economist](https://www.economist.com/economics-a-to-z)
- `crawl sample sentence.ipynb`: Crawl sentences containing specific keywords from [wordhippo](www.wordhippo.com)
-  `crawl sample sentence.py`: Script to crawl sentences containing specific keywords from [wordhippo](www.wordhippo.com). 
	- The first argument is the path of the input file where each line is a term. 
	- The second argument is the path of the output file.
	- Example: `python3 crawl sample sentence.py data/terms/tech_terms.txt data/domain_sentences/tech_sentences.json`

- `sen_translate.py`: Script to translate sentences in English to another language using Google Translate API. 
	- `--filein` should be the path of a json file whose keys are terms, values are lists of sentences.
	- `--fileout` the path of the csv output file whose values in the first column are translated terms and  values in the second colums are corresponding translated sentences.
	-  `--to` the code of the target language. See more at [this](https://cloud.google.com/translate/docs/languages) 
	-  Example: `python3 sen_translate.py --filein data/domain_sentences/eco_sentences.json --fileout data/domain_sentences/eco_sentences_fr.csv --to fr`
	- Notice: Sentences can be translated by, first, transforming the input json file (e.g. `data/domain_sentences/eco_sentences.json`) to the tagged form (putting terms between two html tags, like `data/domain_sentences/eco_sentences.csv`), then using google sheet to translate. However, this way is not consistent, i.e. the translated terms are not always inside the html tags.
- `zeroshot classificaion multilang.ipynb`: Term classification based on contextual embeddings.
- `svm.pkl`: trained SVM model obtained by running `zeroshot classificaion multilang.ipynb`
- `data`: Data directory:
	- `terms`: Directory containing technology terms. Economy terms file is missing but can be crawled using `crawl_tech_terms.ipynb`
		- `c4istar_technologies.txt`: Technology terms obtained from [mendeley](https://data.mendeley.com/datasets/88g8kcwj9r/1)
		- `techopedia.txt`: Technology terms crawled from [techopedia](https://www.techopedia.com/) 
		- `tech_terms.txt`: Combination of two above files
		- `eco_terms.txt`: Missing, but can be crawled from [economist](https://www.economist.com/economics-a-to-z) by using `crawl_tech_terms.ipynb`
	- `domain_sentences`: Directory containing sentences
		- `*.json` : outputs of `crawl sample sentence.py`
		- `*_fr.csv`, `*_de.csv`: outputs of `sen_translate.py`
		- `eco_sentences.csv`, `tech_sentences.csv`: sentences in the tagged form
	
## How to run 
- Step 1: Crawl data using `crawl sample sentence.py`. Crawled data are placed in `data\domain_sentences` in json format.
- Step 2: Translate english training data to other languages by `sen_translate.py`
- Step 3: Train SVM classifier by `zerosho classification multilang.ipynb`. Trained model is saved as `svm.pkl`