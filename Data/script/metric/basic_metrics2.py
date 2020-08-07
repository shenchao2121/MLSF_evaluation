#!/usr/bin/env python
# -*- coding: utf-8 -*-

# =============================================================================
# metrics
# =============================================================================

import os, sys, glob, csv
import numpy as np
from scipy.stats import ttest_ind
import pandas as pd
from sklearn.metrics import roc_curve
from sklearn.metrics import auc


def data_prep(act_file, dec_file):
    '''
    preprocess the data, and export three dataframes
    '''
    df_act = pd.read_csv(act_file, header=0, index_col=0)
    df_act.dropna(axis=0, how='any', inplace=True)
    df_dec = pd.read_csv(dec_file, header=0, index_col=0)
    df_dec.dropna(axis=0, how='any', inplace=True)
    df_act['label'] = np.ones([len(df_act)])
    df_dec['label'] = np.zeros([len(df_dec)])
    df_total = pd.concat([df_act, df_dec], axis=0)
    return df_act, df_dec, df_total



def get_auc(df_total, symbol):
    '''
    calculate the AUROC
    '''
    pred = df_total.iloc[:, 0]
    y = df_total.iloc[:, 1]

    if symbol == '+':
        pos_label = 1
    if symbol == '-':
        pos_label = 0
    ##if the prediction_value is + , pos_label=1; else, pos_label=0
    fpr, tpr, thresholds = roc_curve(y, pred, pos_label)
    myauc = auc(fpr, tpr)
    return myauc



def plot_roc_curve(df_total, symbol, outname):
    '''
    plot the ROC curve
    '''
    pred = df_total.iloc[:, 0]
    y = df_total.iloc[:, 1]
    
    if symbol == '+':
        pos_label = 1
    if symbol == '-':
        pos_label = 0
    ##if the prediction_value is + , pos_label=1; else, pos_label=0
    fpr, tpr, thresholds = roc_curve(y, pred, pos_label)
    myauc = auc(fpr, tpr)
    import matplotlib.pyplot as plt
    plt.plot(fpr, tpr, lw=2, label='AUC:%0.3f' % (myauc))
    plt.plot([0, 1], [0, 1], '--', color=(0.6, 0.6, 0.6))
    plt.xlim([-0.05, 1.05])
    plt.ylim([-0.05, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    ##plt.title('Receiver operating characteristic example')  
    plt.legend(loc="lower right")
    # plt.show()
    plt.savefig('%s_roc.png' % outname, format='png', bbox_inches='tight', transparent=True, dpi=600)


def get_auprc(df_total, symbol):
    '''
    calculate the AUC of precision-recall curves (PRC).
    '''
    pred = df_total.iloc[:, 0]
    y = df_total.iloc[:, 1]

    if symbol == '+':
        #pos_label = 1
        pred = pred
    if symbol == '-':
        #pos_label = 0
        pred = -pred
    from sklearn.metrics import precision_recall_curve
    ##if the prediction_value is + , pos_label=1; else, pos_label=0
    #precision, recall, prc_thresh = precision_recall_curve(y, pred, pos_label)
    precision, recall, prc_thresh = precision_recall_curve(y, pred)
    myauprc = auc(recall, precision)
    return myauprc


def plot_prc_curve(df_total, symbol, outname):
    '''
    plot the precision-recall curves (PRC)
    '''
    pred = df_total.iloc[:, 0]
    y = df_total.iloc[:, 1]

    if symbol == '+':
        #pos_label = 1
        pred = pred
    if symbol == '-':
        #pos_label = 0
        pred = -pred
    ##if the prediction_value is + , pos_label=1; else, pos_label=0
    from sklearn.metrics import precision_recall_curve
    ##if the prediction_value is + , pos_label=1; else, pos_label=0
    precision, recall, prc_thresh = precision_recall_curve(y, pred)
    myauprc = auc(recall, precision)
    import matplotlib.pyplot as plt

    plt.plot(recall, precision, lw=2, label='AUPRC:%0.3f' % (myauprc))
    plt.axhline(y=(len(df_total[df_total.iloc[:, 1] == 1])) / (len(df_total)), xmin=0, xmax=1, ls='--',
                color=(0.6, 0.6, 0.6))
    plt.xlim([-0.05, 1.05])
    plt.ylim([-0.05, 1.05])
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    ##plt.title('Receiver operating characteristic example')
    plt.legend(loc="lower right")
    #plt.show()
    plt.savefig('%s_prc.png'%outname, format='png', bbox_inches='tight', transparent=True, dpi=600)


def calc_ef(df_total, symbol, threshold=0.1):
    '''
    calculate the enrichment factor
    '''
    N_total = len(df_total)
    N_actives = len(df_total[df_total.iloc[:, 1] == 1])
    if symbol == '+':
        total_sorted = df_total.sort_values(by=df_total.columns[0], ascending=False)
    if symbol == '-':
        total_sorted = df_total.sort_values(by=df_total.columns[0], ascending=True)
	
    N_topx_total = int(np.ceil(N_total * threshold))
    topx_total = total_sorted.iloc[:N_topx_total, :]
    N_topx_actives = len(topx_total[topx_total.iloc[:, 1] == 1])
	
    return (N_topx_actives / N_topx_total) / (N_actives / N_total)


def plot_enrichment_curve(df_total, symbol, outname):
    '''
    plot the enrichment curve
    Enrichment curve is true positive rate (sensitivity/recall) vs ranking
    or percent of scores above a given threshold. The ratio of recall to
    ranked percentage is the enrichment factor.

    This method is based on scikit-learn's ROC curve implementation.
	'''
    if symbol == '+':
        total_sorted = df_total.sort_values(by=df_total.columns[0], ascending=False)
    if symbol == '-':
        total_sorted = df_total.sort_values(by=df_total.columns[0], ascending=True)

    y_score = total_sorted.iloc[:, 0].values
    y_true = total_sorted.iloc[:, 1].values

    unique_thresh_inds = np.where(np.diff(y_score))[0]
    threshold_inds = np.r_[unique_thresh_inds, y_true.size - 1]

    tps = np.cumsum(y_true)[threshold_inds]

    tpr = tps / tps[-1]
    db_perc = (threshold_inds + 1) / y_true.size
    thresholds = y_score[threshold_inds]

    if len(db_perc) > 2:
        # Remove redundant points, for storage efficiency.
        optimal_idxs = np.where(np.r_[True,
                                      np.logical_or(np.diff(db_perc, 2),
                                                    np.diff(tpr, 2)),
                                      True])[0]
        db_perc = db_perc[optimal_idxs]
        tpr = tpr[optimal_idxs]
        thresholds = thresholds[optimal_idxs]

    if tps.size == 0 or db_perc[0] != 0:
        # Add "0" point
        tpr = np.r_[0, tpr]
        db_perc = np.r_[0, db_perc]
        thresholds = np.r_[thresholds[0] + 1, thresholds]

    import matplotlib.pyplot as plt
    plt.plot(db_perc * 100, tpr, lw=2)
    plt.plot([0, 100], [0, 1], '--', color=(0.6, 0.6, 0.6))
    plt.xlim([-0.05, 100.05])
    plt.ylim([-0.05, 1.05])
    plt.xlabel('Ranked Library (%)')
    plt.ylabel('True Positive Rate')
    ##plt.title('Receiver operating characteristic example')  
    ##plt.legend(loc="lower right")
    # plt.show()
    plt.savefig('%s_enc.png' % outname, format='png', bbox_inches='tight', transparent=True, dpi=600)
    # return db_perc, tpr, thresholds


def get_logroc_curve(df_total, symbol, outname, min_fp=0.001):
    '''
    plot the logROC curve
    '''
    pred0 = df_total.iloc[:, 0]
    y0 = df_total.iloc[:, 1]

    if symbol == '+':
        pos_label = 1
    if symbol == '-':
        pos_label = 0
    ##if the prediction_value is + , pos_label=1; else, pos_label=0
    fp, tp, thresholds = roc_curve(y0, pred0, pos_label)

    lam_index = np.searchsorted(fp, min_fp)
    y = np.asarray(tp[lam_index:], dtype=np.double)
    x = np.asarray(fp[lam_index:], dtype=np.double)
    if (lam_index != 0):
        y = np.insert(y, 0, tp[lam_index - 1])
        x = np.insert(x, 0, min_fp)
	
    fp0 = np.linspace(0, 1)
    tp0 = np.linspace(0, 1)
    lam_index0 = np.searchsorted(fp0, min_fp)    
    y0 = np.asarray(tp0[lam_index0:], dtype=np.double)
    x0 = np.asarray(fp0[lam_index0:], dtype=np.double)
    if (lam_index0 != 0):
        y0 = np.insert(y0, 0, tp0[lam_index0 - 1])
        x0 = np.insert(x0, 0, min_fp)	
	
	
    import matplotlib.pyplot as plt
    plt.plot(x, y, lw=2)
    plt.plot(x0, y0, '--', color=(0.6, 0.6, 0.6))
    plt.xscale("log")
    # plt.xlim([-3.05, 0.05])
    plt.ylim([-0.05, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    ##plt.title('Receiver operating characteristic example')
    ##plt.legend(loc="lower right")
    # plt.show()
    plt.savefig('%s_logroc.png' % outname, format='png', bbox_inches='tight', transparent=True, dpi=600)
    # return np.log10(x), y


def get_logauc(df_total, symbol, min_fp=0.001, adjusted=False):
    """Calculate logAUC, the AUC of the semilog ROC curve.
    `logAUC_lambda` is defined as the AUC of the ROC curve where the x-axis
    is in log space. In effect, this zooms the ROC curve onto the earlier
    portion of the curve where various classifiers will usually be
    differentiated. The adjusted logAUC is the logAUC minus the logAUC of
    a random classifier, resulting in positive values for better-than-random
    and negative otherwise.
    Reference:
        - Mysinger et al. J. Chem. Inf. Model. 2010, 50, 1561-1573.
    """
    pred0 = df_total.iloc[:, 0]
    y0 = df_total.iloc[:, 1]

    if symbol == '+':
        pos_label = 1
    if symbol == '-':
        pos_label = 0
    ##if the prediction_value is + , pos_label=1; else, pos_label=0
    fp, tp, thresholds = roc_curve(y0, pred0, pos_label)

    lam_index = np.searchsorted(fp, min_fp)
    y = np.asarray(tp[lam_index:], dtype=np.double)
    x = np.asarray(fp[lam_index:], dtype=np.double)
    if (lam_index != 0):
        y = np.insert(y, 0, tp[lam_index - 1])
        x = np.insert(x, 0, min_fp)

    dy = (y[1:] - y[:-1])
    with np.errstate(divide='ignore'):
        intercept = y[1:] - x[1:] * (dy / (x[1:] - x[:-1]))
        intercept[np.isinf(intercept)] = 0.
    norm = np.log10(1. / float(min_fp))
    areas = ((dy / np.log(10.)) + intercept * np.log10(x[1:] / x[:-1])) / norm
    logauc = np.sum(areas)
    if adjusted:
        logauc -= 0.144620062  # random curve logAUC
    return logauc


def bedroc_score(df_total, symbol, alpha=20.0):
    """BEDROC metric implemented according to Truchon and Bayley.
    The Boltzmann Enhanced Descrimination of the Receiver Operator
    Characteristic (BEDROC) score is a modification of the Receiver Operator
    Characteristic (ROC) score that allows for a factor of *early recognition*.
    References:
        The original paper by Truchon et al. is located at `10.1021/ci600426e
        <http://dx.doi.org/10.1021/ci600426e>`_.
    Args:
        y_true (array_like):
            Binary class labels. 1 for positive class, 0 otherwise.
        y_pred (array_like):
            Prediction values.
        decreasing (bool):
            True if high values of ``y_pred`` correlates to positive class.
        alpha (float):
            Early recognition parameter.
    Returns:
        float:
            Value in interval [0, 1] indicating degree to which the predictive
            technique employed detects (early) the positive class.
     """
    y_true = df_total.iloc[:, 1]
    y_pred = df_total.iloc[:, 0]
    assert len(y_true) == len(y_pred), \
        'The number of scores must be equal to the number of labels'
    big_n = len(y_true)
    n = sum(y_true == 1)
    if symbol == '+':
        order = np.argsort(-y_pred)
    if symbol == '-':
        order = np.argsort(y_pred)
    m_rank = (y_true[order] == 1).nonzero()[0]
    s = np.sum(np.exp(-alpha * m_rank / big_n))
    r_a = n / big_n
    rand_sum = r_a * (1 - np.exp(-alpha)) / (np.exp(alpha / big_n) - 1)
    fac = r_a * np.sinh(alpha / 2) / (np.cosh(alpha / 2) -
                                      np.cosh(alpha / 2 - alpha * r_a))
    cte = 1 / (1 - np.exp(alpha * (1 - r_a)))
    return s * fac / rand_sum + cte


def main():
    names = [x for x in os.listdir('.') if os.path.isdir(x)]
    #outname = 'parp1'
    act_file = 'parp1/parp1_actives_glide_SP/parp1_actives_SP_score.csv'
    dec_file = 'parp1/parp1_decoys_glide_SP/parp1_decoys_SP_score.csv'
    df_act, df_dec, df_total = data_prep(act_file, dec_file)
    #plot_roc_curve(df_total, '-', outname)
    #plot_prc_curve(df_total, '-', outname)
    #plot_enrichment_curve(df_total, '-', outname)
    get_logroc_curve(df_total, '-', outname, min_fp=0.001)



if __name__ == '__main__':
    main()		


