from main_scripts import utils
from main_scripts.utils import ref_df, ap_df

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


ap_results, result_keys = utils.get_result_keys(ap_df)
ref_df, ref_keys = utils.get_img_keys(ref_df)
width = 0.8
fs = 15

# 4: Using the reference set, can you identify good and bad annotators?
# Please use statistics and visualizations.
# Feel free to get creative.


def get_duration_data(result_key, index):
    """
    Get the corresponding duration data based on result_key and index
    :param result_key: key of anonymized_project result
    :param index: index of items in result key
    :return: a list of data
    """
    vendor_user_id = ap_results[result_key]['results'][index]['user']['vendor_user_id']
    duration = ap_results[result_key]['results'][index]['task_output']['duration_ms']
    return [vendor_user_id, duration]


def check_duration_condition(result_key, index, group):
    """
    :param result_key: key of anonymized_project result
    :param index: index of items in result key
    :return: boolean value based on whether the answer data is corrupted and if user is is good annotators list
    """
    cond_1 = ap_results[result_key]['results'][index]['task_output']['corrupt_data']
    cond_2 = ap_results[result_key]['results'][index]['user']['vendor_user_id'] in group
    return not cond_1 and cond_2


# Load data
annotator_result_count_df = pd.read_csv("../files/annotator_result_count.csv")
annotators_quality_df = pd.read_csv("../files/annotators_quality_assessment.csv")


def get_group_data(group, file_name=None):
    """
    Function to retrieve data from a group of selected users
    """
    # Get mean durations
    # - Get durations by user
    annotator_durations = []

    for result_key in result_keys:
        result_amount = len(ap_results[result_key]['results'])

        # Collect durations which are not labeled as corrupted
        row = [get_duration_data(result_key, i) for i in range(result_amount) if check_duration_condition(result_key, i, group)]

        # - Add data to list
        annotator_durations.extend(row)

    annotator_durations_df = pd.DataFrame(data=annotator_durations, columns=['vendor_user_id', 'duration_ms'])

    # - Get mean durations
    selected_annotators_durations = []
    for item in annotator_durations_df.groupby('vendor_user_id'):
        name = item[0]
        temp_df = item[1]['duration_ms']
        temp_df = temp_df.to_frame()
        selected_annotators_durations.append([name, np.asarray(temp_df['duration_ms'], dtype=np.float).mean()])

    selected_annotators_durations_df = pd.DataFrame(selected_annotators_durations, columns=['vendor_user_id', 'mean_duration'])

    # Add sample size column
    result_count_df = annotator_result_count_df.loc[annotator_result_count_df['vendor_user_id'].isin(group)]
    result_count = result_count_df['result_count'].to_list()
    selected_annotators_durations_df['result_count'] = result_count

    # Add correct_percent column
    annotators_quality_percent_df = annotators_quality_df[['vendor_user_id', 'correct_p', 'incorrect_p', 'null_p']]

    correct_percent_df = annotators_quality_percent_df.loc[annotators_quality_percent_df['vendor_user_id'].isin(group)]
    correct_percent = correct_percent_df['correct_p'].to_list()
    selected_annotators_durations_df['correct_p'] = correct_percent

    if file_name is not None:
        selected_annotators_durations_df.to_csv(file_name, index=False)

    return selected_annotators_durations_df


# Specifying good annotators group
good_annotators = ["annotator_13", "annotator_15", "annotator_16", "annotator_17", "annotator_20", "annotator_21"]
print(get_group_data(good_annotators))

# Specifying bad annotators group
print("==" * 50)
bad_annotators = ["annotator_04", "annotator_06", "annotator_08", "annotator_12"]
print(get_group_data(bad_annotators))