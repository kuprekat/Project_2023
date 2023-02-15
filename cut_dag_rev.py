import networkx as nx

class Cut:
    def __init__(self, inputs=None, outputs=None):
        self.inputs = []
        if inputs:
            for edge in inputs:
                self.inputs.append(edge)
        self.outputs = []
        if outputs:
            for edge in outputs:
                self.outputs.append(edge)
        self.outputs_amount = len(self.outputs)

    def get_inputs(self):
        return self.inputs

    def get_outputs(self):
        return self.outputs

    def get_outputs_amount(self, new_amount):
        return get.outputs_amount

    

def cut_dag(H, inputs):
    #cuts_dict: {"x1":[cut1, cut2, ..], "x2": [], ...}
    cuts_dict = {}
    G = H.reverse()
    prev_node = ""
    #for each node
    for n in nx.topological_sort(G):
        cuts_for_node = []
        cuts_dict[n] = []
        left_anc_cuts = []
        right_anc_cuts = []
        anc = G.in_edges(n)
        inputs_amount = len(anc)
        dec = list(G.out_edges(n))
        outputs_amount = len(dec)
        #if the node is input it's cuts list is []
        if inputs_amount == 0:
            continue
        #all closest ancestors
        sources = list(zip(*anc))[0]
        counter = 0
        for in_edge in anc:
            if counter == 0:
                #left_anc_cuts is list of cuts: left in_edge + all the cuts of left ancestor
                list_tmp = [in_edge]
                left_anc_cuts.append(Cut(list_tmp))
                left_anc_cuts += cuts_dict[sources[counter]]
                left_edge = in_edge
                counter += 1
            else:
                #right_anc_cuts is list of cuts: right in_edge + all the cuts of right ancestor
                right_anc_cuts.append(Cut(list_tmp))
                right_anc_cuts += cuts_dict[sources[counter]]
                right_edge = in_edge
        for prev_cut_l in left_anc_cuts:
            new_cut_outputs = prev_cut_l.get_outputs().copy()
            if left_edge in new_cut_outputs:
                new_cut_outputs.remove(left_edge)
            new_cut = prev_cut_l.get_inputs().copy()
            if len(right_anc_cuts) == 0:
                cuts_for_node.append(Cut(new_cut, new_cut_outputs + dec))
                continue
            for prev_cut_r in right_anc_cuts:
                new_cut_outputs += prev_cut_r.get_outputs().copy()
                if right_edge in new_cut_outputs:
                    new_cut_outputs.remove(right_edge)
                new_cut += prev_cut_r.get_inputs().copy()
                out_check = len(new_cut_outputs) + 1
                if (len(new_cut) <= inputs) and (out_check < 3):
                    cuts_for_node.append(Cut(new_cut, new_cut_outputs + dec))
                new_cut_outputs = prev_cut_l.get_outputs().copy()
                if left_edge in new_cut_outputs:
                    new_cut_outputs.remove(left_edge)
                new_cut = prev_cut_l.get_inputs().copy()
        cuts_dict[n] = cuts_for_node
    for key in cuts_dict.keys():
        for node_cut in cuts_dict[key]:
            print(key, node_cut.get_inputs(), node_cut.get_outputs())

        
            

        
        

        
            

        
        

