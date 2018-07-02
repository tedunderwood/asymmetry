batch scripts used to run MALLET
================================

The topic models used in this project were created using [MALLET,](http://mallet.cs.umass.edu) and run on a cluster where we have access to nodes with 128GB memory and 24 cores.

The best way to document the process appears to be preserving the batch scripts, which contain instructions to MALLET.

supplement inference
--------------------

After training the main model, it was necessary to infer topic distributions for several supplementary batches of volumes that are implicated by our pre-registered hypotheses but not contained in the (after all random) sample of volumes used in the topic model.

MALLET makes it possible to build topic-inferencers that do this work. The scripts guiding them have been preserved in a **supplementscripts** subfolder.
