from repro_eval.Evaluator import RplEvaluator
from repro_eval.measure import arp
from repro_eval.util import print_base_adv, print_simple_line

QREL = './data/qrels/core17.txt'
ORIG_B = './data/runs/orig/input.WCrobust04'
ORIG_A = './data/runs/orig/input.WCrobust0405'
RPL_B = './data/runs/rpl/14/irc_task1_WCrobust04_001'
RPL_A = './data/runs/rpl/14/irc_task1_WCrobust0405_001'
MEASURE = 'ndcg'


def main():
    rpl_eval = RplEvaluator(qrel_orig_path=QREL,
                            run_b_orig_path=ORIG_B,
                            run_a_orig_path=ORIG_A,
                            run_b_rep_path=RPL_B,
                            run_a_rep_path=RPL_A)

    rpl_eval.trim()
    rpl_eval.evaluate()

    # KTU
    ktau = rpl_eval.ktau_union()
    print("Kendall's tau Union (KTU)")
    print('------------------------------------------------------------------')
    for topic, value in ktau.get('baseline').items():
        print_base_adv(topic, 'KTU', value, ktau.get('advanced').get(topic))
    print_base_adv('ARP', 'KTU', arp(ktau.get('baseline')), arp(ktau.get('advanced')))

    # RBO
    rbo = rpl_eval.rbo()
    print("Rank-biased Overlap (RBO)")
    print('------------------------------------------------------------------')
    for topic, value in rbo.get('baseline').items():
        print_base_adv(topic, 'RBO', value, rbo.get('advanced').get(topic))
    print_base_adv('ARP', 'RBO', arp(rbo.get('baseline')), arp(rbo.get('advanced')))

    # RMSE
    rmse = rpl_eval.rmse()
    print("Root mean square error (RMSE)")
    print('------------------------------------------------------------------')
    for measure, value in rmse.get('baseline').items():
        print_base_adv(measure, 'RMSE', value, rmse.get('advanced').get(measure))

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
    print("Two-tailed paired t-test (p-value)")
    print('------------------------------------------------------------------')
    for measure, value in pvals.get('baseline').items():
        print_base_adv(measure, 'PVAL', value, pvals.get('advanced').get(measure))


if __name__ == "__main__":
    main()
