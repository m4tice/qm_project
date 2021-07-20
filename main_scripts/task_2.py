from main_scripts import utils
from main_scripts.utils import ref_df, ap_df

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


ap_results, result_keys = utils.get_result_keys(ap_df)
annotator_result_count_df = pd.read_csv("../files/annotator_result_count.csv")
export_csv = True
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
    Get the corresponding data based on result_key and index
    :param result_key: key of anonymized_project result
    :param index: index of items in result key
    :return: a list of data
    """
    vendor_user_id = ap_results[result_key]['results'][index]['user']['vendor_user_id']
    cant_solve = ap_results[result_key]['results'][index]['task_output']['cant_solve']
    corrupt_data = ap_results[result_key]['results'][index]['task_output']['corrupt_data']
    return [vendor_user_id, int(cant_solve), int(corrupt_data)]


def get_user_result_count(user_id):
    """
    Get user's result count based on annotator id id
    :param user_id: annotator id
    :return: user's result count
    """
    annotator_result_count_dict = annotator_result_count_df.set_index('vendor_user_id').to_dict()
    count = annotator_result_count_dict['result_count'][user_id]
    return int(count)


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

    cant_solve_percent = round(cant_solve_count / get_user_result_count(vendor_user_id) * 100, 4)
    corrupt_data_percent = round(corrupt_data_count / get_user_result_count(vendor_user_id) * 100, 4)

    # - Add data to list
    grouped_unsolved_data.append([vendor_user_id, cant_solve_count, corrupt_data_count, cant_solve_percent, corrupt_data_percent])


# Store data in Pandas DataFrame
grouped_unsolved_data_df = pd.DataFrame(data=grouped_unsolved_data,
                                        columns=['vendor_user_id', 'cant_solve', 'corrupt_data', 'cant_solve_percent', 'corrupt_data_percent'])

print(grouped_unsolved_data_df[['vendor_user_id', 'cant_solve_percent', 'corrupt_data_percent']])

# Export data to csv file
if export_csv:
    grouped_unsolved_data_df.to_csv("../files/grouped_unsolved_data.csv", index=False)

# Visualization
display_df = grouped_unsolved_data_df[['cant_solve', 'corrupt_data']].astype(float)
xtick_label = [item.split("_")[1] for item in grouped_unsolved_data_df['vendor_user_id']]

ax = display_df.plot(kind='bar', stacked=True)
ax.set_xticklabels(xtick_label, fontsize=11)
ax.set_title("'cant_solve' and 'corrupt_data' occurrences", fontsize=fs)
ax.set_xlabel("Annotators")
ax.set_ylabel("[count]", fontsize=fs)
ax.grid(True)

plt.show()
