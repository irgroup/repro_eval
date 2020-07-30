# repro-eval

### naming convention

- `rpl` replicated 
- `rpd` reproduced
- `rep` replicated/reproduced 

### setup
**`repro_eval`** can be installed as a Python package. Download the repository and it install with:
```
git clone https://github.com/irgroup/repro_eval
pip install repro_eval/
```

Some of the examples include plots and visualizations. Install the required packages with:
```
pip install -r example/requirements.txt
```

### interface 

Replicability test for single run:  
`python -m repro_eval -t rpl -q qrel_orig -r orig_b rpl_b`

Replicability test for baseline and advanced run:  
`python -m repro_eval -t rpl -q qrel_orig -r orig_b orig_a rpl_b rpl_a`

Replicability test for single run with specific measure:  
`python -m repro_eval -t rpl -m rmse -q qrel_orig -r orig_b rpl_b`  
whereas the measure can be `ktu`, `rmse`, `er`, `dri`, `ttest`.

Reproducibility test for single run:  
`python -m repro_eval -t rpd -q qrel_orig qrel_rpd -r orig_b rpd_b`

Reproducibility test for baseline and advanced run:  
`python -m repro_eval -t rpd -q qrel_orig qrel_rpd -r orig_b orig_a rpd_b rpd_a`

##### example 

replicability (full, all measures):  
```commandline
python -m repro_eval -t rpl -q ./example/data/qrels/core17.txt -r ./example/data/runs/orig/input.WCrobust04 ./example/data/runs/orig/input.WCrobust0405 ./example/data/runs/rpl/14/irc_task1_WCrobust04_001 ./example/data/runs/rpl/14/irc_task1_WCrobust0405_001
```
<details>
<summary>output</summary>

```
Kendall's tau Union (KTU)
------------------------------------------------------------------
416                      KTU     BASE    -0.0421   ADV     -0.0273
336                      KTU     BASE    0.0218    ADV     0.0002
443                      KTU     BASE    0.0161    ADV     0.0242
620                      KTU     BASE    0.0117    ADV     0.0122
423                      KTU     BASE    0.0205    ADV     -0.0116
419                      KTU     BASE    0.0244    ADV     -0.0294
439                      KTU     BASE    -0.0169   ADV     -0.0090
345                      KTU     BASE    0.0274    ADV     0.0315
347                      KTU     BASE    -0.0121   ADV     -0.0133
677                      KTU     BASE    0.0254    ADV     0.0142
435                      KTU     BASE    0.0231    ADV     0.0138
408                      KTU     BASE    -0.0023   ADV     0.0124
307                      KTU     BASE    0.0161    ADV     0.0517
404                      KTU     BASE    0.0201    ADV     0.0501
393                      KTU     BASE    0.0101    ADV     0.0723
445                      KTU     BASE    -0.0124   ADV     -0.0092
426                      KTU     BASE    -0.0203   ADV     0.0311
344                      KTU     BASE    -0.0306   ADV     0.0461
321                      KTU     BASE    -0.0077   ADV     0.0128
372                      KTU     BASE    0.0354    ADV     -0.0175
436                      KTU     BASE    0.0137    ADV     -0.0376
646                      KTU     BASE    -0.0232   ADV     0.0274
355                      KTU     BASE    -0.0075   ADV     -0.0014
690                      KTU     BASE    0.0090    ADV     0.0138
367                      KTU     BASE    -0.0144   ADV     0.0383
399                      KTU     BASE    0.0132    ADV     0.0308
362                      KTU     BASE    0.0329    ADV     -0.0072
341                      KTU     BASE    0.0307    ADV     0.0112
414                      KTU     BASE    -0.0039   ADV     0.0009
400                      KTU     BASE    0.0191    ADV     0.0120
356                      KTU     BASE    0.0221    ADV     0.0357
394                      KTU     BASE    0.0199    ADV     0.0134
310                      KTU     BASE    0.0169    ADV     0.0232
363                      KTU     BASE    0.0307    ADV     0.0359
433                      KTU     BASE    -0.0172   ADV     0.0401
442                      KTU     BASE    -0.0094   ADV     0.0368
397                      KTU     BASE    0.0004    ADV     0.0494
379                      KTU     BASE    -0.0257   ADV     0.0245
330                      KTU     BASE    -0.0163   ADV     0.0063
354                      KTU     BASE    0.0096    ADV     -0.0373
614                      KTU     BASE    0.0554    ADV     0.0579
353                      KTU     BASE    -0.0195   ADV     -0.0011
325                      KTU     BASE    0.0078    ADV     0.0150
389                      KTU     BASE    0.0842    ADV     0.1007
422                      KTU     BASE    0.0327    ADV     -0.0201
427                      KTU     BASE    -0.0077   ADV     -0.0109
375                      KTU     BASE    -0.0135   ADV     0.0261
350                      KTU     BASE    0.0170    ADV     0.0182
626                      KTU     BASE    -0.0108   ADV     -0.0094
378                      KTU     BASE    0.0380    ADV     0.0174
ARP                      KTU     BASE    0.0078    ADV     0.0153

Rank-biased Overlap (RBO)
------------------------------------------------------------------
416                      RBO     BASE    0.7633    ADV     0.7715
336                      RBO     BASE    0.5577    ADV     0.9150
443                      RBO     BASE    0.7137    ADV     0.7065
620                      RBO     BASE    0.7582    ADV     0.7508
423                      RBO     BASE    0.8454    ADV     0.8431
419                      RBO     BASE    0.5442    ADV     0.8216
439                      RBO     BASE    0.3504    ADV     0.1365
345                      RBO     BASE    0.5543    ADV     0.8887
347                      RBO     BASE    0.6319    ADV     0.5650
677                      RBO     BASE    0.8906    ADV     0.9438
435                      RBO     BASE    0.5240    ADV     0.4159
408                      RBO     BASE    0.2912    ADV     0.7111
307                      RBO     BASE    0.4107    ADV     0.5752
404                      RBO     BASE    0.6537    ADV     0.8206
393                      RBO     BASE    0.5326    ADV     0.6131
445                      RBO     BASE    0.8099    ADV     0.7904
426                      RBO     BASE    0.3533    ADV     0.6941
344                      RBO     BASE    0.4054    ADV     0.7339
321                      RBO     BASE    0.2391    ADV     0.3768
372                      RBO     BASE    0.6413    ADV     0.8315
436                      RBO     BASE    0.4401    ADV     0.7318
646                      RBO     BASE    0.6520    ADV     0.6031
355                      RBO     BASE    0.7456    ADV     0.7243
690                      RBO     BASE    0.9091    ADV     0.9409
367                      RBO     BASE    0.6082    ADV     0.4707
399                      RBO     BASE    0.8112    ADV     0.5672
362                      RBO     BASE    0.2559    ADV     0.7803
341                      RBO     BASE    0.6187    ADV     0.5256
414                      RBO     BASE    0.8100    ADV     0.8558
400                      RBO     BASE    0.5771    ADV     0.5113
356                      RBO     BASE    0.2681    ADV     0.4761
394                      RBO     BASE    0.2807    ADV     0.6645
310                      RBO     BASE    0.2970    ADV     0.5883
363                      RBO     BASE    0.4381    ADV     0.8471
433                      RBO     BASE    0.1335    ADV     0.7992
442                      RBO     BASE    0.7467    ADV     0.7619
397                      RBO     BASE    0.5117    ADV     0.6125
379                      RBO     BASE    0.1610    ADV     0.1879
330                      RBO     BASE    0.5414    ADV     0.6241
354                      RBO     BASE    0.5623    ADV     0.5624
614                      RBO     BASE    0.5327    ADV     0.5800
353                      RBO     BASE    0.7371    ADV     0.7358
325                      RBO     BASE    0.7245    ADV     0.7125
389                      RBO     BASE    0.8963    ADV     0.7041
422                      RBO     BASE    0.5215    ADV     0.5602
427                      RBO     BASE    0.4341    ADV     0.8960
375                      RBO     BASE    0.6768    ADV     0.9199
350                      RBO     BASE    0.8417    ADV     0.8589
626                      RBO     BASE    0.7840    ADV     0.7671
378                      RBO     BASE    0.1935    ADV     0.2446
ARP                      RBO     BASE    0.5636    ADV     0.6744

Root mean square error (RMSE)
------------------------------------------------------------------
map                      RMSE    BASE    0.0748    ADV     0.0419
gm_map                   RMSE    BASE    0.8454    ADV     0.1257
Rprec                    RMSE    BASE    0.0714    ADV     0.0369
bpref                    RMSE    BASE    0.0624    ADV     0.0365
recip_rank               RMSE    BASE    0.2495    ADV     0.1856
iprec_at_recall_0.00     RMSE    BASE    0.1616    ADV     0.1012
iprec_at_recall_0.10     RMSE    BASE    0.1364    ADV     0.0808
iprec_at_recall_0.20     RMSE    BASE    0.1284    ADV     0.0805
iprec_at_recall_0.30     RMSE    BASE    0.1240    ADV     0.0812
iprec_at_recall_0.40     RMSE    BASE    0.1148    ADV     0.0730
iprec_at_recall_0.50     RMSE    BASE    0.1315    ADV     0.0759
iprec_at_recall_0.60     RMSE    BASE    0.1243    ADV     0.0750
iprec_at_recall_0.70     RMSE    BASE    0.0793    ADV     0.0452
iprec_at_recall_0.80     RMSE    BASE    0.0792    ADV     0.0674
iprec_at_recall_0.90     RMSE    BASE    0.0888    ADV     0.0527
iprec_at_recall_1.00     RMSE    BASE    0.0013    ADV     0.0034
P_5                      RMSE    BASE    0.2173    ADV     0.1575
P_10                     RMSE    BASE    0.2000    ADV     0.1020
P_15                     RMSE    BASE    0.1218    ADV     0.0693
P_20                     RMSE    BASE    0.1319    ADV     0.0738
P_30                     RMSE    BASE    0.1396    ADV     0.0785
P_100                    RMSE    BASE    0.0901    ADV     0.0553
P_200                    RMSE    BASE    0.0620    ADV     0.0330
P_500                    RMSE    BASE    0.0389    ADV     0.0179
P_1000                   RMSE    BASE    0.0194    ADV     0.0103
recall_5                 RMSE    BASE    0.0138    ADV     0.0154
recall_10                RMSE    BASE    0.0268    ADV     0.0173
recall_15                RMSE    BASE    0.0282    ADV     0.0108
recall_20                RMSE    BASE    0.0364    ADV     0.0189
recall_30                RMSE    BASE    0.0505    ADV     0.0269
recall_100               RMSE    BASE    0.0710    ADV     0.0462
recall_200               RMSE    BASE    0.0766    ADV     0.0408
recall_500               RMSE    BASE    0.0916    ADV     0.0564
recall_1000              RMSE    BASE    0.0776    ADV     0.0504
infAP                    RMSE    BASE    0.0748    ADV     0.0419
gm_bpref                 RMSE    BASE    1.2204    ADV     0.0859
Rprec_mult_0.20          RMSE    BASE    0.1431    ADV     0.1009
Rprec_mult_0.40          RMSE    BASE    0.1266    ADV     0.0713
Rprec_mult_0.60          RMSE    BASE    0.1066    ADV     0.0506
Rprec_mult_0.80          RMSE    BASE    0.0864    ADV     0.0447
Rprec_mult_1.00          RMSE    BASE    0.0714    ADV     0.0369
Rprec_mult_1.20          RMSE    BASE    0.0609    ADV     0.0286
Rprec_mult_1.40          RMSE    BASE    0.0544    ADV     0.0273
Rprec_mult_1.60          RMSE    BASE    0.0491    ADV     0.0256
Rprec_mult_1.80          RMSE    BASE    0.0481    ADV     0.0258
Rprec_mult_2.00          RMSE    BASE    0.0420    ADV     0.0240
utility                  RMSE    BASE    38.8999    ADV     20.5621
11pt_avg                 RMSE    BASE    0.0741    ADV     0.0398
binG                     RMSE    BASE    0.0288    ADV     0.0219
G                        RMSE    BASE    0.0219    ADV     0.0151
ndcg                     RMSE    BASE    0.0742    ADV     0.0373
ndcg_rel                 RMSE    BASE    0.0676    ADV     0.0389
Rndcg                    RMSE    BASE    0.0729    ADV     0.0357
ndcg_cut_5               RMSE    BASE    0.1809    ADV     0.1121
ndcg_cut_10              RMSE    BASE    0.1521    ADV     0.0912
ndcg_cut_15              RMSE    BASE    0.1150    ADV     0.0703
ndcg_cut_20              RMSE    BASE    0.1100    ADV     0.0624
ndcg_cut_30              RMSE    BASE    0.1108    ADV     0.0555
ndcg_cut_100             RMSE    BASE    0.0906    ADV     0.0486
ndcg_cut_200             RMSE    BASE    0.0793    ADV     0.0405
ndcg_cut_500             RMSE    BASE    0.0809    ADV     0.0397
ndcg_cut_1000            RMSE    BASE    0.0742    ADV     0.0373
map_cut_5                RMSE    BASE    0.0103    ADV     0.0099
map_cut_10               RMSE    BASE    0.0169    ADV     0.0168
map_cut_15               RMSE    BASE    0.0200    ADV     0.0138
map_cut_20               RMSE    BASE    0.0230    ADV     0.0177
map_cut_30               RMSE    BASE    0.0318    ADV     0.0230
map_cut_100              RMSE    BASE    0.0537    ADV     0.0331
map_cut_200              RMSE    BASE    0.0623    ADV     0.0391
map_cut_500              RMSE    BASE    0.0745    ADV     0.0419
map_cut_1000             RMSE    BASE    0.0748    ADV     0.0419
relative_P_5             RMSE    BASE    0.2173    ADV     0.1575
relative_P_10            RMSE    BASE    0.2000    ADV     0.1020
relative_P_15            RMSE    BASE    0.1219    ADV     0.0693
relative_P_20            RMSE    BASE    0.1319    ADV     0.0738
relative_P_30            RMSE    BASE    0.1398    ADV     0.0785
relative_P_100           RMSE    BASE    0.1044    ADV     0.0656
relative_P_200           RMSE    BASE    0.0896    ADV     0.0469
relative_P_500           RMSE    BASE    0.0917    ADV     0.0564
relative_P_1000          RMSE    BASE    0.0776    ADV     0.0504
success_1                RMSE    BASE    0.4690    ADV     0.3464
success_5                RMSE    BASE    0.2449
success_10               RMSE    BASE    0.2449
set_P                    RMSE    BASE    0.0194    ADV     0.0103
set_relative_P           RMSE    BASE    0.0776    ADV     0.0504
set_recall               RMSE    BASE    0.0776    ADV     0.0504
set_map                  RMSE    BASE    0.0234    ADV     0.0127
set_F                    RMSE    BASE    0.0288    ADV     0.0156

Effect ratio (ER)
------------------------------------------------------------------
map                      ER      0.9995
gm_map                   ER      1.5355
Rprec                    ER      0.9800
bpref                    ER      1.0337
recip_rank               ER      0.9537
iprec_at_recall_0.00     ER      1.3568
iprec_at_recall_0.10     ER      1.0145
iprec_at_recall_0.20     ER      0.7347
iprec_at_recall_0.30     ER      0.9327
iprec_at_recall_0.40     ER      1.0209
iprec_at_recall_0.50     ER      1.0420
iprec_at_recall_0.60     ER      1.0763
iprec_at_recall_0.70     ER      1.4027
iprec_at_recall_0.80     ER      1.4350
iprec_at_recall_0.90     ER      2.0266
iprec_at_recall_1.00     ER      1.2113
P_5                      ER      1.0000
P_10                     ER      0.9615
P_15                     ER      0.8732
P_20                     ER      0.6598
P_30                     ER      0.7872
P_100                    ER      0.8289
P_200                    ER      1.1093
P_500                    ER      1.3894
P_1000                   ER      1.3393
recall_5                 ER      1.5246
recall_10                ER      1.2527
recall_15                ER      0.8754
recall_20                ER      0.6278
recall_30                ER      0.8939
recall_100               ER      0.8649
recall_200               ER      1.2028
recall_500               ER      1.2141
recall_1000              ER      1.1980
infAP                    ER      0.9995
gm_bpref                 ER      1.9791
Rprec_mult_0.20          ER      0.9514
Rprec_mult_0.40          ER      0.7819
Rprec_mult_0.60          ER      0.9816
Rprec_mult_0.80          ER      1.0073
Rprec_mult_1.00          ER      0.9800
Rprec_mult_1.20          ER      1.1698
Rprec_mult_1.40          ER      1.1482
Rprec_mult_1.60          ER      1.1942
Rprec_mult_1.80          ER      1.2484
Rprec_mult_2.00          ER      1.2914
utility                  ER      1.3393
11pt_avg                 ER      1.0560
binG                     ER      1.0475
G                        ER      1.0782
ndcg                     ER      1.1006
ndcg_rel                 ER      1.0011
Rndcg                    ER      1.0240
ndcg_cut_5               ER      1.0210
ndcg_cut_10              ER      0.9721
ndcg_cut_15              ER      0.9711
ndcg_cut_20              ER      0.7974
ndcg_cut_30              ER      0.8690
ndcg_cut_100             ER      0.8864
ndcg_cut_200             ER      1.0363
ndcg_cut_500             ER      1.0965
ndcg_cut_1000            ER      1.1006
map_cut_5                ER      1.0174
map_cut_10               ER      1.2620
map_cut_15               ER      0.9572
map_cut_20               ER      0.7845
map_cut_30               ER      0.8635
map_cut_100              ER      0.8275
map_cut_200              ER      0.9173
map_cut_500              ER      0.9963
map_cut_1000             ER      0.9995
relative_P_5             ER      1.0000
relative_P_10            ER      0.9615
relative_P_15            ER      0.8722
relative_P_20            ER      0.6598
relative_P_30            ER      0.7927
relative_P_100           ER      0.8342
relative_P_200           ER      1.1999
relative_P_500           ER      1.2157
relative_P_1000          ER      1.1980
success_1                ER      0.8571
success_5                ER      2.0000
success_10               ER      1.5000
set_P                    ER      1.3393
set_relative_P           ER      1.1980
set_recall               ER      1.1980
set_map                  ER      1.3253
set_F                    ER      1.3187

Delta Relative Improvement (DRI)
------------------------------------------------------------------
map                      DRI     -0.0060
gm_map                   DRI     0.0757
Rprec                    DRI     -0.0010
bpref                    DRI     -0.0058
recip_rank               DRI     0.0049
iprec_at_recall_0.00     DRI     -0.0282
iprec_at_recall_0.10     DRI     0.0002
iprec_at_recall_0.20     DRI     0.0430
iprec_at_recall_0.30     DRI     0.0043
iprec_at_recall_0.40     DRI     -0.0128
iprec_at_recall_0.50     DRI     -0.0207
iprec_at_recall_0.60     DRI     -0.0204
iprec_at_recall_0.70     DRI     -0.0833
iprec_at_recall_0.80     DRI     -0.1014
iprec_at_recall_0.90     DRI     -0.2018
iprec_at_recall_1.00     DRI     -1.0723
P_5                      DRI     0.0039
P_10                     DRI     0.0117
P_15                     DRI     0.0228
P_20                     DRI     0.0550
P_30                     DRI     0.0362
P_100                    DRI     0.0208
P_200                    DRI     -0.0148
P_500                    DRI     -0.0341
P_1000                   DRI     -0.0252
recall_5                 DRI     -0.0373
recall_10                DRI     -0.0270
recall_15                DRI     0.0188
recall_20                DRI     0.0613
recall_30                DRI     0.0161
recall_100               DRI     0.0103
recall_200               DRI     -0.0259
recall_500               DRI     -0.0192
recall_1000              DRI     -0.0136
infAP                    DRI     -0.0060
gm_bpref                 DRI     0.1053
Rprec_mult_0.20          DRI     0.0069
Rprec_mult_0.40          DRI     0.0312
Rprec_mult_0.60          DRI     -0.0004
Rprec_mult_0.80          DRI     -0.0043
Rprec_mult_1.00          DRI     -0.0010
Rprec_mult_1.20          DRI     -0.0222
Rprec_mult_1.40          DRI     -0.0219
Rprec_mult_1.60          DRI     -0.0257
Rprec_mult_1.80          DRI     -0.0307
Rprec_mult_2.00          DRI     -0.0338
utility                  DRI     0.0066
11pt_avg                 DRI     -0.0132
binG                     DRI     -0.0113
G                        DRI     -0.0151
ndcg                     DRI     -0.0130
ndcg_rel                 DRI     -0.0022
Rndcg                    DRI     -0.0059
ndcg_cut_5               DRI     -0.0009
ndcg_cut_10              DRI     0.0111
ndcg_cut_15              DRI     0.0093
ndcg_cut_20              DRI     0.0430
ndcg_cut_30              DRI     0.0283
ndcg_cut_100             DRI     0.0162
ndcg_cut_200             DRI     -0.0083
ndcg_cut_500             DRI     -0.0146
ndcg_cut_1000            DRI     -0.0130
map_cut_5                DRI     0.0054
map_cut_10               DRI     -0.0347
map_cut_15               DRI     0.0146
map_cut_20               DRI     0.0449
map_cut_30               DRI     0.0317
map_cut_100              DRI     0.0314
map_cut_200              DRI     0.0122
map_cut_500              DRI     -0.0052
map_cut_1000             DRI     -0.0060
relative_P_5             DRI     0.0039
relative_P_10            DRI     0.0117
relative_P_15            DRI     0.0229
relative_P_20            DRI     0.0545
relative_P_30            DRI     0.0347
relative_P_100           DRI     0.0180
relative_P_200           DRI     -0.0255
relative_P_500           DRI     -0.0193
relative_P_1000          DRI     -0.0136
success_1                DRI     0.0333
success_5                DRI     -0.0222
success_10               DRI     -0.0227
set_P                    DRI     -0.0252
set_relative_P           DRI     -0.0136
set_recall               DRI     -0.0136
set_map                  DRI     -0.0390
set_F                    DRI     -0.0232

Two-tailed paired t-test (p-value)
------------------------------------------------------------------
map                      PVAL    BASE    0.7001    ADV     0.6543
gm_map                   PVAL    BASE    0.4844    ADV     0.6685
Rprec                    PVAL    BASE    0.7425    ADV     0.6369
bpref                    PVAL    BASE    0.8014    ADV     0.8097
recip_rank               PVAL    BASE    0.9708    ADV     0.8970
iprec_at_recall_0.00     PVAL    BASE    0.7443    ADV     0.8939
iprec_at_recall_0.10     PVAL    BASE    0.8421    ADV     0.7747
iprec_at_recall_0.20     PVAL    BASE    0.9859    ADV     0.4898
iprec_at_recall_0.30     PVAL    BASE    0.6625    ADV     0.4960
iprec_at_recall_0.40     PVAL    BASE    0.6059    ADV     0.5784
iprec_at_recall_0.50     PVAL    BASE    0.5075    ADV     0.5185
iprec_at_recall_0.60     PVAL    BASE    0.6685    ADV     0.7158
iprec_at_recall_0.70     PVAL    BASE    0.6349    ADV     0.8604
iprec_at_recall_0.80     PVAL    BASE    0.7431    ADV     0.9836
iprec_at_recall_0.90     PVAL    BASE    0.3551    ADV     0.6132
iprec_at_recall_1.00     PVAL    BASE    0.8047    ADV     0.9632
P_5                      PVAL    BASE    0.7282    ADV     0.7156
P_10                     PVAL    BASE    0.6547    ADV     0.6977
P_15                     PVAL    BASE    0.7097    ADV     0.8717
P_20                     PVAL    BASE    0.7674    ADV     0.7275
P_30                     PVAL    BASE    0.8141    ADV     0.8819
P_100                    PVAL    BASE    0.7718    ADV     0.5892
P_200                    PVAL    BASE    0.7939    ADV     0.8647
P_500                    PVAL    BASE    0.6805    ADV     0.8472
P_1000                   PVAL    BASE    0.6923    ADV     0.8141
recall_5                 PVAL    BASE    0.8928    ADV     0.7431
recall_10                PVAL    BASE    0.9377    ADV     0.8453
recall_15                PVAL    BASE    0.9107    ADV     0.9557
recall_20                PVAL    BASE    0.9386    ADV     0.8502
recall_30                PVAL    BASE    0.9871    ADV     0.9134
recall_100               PVAL    BASE    0.6141    ADV     0.4410
recall_200               PVAL    BASE    0.5990    ADV     0.7428
recall_500               PVAL    BASE    0.3830    ADV     0.4185
recall_1000              PVAL    BASE    0.4268    ADV     0.4374
infAP                    PVAL    BASE    0.7001    ADV     0.6543
gm_bpref                 PVAL    BASE    0.6478    ADV     0.9532
Rprec_mult_0.20          PVAL    BASE    0.9536    ADV     0.9882
Rprec_mult_0.40          PVAL    BASE    0.9510    ADV     0.6948
Rprec_mult_0.60          PVAL    BASE    0.8041    ADV     0.7100
Rprec_mult_0.80          PVAL    BASE    0.7220    ADV     0.6477
Rprec_mult_1.00          PVAL    BASE    0.7425    ADV     0.6369
Rprec_mult_1.20          PVAL    BASE    0.5581    ADV     0.6220
Rprec_mult_1.40          PVAL    BASE    0.5266    ADV     0.5630
Rprec_mult_1.60          PVAL    BASE    0.4934    ADV     0.5750
Rprec_mult_1.80          PVAL    BASE    0.4660    ADV     0.5930
Rprec_mult_2.00          PVAL    BASE    0.4490    ADV     0.6098
utility                  PVAL    BASE    0.6923    ADV     0.8141
11pt_avg                 PVAL    BASE    0.6772    ADV     0.6879
binG                     PVAL    BASE    0.7769    ADV     0.8279
G                        PVAL    BASE    0.7161    ADV     0.7779
ndcg                     PVAL    BASE    0.5679    ADV     0.5655
ndcg_rel                 PVAL    BASE    0.8013    ADV     0.7427
Rndcg                    PVAL    BASE    0.7772    ADV     0.7420
ndcg_cut_5               PVAL    BASE    0.8855    ADV     0.8443
ndcg_cut_10              PVAL    BASE    0.7655    ADV     0.7908
ndcg_cut_15              PVAL    BASE    0.8195    ADV     0.8474
ndcg_cut_20              PVAL    BASE    0.8021    ADV     0.8584
ndcg_cut_30              PVAL    BASE    0.8123    ADV     0.9729
ndcg_cut_100             PVAL    BASE    0.7779    ADV     0.4943
ndcg_cut_200             PVAL    BASE    0.7426    ADV     0.7074
ndcg_cut_500             PVAL    BASE    0.5624    ADV     0.5504
ndcg_cut_1000            PVAL    BASE    0.5679    ADV     0.5655
map_cut_5                PVAL    BASE    0.7930    ADV     0.7675
map_cut_10               PVAL    BASE    0.9042    ADV     0.7673
map_cut_15               PVAL    BASE    0.8403    ADV     0.8489
map_cut_20               PVAL    BASE    0.8800    ADV     0.9813
map_cut_30               PVAL    BASE    0.8867    ADV     0.9984
map_cut_100              PVAL    BASE    0.8958    ADV     0.6461
map_cut_200              PVAL    BASE    0.8762    ADV     0.7220
map_cut_500              PVAL    BASE    0.7280    ADV     0.6743
map_cut_1000             PVAL    BASE    0.7001    ADV     0.6543
relative_P_5             PVAL    BASE    0.7282    ADV     0.7156
relative_P_10            PVAL    BASE    0.6547    ADV     0.6977
relative_P_15            PVAL    BASE    0.7080    ADV     0.8713
relative_P_20            PVAL    BASE    0.7663    ADV     0.7240
relative_P_30            PVAL    BASE    0.8126    ADV     0.8803
relative_P_100           PVAL    BASE    0.5888    ADV     0.3251
relative_P_200           PVAL    BASE    0.5206    ADV     0.6721
relative_P_500           PVAL    BASE    0.3782    ADV     0.4128
relative_P_1000          PVAL    BASE    0.4268    ADV     0.4374
success_1                PVAL    BASE    0.8298    ADV     1.0000
success_5                PVAL    BASE    0.7095    ADV     1.0000
success_10               PVAL    BASE    0.7095    ADV     1.0000
set_P                    PVAL    BASE    0.6923    ADV     0.8141
set_relative_P           PVAL    BASE    0.4268    ADV     0.4374
set_recall               PVAL    BASE    0.4268    ADV     0.4374
set_map                  PVAL    BASE    0.5982    ADV     0.7395
set_F                    PVAL    BASE    0.6768    ADV     0.7968
```
</details>

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

### todos
- [x] cli
- [x] pretty print
- [x] interface extension for various runs
- [x] plots (see subtasks below)
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
- [x] plot: arp scores vs. run constellations (rpl) 
- [x] plot: kendall's tau vs. cut-off (rpl) 
- [x] plot: rmse vs. cut-off (rpl) 
- [x] plot: er vs. run constellations 
- [x] plot: er vs. deltaRI 
---
- [ ] correlation analysis (bonus)
- [ ] custom k for cut-offs? (bonus)

### open issues

- [ ] p-vals do not comply with results in sigir-paper

### misc & links

We use the implementation of the Rank-biased Overlap (RBO) by [dlukes](https://github.com/dlukes) at [620b84e](https://github.com/dlukes/rbo/tree/620b84e55e8b596e7fd9005cc8ca4b7a8522f2d6).
We build up on the [pytrec_eval](https://github.com/cvangysel/pytrec_eval) interface for the underlying IR measures.
We benefited from these codebases a lot and would like to express our gratitude for authors of these repositories.
