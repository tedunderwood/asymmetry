# Slightly adjusted version of generate_path_list
# which I used to add supplements beyond topicsample.

# This version was used to add the second supplement.

import csv, os

import pandas as pd
import SonicScrewdriver as utils

pathdict = dict()

with open('../../noveltmmeta/get_EF/ids2pathlist.tsv', encoding = 'utf-8') as f:
    for line in f:
        fields = line.strip().split('\t')
        pathdict[fields[0]] = fields[1]

docids2get = []

meta = pd.read_csv('second_supplement.tsv', sep = '\t')


outrows = []
missing = 0
themissing = []

for d in meta.docid:
    cleand = utils.clean_pairtree(d)
    dollarless = d.replace('$', '')

    if d in pathdict:
        outrows.append((d, pathdict[d]))
    elif cleand in pathdict:
        outrows.append((cleand, pathdict[cleand]))
    elif dollarless in pathdict:
        outrows.append((dollarless, pathdict[dollarless]))
    else:
        possiblepath, postfix = utils.pairtreepath(d, '')
        thepathtotest = '/Volumes/TARDIS/work/ef/fic/' + possiblepath + postfix + '/' + d + '.json.bz2'
        thepath = possiblepath + postfix + '/' + d + '.json.bz2'
        if os.path.isfile(thepathtotest):
            outrows.append((d, thepath))
            print('worked')
        else:
            thepathtotest = thepathtotest.replace('uc1.b', 'uc1.$b')
            thepath = thepath.replace('uc1.b', 'uc1.$b')
            if os.path.isfile(thepathtotest):
                outrows.append((d, thepath))
                print('worked')
            else:
                print('failed')
                missing += 1
                themissing.append(d)

with open('second_supplement_pathlist.tsv', mode = 'w', encoding = 'utf-8') as f:
    f.write('docid\tpath\n')
    for docid, path in outrows:
        f.write(docid + '\t' + path + '\n')

print(missing)
print(themissing)

meta.set_index('docid', inplace = True)
missingmeta = meta.loc[themissing, : ]
missingmeta.to_csv('second_need2rsync.tsv', sep = '\t', index_label = 'docid')


