import pandas as pd
import numpy as np
import random, sys, os
from scipy.stats import entropy
from scipy.spatial.distance import cosine

def get_kld_timelines(package):
    '''
    Calculates Kullback-Leibler divergence forward and back in time
    for a "segment" of rows in the metadata frame.

    Accepts as its argument a 3-tuple that should be:

    1 metadata DataFrame
    2 doc-topic proportions (data), as a DataFrame indexed by docid
    3 segment, a 2-tuple (startposition, endposition)

    Returns three objects:

    1 A set of three timelines for each volume. Each timeline records
    the average KLD at a temporal offsets from - 50 years to + 50 yrs.
    There are three different timelines for each vol, because we calculate
    the mean within different fractions of the total distribution: all
    the vols at that offset, the bottom 0.05 of klds, or the bottom
    0.025 of klds.

    2 summary statistics listing the novelty, transience, and resonance
    averaged over different timespans and fractions. For def of novelty,
    transience and resonance see Barron et al. (2018).

    3 cosine-distance calculated backward and forward in time. This is not
    something we're necessarily planning to use in the experiment, but
    it's here to permit various kinds of sanity checking.
    '''

    meta, data, segment = package
    start, end = segment

    klds4vols = dict()
    novtrares4vols = dict()
    cosines4vols = dict()
    cosnovtrares4vols = dict()

    fractions2check = [1.0, 0.2, 0.05, 0.025]

    timeradii2check = [10, 25, 40]

    for idx in range(start, end):
        row = meta.loc[idx, : ]
        date = int(row['latestcomp'])
        doc1 = row['docid']
        author1 = row['lastname']

        # There are some material changes from earlier versions here;
        # note the field names "latestcomp" (instead of inferreddate)
        # and "lastname" (instead of author).

        # The first of these is a move to better track dates of composition.
        # In cases where the author died before the book was published, we say
        # "latest possible date of composition" is the year of author death.
        # This affects a minority (less than 5%) of books in this corpus, since
        # the corpus is already deduplicated to the earliest example of a title in the
        # library. But it's worth doing the best we can with available evidence.

        # The second change is a move to be maximally conservative in avoiding
        # self-comparisons. Author names have a lot of finicky flourishes,
        # and though I've tried to standardize, it's possible that a middle
        # initial in one record is spelled out in another. But last names are
        # relatively invariant. We'll also miss a chance to compare Charles Dickens
        # to Monica Dickens (also a writer). But I think our data is robust
        # enough to survive loss of a small more-or-less random slice.

        klds4year = dict()
        cosines4year = dict()

        floor = date - 50
        if floor < 1800:
            floor = 1800
        ceiling = date + 51
        if ceiling > 2009:
            ceiling = 2009

        # The asymmetry there is because the central date itself
        # will not be counted as part of either the forward range
        # (1851-1900, inclusive) or the backward range (1800-1849, inclusive).
        # Yet python by default would assume that 1850 is included looking
        # forward. If we exclude it on both sides, we have to add one
        # to the endpoint.

        # First let's just calculate KLD for individual documents,
        # and organize those calculations by year.

        for yr in range (floor, ceiling):
            offset = yr - date
            klds4year[offset] = []
            cosines4year[offset] = []

            thisyear = meta.loc[meta.latestcomp == yr, : ]

            for idx2 in thisyear.index:
                author2 = thisyear.loc[idx2, 'lastname']
                doc2 = thisyear.loc[idx2, 'docid']

                if author1 == author2:
                    continue
                    # We don't check KLD btw vols with the same author.
                    # In practice, this means the same last name.

                if doc2 not in data.index:
                    continue

                ent = entropy(data.loc[doc1, : ], data.loc[doc2, : ])
                # NB the order of the two arguments for this function
                # matters! KL(a|b) ≠ KL(b|a).

                klds4year[offset].append(ent)

                cos = cosine(data.loc[doc1, : ], data.loc[doc2, : ])
                cosines4year[offset].append(cos)

        # Now to average kld by year. We will get different
        # averages when we consider different "fractions" of the range.

        avgkldbyyear = dict()
        avgcosbyyear = dict()

        for fraction in fractions2check:
            avgkldbyyear[fraction] = dict()
            avgcosbyyear[fraction] = dict()

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

            if i in cosines4year and len(cosines4year[i]) > 0:
                thecos = cosines4year[i]
                thecos.sort()
                for fraction in fractions2check:
                    cut = int(len(thecos) * fraction)
                    if cut < 1:
                        cut = 1
                    selectedgroup = thecos[0 : cut]
                    average = sum(selectedgroup) / len(selectedgroup)
                    avgcosbyyear[fraction][i] = average

        klds4vols[doc1] = avgkldbyyear
        cosines4vols[doc1] = avgcosbyyear

        # these arcs for different fractions will be written out in the "klds" files

        novelty = dict()
        transience = dict()
        resonance = dict()

        cosnovelty = dict()
        costransience = dict()
        cosresonance = dict()

        for fraction in fractions2check:
            novelty[fraction] = dict()
            transience[fraction] = dict()
            resonance[fraction] = dict()
            cosnovelty[fraction] = dict()
            costransience[fraction] = dict()
            cosresonance[fraction] = dict()

            for timeradius in timeradii2check:

                novsum = 0
                trasum = 0

                cosnovsum = 0
                costrasum = 0

                fullradius = True
                for i in range(-timeradius, 0):
                    if i in avgkldbyyear[fraction]:
                        novsum += avgkldbyyear[fraction][i]
                        cosnovsum += avgcosbyyear[fraction][i]
                    else:
                        fullradius = False

                if fullradius:
                    novelty[fraction][timeradius] = novsum / timeradius
                    cosnovelty[fraction][timeradius] = cosnovsum / timeradius
                else:
                    novelty[fraction][timeradius] = np.nan
                    cosnovelty[fraction][timeradius] = np.nan

                fullradius = True
                for i in range(1, timeradius + 1):
                    if i in avgkldbyyear[fraction]:
                        trasum += avgkldbyyear[fraction][i]
                        costrasum += avgcosbyyear[fraction][i]
                    else:
                        fullradius = False

                if fullradius:
                    transience[fraction][timeradius] = trasum / timeradius
                    costransience[fraction][timeradius] = costrasum / timeradius
                else:
                    transience[fraction][timeradius] = np.nan
                    costransience[fraction][timeradius] = np.nan

                resonance[fraction][timeradius] = novelty[fraction][timeradius] - transience[fraction][timeradius]

                cosresonance[fraction][timeradius] = cosnovelty[fraction][timeradius] - costransience[fraction][timeradius]

        novtrares4vols[doc1] = dict()
        cosnovtrares4vols[doc1] = dict()

        novtrares4vols[doc1]['novelty'] = novelty
        cosnovtrares4vols[doc1]['novelty'] = cosnovelty
        novtrares4vols[doc1]['transience'] = transience
        cosnovtrares4vols[doc1]['transience'] = costransience
        novtrares4vols[doc1]['resonance'] = resonance
        cosnovtrares4vols[doc1]['resonance'] = cosresonance

    return klds4vols, novtrares4vols, cosines4vols, cosnovtrares4vols

