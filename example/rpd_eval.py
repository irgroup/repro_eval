from repro_eval.Evaluator import RpdEvaluator
from repro_eval.util import print_base_adv, print_simple_line

QREL = './data/qrels/core17.txt'
QREL_RPD = './data/qrels/core18.txt'
ORIG_B = './data/runs/orig/input.WCrobust04'
ORIG_A = './data/runs/orig/input.WCrobust0405'
RPD_B = './data/runs/rpd/14/irc_task2_WCrobust04_001'
RPD_A = './data/runs/rpd/14/irc_task2_WCrobust0405_001'
MEASURE = 'ndcg'


def main():
    rpd_eval = RpdEvaluator(qrel_orig_path=QREL,
                            run_b_orig_path=ORIG_B,
                            run_a_orig_path=ORIG_A,
                            run_b_rep_path=RPD_B,
                            run_a_rep_path=RPD_A,
                            qrel_rpd_path=QREL_RPD)

    rpd_eval.trim()
    rpd_eval.evaluate()

    # ER
    print("Effect ratio (ER)")
    print('------------------------------------------------------------------')
    er = rpd_eval.er()
    for measure, value in er.items():
        print_simple_line(measure, 'ER', value)

    # DRI
    print("Delta Relative Improvement (DRI)")
    print('------------------------------------------------------------------')
    dri = rpd_eval.dri()
    for measure, value in dri.items():
        print_simple_line(measure, 'DRI', value)

    # ttest
    pvals = rpd_eval.ttest()
    print("Two-tailed unpaired t-test (p-value)")
    print('------------------------------------------------------------------')
    for measure, value in pvals.get('baseline').items():
        print_base_adv(measure, 'PVAL', value, pvals.get('advanced').get(measure))


if __name__ == "__main__":
    main()
