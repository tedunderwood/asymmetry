Dictionary for thirdmastermeta.tsv
==================================

The metadata included in the table can be divided into two broad categories: basic metadata for the volume (including a lot of inferred demographics about the author) and columns that mark volumes as belonging to sets used for testing hypotheses.

basic metadata
--------------

**docid** The index for the table; should be unique for each row.

**allcopiesofwork** How many copies with the same author/title were found in HathiTrust?

**copiesin25yrs** Same question, except limited to the 25 years after the first copy we found (which should be this copy).

**author** Derived from HathiTrust, with some normalization. Blank in some cases.

**earlyedition** Will be True in most casers, but False where the date of publication significantly postdates the author's death. Could be used to further filter metadata.

**imprint** Place of publication | publisher | date. Sometimes semicolons are used as delimiters here, sometimes pipes.

**inferreddate** A date inferred fairly directly from the Hathi record: as far as we can tell, when was this volume actually published.

**lastname** Used to prevent comparing an author to herself in entropy calculations. Where author name is blank we invent a unique "anonymous" + integer key.

**latestcomp** Latest possible date of composition. This is the date that should be used for most purposes in our analysis.

**nationality** Everything we know about nationality. When actual nationality is not known, we infer (from publication places associated with the author) a "guess: us" or "guess: non-us."

**isusa** Simplifies the previous column to a 0/1 binary that could be used in regression.

**actualgender** In rare cases where we know it.

**likelygender** Which is either actualgender or a probabilistic inference from Gender-ID.py, by Bridget Baird and Cameron Blevins.

**title** May not be exactly == to title listed in Hathi, because we have tried to update where more precise titles are known for e.g. "Collected Works."

**authordate** Usually inferred from Hathi, sometimes from manual correction.

**birth** The birth year from authordate.

**age** Latestcomp - birth.

**recordid** Could be used to get other vols of a multivolume set.

samples for testing hypotheses
-------------------------------

These columns contain either 0 (volume is not in the category) or 1 (it is).

Almost all of these columns are paired, with some volumes in a "hypothesis" set and others in a (disjoint) "contrast" set. Volumes in the contrast set are selected one by one to match the "isusa" and "latestcomp" flags of the hypothesis volumes as closely as possible. This system is designed to allow us to test the hypotheses using matching methods to control confounding.

Note that books by *authors* in the hypothesis set are excluded from the contrast set. Also note that (most of) the contrast sets are selected from a manually groomed sample of about 1200 books—groomed both to exclude most juvenile fiction & nonfiction, and to improve the accuracy of dating. These are efforts to make the contrast sets as close as possible to the hypothesis sets, which are usually selected from adult fiction and dated manually.

**best1821_1900** (and **best1821_1900contrast**): Books reported as bestsellers, before 1900. Before 1895, this usually means the book was *perceived* as a best seller; it's rarely based on actual sales figures.

**best1900_1950** (and contrast) A sample of bestsellers 1900-1949, almost all US.

**best1950_1990** (and contrast) A sample of bestsellers 1950-89, almost all US. Note that 20 years on either end of the timeline are excluded from these sets.

**anybest** All volumes reported as bestsellers. Note that this category is larger than the sum of the previous three, because the dated categories of bestsellers are "throttled down" to a cap of 140 vols by the difficulty of getting a contrast set that matches date/nationality. For the same reason, there is no contrast set for **anybest** itself.

**reviewed1850-1950** Vols selected manually from reviews in elite periodicals; work by Jordan Sellers, Jessica Mercado, and Sabrina Lee is reflected here.

**reviewed1850-1950contrast** Listed separately because it's generated a little differently; manually selected volume by volume to match nationality and date in the previous set. Other contrast sets were generated automatically.

**heath** (and contrast) American fiction published by Heath.

**usnorton** (and contrast) American fiction (and a small amount of short fiction) published by Norton.

**nonusnorton** (and contrast) Non-US fiction (and some short fiction) published by Norton.

**mostdiscussed** (and contrast) Based on Richard So's list of works of American fiction most discussed in academic journals.

**preregistered** (and contrast) Our list of 20 preregistered volumes.

**reviewed1965-1990** (and contrast) Based on Richard So's list of most widely reviewed fiction.

**toremove** A flag suggesting that this volume might be removed if we produced a fourth model; often these are actually works of nonfiction.
