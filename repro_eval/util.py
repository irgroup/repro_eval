from repro_eval.config import TRIM_THRESH


def trim(run, thresh=TRIM_THRESH):
    for topic, docs in run.items():
        run[topic] = dict(list(run[topic].items())[:thresh])


def print_base_adv(measure_topic, repro_measure, base_value, adv_value=None):
    if adv_value:
        fill = ('{:3s}' if base_value < 0 else '{:4s}')
        print(('{:25s}{:8s}{:8s}{:.4f}' + fill + '{:8s}{:.4f}').format(measure_topic, repro_measure,
                                                                       'BASE', base_value, ' ', 'ADV', adv_value))
    else:
        print('{:25s}{:8s}{:8s}{:.4f}'.format(measure_topic, repro_measure, 'BASE', base_value))


def print_simple_line(measure, repro_measure, value):
    print('{:25s}{:8s}{:.4f}'.format(measure, repro_measure, value))

