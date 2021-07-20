from main_scripts import utils
from main_scripts.utils import ref_df, ap_df

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


ap_results, result_keys = utils.get_result_keys(ap_df)
ref_df, ref_keys = utils.get_img_keys(ref_df)
export_csv = True


def percent_cal(value, sum):
    """
    Calculate percent value
    """
    return value / sum * 100


# 4: Using the reference set, can you identify good and bad annotators? Please use statistics and visualizations.
# Feel free to get creative.


# Get annotators
annotators = []
for result_key in result_keys:
    result_amount = len(ap_results[result_key]['results'])
    vendor_user_ids = [ap_results[result_key]['results'][i]['user']['vendor_user_id'] for i in range(result_amount)]
    annotators.extend(vendor_user_ids)

annotators = sorted(set(annotators))


# Get reference set
ref_ans = [[key, ref_df[key]['is_bicycle']] for key in ref_keys]


# Get annotators' answers
annotators_ans = []
for result_key in result_keys:
    result_amount = len(ap_results[result_key]['results'])

    # annotators
    vendor_user_ids = [ap_results[result_key]['results'][i]['user']['vendor_user_id'] for i in range(result_amount)]

    # annotators' answers
    answers = [ap_results[result_key]['results'][i]['task_output']['answer'] for i in range(result_amount)]

    # image name
    image_url = ap_results[result_key]['results'][0]['task_input']['image_url']
    image_name = image_url.split("/")[-1]
    image_name = image_name.split(".")[0]

    for idx, ans in zip(vendor_user_ids, answers):
        annotators_ans.append([idx, image_name, ans])


# Group the annotators' answer by annotators
annotators_packages = []
for an_id in annotators:
    temp = [[idx, im_name, ans] for idx, im_name, ans in annotators_ans if an_id == idx]
    annotators_packages.append(temp)


# Count the correct, incorrect and null answers
annotators_quality = []
for annotator_package in annotators_packages:
    # - Initialization of counters
    correct, incorrect, null = 0, 0, 0

    # - Current annotator
    vendor_user_id = annotator_package[0][0]

    # - Looping through each package and count the correct, incorrect and null answer
    for user_id, im_name, user_an in annotator_package:
        # -- Get row index of reference answer
        idx = [i for i, ref in enumerate(ref_ans) if im_name in ref][0]

        # -- Conditions
        correct_cond1 = user_an == 'yes' and ref_ans[idx][1]
        correct_cond2 = user_an == 'no' and not ref_ans[idx][1]
        null_cond = user_an == ""

        # -- Check condition and count
        if correct_cond1 or correct_cond2:
            correct += 1
        elif null_cond:
            null += 1
        else:
            incorrect += 1

    total = correct + incorrect + null

    # - Add data to list
    annotators_quality.append([vendor_user_id, correct, incorrect, null, total,
                               percent_cal(correct, total), percent_cal(incorrect, total), percent_cal(null, total)])

    print(vendor_user_id, correct, incorrect, null, total,
                               percent_cal(correct, total), percent_cal(incorrect, total), percent_cal(null, total))


# Store data in Pandas DataFrame
annotators_quality_df = pd.DataFrame(data=annotators_quality,
                                     columns=['vendor_user_id', 'correct', 'incorrect', 'null', 'total',
                                              'correct_p', 'incorrect_p', 'null_p'])

# Export data to csv file
if export_csv:
    annotators_quality_df.to_csv("../files/annotators_quality_assessment.csv", index=False)


print(annotators_quality_df)
