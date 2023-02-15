import networkx as nx

def cut_dag(G, inputs):
    #cuts_dict: {"x1":[cut1, cut2, ..], "x2": [], ...}
    cuts_dict = {}
    prev_node = ""
    for n in nx.topological_sort(G):
        cuts_for_node = []
        cuts_dict[n] = []
        left_anc_cuts = []
        right_anc_cuts = []
        anc = G.in_edges(n)
        inputs_amount = len(anc)
        #if the node is input it's cuts list is []
        if inputs_amount == 0:
            continue
        sources = list(zip(*anc))[0]
        counter = 0
        for in_edge in anc:
            if counter == 0:
                list_tmp = []
                list_tmp.append(in_edge)
                left_anc_cuts.append(list_tmp.copy())
                for c in cuts_dict[sources[0]]:
                    left_anc_cuts.append(c)
                counter += 1
            else:
                list_tmp = []
                list_tmp.append(in_edge)
                right_anc_cuts.append(list_tmp.copy())
                for c in cuts_dict[sources[1]]:
                    right_anc_cuts.append(c)
        for l in left_anc_cuts:
            new_cut = l.copy()
            if len(right_anc_cuts) == 0:
                cuts_for_node.append(new_cut)
                continue
            for r in right_anc_cuts:
                new_cut += r.copy()
                if len(new_cut) < 3:
                    cuts_for_node.append(new_cut)
                new_cut = l.copy()
        cuts_dict[n] = cuts_for_node
    print("ALL DICT", cuts_dict)
        
            

        
        

