import numpy as np


def evidence(table, prior=None):
    """Calculate evidence details from a table

    Parameters
    ----------
    table : biom
        A biom table that has been partitioned to only include the samples in
        support of an association (positive) or contradict an association
        (negative).
    prior : iterable of str, optional
        Sample IDs in which a positive association was previously observed

    Returns
    -------
    np.array of int
        The index positions of the observations of association evidence
    np.array of float
        The strength of the evidence
    np.array of int
        The number of evidence data points per observation
    """
    strength = table.sum('observation')

    if prior is None:
        associations = (strength > 0).nonzero()[0]
    else:
        # only keep the observations in which a prior association was found
        prior_ = np.zeros_like(strength, dtype=bool)
        prior_[prior] = True
        associations = np.logical_and(strength > 0, prior_).nonzero()[0]

    association_strength = strength[associations]
    association_counts = table.pa(inplace=False).sum('observation')[associations]

    return associations, association_strength, association_counts


def accumulate_evidence(left, right, right_obs_ids=None):
    """Accumulate evidence between tables

    Parameters
    ----------
    left : biom.Table
        A BIOM table containing observations to assess evidence for
    right : biom.Table
        A BIOM table containing observations to assess evidence for
    right_obs_ids : iterable of str, optional
        The feature IDs in the right table to operate on, all if None.

    Raises
    ------
    ValueError
        If the sample IDs in both tables are not identical
    ValueError
        If the right IDs specified are not a subset of the right table.

    Returns
    -------
    np.array
        A matrix of the positive minus the negative evidence. The observation
        IDs in the right table compose the rows, and the observation IDs in the
        left table compose the columns.
    np.array
        A matrix of the total evidence. The observation IDs in the right
        table compose the rows, and the observation IDs in the left table
        compose the columns.
    np.array
        A matrix of the number of times a positive interaction was observed.
        The observation IDs in the right table compose the rows, and the
        observation IDs in the left table compose the columns.
    np.array
        A matrix of the total number of possible interactions which could have
        been observed. The observation IDs in the right table compose the rows,
        and the observation IDs in the left table compose the columns.
    """
    if set(left.ids()) != set(right.ids()):
        raise ValueError("Sample IDs between tables are not identical")

    if right_obs_ids is None:
        right_obs_ids = right.ids(axis='observation')
    else:
        if not set(right_obs_ids).issubset(right.ids(axis='observation')):
            raise ValueError("Right IDs are not a subset of right")

    former_obs_order = left.ids(axis='observation')
    left = left.sort_order(right.ids())
    if (former_obs_order != left.ids(axis='observation')).any():
        raise ValueError("This should never happen and would be bad.")

    accum_evidence = np.zeros((len(right_obs_ids),
                               left.ids(axis='observation').size))
    accum_total_evidence = np.zeros_like(accum_evidence)
    accum_counts = np.zeros_like(accum_evidence)
    accum_total_counts = np.zeros_like(accum_evidence)

    right_ids = right.ids()
    left_obs = left.ids(axis='observation')
    for row, i in enumerate(right_obs_ids):
        right_v = right.data(i, dense=False, axis='observation')
        right_nz = right_v.indices

        if not right_nz.size:
            continue

        current_ids = set(right_ids[right_nz])
        pos = left.filter(lambda v, i, md: i in current_ids,
                          inplace=False)
        neg = left.filter(lambda v, i, md: i not in current_ids,
                          inplace=False)

        pos_assoc, pos_assoc_strength, pos_assoc_counts = evidence(pos)
        neg_assoc, neg_assoc_strength, neg_assoc_counts = evidence(neg, pos_assoc)

        accum_evidence[row, pos_assoc] += pos_assoc_strength
        accum_evidence[row, neg_assoc] -= neg_assoc_strength

        accum_counts[row, pos_assoc] += pos_assoc_counts

        accum_total_evidence[row, pos_assoc] += pos_assoc_strength
        accum_total_evidence[row, neg_assoc] += neg_assoc_strength

        accum_total_counts[row, pos_assoc] += pos_assoc_counts
        accum_total_counts[row, neg_assoc] += neg_assoc_counts

    return (accum_evidence,
            accum_total_evidence,
            accum_counts,
            accum_total_counts)
