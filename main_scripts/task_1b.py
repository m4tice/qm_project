from main_scripts import utils
from main_scripts.utils import ref_df, ap_df

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


ap_results, result_keys = utils.get_result_keys(ap_df)
fs = 15
remove_data_issue = True

# 1b: What are the average, min and max annotation times (durations)?
# Feel free to add visual representations here such as graphs if you like.
durations = []
for result_key in result_keys:
    result_amount = len(ap_results[result_key]['results'])

    # Collect durations which are not labeled as corrupted
    duration = [ap_results[result_key]['results'][i]['task_output']['duration_ms'] for i in range(result_amount)
                if not ap_results[result_key]['results'][i]['task_output']['corrupt_data']]

    # - Add data to list
    durations.extend(duration)


# Remove data issue
if remove_data_issue:
    data_issue = [item for item in durations if item < 0]               # Collect outliers that are negative
    durations = [item for item in durations if item not in data_issue]  # Remove outliers


# Store data in Pandas DataFrame
idx = np.arange(0, len(durations))
durations_df = pd.DataFrame({"index": idx, "duration": durations})

durations_df.to_csv("annotation_time.csv", index=False)
print(durations_df['duration'].describe())


# Scatter plot of annotation time
ax1 = durations_df.plot.scatter(x='index', y='duration')
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
