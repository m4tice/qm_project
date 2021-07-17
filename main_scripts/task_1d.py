from main_scripts import utils
from main_scripts.utils import ref_df, ap_df

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


ap_results, result_keys = utils.get_result_keys(ap_df)
export_csv = False

# 1d: Are there questions for which annotators highly disagree?
disagree_limit = 2
highly_disagree_questions = []

for result_key in result_keys:
    result_amount = len(ap_results[result_key]['results'])
    answers = [ap_results[result_key]['results'][i]['task_output']['answer'] for i in range(result_amount)]
    solves = [ap_results[result_key]['results'][i]['task_output']['cant_solve'] for i in range(result_amount)]
    corrupts = [ap_results[result_key]['results'][i]['task_output']['corrupt_data'] for i in range(result_amount)]

    cant_solve = solves.count(True)
    corrupt_amount = corrupts.count(True)
    ans_yes = answers.count('yes')
    ans_no = answers.count('no')

    cond = ans_yes > disagree_limit and ans_no > disagree_limit

    # - Add data to list
    if cond:
        highly_disagree_questions.append([result_key, ans_yes, ans_no, cant_solve, corrupt_amount])

highly_disagree_questions = np.array(highly_disagree_questions)
highly_disagree_questions_df = pd.DataFrame({"result_key": highly_disagree_questions[:, 0],
                                             "yes": highly_disagree_questions[:, 1],
                                             "no": highly_disagree_questions[:, 2],
                                             "cant_solve": highly_disagree_questions[:, 3],
                                             "corrupt_data": highly_disagree_questions[:, 4]})

# Export data to csv file
if export_csv:
    highly_disagree_questions_df.to_csv("../files/highly_disagree_questions.csv")

print(highly_disagree_questions_df)
