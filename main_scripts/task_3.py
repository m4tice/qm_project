from main_scripts import utils
from main_scripts.utils import ref_df, ap_df

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


ref_df, ref_keys = utils.get_img_keys(ref_df)
fs = 12

# 3: Is the reference set balanced? Please demonstrate via numbers and visualizations.

# Get data
ref_ans = [[key, ref_df[key]['is_bicycle']] for key in ref_keys]

# Get unique values and counts
answers, answer_count = np.unique(np.array(ref_ans)[:, 1], return_counts=True)


# Numerics visualization
false_count, true_count = answer_count  # Count number of true and false values
total = true_count + false_count        # Count the total values
diff = abs(true_count - false_count)    # Count the difference between two types

# - Percentage values
true_percent = round(true_count / total * 100, 2)
false_percent = round(false_count / total * 100, 2)
diff_percent = round(diff / total * 100, 2)

print("True samples                 : {} in {} ({}%)".format(true_count, total, true_percent))
print("False samples                : {} in {} ({}%)".format(false_count, total, false_percent))
print("Difference between two counts: {}           ({}%)".format(diff, diff_percent))


# Visualization
# - Display in sample counts
fig1, ax1 = plt.subplots()
rects1 = ax1.bar(["True", "False"], [true_count, false_count], width=0.35)
ax1.set_title("Distribution of reference set", fontsize=fs)
ax1.set_xlabel("Type", fontsize=fs)
ax1.set_ylabel("[count]", fontsize=fs)
ax1.grid(True)
utils.auto_label(rects1, [true_count, false_count], ax1)

# - Display in percentage
fig2, ax2 = plt.subplots()
rects2 = ax2.bar(["True", "False"], [true_percent, false_percent], width=0.35)
ax2.set_title("Distribution of reference set in percentage", fontsize=fs)
ax2.set_xlabel("Type", fontsize=fs)
ax2.set_ylabel("[%]", fontsize=fs)
ax2.grid(True)
utils.auto_label(rects2, [true_percent, false_percent], ax2)

plt.show()
