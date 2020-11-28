# Calculate kld for supplement4 model

# This is based on previous calculate-kld scripts,
# but substantially revised in 2020 to address a different
# research question

import pandas as pd
import numpy as np
import random, sys, os
from multiprocessing import Pool
import kld_calc_worker_supp4 as kcw

numthreads = 12
# this can be changed if you like

measures2check = ['novelty', 'transience', 'resonance']
fractions2check = [1.0, 0.2, 0.05, 0.025]
timeradii2check = [10, 25, 40]
chunksize = 2000

meta = pd.read_csv('../meta/supp3allmeta.tsv', sep = '\t')
data = pd.read_csv('../supp3model/supp3_doc_topics.tsv', sep = '\t', index_col = 'docid')

totalvols = meta.shape[0]

startposition = int(sys.argv[1])
endposition = startposition + chunksize
if endposition > totalvols:
    endposition = totalvols

print(startposition, endposition)

outputname = 'supp4_' + str(startposition)
cosinefile = '../results/' + outputname + 'cosines.tsv'
kldsfile = '../results/' + outputname + 'klds.tsv'
summaryfile = '../results/' + outputname + 'summary.tsv'
cossummaryfile = '../results/' + outputname + 'cossummary.tsv'

segments = []
increment = ((endposition - startposition) // numthreads) + 1
for floor in range(startposition, endposition, increment):
    ceiling = floor + increment
    if ceiling > endposition:
        ceiling = endposition
    segments.append((floor, ceiling))

packages = []
for segment in segments:
    package = (meta, data, segment)
    packages.append(package)

print('Beginning multiprocessing.')
pool = Pool(processes = numthreads)

res = pool.map_async(kcw.get_kld_timelines, packages)
res.wait()
resultlist = res.get()
pool.close()
pool.join()
print('Multiprocessing concluded.')

for result in resultlist:
    klds4vols, novtrares4vols, cosines4vols, cosnovtrares4vols = result

    if not os.path.isfile(kldsfile):
        with open(kldsfile, mode = 'w', encoding = 'utf-8') as f:
            header = 'docid' + '\t' + 'fraction' + '\t' + '\t'.join([str(x) for x in range(-50, 51)]) + '\n'
            f.write(header)

    if not os.path.isfile(summaryfile):
        with open(summaryfile, mode = 'w', encoding = 'utf-8') as f:
            outlist = ['docid']
            for measure in measures2check:
                for frac in fractions2check:
                    for radius in timeradii2check:
                        outlist.append(measure + '_' + str(frac) + '_' + str(radius))
            header = '\t'.join(outlist) + '\n'
            f.write(header)

    if not os.path.isfile(cosinefile):
        with open(cosinefile, mode = 'w', encoding = 'utf-8') as f:
            header = 'docid' + '\t' + 'fraction' + '\t' + '\t'.join([str(x) for x in range(-50, 51)]) + '\n'
            f.write(header)

    if not os.path.isfile(cossummaryfile):
        with open(cossummaryfile, mode = 'w', encoding = 'utf-8') as f:
            outlist = ['docid']
            for measure in measures2check:
                for frac in fractions2check:
                    for radius in timeradii2check:
                        outlist.append(measure + '_' + str(frac) + '_' + str(radius))
            header = '\t'.join(outlist) + '\n'
            f.write(header)

    with open(cosinefile, mode = 'a', encoding = 'utf-8') as f:
        for docid, cosdict in cosines4vols.items():
            for frac in fractions2check:
                outlist = [docid, frac]
                for i in range(-50, 51):
                    if i in cosdict[frac]:
                        outlist.append(cosdict[frac][i])
                    else:
                        outlist.append(np.nan)

                outline = '\t'.join([str(x) for x in outlist]) + '\n'
                f.write(outline)

    with open(kldsfile, mode = 'a', encoding = 'utf-8') as f:
        for docid, klddict in klds4vols.items():
            for frac in fractions2check:
                outlist = [docid, frac]
                for i in range(-50, 51):
                    if i in klddict[frac]:
                        outlist.append(klddict[frac][i])
                    else:
                        outlist.append(np.nan)

                outline = '\t'.join([str(x) for x in outlist]) + '\n'
                f.write(outline)


    with open(summaryfile, mode = 'a', encoding = 'utf-8') as f:
        for docid, summary in novtrares4vols.items():
            outlist = [docid]
            for measure in measures2check:
                for frac in fractions2check:
                    for radius in timeradii2check:
                        outlist.append(summary[measure][frac][radius])

            outline = '\t'.join([str(x) for x in outlist]) + '\n'
            f.write(outline)

    with open(cossummaryfile, mode = 'a', encoding = 'utf-8') as f:
        for docid, summary in cosnovtrares4vols.items():
            outlist = [docid]
            for measure in measures2check:
                for frac in fractions2check:
                    for radius in timeradii2check:
                        outlist.append(summary[measure][frac][radius])

            outline = '\t'.join([str(x) for x in outlist]) + '\n'
            f.write(outline)



