import pytest
from repro_eval.Evaluator import RpdEvaluator

rpd_eval = RpdEvaluator(qrels_orig_path='./example/qrels/core17.txt',
                        run_b_orig_path='./example/orig_b.txt',
                        run_a_orig_path='./example/orig_a.txt',
                        run_b_rep_path='./example/rpd_b.txt',
                        run_a_rep_path='./example/rpd_a.txt')

rpd_eval.trim()
rpd_eval.evaluate()


def test_rbo():

    rbo = rpd_eval.rbo()

    assert isinstance(rbo.get('baseline'), float)
    assert isinstance(rbo.get('advanced'), float)


