from collections import Counter
import sys, os, re

special = dict()
with open('specialconversions.tsv', encoding = 'utf-8') as f:
    for line in f:
        row = line.strip().split('\t')
        special[row[0]] = row[1]

stopwords = set()
with open('minimalstopwords.txt', encoding = 'utf-8') as f:
    for line in f:
        stopwords.add(line.strip())

sourcedir = 'influencedata/'
files = os.listdir(sourcedir)
files = [x for x in files if x.endswith('.txt')]

targetdir = 'data/'

docfreq = Counter()
ctr = 0
hyphens = 0

for fil in files:
    thisfilevocab = set()
    ctr += 1
    if ctr % 1000 == 1:
        print(ctr)
    outfile = []

    with open(sourcedir + fil, encoding = 'utf=8') as f:
        for line in f:
            line = line.replace("’", "'")
            fields = line.strip().split()
            token = fields[0]
            count = len(fields)

            if token in special:
                tlist = [special[token]]
            elif '-' in token:
                tlist = token.split('-')
                hyphens += 1
            elif '—' in token:
                tlist = token.split('—')
                hyphens += 1
            elif not token.isalpha():
                tlist = re.findall(r"\w+", token)
                # just get the alphabetic parts
            else:
                tlist = [token]

            legit_tlist = []

            for t in tlist:
                if len(t) < 2:
                    continue
                    # no single letters
                elif t in stopwords:
                    continue
                    # no stopwords
                else:
                    legit_tlist.append(t)
                    thisfilevocab.add(t)
            if len(legit_tlist) > 0 and count > 0:
                lineaslist = legit_tlist * count
                newline = ' '.join(lineaslist)
                outfile.append(newline)

    with open(targetdir + fil, mode = 'w', encoding = 'utf-8') as f:
        for line in outfile:
            f.write(line + '\n')

    # we create a vocabulary for each file and
    # add it in a separate step because
    # tokens in the file are broken out by page
    # not aggregated; if we added each line
    # we'd get pagefreq not docfreq.

    for token in thisfilevocab:
        docfreq[token] += 1


vocab = [x[0] for x in docfreq.most_common(30000)]

with open('vocab.txt', mode = 'w', encoding = 'utf-8'):
    for v in vocab:
        f.write(v + '\n')
