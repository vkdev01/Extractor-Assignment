# Wiki Extractor

It searches wikipedia for a given 'keyword', scraps all the links the get displayed and crawls them one by one.

---

## how to run

```bash

python wiki_extractor.py --k "<keyword-to-search>" --l <num of links to crawl> --o "name of out file without extension"

```
e.g, 
python wiki_extractor.py --k "Machine Learning" --l 100 --o "ML_articles"