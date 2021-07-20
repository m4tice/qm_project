from main_scripts import utils
from main_scripts.utils import ref_df, ap_df

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


ref_df, ref_keys = utils.get_img_keys(ref_df)
fs = 15

# Get data
ref_ans = [[ref_key, ref_df[ref_key]['is_bicycle']] for ref_key in ref_keys]
ref_ans = np.array(ref_ans)

# Store the collected data in Pandas DataFrame
ref_ans_df = pd.DataFrame({'key': ref_ans[:, 0], 'is_bicycle': ref_ans[:, 1]})
ref_ans_df = ref_ans_df.groupby('is_bicycle').nunique()
ref_ans_df = ref_ans_df.rename(columns={"key": "count"})
ax = ref_ans_df.plot.pie(y='count', autopct='%.2f%%', labels=None)
ax.set_title("Reference set distribution percentage", fontsize=fs)

plt.show()
