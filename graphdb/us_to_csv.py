import pandas as pd

import_df = pd.read_csv('us_cooperations.csv')
export_set = set()

for index, row in import_df.iterrows():
    print(row['author1_id'], row['author2_id'])
    export_set.add(row['author1_id'])
    export_set.add(row['author2_id'])

export_data = {'author_id': list(export_set)}
export_df = pd.DataFrame(data=export_data)

print(export_df.shape)
export_df.to_csv('US2.csv', index=False)