from main_scripts import utils
from main_scripts.utils import ref_df, ap_df

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


ap_results, result_keys = utils.get_result_keys(ap_df)
export_csv = False
fs = 15

# 2a: How often does each occur in the project and
# do you see a trend within the annotators that made use of these options?


def unsolved_check(result_key, index):
    """
    :param result_key: key of anonymized_project result
    :param index: index of items in result key
    :return: boolean value based on whether the answer is cant_solve or the data is corrupted
    """
    cant_solve_cond = ap_results[result_key]['results'][index]['task_output']['cant_solve']
    corrupt_data_cond = ap_results[result_key]['results'][index]['task_output']['corrupt_data']
    return cant_solve_cond or corrupt_data_cond


def get_data(result_key, index):
    """
    Get the corresponded data based on result_key and index
    :param result_key: key of anonymized_project result
    :param index: index of items in result key
    :return: a list of data
    """
    vendor_user_id = ap_results[result_key]['results'][index]['user']['vendor_user_id']
    cant_solve = ap_results[result_key]['results'][index]['task_output']['cant_solve']
    corrupt_data = ap_results[result_key]['results'][index]['task_output']['corrupt_data']
    return [vendor_user_id, int(cant_solve), int(corrupt_data)]


# Gather rows of data with users with 'cant_solve' and 'corrupt_data'
unsolved_data = []

for result_key in result_keys:
    result_amount = len(ap_results[result_key]['results'])
    unsolved = [get_data(result_key, i) for i in range(result_amount) if unsolved_check(result_key, i)]

    # - Add data to list
    unsolved_data.extend(unsolved)


# Get unique user ids
unsolved_user = sorted(set(np.array(unsolved_data)[:, 0]))


# Get the count of 'cant_solve' and 'corrupt_data' for each user and store them in a list
grouped_unsolved_data = []

for vendor_user_id in unsolved_user:
    # - Retrieve the answers of a specific user
    user_result = np.array([item for item in unsolved_data if item[0] == vendor_user_id])

    # - Count the 'cant_solve' and 'corrupt_data' occurrences
    cant_solve_count = np.sum(user_result[:, 1] == '1')
    corrupt_data_count = np.sum(user_result[:, 2] == '1')

    # - Add data to list
    grouped_unsolved_data.append([vendor_user_id, cant_solve_count, corrupt_data_count])


# Store data in Pandas dataframe
grouped_unsolved_data_df = pd.DataFrame({'vendor_user_id': np.array(grouped_unsolved_data)[:, 0],
                                         'cant_solve': np.array(grouped_unsolved_data)[:, 1],
                                         'corrupt_data': np.array(grouped_unsolved_data)[:, 2]})

# Export data to csv file
if export_csv:
    grouped_unsolved_data_df.to_csv("../files/grouped_unsolved_data.csv")

# Visualization
display_df = grouped_unsolved_data_df[['cant_solve', 'corrupt_data']].astype(float)

ax = display_df.plot(kind='bar', stacked=True)
ax.set_xticklabels(grouped_unsolved_data_df['vendor_user_id'])
ax.set_title("'cant_solve' and 'corrupt_data' occurrences", fontsize=fs)
ax.set_xlabel("vendor_user_id")
ax.set_ylabel("[count]", fontsize=fs)
ax.grid(True)

plt.show()
