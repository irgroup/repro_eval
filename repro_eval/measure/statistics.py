import math
from scipy.stats.stats import ttest_rel, ttest_ind
from tqdm import tqdm
from repro_eval.util import topic_scores


def _ttest(orig_score, rep_score, rpd=True, pbar=False):
    """

    @param orig_score: The original scores.
    @param rep_score: The reproduced/replicated scores.
    @param rpd: Boolean indicating if the evaluated runs are reproduced.
    @param pbar: Boolean value indicating if progress bar should be printed.
    @return: Generator with p-values.
    """
    if rpd:  # paired two-tailed t-test
        topic_scores_orig = topic_scores(orig_score)
        topic_scores_rep = topic_scores(rep_score)

        generator = tqdm(topic_scores_orig.items()) if pbar else topic_scores_orig.items()

        for measure, scores in generator:
            yield measure, ttest_rel(scores, topic_scores_rep.get(measure)).pvalue

    else:  # else unpaired two-tailed t-test
        topic_scores_orig = topic_scores(orig_score)
        topic_scores_rep = topic_scores(rep_score)

        generator = tqdm(topic_scores_orig.items()) if pbar else topic_scores_orig.items()

        for measure, scores in generator:
            yield measure, ttest_ind(scores, topic_scores_rep.get(measure)).pvalue


def ttest(orig_score, rep_score, rpd=True, pbar=False):
    """

    @param orig_score: The original scores.
    @param rep_score: The reproduced/replicated scores.
    @param rpd: Boolean indicating if the evaluated runs are reproduced.
    @param pbar: Boolean value indicating if progress bar should be printed.
    @return: Dictionary with p-values that compare the score distributions of the baseline and advanced run.
    """
    pvals = dict(_ttest(orig_score, rep_score, rpd=rpd, pbar=pbar))
    nan_list = list(filter(lambda x: math.isnan(x), pvals.values()))
    if len(nan_list) == len(pvals):  # is every pval is nan?
        if orig_score == rep_score:  # equal score distributions?
            pvals = dict.fromkeys(pvals, 1.0)

    return pvals
