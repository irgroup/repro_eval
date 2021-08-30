"""Evaluation measures at the level of document orderings."""

from repro_eval.config import TRIM_THRESH, PHI
from scipy.stats.stats import kendalltau
from tqdm import tqdm
from repro_eval.measure.external.rbo import rbo
from repro_eval.util import break_ties


def _rbo(run, ideal, p, depth):
    # Implementation taken from the TREC Health Misinformation Track with modifications
    # see also: https://github.com/claclark/Compatibility
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

    for topic, docs in generator:
        orig_docs = list(orig_run.get(topic).keys())[:trim_thresh]
        rep_docs = list(rep_run.get(topic).keys())[:trim_thresh]
        union = list(sorted(set(orig_docs + rep_docs)))
        orig_idx = [union.index(doc) for doc in orig_docs]
        rep_idx = [union.index(doc) for doc in rep_docs]
        yield topic, round(kendalltau(orig_idx, rep_idx).correlation, 14)


def ktau_union(orig_run, rep_run, trim_thresh=TRIM_THRESH, pbar=False):
    """
    Determines the Kendall's tau Union (KTU) between the original and reproduced document orderings
    according to the following paper:
    Timo Breuer, Nicola Ferro, Norbert Fuhr, Maria Maistro, Tetsuya Sakai, Philipp Schaer, Ian Soboroff.
    How to Measure the Reproducibility of System-oriented IR Experiments.
    Proceedings of SIGIR, pages 349-358, 2020.

    @param orig_run: The original run.
    @param rep_run: The reproduced/replicated run.
    @param trim_thresh: Threshold values for the number of documents to be compared.
    @param pbar: Boolean value indicating if progress bar should be printed.
    @return: Dictionary with KTU values that compare the document orderings of the original and reproduced runs.
    """

    # Safety check for runs that are not added via pytrec_eval
    orig_run = break_ties(orig_run)
    rep_run = break_ties(rep_run)

    return dict(_ktau_union(orig_run, rep_run, trim_thresh=trim_thresh, pbar=pbar))


def _RBO(orig_run, rep_run, phi, trim_thresh=TRIM_THRESH, pbar=False, misinfo=True):
    """
    Helping function returning a generator to determine the Rank-Biased Overlap (RBO) for all topics.

    @param orig_run: The original run.
    @param rep_run: The reproduced/replicated run.
    @param phi: Parameter for top-heaviness of the RBO.
    @param trim_thresh: Threshold values for the number of documents to be compared.
    @param pbar: Boolean value indicating if progress bar should be printed.
    @param misinfo: Use the RBO implementation that is also used in the TREC Health Misinformation Track.
                    See also: https://github.com/claclark/Compatibility
    @return: Generator with RBO values.
    """

    generator = tqdm(rep_run.items()) if pbar else rep_run.items()

    if misinfo:
        for topic, docs in generator:
            yield topic, _rbo(list(rep_run.get(topic).keys())[:trim_thresh],
                              list(orig_run.get(topic).keys())[:trim_thresh],
                              p=phi,
                              depth=trim_thresh)

    else:
        for topic, docs in generator:
            yield topic, rbo(list(rep_run.get(topic).keys())[:trim_thresh],
                             list(orig_run.get(topic).keys())[:trim_thresh],
                             p=phi).ext


def RBO(orig_run, rep_run, phi=PHI, trim_thresh=TRIM_THRESH, pbar=False, misinfo=True):
    """
    Determines the Rank-Biased Overlap (RBO) between the original and reproduced document orderings
    according to the following paper:
    Timo Breuer, Nicola Ferro, Norbert Fuhr, Maria Maistro, Tetsuya Sakai, Philipp Schaer, Ian Soboroff.
    How to Measure the Reproducibility of System-oriented IR Experiments.
    Proceedings of SIGIR, pages 349-358, 2020.

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

    return dict(_RBO(orig_run, rep_run, phi=phi, trim_thresh=trim_thresh, pbar=pbar, misinfo=misinfo))
