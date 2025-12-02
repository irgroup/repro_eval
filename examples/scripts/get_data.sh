#!/bin/bash

wget https://www.dropbox.com/s/p1wwqqka1n3el6b/runs.tar.gz 
mkdir ./data
mkdir ./data/qrels
wget -O "./data/qrels/core17.txt" https://trec.nist.gov/data/core/qrels.txt
wget -O "./data/qrels/core18.txt" https://trec.nist.gov/data/core/qrels2018.txt
tar -xzvf runs.tar.gz -C ./data/
