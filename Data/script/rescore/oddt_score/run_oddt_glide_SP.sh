#!/bin/bash
module purge
#export PYTHONPATH=/home/shenchao/python_module2/lib/python2.7/site-packages:/opt/anaconda2/5.3.0/lib/python2.7/site-packages:/opt/openbabel/2.4.1/lib64/python2.7/site-packages
export PYTHONPATH=/home/shenchao/python_module2/lib/python2.7/site-packages:/opt/openbabel/2.4.1/lib64/python2.7/site-packages
export LD_LIBRARY_PATH=/opt/anaconda2/5.3.0/lib:/opt/openbabel/2.4.1/lib:${LD_LIBRARY_PATH}
module load openbabel
module load anaconda2

python oddt_perform_glide_SP.py
