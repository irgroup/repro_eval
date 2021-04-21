import pytest
from repro_eval.Evaluator import RpdEvaluator

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

    base_rpd_eval = RpdEvaluator(qrel_orig_path='./example/data/qrels/core17.txt',
                                 run_b_orig_path='./example/orig_b.txt')
    base_rpd_eval.trim()
    base_rpd_eval.evaluate()

    base_ktu = base_rpd_eval.ktau_union(run_b_path='./example/rpd_b.txt')
    assert 'baseline' in base_ktu.keys()
    assert ktu.get('baseline') == base_ktu.get('baseline')



