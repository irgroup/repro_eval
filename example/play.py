from repro_eval.Evaluator import RplEvaluator
from repro_eval.util import print_base_adv, print_simple_line, trim
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="darkgrid")

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

# def main():
#
#     rpl_eval = RplEvaluator(qrel_orig_path=QREL,
#                             run_b_orig_path=ORIG_B,
#                             run_b_rep_path=RPL_B)
#
#     rpl_eval.trim()
#     rpl_eval.evaluate()
#     rpl_eval.er()

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


def main():
    rpl_eval = RplEvaluator(qrel_orig_path=QREL,
                            run_b_orig_path=ORIG_B,
                            run_a_orig_path=ORIG_A,
                            run_b_rep_path=None,
                            run_a_rep_path=None)

    rpl_eval.trim()
    rpl_eval.evaluate()

    for run_name, info in runs_rpl.items():
        with open(info.get('path')) as run_file:
            info['run'] = pytrec_eval.parse_run(run_file)
            trim(info['run'])
            info['scores'] = rpl_eval.evaluate(info['run'])

    dri_er = {
        'wcr04_tf_1': {
            'er': rpl_eval.er(runs_rpl['rpl_wcr04_tf_1']['scores'], runs_rpl['rpl_wcr0405_tf_1']['scores']),
            'dri': rpl_eval.dri(runs_rpl['rpl_wcr04_tf_1']['scores'], runs_rpl['rpl_wcr0405_tf_1']['scores'])
        },
        'wcr04_tf_2': {
            'er': rpl_eval.er(runs_rpl['rpl_wcr04_tf_2']['scores'], runs_rpl['rpl_wcr0405_tf_2']['scores']),
            'dri': rpl_eval.dri(runs_rpl['rpl_wcr04_tf_2']['scores'], runs_rpl['rpl_wcr0405_tf_2']['scores'])
        },
        'wcr04_tf_3': {
            'er': rpl_eval.er(runs_rpl['rpl_wcr04_tf_3']['scores'], runs_rpl['rpl_wcr0405_tf_3']['scores']),
            'dri': rpl_eval.dri(runs_rpl['rpl_wcr04_tf_3']['scores'], runs_rpl['rpl_wcr0405_tf_3']['scores'])
        },
        'wcr04_tf_4': {
            'er': rpl_eval.er(runs_rpl['rpl_wcr04_tf_4']['scores'], runs_rpl['rpl_wcr0405_tf_4']['scores']),
            'dri': rpl_eval.dri(runs_rpl['rpl_wcr04_tf_4']['scores'], runs_rpl['rpl_wcr0405_tf_4']['scores'])
        },
        'wcr04_tf_5': {
            'er': rpl_eval.er(runs_rpl['rpl_wcr04_tf_5']['scores'], runs_rpl['rpl_wcr0405_tf_5']['scores']),
            'dri': rpl_eval.dri(runs_rpl['rpl_wcr04_tf_5']['scores'], runs_rpl['rpl_wcr0405_tf_5']['scores'])
        },

    }

    measures = ['P_10', 'map', 'ndcg']
    marker_color = [('o', 'b'), ('^', 'g'), ('v', 'r')]

    fig, ax1 = plt.subplots()
    ax1.set_xlabel('Effect Ratio (ER)')
    ax1.set_ylabel(u'Delta Relative Improvement (ΔRI)')

    for measure, mk in zip(measures, marker_color):
        ax1.plot([dri_er[r]['er'][measure] for r in dri_er.keys()],
                 [dri_er[r]['dri'][measure] for r in dri_er.keys()],
                 marker=mk[0], color=mk[1], linestyle='None', label=measure)

    ax1.tick_params(axis='y', labelcolor='k')
    fig.tight_layout()
    plt.axhline(0, color='grey')
    plt.axvline(1, color='grey')
    plt.legend()
    plt.title('Replicability')
    plt.show()


    pass


if __name__ == "__main__":
    main()
