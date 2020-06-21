import pandas as pd
import numpy as np


import_df = pd.read_csv('processed/CN_Cooperates_CN_edges.csv')
unique_authors = pd.concat([import_df['Left'], import_df['Right']]).unique()
print(unique_authors.shape)
export_data = {'author_id': list(unique_authors)}
export_df = pd.DataFrame(data=export_data)
export_df.to_csv('processed/CN.csv', index=False)