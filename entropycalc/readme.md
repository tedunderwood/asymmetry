entropy calculations
====================

Once the collection has been topic-modeled, these are the scripts that actually calculate "novelty," "transience," and "resonance.""

All of those concepts are variations of cross-entropy, or Kullback-Leibler divergence, so the key script is **calculate_kld.py**.

We have to calculate KLD for each of 38,000 volumes within a 100-year window, which is to say, against roughly 19,000 volumes. 38k x 19k is almost a billion calculations, each of which is nontrivial in itself, so ... I needed to send this to the cluster, break it into multiple batch jobs, and also make sure I was using all the cores *within* each cluster node!

I used multiprocessing. **calculate_kld.py** starts a Pool and each process in the pool calls **kld_calc_worker.py** with a particular segment of volumes to calculate.

Each batch job produces three files. A *matrix* which records kld for each comparison, a *klds* file which records the mean kld at each offset backward and forward in time (for each volume), and a *summary* file which records overall novelty, transience, and resonance for each volume.
