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


# Load data
annotator_result_count_df = pd.read_csv("../files/annotator_result_count.csv")
annotators_quality_df = pd.read_csv("../files/annotators_quality_assessment.csv")
annotators_quality = annotators_quality_df.values.tolist()


# Amount display
labels = annotators_quality_df['vendor_user_id']
display_df = annotators_quality_df[['correct', 'incorrect', 'null']]
ax1 = display_df.plot(kind='bar', stacked=True, use_index=False)
ax1.set_xticklabels(labels)
ax1.grid(True)
ax1.set_title("Annotators assessment", fontsize=fs)
ax1.set_xlabel("Annotators", fontsize=fs)
ax1.set_ylabel("[count]", fontsize=fs)
ax1.legend(prop={'size': fs})
ax1.axhline(y=annotator_result_count_df.mean().values, color='r', linestyle='-')
ax1.axhline(y=annotator_result_count_df.std().values, color='purple', linestyle='-')
ax1.legend(['mean', 'standard_deviation', 'correct', 'incorrect', 'null'])

# - Add numbers to bars
for p, correct_count, incorrect_count in zip(ax1.patches, annotators_quality_df['correct'].values, annotators_quality_df['incorrect'].values):
    ax1.annotate(str(correct_count), (p.get_x(), p.get_height() + 10), fontsize=12)
    ax1.annotate(str(incorrect_count), (p.get_x(), p.get_height() + incorrect_count + 150), fontsize=12)


# Percentage display
ax2 = annotators_quality_df[['correct_p', 'incorrect_p', 'null_p']].plot(kind='bar', stacked=True, use_index=False)
ax2.set_ylim([85, 102])
ax2.set_xticklabels(labels)
ax2.grid(True)
ax2.set_title("Annotators assessment in percentage", fontsize=fs)
ax2.set_xlabel("Annotators", fontsize=fs)
ax2.set_ylabel("[%]", fontsize=fs)
ax2.axhline(y=annotators_quality_df['correct_p'].mean(), color='r', linestyle='-')   # draw mean line
ax2.legend(['mean', 'correct', 'incorrect', 'null'], prop={'size': 12})

# - Add numbers to bars
for p, correct_p, incorrect_p in zip(ax2.patches, annotators_quality_df['correct_p'].values, annotators_quality_df['incorrect_p'].values):
    ax2.annotate(str(round(correct_p, 2)), (p.get_x(), 88))
    ax2.annotate(str(round(incorrect_p, 2)), (p.get_x(), 97))


# Pie chart of average correct, incorrect and null samples
pie_labels = 'correct', 'incorrect', 'null'
pie_values = [annotators_quality_df['correct_p'].mean(),
              annotators_quality_df['incorrect_p'].mean(),
              annotators_quality_df['null_p'].mean()]

explode = (0, 0, 0.1)

fig3, ax3 = plt.subplots()
ax3.pie(pie_values, explode=explode, autopct='%1.3f%%', startangle=90, textprops={'fontsize': 14})
ax3.axis('equal')
ax3.set_title("Overall performance of all annotators", fontsize=fs)
ax3.legend(pie_labels, prop={'size': fs})

print(annotators_quality_df['correct_p'].describe())

plt.show()
