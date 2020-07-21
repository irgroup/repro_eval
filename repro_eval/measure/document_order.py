from repro_eval.config import TRIM_THRESH, PHI
from scipy.stats.stats import kendalltau
from .external.rbo import rbo


def _ktau_union(orig_run, rep_run, trim_thresh=TRIM_THRESH):
    for topic, docs in rep_run.items():
        orig_docs = list(orig_run.get(topic).keys())[:trim_thresh]
        rep_docs = list(rep_run.get(topic).keys())[:trim_thresh]
        union = list(sorted(set(orig_docs + rep_docs)))
        orig_idx = [union.index(doc) for doc in orig_docs]
        rep_idx = [union.index(doc) for doc in rep_docs]
        yield topic, kendalltau(orig_idx, rep_idx).correlation


def ktau_union(orig_run, rep_run, trim_thresh=TRIM_THRESH):
    return dict(_ktau_union(orig_run, rep_run, trim_thresh=trim_thresh))


def _RBO(orig_run, rep_run, phi, trim_thresh=TRIM_THRESH):
    for topic, docs in rep_run.items():
        yield topic, rbo(list(rep_run.get(topic).keys())[:trim_thresh],
                         list(orig_run.get(topic).keys())[:trim_thresh],
                         p=phi).ext


def RBO(orig_run, rep_run, phi=PHI, trim_thresh=TRIM_THRESH):
    return dict(_RBO(orig_run, rep_run, phi=phi, trim_thresh=trim_thresh))