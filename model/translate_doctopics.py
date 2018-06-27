# translate_doctopics.py

# This script takes the doctopics file produced by MALLET and turns it
# into a form that is slightly easier to read.

import sys
import numpy as np

outrows = []
ctr = 0
split_files = dict()

with open('20thdoctopics.txt', encoding = 'utf-8') as f:
    for line in f:
        fields = line.strip().split('\t')
        fields[1] = fields[1].replace('file:/projects/ischoolichass/ichass/usesofscale/mallet-2.0.8/../code/asymmetry/twentieth/', '')
        fields[1] = fields[1].replace('.txt', '')
        if '%7C' in fields[1]:
            parts = fields[1].split('%7C')
            docid = parts[0]
            if docid not in split_files:
                split_files[docid] = []
            split_files[docid].append(np.array([float(x) for x in fields[2:]]))
            if len(parts[1]) > 1:
                ctr = ctr + 1
        else:
            outrows.append(fields[1: ])

print(ctr)

header = "docid\t" + '\t'.join([str(x) for x in range(0, 500)]) + '\n'
with open('20th_doc_topics.tsv', mode = 'w', encoding = 'utf-8') as f:
    f.write(header)
    for row in outrows:
        f.write('\t'.join(row) + '\n')

with open('20th_doc_topics.tsv', mode = 'a', encoding = 'utf-8') as f:
    for docid, volparts in split_files.items():
        allvols = np.sum(volparts, axis = 0)
        normalized = allvols / np.sum(allvols)
        f.write(docid + '\t' + '\t'.join([str(x) for x in normalized]) + '\n')
