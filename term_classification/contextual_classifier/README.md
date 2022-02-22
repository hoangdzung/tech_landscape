
  

# Contextual classifier 
Directory containing data, script to prepare data, train and inference model. This is the step 2.1 of the whole process.

## File structure

-  `classifier`: Data directory containing data, script to crawl them and train the classifier. See `classifier/README.md` for more details.
- `infer_terms_from_db.py`: assign technology score for terms extracted in the annotation phase. 
	- Each sentence is assigned a score based on zeroshot classification. The hypotheses used are 'is technology' and 'is non-technology'	- Each term is assigned a score based on the classifier trained in the previous step
	- The final score of a term is the multiplication of these two above scores .
	- `--term_clf`: path to the trained classifier in the previous step.
	- `--filein`: path to annotation files obtained from the annotation phase.
	- `--fileout`: path to the output file. Each line of this file is similar to the corresponding line of the input file, except having an additional field 'terms' :[('term_i,'score_i'),...]
	- `--batch_size`: batch size for zeroshot inference
	- `--kw`: the field of json corresponding to the text content
## How to run
- Step 1: Crawl data and train model in `classififer`
- Step 2 (optional): Remove annotated records not having sufficient information/fields. Actually, this should be done in the annotation phase.
- Step 3: Run `infer_terms_from_db.py` to assign score for each term

## What's next?

We further build a classifier based on the abstracts of terms. We only care about the terms whose scores are larger or equal to a specific threshold to reduce computational cost.
