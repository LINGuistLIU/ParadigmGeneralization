import os
from paradigmGeneral import *

languagelist = ['de', 'es', 'fi']

print('Extracting paradigms ... ')

ppath = 'paradigmsDurrettDeNero/'
if not os.path.exists(ppath):
    os.mkdir(ppath)

for language in languagelist:
    print(language)
    os.system("pypy paradigmextract/pextract.py < DurrettDeNero/" + language + "_train_dev.txt > " + ppath + language + ".p")

#-----------------------------------------------------------------------

print('2nd-order generalization ... ')

paligned = ppath + 'aligned/'
if not os.path.exists(ppath):
    os.mkdir(ppath)

csvname = 'paradigmCountDurrettDeNero.csv'
_ = ParadigmCounts(languagelist, ppath, csvname)




