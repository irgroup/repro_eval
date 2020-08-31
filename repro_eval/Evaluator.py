import pytrec_eval
from repro_eval.util import trim
from repro_eval.measure.statistics import ttest
from repro_eval.measure.overall_effects import ER, deltaRI
from repro_eval.measure.document_order import ktau_union as ktu, RBO
from repro_eval.measure.effectiveness import rmse as RMSE
from repro_eval.config import ERR_MSG


class Evaluator(object):

    def __init__(self, **kwargs):
        self.qrel_orig_path = kwargs.get('qrel_orig_path', None)
        self.run_b_orig_path = kwargs.get('run_b_orig_path', None)
        self.run_a_orig_path = kwargs.get('run_a_orig_path', None)
        self.run_b_rep_path = kwargs.get('run_b_rep_path', None)
        self.run_a_rep_path = kwargs.get('run_a_rep_path', None)
        self.run_b_orig = None
        self.run_a_orig = None
        self.run_b_rep = None
        self.run_a_rep = None
        self.run_b_orig_score = None
        self.run_a_orig_score = None
        self.run_b_rep_score = None
        self.run_a_rep_score = None

        if self.qrel_orig_path:
            with open(self.qrel_orig_path, 'r') as f_qrel:
                qrel_orig = pytrec_eval.parse_qrel(f_qrel)
                self.rel_eval = pytrec_eval.RelevanceEvaluator(qrel_orig, pytrec_eval.supported_measures)

        if self.run_b_orig_path:
            with open(self.run_b_orig_path, 'r') as f_run:
                self.run_b_orig = pytrec_eval.parse_run(f_run)

        if self.run_a_orig_path:
            with open(self.run_a_orig_path, 'r') as f_run:
                self.run_a_orig = pytrec_eval.parse_run(f_run)

        if self.run_b_rep_path:
            with open(self.run_b_rep_path, 'r') as f_run:
                self.run_b_rep = pytrec_eval.parse_run(f_run)

        if self.run_a_rep_path:
            with open(self.run_a_rep_path, 'r') as f_run:
                self.run_a_rep = pytrec_eval.parse_run(f_run)

    def trim(self, t=None, run=None):
        if run:
            if t:
                trim(run, thresh=t)
            else:
                trim(run)
            return

        if self.run_b_orig:
            if t:
                trim(self.run_b_orig, thresh=t)
            else:
                trim(self.run_b_orig)

        if self.run_a_orig:
            if t:
                trim(self.run_a_orig, thresh=t)
            else:
                trim(self.run_a_orig)

        if self.run_b_rep:
            if t:
                trim(self.run_b_rep, thresh=t)
            else:
                trim(self.run_b_rep)

        if self.run_a_rep:
            if t:
                trim(self.run_a_rep, thresh=t)
            else:
                trim(self.run_a_rep)

    def evaluate(self, run=None):
        if self.run_b_orig:
            self.run_b_orig_score = self.rel_eval.evaluate(self.run_b_orig)
        if self.run_a_orig:
            self.run_a_orig_score = self.rel_eval.evaluate(self.run_a_orig)

    def er(self, run_b_score=None, run_a_score=None):
        if self.run_b_orig_score and self.run_a_orig_score and run_b_score and run_a_score:
            return ER(orig_score_b=self.run_b_orig_score, orig_score_a=self.run_a_orig_score,
                      rep_score_b=run_b_score, rep_score_a=run_a_score)
        if self.run_b_orig_score and self.run_a_orig_score and self.run_b_rep_score and self.run_a_rep_score:
            return ER(orig_score_b=self.run_b_orig_score, orig_score_a=self.run_a_orig_score,
                      rep_score_b=self.run_b_rep_score, rep_score_a=self.run_a_rep_score)
        else:
            print(ERR_MSG)

    def dri(self, run_b_score=None, run_a_score=None):
        if self.run_b_orig_score and self.run_a_orig_score and run_b_score and run_a_score:
            return deltaRI(orig_score_b=self.run_b_orig_score, orig_score_a=self.run_a_orig_score,
                           rep_score_b=run_b_score, rep_score_a=run_a_score)
        if self.run_b_orig_score and self.run_a_orig_score and self.run_b_rep_score and self.run_a_rep_score:
            return deltaRI(orig_score_b=self.run_b_orig_score, orig_score_a=self.run_a_orig_score,
                           rep_score_b=self.run_b_rep_score, rep_score_a=self.run_a_rep_score)
        else:
            print(ERR_MSG)

    def _ttest(self, rpd=True, run_b_score=None, run_a_score=None):
        if self.run_b_orig_score and self.run_b_rep_score:
            if run_b_score and run_a_score:
                return {'baseline': ttest(self.run_b_orig_score, run_b_score, rpd=rpd),
                        'advanced': ttest(self.run_a_orig_score, run_a_score, rpd=rpd)}
            if run_b_score:
                return {'baseline': ttest(self.run_b_orig_score, run_b_score, rpd=rpd)}
            if self.run_a_orig_score and self.run_a_rep_score:
                return {'baseline': ttest(self.run_b_orig_score, self.run_b_rep_score, rpd=rpd),
                        'advanced': ttest(self.run_a_orig_score, self.run_a_rep_score, rpd=rpd)}
            else:
                return {'baseline': ttest(self.run_b_orig_score, self.run_b_rep_score, rpd=rpd)}
        else:
            print(ERR_MSG)


class RpdEvaluator(Evaluator):

    def evaluate(self, run=None):
        if run:
            return self.rel_eval.evaluate(run)

        super(RpdEvaluator, self).evaluate()
        if self.run_b_rep:
            self.run_b_rep_score = self.rel_eval.evaluate(self.run_b_rep)
        if self.run_a_rep:
            self.run_a_rep_score = self.rel_eval.evaluate(self.run_a_rep)

    def ktau_union(self, run_b_score=None, run_a_score=None):
        if self.run_b_orig_score and run_b_score:
            if self.run_a_orig_score and run_a_score:
                return {'baseline': ktu(self.run_b_orig, run_b_score),
                        'advanced': ktu(self.run_a_orig, run_a_score)}
            else:
                return {'baseline':  ktu(self.run_b_orig, run_b_score)}
        if self.run_b_orig_score and self.run_b_rep_score:
            if self.run_a_orig_score and self.run_a_rep_score:
                return {'baseline': ktu(self.run_b_orig, self.run_b_rep),
                        'advanced': ktu(self.run_a_orig, self.run_a_rep)}
            else:
                return {'baseline':  ktu(self.run_b_orig, self.run_b_rep)}
        else:
            print(ERR_MSG)

    def rbo(self, run_b_score=None, run_a_score=None):
        if self.run_b_orig_score and run_b_score:
            if self.run_a_orig_score and run_a_score:
                return {'baseline': RBO(self.run_b_orig, run_b_score),
                        'advanced': RBO(self.run_a_orig, run_a_score)}
            else:
                return {'baseline':  RBO(self.run_b_orig, run_b_score)}
        if self.run_b_orig_score and self.run_b_rep_score:
            if self.run_a_orig_score and self.run_a_rep_score:
                return {'baseline': RBO(self.run_b_orig, self.run_b_rep),
                        'advanced': RBO(self.run_a_orig, self.run_a_rep)}
            else:
                return {'baseline':  RBO(self.run_b_orig, self.run_b_rep)}
        else:
            print(ERR_MSG)

    def rmse(self, run_b_score=None, run_a_score=None):
        if self.run_b_orig_score and run_b_score:
            if self.run_a_orig_score and run_a_score:
                return {'baseline': RMSE(self.run_b_orig_score, run_b_score),
                        'advanced': RMSE(self.run_a_orig_score, run_a_score)}
            else:
                return {'baseline': RMSE(self.run_b_orig_score, run_b_score)}
        if self.run_b_orig_score and self.run_b_rep_score:
            if self.run_a_orig_score and self.run_a_rep_score:
                return {'baseline': RMSE(self.run_b_orig_score, self.run_b_rep_score),
                        'advanced': RMSE(self.run_a_orig_score, self.run_a_rep_score)}
            else:
                return {'baseline': RMSE(self.run_b_orig_score, self.run_b_rep_score)}
        else:
            print(ERR_MSG)

    def ttest(self, run_b_score=None, run_a_score=None):
        return self._ttest(run_b_score=run_b_score, run_a_score=run_a_score)


class RplEvaluator(Evaluator):

    def __init__(self, **kwargs):
        super(RplEvaluator, self).__init__(**kwargs)
        self.qrel_rpd_path = kwargs.get('qrel_rpd_path', None)

        if self.qrel_rpd_path:
            with open(self.qrel_rpd_path, 'r') as f_qrel:
                qrel_rpd = pytrec_eval.parse_qrel(f_qrel)
                self.rel_eval_rpd = pytrec_eval.RelevanceEvaluator(qrel_rpd, pytrec_eval.supported_measures)

    def evaluate(self, run=None):
        if run:
            return self.rel_eval_rpd.evaluate(run)

        super(RplEvaluator, self).evaluate()
        if self.run_b_rep:
            self.run_b_rep_score = self.rel_eval_rpd.evaluate(self.run_b_rep)
        if self.run_a_rep:
            self.run_a_rep_score = self.rel_eval_rpd.evaluate(self.run_a_rep)

    def ttest(self, run_b_score=None, run_a_score=None):
        return self._ttest(rpd=False, run_b_score=run_b_score, run_a_score=run_a_score)
