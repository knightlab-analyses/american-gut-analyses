# Novelty

The goal is to count how many "unique" feature we see on a randomly selected number of samples.

A "unique" feature in the AGP context is a sOTU and the uniqueness is if they are a singleton, doubleton and so on.

# To run

You need a biom table and the pickles folder in where you are running your commands. Note that the number of
iterations (= 100, how many times we are gonna repeat each step), the steps (= 100, the number of samples we are
gonna select between steps), the max_ocurrances (= 11, the maximum number of "unique" features), and the
number of parallel jobs (= 64) are hardcoded in the script.

    $ curl -o deblur_125nt_no_blooms.biom ftp://ftp.microbio.me/AmericanGut/manuscript-package/1250/deblur_125nt_no_blooms.biom
    $ mkdir pickles
    $ novelty.py deblur_125nt_no_blooms.biom
    $ merge_pickles.py
    $ plot.py
