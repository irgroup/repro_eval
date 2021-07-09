"""Evaluation measures at the level of effectiveness."""

import numpy as np
from math import sqrt
from copy import deepcopy
from tqdm import tqdm
from repro_eval.config import exclude


def _rmse(orig_score, rep_core, pbar=False):
    """
    Helping function returning a generator to determine the Root Mean Square Error (RMSE) for all topics.

    @param orig_score: The original scores.
    @param rep_core: The reproduced/replicated scores.
    @param pbar: Boolean value indicating if progress bar should be printed.
    @return: Generator with RMSE values.
    """
    orig_cp = deepcopy(orig_score)
    rep_cp = deepcopy(rep_core)
    measures_all = list(list(orig_cp.values())[0].keys())
    topics = orig_cp.keys()
    measures_valid = [m for m in measures_all if m not in exclude]

    measures = tqdm(measures_valid) if pbar else measures_valid

    for measure in measures:
        orig_measure = np.array([orig_cp.get(topic).get(measure) for topic in topics])
        rpl_measure = np.array([rep_cp.get(topic).get(measure) for topic in topics])
        diff = orig_measure - rpl_measure
        yield measure, sqrt(sum(np.square(diff))/len(diff))


def rmse(orig_score, rep_score, pbar=False):
    """
    Determines the Root Mean Square Error (RMSE) between the original and reproduced topic scores
    according to the following paper:
    Timo Breuer, Nicola Ferro, Norbert Fuhr, Maria Maistro, Tetsuya Sakai, Philipp Schaer, Ian Soboroff.
    How to Measure the Reproducibility of System-oriented IR Experiments.
    Proceedings of SIGIR, pages 349-358, 2020.

    @param orig_score: The original scores.
    @param rep_core: The reproduced/replicated scores.
    @param pbar: Boolean value indicating if progress bar should be printed.
    @return: Dictionary with RMSE values that measure the closeness between the original and reproduced topic scores.
    """
    return dict(_rmse(orig_score, rep_score, pbar=pbar))


def _maxrmse(orig_score, pbar=False):
    """
    Helping function returning a generator to determine the maximum Root Mean Square Error (RMSE) for all topics.

    @param orig_score: The original scores.
    @param pbar: Boolean value indicating if progress bar should be printed.
    @return: Generator with RMSE values.
    """
    orig_cp = deepcopy(orig_score)
    measures_all = list(list(orig_cp.values())[0].keys())
    topics = orig_cp.keys()
    measures_valid = [m for m in measures_all if m not in exclude]
    measures = tqdm(measures_valid) if pbar else measures_valid

    for measure in measures:
        orig_measure = np.array([orig_cp.get(topic).get(measure) for topic in topics])
        _max = np.vectorize(lambda x: max(x, 1 - x))
        maxdiff = _max(orig_measure)
        yield measure, sqrt(sum(np.square(maxdiff))/len(maxdiff))


def nrmse(orig_score, rep_score, pbar=False):
    """
    Determines the normalized Root Mean Square Error (RMSE) between the original and reproduced topic scores.

    @param orig_score: The original scores.
    @param rep_core: The reproduced/replicated scores.
    @param pbar: Boolean value indicating if progress bar should be printed.
    @return: Dictionary with RMSE values that measure the closeness between the original and reproduced topic scores.
    """
    rmse = dict(_rmse(orig_score, rep_score, pbar=pbar))
    maxrmse = dict(_maxrmse(orig_score, pbar=pbar))
    return {measure: score / maxrmse.get(measure) for measure, score in rmse.items()}
