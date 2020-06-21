import pandas as pd
import numpy as np

import_df = pd.read_csv('xxx.csv')
unique_authors = pd.concat([import_df['Left'], import_df['Right']]).unique()
print(unique_authors.shape)
export_data = {'author_id': list(unique_authors)}
export_df = pd.DataFrame(data=export_data)
export_df.to_csv('US_author.csv', index=False)