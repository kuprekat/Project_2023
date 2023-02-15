def parse_dot(filename):
    renames = {}
    edges = []
    nodes = set()
    invert_flag = 0
    not_counter = 0

    with open(filename) as file:
        lines = [line.rstrip() for line in file]

    for l in lines:
        if len(l) < 1:
            continue
        not_flag = 0
        node_pos = l.find('label')
        if node_pos != -1:
            words = l.split()
            node = words[0]
            name = words[3][1:-2]
            renames[node] = name
            continue
        if (l.find('->') != -1) and (l.find('invis') == -1):
            if l.find('dotted') != -1:
                not_flag = 1
            words = l.split()
            left = words[0]
            right = words[2]
            if right in renames.keys():
                right = renames[right]
            if not not_flag:
                edges.append((right, left))
            else:
                new_node = f"not{not_counter}"
                edges.append((right, new_node))
                edges.append((new_node, left))
                nodes.add(new_node)
                not_counter += 1
            nodes.add(left)
            nodes.add(right)
    return(nodes, edges)





        