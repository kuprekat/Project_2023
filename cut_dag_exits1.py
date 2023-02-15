import networkx as nx

class Cut:
    def __init__(self, inputs=None, outputs_amount=1):
        if inputs:
            self.inputs = inputs
        else:
            self.inputs = []
        self.outputs_amount = outputs_amount

    def set_inputs(self, inputs):
        self.inputs = inputs

    def get_inputs(self):
        return self.inputs

    def set_outputs_amount(self, new_amount):
        self.outputs_amount = self.outputs_amount + new_amount - 1

    

def cut_dag(G, inputs):
    #cuts_dict: {"x1":[cut1, cut2, ..], "x2": [], ...}
    cuts_dict = {}
    prev_node = ""
    #for each node
    for n in nx.topological_sort(G):
        cuts_for_node = []
        cuts_dict[n] = []
        left_anc_cuts = []
        right_anc_cuts = []
        anc = G.in_edges(n)
        inputs_amount = len(anc)
        dec = G.out_edges(n)
        outputs_amount = len(dec)
        #if the node is input it's cuts list is []
        if inputs_amount == 0:
            continue
        #all closest ancestors
        sources = list(zip(*anc))[0]
        counter = 0
        for in_edge in anc:
            list_tmp = []
            list_tmp.append(in_edge)
            if counter == 0:
                #left_anc_cuts is list of cuts: left in_edge + all the cuts of left ancestor
                left_anc_cuts.append(list_tmp)
                for c in cuts_dict[sources[counter]]:
                    left_anc_cuts.append(c.get_inputs())
                counter += 1
            else:
                #right_anc_cuts is list of cuts: right in_edge + all the cuts of right ancestor
                right_anc_cuts.append(list_tmp)
                for c in cuts_dict[sources[counter]]:
                    right_anc_cuts.append(c.get_inputs())
        for l in left_anc_cuts:
            new_cut = l.copy()
            if len(right_anc_cuts) == 0:
                cuts_for_node.append(Cut(new_cut))
                continue
            for r in right_anc_cuts:
                new_cut += r.copy()
                if len(new_cut) <= inputs:
                    cuts_for_node.append(Cut(new_cut))
                new_cut = l.copy()
        cuts_dict[n] = cuts_for_node
    for key in cuts_dict.keys():
        for node_cut in cuts_dict[key]:
            print(key, node_cut.get_inputs())

        
            

        
        

