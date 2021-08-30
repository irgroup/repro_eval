import itertools
from collections import OrderedDict
import numpy as np
from repro_eval.config import TRIM_THRESH, exclude


def trim(run, thresh=TRIM_THRESH):
    """
    Use this function to trim a run to a length of a document length specified by thresh.

    @param run: The run to be trimmed.
    @param thresh: The threshold value of the run length.
    """
    for topic, docs in run.items():
        run[topic] = dict(list(run[topic].items())[:thresh])


def arp(topic_scores):
    """
    This function computes the Average Retrieval Performance (ARP) according to the following paper:
    Timo Breuer, Nicola Ferro, Norbert Fuhr, Maria Maistro, Tetsuya Sakai, Philipp Schaer, Ian Soboroff.
    How to Measure the Reproducibility of System-oriented IR Experiments.
    Proceedings of SIGIR, pages 349-358, 2020.

    The ARP score is defined by the mean across the different topic scores of a run.

    @param topic_scores: Topic scores of an evaluated run.
    @return: The ARP score.
    """
    return np.array(list(topic_scores.values())).mean()


def _arp_scores(run):
    """
    Helping function returning a generator for determining the Average Retrieval Performance (ARP) scores.

    @param run: The run to be evaluated.
    @return: Generator with ARP scores for each trec_eval evaluation measure.
    """
    measures_all = list(list(run.values())[0].keys())
    measures_valid = [m for m in measures_all if m not in exclude]
    topics = run.keys()

    for measure in measures_valid:
        yield measure, np.array(list([run.get(topic).get(measure) for topic in topics])).mean()


def arp_scores(run):
    """
    This function computes the Average Retrieval Performance (ARP) scores according to the following paper:
    Timo Breuer, Nicola Ferro, Norbert Fuhr, Maria Maistro, Tetsuya Sakai, Philipp Schaer, Ian Soboroff.
    How to Measure the Reproducibility of System-oriented IR Experiments.
    Proceedings of SIGIR, pages 349-358, 2020.

    The ARP score is defined by the mean across the different topic scores of a run.
    For all measures outputted by trec_eval, the ARP scores will be determined.

    @param run: The run to be evaluated.
    @return: Dictionary containing the ARP scores for every measure outputted by trec_eval.
    """
    return dict(_arp_scores(run))


def _topic_scores(run_scores):
    """
    Helping function returning a generator for determining the topic scores for each measure.

    @param run_scores: The run scores of the previously evaluated run.
    @return: Generator with topic scores for each trec_eval evaluation measure.
    """
    measures_all = list(list(run_scores.values())[0].keys())
    measures_valid = [m for m in measures_all if m not in exclude]
    topics = run_scores.keys()

    for measure in measures_valid:
        yield measure, [run_scores.get(topic).get(measure) for topic in topics]


def topic_scores(run_scores):
    """
    Use this function for a dictionary that contains the topic scores for each measure outputted by trec_eval.

    @param run_scores: The run scores of the previously evaluated run.
    @return: Dictionary containing the topic scores for every measure outputted by trec_eval.
    """
    return dict(_topic_scores(run_scores))


def print_base_adv(measure_topic, repro_measure, base_value, adv_value=None):
    """
    Pretty print output in trec_eval inspired style. Use this for printing baseline and/or advanced results.

    @param measure_topic: The topic number.
    @param repro_measure: Name of the reproduction/replication measure.
    @param base_value: Value of the evaluated baseline run.
    @param adv_value: Value of the evaluated advanced run.
    """
    if adv_value:
        fill = ('{:3s}' if base_value < 0 else '{:4s}')
        print(('{:25s}{:8s}{:8s}{:.4f}' + fill + '{:8s}{:.4f}').format(measure_topic, repro_measure,
                                                                       'BASE', base_value, ' ', 'ADV', adv_value))
    else:
        print('{:25s}{:8s}{:8s}{:.4f}'.format(measure_topic, repro_measure, 'BASE', base_value))


def print_simple_line(measure, repro_measure, value):
    """
    Use this for printing lines with trec_eval and reproduction/replication measures.
    Pretty print output in trec_eval inspired style.
    @param measure: Name of the trec_eval measure.
    @param repro_measure: Name of the reproduction/replication measure.
    @param value: Value of the evaluated run.
    @return:
    """
    print('{:25s}{:8s}{:.4f}'.format(measure, repro_measure, value))


def break_ties(run):
    """
    Use this function to break score ties like it is implemented in trec_eval.
    Documents with the same score will be sorted in reverse alphabetical order.
    :param run: Run with score ties. Nested dictionary structure (cf. pytrec_eval)
    :return: Reordered run
    """
    for topic, ranking in run.items():
        docid_score_tuple = list(ranking.items())
        reordered_ranking = []
        for k, v in itertools.groupby(docid_score_tuple, lambda item: item[1]):
            reordered_ranking.extend(sorted(v, reverse=True))
        run[topic] = OrderedDict(reordered_ranking)
    return run
