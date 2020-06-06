import networkx as nx
import pandas as pd
import json


def generate_gexf_from_csv(csv_file, gexf_file, num_co_limit):
    df = pd.read_csv(csv_file)
    cooperations = set()
    graph = nx.Graph()

    for item in df['co_data']:    
        json_dict = json.loads(item)
        participants = json_dict['participants']

        print("Handling group {}, which contains {} participants".format(json_dict['ratifyNo'], len(participants)))

        for i in range(len(participants) - 1):
            for j in range(i, len(participants)):
                cooperation = participants[i][0], participants[j][0]
                
                if cooperation not in cooperations and (cooperation[1], cooperation[0]) not in cooperations:
                    cooperations.add(cooperation)
        
        if (len(cooperations) > num_co_limit):
            break

    print("{} cooperations are found".format(len(cooperations)))

    graph.add_edges_from(list(cooperations))
    nx.write_gexf(graph, gexf_file)


if __name__ == "__main__":
    csv_file = "cn_co.csv"
    gexf_file = "test.gexf"
    num_co_limit = 100000

    generate_gexf_from_csv(csv_file, gexf_file, num_co_limit)