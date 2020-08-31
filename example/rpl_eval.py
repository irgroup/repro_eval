from repro_eval.Evaluator import RplEvaluator
from repro_eval.util import print_base_adv, print_simple_line

QREL = './data/qrels/core17.txt'
QREL_RPL = './data/qrels/core18.txt'
ORIG_B = './data/runs/orig/input.WCrobust04'
ORIG_A = './data/runs/orig/input.WCrobust0405'
RPL_B = './data/runs/rpl/14/irc_task2_WCrobust04_001'
RPL_A = './data/runs/rpl/14/irc_task2_WCrobust0405_001'
MEASURE = 'ndcg'


def main():
    rpl_eval = RplEvaluator(qrel_orig_path=QREL,
                            run_b_orig_path=ORIG_B,
                            run_a_orig_path=ORIG_A,
                            run_b_rep_path=RPL_B,
                            run_a_rep_path=RPL_A,
                            qrel_rpd_path=QREL_RPL)

    rpl_eval.trim()
    rpl_eval.evaluate()

    # ER
    print("Effect ratio (ER)")
    print('------------------------------------------------------------------')
    er = rpl_eval.er()
    for measure, value in er.items():
        print_simple_line(measure, 'ER', value)

    # DRI
    print("Delta Relative Improvement (DRI)")
    print('------------------------------------------------------------------')
    dri = rpl_eval.dri()
    for measure, value in dri.items():
        print_simple_line(measure, 'DRI', value)

    # ttest
    pvals = rpl_eval.ttest()
    print("Two-tailed unpaired t-test (p-value)")
    print('------------------------------------------------------------------')
    for measure, value in pvals.get('baseline').items():
        print_base_adv(measure, 'PVAL', value, pvals.get('advanced').get(measure))


if __name__ == "__main__":
    main()
