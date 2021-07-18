from main_scripts import utils
from main_scripts.utils import ref_df, ap_df

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


ap_results, result_keys = utils.get_result_keys(ap_df)
export_csv = False
fs = 15

# 1d: Are there questions for which annotators highly disagree?
question_answers = []

for result_key in result_keys:
    result_amount = len(ap_results[result_key]['results'])
    answers = [ap_results[result_key]['results'][i]['task_output']['answer'] for i in range(result_amount)]
    solves = [ap_results[result_key]['results'][i]['task_output']['cant_solve'] for i in range(result_amount)]
    corrupts = [ap_results[result_key]['results'][i]['task_output']['corrupt_data'] for i in range(result_amount)]

    cant_solve = solves.count(True)
    corrupt_amount = corrupts.count(True)
    ans_yes = answers.count('yes')
    ans_no = answers.count('no')

    # - Add data to list
    question_answers.append([result_key, ans_yes, ans_no, cant_solve, corrupt_amount])

question_answers = np.array(question_answers)
question_answers_df = pd.DataFrame({"result_key": question_answers[:, 0],
                                    "yes": question_answers[:, 1],
                                    "no": question_answers[:, 2],
                                    "cant_solve": question_answers[:, 3],
                                    "corrupt_data": question_answers[:, 4]})


# Visualization
cs = plt.get_cmap('tab20')

# Group questions based on difference
question_answers_grouped = question_answers_df.groupby('yes')
total_answer = len(question_answers)

question_groups = [[int(item[0]), len(item[1])] for item in question_answers_grouped]
question_groups = [["{}-{}".format(item[0], 10 - item[0]), item[1], round(item[1] / total_answer * 100, 2)]
                   for item in sorted(question_groups)]
question_groups = np.array(question_groups)

question_groups_df = pd.DataFrame({"yes-no": question_groups[:, 0],
                                   "count": question_groups[:, 1],
                                   "percent": question_groups[:, 2]})

question_groups_df = question_groups_df.astype({'count': int, 'percent': float})
ax = question_groups_df.plot.pie(y='percent', autopct='%.2f', colormap=cs, labels=None)
ax.set_title("Questions grouped based on yes-no count percentage", fontsize=fs)
ax.legend(question_groups_df['yes-no'], prop={'size': fs})


# Export data to csv file
if export_csv:
    question_answers_df.to_csv("../files/question_answers.csv")
    question_groups_df.to_csv("../files/question_groups.csv")

print(question_groups_df)

plt.show()
