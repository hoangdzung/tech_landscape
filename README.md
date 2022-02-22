

# Technology landscape
Provided a set of raw texts from indeed, patent, twitter and so on of several companies, we need to extract a list of interested technologies. Due to the huge amount of data, most of raw data are unavailable and should be requested.
	
## How to run
- Step 1: Annotate data using `dbpedia_annotation`
- Step 2: Remove non-technology terms using `term_classification`. 
- Step 3: Keep the most relevant technologies using `relevant_score`.
