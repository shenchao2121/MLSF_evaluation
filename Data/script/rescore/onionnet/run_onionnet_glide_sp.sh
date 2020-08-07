#!/bin/bash
module purge
export PYTHONPATH=/home/shenchao/python_module3.6/lib/python3.6/site-packages:/opt/anaconda3/5.2.0/lib/python3.6/site-packages
export LD_LIBRARY_PATH=/opt/anaconda3/5.2.0/lib:${LD_LIBRARY_PATH}
module load anaconda3/5.2.0
module load openbabel

python onionnet_perform_glide_sp.py
