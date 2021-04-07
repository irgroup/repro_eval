import pytest
from repro_eval.Evaluator import RpdEvaluator
from repro_eval.config import ERR_MSG

rpd_eval = RpdEvaluator(qrel_orig_path=None,
                        run_b_orig_path=None,
                        run_a_orig_path=None,
                        run_b_rep_path=None,
                        run_a_rep_path=None)


def test_ktu(capfd):
    assert None is rpd_eval.ktau_union()
    out, err = capfd.readouterr()
    assert out == ''.join([ERR_MSG, '\n'])


def test_rbo(capfd):
    assert None is rpd_eval.rbo()
    out, err = capfd.readouterr()
    assert out == ''.join([ERR_MSG, '\n'])


def test_rmse(capfd):
    assert None is rpd_eval.rmse()
    out, err = capfd.readouterr()
    assert out == ''.join([ERR_MSG, '\n'])


def test_er(capfd):
    assert None is rpd_eval.er()
    out, err = capfd.readouterr()
    assert out == ''.join([ERR_MSG, '\n'])


def test_dri(capfd):
    assert None is rpd_eval.dri()
    out, err = capfd.readouterr()
    assert out == ''.join([ERR_MSG, '\n'])


def test_ttest(capfd):
    assert None is rpd_eval.ttest()
    out, err = capfd.readouterr()
    assert out == ''.join([ERR_MSG, '\n'])
