from repro_eval.Evaluator import RplEvaluator
from repro_eval.measure.util import arp
from repro_eval.util import print_base_adv, print_simple_line

import pytrec_eval

QREL = './data/qrels/core17.txt'
ORIG_B = './data/runs/orig/input.WCrobust04'
ORIG_A = './data/runs/orig/input.WCrobust0405'
RPL_B = './data/runs/rpl/14/irc_task1_WCrobust04_001'
RPL_A = './data/runs/rpl/14/irc_task1_WCrobust0405_001'
MEASURE = 'ndcg'


def main():

    rpl_eval = RplEvaluator(qrel_orig_path=QREL,
                            run_b_orig_path=ORIG_B,
                            run_b_rep_path=RPL_B)

    rpl_eval.trim()
    rpl_eval.evaluate()
    rpl_eval.er()

    # rpl_eval = RplEvaluator(qrel_orig_path=QREL,
    #                         run_b_orig_path=ORIG_B,
    #                         run_a_orig_path=ORIG_A,
    #                         run_b_rep_path=RPL_B,
    #                         run_a_rep_path=RPL_A)
    #
    # rpl_eval.trim()
    # rpl_eval.evaluate()
    #
    # with open('../data/runs/rpl/15/irc_task1_WCrobust04_001') as f_run:
    #     another_run = pytrec_eval.parse_run(f_run)
    #
    # rpl_eval.trim(run=another_run)
    # scores = rpl_eval.evaluate(run=another_run)
    #
    # rmse_scores = rpl_eval.rmse(run_b_score=scores)
    #
    # print(rmse_scores)
    # pass


if __name__ == "__main__":
    main()
