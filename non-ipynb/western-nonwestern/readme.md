# Dependencies

For this analysis, we're going to need two environments: a Python3 QIIME2 one and a Python2 one to utilize part of Qiita. We'll manage environments using [conda](https://anaconda.org/).

The Python3 environment will need to contain:

- QIIME2 [2017.4.0](https://docs.qiime2.org/2017.4/install/), note: later versions of QIIME2 should be fine as well
- q2-state-unifrac [master](https://github.com/wasade/q2-state-unifrac)

The Python2 environment will need to contain:

- QIIME [1.9.1](http://qiime.org/install/install.html)

# Data sources

Demux files were obtained from [Qiita](https://qiita.ucsd.edu) for the non-AGP data sets. Specifically:

    - [Yatsunenko et al. 2012 Nature](https://qiita.ucsd.edu/study/description/850)
    - [Clemente et al. 2015 Sci. Adv.](https://qiita.ucsd.edu/study/description/10052)
    - [Obregon-Tito et al. 2015 Nat. Comm.](https://qiita.ucsd.edu/study/description/1448)
