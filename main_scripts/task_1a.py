from main_scripts import utils
from main_scripts.utils import ref_df, ap_df

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


ap_results, result_keys = utils.get_result_keys(ap_df)
export_csv = False

# 1a: How many annotators did contribute to the dataset?
annotators = []
for result_key in result_keys:
    result_amount = len(ap_results[result_key]['results'])
    vendor_user_ids = [ap_results[result_key]['results'][i]['user']['vendor_user_id'] for i in range(result_amount)]

    # - Add data to list
    annotators.extend(vendor_user_ids)

annotators = sorted(set(annotators))
annotators_df = pd.DataFrame({'annotators': annotators})

# Export data to csv file
if export_csv:
    annotators_df.to_csv("../files/annotators.csv")

print(annotators_df)
