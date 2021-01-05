"""
Use repro_eval from the command line with e.g.

python -m repro_eval -t rpd -q qrel_orig -r orig_b rpd_b

python -m repro_eval -t rpd -q qrel_orig -r orig_b orig_a rpd_b rpd_a

python -m repro_eval -t rpd -m rmse -q qrel_orig -r orig_b rpd_b

python -m repro_eval -t rpl -q qrel_orig qrel_rpl -r orig_b rpl_b

python -m repro_eval -t rpl -q qrel_orig qrel_rpl -r orig_b orig_a rpl_b rpl_a

after having installed the Python package.
For other more specific examples also have a look at the README file.
Depending on the provided parameters and input run files,
evaluation measures will be printed.
"""

import argparse
from repro_eval.Evaluator import RpdEvaluator, RplEvaluator
from repro_eval.util import print_simple_line, print_base_adv
from repro_eval.util import arp


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-t', '--type')
    parser.add_argument('-m', '--measure', nargs='+')
    parser.add_argument('-q', '--qrels', nargs='+')
    parser.add_argument('-r', '--runs', nargs='+')

    args = parser.parse_args()

    if args.type in ['rpd', 'reproducibility']:
        if len(args.runs) == 4:
            rpd_eval = RpdEvaluator(qrel_orig_path=args.qrels[0],
                                    run_b_orig_path=args.runs[0],
                                    run_a_orig_path=args.runs[1],
                                    run_b_rep_path=args.runs[2],
                                    run_a_rep_path=args.runs[3])

        if len(args.runs) == 2:
            rpd_eval = RpdEvaluator(qrel_orig_path=args.qrels[0],
                                    run_b_orig_path=args.runs[0],
                                    run_a_orig_path=None,
                                    run_b_rep_path=args.runs[1],
                                    run_a_rep_path=None)

        rpd_eval.trim()
        rpd_eval.evaluate()

        measure_list = args.measure if args.measure is not None else []

        # KTU
        if 'ktu' in measure_list or args.measure is None:
            ktu = rpd_eval.ktau_union()
            print("Kendall's tau Union (KTU)")
            print('------------------------------------------------------------------')
            for topic, value in ktu.get('baseline').items():
                value_adv = ktu.get('advanced').get(topic) if ktu.get('advanced') is not None else None
                print_base_adv(topic, 'KTU', value, value_adv)
            value_adv = arp(ktu.get('advanced')) if ktu.get('advanced') is not None else None
            print_base_adv('ARP', 'KTU', arp(ktu.get('baseline')), value_adv)
            print()

        # RBO
        if 'rbo' in measure_list or args.measure is None:
            rbo = rpd_eval.rbo()
            print("Rank-biased Overlap (RBO)")
            print('------------------------------------------------------------------')
            for topic, value in rbo.get('baseline').items():
                value_adv = rbo.get('advanced').get(topic) if rbo.get('advanced') is not None else None
                print_base_adv(topic, 'RBO', value, value_adv)
            value_adv = arp(rbo.get('advanced')) if rbo.get('advanced') is not None else None
            print_base_adv('ARP', 'RBO', arp(rbo.get('baseline')), value_adv)
            print()

        # RMSE
        if 'rmse' in measure_list or args.measure is None:
            rmse = rpd_eval.rmse()
            print("Root mean square error (RMSE)")
            print('------------------------------------------------------------------')
            for measure, value in rmse.get('baseline').items():
                value_adv = rmse.get('advanced').get(measure) if rmse.get('advanced') is not None else None
                print_base_adv(measure, 'RMSE', value, value_adv)
            print()

        # ER
        if 'er' in measure_list or args.measure is None and len(args.runs) == 4:
            print("Effect ratio (ER)")
            print('------------------------------------------------------------------')
            er = rpd_eval.er()
            for measure, value in er.items():
                print_simple_line(measure, 'ER', value)
            print()

        # DRI
        if 'dri' in measure_list or args.measure is None and len(args.runs) == 4:
            print("Delta Relative Improvement (DRI)")
            print('------------------------------------------------------------------')
            dri = rpd_eval.dri()
            for measure, value in dri.items():
                print_simple_line(measure, 'DRI', value)
            print()

        # ttest
        if 'ttest' in measure_list or args.measure is None:
            pvals = rpd_eval.ttest()
            print("Two-tailed paired t-test (p-value)")
            print('------------------------------------------------------------------')
            for measure, value in pvals.get('baseline').items():
                value_adv = pvals.get('advanced').get(measure) if pvals.get('advanced') is not None else None
                print_base_adv(measure, 'PVAL', value, value_adv)
            print()

    if args.type in ['rpl', 'replicability']:
        if len(args.runs) == 4:
            rpl_eval = RplEvaluator(qrel_orig_path=args.qrels[0],
                                    run_b_orig_path=args.runs[0],
                                    run_a_orig_path=args.runs[1],
                                    run_b_rep_path=args.runs[2],
                                    run_a_rep_path=args.runs[3],
                                    qrel_rpl_path=args.qrels[1])

        if len(args.runs) == 2:
            rpl_eval = RplEvaluator(qrel_orig_path=args.qrels[0],
                                    run_b_orig_path=args.runs[0],
                                    run_a_orig_path=None,
                                    run_b_rep_path=args.runs[1],
                                    run_a_rep_path=None,
                                    qrel_rpl_path=args.qrels[1])

        rpl_eval.trim()
        rpl_eval.evaluate()

        measure_list = args.measure if args.measure is not None else []

        # ER
        if 'er' in measure_list or args.measure is None and len(args.runs) == 4:
            print("Effect ratio (ER)")
            print('------------------------------------------------------------------')
            er = rpl_eval.er()
            for measure, value in er.items():
                print_simple_line(measure, 'ER', value)
            print()

        # DRI
        if 'dri' in measure_list or args.measure is None and len(args.runs) == 4:
            print("Delta Relative Improvement (DRI)")
            print('------------------------------------------------------------------')
            dri = rpl_eval.dri()
            for measure, value in dri.items():
                print_simple_line(measure, 'DRI', value)
            print()

        # ttest
        if 'ttest' in measure_list or args.measure is None:
            pvals = rpl_eval.ttest()
            print("Two-tailed unpaired t-test (p-value)")
            print('------------------------------------------------------------------')
            for measure, value in pvals.get('baseline').items():
                value_adv = pvals.get('advanced').get(measure) if pvals.get('advanced') is not None else None
                print_base_adv(measure, 'PVAL', value, value_adv)
            print()


if __name__ == "__main__":
    main()
