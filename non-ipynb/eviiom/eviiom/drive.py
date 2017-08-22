import click
import biom
import numpy as np
import joblib
import h5py
from functools import partial
from eviiom._core import accumulate_evidence


def _computable(left, right, right_obs):
    left = biom.load_table(left)
    right = biom.load_table(right)

    # this vastly improves the performance of Table.filter
    left.del_metadata()
    right.del_metadata()

    return (right_obs, accumulate_evidence(left, right, right_obs))


@click.group()
def cli():
    pass


@cli.command()
@click.option('--left-table', type=click.Path(exists=True), required=True,
              help="A BIOM table")
@click.option('--right-table', type=click.Path(exists=True), required=True,
              help="A BIOM table")
@click.option('--threads', type=int, default=1)
@click.option('--min-overlap', type=int, default=3,
              help='The minimum number of supporting samples overlapping')
@click.option('--output', type=click.Path(exists=False), required=True)
@click.option('--left-as-observations', is_flag=True, default=False,
              required=False,
              help='Set the observation IDs in the left table as the '
                   'observation IDs in the resulting table')
def blend(left_table, right_table, threads, min_overlap,
          output, left_as_observations):
    left_tmp = biom.load_table(left_table)
    left_sam = left_tmp.ids()

    right_tmp = biom.load_table(right_table)
    right_sam = right_tmp.ids()
    right_obs = right_tmp.ids(axis='observation')

    f = partial(_computable, left_table, right_table)

    chunk = int(np.floor(len(right_obs) / threads))
    with joblib.parallel.Parallel(n_jobs=threads, verbose=10) as par:
        results = par(joblib.delayed(f)(right_obs[i:i+chunk])
                      for i in range(0, len(right_obs), chunk))

    # merge results
    # clip to avoid negative evidence, and to avoid divide by zeros
    evidence = np.vstack([r[0] for _, r in results]).clip(0)
    evidence_total = np.vstack([r[1] for _, r in results]).clip(1)
    counts = np.vstack([r[2] for _, r in results])
    counts_total = np.vstack([r[3] for _, r in results]).clip(1)

    # convert counts data to fraction in support
    min_counts = np.where(counts >= min_overlap, counts, 0)
    fraction_counts = min_counts / counts_total.clip(1)

    # normalize the evidence by the total amount of positive/negative evidence
    normalized_evidence = evidence / evidence_total.clip(1)

    # scale the evidence by the number of supporting interactions
    normalized_evidence *= fraction_counts

    # whether the left input table is on the observation axis, or the right
    if left_as_observations:
        o = left_tmp
        s = right_tmp
        d = normalized_evidence.T
    else:
        s = left_tmp
        o = right_tmp
        d = normalized_evidence

    final = biom.Table(d,
                       o.ids(axis='observation'),
                       s.ids(axis='observation'),
                       o.metadata(axis='observation'),
                       s.metadata(axis='observation'))

    final.remove_empty()

    with h5py.File(output, 'w') as fp:
        final.to_hdf5(fp, 'asd')


if __name__ == '__main__':
    cli()
