import networkx as nx


f = open('raw/uscn_co_filtered.txt')
# edges = list()
graph = nx.Graph()

for i, line in enumerate(f.readlines()):
    line = line.strip()
    line = line.split(',')
    graph.add_node(i, labelV='US', author_id=line[1])
    graph.add_node(i + 1000000, labelV='CN', author_id=line[2])
    graph.add_edge(i, i + 1000000, labelE='Cooperates')
    # edges.append((line[1], line[2]))

# graph.add_edges_from(edges)
print(graph.number_of_nodes(), graph.number_of_edges())

nx.write_graphml(graph, "planb.xml")