#!/usr/bin/env python3

# unpackEF.py

# Based on
# parsefeaturejsons.py

# but with a basically different goal. This version
# of the script does not normalize features, and it
# writes the files to disk as a pseudo-text with
# words separated by spaces.

# it expects to have the following files living in the same
# folder:

# SonicScrewdriver.py
# CorrectionRules.txt
# VariantSpellings.txt

# Note that if you want to run this on your own machine,
# you will need to change the "rootpath," below --
# circa line 470 -- which is the
# folder where we expect to find Extracted Features living.

# Also, you'll need to create a metadata file that pairs
# docids with paths to the features.

# Example of USAGE:

# run parsefeaturejsons wholevolume ids2pathlist.tsv

import csv, os, sys, bz2, random, json
from collections import Counter

import numpy as np
import pandas as pd

# import utils
import SonicScrewdriver as utils

# By default, this script does spelling normalization according to
# rules that update archaic spelling and normalize to British where
# practice differs across the Atlantic.

# It also corrects ocr errors.

translator = dict()

with open('CorrectionRules.txt', encoding = 'utf-8') as f:
    reader = csv.reader(f, delimiter = '\t')
    for row in reader:
        if len(row) < 2:
            continue
        translator[row[0]] = row[1]

with open('VariantSpellings.txt', encoding = 'utf-8') as f:
    reader = csv.reader(f, delimiter = '\t')
    for row in reader:
        if len(row) < 2:
            continue
        translator[row[0]] = row[1]

stopwords = set()
with open('minimalstopwords.txt', encoding = 'utf-8') as f:
    for line in f:
        stopwords.add(line.strip())


def normalize_token(token):
    ''' Normalizes a token by lowercasing it and and splitting
    on the hyphen.
    '''

    token = token.lower()

    if len(token) < 1:
        return [token]
    elif token[0].isdigit() and token[-1].isdigit():
        return ["#arabicnumeral"]

    elif '-' in token:
        return token.split('-')
        # I never want to treat hyphenated words as distinct
        # features; for modeling it's preferable to count the
        # pieces
    else:
        return [token]

def add_feature(feature, count, features):
    ''' Adds feature-count to a dictionary
    if feature is already in the dictionary.
    '''

    if feature in features:
        features[feature] = count


class VolumeFromJson:

    # A data object that contains page-level wordcounts read from
    # json.

    # It normalizes wordcounts by lower-casing, and by folding certain
    # categories of word together; see normalize_token above.

    # It also includes functions that allow a volume to divide itself
    # according to instructions. E.g.: "volume, cut yourself into
    # three parts, after leaving out certain pages!"

    def __init__(self, volumepath, volumeid):
        '''Initializes a LoadedVolume by reading wordcounts from
        a json file. By default it reads all the pages. But if
        skip-front and skip-back are set to positive values,
        it will skip n pages.'''


        if volumepath.endswith('bz2'):
            with bz2.open(volumepath, mode = 'rt', encoding = 'utf-8') as f:
                thestring = f.read()
        else:
            with open(volumepath, encoding = 'utf-8') as f:
                thestring = f.read()

        thejson = json.loads(thestring)

        self.volumeid = thejson['id']

        pagedata = thejson['features']['pages']

        self.numpages = len(pagedata)
        self.pagecounts = []
        self.totalcounts = Counter()
        self.totaltokens = 0
        self.bodytokens = 0

        chunktokens = 0
        typesinthischunk = set()
        # a set of types in the current 10k-word chunk; progress
        # toward which is tracked by chunktokens

        self.integerless_pages = 0
        self.skipped_pages = 0
        compromise_pg = 0

        capitalizedbodytokens = 0

        for i in range(self.numpages):
            thispagecounts = Counter()
            thisbodytokens = 0
            thisheadertokens = 0
            thispage = pagedata[i]

            # There are really two ways of numbering pages. They come in an order,
            # which gives them an inherent ordinality (this is the *first* page). But
            # they also have cardinal *labels* attached, in the "seq" field. These labels
            # are usually, but not necessarily, convertible to integers. (Usually "00000001",
            # but could be "notes.") *Usually* they are == to the ordinal number,
            # but again, not necessarily! The world is full of fun edge cases!

            # In this loop, i is the ordinal page number, and cardinal_page is the cardinal
            # label; its value will be -1 if it can't be converted to an integer.

            # compromise_pg skips pages that have no integer seq, but otherwise
            # proceeds ordinally

            try:
                cardinal_page = int(thispage['seq'])
            except:
                cardinal_page = -1

            if cardinal_page > 0:
                compromise_pg += 1
            elif cardinal_page < 0:
                self.integerless_pages += 1

            if cardinal_page >= 0:

                bodywords = thispage['body']['tokenPosCount']
                for token, partsofspeech in bodywords.items():

                    normaltokenlist = normalize_token(token)

                    # Notice that we treat each word as a list, to permit
                    # counting both parts of a hyphenated word.
                    # But usually this will be a list of one.

                    for normaltoken in normaltokenlist:

                        for part, count in partsofspeech.items():
                            thisbodytokens += count
                            chunktokens += count
                            thispagecounts[normaltoken] += count


                headerwords = thispage['header']['tokenPosCount']
                for token, partsofspeech in headerwords.items():
                    normaltokenlist = normalize_token(token)

                    for normaltoken in normaltokenlist:
                        normaltoken = "#header" + normaltoken

                        for part, count in partsofspeech.items():
                            thisheadertokens += count
                            thispagecounts[normaltoken] += count

                # You will notice that I treat footers (mostly) as part of the body
                # Footers are rare, and rarely interesting.

                footerwords = thispage['footer']['tokenPosCount']
                for token, partsofspeech in footerwords.items():

                    normaltokenlist = normalize_token(token)

                    for normaltoken in normaltokenlist:

                        for part, count in partsofspeech.items():
                            thisbodytokens += count
                            chunktokens += count
                            thispagecounts[normaltoken] += count

                self.pagecounts.append(thispagecounts)

                for key, value in thispagecounts.items():
                    self.totalcounts[key] += value

                self.totaltokens += thisbodytokens
                self.totaltokens += thisheadertokens
                self.bodytokens += thisbodytokens

            else:
                # print(i, cardinal_page, compromise_pg)
                self.skipped_pages += 1

        # We are done with the __init__ method for this volume.

    def write_volume(self, outpath, folder, override = False, translator = dict(), use_headers = False, skip_front = 0, skip_back = 0):

        global stopwords

        ''' This writes volume text after using a translation table to normalize,
        e.g., British or archaic spelling.

        It can be instructed to skip a certain fraction of pages at the front or back of the volume.

        It can also be instructed to split a volume into parts, although I'm
        not currently using that feature. 38,000 documents is plenty.
        '''

        startposition = int(skip_front * len(self.pagecounts))
        endposition = len(self.pagecounts) - int(skip_back * len(self.pagecounts))

        if startposition > endposition:
            print('Error in page trimming')
            sys.exit(0)

        pagedata = self.pagecounts[startposition: endposition]

        totaltokens = 0

        with open(outpath, mode = 'w', encoding = 'utf-8') as f:
            for page in pagedata:
                for token, count in page.items():
                    if token.startswith('#header') and not use_headers:
                        continue
                    elif len(token) < 1:
                        continue
                    elif len(token) < 2 and not token[0].isalpha():
                        continue
                    elif token in translator:
                        token = translator[token]

                    if token in stopwords:
                        continue

                    f.write(' '.join([token] * count) + '\n')

                    totaltokens += count

        metarow = dict()
        metarow['docid'] = outpath.replace('.txt', '').replace(folder, '')
        metarow['path'] = outpath
        metarow['totaltokens'] = totaltokens
        metarow['skipped_pages'] = self.skipped_pages
        metarow['trimmed_pages'] = int(skip_front * len(self.pagecounts)) + int(skip_back * len(self.pagecounts))

        return metarow

if __name__ == "__main__":

    args = sys.argv


    # The root path where volumes are stored is hard-coded here:

    rootpath = '/Volumes/TARDIS/work/ef/fic/'
    outfolder = '/Users/tunder/work/influencedata/'

    # You will need to change that if you're using it on your own machine.

    if len(args) < 2:
        print('This script requires a command-line argument:')
        print('a metadata file to use.')
        sys.exit(0)

    else:
        missing = 0
        path_to_meta = args[1]
        all_outrows = []

        meta = pd.read_csv(path_to_meta, dtype = 'object', index_col = 'docid', sep = '\t')
        ctr = 0

        for index, row in meta.iterrows():
            ctr += 1
            if ctr % 100 == 1:
                print(ctr)

            inpath = rootpath + row['path']
            if not os.path.isfile(inpath):
                missing += 1
                print('missing')
            else:
                vol = VolumeFromJson(inpath, index)
                outpath = outfolder + utils.clean_pairtree(index) + '.txt'
                metarow = vol.write_volume(outpath, folder = outfolder, override = True, translator = translator, use_headers = False, skip_front = .1, skip_back = 0.05)
                all_outrows.append(metarow)

        print(missing)

        columns = ['docid', 'htid', 'totaltokens', 'skipped_pages', 'trimmed_pages', 'path']
        with open('parsing_metadata.tsv', mode = 'w', encoding = 'utf-8') as f:
            scribe = csv.DictWriter(f, fieldnames = columns, delimiter = '\t')
            scribe.writeheader()

            for row in all_outrows:
                scribe.writerow(row)




