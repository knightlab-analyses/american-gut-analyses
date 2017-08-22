import unittest

import biom
import numpy as np
import numpy.testing as npt

from eviiom._core import evidence, accumulate_evidence


class CoreTests(unittest.TestCase):
    def test_evidence(self):
        table = biom.Table(np.array([[0, 0.1, 0.2], [0, 0, 0], [0, 0.7, 0]]),
                           ['o1', 'o2', 'o3'],
                           ['s1', 's2', 's3'])

        exp_idx = np.array([0, 2])  # s1, s3
        exp_sum = np.array([0.3, 0.7])
        exp_counts = np.array([2, 1])

        obs_idx, obs_sum, obs_counts = evidence(table)

        npt.assert_equal(obs_idx, exp_idx)
        npt.assert_almost_equal(obs_sum, exp_sum)
        npt.assert_equal(obs_counts, exp_counts)

    def test_counter_evidence(self):
        table = biom.Table(np.array([[0, 0.1, 0.2], [0, 0, 0], [0, 0.7, 0]]),
                           ['o1', 'o2', 'o3'],
                           ['s4', 's5', 's6'])

        prior = np.array([1, 2])
        exp_idx = np.array([2, ])
        exp_sum = np.array([0.7, ])
        exp_counts = np.array([1, ])

        obs_idx, obs_sum, obs_counts = evidence(table, prior=prior)

        npt.assert_equal(obs_idx, exp_idx)
        npt.assert_almost_equal(obs_sum, exp_sum)
        npt.assert_equal(obs_counts, exp_counts)

    def test_accumulate_evidence(self):
        tab_a = biom.Table(np.array([[0, 0.1, 0.2], [0, 0, 0], [0, 0.7, 0]]),
                           ['o1', 'o2', 'o3'],
                           ['s4', 's5', 's6'])

        tab_b = biom.Table(np.array([[0, 1, 1],
                                     [0, 0, 0],
                                     [0, 1, 0],
                                     [1, 0, 0]]),
                           ['o4', 'o5', 'o6', 'o7'],
                           ['s6', 's5', 's4'])

        evidence = np.array([[0.1 - 0.2, 0, 0.1 - 0.2, 0.2 - 0.1],
                             [0, 0, 0, 0],
                             [0.7, 0, 0.7, 0]]).T
        evidence_total = np.array([[0.3, 0, 0.3, 0.3],
                                   [0, 0, 0, 0],
                                   [0.7, 0, 0.7, 0]]).T
        counts = np.array([[1, 0, 1, 1],
                           [0, 0, 0, 0],
                           [1, 0, 1, 0]]).T
        counts_total = np.array([[2, 0, 2, 2],
                                 [0, 0, 0, 0],
                                 [1, 0, 1, 0]]).T

        obs_evidence, obs_evidence_total, obs_counts, obs_counts_total = \
            accumulate_evidence(tab_a, tab_b)

        npt.assert_almost_equal(obs_evidence, evidence)
        npt.assert_almost_equal(obs_evidence_total, evidence_total)
        npt.assert_almost_equal(obs_counts, counts)
        npt.assert_almost_equal(obs_counts_total, counts_total)

    def test_accumulate_evidence_partition(self):
        left = biom.Table(np.array([[0, 1, 2, 3, 0],
                                    [1, 0, 1, 0, 0],
                                    [0, 3, 4, 2, 1]]),
                          ['ol1', 'ol2', 'ol3'],
                          ['s1', 's2', 's3', 's4', 's5'])
        right = biom.Table(np.array([[1, 0, 1, 0, 1],
                                     [0, 1, 0, 1, 0],
                                     [1, 0, 1, 0, 1],
                                     [0, 1, 1, 1, 0]]),
                           ['or1', 'or2', 'or3', 'or4'],
                           ['s1', 's2', 's3', 's4', 's5'])

        evidence = np.array([[2 - 4, 2, 5 - 5],
                             [4 - 2, 0, 5 - 5]])
        evidence_total = np.array([[6, 2, 10],
                                   [6, 0, 10]])
        counts = np.array([[1, 2, 2],
                           [2, 0, 2]])
        counts_total = np.array([[3, 2, 4],
                                 [3, 0, 4]])

        obs_evidence, obs_evidence_total, obs_counts, obs_counts_total = \
            accumulate_evidence(left, right, ['or1', 'or2'])

        npt.assert_almost_equal(obs_evidence, evidence)
        npt.assert_almost_equal(obs_evidence_total, evidence_total)
        npt.assert_almost_equal(obs_counts, counts)
        npt.assert_almost_equal(obs_counts_total, counts_total)

    def test_accumulate_evidence_id_mismatch(self):
        tab_a = biom.Table(np.array([[0, 0.1, 0.2], [0, 0, 0], [0, 0.7, 0]]),
                           ['o1', 'o2', 'o3'],
                           ['s4', 's5', 's6'])
        tab_b = biom.Table(np.array([[0, 0.1, 0.2], [0, 0, 0], [0, 0.7, 0]]),
                           ['o1', 'o2', 'o3'],
                           ['s4', 's5', 's10'])
        with self.assertRaises(ValueError):
            accumulate_evidence(tab_a, tab_b)

    def test_accumulate_evidence_id_subset_mismatch(self):
        tab_a = biom.Table(np.array([[0, 0.1, 0.2], [0, 0, 0], [0, 0.7, 0]]),
                           ['o1', 'o2', 'o3'],
                           ['s4', 's5', 's6'])
        tab_b = biom.Table(np.array([[0, 0.1, 0.2], [0, 0, 0], [0, 0.7, 0]]),
                           ['o1', 'o2', 'o3'],
                           ['s4', 's5', 's6'])
        with self.assertRaisesRegex(ValueError, 'subset'):
            accumulate_evidence(tab_a, tab_b, ['o1', 'o2', 'o20'])


if __name__ == '__main__':
    unittest.main()
