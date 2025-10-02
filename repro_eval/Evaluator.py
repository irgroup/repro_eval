import ir_measures
from ir_measures import *
import pandas as pd
from collections import defaultdict
from repro_eval.util import trim, break_ties
from repro_eval.measure.statistics import ttest
from repro_eval.measure.overall_effects import ER, deltaRI
from repro_eval.measure.document_order import ktau_union, RBO
from repro_eval.measure.effectiveness import rmse as RMSE, nrmse as nRMSE
from repro_eval import ERR_MSG, RBO_DEPTH, RBO_P


def load_run(path): 
    run = ir_measures.read_trec_run(path)
    nested_run = defaultdict(dict)
    for sd in run:
        nested_run[sd.query_id][sd.doc_id] = sd.score
    nested_run = dict(nested_run)
    nested_run = {t: nested_run[t] for t in sorted(nested_run)}
    return nested_run


def load_qrels(path):
    qrels = ir_measures.read_trec_qrels(path)
    nested_qrels = defaultdict(dict)
    for d in qrels:
        nested_qrels[d.query_id][d.doc_id] = d.relevance
    nested_qrels = dict(nested_qrels)
    nested_qrels = {t: nested_qrels[t] for t in sorted(nested_qrels)}
    return nested_qrels


def load_measures():
    measures = []
    trec_eval_measures = [
        'P', 'recall', 'ndcg', 'ndcg_cut', 'map_cut', 
        'set_map', 'set_P', 'set_relative_P', 'set_recall', 'set_F', 
        'Rprec', 'infAP', 'bpref', 'recip_rank', 'map', 'iprec_at_recall'
        # 'num_rel_ret', 'num_ret', 'num_rel', 'num_q', 
        ]
    for trec_eval_measure in trec_eval_measures:
        measures += ir_measures.convert_trec_name(trec_eval_measure) 
    parsed_measures = [ir_measures.parse_measure(measure) for measure in measures]
    return parsed_measures


class Evaluator(object):
    """
    An abstract evaluator that holds the original baseline and advanced run as well as
    the reproduced/replicated baseline and advanced run.
    """

    def __init__(self, **kwargs):
        self.qrels_orig_path = kwargs.get('qrels_orig_path', None)
        self.qrels_orig = load_qrels(self.qrels_orig_path)
        self.run_b_orig_path = kwargs.get('run_b_orig_path', None)
        self.run_a_orig_path = kwargs.get('run_a_orig_path', None)
        self.run_b_rep_path = kwargs.get('run_b_rep_path', None)
        self.run_a_rep_path = kwargs.get('run_a_rep_path', None)
        self.run_b_orig = load_run(self.run_b_orig_path) if self.run_b_orig_path else None
        self.run_a_orig = load_run(self.run_a_orig_path) if self.run_a_orig_path else None
        self.run_b_rep = load_run(self.run_b_rep_path) if self.run_b_rep_path else None
        self.run_a_rep = load_run(self.run_a_rep_path) if self.run_a_rep_path else None
        self.run_b_orig_score = None
        self.run_a_orig_score = None
        self.run_b_rep_score = None
        self.run_a_rep_score = None
        self.measures = load_measures()


    def trim(self, t=None, run=None):
        """
        Trims all runs of the Evaluator to the length specified by the threshold value t.

        @param t: Threshold parameter or number of top-k documents to be considered.
        @param run: If run is not None, only the provided run will be trimmed.
        """
        if run:
            run = break_ties(run)
            if t:
                trim(run, thresh=t)
            else:
                trim(run)
            return

        if self.run_b_orig:
            self.run_b_orig = break_ties(self.run_b_orig)
            if t:
                trim(self.run_b_orig, thresh=t)
            else:
                trim(self.run_b_orig)

        if self.run_a_orig:
            self.run_a_orig = break_ties(self.run_a_orig)
            if t:
                trim(self.run_a_orig, thresh=t)
            else:
                trim(self.run_a_orig)

        if self.run_b_rep:
            self.run_b_rep = break_ties(self.run_b_rep)
            if t:
                trim(self.run_b_rep, thresh=t)
            else:
                trim(self.run_b_rep)

        if self.run_a_rep:
            self.run_a_rep = break_ties(self.run_a_rep)
            if t:
                trim(self.run_a_rep, thresh=t)
            else:
                trim(self.run_a_rep)

    def evaluate(self):
        """
        Evaluates the original baseline and advanced run if available.

        @param run: Reproduced or replicated run that will be evaluated.
        """

        if self.run_b_orig:
            self.run_b_orig = break_ties(self.run_b_orig)
            per_topic_results = pd.DataFrame(ir_measures.calc(self.measures, self.qrels_orig, self.run_b_orig)[1])
            self.run_b_orig_score =  {
                qid: dict(zip(g["measure"].astype(str), g["value"]))
                for qid, g in per_topic_results.groupby("query_id")
            }

        if self.run_a_orig:
            self.run_a_orig = break_ties(self.run_a_orig)
            per_topic_results = pd.DataFrame(ir_measures.calc(self.measures, self.qrels_orig, self.run_a_orig)[1])
            self.run_a_orig_score =  {
                qid: dict(zip(g["measure"].astype(str), g["value"]))
                for qid, g in per_topic_results.groupby("query_id")
            }

    def er(self, run_b_score=None, run_a_score=None, run_b_path=None, run_a_path=None, print_feedback=False):
        """
        Determines the Effect Ratio (ER), see also: https://dl.acm.org/doi/10.1145/3397271.3401036

        The ER value is determined by the ratio between the mean improvements
        of the original and reproduced/replicated experiments.

        @param run_b_score: Scores of the baseline run,
                            if not provided the scores of the RpdEvaluator object will be used instead.
        @param run_a_score: Scores of the advanced run,
                            if not provided the scores of the RpdEvaluator object will be used instead.
        @param print_feedback: Boolean value indicating if feedback on progress should be printed.
        @return: Dictionary containing the ER values for the specified run combination.
        """
        if print_feedback:
            print('Determining Effect Ratio (ER)')

        if self.run_b_orig_score and self.run_a_orig_score and run_b_path and run_a_path:
            with open(run_b_path, 'r') as b_run, open(run_a_path, 'r') as a_run:
                run_b_rep = pytrec_eval.parse_run(b_run)
                run_b_rep = {t: run_b_rep[t] for t in sorted(run_b_rep)}
                run_b_rep_score = self.rel_eval_rpl.evaluate(run_b_rep) if hasattr(self, 'rel_eval_rpl') else self.rel_eval.evaluate(run_b_rep)
                run_a_rep = pytrec_eval.parse_run(a_run)
                run_a_rep = {t: run_a_rep[t] for t in sorted(run_a_rep)}
                run_a_rep_score = self.rel_eval_rpl.evaluate(run_a_rep) if hasattr(self, 'rel_eval_rpl') else self.rel_eval.evaluate(run_a_rep)
            return ER(orig_score_b=self.run_b_orig_score, orig_score_a=self.run_a_orig_score,
                      rep_score_b=run_b_rep_score, rep_score_a=run_a_rep_score, pbar=print_feedback)

        if self.run_b_orig_score and self.run_a_orig_score and run_b_score and run_a_score:
            return ER(orig_score_b=self.run_b_orig_score, orig_score_a=self.run_a_orig_score,
                      rep_score_b=run_b_score, rep_score_a=run_a_score, pbar=print_feedback)

        if self.run_b_orig_score and self.run_a_orig_score and self.run_b_rep_score and self.run_a_rep_score:
            return ER(orig_score_b=self.run_b_orig_score, orig_score_a=self.run_a_orig_score,
                      rep_score_b=self.run_b_rep_score, rep_score_a=self.run_a_rep_score, pbar=print_feedback)
        else:
            print(ERR_MSG)

    def dri(self, run_b_score=None, run_a_score=None, run_b_path=None, run_a_path=None, print_feedback=False):
        """
        Determines the Delta Relative Improvement (DeltaRI), see also: https://dl.acm.org/doi/10.1145/3397271.3401036

        The DeltaRI value is determined by the difference between the relative improvements
        of the original and reproduced/replicated experiments.

        @param run_b_score: Scores of the baseline run,
                            if not provided the scores of the RpdEvaluator object will be used instead.
        @param run_a_score: Scores of the advanced run,
                            if not provided the scores of the RpdEvaluator object will be used instead.
        @param print_feedback: Boolean value indicating if feedback on progress should be printed.
        @return: Dictionary containing the DRI values for the specified run combination.
        """
        if print_feedback:
            print('Determining Delta Relative Improvement (DRI)')

        if self.run_b_orig_score and self.run_a_orig_score and run_b_path and run_a_path:
            with open(run_b_path, 'r') as b_run, open(run_a_path, 'r') as a_run:
                run_b_rep = pytrec_eval.parse_run(b_run)
                run_b_rep = {t: run_b_rep[t] for t in sorted(run_b_rep)}
                run_b_rep_score = self.rel_eval_rpl.evaluate(run_b_rep) if hasattr(self, 'rel_eval_rpl') else self.rel_eval.evaluate(run_b_rep)
                run_a_rep = pytrec_eval.parse_run(a_run)
                run_a_rep = {t: run_a_rep[t] for t in sorted(run_a_rep)}
                run_a_rep_score = self.rel_eval_rpl.evaluate(run_a_rep) if hasattr(self, 'rel_eval_rpl') else self.rel_eval.evaluate(run_a_rep)
            return deltaRI(orig_score_b=self.run_b_orig_score, orig_score_a=self.run_a_orig_score,
                           rep_score_b=run_b_rep_score, rep_score_a=run_a_rep_score, pbar=print_feedback)

        if self.run_b_orig_score and self.run_a_orig_score and run_b_score and run_a_score:
            return deltaRI(orig_score_b=self.run_b_orig_score, orig_score_a=self.run_a_orig_score,
                           rep_score_b=run_b_score, rep_score_a=run_a_score, pbar=print_feedback)

        if self.run_b_orig_score and self.run_a_orig_score and self.run_b_rep_score and self.run_a_rep_score:
            return deltaRI(orig_score_b=self.run_b_orig_score, orig_score_a=self.run_a_orig_score,
                           rep_score_b=self.run_b_rep_score, rep_score_a=self.run_a_rep_score, pbar=print_feedback)
        else:
            print(ERR_MSG)

    def _ttest(self, rpd=True, run_b_score=None, run_a_score=None, print_feedback=False):
        """
        Conducts either a paired (reproducibility) or unpaired (replicability) two-sided t-test,
        see also: https://dl.acm.org/doi/10.1145/3397271.3401036

        @param rpd: Boolean indicating if the evaluated runs are reproduced.
        @param run_b_score: Scores of the baseline run,
                            if not provided the scores of the RpdEvaluator object will be used instead.
        @param run_a_score: Scores of the advanced run,
                            if not provided the scores of the RpdEvaluator object will be used instead.
        @param print_feedback: Boolean value indicating if feedback on progress should be printed.
        @return: Dictionary with p-values that compare the score distributions of the baseline and advanced run.
        """
        if self.run_b_orig_score and (self.run_b_rep_score or run_b_score):
            if run_b_score and run_a_score:
                if print_feedback:
                    print('Determining p-values of t-test for baseline and advanced run.')
                return {'baseline': ttest(self.run_b_orig_score, run_b_score, rpd=rpd, pbar=print_feedback),
                        'advanced': ttest(self.run_a_orig_score, run_a_score, rpd=rpd, pbar=print_feedback)}
            if run_b_score:
                if print_feedback:
                    print('Determining p-values of t-test for baseline run.')
                return {'baseline': ttest(self.run_b_orig_score, run_b_score, rpd=rpd, pbar=print_feedback)}
            if self.run_a_orig_score and self.run_a_rep_score:
                if print_feedback:
                    print('Determining p-values of t-test for baseline and advanced run.')
                return {'baseline': ttest(self.run_b_orig_score, self.run_b_rep_score, rpd=rpd, pbar=print_feedback),
                        'advanced': ttest(self.run_a_orig_score, self.run_a_rep_score, rpd=rpd, pbar=print_feedback)}
            else:
                if print_feedback:
                    print('Determining p-values of t-test for baseline run.')
                return {'baseline': ttest(self.run_b_orig_score, self.run_b_rep_score, rpd=rpd, pbar=print_feedback)}
        else:
            print(ERR_MSG)


class RpdEvaluator(Evaluator):
    """
    The Reproducibility Evaluator is used for quantifying the different levels of reproduction for runs that were
    derived from the same test collection used in the original experiment.
    """

    def evaluate(self, run=None, run_path=None):
        """
        Evaluates the scores of the original and reproduced baseline and advanced runs.
        If a (reproduced) run is provided only this one will be evaluated and a dictionary with the corresponding
        scores is returned.
        @param run: A reproduced run. If not specified, the original and reproduced runs of the the RpdEvaluator will
                    be used instead.
        @return: If run is specified, a dictionary with the corresponding scores is returned.
        """
        if run or run_path:
            run = load_run(run_path) if run_path else run
            run = break_ties(run)
            per_topic_results = pd.DataFrame(ir_measures.calc(self.measures, self.qrels_orig, run)[1])
            return  {
                qid: dict(zip(g["measure"].astype(str), g["value"]))
                for qid, g in per_topic_results.groupby("query_id")
            }

        super(RpdEvaluator, self).evaluate()

        if self.run_b_rep:
            self.run_b_rep = break_ties(self.run_b_rep)
            per_topic_results = pd.DataFrame(ir_measures.calc(self.measures, self.qrels_orig, self.run_b_rep)[1])
            self.run_b_rep_score =  {
                qid: dict(zip(g["measure"].astype(str), g["value"]))
                for qid, g in per_topic_results.groupby("query_id")
            }
        if self.run_a_rep:
            self.run_a_rep = break_ties(self.run_a_rep)
            per_topic_results = pd.DataFrame(ir_measures.calc(self.measures, self.qrels_orig, self.run_a_rep)[1])
            self.run_a_rep_score =  {
                qid: dict(zip(g["measure"].astype(str), g["value"]))
                for qid, g in per_topic_results.groupby("query_id")
            }

    def ktu(self, run_b_rep=None, run_a_rep=None, run_b_path=None, run_a_path=None, print_feedback=False, per_topic=False):
        """
        Determines Kendall's tau Union (KTU) between the original and reproduced document orderings,
        see also: https://dl.acm.org/doi/10.1145/3397271.3401036

        @param run_b_rep: Scores of the baseline run,
                          if not provided the scores of the RpdEvaluator object will be used instead.
        @param run_a_rep: Scores of the advanced run,
                          if not provided the scores of the RpdEvaluator object will be used instead.
        @param run_b_path: Path to another reproduced baseline run,
                           if not provided the reproduced baseline run of the RpdEvaluator object will be used instead.
        @param run_a_path: Path to another reproduced advanced run,
                           if not provided the reproduced advanced run of the RpdEvaluator object will be used instead.
        @param print_feedback: Boolean value indicating if feedback on progress should be printed.
        @return: Dictionary with KTU values that compare the document orderings of the original and reproduced runs.
        """
        if self.run_b_orig and run_b_path:
            if self.run_a_orig and run_a_path:
                if print_feedback:
                    print("Determining Kendall's tau Union (KTU) for baseline and advanced run.")
                with open(run_b_path, 'r') as b_run, open(run_a_path, 'r') as a_run:
                    run_b_rep = pytrec_eval.parse_run(b_run)
                    run_b_rep = {t: run_b_rep[t] for t in sorted(run_b_rep)}
                    run_a_rep = pytrec_eval.parse_run(a_run)
                    run_a_rep = {t: run_a_rep[t] for t in sorted(run_a_rep)}
                return {'baseline': ktau_union(self.run_b_orig, run_b_rep, pbar=print_feedback, per_topic=per_topic),
                        'advanced': ktau_union(self.run_a_orig, run_a_rep, pbar=print_feedback, per_topic=per_topic)}
            else:
                if print_feedback:
                    print("Determining Kendall's tau Union (KTU) for baseline run.")
                with open(run_b_path, 'r') as b_run:
                    run_b_rep = pytrec_eval.parse_run(b_run)
                    run_b_rep = {t: run_b_rep[t] for t in sorted(run_b_rep)}
                return {'baseline': ktau_union(self.run_b_orig, run_b_rep, pbar=print_feedback, per_topic=per_topic)}

        if self.run_b_orig and run_b_rep:
            if self.run_a_orig and run_a_rep:
                if print_feedback:
                    print("Determining Kendall's tau Union (KTU) for baseline and advanced run.")
                return {'baseline': ktau_union(self.run_b_orig, run_b_rep, pbar=print_feedback, per_topic=per_topic),
                        'advanced': ktau_union(self.run_a_orig, run_a_rep, pbar=print_feedback, per_topic=per_topic)}
            else:
                if print_feedback:
                    print("Determining Kendall's tau Union (KTU) for baseline run.")
                return {'baseline':  ktau_union(self.run_b_orig, run_b_rep, pbar=print_feedback, per_topic=per_topic)}

        if self.run_b_orig and self.run_b_rep:
            if self.run_a_orig and self.run_a_rep:
                if print_feedback:
                    print("Determining Kendall's tau Union (KTU) for baseline and advanced run.")
                return {'baseline': ktau_union(self.run_b_orig, self.run_b_rep, pbar=print_feedback, per_topic=per_topic),
                        'advanced': ktau_union(self.run_a_orig, self.run_a_rep, pbar=print_feedback, per_topic=per_topic)}
            else:
                if print_feedback:
                    print("Determining Kendall's tau Union (KTU) for baseline run.")
                return {'baseline':  ktau_union(self.run_b_orig, self.run_b_rep, pbar=print_feedback, per_topic=per_topic)}
        else:
            print(ERR_MSG)

    def rbo(self, run_b_rep=None, run_a_rep=None, run_b_path=None, run_a_path=None, print_feedback=False, p=RBO_P, depth=RBO_DEPTH, per_topic=False):
        """
        Determines the Rank-Biased Overlap (RBO) between the original and reproduced document orderings,
        see also: https://dl.acm.org/doi/10.1145/3397271.3401036

        @param run_b_rep: Scores of the baseline run,
                          if not provided the scores of the RpdEvaluator object will be used instead.
        @param run_a_rep: Scores of the advanced run,
                          if not provided the scores of the RpdEvaluator object will be used instead.
        @param run_b_path: Path to another reproduced baseline run,
                           if not provided the reproduced baseline run of the RpdEvaluator object will be used instead.
        @param run_a_path: Path to another reproduced advanced run,
                           if not provided the reproduced advanced run of the RpdEvaluator object will be used instead.
        @param print_feedback: Boolean value indicating if feedback on progress should be printed.
        @param misinfo: Use the RBO implementation that is also used in the TREC Health Misinformation Track.
                        See also: https://github.com/claclark/Compatibility
        @return: Dictionary with RBO values that compare the document orderings of the original and reproduced runs.
        """
        if self.run_b_orig and run_b_path:
            if self.run_a_orig and run_a_path:
                if print_feedback:
                    print("Determining Rank-biased Overlap (RBO) for baseline and advanced run.")
                with open(run_b_path, 'r') as b_run, open(run_a_path, 'r') as a_run:
                    run_b_rep = pytrec_eval.parse_run(b_run)
                    run_b_rep = {t: run_b_rep[t] for t in sorted(run_b_rep)}
                    run_a_rep = pytrec_eval.parse_run(a_run)
                    run_a_rep = {t: run_a_rep[t] for t in sorted(run_a_rep)}
                return {'baseline': RBO(self.run_b_orig, run_b_rep, pbar=print_feedback, p=p, depth=depth, per_topic=per_topic),
                        'advanced': RBO(self.run_a_orig, run_a_rep, pbar=print_feedback, p=p, depth=depth, per_topic=per_topic)}
            else:
                if print_feedback:
                    print("Determining Rank-biased Overlap (RBO) for baseline run.")
                with open(run_b_path, 'r') as b_run:
                    run_b_rep = pytrec_eval.parse_run(b_run)
                    run_b_rep = {t: run_b_rep[t] for t in sorted(run_b_rep)}
                return {'baseline': RBO(self.run_b_orig, run_b_rep, pbar=print_feedback, p=p, depth=depth, per_topic=per_topic)}

        if self.run_b_orig and run_b_rep:
            if self.run_a_orig and run_a_rep:
                if print_feedback:
                    print("Determining Rank-biased Overlap (RBO) for baseline and advanced run.")
                return {'baseline': RBO(self.run_b_orig, run_b_rep, pbar=print_feedback, p=p, depth=depth, per_topic=per_topic),
                        'advanced': RBO(self.run_a_orig, run_a_rep, pbar=print_feedback, p=p, depth=depth, per_topic=per_topic)}
            else:
                if print_feedback:
                    print("Determining Rank-biased Overlap (RBO) for baseline run.")
                return {'baseline':  RBO(self.run_b_orig, run_b_rep, pbar=print_feedback, p=p, depth=depth, per_topic=per_topic)}
        if self.run_b_orig and self.run_b_rep:
            if self.run_a_orig and self.run_a_rep:
                if print_feedback:
                    print("Determining Rank-biased Overlap (RBO) for baseline and advanced run.")
                return {'baseline': RBO(self.run_b_orig, self.run_b_rep, pbar=print_feedback, p=p, depth=depth, per_topic=per_topic),
                        'advanced': RBO(self.run_a_orig, self.run_a_rep, pbar=print_feedback, p=p, depth=depth, per_topic=per_topic)}
            else:
                if print_feedback:
                    print("Determining Rank-biased Overlap (RBO) for baseline run.")
                return {'baseline':  RBO(self.run_b_orig, self.run_b_rep, pbar=print_feedback, p=p, depth=depth, per_topic=per_topic)}
        else:
            print(ERR_MSG)

    def rmse(self, run_b_score=None, run_a_score=None, run_b_path=None, run_a_path=None, print_feedback=False):
        """
        Determines the Root Mean Square Error (RMSE), see also: https://dl.acm.org/doi/10.1145/3397271.3401036

        @param run_b_score: Scores of the baseline run,
                            if not provided the scores of the RpdEvaluator object will be used instead.
        @param run_a_score: Scores of the advanced run,
                            if not provided the scores of the RpdEvaluator object will be used instead.
        @param run_b_path: Path to another reproduced baseline run,
                           if not provided the reproduced baseline run of the RpdEvaluator object will be used instead.
        @param run_a_path: Path to another reproduced advanced run,
                           if not provided the reproduced advanced run of the RpdEvaluator object will be used instead.
        @param print_feedback: Boolean value indicating if feedback on progress should be printed.
        @return: Dictionary with RMSE values that measure the closeness
                 between the topics scores of the original and reproduced runs.
        """
        if self.run_b_orig and run_b_path:
            if self.run_a_orig and run_a_path:
                if print_feedback:
                    print("Determining Root Mean Square Error (RMSE) for baseline and advanced run.")
                with open(run_b_path, 'r') as b_run, open(run_a_path, 'r') as a_run:
                    run_b_rep = pytrec_eval.parse_run(b_run)
                    run_b_rep = {t: run_b_rep[t] for t in sorted(run_b_rep)}
                    run_b_rep_score = self.rel_eval.evaluate(run_b_rep)
                    run_a_rep = pytrec_eval.parse_run(a_run)
                    run_a_rep = {t: run_a_rep[t] for t in sorted(run_a_rep)}
                    run_a_rep_score = self.rel_eval.evaluate(run_a_rep)
                return {'baseline': RMSE(self.run_b_orig_score, run_b_rep_score, pbar=print_feedback),
                        'advanced': RMSE(self.run_a_orig_score, run_a_rep_score, pbar=print_feedback)}
            else:
                if print_feedback:
                    print("Determining Root Mean Square Error (RMSE) for baseline run.")
                with open(run_b_path, 'r') as b_run:
                    run_b_rep = pytrec_eval.parse_run(b_run)
                    run_b_rep = {t: run_b_rep[t] for t in sorted(run_b_rep)}
                    run_b_rep_score = self.rel_eval.evaluate(run_b_rep)
                return {'baseline': RMSE(self.run_b_orig_score, run_b_rep_score, pbar=print_feedback)}

        if self.run_b_orig_score and run_b_score:
            if self.run_a_orig_score and run_a_score:
                if print_feedback:
                    print("Determining Root Mean Square Error (RMSE) for baseline and advanced run.")
                return {'baseline': RMSE(self.run_b_orig_score, run_b_score, pbar=print_feedback),
                        'advanced': RMSE(self.run_a_orig_score, run_a_score, pbar=print_feedback)}
            else:
                if print_feedback:
                    print("Determining Root Mean Square Error (RMSE) for baseline run.")
                return {'baseline': RMSE(self.run_b_orig_score, run_b_score, pbar=print_feedback)}
        if self.run_b_orig_score and self.run_b_rep_score:
            if self.run_a_orig_score and self.run_a_rep_score:
                if print_feedback:
                    print("Determining Root Mean Square Error (RMSE) for baseline and advanced run.")
                return {'baseline': RMSE(self.run_b_orig_score, self.run_b_rep_score, pbar=print_feedback),
                        'advanced': RMSE(self.run_a_orig_score, self.run_a_rep_score, pbar=print_feedback)}
            else:
                if print_feedback:
                    print("Determining Root Mean Square Error (RMSE) for baseline run.")
                return {'baseline': RMSE(self.run_b_orig_score, self.run_b_rep_score, pbar=print_feedback)}
        else:
            print(ERR_MSG)

    def nrmse(self, run_b_score=None, run_a_score=None, run_b_path=None, run_a_path=None, print_feedback=False):
        """
        Determines the normalized Root Mean Square Error (RMSE).

        @param run_b_score: Scores of the baseline run,
                            if not provided the scores of the RpdEvaluator object will be used instead.
        @param run_a_score: Scores of the advanced run,
                            if not provided the scores of the RpdEvaluator object will be used instead.
        @param run_b_path: Path to another reproduced baseline run,
                           if not provided the reproduced baseline run of the RpdEvaluator object will be used instead.
        @param run_a_path: Path to another reproduced advanced run,
                           if not provided the reproduced advanced run of the RpdEvaluator object will be used instead.
        @param print_feedback: Boolean value indicating if feedback on progress should be printed.
        @return: Dictionary with nRMSE values that measure the closeness
                 between the topics scores of the original and reproduced runs.
        """
        if self.run_b_orig and run_b_path:
            if self.run_a_orig and run_a_path:
                if print_feedback:
                    print("Determining normalized Root Mean Square Error (RMSE) for baseline and advanced run.")
                with open(run_b_path, 'r') as b_run, open(run_a_path, 'r') as a_run:
                    run_b_rep = pytrec_eval.parse_run(b_run)
                    run_b_rep = {t: run_b_rep[t] for t in sorted(run_b_rep)}
                    run_b_rep_score = self.rel_eval.evaluate(run_b_rep)
                    run_a_rep = pytrec_eval.parse_run(a_run)
                    run_a_rep = {t: run_a_rep[t] for t in sorted(run_a_rep)}
                    run_a_rep_score = self.rel_eval.evaluate(run_a_rep)
                return {'baseline': nRMSE(self.run_b_orig_score, run_b_rep_score, pbar=print_feedback),
                        'advanced': nRMSE(self.run_a_orig_score, run_a_rep_score, pbar=print_feedback)}
            else:
                if print_feedback:
                    print("Determining normalized Root Mean Square Error (RMSE) for baseline run.")
                with open(run_b_path, 'r') as b_run:
                    run_b_rep = pytrec_eval.parse_run(b_run)
                    run_b_rep = {t: run_b_rep[t] for t in sorted(run_b_rep)}
                    run_b_rep_score = self.rel_eval.evaluate(run_b_rep)
                return {'baseline': nRMSE(self.run_b_orig_score, run_b_rep_score, pbar=print_feedback)}

        if self.run_b_orig_score and run_b_score:
            if self.run_a_orig_score and run_a_score:
                if print_feedback:
                    print("Determining normalized Root Mean Square Error (RMSE) for baseline and advanced run.")
                return {'baseline': nRMSE(self.run_b_orig_score, run_b_score, pbar=print_feedback),
                        'advanced': nRMSE(self.run_a_orig_score, run_a_score, pbar=print_feedback)}
            else:
                if print_feedback:
                    print("Determining normalized Root Mean Square Error (RMSE) for baseline run.")
                return {'baseline': nRMSE(self.run_b_orig_score, run_b_score, pbar=print_feedback)}
        if self.run_b_orig_score and self.run_b_rep_score:
            if self.run_a_orig_score and self.run_a_rep_score:
                if print_feedback:
                    print("Determining Root Mean Square Error (RMSE) for baseline and advanced run.")
                return {'baseline': nRMSE(self.run_b_orig_score, self.run_b_rep_score, pbar=print_feedback),
                        'advanced': nRMSE(self.run_a_orig_score, self.run_a_rep_score, pbar=print_feedback)}
            else:
                if print_feedback:
                    print("Determining normalized Root Mean Square Error (RMSE) for baseline run.")
                return {'baseline': nRMSE(self.run_b_orig_score, self.run_b_rep_score, pbar=print_feedback)}
        else:
            print(ERR_MSG)

    def ttest(self, run_b_score=None, run_a_score=None, run_b_path=None, run_a_path=None, print_feedback=False):
        """
        Conducts a paired two-tailed t-test for reproduced runs that were derived from the same test collection
        as in the original experiment.

        @param run_b_score: Scores of the baseline run,
                            if not provided the scores of the RpdEvaluator object will be used instead.
        @param run_a_score: Scores of the advanced run,
                            if not provided the scores of the RpdEvaluator object will be used instead.
        @param run_b_path: Path to another reproduced baseline run,
                           if not provided the reproduced baseline run of the RpdEvaluator object will be used instead.
        @param run_a_path: Path to another reproduced advanced run,
                           if not provided the reproduced advanced run of the RpdEvaluator object will be used instead.
        @param print_feedback: Boolean value indicating if feedback on progress should be printed.
        @return: Dictionary with p-values that compare the score distributions of the baseline and advanced run.
        """
        if run_b_path:
            if run_a_path:
                with open(run_b_path, 'r') as b_run, open(run_a_path, 'r') as a_run:
                    run_b_rep = pytrec_eval.parse_run(b_run)
                    run_b_rep = {t: run_b_rep[t] for t in sorted(run_b_rep)}
                    run_b_rep_score = self.rel_eval.evaluate(run_b_rep)
                    run_a_rep = pytrec_eval.parse_run(a_run)
                    run_a_rep = {t: run_a_rep[t] for t in sorted(run_a_rep)}
                    run_a_rep_score = self.rel_eval.evaluate(run_a_rep)
                return self._ttest(run_b_score=run_b_rep_score, run_a_score=run_a_rep_score, print_feedback=print_feedback)
            else:
                with open(run_b_path, 'r') as b_run:
                    run_b_rep = pytrec_eval.parse_run(b_run)
                    run_b_rep = {t: run_b_rep[t] for t in sorted(run_b_rep)}
                    run_b_rep_score = self.rel_eval.evaluate(run_b_rep)
                return self._ttest(run_b_score=run_b_rep_score, run_a_score=None, print_feedback=print_feedback)

        return self._ttest(run_b_score=run_b_score, run_a_score=run_a_score, print_feedback=print_feedback)


class RplEvaluator(Evaluator):
    """
    The Replicability Evaluator is used for quantifying the different levels of replication for runs that were
    derived from a test collection not used in the original experiment.
    """
    def __init__(self, **kwargs):
        super(RplEvaluator, self).__init__(**kwargs)
        self.qrels_rpl_path = kwargs.get('qrels_rpl_path', None)
        if self.qrels_rpl_path:
            self.qrels_rpl = load_qrels(self.qrels_rpl_path)

    def evaluate(self, run=None, run_path=None, rpl=True):
        """
        Evaluates the scores of the original and replicated baseline and advanced runs.
        If a (replicated) run is provided only this one will be evaluated and a dictionary with the corresponding
        scores is returned.
        @param run: A replicated run. If not specified, the original and replicated runs of the the RplEvaluator will
                    be used instead.
        @return: If run is specified, a dictionary with the corresponding scores is returned.
        """
        if run or run_path:
            run = load_run(run_path) if run_path else run
            run = break_ties(run)
            if rpl:
                per_topic_results = pd.DataFrame(ir_measures.calc(self.measures, self.qrels_rpl, run)[1])
            else:
                per_topic_results = pd.DataFrame(ir_measures.calc(self.measures, self.qrels_orig, run)[1])
            return  {
                qid: dict(zip(g["measure"].astype(str), g["value"]))
                for qid, g in per_topic_results.groupby("query_id")
            }

        super(RplEvaluator, self).evaluate()

        if self.run_b_rep:
            self.run_b_rep = break_ties(self.run_b_rep)
            per_topic_results = pd.DataFrame(ir_measures.calc(self.measures, self.qrels_rpl, self.run_b_rep)[1])
            self.run_b_rep_score =  {
                qid: dict(zip(g["measure"].astype(str), g["value"]))
                for qid, g in per_topic_results.groupby("query_id")
            }
        if self.run_a_rep:
            self.run_a_rep = break_ties(self.run_a_rep)
            per_topic_results = pd.DataFrame(ir_measures.calc(self.measures, self.qrels_rpl, self.run_a_rep)[1])
            self.run_a_rep_score =  {
                qid: dict(zip(g["measure"].astype(str), g["value"]))
                for qid, g in per_topic_results.groupby("query_id")
            }


    def ttest(self, run_b_score=None, run_a_score=None, run_b_path=None, run_a_path=None, print_feedback=False):
        """
        Conducts an un-paired two-tailed t-test for replicated runs that were derived from a test collection
        not used in the original experiment.

        @param run_b_score: Scores of the baseline run,
                            if not provided the scores of the RpdEvaluator object will be used instead.
        @param run_a_score: Scores of the advanced run,
                            if not provided the scores of the RpdEvaluator object will be used instead.
        @param run_b_path: Path to another replicated baseline run,
                           if not provided the replicated baseline run of the RplEvaluator object will be used instead.
        @param run_a_path: Path to another replicated advanced run,
                           if not provided the replicated advanced run of the RplEvaluator object will be used instead.
        @param print_feedback: Boolean value indicating if feedback on progress should be printed.
        @return: Dictionary with p-values that compare the score distributions of the baseline and advanced run.
        """
        if run_b_path:
            if run_a_path:
                with open(run_b_path, 'r') as b_run, open(run_a_path, 'r') as a_run:
                    run_b_rep = pytrec_eval.parse_run(b_run)
                    run_b_rep = {t: run_b_rep[t] for t in sorted(run_b_rep)}
                    run_b_rep_score = self.rel_eval_rpl.evaluate(run_b_rep)
                    run_a_rep = pytrec_eval.parse_run(a_run)
                    run_a_rep = {t: run_a_rep[t] for t in sorted(run_a_rep)}
                    run_a_rep_score = self.rel_eval_rpl.evaluate(run_a_rep)
                return self._ttest(rpd=False, run_b_score=run_b_rep_score, run_a_score=run_a_rep_score, print_feedback=print_feedback)
            else:
                with open(run_b_path, 'r') as b_run:
                    run_b_rep = pytrec_eval.parse_run(b_run)
                    run_b_rep = {t: run_b_rep[t] for t in sorted(run_b_rep)}
                    run_b_rep_score = self.rel_eval_rpl.evaluate(run_b_rep)
                return self._ttest(rpd=False, run_b_score=run_b_rep_score, run_a_score=None, print_feedback=print_feedback)

        return self._ttest(rpd=False, run_b_score=run_b_score, run_a_score=run_a_score, print_feedback=print_feedback)
