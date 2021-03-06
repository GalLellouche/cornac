# -*- coding: utf-8 -*-

"""
@author: Aghiles Salah <asalah@smu.edu.sg>
"""

from cornac.eval_methods import CrossValidation
from cornac.data import reader
import numpy as np


def test_partition_data():
    data = reader.read_uir('./tests/data.txt')

    nfolds = 5
    cv = CrossValidation(data=data, n_folds=nfolds)

    ref_set = set(range(nfolds))
    res_set = set(cv.partition)
    fold_sizes = np.unique(cv.partition, return_counts=True)[1]

    assert len(data) == len(cv.partition)
    assert res_set == ref_set
    assert np.all(fold_sizes == 2)


def test_validate_partition():
    data = reader.read_uir('./tests/data.txt')

    nfolds = 5
    cv = CrossValidation(data=data, n_folds=nfolds)

    try:
        cv._validate_partition([0, 0, 1, 1])
    except:
        assert True

    try:
        cv._validate_partition([0, 0, 1, 1, 2, 2, 2, 2, 3, 3])
    except:
        assert True


def test_get_train_test_sets_next_fold():
    data = reader.read_uir('./tests/data.txt')

    nfolds = 5
    cv = CrossValidation(data=data, n_folds=nfolds)
    
    for n in range(cv.n_folds):
        cv._get_train_test()
        assert cv.current_fold == n
        assert cv.train_set.matrix.shape == (8, 8)
        cv._next_fold()
        