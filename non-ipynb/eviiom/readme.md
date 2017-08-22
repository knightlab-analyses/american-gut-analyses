# Phylogenetic organization to metabolites

This analysis depends on two environments, first one composed of [scikit-bio >= 0.5.0](http://scikit-bio.org/), [biom-format >= 2.1.5](http://biom-format.org/), [joblib](https://pythonhosted.org/joblib/), [iow](https://pypi.python.org/pypi/iow) and [click](http://click.pocoo.org/5/).. And second, one composed of [QIIME v1.9.1](http://qiime.org/). The `commands.sh` script expects the first environment to be named `sk050-biom215` and the second to be named `qiime191`. 

# 16S Data

The AG 150nt 16S dataset was used for this analysis, filtered to the samples with HPLC-MS data, with bloom features removed, samples with fewer than 1000 sequences removed, and singletons/doubletons removed.

# HPLC-MS Data

It assumes the HPLC-MS data are represented as BIOM, are unnormalied, and filtered to remove features correlated to blooms and correlated to the AGP swabs.

# To run

    $ cd bin
    $ sh commands.sh
