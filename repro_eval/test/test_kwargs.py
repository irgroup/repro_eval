import pytest
import pytrec_eval
from repro_eval.Evaluator import RpdEvaluator


rpd_eval = RpdEvaluator(qrel_orig_path='./example/data/qrels/core17.txt',
                        run_b_orig_path='./example/orig_b.txt',
                        run_a_orig_path='./example/orig_a.txt',
                        run_b_rep_path='./example/rpd_b.txt',
                        run_a_rep_path='./example/rpd_a.txt')

rpd_eval.trim()
rpd_eval.evaluate()

ktu = rpd_eval.ktau_union()
ktu_base = ktu.get('baseline')
ktu_adv = ktu.get('advanced')

rbo = rpd_eval.rbo()
rbo_base = rbo.get('baseline')
rbo_adv = rbo.get('advanced')


def test_path_ktu():
    _ktu = rpd_eval.ktau_union(run_b_path='./example/rpd_b.txt', run_a_path='./example/rpd_a.txt')
    assert 'baseline' in _ktu.keys()
    assert ktu_base == _ktu.get('baseline')
    assert 'advanced' in _ktu.keys()
    assert ktu_adv == _ktu.get('advanced')


def test_path_rbo():
    _rbo = rpd_eval.rbo(run_b_path='./example/rpd_b.txt', run_a_path='./example/rpd_a.txt')
    assert 'baseline' in _rbo.keys()
    assert rbo_base == _rbo.get('baseline')
    assert 'advanced' in _rbo.keys()
    assert rbo_adv == _rbo.get('advanced')


def test_run_ktu():
    with open('./example/rpd_b.txt') as _base_file, open('./example/rpd_a.txt') as _adv_file:
        _base_run = pytrec_eval.parse_run(_base_file)
        _adv_run = pytrec_eval.parse_run(_adv_file)
    _ktu = rpd_eval.ktau_union(run_b_rep=_base_run, run_a_rep=_adv_run)
    assert 'baseline' in _ktu.keys()
    assert ktu_base == _ktu.get('baseline')
    assert 'advanced' in _ktu.keys()
    assert ktu_adv == _ktu.get('advanced')


def test_run_rbo():
    with open('./example/rpd_b.txt') as _base_file, open('./example/rpd_a.txt') as _adv_file:
        _base_run = pytrec_eval.parse_run(_base_file)
        _adv_run = pytrec_eval.parse_run(_adv_file)
    _rbo = rpd_eval.rbo(run_b_rep=_base_run, run_a_rep=_adv_run)
    assert 'baseline' in _rbo.keys()
    assert rbo_base == _rbo.get('baseline')
    assert 'advanced' in _rbo.keys()
    assert rbo_adv == _rbo.get('advanced')
