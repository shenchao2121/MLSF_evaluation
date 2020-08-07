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
#export PATH=/home/shenchao/AI_evaluation/software/deltavina/deltavina-master/bin:$PATH 
# pythonpath for deltevina 
#export PYTHONPATH='/home/shenchao/AI_evaluation/software/deltavina/deltavina-master' 

# set vina dir 
export VINADIR=/home/shenchao/AI_evaluation/software/deltavina/vina4dv-master/build/linux/release



##conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
##conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge
##conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/msys2/
##conda config --set show_channel_urls yes
##conda install -c openbabel openbabel --prefix=/home/shenchao/python_module3.6
##modify /home/shenchao/python_module3.6/lib/python3.6/site-packages/openbabel/pybel.py
### #from . import openbabel as ob  ->  import openbabel as ob

module purge
export PYTHONPATH=/home/shenchao/python_module3.6/lib/python3.6/site-packages/openbabel:/home/shenchao/python_module3.6/lib/python3.6/site-packages:/opt/anaconda3/5.2.0/lib/python3.6/site-packages
module load anaconda3/5.2.0
export PATH=/home/shenchao/python_module3.6/bin:${PATH}

export PYTHONPATH=/home/shenchao/AI_evaluation/software/deltaVinaXGB/build/lib:${PYTHONPATH}
#module load R
#export R_LIBS=/home/shenchao/R_packages:${R_LIBS}
##install.packages('randomForest',"repos" = c(CRAN="https://mirrors.tuna.tsinghua.edu.cn/CRAN/"), lib='/home/shenchao/R_packages')

#python /home/shenchao/AI_evaluation/software/deltaVinaXGB/build/lib/DXGB/run_DXGB.py --modeldir /home/shenchao/AI_evaluation/software/deltaVinaXGB/Model --runfeatures --datadir 4g3e/ --pdbid 4g3e --average
python deltaXGB_perform_ledock.py

















