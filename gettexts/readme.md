getting texts
=============

This is the code we used to get texts used in the experiment.

It was run initially to produce the sample of ~38,000 texts used in topic modeling.

Then, when we needed to supplement that list of texts in order to address specific hypotheses, we ran the code again, in order to create "supplement" folders. In producing our topic model with MALLET, we had also produced a ["topic inference tool"](http://mallet.cs.umass.edu/topics.php) that could predict topics for these new documents.

That permitted us to predict topic distributions for the new documents, and then calculate novelty/transience/resonance.

the process
-----------

Downloading and transforming data tends to be a messy process, and the code we provide here is not intended to make it replicable in a push-button way.

In particular, the process of actually getting the files is probably better explained on [the HathiTrust Extracted Feature page itself.](https://wiki.htrc.illinois.edu/display/COM/Extracted+Features+Dataset)

But once you've got the EF files, the next step is to run **unpackEF.py.** In our workflow, the process of getting the files is dependent on first creating a list of HT docids aligned with pairtree paths. (You can find examples of these lists in the **pathlist** subfolder.) We run **unpackEF** by passing one of these pathlists to it as a control-line argument. The command might be, for instance,

    python3 unpackEF.py pathlists/first_supplement_pathlist.tsv

That instructs the script to find the EF json files at the locations specified by the paths in first_supplement_pathlist, unpack them into text files, and write them at a location that I have right now awkwardly left as a hard-coded parameter inside unpackEF.py.

The next step is to run **clean_vocab.py**, which does a range of things, mainly ensure that one-character words are excluded, hyphenated words are split on the hyphen, etc. It would have been better to build some of this into the original unpackEF script, but that's not the way the process evolved, and we're not chiseling a workflow in marble that will endure for decades. So first I run **unpackEF** to fill one folder, then I use **clean_vocab** to move the cleaned files into a second folder. Then they are ready to be topic-modeled. For that part, see [the **batch_scripts/** folder.](https://github.com/tedunderwood/asymmetry/tree/master/batchscripts)


