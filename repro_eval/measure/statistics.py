from scipy.stats.stats import ttest_rel, ttest_ind
from repro_eval.util import topic_scores


def _ttest(orig_score, rep_score, rpd=True):
    """

    @param orig_score: The original scores.
    @param rep_score: The reproduced/replicated scores.
    @param rpd: Boolean indicating if the evaluated runs are reproduced.
    @return: Generator with p-values.
    """
    if rpd: # paired two-tailed t-test
        topic_scores_orig = topic_scores(orig_score)
        topic_scores_rep = topic_scores(rep_score)

        for measure, scores in topic_scores_orig.items():
            yield measure, ttest_rel(scores, topic_scores_rep.get(measure)).pvalue

    else:  # else unpaired two-tailed t-test
        topic_scores_orig = topic_scores(orig_score)
        topic_scores_rep = topic_scores(rep_score)

        for measure, scores in topic_scores_orig.items():
            yield measure, ttest_ind(scores, topic_scores_rep.get(measure)).pvalue


def ttest(orig_score, rep_score, rpd=True):
    """

    @param orig_score: The original scores.
    @param rep_score: The reproduced/replicated scores.
    @param rpd: Boolean indicating if the evaluated runs are reproduced.
    @return: Dictionary with p-values that compare the score distributions of the baseline and advanced run.
    """
    return dict(_ttest(orig_score, rep_score, rpd=rpd))
