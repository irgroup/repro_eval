import pytrec_eval
from repro_eval.Evaluator import RplEvaluator
from repro_eval.util import trim
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
sns.set()
sns.set_style('whitegrid')
palette = sns.color_palette("GnBu_d")
sns.set_palette(palette)
colors = sns.color_palette()

ORIG_B = './data/runs/orig/input.WCrobust04'
ORIG_A = './data/runs/orig/input.WCrobust0405'
QREL = 'data/qrels/core17.txt'
QREL_RPL = 'data/qrels/core18.txt'

runs_rpl = {
    'rpl_wcr04_tf_1':
        {'path': './data/runs/rpl/45/irc_task2_WCrobust04_001'},
    'rpl_wcr0405_tf_1':
        {'path': './data/runs/rpl/45/irc_task2_WCrobust0405_001'},
    'rpl_wcr04_tf_2':
        {'path': './data/runs/rpl/46/irc_task2_WCrobust04_001'},
    'rpl_wcr0405_tf_2':
        {'path': './data/runs/rpl/46/irc_task2_WCrobust0405_001'},
    'rpl_wcr04_tf_3':
        {'path': './data/runs/rpl/47/irc_task2_WCrobust04_001'},
    'rpl_wcr0405_tf_3':
        {'path': './data/runs/rpl/47/irc_task2_WCrobust0405_001'},
    'rpl_wcr04_tf_4':
        {'path': './data/runs/rpl/48/irc_task2_WCrobust04_001'},
    'rpl_wcr0405_tf_4':
        {'path': './data/runs/rpl/48/irc_task2_WCrobust0405_001'},
    'rpl_wcr04_tf_5':
        {'path': './data/runs/rpl/49/irc_task2_WCrobust04_001'},
    'rpl_wcr0405_tf_5':
        {'path': './data/runs/rpl/49/irc_task2_WCrobust0405_001'}
}


def main():
    rpl_eval = RplEvaluator(qrel_orig_path=QREL,
                            run_b_orig_path=ORIG_B,
                            run_a_orig_path=ORIG_A,
                            run_b_rep_path=None,
                            run_a_rep_path=None,
                            qrel_rpd_path=QREL_RPL)

    rpl_eval.trim()
    rpl_eval.evaluate()

    for run_name, info in runs_rpl.items():
        with open(info.get('path')) as run_file:
            info['run'] = pytrec_eval.parse_run(run_file)
            trim(info['run'])
            info['scores'] = rpl_eval.evaluate(info['run'])

    pairs = [('rpl_wcr04_tf_1', 'rpl_wcr0405_tf_1'),
             ('rpl_wcr04_tf_2', 'rpl_wcr0405_tf_2'),
             ('rpl_wcr04_tf_3', 'rpl_wcr0405_tf_3'),
             ('rpl_wcr04_tf_4', 'rpl_wcr0405_tf_4'),
             ('rpl_wcr04_tf_5', 'rpl_wcr0405_tf_5')]

    df_content = {
        'P_10': [rpl_eval.er(run_b_score=runs_rpl[pair[0]]['scores'], run_a_score=runs_rpl[pair[1]]['scores'])['P_10'] for pair in pairs],
        'ndcg': [rpl_eval.er(run_b_score=runs_rpl[pair[0]]['scores'], run_a_score=runs_rpl[pair[1]]['scores'])['ndcg'] for pair in pairs],
        'map': [rpl_eval.er(run_b_score=runs_rpl[pair[0]]['scores'], run_a_score=runs_rpl[pair[1]]['scores'])['map'] for pair in pairs],
    }

    df = pd.DataFrame(df_content, index=['tf_1', 'tf_2', 'tf_3', 'tf_4', 'tf_5'])
    orig_val = 1
    ax = df.plot.bar(rot=0)
    ax.hlines(orig_val, -.5, 5.5, linestyles='dashed', color='black')
    ax.annotate(' ', (3, orig_val), color='black')
    ax.set_xlabel("Replicated Run")
    ax.set_ylabel("Effect Ratio (ER)")
    ax.get_figure().savefig('data/plots/rpl_er.pdf', format='pdf', bbox_inches='tight')
    plt.show()


if __name__ == "__main__":
    main()
