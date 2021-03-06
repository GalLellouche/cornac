# -*- coding: utf-8 -*-

"""
@author: Quoc-Tuan Truong <tuantq.vnu@gmail.com>
"""

from cornac.data import reader
from cornac.eval_methods import RatioSplit, CrossValidation
from cornac.models import PMF
from cornac.metrics import MAE, RMSE, Recall, FMeasure
from cornac.experiment.experiment import Experiment


def test_with_ratio_split():
    data_file = './tests/data.txt'
    data = reader.read_uir(data_file)
    exp = Experiment(eval_method=RatioSplit(data, verbose=True),
                     models=[PMF(1, 0)],
                     metrics=[MAE(), RMSE(), Recall(1), FMeasure(1)],
                     verbose=True)
    exp.run()

    assert (1, 4) == exp.results.avg.shape

    assert 1 == len(exp.results.per_user)
    assert 4 == len(exp.results.per_user['PMF'])
    assert 2 == len(exp.results.per_user['PMF']['MAE'])
    assert 2 == len(exp.results.per_user['PMF']['RMSE'])
    assert 2 == len(exp.results.per_user['PMF']['Recall@1'])
    assert 2 == len(exp.results.per_user['PMF']['F1@1'])

    try:
        Experiment(None, None, None)
    except ValueError:
        assert True

    try:
        Experiment(None, [PMF(1, 0)], None)
    except ValueError:
        assert True


def test_with_cross_validation():
    data_file = './tests/data.txt'
    data = reader.read_uir(data_file)
    exp = Experiment(eval_method=CrossValidation(data),
                     models=[PMF(1, 0)],
                     metrics=[MAE(), RMSE(), Recall(1), FMeasure(1)],
                     verbose=True)
    exp.run()