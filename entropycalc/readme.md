entropy calculations
====================

Once the collection has been topic-modeled, these are the scripts that actually calculate "novelty," "transience," and "resonance.""

All of those concepts are variations on Kullback-Leibler divergence, so the key script is **calculate_kld.py**.

We have to calculate KLD for each of 38,000 volumes within a 100-year window, which is to say, against roughly 19,000 volumes. 38k x 19k is almost a billion calculations, each of which is nontrivial in itself, so ... I needed to send this to the cluster, break it into multiple batch jobs, and also make sure I was using all the cores *within* each cluster node!

I used multiprocessing. **calculate_kld.py** starts a Pool and each process in the pool calls **kld_calc_worker.py** with a particular segment of volumes to calculate.

Each batch job produces three files. A *matrix* which records kld for each comparison, a *klds* file which records the mean kld at each offset backward and forward in time (for each volume), and a *summary* file which records overall novelty, transience, and resonance for each volume.

variants
--------

The description above covers the main workflow, but I found I needed to repeat this for several other branches of inquiry. Most of these are pursuing questions not central to the main project.

**calculate_kld_on_idf.py** was used to calculate novelty, etc on tf-idf vectors, because I was suspicious about temporal distortion created by topic modeling itself. It calls **kld_calc_worker2.py**.

**calculate_20_kld.py** calculates novelty/transience/resonance on a 20c-specific model, again because I was getting suspicious about the "novelty mountain" effect. It calls **kld_calc_worker_20c.py**

**calculate_19_kld.py** calculates novelty etc on a 19c-specific model. But it *also* diverges from previous scripts in replacing the matrix with cosine calculations.

**calculate_unified_kld.py** is designed to work with the new unified corpus. This entails some changes to field names (e.g. earliestdate rather than inferreddate). I'm also being very cautious about self-comparison, excluding any pairs of works by authors with the same last name. Also, cosine calculations are inherited from the 19th-century script.

Ideally, I would refactor the workflow to generalize and stop spinning off variants like this. But I'm still in exploration mode and don't yet know what needs to be generalized.
