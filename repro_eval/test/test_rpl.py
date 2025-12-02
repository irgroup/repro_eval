import pytest
from repro_eval.Evaluator import RplEvaluator

rpl_eval = RplEvaluator(qrels_orig_path='./example/qrels/core17.txt',
                        run_b_orig_path='./example/orig_b.txt',
                        run_a_orig_path='./example/orig_a.txt',
                        run_b_rep_path='./example/rpl_b.txt',
                        run_a_rep_path='./example/rpl_a.txt',
                        qrels_rpl_path='./example/qrels/core18.txt')

rpl_eval.trim()
rpl_eval.evaluate()


def test_er():
    er = rpl_eval.er()
    assert 'AP' in er.keys()
    assert 'nDCG' in er.keys()
    assert 'P@10' in er.keys()


def test_dri():
    dri = rpl_eval.dri()
    assert 'AP' in dri.keys()
    assert 'nDCG' in dri.keys()
    assert 'P@10' in dri.keys()


def test_ttest():
    ttest = rpl_eval.ttest()
    assert 'baseline' in ttest.keys()
    assert 'advanced' in ttest.keys()