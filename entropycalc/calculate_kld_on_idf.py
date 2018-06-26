# calculate_kld_on_idf.py

# This version of calculate_kld is designed to work
# on idfvectors.

import pandas as pd
import numpy as np
import random, sys, os
from multiprocessing import Pool
import kld_calc_worker as kcw

numthreads = 12
# this can be changed if you like

measures2check = ['novelty', 'transience', 'resonance']
fractions2check = [1.0, 0.05, 0.025]
timeradii2check = [10, 25, 40]
chunksize = 2000

meta = pd.read_csv('../meta/filteredsample.tsv', sep = '\t')
data = pd.read_csv('../model/idfvectors.tsv', sep = '\t', index_col = 'docid')

totalvols = meta.shape[0]

startposition = int(sys.argv[1])
endposition = startposition + chunksize
if endposition > totalvols:
    endposition = totalvols

print(startposition, endposition)

outputname = 'seg' + str(startposition)
matrixfile = '../idfresults/' + outputname + 'matrix.tsv'
kldsfile = '../idfresults/' + outputname + 'klds.tsv'
summaryfile = '../idfresults/' + outputname + 'summary.tsv'

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
    matrix, klds4vols, novtrares4vols = result

    if not os.path.isfile(matrixfile):
        with open(matrixfile, mode = 'w', encoding = 'utf-8') as f:
            header = 'docid' + '\t' + '\t'.join([str(x) for x in range(0, totalvols)]) + '\n'
            f.write(header)

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

    with open(matrixfile, mode = 'a', encoding = 'utf-8') as f:
        for docid, row in matrix.items():
            outrow = docid + '\t' + '\t'.join([str(x) for x in row]) + '\n'
            f.write(outrow)

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




