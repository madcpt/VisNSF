import networkx as nx


graph = nx.Graph()
f = open('collaborations_bak.txt')

for line in f.readlines():
    line = line.strip()
    line = line.split(',')
    graph.add_node(line[1], country='US')
    graph.add_node(line[2], country='CN')
    graph.add_edges_from([(line[1], line[2])])
    print(line[1], line[2])

print(graph.number_of_nodes(), graph.number_of_edges())

nx.write_gexf(graph, 'tttttest.gexf')