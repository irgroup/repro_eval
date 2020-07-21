import numpy as np
from math import sqrt
from copy import deepcopy
from repro_eval.config import exclude


def _rmse(orig_score, rep_core):
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
    return dict(_rmse(orig_score, rep_score))