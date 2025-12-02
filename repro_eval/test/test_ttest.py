import pytest
from repro_eval.Evaluator import RpdEvaluator


def test_ttest_with_identical_score_distributions():
    rpd_eval = RpdEvaluator(qrels_orig_path='./example/qrels/core17.txt',
                            run_b_orig_path='./example/orig_b.txt',
                            run_a_orig_path='./example/orig_a.txt',
                            run_b_rep_path='./example/orig_b.txt',
                            run_a_rep_path='./example/orig_a.txt')

    rpd_eval.trim()
    rpd_eval.evaluate()

    ttest = rpd_eval.ttest()

    pvals = list(filter(lambda x: x == 1.0, ttest.get('baseline').values()))
    assert len(pvals) == len(ttest.get('baseline').keys())

    pvals = list(filter(lambda x: x == 1.0, ttest.get('advanced').values()))
    assert len(pvals) == len(ttest.get('advanced').keys())
