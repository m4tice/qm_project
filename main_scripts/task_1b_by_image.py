from main_scripts import utils
from main_scripts.utils import ref_df, ap_df

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import requests


ap_results, result_keys = utils.get_result_keys(ap_df)
export_csv = True


annotation_time_df = pd.read_csv("../files/annotation_time.csv")
annotation_time_by_image_df = annotation_time_df.groupby("image_name")

# Stack data into list
annotation_time_by_image = []
for item in annotation_time_by_image_df:
    annotation_time_by_image.append([item[0], item[1]['duration'].mean(), item[1]['duration'].max(), item[1]['duration'].min()])

annotation_time_by_image_df = pd.DataFrame(data=annotation_time_by_image, columns=['image_name', 'mean', 'max', 'min'])

# Get types of annotation time
max_image_anno_time = annotation_time_by_image_df['max'].max()
min_image_anno_time = annotation_time_by_image_df['min'].min()
max_image_ave_anno_time = annotation_time_by_image_df['mean'].max()
min_image_ave_anno_time = annotation_time_by_image_df['mean'].min()

# Get images based on annotation time types
image_max_time = annotation_time_by_image_df.loc[annotation_time_by_image_df['max'] == max_image_anno_time]
image_min_time = annotation_time_by_image_df.loc[annotation_time_by_image_df['min'] == min_image_anno_time]
image_max_ave_time = annotation_time_by_image_df.loc[annotation_time_by_image_df['mean'] == max_image_ave_anno_time]
image_min_ave_time = annotation_time_by_image_df.loc[annotation_time_by_image_df['mean'] == min_image_ave_anno_time]

# Display
print("Max annotation time:         %.2f ms - of %s" % (max_image_anno_time, image_max_time['image_name'].values))
print("Min annotation time:         %.2f ms - of %s" % (min_image_anno_time, image_min_time['image_name'].values))
print("Max average annotation time: %.2f ms - of %s" % (max_image_ave_anno_time, image_max_ave_time['image_name'].values))
print("Min average annotation time: %.2f ms - of %s" % (min_image_ave_anno_time, image_min_ave_time['image_name'].values))

# Export data to csv file
if export_csv:
    annotation_time_by_image_df.to_csv("../files/annotation_time_by_image.csv", index=False)

fig, ax = plt.subplots(1, 4)
fig.tight_layout()
images_df = [image_max_time, image_min_time, image_max_ave_time, image_min_ave_time]
titles = ['max', 'min', 'max_ave', 'min_ave']

for idx, item in enumerate(images_df):
    im_url = annotation_time_df.loc[annotation_time_df['image_name'] == item['image_name'].values[0]]
    im_url = im_url['image_url'].values[0]
    im = Image.open(requests.get(im_url, stream=True).raw)
    ax[idx].imshow(im)
    ax[idx].set_title(titles[idx])

print(annotation_time_by_image_df.describe())

plt.show()
