from main_scripts import utils
from main_scripts.utils import ref_df, ap_df

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


ap_results, result_keys = utils.get_result_keys(ap_df)
export_csv = True
remove_data_issue = True
fs = 15

# 1b: What are the average, min and max annotation times (durations)?
# Feel free to add visual representations here such as graphs if you like.


def get_duration_data(result_key, index):
    """
    Get the corresponding duration data based on result_key and index
    :param result_key: key of anonymized_project result
    :param index: index of items in result key
    :return: a list of data
    """
    vendor_user_id = ap_results[result_key]['results'][index]['user']['vendor_user_id']
    duration = ap_results[result_key]['results'][index]['task_output']['duration_ms']
    image_url = ap_results[result_key]['results'][0]['task_input']['image_url']
    image_name = image_url.split("/")[-1]
    image_name = image_name.split(".")[0]
    return [vendor_user_id, image_name, duration, image_url]


durations = []
for result_key in result_keys:
    result_amount = len(ap_results[result_key]['results'])

    # Collect durations which are not labeled as corrupted
    rows = [get_duration_data(result_key, i) for i in range(result_amount)
                if not ap_results[result_key]['results'][i]['task_output']['corrupt_data']]

    # - Add data to list
    durations.extend(rows)


# Store data in Pandas DataFrame
durations_df = pd.DataFrame(data=durations, columns=['vendor_user_id', 'image_name', 'duration', 'image_url'])
idxs = np.arange(0, len(durations))
durations_df['idx'] = idxs

# Remove data issue
if remove_data_issue:
    durations_df = durations_df.loc[durations_df['duration'] > 0]

# Export data to csv file
if export_csv:
    durations_df.to_csv("../files/annotation_time.csv", index=False)

print(durations_df['duration'].describe())


# Scatter plot of annotation time
ax1 = durations_df.plot.scatter(x='idx', y='duration')
ax1.axhline(y=durations_df["duration"].mean(), color='r', linestyle='-')    # draw mean line
ax1.set_yticks(list(ax1.get_yticks()) + [durations_df["duration"].mean()])  # add extra tick for mean line
ax1.set_title("Scatter plot of annotation time", fontsize=fs)
ax1.set_xlabel("Samples", fontsize=fs)
ax1.set_ylabel("Duration [ms]", fontsize=fs)
ax1.grid(True)

# Histogram of annotation time
fig2, ax2 = plt.subplots()
ax2 = durations_df['duration'].plot.hist(bins=200)
ax2.set_title("Histogram of annotation time", fontsize=fs)
ax2.set_xlabel("Duration [ms]", fontsize=fs)
ax2.grid(True)

plt.show()
