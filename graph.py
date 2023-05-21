import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_agraph import write_dot, graphviz_layout
from parse_dot import *
from cut_dag_exits import *
from process_subgraph import *

import sys

def get_nodes(H, cuts, node):
    #print(list(cuts[node]))
    G = H.copy()
    input_amount = 0
    cut_no = 0
    for cut in cuts[node]:
        input_amount = max(input_amount, cut.get_inputs_amount())
        cut_no += 1
        #print(input_amount, cut_no)
    #print(list(cuts[node]))
    G.remove_edges_from(list(cuts[node])[cut_no - 1].get_inputs())
    G.remove_edges_from(list(cuts[node])[cut_no - 1].get_outputs())
    for c in nx.weakly_connected_components(G):
        S = G.subgraph(c).copy()
        if S.has_node(node):
            print("SELECTED NODES ", S.nodes())
            return list(S.nodes())
        else:
            continue

if len(sys.argv) < 2:
    print("No input file\n")
    exit(1)
filename = sys.argv[1]

edges = []
nodes = set()
nodes, edges = parse_dot(filename)
G = nx.DiGraph()
G.add_nodes_from(nodes, ntype="none", out_am = 0)
G.add_edges_from(edges)
set_node_types(G)
#init_func(G, 3)
#set_func(G, 3)
#print(list(G.nodes(data=True)))
cuts = cut_dag(G, 3, 1)
#print(type(cuts))
sub_nodes = get_nodes(G, cuts, "Node86")
H = G.subgraph(sub_nodes).copy()
inputs_amount = add_inputs(H)
init_func(H, inputs_amount)
func_dict = set_func(H, inputs_amount)
print("RESULT FUCTIONS:")
for key in func_dict.keys():
    print("   ", key, func_dict[key])
print("\n")
for n in list(H.nodes(data=True)):
    print(n)

pos=graphviz_layout(H, prog='dot')
plt.figure(1)
nx.draw(H, pos,with_labels=True, font_weight='bold', arrows=True)
#plt.show()

pos=graphviz_layout(G, prog='dot')
plt.figure(2)
nx.draw(G, pos,with_labels=True, font_weight='bold', arrows=True)
plt.show()

