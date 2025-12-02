import itertools
from collections import defaultdict, OrderedDict
import numpy as np
import pandas as pd
import ir_measures
from ir_measures import *


def trim_run(run, thresh):
    """
    Use this function to trim a run to a length of a document length specified by thresh.

    @param run: The run to be trimmed.
    @param thresh: The threshold value of the run length.
    """
    for topic, _ in run.items():
        run[topic] = dict(list(run[topic].items())[:thresh])


def arp(topic_scores):
    """
    This function computes the Average Retrieval Performance (ARP), 
    see also: https://dl.acm.org/doi/10.1145/3397271.3401036

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
    measures = list(list(run.values())[0].keys())
    topics = run.keys()
    for measure in measures:
        yield measure, np.array(list([run.get(topic).get(measure) for topic in topics])).mean()


def arp_scores(run):
    """
    This function computes the Average Retrieval Performance (ARP) scores, 
    see also: https://dl.acm.org/doi/10.1145/3397271.3401036

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
    measures = list(list(run_scores.values())[0].keys())
    topics = run_scores.keys()
    for measure in measures:
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
    """
    print('{:25s}{:8s}{:.4f}'.format(measure, repro_measure, value))


def break_ties(run):
    """
    Use this function to break score ties like it is implemented in trec_eval.
    Documents with the same score will be sorted in reverse alphabetical order.
    
    @param run: Run with score ties. Nested dictionary structure (cf. pytrec_eval)
    @return: Reordered run
    """
    for topic, ranking in run.items():
        docid_score_tuple = list(ranking.items())
        reordered_ranking = []
        for _, v in itertools.groupby(docid_score_tuple, lambda item: item[1]):
            reordered_ranking.extend(sorted(v, reverse=True))
        run[topic] = OrderedDict(reordered_ranking)
    return run


def load_run(path):
    """
    Use this function to load a run in TREC-format with the help of ir_measures. 
    Documents with the same score will be sorted in reverse alphabetical order.
    
    @param path: Path to the run file.
    @return: Reordered run in a nested dictionary.
    """
    run = ir_measures.read_trec_run(path)
    nested_run = defaultdict(dict)
    for sd in run:
        nested_run[sd.query_id][sd.doc_id] = sd.score
    nested_run = dict(nested_run)
    nested_run = {t: nested_run[t] for t in sorted(nested_run)}
    return nested_run


def load_qrels(path):
    """
    Use this function to load a qrels file in TREC-format with the help of ir_measures. 
    
    @param path: Path to the qrels file.
    @return: Relevance labels in a nested dictionary.
    """
    qrels = ir_measures.read_trec_qrels(path)
    nested_qrels = defaultdict(dict)
    for d in qrels:
        nested_qrels[d.query_id][d.doc_id] = d.relevance
    nested_qrels = dict(nested_qrels)
    nested_qrels = {t: nested_qrels[t] for t in sorted(nested_qrels)}
    return nested_qrels


def load_measures():
    """
    Use this function to load retrieval measures that will be evaluated. 
    
    @return: List with measures following the naming convention of ir_measures.
    """
    measures = []
    trec_eval_measures = [
        'P', 'recall', 'ndcg', 'ndcg_cut', 'map_cut', 
        'set_map', 'set_P', 'set_relative_P', 'set_recall', 'set_F', 
        'Rprec', 'infAP', 'bpref', 'recip_rank', 'map', 'iprec_at_recall'
        ]
    for trec_eval_measure in trec_eval_measures:
        measures += ir_measures.convert_trec_name(trec_eval_measure) 
    parsed_measures = [ir_measures.parse_measure(measure) for measure in measures]
    return parsed_measures


def evaluate_run(measures, qrels, run):
    """
    Use this function to evaluate a run with the provided measures and qrels. 
    
    @param measures: List with a set of measures, cf. load_measures().
    @param qrels: The relevance labels (qrels), cf. load_qrels().
    @param run: The run to be evaluated, cf. load_run().
    @return: List with measures following ir_measures naming convention.
    """
    per_topic_results = pd.DataFrame(ir_measures.calc(measures, qrels, run)[1])
    return {
        qid: dict(zip(g["measure"].astype(str), g["value"]))
        for qid, g in per_topic_results.groupby("query_id")
    }
