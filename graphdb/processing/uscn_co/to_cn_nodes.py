import pandas as pd


import_df = pd.read_csv('processed/US_Cooperates_CN_edges.csv')
unique_authors = (import_df['Right']).unique()

print(unique_authors.shape)

export_data = {'author_id': list(unique_authors)}
export_df = pd.DataFrame(data=export_data)
export_df.to_csv('processed/CN.csv', index=False)