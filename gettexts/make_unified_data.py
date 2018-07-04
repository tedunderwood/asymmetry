import os, csv

lexicon = set()

with open('newvocab.tsv', encoding = 'utf-8') as f:
    reader = csv.reader(f, delimiter = '\t')
    for row in reader:
        if int(row[1]) > 49:
            lexicon.add(row[0])
        elif int(row[1]) < 49:
            break
        else:
            continue

print(len(lexicon))

allfiles = [x for x in os.listdir('finaldata') if x.endswith('.txt')]

for afile in allfiles:
    inpath = 'finaldata/' + afile
    outpath = 'unifieddata/' + afile

    inlex = []

    with open(inpath, encoding = 'utf-8') as f:
        for line in f:
            words = line.strip().split()
            if words[0] in lexicon:
                inlex.append(line)

    with open(outpath, mode = 'w', encoding = 'utf-8') as f:
        for line in inlex:
            f.write(line)


