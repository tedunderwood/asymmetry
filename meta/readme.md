metadata
=========

If you're looking for the original sources of our lists of volumes in particular anthologies, or "most discussed" on JSTOR, most of that is in the subdirectory ```/canon.```

The metadata most immediately used in the calculations supporting "Can We Map Culture?" is **thirdmastermeta.tsv.** This file merges HathiTrust metadata with columns that identify volumes in particular treatment categories, and also in "contrast sets" selected to match the nationality and date distribution of the treatment categories.

A closely related table (but lacking the enriched columns to test particular hypotheses) is **supp3allmeta.tsv.**

earlier versions of metadata
----------------------------

**topicsample.tsv** is the metadata originally selected for topic modeling. 38,653 volumes, selected from a deduplicated sample (workmeta.tsv in the noveltmmeta repo), and evenly distributed across time 1800-2009, except that they're a little sparse before 1830. Typically with a sample this large you lose some for various reasons (not actually present in EF, etc). So ...

**filteredsample.tsv** are the volumes I actually had available for topic modeling--the ones present in the model.

**lastnamesample.tsv** is a further evolution of filteredsample; basically, it just adds a column for **lastname,** so we can use last names to forbid comparisons and thus very conservatively avoid the risk that an author might be compared to her own future (or past) publications.

**unified_sample.tsv** is the union of **lastnamesample** and **../supplement1/lastnamesupp1meta.tsv**; it documents volumes used in the unified model that folded in about 873 vols from **prestigeficmeta.**
