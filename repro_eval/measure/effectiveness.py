"""Evaluation measures at the level of effectiveness."""

import numpy as np
from math import sqrt
from copy import deepcopy
from repro_eval.config import exclude


def _rmse(orig_score, rep_core):
    """
    Helping function returning a generator to determine the Root Mean Square Error (RMSE) for all topics.

    @param orig_score: The original scores.
    @param rep_core: The reproduced/replicated scores.
    @return: Generator with RMSE values.
    """
    orig_cp = deepcopy(orig_score)
    rep_cp = deepcopy(rep_core)
    measures_all = list(list(orig_cp.values())[0].keys())
    topics = orig_cp.keys()
    measures_valid = [m for m in measures_all if m not in exclude]

    for measure in measures_valid:
        orig_measure = np.array([orig_cp.get(topic).get(measure) for topic in topics])
        rpl_measure = np.array([rep_cp.get(topic).get(measure) for topic in topics])
        diff = orig_measure - rpl_measure
        yield measure, sqrt(sum(np.square(diff))/len(diff))


def rmse(orig_score, rep_score):
    """
    Determines the Root Mean Square Error (RMSE) between the original and reproduced topic scores
    according to the following paper:
    Timo Breuer, Nicola Ferro, Norbert Fuhr, Maria Maistro, Tetsuya Sakai, Philipp Schaer, Ian Soboroff.
    How to Measure the Reproducibility of System-oriented IR Experiments.
    Proceedings of SIGIR, pages 349-358, 2020.

    @param orig_score: The original scores.
    @param rep_core: The reproduced/replicated scores.
    @return: Dictionary with RMSE values that measure the closeness between the original and reproduced topic scores.
    """
    return dict(_rmse(orig_score, rep_score))
