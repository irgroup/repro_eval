import pytrec_eval
from repro_eval.Evaluator import RpdEvaluator
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

runs_rpd = {
    'rpd_wcr04_tf_1':
        {'path': './data/runs/rpd/45/irc_task1_WCrobust04_001'},
    'rpd_wcr0405_tf_1':
        {'path': './data/runs/rpd/45/irc_task1_WCrobust0405_001'},
    'rpd_wcr04_tf_2':
        {'path': './data/runs/rpd/46/irc_task1_WCrobust04_001'},
    'rpd_wcr0405_tf_2':
        {'path': './data/runs/rpd/46/irc_task1_WCrobust0405_001'},
    'rpd_wcr04_tf_3':
        {'path': './data/runs/rpd/47/irc_task1_WCrobust04_001'},
    'rpd_wcr0405_tf_3':
        {'path': './data/runs/rpd/47/irc_task1_WCrobust0405_001'},
    'rpd_wcr04_tf_4':
        {'path': './data/runs/rpd/48/irc_task1_WCrobust04_001'},
    'rpd_wcr0405_tf_4':
        {'path': './data/runs/rpd/48/irc_task1_WCrobust0405_001'},
    'rpd_wcr04_tf_5':
        {'path': './data/runs/rpd/49/irc_task1_WCrobust04_001'},
    'rpd_wcr0405_tf_5':
        {'path': './data/runs/rpd/49/irc_task1_WCrobust0405_001'}
}


def main():
    rpd_eval = RpdEvaluator(qrel_orig_path=QREL,
                            run_b_orig_path=ORIG_B,
                            run_a_orig_path=ORIG_A,
                            run_b_rep_path=None,
                            run_a_rep_path=None)

    rpd_eval.trim()
    rpd_eval.evaluate()

    for run_name, info in runs_rpd.items():
        with open(info.get('path')) as run_file:
            info['run'] = pytrec_eval.parse_run(run_file)
            trim(info['run'])
            info['scores'] = rpd_eval.evaluate(info['run'])

    pairs = [('rpd_wcr04_tf_1', 'rpd_wcr0405_tf_1'),
             ('rpd_wcr04_tf_2', 'rpd_wcr0405_tf_2'),
             ('rpd_wcr04_tf_3', 'rpd_wcr0405_tf_3'),
             ('rpd_wcr04_tf_4', 'rpd_wcr0405_tf_4'),
             ('rpd_wcr04_tf_5', 'rpd_wcr0405_tf_5')]

    df_content = {
        'P_10': [rpd_eval.er(run_b_score=runs_rpd[pair[0]]['scores'], run_a_score=runs_rpd[pair[1]]['scores'])['P_10'] for pair in pairs],
        'ndcg': [rpd_eval.er(run_b_score=runs_rpd[pair[0]]['scores'], run_a_score=runs_rpd[pair[1]]['scores'])['ndcg'] for pair in pairs],
        'map': [rpd_eval.er(run_b_score=runs_rpd[pair[0]]['scores'], run_a_score=runs_rpd[pair[1]]['scores'])['map'] for pair in pairs],
    }

    df = pd.DataFrame(df_content, index=['tf_1', 'tf_2', 'tf_3', 'tf_4', 'tf_5'])
    orig_val = 1
    ax = df.plot.bar(rot=0)
    ax.hlines(orig_val, -.5, 5.5, linestyles='dashed', color='black')
    ax.annotate(' ', (3, orig_val), color='black')
    ax.set_xlabel("Reproduced Run")
    ax.set_ylabel("Effect Ratio (ER)")
    ax.get_figure().savefig('data/plots/rpd_er.pdf', format='pdf', bbox_inches='tight')
    plt.show()


if __name__ == "__main__":
    main()
