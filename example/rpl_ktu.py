from repro_eval.Evaluator import RplEvaluator
from repro_eval.util import print_base_adv, print_simple_line, trim, arp
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="darkgrid")
import pandas as pd
import matplotlib.pyplot as plt
import pytrec_eval

QREL = './data/qrels/core17.txt'
ORIG_B = './data/runs/orig/input.WCrobust04'
ORIG_A = './data/runs/orig/input.WCrobust0405'
RPL_B = './data/runs/rpl/14/irc_task1_WCrobust04_001'
RPL_A = './data/runs/rpl/14/irc_task1_WCrobust0405_001'
MEASURE = 'ndcg'


runs_rpl = {
    'rpl_wcr04_tf_1':
        {'path': './data/runs/rpl/45/irc_task1_WCrobust04_001'},
    'rpl_wcr0405_tf_1':
        {'path': './data/runs/rpl/45/irc_task1_WCrobust0405_001'},
    'rpl_wcr04_tf_2':
        {'path': './data/runs/rpl/46/irc_task1_WCrobust04_001'},
    'rpl_wcr0405_tf_2':
        {'path': './data/runs/rpl/46/irc_task1_WCrobust0405_001'},
    'rpl_wcr04_tf_3':
        {'path': './data/runs/rpl/47/irc_task1_WCrobust04_001'},
    'rpl_wcr0405_tf_3':
        {'path': './data/runs/rpl/47/irc_task1_WCrobust0405_001'},
    'rpl_wcr04_tf_4':
        {'path': './data/runs/rpl/48/irc_task1_WCrobust04_001'},
    'rpl_wcr0405_tf_4':
        {'path': './data/runs/rpl/48/irc_task1_WCrobust0405_001'},
    'rpl_wcr04_tf_5':
        {'path': './data/runs/rpl/49/irc_task1_WCrobust04_001'},
    'rpl_wcr0405_tf_5':
        {'path': './data/runs/rpl/49/irc_task1_WCrobust0405_001'}
}


def main():
    cutoffs = [1000, 100, 50, 20, 10, 5]

    # BASELINE
    for run_name, info in zip(list(runs_rpl.keys())[::2], list(runs_rpl.values())[::2]):
        rpl_eval = RplEvaluator(qrel_orig_path=QREL,
                                run_b_orig_path=ORIG_B,
                                run_a_orig_path=ORIG_A,
                                run_b_rep_path=None,
                                run_a_rep_path=None)

        rpl_eval.trim()
        rpl_eval.evaluate()

        with open(info.get('path')) as run_file:
            info['run'] = pytrec_eval.parse_run(run_file)
            for cutoff in cutoffs:
                rpl_eval.trim(cutoff)
                rpl_eval.trim(cutoff, info['run'])
                info['ktu_' + str(cutoff)] = arp(rpl_eval.ktau_union(info['run'])['baseline'])

    df_content = {}
    for run_name, info in zip(list(runs_rpl.keys())[::2], list(runs_rpl.values())[::2]):
        df_content[run_name] = [info.get('ktu_' + str(cutoff)) for cutoff in cutoffs[::-1]]

    ax = pd.DataFrame(data=df_content, index=[str(cutoff) for cutoff in cutoffs[::-1]]).plot(style='-*')
    ax.set_xlabel('Cut-off values')
    ax.set_ylabel(r"Kendall's $\tau$")
    ax.get_figure().savefig('data/plots/rpl_b_ktu.pdf', format='pdf', bbox_inches='tight')
    plt.show()

    # ADVANCED
    for run_name, info in zip(list(runs_rpl.keys())[1::2], list(runs_rpl.values())[1::2]):
        rpl_eval = RplEvaluator(qrel_orig_path=QREL,
                                run_b_orig_path=ORIG_B,
                                run_a_orig_path=ORIG_A,
                                run_b_rep_path=None,
                                run_a_rep_path=None)

        rpl_eval.trim()
        rpl_eval.evaluate()

        with open(info.get('path')) as run_file:
            info['run'] = pytrec_eval.parse_run(run_file)
            for cutoff in cutoffs:
                rpl_eval.trim(cutoff)
                rpl_eval.trim(cutoff, info['run'])
                # scores = rpl_eval.evaluate(info['run'])
                info['ktu_' + str(cutoff)] = arp(rpl_eval.ktau_union(info['run'])['baseline'])

    df_content = {}
    for run_name, info in zip(list(runs_rpl.keys())[1::2], list(runs_rpl.values())[1::2]):
        df_content[run_name] = [info.get('ktu_' + str(cutoff)) for cutoff in cutoffs[::-1]]

    ax = pd.DataFrame(data=df_content, index=[str(cutoff) for cutoff in cutoffs[::-1]]).plot(style='-*')
    ax.set_xlabel('Cut-off values')
    ax.set_ylabel(r"Kendall's $\tau$")
    ax.get_figure().savefig('data/plots/rpl_a_ktu.pdf', format='pdf', bbox_inches='tight')
    plt.show()


if __name__ == "__main__":
    main()
