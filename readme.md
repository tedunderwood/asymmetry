Temporal asymmetries in fiction
================================

Ted Underwood and Richard Jean So. "Temporal asymmetries" is our cautious name for a project investigating the information-theoretic measures that [Barron et al (2018)](http://www.pnas.org/content/early/2018/04/16/1717729115) use to track innovation in French Revolutionary debates.

We're asking whether the same measures can be used to illuminate literary history across a much longer timeline (1800-2009). We also seek to validate these measures of asymmetry by correlating them with familiar social measures of prominence and influence.

Initial hypotheses for this experiment [have been preregistered with OSF.](https://osf.io/zuq9a/register/5771ca429ad5a1020de2872e)

The project is ongoing and might lead to more than one publication, but this state/version of the repository is organized primarily to support "Can We Map Culture?" (currently under consideration at *The Journal of Cultural Analytics.*)

The analysis and visualization scripts supporting that article in particular are gathered in the directory [```/mapculture.```](https://github.com/tedunderwood/asymmetry/tree/master/mapculture) But to understand how metadata was constructed, you may need to follow trails of breadcrumbs that lead from that directory to other parts of this repo.

meta
----

Contains metadata for volumes of fiction used in the project.

gettexts
--------

The texts we use are drawn ultimately from [HathiTrust Extracted Features.](https://wiki.htrc.illinois.edu/display/COM/Extracted+Features+Dataset) This folder contains code used to unpack those feature files into flat files that can be topic-modeled.

entropycalc
-----------

Python scripts we used to calculate KL divergence and cosine symmetry on pairs of volumes, and to aggregate the results. Note that the specific scripts used for the most recent version of the project (reflected in "Can We Map Culture?") are also present in ```/mapculture.```

batchscripts
------------
PBS and SLURM scripts we used to parallelize the ```entropycalc``` scripts across a cluster.
