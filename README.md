# ParadigmGeneralization

This repository is the scripts and data we used for paradigm generalization in 

[Silfverberg, M.; Liu, L.; Hulden, M. (2018). A Computational Model for the Linguistic Notion of Morphological Paradigm. In Proceedings of the 27th International Conference on Computational Linguistics (pp. 1615-1626).](http://aclweb.org/anthology/C18-1137)

## Datasets

Two data sets are used for experiments on paradigm generalization.

The first data set is the combination of the training and development sets used by Durrett and DeNero (2013) which are reformatted for current experiment. It is in the directory DurrettDeNero/.

The second data set is the combination of the training, development and testing part of the low, medium, high data setting for each of the 33 languages in CoNLL-SIGMORPHON 2017 shared task data (Cotterell et al. 2017). Only complete tables are used for each language. The data is reformatted and stored in the directory CoNLL-SIGMORPHON2017/. The complete table size for each part-of-speech of each language is as follows:

['albanian V=121 N=21', 'bengali V=47 N=13', 'catalan V=54', 'danish V=9 N=7', 'dutch V=17 ADJ=10', 'english V=6', 'estonian V=80 N=31', 'faroese V=15 N=17 ADJ=18', 'finnish V=142 N=29 ADJ=29', 'french V=50', 'georgian V=72 N=20 ADJ=20', 'german V=30 N=9', 'hebrew V=29 N=27', 'hindi V=212', 'hungarian V=60 N=35', 'icelandic V=29 N=17', 'irish V=64 N=14 ADJ=14', 'italian V=52', 'latin V=100 N=13 ADJ=32', 'latvian V=43 N=15 ADJ=25', 'lithuanian V=50 N=15 ADJ=77', 'lower-sorbian V=22 N=19 ADJ=34', 'northern-sami V=55 N=14 ADJ=14', 'persian V=137', 'portuguese V=77', 'romanian V=38 N=7 ADJ=17', 'slovak N=13 ADJ=28', 'slovene V=26 N=19 ADJ=54', 'spanish V=71', 'swedish V=12 N=9 ADJ=16', 'turkish V=121 N=109 ADJ=73', 'urdu V=212 N=7', 'welsh V=64']

## Scripts

The script in the directory paradigmextract/ is for 1st-order paradigm extraction, i.e. to extract paradigms from inflection tables. It is from https://github.com/marfors/paradigmextract with minor changes.

-------------------------------------------------------------

To get the counts of 1st-order (i.e. paradigms extracted from inflection tables) and 2nd-order (i.e. more abstract paradigms generalized on top of 1st-order paradigms) paradigms on DurrettDeNero data set,

$ python paradigmGeneralDurrettDeNero.py

- This will store the counts in paradigmCountDurrettDeNero.csv.

- 1st-order paradigms will be stored in the directory paradigmsDurrettDeNero/.

- 2nd-order paradigms will be stored in the directory paradigmsDurrettDeNero/2nd_order/.

-------------------------------------------------------------

To get the counts of 1st-order (i.e. paradigms extracted from inflection tables) and 2nd-order (i.e. more abstract paradigms generalized on top of 1st-order paradigms) paradigms on CoNLL-SIGMORPHON2017 data set,

$ python paradigmGeneralCoNLL-SIGMORPHON2017.py

- This will store the counts in paradigmCountCoNLL-SIGMORPHON2017.csv.

- 1st-order paradigms will be stored in the directory paradigmsCoNLL-SIGMORPHON2017/.

- 2nd-order paradigms will be stored in the directory paradigmsCoNLL-SIGMORPHON2017/2nd_order/.


