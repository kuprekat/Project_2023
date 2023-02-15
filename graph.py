import matplotlib.pyplot as plt
import networkx as nx
from parse_dot import *
from cut_dag_rev import *
from set_func import *

import sys

if len(sys.argv) < 2:
    print("No input file\n")
    exit(1)
filename = sys.argv[1]

edges = []
nodes = set()
nodes, edges = parse_dot(filename)
G = nx.DiGraph()
G.add_nodes_from(nodes, ntype="none")
G.add_edges_from(edges)
set_node_types(G)
init_func(G, 3)
set_func(G, 3)
print(list(G.nodes(data=True)))
cut_dag(G, 3)

subax1 = plt.subplot(121)
nx.draw(G, with_labels=True, font_weight='bold')
plt.show() 
