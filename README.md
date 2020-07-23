# repro-eval

### naming convention

- `rpl` replicated 
- `rpd` reproduced
- `rep` replicated/reproduced = repeated

### todos
- [x] cli
- [x] pretty print
- [x] interface extension for various runs
- [ ] plots (see subtasks below)
- [ ] code documentation
---
- [x] implement kendall's tau
- [x] implement rmse 
- [x] implement arp
- [x] implement rbo
- [x] implement effect ratio
- [x] implement delta relative improvement
- [x] implement p-values of ttests
- [x] implement absolute per-topic difference
- [x] Evaluator class
- [x] load runs in bulk
- [x] use-case: arp scores vs. run constellations (rpl) (plot)
- [ ] use-case: kendall's tau vs. cut-off (plot)
- [x] use-case: rmse vs. cut-off (rpl) (plot) 
- [x] use-case: er vs. run constellations (plot)
- [ ] use-case: er vs. deltaRI (plot)
---
- [ ] use-case: auto-generate pdf for overviews (bonus)
- [ ] correlation analysis (bonus)
- [ ] custom k for cut-offs? (bonus)

### open issues

- [ ] p-vals do not comply with results in sigir-paper

### interface 

Replicability test for single run:  
`python -m repro_eval -rpl qrel_orig orig_b rpl_b`

Replicability test for single run with specific measure:  
`python -m repro_eval -rpl -m rmse qrel_orig orig_b rpl_b`

Replicability test for baseline and advanced run:  
`python -m repro_eval -rpl qrel_orig orig_b orig_a rpl_b rpl_a`

Reproducibility test for single run:  
`python -m repro_eval -rpd qrel_orig qrel_rpd orig_b rpd_b`

Reproducibility test for baseline and advanced run:  
`python -m repro_eval -rpd qrel_orig qrel_rpd orig_b orig_a rpd_b rpd_a`


##### example 

replicability (full, all measures):  
```commandline
python -m repro_eval -t rpl -q ./example/data/qrels/core17.txt -r ./example/data/runs/orig/input.WCrobust04 ./example/data/runs/orig/input.WCrobust0405 ./example/data/runs/rpl/14/irc_task1_WCrobust04_001 ./example/data/runs/rpl/14/irc_task1_WCrobust0405_001
```

replicability (full, rmse):  
```commandline
python -m repro_eval -t rpl  -m rmse -q ./example/data/qrels/core17.txt -r ./example/data/runs/orig/input.WCrobust04 ./example/data/runs/orig/input.WCrobust0405 ./example/data/runs/rpl/14/irc_task1_WCrobust04_001 ./example/data/runs/rpl/14/irc_task1_WCrobust0405_001
```

replicability (baseline only, rmse):  
```commandline
python -m repro_eval -t rpl  -m rmse -q ./example/data/qrels/core17.txt -r ./example/data/runs/orig/input.WCrobust04 ./example/data/runs/rpl/14/irc_task1_WCrobust04_001
```

reproducibility (full):  
```commandline
python -m repro_eval -t rpd  -m er -q ./example/data/qrels/core17.txt ./example/data/qrels/core18.txt -r ./example/data/runs/orig/input.WCrobust04 ./example/data/runs/orig/input.WCrobust0405 ./example/data/runs/rpd/14/irc_task2_WCrobust04_001 ./example/data/runs/rpd/14/irc_task2_WCrobust0405_001
```

reproducibility (baseline only):  
```commandline
python -m repro_eval -t rpd -q ./example/data/qrels/core17.txt ./example/data/qrels/core18.txt -r ./example/data/runs/orig/input.WCrobust04 ./example/data/runs/rpd/14/irc_task2_WCrobust04_001
```


### setup
**`repro_eval`** can be installed as a Python package. Download the repository and it install with:
```
git clone https://github.com/irgroup/repro_eval
pip install repro_eval/
```

Some of the examples include visualizations. Install the required packages with:
```
pip install -r example/requirements.txt
```

### misc & links

- [ECIR21: Demo track](https://www.ecir2021.eu/call-for-demo-papers/)
- [pytrec_eval](https://github.com/cvangysel/pytrec_eval)
