import pandas as pd
from itertools import combinations

import_df = pd.read_csv('cn_cooperations.csv')
grouped = import_df.groupby('grant_id')
export_data = {'Left': list(), 'Right': list()}

for name, group in grouped:
    # print(name)
    participants = group['participant_id'].tolist()

    for comb in combinations(participants, 2):
        print(comb)
        export_data['Left'].append(comb[0])
        export_data['Right'].append(comb[1])

export_df = pd.DataFrame(data=export_data)
export_df.to_csv('out.csv', index=False)