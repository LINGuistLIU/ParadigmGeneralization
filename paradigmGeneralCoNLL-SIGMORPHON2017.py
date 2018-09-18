import os
from paradigmGeneral import *

languagelist = ['albanian', 'bengali', 'catalan', 'danish', 'dutch', 'english', 'estonian', 'faroese', 'finnish', 'french', 'georgian', 'german', 'hebrew', 'hindi', 'hungarian', 'icelandic', 'irish', 'italian', 'latin', 'latvian', 'lithuanian', 'lower-sorbian', 'northern-sami', 'persian', 'portuguese', 'romanian', 'slovak', 'slovene', 'spanish', 'swedish', 'turkish', 'urdu', 'welsh']

print('Extracting paradigms ... ')

ppath = 'paradigmsCoNLL-SIGMORPHON2017/'
if not os.path.exists(ppath):
    os.mkdir(ppath)

for language in languagelist:
    print(language)
    os.system("pypy paradigmextract/pextract.py < CoNLL-SIGMORPHON2017/" + language + "_all.txt > " + ppath + language + ".p")

print('----------------------------')
print('2nd-order generalization ... ')

ppath2 = ppath + '2nd_order/'
if not os.path.exists(ppath2):
    os.mkdir(ppath2)

csvname = 'paradigmCountCoNLL-SIGMORPHON2017.csv'
_ = ParadigmCounts(languagelist, ppath, ppath2, csvname)
