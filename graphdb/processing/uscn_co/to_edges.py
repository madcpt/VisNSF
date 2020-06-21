import pandas as pd


export_data = {'Left': list(), 'Right': list()}
f = open('raw/uscn_co_filtered.txt')

for line in f.readlines():
    line = line.strip()
    line = line.split(',')
    export_data['Left'].append(line[1])
    export_data['Right'].append(line[2])
    print(line[1], line[2])

print(len(export_data['Left']))

export_df = pd.DataFrame(data=export_data)
export_df.to_csv('processed/US_Cooperates_CN_edges.csv', index=False)
