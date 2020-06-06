import pandas as pd
import json
from itertools import combinations


def generate_co_from_csv(csv_file):
    df = pd.read_csv(csv_file)
    cooperations = set()
    left = list()
    right = list()

    for item in df['co_data']:    
        json_dict = json.loads(item)
        participants = json_dict['participants']

        print("Handling group {}, which contains {} participants".format(json_dict['ratifyNo'], len(participants)))

        for cooperation in combinations(participants, 2):  
            cooperation = (cooperation[0][0], cooperation[1][0])

            if cooperation not in cooperations and (cooperation[1], cooperation[0]) not in cooperations:
                cooperations.add(cooperation)

                left.append(cooperation[0])
                right.append(cooperation[1])

    print("{} cooperations are found".format(len(cooperations)))

    return left, right


if __name__ == "__main__":
    csv_file = "cn_co_correct.csv"

    left, right = generate_co_from_csv(csv_file)
    print(len(left), len(right))

    df = pd.DataFrame(data={'Left': left, 'Right': right})
    df.to_csv('xxx.csv', index=False)
    