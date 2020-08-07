#!/bin/bash

module purge
export PYTHONPATH=/home/shenchao/python_module2/lib/python2.7/site-packages:/opt/openbabel/2.4.1/lib64/python2.7/site-packages:/home/shenchao/AI_evaluation/software/pafnucy/tfbio-master
##module load openbabel
##export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/openbabel/2.4.1/lib
module load anaconda2
python2 pafnucy_perform_gold_chemplp.py








