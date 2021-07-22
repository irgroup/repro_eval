import pytest
from repro_eval.Evaluator import RpdEvaluator

rpd_eval = RpdEvaluator(qrel_orig_path='./example/data/qrels/core17.txt',
                        run_b_orig_path='./example/orig_b.txt',
                        run_a_orig_path='./example/orig_a.txt',
                        run_b_rep_path='./example/rpd_b.txt',
                        run_a_rep_path='./example/rpd_a.txt')

rpd_eval.trim()
rpd_eval.evaluate()


def test_rbo():
    # compare rbo implementations by the 10th decimal

    rbo = rpd_eval.rbo()
    rbo_slow = rpd_eval.rbo(misinfo=False)

    for k, v in rbo.get('baseline').items():
        rbo['baseline'][k] = round(v, 10)
    for k, v in rbo.get('advanced').items():
        rbo['advanced'][k] = round(v, 10)
    for k, v in rbo_slow.get('baseline').items():
        rbo_slow['baseline'][k] = round(v, 10)
    for k, v in rbo_slow.get('advanced').items():
        rbo_slow['advanced'][k] = round(v, 10)

    assert rbo.get('baseline') == rbo_slow.get('baseline')
    assert rbo.get('advanced') == rbo_slow.get('advanced')


