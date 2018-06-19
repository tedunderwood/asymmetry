import csv

import pandas as pd
import SonicScrewdriver as utils

pathdict = dict()

with open('../noveltmmeta/get_EF/ids2pathlist.tsv', encoding = 'utf-8') as f:
    for line in f:
        fields = line.strip().split('\t')
        pathdict[fields[0]] = fields[1]

meta = pd.read_csv('topicsample.tsv', sep = '\t')

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
        missing += 1
        themissing.append(d)

with open('pathlist.tsv', mode = 'w', encoding = 'utf-8') as f:
    f.write('docid\tpath\n')
    for docid, path in outrows:
        f.write(docid + '\t' + path + '\n')

print(missing)
print(themissing)


