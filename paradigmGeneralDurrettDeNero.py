import os
from paradigmGeneral import *

languagelist = ['de', 'es', 'fi']

print('Extracting paradigms ... ')

ppath = 'paradigmsDurrettDeNero/'
if not os.path.exists(ppath):
    os.mkdir(ppath)

for language in languagelist:
    print(language)
    if language == 'fi':
        os.system('cat DurrettDeNero/fi_train_dev2.txt >> DurrettDeNero/fi_train_dev.txt')
    os.system("pypy paradigmextract/pextract.py < DurrettDeNero/" + language + "_train_dev.txt > " + ppath + language + ".p")

print('----------------------------')

print('2nd-order generalization ... ')

ppath2 = ppath + '2nd_order/'
if not os.path.exists(ppath2):
    os.mkdir(ppath2)

csvname = 'paradigmCountDurrettDeNero.csv'
_ = ParadigmCounts(languagelist, ppath, ppath2, csvname)




