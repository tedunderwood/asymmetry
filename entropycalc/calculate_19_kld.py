import pandas as pd
import numpy as np
import random, sys, os
from multiprocessing import Pool
import kld_calc_worker_19c as kcw

numthreads = 12
# this can be changed if you like

measures2check = ['novelty', 'transience', 'resonance']
fractions2check = [1.0, 0.05, 0.025]
timeradii2check = [10, 25, 40]
chunksize = 2500

meta = pd.read_csv('../meta/filtered19csample.tsv', sep = '\t')
data = pd.read_csv('../model/19th_doc_topics.tsv', sep = '\t', index_col = 'docid')

totalvols = meta.shape[0]

startposition = int(sys.argv[1])
endposition = startposition + chunksize
if endposition > totalvols:
    endposition = totalvols

print(startposition, endposition)

outputname = 'seg' + str(startposition)
cosinefile = '../results/' + outputname + 'cosines.tsv'
kldsfile = '../results/' + outputname + 'klds.tsv'
summaryfile = '../results/' + outputname + 'summary.tsv'

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
    klds4vols, novtrares4vols, cosines4vols = result

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
            header = 'docid\t' + 'backward\t' + 'forward\n'
            f.write(header)

    with open(cosinefile, mode = 'a', encoding = 'utf-8') as f:
        for docid, costuple in cosines4vols.items():
            backward, forward = costuple
            outrow = docid + '\t' + backward + '\t' + forward + '\n'
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




