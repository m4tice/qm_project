from main_scripts import utils
from main_scripts.utils import ref_df, ap_df

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


ap_results, result_keys = utils.get_result_keys(ap_df)
export_csv = True
fs = 15

# 1c: Did all annotators produce the same amount of results, or are there differences?
annotators_list = []
for result_key in result_keys:
    result_amount = len(ap_results[result_key]['results'])
    vendor_user_id = [ap_results[result_key]['results'][i]['user']['vendor_user_id'] for i in range(result_amount)]

    # - Add data to list
    annotators_list.extend(vendor_user_id)

# Count the occurrences of annotators
annotators, annotator_count = np.unique(np.array(annotators_list), return_counts=True)

# Store data in Pandas DataFrame
annotator_result_count_df = pd.DataFrame({"vendor_user_id": annotators, "result_count": annotator_count})

# Visualization
ax = annotator_result_count_df['result_count'].plot(kind='bar')
ax.set_xticklabels(annotator_result_count_df['vendor_user_id'])
ax.grid(True)
ax.set_title("Users result counts", fontsize=fs)
ax.set_xlabel("Annotators", fontsize=fs)
ax.set_ylabel("[count]", fontsize=fs)

ax.axhline(y=annotator_result_count_df["result_count"].mean(), color='r', linestyle='-')   # draw mean line
ax.axhline(y=annotator_result_count_df["result_count"].std(), color='purple', linestyle='-')    # draw std line
ax.legend(["mean", "standard deviation", "count"], prop={'size': fs})

# Add numbers to bars
for p, count in zip(ax.patches, annotator_result_count_df['result_count'].values):
    ax.annotate(str(count), (p.get_x(), p.get_height() + 20))

# Export data to csv file
if export_csv:
    annotator_result_count_df.to_csv("../files/annotator_result_count.csv", index=False)

print(annotator_result_count_df)

plt.show()
