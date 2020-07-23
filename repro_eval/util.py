import numpy as np
from repro_eval.config import TRIM_THRESH, exclude


def trim(run, thresh=TRIM_THRESH):
    for topic, docs in run.items():
        run[topic] = dict(list(run[topic].items())[:thresh])


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


def print_base_adv(measure_topic, repro_measure, base_value, adv_value=None):
    if adv_value:
        fill = ('{:3s}' if base_value < 0 else '{:4s}')
        print(('{:25s}{:8s}{:8s}{:.4f}' + fill + '{:8s}{:.4f}').format(measure_topic, repro_measure,
                                                                       'BASE', base_value, ' ', 'ADV', adv_value))
    else:
        print('{:25s}{:8s}{:8s}{:.4f}'.format(measure_topic, repro_measure, 'BASE', base_value))


def print_simple_line(measure, repro_measure, value):
    print('{:25s}{:8s}{:.4f}'.format(measure, repro_measure, value))

