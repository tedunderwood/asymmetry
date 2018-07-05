import pandas as pd
import numpy as np
import random, sys, os
from scipy.stats import entropy

def get_kld_timelines(package):
    '''
    Calculates Kullback-Leibler divergence forward and back in time
    for a "segment" of rows in the metadata frame.

    Accepts as its argument a 3-tuple that should be:

    1 metadata DataFrame
    2 doc-topic proportions (data), as a DataFrame indexed by docid
    3 segment, a 2-tuple (startposition, endposition)

    Returns three objects:

    1 A matrix that has a row for every vol in the segment, and a
    column for every vol in metadata. It records KLD at each intersection,
    with np.nan for missing data (combinations not checked).

    2 A set of three timelines for each volume. Each timeline records
    the average KLD at a temporal offsets from -50 years to + 50yrs.
    There are three different timelines for each vol, because we calculate
    the mean within different fractions of the total distribution: all
    the vols at that offset, the bottom 0.05 of klds, or the bottom
    0.025 of klds.

    3 summary statistics listing the novelty, transience, and resonance
    averaged over different timespans and fractions. For def of novelty,
    transience and resonance see Barron et al. (2018).
    '''

    meta, data, segment = package
    start, end = segment

    matrixwidth = meta.shape[0]

    matrix = dict()
    klds4vols = dict()
    novtrares4vols = dict()

    fractions2check = [1.0, 0.05, 0.025]
    timeradii2check = [10, 25, 40]

    for idx in range(start, end):
        row = meta.iloc[idx, : ]
        date = int(row['inferreddate'])
        doc1 = row['docid']
        author1 = row['author']

        klds4year = dict()
        matrixrow = np.zeros(matrixwidth)
        matrixrow.fill(np.nan)
        # we initialize to nan to indicate missing data

        floor = date - 50
        if floor < 1900:
            floor = 1900
        ceiling = date + 51
        if ceiling > 2009:
            ceiling = 2009

        for yr in range (floor, ceiling):
            offset = yr - date
            klds4year[offset] = []
            if offset == 0:
                continue

            thisyear = meta.loc[meta.inferreddate == yr, : ]

            for idx2 in thisyear.index:
                author2 = thisyear.loc[idx2, 'author']
                doc2 = thisyear.loc[idx2, 'docid']
                position = thisyear.loc[idx2, 'position']

                if author1 == author2:
                    continue
                    # We don't check KLD btw vols with the same author.

                if doc2 not in data.index:
                    continue

                ent = entropy(data.loc[doc1, : ], data.loc[doc2, : ])
                # NB the order of the two arguments for this function
                # matters! KL(a|b) ≠ KL(b|a).

                matrixrow[position] = ent

                klds4year[offset].append(ent)

        matrix[doc1] = matrixrow

        avgkldbyyear = dict()
        for fraction in fractions2check:
            avgkldbyyear[fraction] = dict()

        for i in range(-50, 51):
            if i in klds4year and len(klds4year[i]) > 0:
                thekl = klds4year[i]
                thekl.sort()
                for fraction in fractions2check:
                    cut = int(len(thekl) * fraction)
                    if cut < 1:
                        cut = 1
                    selectedgroup = thekl[0 : cut]
                    average = sum(selectedgroup) / len(selectedgroup)
                    avgkldbyyear[fraction][i] = average

        klds4vols[doc1] = avgkldbyyear

        novelty = dict()
        transience = dict()
        resonance = dict()

        for fraction in fractions2check:
            novelty[fraction] = dict()
            transience[fraction] = dict()
            resonance[fraction] = dict()

            for timeradius in timeradii2check:

                novsum = 0
                trasum = 0

                fullradius = True
                for i in range(-timeradius, 0):
                    if i in avgkldbyyear[fraction]:
                        novsum += avgkldbyyear[fraction][i]
                    else:
                        fullradius = False

                if fullradius:
                    novelty[fraction][timeradius] = novsum / timeradius
                else:
                    novelty[fraction][timeradius] = np.nan

                fullradius = True
                for i in range(1, timeradius + 1):
                    if i in avgkldbyyear[fraction]:
                        trasum += avgkldbyyear[fraction][i]
                    else:
                        fullradius = False

                if fullradius:
                    transience[fraction][timeradius] = trasum / timeradius
                else:
                    transience[fraction][timeradius] = np.nan

                resonance[fraction][timeradius] = novelty[fraction][timeradius] - transience[fraction][timeradius]

        novtrares4vols[doc1] = dict()

        novtrares4vols[doc1]['novelty'] = novelty
        novtrares4vols[doc1]['transience'] = transience
        novtrares4vols[doc1]['resonance'] = resonance

    return matrix, klds4vols, novtrares4vols

