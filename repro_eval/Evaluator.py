import pytrec_eval
from repro_eval.util import trim
from repro_eval.measure.statistics import ttest
from repro_eval.measure.overall_effects import ER, deltaRI
from repro_eval.measure.document_order import ktau_union as ktu, RBO
from repro_eval.measure.effectiveness import rmse as RMSE
from repro_eval.config import ERR_MSG


class Evaluator(object):
    '''
    An abstract evaluator that holds the original baseline and advanced run as well as
    the reproduced/replicated baseline and advanced run.
    '''

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
        '''
        Trims all runs of the Evaluator to the length specified by the threshold value t.

        @param t: Threshold parameter or number of top-k documents to be considered.
        @param run: If run is not None, only the provided run will be trimmed.
        '''
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
        '''
        Evaluates the original baseline and advanced run if available.

        @param run: Reproduced or replicated run that will be evaluated.
        '''
        if self.run_b_orig:
            self.run_b_orig_score = self.rel_eval.evaluate(self.run_b_orig)
        if self.run_a_orig:
            self.run_a_orig_score = self.rel_eval.evaluate(self.run_a_orig)

    def er(self, run_b_score=None, run_a_score=None):
        '''
        Determines the Effect Ratio (ER) according to the following paper:
        Timo Breuer, Nicola Ferro, Norbert Fuhr, Maria Maistro, Tetsuya Sakai, Philipp Schaer, Ian Soboroff.
        How to Measure the Reproducibility of System-oriented IR Experiments.
        Proceedings of SIGIR, pages 349-358, 2020.

        The ER value is determined by the ratio between the mean improvements
        of the original and reproduced/replicated experiments.

        @param run_b_score: Scores of the baseline run,
                            if not provided the scores of the RpdEvaluator object will be used instead.
        @param run_a_score: Scores of the advanced run,
                            if not provided the scores of the RpdEvaluator object will be used instead.
        @return: Dictionary containing the ER values for the specified run combination.
        '''
        if self.run_b_orig_score and self.run_a_orig_score and run_b_score and run_a_score:
            return ER(orig_score_b=self.run_b_orig_score, orig_score_a=self.run_a_orig_score,
                      rep_score_b=run_b_score, rep_score_a=run_a_score)
        if self.run_b_orig_score and self.run_a_orig_score and self.run_b_rep_score and self.run_a_rep_score:
            return ER(orig_score_b=self.run_b_orig_score, orig_score_a=self.run_a_orig_score,
                      rep_score_b=self.run_b_rep_score, rep_score_a=self.run_a_rep_score)
        else:
            print(ERR_MSG)

    def dri(self, run_b_score=None, run_a_score=None):
        '''
        Determines the Delta Relative Improvement (DeltaRI) according to the following paper:
        Timo Breuer, Nicola Ferro, Norbert Fuhr, Maria Maistro, Tetsuya Sakai, Philipp Schaer, Ian Soboroff.
        How to Measure the Reproducibility of System-oriented IR Experiments.
        Proceedings of SIGIR, pages 349-358, 2020.

        The DeltaRI value is determined by the difference between the relative improvements
        of the original and reproduced/replicated experiments.

        @param run_b_score: Scores of the baseline run,
                            if not provided the scores of the RpdEvaluator object will be used instead.
        @param run_a_score: Scores of the advanced run,
                            if not provided the scores of the RpdEvaluator object will be used instead.
        @return: Dictionary containing the DRI values for the specified run combination.
        '''
        if self.run_b_orig_score and self.run_a_orig_score and run_b_score and run_a_score:
            return deltaRI(orig_score_b=self.run_b_orig_score, orig_score_a=self.run_a_orig_score,
                           rep_score_b=run_b_score, rep_score_a=run_a_score)
        if self.run_b_orig_score and self.run_a_orig_score and self.run_b_rep_score and self.run_a_rep_score:
            return deltaRI(orig_score_b=self.run_b_orig_score, orig_score_a=self.run_a_orig_score,
                           rep_score_b=self.run_b_rep_score, rep_score_a=self.run_a_rep_score)
        else:
            print(ERR_MSG)

    def _ttest(self, rpd=True, run_b_score=None, run_a_score=None):
        '''
        Conducts either a paired (reproducibility) or unpaired (replicability) two-sided t-test according to the following paper:
        Timo Breuer, Nicola Ferro, Norbert Fuhr, Maria Maistro, Tetsuya Sakai, Philipp Schaer, Ian Soboroff.
        How to Measure the Reproducibility of System-oriented IR Experiments.
        Proceedings of SIGIR, pages 349-358, 2020.

        @param rpd: Boolean indicating if the evaluated runs are reproduced.
        @param run_b_score: Scores of the baseline run,
                            if not provided the scores of the RpdEvaluator object will be used instead.
        @param run_a_score: Scores of the advanced run,
                            if not provided the scores of the RpdEvaluator object will be used instead.
        @return: Dictionary with p-values that compare the score distributions of the baseline and advanced run.
        '''
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
    '''
    The Reproducibility Evaluator is used for quantifying the different levels of reproduction for runs that were
    derived from the same test collection used in the original experiment.
    '''

    def evaluate(self, run=None):
        '''
        Evaluates the scores of the original and reproduced baseline and advanced runs.
        If a (reproduced) run is provided only this one will be evaluated and a dictionary with the corresponding
        scores is returned.
        @param run: A reproduced run. If not specified, the original and reproduced runs of the the RpdEvaluator will
                    be used instead.
        @return: If run is specified, a dictionary with the corresponding scores is returned.
        '''
        if run:
            return self.rel_eval.evaluate(run)

        super(RpdEvaluator, self).evaluate()
        if self.run_b_rep:
            self.run_b_rep_score = self.rel_eval.evaluate(self.run_b_rep)
        if self.run_a_rep:
            self.run_a_rep_score = self.rel_eval.evaluate(self.run_a_rep)

    def ktau_union(self, run_b_score=None, run_a_score=None):
        '''
        Determines Kendall's tau Union (KTU) between the original and reproduced document orderings
        according to the following paper:
        Timo Breuer, Nicola Ferro, Norbert Fuhr, Maria Maistro, Tetsuya Sakai, Philipp Schaer, Ian Soboroff.
        How to Measure the Reproducibility of System-oriented IR Experiments.
        Proceedings of SIGIR, pages 349-358, 2020.

        @param run_b_score: Scores of the baseline run,
                            if not provided the scores of the RpdEvaluator object will be used instead.
        @param run_a_score: Scores of the advanced run,
                            if not provided the scores of the RpdEvaluator object will be used instead.
        @return: Dictionary with KTU values that compare the document orderings of the original and reproduced runs.
        '''
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
        '''
        Determines the Rank-Biased Overlap (RBO) between the original and reproduced document orderings
        according to the following paper:
        Timo Breuer, Nicola Ferro, Norbert Fuhr, Maria Maistro, Tetsuya Sakai, Philipp Schaer, Ian Soboroff.
        How to Measure the Reproducibility of System-oriented IR Experiments.
        Proceedings of SIGIR, pages 349-358, 2020.

        @param run_b_score: Scores of the baseline run,
                            if not provided the scores of the RpdEvaluator object will be used instead.
        @param run_a_score: Scores of the advanced run,
                            if not provided the scores of the RpdEvaluator object will be used instead.
        @return: Dictionary with RBO values that compare the document orderings of the original and reproduced runs.
        '''
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
        '''
        Determines the Root Mean Square Error (RMSE) according to the following paper:
        Timo Breuer, Nicola Ferro, Norbert Fuhr, Maria Maistro, Tetsuya Sakai, Philipp Schaer, Ian Soboroff.
        How to Measure the Reproducibility of System-oriented IR Experiments.
        Proceedings of SIGIR, pages 349-358, 2020.

        @param run_b_score: Scores of the baseline run,
                            if not provided the scores of the RpdEvaluator object will be used instead.
        @param run_a_score: Scores of the advanced run,
                            if not provided the scores of the RpdEvaluator object will be used instead.
        @return: Dictionary with RMSE values that measure the closeness
                 between the topics scores of the original and reproduced runs.
        '''
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
        '''
        Conducts a paired two-tailed t-test for reproduced runs that were derived from the same test collection
        as in the original experiment.

        @param run_b_score: Scores of the baseline run,
                            if not provided the scores of the RpdEvaluator object will be used instead.
        @param run_a_score: Scores of the advanced run,
                            if not provided the scores of the RpdEvaluator object will be used instead.
        @return: Dictionary with p-values that compare the score distributions of the baseline and advanced run.
        '''
        return self._ttest(run_b_score=run_b_score, run_a_score=run_a_score)


class RplEvaluator(Evaluator):
    '''
    The Replicability Evaluator is used for quantifying the different levels of replication for runs that were
    derived from a test collection not used in the original experiment.
    '''
    def __init__(self, **kwargs):
        super(RplEvaluator, self).__init__(**kwargs)
        self.qrel_rpd_path = kwargs.get('qrel_rpd_path', None)

        if self.qrel_rpd_path:
            with open(self.qrel_rpd_path, 'r') as f_qrel:
                qrel_rpd = pytrec_eval.parse_qrel(f_qrel)
                self.rel_eval_rpd = pytrec_eval.RelevanceEvaluator(qrel_rpd, pytrec_eval.supported_measures)

    def evaluate(self, run=None):
        '''
        Evaluates the scores of the original and replicated baseline and advanced runs.
        If a (replicated) run is provided only this one will be evaluated and a dictionary with the corresponding
        scores is returned.
        @param run: A replicated run. If not specified, the original and replicated runs of the the RplEvaluator will
                    be used instead.
        @return: If run is specified, a dictionary with the corresponding scores is returned.
        '''
        if run:
            return self.rel_eval_rpd.evaluate(run)

        super(RplEvaluator, self).evaluate()
        if self.run_b_rep:
            self.run_b_rep_score = self.rel_eval_rpd.evaluate(self.run_b_rep)
        if self.run_a_rep:
            self.run_a_rep_score = self.rel_eval_rpd.evaluate(self.run_a_rep)

    def ttest(self, run_b_score=None, run_a_score=None):
        '''
        Conducts an un-paired two-tailed t-test for replicated runs that were derived from a test collection
        not used in the original experiment.

        @param run_b_score: Scores of the baseline run,
                            if not provided the scores of the RpdEvaluator object will be used instead.
        @param run_a_score: Scores of the advanced run,
                            if not provided the scores of the RpdEvaluator object will be used instead.
        @return: Dictionary with p-values that compare the score distributions of the baseline and advanced run.
        '''
        return self._ttest(rpd=False, run_b_score=run_b_score, run_a_score=run_a_score)
