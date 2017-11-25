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
