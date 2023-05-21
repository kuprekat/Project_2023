import networkx as nx

def add_inputs(G):
    amount = 0
    outputs = 0
    for node in nx.topological_sort(G):
        current_input_amount = len(G.in_edges(node))
        current_output_amount = len(G.out_edges(node))
        inp = 0
        
        if G.nodes[node]["ntype"] == "not":
            inp = 1
        if G.nodes[node]["ntype"] == "and":
            inp = 2
        for i in range(inp - current_input_amount):
            G.add_node(f"x{amount}", ntype="input")
            G.add_edge(f"x{amount}", node)
            amount += 1

        for i in range(G.nodes[node]["out_am"] - current_output_amount):
            G.add_node(f"out{outputs}", ntype="output")
            G.add_edge(node, f"out{outputs}")
            outputs += 1
        
    return amount

def set_node_types(G):
    for n in nx.topological_sort(G):
        anc = G.in_edges(n)
        dec = G.out_edges(n)
        inputs_amount = len(anc)
        outputs_amount = len(dec)
        if inputs_amount == 0:
            G.nodes[n]["ntype"] = "input"
        if inputs_amount == 1:
            G.nodes[n]["ntype"] = "not"
        if inputs_amount == 2:
            G.nodes[n]["ntype"] = "and"
        G.nodes[n]["out_am"] = outputs_amount

def init_func(G, inputs):
    for n in nx.topological_sort(G):               
        G.nodes[n]["func"] = [0]*pow(2, inputs)
        
def set_func(G, inputs):
    inp_count = 0
    func_dict = {}
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
        if G.nodes[n]["ntype"] == "output":
            anc = G.in_edges(n)
            sources = list(zip(*anc))[0]
            func = G.nodes[sources[0]]["func"]
            G.nodes[n]["func"] = func
            func_dict[n] = func
    return func_dict
