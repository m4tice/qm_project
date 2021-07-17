from main_scripts import utils
from main_scripts.utils import ref_df, ap_df

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


ap_results, result_keys = utils.get_result_keys(ap_df)
fs = 15

# 1b: What are the average, min and max annotation times (durations)?
# Feel free to add visual representations here such as graphs if you like.
durations = []
for result_key in result_keys:
    result_amount = len(ap_results[result_key]['results'])
    duration = [ap_results[result_key]['results'][i]['task_output']['duration_ms'] for i in range(result_amount)]

    # - Add data to list
    durations.extend(duration)

min_duration = min(durations)
max_duration = max(durations)
print("Max duration: {} [ms]\nMin duration: {} [ms]".format(max_duration, min_duration))


# Histogram of annotation time
fig1, ax1 = plt.subplots()
ax1.hist(durations, bins=2000)
ax1.set_title("Histogram of annotation time", fontsize=fs)
ax1.set_xlabel("Annotation times [ms]", fontsize=fs)
ax1.set_ylabel("[count]", fontsize=fs)
ax1.grid(True)


# Scatter plot of annotation time
xs = np.arange(0, len(durations))
fig2, ax2 = plt.subplots()
ax2.scatter(xs, durations)
ax2.set_title("Scatter plot of annotation time", fontsize=fs)
ax2.set_xlabel("Samples", fontsize=fs)
ax2.set_ylabel("Duration time [ms]", fontsize=fs)
ax2.grid(True)

plt.show()
