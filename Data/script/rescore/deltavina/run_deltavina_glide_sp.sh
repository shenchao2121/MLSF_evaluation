#!/bin/bash

#path for MSMS 
export PATH=$PATH:/home/shenchao/AI_evaluation/software/deltavina/msms

# set mgltool variable 
export MGL=/opt/mgltools/1.5.6
# set mgltool python 
export MGLPY=$MGL/bin/python 
# set mgl utilities path 
export MGLUTIL=$MGL/MGLToolsPckgs/AutoDockTools/Utilities24/ 

# path for deltevina 
export PATH=/home/shenchao/AI_evaluation/software/deltavina/deltavina-master/bin:$PATH 
# pythonpath for deltevina 
export PYTHONPATH='/home/shenchao/AI_evaluation/software/deltavina/deltavina-master' 

# set vina dir 
export VINADIR=/home/shenchao/AI_evaluation/software/deltavina/vina4dv-master/build/linux/release

module load anaconda2
export PYTHONPATH=${PYTHONPATH}:/opt/openbabel/2.4.1/lib64/python2.7/site-packages
export LD_LIBRARY_PATH=/opt/anaconda2/5.3.0/lib:${LD_LIBRARY_PATH}
module load R
export R_LIBS=/home/shenchao/R_packages:${R_LIBS}
##install.packages('randomForest',"repos" = c(CRAN="https://mirrors.tuna.tsinghua.edu.cn/CRAN/"), lib='/home/shenchao/R_packages')
python deltavina_perform_glide_sp.py




