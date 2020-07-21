import numpy as np
from repro_eval.config import exclude


def arp(topic_scores):
    return np.array(list(topic_scores.values())).mean()


def _arp_scores(run):
    measures_all = list(list(run.values())[0].keys())
    measures_valid = [m for m in measures_all if m not in exclude]
    topics = run.keys()

    for measure in measures_valid:
        yield measure, np.array(list([run.get(topic).get(measure) for topic in topics])).mean()


def arp_scores(run):
    return dict(_arp_scores(run))


def _topic_scores(run_scores):
    measures_all = list(list(run_scores.values())[0].keys())
    measures_valid = [m for m in measures_all if m not in exclude]
    topics = run_scores.keys()

    for measure in measures_valid:
        yield measure, [run_scores.get(topic).get(measure) for topic in topics]


def topic_scores(run_scores):
    return dict(_topic_scores(run_scores))
