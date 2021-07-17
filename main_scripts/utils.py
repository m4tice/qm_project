import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


ap_df = pd.read_json('../files/anonymized_project.json')
ref_df = pd.read_json('../files/references.json')


def get_result_keys(df):
    """
    Get dataframe and result_keys
    :param df: input dataframe
    :return: dataframe and result_keys
    """
    ap_results = df.iloc[0][0]['results']
    result_keys = list(ap_results.keys())
    return ap_results, result_keys


def get_img_keys(df):
    """
    Get dataframe and result_keys
    :param df: input dataframe
    :return: dataframe and result_keys
    """
    ref_keys = df.keys()
    return ref_df, ref_keys


def auto_label(rects, values, ax):
    """
    Attach a text label above each bar displaying its height
    """
    for rect, item in zip(rects, values):
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., height,
                '%0.2f' % item,
                ha='center', va='bottom')

