data about the topic model
==========================

We produced the topic model using MALLET. For details of the scripts involved, see the /batchscripts directory.

Our approach to modeling was shaped by [Schofield, Magnusson, and Mimno (2017)](http://www.cs.cornell.edu/~xanda/stopwords2017.pdf), which reports that "beyond high-probability terms, the effects of stoplists on training are limited, and that removing unwanted terms after training should be sufficient."

In other words, long lists of stopwords don't really improve the underlying partitioning of the corpus. They simply make topics *look* better by removing very common (or rare) terms; this makes it easier for the human eye to scan a keyword list. But if that's our goal, it can be achieved just as well by removing stopwords from the keyword list *after* training.

We have accordingly written a Python script (**translate_keys.py**) that quite simply filters the list of topic keys by rejecting extremely common or rare words (unless all the words in the topic are extremely common or rare).

The original list of keys is in **keys.txt**; the translated list is in **filtered_keys.txt**.
