import pytest
from repro_eval.Evaluator import RpdEvaluator, RplEvaluator
import numpy as np

rpd_eval = RpdEvaluator(qrel_orig_path='./example/data/qrels/core17.txt',
                        run_b_orig_path='./example/orig_b.txt',
                        run_a_orig_path='./example/orig_a.txt',
                        run_b_rep_path='./example/rpd_b.txt',
                        run_a_rep_path='./example/rpd_a.txt')

rpd_eval.trim()
rpd_eval.evaluate()


def test_ktu_path_param():
    ktu = rpd_eval.ktau_union()
    assert 'baseline' in ktu.keys()
    assert 'advanced' in ktu.keys()

    _rpd_eval = RpdEvaluator(qrel_orig_path='./example/data/qrels/core17.txt',
                            run_b_orig_path='./example/orig_b.txt',
                            run_a_orig_path='./example/orig_a.txt')
    _rpd_eval.trim()
    _rpd_eval.evaluate()

    _ktu = _rpd_eval.ktau_union(run_b_path='./example/rpd_b.txt')
    assert 'baseline' in _ktu.keys()
    assert ktu.get('baseline') == _ktu.get('baseline')

    _ktu = _rpd_eval.ktau_union(run_b_path='./example/rpd_b.txt', run_a_path='./example/rpd_a.txt')
    assert 'advanced' in _ktu.keys()
    assert ktu.get('advanced') == _ktu.get('advanced')


def test_rbo_path_param():
    rbo = rpd_eval.rbo()
    assert 'baseline' in rbo.keys()
    assert 'advanced' in rbo.keys()

    _rpd_eval = RpdEvaluator(qrel_orig_path='./example/data/qrels/core17.txt',
                             run_b_orig_path='./example/orig_b.txt',
                             run_a_orig_path='./example/orig_a.txt')
    _rpd_eval.trim()
    _rpd_eval.evaluate()

    _rbo = _rpd_eval.rbo(run_b_path='./example/rpd_b.txt')
    assert 'baseline' in _rbo.keys()
    assert rbo.get('baseline') == _rbo.get('baseline')

    _rbo = _rpd_eval.rbo(run_b_path='./example/rpd_b.txt', run_a_path='./example/rpd_a.txt')
    assert 'advanced' in _rbo.keys()
    assert rbo.get('advanced') == _rbo.get('advanced')


def test_rmse_path_param():
    rmse = rpd_eval.rmse()
    assert 'baseline' in rmse.keys()
    assert 'advanced' in rmse.keys()

    _rpd_eval = RpdEvaluator(qrel_orig_path='./example/data/qrels/core17.txt',
                             run_b_orig_path='./example/orig_b.txt',
                             run_a_orig_path='./example/orig_a.txt')
    _rpd_eval.trim()
    _rpd_eval.evaluate()

    _rmse = _rpd_eval.rmse(run_b_path='./example/rpd_b.txt')
    assert 'baseline' in _rmse.keys()
    assert rmse.get('baseline') == _rmse.get('baseline')

    _rmse = _rpd_eval.rmse(run_b_path='./example/rpd_b.txt', run_a_path='./example/rpd_a.txt')
    assert 'advanced' in _rmse.keys()
    assert rmse.get('advanced') == _rmse.get('advanced')


def test_rpd_ttest_path_param():
    pval = rpd_eval.ttest()
    assert 'baseline' in pval.keys()
    assert 'advanced' in pval.keys()

    _rpd_eval = RpdEvaluator(qrel_orig_path='./example/data/qrels/core17.txt',
                             run_b_orig_path='./example/orig_b.txt',
                             run_a_orig_path='./example/orig_a.txt')
    _rpd_eval.trim()
    _rpd_eval.evaluate()

    _pval = _rpd_eval.ttest(run_b_path='./example/rpd_b.txt')
    assert 'baseline' in _pval.keys()
    # pick a few samples here since nan comparisons cause problems in combination with assert
    assert pval.get('baseline').get('ndcg') == _pval.get('baseline').get('ndcg')
    assert pval.get('baseline').get('P_10') == _pval.get('baseline').get('P_10')
    assert pval.get('baseline').get('map') == _pval.get('baseline').get('map')

    _pval = _rpd_eval.ttest(run_b_path='./example/rpd_b.txt', run_a_path='./example/rpd_a.txt')
    assert 'advanced' in _pval.keys()
    # pick a few samples here since nan comparisons cause problems in combination with assert
    assert pval.get('advanced').get('ndcg') == _pval.get('advanced').get('ndcg')
    assert pval.get('advanced').get('P_10') == _pval.get('advanced').get('P_10')
    assert pval.get('advanced').get('map') == _pval.get('advanced').get('map')


def test_rpl_ttest_path_param():
    rpl_eval = RplEvaluator(qrel_orig_path='./example/data/qrels/core17.txt',
                            run_b_orig_path='./example/orig_b.txt',
                            run_a_orig_path='./example/orig_a.txt',
                            run_b_rep_path='./example/rpl_b.txt',
                            run_a_rep_path='./example/rpl_a.txt',
                            qrel_rpl_path='./example/data/qrels/core18.txt')

    rpl_eval.trim()
    rpl_eval.evaluate()

    pval = rpl_eval.ttest()
    assert 'baseline' in pval.keys()
    assert 'advanced' in pval.keys()

    _rpl_eval = RplEvaluator(qrel_orig_path='./example/data/qrels/core17.txt',
                             run_b_orig_path='./example/orig_b.txt',
                             run_a_orig_path='./example/orig_a.txt',
                             qrel_rpl_path='./example/data/qrels/core18.txt')
    _rpl_eval.trim()
    _rpl_eval.evaluate()

    _pval = _rpl_eval.ttest(run_b_path='./example/rpl_b.txt')
    assert 'baseline' in _pval.keys()
    # pick a few samples here since nan comparisons cause problems in combination with assert
    assert pval.get('baseline').get('ndcg') == _pval.get('baseline').get('ndcg')
    assert pval.get('baseline').get('P_10') == _pval.get('baseline').get('P_10')
    assert pval.get('baseline').get('map') == _pval.get('baseline').get('map')

    _pval = _rpl_eval.ttest(run_b_path='./example/rpl_b.txt', run_a_path='./example/rpl_a.txt')
    assert 'advanced' in _pval.keys()
    # pick a few samples here since nan comparisons cause problems in combination with assert
    assert pval.get('advanced').get('ndcg') == _pval.get('advanced').get('ndcg')
    assert pval.get('advanced').get('P_10') == _pval.get('advanced').get('P_10')
    assert pval.get('advanced').get('map') == _pval.get('advanced').get('map')
