import networkx as nx

def set_node_types(G):
    for n in nx.topological_sort(G):
        anc = G.in_edges(n)
        inputs_amount = len(anc)
        if inputs_amount == 0:
            G.nodes[n]["ntype"] = "input"
        if inputs_amount == 1:
            G.nodes[n]["ntype"] = "not"
        if inputs_amount == 2:
            G.nodes[n]["ntype"] = "and"

def init_func(G, inputs):
    for n in nx.topological_sort(G):               
        G.nodes[n]["func"] = [0]*pow(2, inputs)
        
def set_func(G, inputs):
    inp_count = 0
    for n in nx.topological_sort(G):
        if G.nodes[n]["ntype"] == "input":
            for i in range(pow(2, inputs)):
                G.nodes[n]["func"][i] = i >> inp_count & 1
            inp_count += 1     
        if G.nodes[n]["ntype"] == "not":
            anc = G.in_edges(n)
            sources = list(zip(*anc))[0]
            pred_func = G.nodes[sources[0]]["func"]
            func = list(map(lambda x: 1 - x, pred_func))
            G.nodes[n]["func"] = func
        if G.nodes[n]["ntype"] == "and":
            anc = G.in_edges(n)
            sources = list(zip(*anc))[0]
            left_func = G.nodes[sources[0]]["func"]
            right_func = G.nodes[sources[1]]["func"]
            func = list(map(lambda x, y: x & y, left_func, right_func))
            G.nodes[n]["func"] = func
