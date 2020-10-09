import numpy as np
from copy import deepcopy
from tqdm import tqdm
from repro_eval.config import exclude


def diff(topic_score_a, topic_score_b):
    """
    Use this function to get a generator with absoulte differences
    between the topic scores of the baseline and advanced runs.

    @param topic_score_a: Topic scores of the advanced run.
    @param topic_score_b: Topic scores of the baseline run.
    @return: Generator with absolute differences between the topics scores.
    """
    for measure, value in topic_score_a.items():
        if measure not in exclude:
            yield measure, value - topic_score_b.get(measure)


def topic_diff(run_a, run_b):
    """
    Use this function to get a generator with absoulte differences
    between the topic scores of the baseline and advanced runs for each measure.

    @param run_a: The advanced run.
    @param run_b: The baseline run.
    @return: Generator with absolute differences between the topics scores for each measure.
    """
    run_a_cp = deepcopy(run_a)
    run_b_cp = deepcopy(run_b)

    for topic, measures in run_a_cp.items():
        yield topic, dict(diff(measures, run_b_cp.get(topic)))


def _mean_improvement(run_a, run_b):
    """
    Helping function returning a generator for determining the mean improvements.

    @param run_a: The advanced run.
    @param run_b: The baseline run.
    @return: Generator with mean improvements.
    """
    measures_all = list(list(run_a.values())[0].keys())
    measures_valid = [m for m in measures_all if m not in exclude]
    topics = run_a.keys()
    delta = dict(topic_diff(run_a, run_b))

    for measure in measures_valid:
        yield measure, np.array([delta.get(topic).get(measure) for topic in topics]).mean()


def mean_improvement(run_a, run_b):
    """
    Determines the relative improvement that is used to derive the Delta Relative Improvement (DeltaRI).

    @param run_a: The advanced run.
    @param run_b: The baseline run.
    @return: Dictionary with mean improvements for each measure.
    """
    return dict(_mean_improvement(run_a, run_b))


def _er(orig_score_a, orig_score_b, rep_score_a, rep_score_b, pbar=False):
    """
    Helping function returning a generator for determining the Effect Ratio (ER).

    @param orig_score_a: Scores of the original advanced run.
    @param orig_score_b: Scores of the original baseline run.
    @param rep_score_a: Scores of the reproduced/replicated advanced run.
    @param rep_score_b: Scores of the reproduced/replicated baseline run.
    @param pbar: Boolean value indicating if progress bar should be printed.
    @return: Generator with ER scores.
    """
    mi_orig = mean_improvement(orig_score_a, orig_score_b)
    mi_rep = mean_improvement(rep_score_a, rep_score_b)

    generator = tqdm(mi_rep.items()) if pbar else mi_rep.items()

    for measure, value in generator:
        yield measure, value / mi_orig.get(measure)


def ER(orig_score_a, orig_score_b, rep_score_a, rep_score_b, pbar=False):
    """
    Determines the Effect Ratio (ER) according to the following paper:
    Timo Breuer, Nicola Ferro, Norbert Fuhr, Maria Maistro, Tetsuya Sakai, Philipp Schaer, Ian Soboroff.
    How to Measure the Reproducibility of System-oriented IR Experiments.
    Proceedings of SIGIR, pages 349-358, 2020.

    The ER value is determined by the ratio between the mean improvements
    of the original and reproduced/replicated experiments.

    @param orig_score_a: Scores of the original advanced run.
    @param orig_score_b: Scores of the original baseline run.
    @param rep_score_a: Scores of the reproduced/replicated advanced run.
    @param rep_score_b: Scores of the reproduced/replicated baseline run.
    @param pbar: Boolean value indicating if progress bar should be printed.
    @return: Dictionary containing the ER values for the specified run combination.
    """
    return dict(_er(orig_score_a, orig_score_b, rep_score_a, rep_score_b, pbar=pbar))


def _mean_score(scores):
    """
    Helping function to determine the mean scores across the topics for each measure.

    @param scores: Run scores.
    @return: Generator with mean scores.
    """
    measures_all = list(list(scores.values())[0].keys())
    measures_valid = [m for m in measures_all if m not in exclude]
    topics = scores.keys()

    for measure in measures_valid:
        yield measure, np.array([scores.get(topic).get(measure) for topic in topics]).mean()


def mean_score(scores):
    """
    Use this function to compute the mean scores across the topics for each measure.

    @param scores: Run scores.
    @return: Dictionary containing the mean scores for each measure.
    """
    return dict(_mean_score(scores))


def _rel_improve(scores_a, scores_b):
    """
    Helping function returning a generator for determining the relative improvements.

    @param scores_a: Scores of the advanced run.
    @param scores_b: Scores of the baseline run.
    @return: Generator with relative improvements.
    """
    mean_scores_a = mean_score(scores_a)
    mean_scores_b = mean_score(scores_b)

    for measure, mean in mean_scores_a.items():
        yield measure, (mean - mean_scores_b.get(measure)) / mean_scores_b.get(measure)


def rel_improve(scores_a, scores_b):
    """
    Determines the relative improvement that is used to derive the Delta Relative Improvement (DeltaRI).

    @param scores_a: Scores of the advanced run.
    @param scores_b: Scores of the baseline run.
    @return: Dictionary with relative improvements for each measure.
    """
    return dict(_rel_improve(scores_a, scores_b))


def _deltaRI(orig_score_a, orig_score_b, rep_score_a, rep_score_b, pbar=False):
    """
    Helping function returning a generator for determining the Delta Relative Improvement (DeltaRI).

    @param orig_score_a: Scores of the original advanced run.
    @param orig_score_b: Scores of the original baseline run.
    @param rep_score_a: Scores of the reproduced/replicated advanced run.
    @param rep_score_b: Scores of the reproduced/replicated baseline run.
    @param pbar: Boolean value indicating if progress bar should be printed.
    @return: Generator with DeltaRI scores.
    """
    rel_improve_orig = rel_improve(orig_score_a, orig_score_b)
    rel_improve_rep = rel_improve(rep_score_a, rep_score_b)

    generator = tqdm(rel_improve_orig.items()) if pbar else rel_improve_orig.items()

    for measure, ri in generator:
        yield measure, ri - rel_improve_rep.get(measure)


def deltaRI(orig_score_a, orig_score_b, rep_score_a, rep_score_b, pbar=False):
    """
    Determines the Delta Relative Improvement (DeltaRI) according to the following paper:
    Timo Breuer, Nicola Ferro, Norbert Fuhr, Maria Maistro, Tetsuya Sakai, Philipp Schaer, Ian Soboroff.
    How to Measure the Reproducibility of System-oriented IR Experiments.
    Proceedings of SIGIR, pages 349-358, 2020.

    The DeltaRI value is determined by the difference between the relative improvements
    of the original and reproduced/replicated experiments.

    @param orig_score_a: Scores of the original advanced run.
    @param orig_score_b: Scores of the original baseline run.
    @param rep_score_a: Scores of the reproduced/replicated advanced run.
    @param rep_score_b: Scores of the reproduced/replicated baseline run.
    @param pbar: Boolean value indicating if progress bar should be printed.
    @return: Dictionary containing the DeltaRI values for the specified run combination.
    """
    return dict(_deltaRI(orig_score_a, orig_score_b, rep_score_a, rep_score_b, pbar=pbar))
