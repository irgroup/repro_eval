import pytrec_eval
from repro_eval.Evaluator import RpdEvaluator
from repro_eval.util import arp, arp_scores
from repro_eval.util import trim
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
sns.set()
sns.set_style('whitegrid')
# palette = sns.color_palette("GnBu_d")
# sns.set_palette(palette)
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



def average_retrieval_performance(baseline_scores, reproduced_scores: dict, measures: list, xlabel: str, ylabel: str, outfile: str):
    reproduced_scores_arp = [arp_scores(topic_scores) for idx, topic_scores in reproduced_scores.items()]
    baseline_scores_arp = arp_scores(baseline_scores)
    index = list(reproduced_scores.keys())
    df_content = {}
    for measure in measures:
        df_content[measure] = [scores.get(measure) for scores in reproduced_scores_arp]
    df = pd.DataFrame(df_content, index=index)

    ax = df.plot.bar(rot=0)
    for num, measure in enumerate(measures):
        orig_val = baseline_scores_arp.get(measure)
        ax.hlines(orig_val, -.5, 5.5, linestyles='dashed', color=colors[num])
        ax.annotate(' ', (num, orig_val), color=colors[num])
        ax.set_ylim(0.0, 1.0)

    legend_content = [measure + ' (orig)' for measure in measures] + [measure + ' (rpl)' for measure in measures]
    ax.legend(legend_content, loc='lower left')

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.get_figure().savefig(outfile, format='pdf', bbox_inches='tight')
    plt.show()


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

    average_retrieval_performance(rpd_eval.run_b_orig_score,
                                  {
                                      'tf_1': runs_rpd.get('rpd_wcr04_tf_1').get('scores'),
                                      'tf_2': runs_rpd.get('rpd_wcr04_tf_2').get('scores'),
                                      'tf_3': runs_rpd.get('rpd_wcr04_tf_3').get('scores'),
                                      'tf_4': runs_rpd.get('rpd_wcr04_tf_4').get('scores'),
                                      'tf_5': runs_rpd.get('rpd_wcr04_tf_5').get('scores'),
                                  },
                                  measures=['P_10', 'ndcg', 'bpref', 'map'],
                                  xlabel='Reproduced run (wcr04)',
                                  ylabel='Score',
                                  outfile='data/plots/rpd_b_arp.pdf')

    average_retrieval_performance(rpd_eval.run_a_orig_score,
                                  {
                                      'tf_1': runs_rpd.get('rpd_wcr0405_tf_1').get('scores'),
                                      'tf_2': runs_rpd.get('rpd_wcr0405_tf_2').get('scores'),
                                      'tf_3': runs_rpd.get('rpd_wcr0405_tf_3').get('scores'),
                                      'tf_4': runs_rpd.get('rpd_wcr0405_tf_4').get('scores'),
                                      'tf_5': runs_rpd.get('rpd_wcr0405_tf_5').get('scores'),
                                  },
                                  measures=['P_10', 'ndcg', 'bpref', 'map'],
                                  xlabel='Reproduced run (wcr0405)',
                                  ylabel='Score',
                                  outfile='data/plots/rpd_a_arp.pdf')


if __name__ == "__main__":
    main()