import pytest
from repro_eval.Evaluator import RplEvaluator
from repro_eval.config import ERR_MSG

rpd_eval = RplEvaluator(qrel_orig_path=None,
                        run_b_orig_path=None,
                        run_a_orig_path=None,
                        run_b_rep_path=None,
                        run_a_rep_path=None,
                        qrel_rpl_path=None)


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
