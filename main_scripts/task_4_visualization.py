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


def percent_cal(item):
    """
    Function for calculating the percentage values
    :param item:
    :return: percentage values
    """
    idx, correct, incorrect, null, total = item
    correct_percent = round(correct / total * 100, 2)
    incorrect_percent = round(incorrect / total * 100, 2)
    null_percent = round(null / total * 100, 2)

    return [idx, correct_percent, incorrect_percent, null_percent]


# Load data
annotators_quality_df = pd.read_csv("../files/annotators_quality_assessment.csv")
annotators_quality = annotators_quality_df.values.tolist()


# Amount display
labels = annotators_quality_df['id']
display_df = annotators_quality_df[['correct', 'incorrect', 'null']]
ax1 = display_df.plot(kind='bar', stacked=True, use_index=False)
ax1.set_xticklabels(labels)
ax1.grid(True)
ax1.set_title("Annotators assessment", fontsize=fs)
ax1.set_xlabel("Annotators", fontsize=fs)
ax1.set_ylabel("[count]", fontsize=fs)
ax1.legend(prop={'size': fs})


# Percentage display
percent_data = np.array([percent_cal(item) for item in annotators_quality])
correct_p = [item for item in percent_data[:, 1]]
incorrect_p = [item for item in percent_data[:, 2]]
null_p = [item for item in percent_data[:, 3]]

df = pd.DataFrame({'correct %': correct_p, 'incorrect %': incorrect_p, 'null %': null_p})
ax2 = df.plot(kind='bar', stacked=True, use_index=False)
ax2.set_xticklabels(labels)
ax2.grid(True)
ax2.set_title("Annotators assessment in percentage", fontsize=fs)
ax2.set_xlabel("Annotators", fontsize=fs)
ax2.set_ylabel("[%]", fontsize=fs)
ax2.legend(prop={'size': fs})

plt.show()
