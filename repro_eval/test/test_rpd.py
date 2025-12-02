import pytest
from repro_eval.Evaluator import RpdEvaluator

rpd_eval = RpdEvaluator(qrels_orig_path='./example/qrels/core17.txt',
                        run_b_orig_path='./example/orig_b.txt',
                        run_a_orig_path='./example/orig_a.txt',
                        run_b_rep_path='./example/rpd_b.txt',
                        run_a_rep_path='./example/rpd_a.txt')

rpd_eval.trim()
rpd_eval.evaluate()


def test_ktu():
    ktu = rpd_eval.ktu()
    assert 'baseline' in ktu.keys()
    assert 'advanced' in ktu.keys()


def test_rbo():
    rbo = rpd_eval.rbo()
    assert 'baseline' in rbo.keys()
    assert 'advanced' in rbo.keys()


def test_rmse():
    rmse = rpd_eval.rmse()
    assert 'baseline' in rmse.keys()
    assert 'advanced' in rmse.keys()


def test_nrmse():
    nrmse = rpd_eval.nrmse()
    assert 'baseline' in nrmse.keys()
    assert 'advanced' in nrmse.keys()


def test_er():
    er = rpd_eval.er()
    assert 'AP' in er.keys()
    assert 'nDCG' in er.keys()
    assert 'P@10' in er.keys()


def test_dri():
    dri = rpd_eval.dri()
    assert 'AP' in dri.keys()
    assert 'nDCG' in dri.keys()
    assert 'P@10' in dri.keys()


def test_ttest():
    ttest = rpd_eval.ttest()
    assert 'baseline' in ttest.keys()
    assert 'advanced' in ttest.keys()