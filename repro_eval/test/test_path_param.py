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
