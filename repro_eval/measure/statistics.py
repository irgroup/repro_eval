from scipy.stats.stats import ttest_rel, ttest_ind
from . import topic_scores


def _ttest(orig_score, rep_score, rpl=True):
    if rpl: # paired two-tailed t-test
        topic_scores_orig = topic_scores(orig_score)
        topic_scores_rep = topic_scores(rep_score)

        for measure, scores in topic_scores_orig.items():
            yield measure, ttest_rel(scores, topic_scores_rep.get(measure)).pvalue

    else:  # else unpaired two-tailed t-test
        topic_scores_orig = topic_scores(orig_score)
        topic_scores_rep = topic_scores(rep_score)

        for measure, scores in topic_scores_orig.items():
            yield measure, ttest_ind(scores, topic_scores_rep.get(measure)).pvalue


def ttest(orig_score, rep_score, rpl=True):
    return dict(_ttest(orig_score, rep_score, rpl=rpl))