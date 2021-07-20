from main_scripts import utils
from main_scripts.utils import ref_df, ap_df

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


ap_results, result_keys = utils.get_result_keys(ap_df)
export_csv = True


annotation_time_df = pd.read_csv("../files/annotation_time.csv")
annotation_time_by_user_df = annotation_time_df.groupby("vendor_user_id")

# Stack data into list
annotation_time_by_user = []
for item in annotation_time_by_user_df:
    annotation_time_by_user.append([item[0], item[1]['duration'].mean(), item[1]['duration'].max(), item[1]['duration'].min()])

annotation_time_by_user_df = pd.DataFrame(data=annotation_time_by_user, columns=['vendor_user_id', 'mean', 'max', 'min'])

# Get types of annotation time
max_user_anno_time = annotation_time_by_user_df['max'].max()
min_user_anno_time = annotation_time_by_user_df['min'].min()
max_user_ave_anno_time = annotation_time_by_user_df['mean'].max()
min_user_ave_anno_time = annotation_time_by_user_df['mean'].min()

# Get users based on annotation time types
user_max_time = annotation_time_by_user_df.loc[annotation_time_by_user_df['max'] == max_user_anno_time]
user_min_time = annotation_time_by_user_df.loc[annotation_time_by_user_df['min'] == min_user_anno_time]
user_max_ave_time = annotation_time_by_user_df.loc[annotation_time_by_user_df['mean'] == max_user_ave_anno_time]
user_min_ave_time = annotation_time_by_user_df.loc[annotation_time_by_user_df['mean'] == min_user_ave_anno_time]

# Display
print("Max annotation time:         %.2f ms - by %s" % (max_user_anno_time, user_max_time['vendor_user_id'].values))
print("Min annotation time:         %.2f ms - by %s" % (min_user_anno_time, user_min_time['vendor_user_id'].values))
print("Max average annotation time: %.2f ms - by %s" % (max_user_ave_anno_time, user_max_ave_time['vendor_user_id'].values))
print("Min average annotation time: %.2f ms - by %s" % (min_user_ave_anno_time, user_min_ave_time['vendor_user_id'].values))

# Export data to csv file
if export_csv:
    annotation_time_by_user_df.to_csv("../files/annotation_time_by_user.csv", index=False)

print(annotation_time_by_user_df)
