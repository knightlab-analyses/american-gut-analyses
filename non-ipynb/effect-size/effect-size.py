#!/usr/bin/env python

import click
import joblib
import pickle

import pandas as pd
import numpy as np

from os import mkdir
from os.path import join, isdir, basename, exists
from itertools import combinations
from operator import itemgetter
from functools import partial
from skbio import DistanceMatrix
from skbio.stats.distance import permanova
from scipy.stats import mannwhitneyu, spearmanr


NA_VALUES = ['nan', 'Not applicable', 'Missing: Not provided', 'None']


@click.option('--mappings', multiple=True, type=click.Path(exists=True),
              help='mapping directory filepath')
@click.option('--alphas', multiple=True, type=click.Path(exists=True),
              help='alpha directory filepath')
@click.option('--betas', multiple=True, type=click.Path(exists=True),
              help='beta directory filepath')
@click.option('--output', type=click.Path(exists=False),
              help='output filepath')
@click.option('--jobs', type=click.IntRange(1, 64), default=1,
              help='jobs to start')
@click.option('--permutations', type=click.IntRange(10, 10000), default=10,
              help='jobs to start')
@click.option('--alpha-method', type=click.Choice(['mannwhitneyu', 'spearmanr']),
              default='mannwhitneyu')
@click.command()
def effect_size(mappings, alphas, betas, output, jobs, permutations,
                alpha_method):
    if not mappings:
        raise ValueError("You need to pass a mappings")
    if not alphas and not betas:
        raise ValueError("You need to pass either alphas or betas")
    if alphas and betas:
        raise ValueError("You can't pass both alphas and betas")
    if output is None:
        raise ValueError("You need to pass a output")

    if not isdir(output):
        mkdir(output)

    # As we can have multiple mapping, alpha or files, we will construct a mfs
    # dictionary with all the dataframes. Additionally, we will load the
    # data_dictionary.csv file so we can use it to process the data
    mappings = {f: pd.read_csv(f, sep='\t', dtype=str, na_values=NA_VALUES)
                for f in mappings}
    for m, mf in mappings.items():
        mappings[m].set_index('#SampleID', inplace=True)
    if betas:
        betas = {f: DistanceMatrix.read(f) for f in betas}
        print (
            'maps: %d, betas: %d, cols: %s' % (
                len(mappings), len(betas), [
                    len(m.columns.values) for _, m in mappings.items()]))

        with joblib.parallel.Parallel(n_jobs=jobs, verbose=100) as par:
            par(joblib.delayed(
                _process_column)(bf, c, fname, method)
                for bf, c, fname, method in _generate_betas(
                    betas, mappings, permutations, output))
    else:
        alphas = {f: pd.read_csv(f, sep='\t', dtype=str, na_values=NA_VALUES)
                  for f in alphas}
        for a, af in alphas.items():
            alphas[a].set_index('#SampleID', inplace=True)

        for af, c, fname, method in _generate_alphas(alphas, mappings,
                                                     output, alpha_method):
            _process_column(af, c, fname, method)


def _beta(permutations, data, xvalues, yvalues):
    x_ids = list(xvalues.index.values)
    y_ids = list(yvalues.index.values)
    ids = x_ids + y_ids
    data_test = data.filter(ids)
    permanova_result = permanova(
        distance_matrix=data_test,
        # we can use use either x or y cause they are the same
        column=xvalues.name,
        grouping=pd.concat([xvalues, yvalues]).to_frame(),
        permutations=permutations).to_dict()
    xvals = list(
        data_test.filter(xvalues.index.values).to_series().dropna().values)
    yvals = list(
        data_test.filter(yvalues.index.values).to_series().dropna().values)
    return (permanova_result['p-value'], permanova_result['test statistic'],
            xvals, yvals)


def _alpha(alpha_method, data, xvalues, yvalues):
    x_data = data.loc[xvalues.index.values].dropna().tolist()
    y_data = data.loc[yvalues.index.values].dropna().tolist()
    to_trim = np.min([len(x_data), len(y_data)])
    if alpha_method == 'mannwhitneyu':
        stat, pval = mannwhitneyu(x_data, y_data)
    else:
        x_data = np.random.choice(x_data, size=to_trim, replace=False)
        y_data = np.random.choice(y_data, size=to_trim, replace=False)
        stat, pval = spearmanr(x_data, y_data)
    return pval, stat, x_data, y_data


def _generate_betas(betas, mappings, permutations, output):
    method = partial(_beta, permutations)
    for beta, bf in betas.items():
        bfp = basename(beta)
        for mapping, mf in mappings.items():
            mfp = basename(mapping)
            for col in mf.columns.values:
                fname = join(output, '%s.%s.%s.%d.pickle' % (
                    bfp, mfp, col, permutations))
                if not exists(fname):
                    yield (bf, mf[col].dropna(), fname, method)


def _generate_alphas(alphas, mappings, output, alpha_method):
    method = partial(_alpha, alpha_method)
    for alpha, af in alphas.items():
        afp = basename(alpha)
        for ac in af.columns.values:
            for mapping, mf in mappings.items():
                mfp = basename(mapping)
                for col in mf.columns.values:
                    fname = join(output, '%s.%s.%s.%s.%s.pickle' % (
                        alpha_method, afp, ac, mfp, col))
                    if not exists(fname):
                        yield (
                            pd.to_numeric(af[ac], errors='coerce'),
                            mf[col].dropna(), fname, method)


def _process_column(data, cseries, fname, method):
    """calculate significant comparisons and return them as a list/rows

    Parameters
    ===========
    """
    values = {k: df.dropna() for k, df in cseries.groupby(cseries)}
    # Step 1. Pairwise pvals, only keeping those ones that are significant
    qip = []
    pairwise_comparisons = []
    for x, y in combinations(values.keys(), 2):
        pval, stat, xval, yval = method(data, values[x], values[y])
        if np.isnan(pval) or np.isnan(stat):
            continue
        qip.append(pval)
        pairwise_comparisons.append(
            (pval,
             x, len(xval), np.var(xval), np.mean(xval),
             y, len(yval), np.var(yval), np.mean(yval)))

    if qip:
        pooled_pval = len(qip) * np.min(qip)
    else:
        pooled_pval = None
    results = {'cseries': cseries.name,
               'pairwise_comparisons': pairwise_comparisons,
               'pooled_pval': pooled_pval}

    with open(fname, 'wb') as f:
        pickle.dump(results, f)

    return []


if __name__ == '__main__':
    effect_size()
