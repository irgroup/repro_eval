import numpy as np
from copy import deepcopy
from repro_eval.config import exclude


def diff(topic_score_a, topic_score_b):
    for measure, value in topic_score_a.items():
        if measure not in exclude:
            yield measure, value - topic_score_b.get(measure)


def topic_diff(run_a, run_b):
    run_a_cp = deepcopy(run_a)
    run_b_cp = deepcopy(run_b)

    for topic, measures in run_a_cp.items():
        yield topic, dict(diff(measures, run_b_cp.get(topic)))


def _mean_improvement(run_a, run_b):
    measures_all = list(list(run_a.values())[0].keys())
    measures_valid = [m for m in measures_all if m not in exclude]
    topics = run_a.keys()
    delta = dict(topic_diff(run_a, run_b))

    for measure in measures_valid:
        yield measure, np.array([delta.get(topic).get(measure) for topic in topics]).mean()


def mean_improvement(run_a, run_b):
    return dict(_mean_improvement(run_a, run_b))


def _er(orig_score_a, orig_score_b, rep_score_a, rep_score_b):
    mi_orig = mean_improvement(orig_score_a, orig_score_b)
    mi_rep = mean_improvement(rep_score_a, rep_score_b)

    for measure, value in mi_rep.items():
        yield measure, value / mi_orig.get(measure)


def ER(orig_score_a, orig_score_b, rep_score_a, rep_score_b):
    return dict(_er(orig_score_a, orig_score_b, rep_score_a, rep_score_b))


def _mean_score(scores):
    measures_all = list(list(scores.values())[0].keys())
    measures_valid = [m for m in measures_all if m not in exclude]
    topics = scores.keys()

    for measure in measures_valid:
        yield measure, np.array([scores.get(topic).get(measure) for topic in topics]).mean()


def mean_score(scores):
    return dict(_mean_score(scores))


def _rel_improve(scores_a, scores_b):
    mean_scores_a = mean_score(scores_a)
    mean_scores_b = mean_score(scores_b)

    for measure, mean in mean_scores_a.items():
        yield measure, (mean - mean_scores_b.get(measure)) / mean_scores_b.get(measure)


def rel_improve(scores_a, scores_b):
    return dict(_rel_improve(scores_a, scores_b))


def _deltaRI(orig_score_a, orig_score_b, rep_score_a, rep_score_b):
    rel_improve_orig = rel_improve(orig_score_a, orig_score_b)
    rel_improve_rep = rel_improve(rep_score_a, rep_score_b)

    for measure, ri in rel_improve_orig.items():
        yield measure, ri - rel_improve_rep.get(measure)


def deltaRI(orig_score_a, orig_score_b, rep_score_a, rep_score_b):
    return dict(_deltaRI(orig_score_a, orig_score_b, rep_score_a, rep_score_b))