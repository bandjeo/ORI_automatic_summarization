================================================
Project setup (requires python3 64-bit):
================================================
python venv .env
.env/Scripts/activate
pip Install nltk
pip install spacy==2.1.3
python -m spacy download en
pip install neuralcoref

project won't run correctly until the required nltk packages are installed (console will show required packages)
================================================
Running project:
========================================================================================================================
python text_rank.py => runs TextRank and TextRank with UCS on test.txt file, prints summaries in console
python noun_rank.py => runs noun based method on test.txt file, prints summary in console
python preprocess_files.py => used on wikipedia text dump*, separates each txt file in data
			 folder into articles (a txt file is created in data\articles for each article)			
python analytics.py => runs all methods on each article in data\articles and shows average time, summary length
			and percentage of vocabulary retained - for each method

* Wikipedia text dump consists of separated compressed txt files, each containing text from multiple articles
========================================================================================================================


==================================================================================================================================
Results from 216 wikipedia articles:
==================================================================================================================================
Method              | Average Time [s]   | Average Number of extracted sentences  | Average fraction of vocabulary    
----------------------------------------------------------------------------------------------------------------------------------
Text Rank           |  2.0849710989881447|                      18.166666666666668|                0.22838957244415872
Text Rank UCS       |  1.6427143227171015|                       7.694444444444445|                0.26627099682473626
Noun Rank           |   5.322123860871351|                      18.166666666666668|                  0.281163601872257
