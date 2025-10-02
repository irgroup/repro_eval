TRIM_THRESH = 1000  # default threshold for trimming the runs
ERR_MSG = 'Please provide adequate run combinations and have them evaluated first.'  # error message
RBO_DEPTH = 1000 # default parameter for the Rank-Biased Overlap (RBO)
RBO_P = 0.95 # default parameter for the Rank-Biased Overlap (RBO)

# evaluation measures of trec_eval that will be excluded from the reproduction and replication measures
exclude = [
    'runid',
    'num_q',
    'num_ret',
    'num_rel',
    'num_rel_ret',
    'num_nonrel_judged_ret',
    'relstring'
]
