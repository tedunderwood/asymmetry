data about the topic model
==========================

We produced the topic model using MALLET. For details of the scripts involved, see the /batchscripts directory.

Our approach to modeling was shaped by [Schofield, Magnusson, and Mimno (2017)](http://www.cs.cornell.edu/~xanda/stopwords2017.pdf), which reports that "beyond high-probability terms, the effects of stoplists on training are limited, and that removing unwanted terms after training should be sufficient."

In other words, long lists of stopwords don't really improve the underlying partitioning of the corpus. They simply make topics *look* better by removing very common (or rare) terms; this makes it easier for the human eye to scan a keyword list. But if that's our goal, it can be achieved just as well by removing stopwords from the keyword list *after* training.

We have accordingly written a Python script (**translate_keys.py**) that quite simply filters the list of topic keys by rejecting extremely common or rare words (unless all the words in the topic are extremely common or rare).

The original list of keys is in **keys.txt**; the translated list is in **filtered_keys.txt**.

topic distributions
-------------------

Much of the analysis we perform relies on "a doctopics file"--a table that indicates the distribution of each volume across the topics in the model.

These files run ~400MB--too large to fit comfortably in a github repo. So for the moment, we are simply providing Dropbox links here to download the files.

The raw doctopics file produced by MALLET: [https://www.dropbox.com/s/qsuhh1yiqd118jj/doctopics.txt?dl=0](https://www.dropbox.com/s/qsuhh1yiqd118jj/doctopics.txt?dl=0)

To make exploratory data analysis easier, we translate the raw doctopics file into a pandas-friendly version. The key change here is to simplify the row index, making it identical to "docid"s in our metadata by removing paths and reunifying some long volumes that got split into 2-3 parts for modeling. The translation is done by **translate_doctopics.py**

The "translated" doctopics file: [https://www.dropbox.com/s/ljc3iauco9jm53d/doc_topics.tsv?dl=0](https://www.dropbox.com/s/ljc3iauco9jm53d/doc_topics.tsv?dl=0)

variant models
---------------

Here I am describing files that you won't yet see in the repo (because they're too large), but that I need to keep track of locally.

The generic "doc_topics.tsv" file described above is based on a model that used all 38,583 volumes in the random sample, and only those volumes. This model has 500 topics, produced using the optimize-priors option in MALLET.

There's also a 19th_doc_topics.tsv and 20th_doc_topics.tsv, produced using volumes from 1800 - 1914 and 1900-2009, respectively. The 20c one uses 500 topics; the 19c one (for no particular reason) 400.

Finally, there's a unified_doc_topics.tsv, which combines the 38,583 randomly-selected volumes with 873 volumes in **../supplement1/lastnamesupp1meta.tsv** (mostly volumes from the reviewed/random prestige fiction dataset.) This model has 400 topics, produced using optimized priors, and a total of 39,456 rows.
