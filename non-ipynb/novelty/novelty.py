from biom import load_table
from random import sample
import numpy as np
import pandas as pd
import seaborn as sns
from joblib import Parallel, delayed
from sys import argv

if len(argv) != 2:
    raise ValueError('No biom passed')

print (argv[1])
biom_table = load_table(argv[1])
biom_table.del_metadata()

iterations = 100
step = 100
max_occurrences = 11

def calculate(iterations, biom_table, samples_to_select, max_occurrences):
    """Calculate the number of features with up to max_occurrences features in
    samples_to_select samples

    Parameters
    ----------
    iterations : int
        Times each step should be repeated
    biom_table : biom.table.Table
        Biom table that we need to process
    samples_to_select : int
        Number of samples we need to select in each iteration
    max_occurrences : int
        Number of feature ocurrences so a sample is selected

    Returns
    -------
    A pickle of the results, with cols:
    max_ocurrances, samples_to_select, uniques
    """
    sids = list(biom_table.ids())
    results = []
    for i in range(iterations):
        samples = sample(sids, samples_to_select)
        data = biom_table.data(samples.pop())
        for row in samples:
            data += biom_table.data(row)
        data = data[(data >= 1) & (data <= max_occurrences)]
        results.append((1, (max_occurrences, samples_to_select, len(data))))
    fp = 'pickles/samples_to_select-%d_max_occurrences-%d.pickle' % (
        samples_to_select, max_occurrences)
    results_df = pd.DataFrame.from_items(
        results, orient='index',
        columns=['max_occurrences', 'samples_to_select', 'uniques'])
    results_df.to_pickle(fp)
    return results

steps = range(step, len(biom_table.ids()), step)
print (len(biom_table.ids()))

results = Parallel(n_jobs=64)(
    delayed(calculate)(
        iterations, biom_table, samples_to_select, i)
        for samples_to_select in steps for i in range(1, max_occurrences))
