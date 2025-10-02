from repro_eval import TRIM_THRESH
from scipy.stats.stats import kendalltau
from tqdm import tqdm
from repro_eval.util import break_ties
import numpy as np


def _rbo(run, ideal, p, depth):
    # Implementation reproduced from Clarke et al.
    # paper: https://dl.acm.org/doi/10.1145/3451161
    # code: https://github.com/claclark/Compatibility
    run_set = set()
    ideal_set = set()
    score = 0.0
    normalizer = 0.0
    weight = 1.0
    for i in range(depth):
        if i < len(run):
            run_set.add(run[i])
        if i < len(ideal):
            ideal_set.add(ideal[i])
        score += weight*len(ideal_set.intersection(run_set))/(i + 1)
        normalizer += weight
        weight *= p
    return score/normalizer


def _ktau_union(orig_run, rep_run, trim_thresh=TRIM_THRESH, pbar=False):
    """
    Helping function returning a generator to determine Kendall's tau Union (KTU) for all topics.

    @param orig_run: The original run.
    @param rep_run: The reproduced/replicated run.
    @param trim_thresh: Threshold values for the number of documents to be compared.
    @param pbar: Boolean value indicating if progress bar should be printed.
    @return: Generator with KTU values.
    """

    generator = tqdm(rep_run.items()) if pbar else rep_run.items()

    for topic, _ in generator:
        orig_docs = list(orig_run.get(topic).keys())[:trim_thresh]
        rep_docs = list(rep_run.get(topic).keys())[:trim_thresh]
        union = list(sorted(set(orig_docs + rep_docs)))
        orig_idx = [union.index(doc) for doc in orig_docs]
        rep_idx = [union.index(doc) for doc in rep_docs]
        yield topic, float(round(kendalltau(orig_idx, rep_idx).correlation, 14))


def ktau_union(orig_run, rep_run, trim_thresh=TRIM_THRESH, pbar=False, per_topic=False):
    """
    Determines the Kendall's tau Union (KTU) between the original and reproduced document orderings,
    see also: https://dl.acm.org/doi/10.1145/3397271.3401036

    @param orig_run: The original run.
    @param rep_run: The reproduced/replicated run.
    @param trim_thresh: Threshold values for the number of documents to be compared.
    @param pbar: Boolean value indicating if progress bar should be printed.
    @return: Dictionary with KTU values that compare the document orderings of the original and reproduced runs.
    """

    # Safety check for runs that are not added via pytrec_eval
    orig_run = break_ties(orig_run)
    rep_run = break_ties(rep_run)
    ktu_per_topic = dict(_ktau_union(orig_run, rep_run, trim_thresh=trim_thresh, pbar=pbar))
    if per_topic:
        return ktu_per_topic  
    else:
        return float(np.mean(list(ktu_per_topic.values())))


def _RBO(orig_run, rep_run, p, depth, pbar=False):
    """
    Helping function returning a generator to determine the Rank-Biased Overlap (RBO) for all topics.

    @param orig_run: The original run.
    @param rep_run: The reproduced/replicated run.
    @param phi: Parameter for top-heaviness of the RBO.
    @param trim_thresh: Threshold values for the number of documents to be compared.
    @param pbar: Boolean value indicating if progress bar should be printed.
    
    @return: Generator with RBO values.
    """

    generator = tqdm(rep_run.items()) if pbar else rep_run.items()

    for topic, _ in generator:
        yield topic, _rbo(list(rep_run.get(topic).keys()),
                    list(orig_run.get(topic).keys()),
                    p=p,
                    depth=depth)
        

def RBO(orig_run, rep_run, p, depth, pbar, per_topic):
    """
    Determines the Rank-Biased Overlap (RBO) between the original and reproduced document orderings,
    see also: https://dl.acm.org/doi/10.1145/3397271.3401036

    @param orig_run: The original run.
    @param rep_run: The reproduced/replicated run.
    @param phi: Parameter for top-heaviness of the RBO.
    @param trim_thresh: Threshold values for the number of documents to be compared.
    @param pbar: Boolean value indicating if progress bar should be printed.
    @param misinfo: Use the RBO implementation that is also used in the TREC Health Misinformation Track.
                    See also: https://github.com/claclark/Compatibility
    @return: Dictionary with RBO values that compare the document orderings of the original and reproduced runs.
    """

    # Safety check for runs that are not added via pytrec_eval
    orig_run = break_ties(orig_run)
    rep_run = break_ties(rep_run)
    rbo_per_topic = dict(_RBO(orig_run, rep_run, p=p, depth=depth, pbar=pbar))
    if per_topic:
        return rbo_per_topic  
    else:
        return float(np.mean(list(rbo_per_topic.values())))
