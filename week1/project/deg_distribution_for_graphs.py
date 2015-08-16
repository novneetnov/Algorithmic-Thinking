#http://www.codeskulptor.org/#user40_EUsDUzjwEH_1.py
"""
Project 1 : Brute Force algorithms to compute 
in-degree distributions
"""

EX_GRAPH0 = {0: set([1, 2]),
             1: set([]),
             2: set([])}

EX_GRAPH1 = {0: set([1, 4, 5]),
             1: set([2, 6]),
             2: set([3]),
             3: set([0]),
             4: set([1]),
             5: set([2]),
             6: set([])}

EX_GRAPH2 = {0: set([1, 4, 5]),
             1: set([2, 6]),
             2: set([3, 7]),
             3: set([7]),
             4: set([1]),
             5: set([2]),
             6: set([]),
             7: set([3]),
             8: set([1, 2]),
             9: set([0, 3, 4, 5, 6, 7])}


def make_complete_graph(num_nodes):
    """
    Returns a complete graph with the given number of nodes
    """
    node_list = [node for node in range(num_nodes)]
    digraph = {}
    if num_nodes > 0:
        for node in node_list:
            digraph[node] = set([])
            edge_list = list(node_list)
            edge_list.remove(node)
            for edge in edge_list:
                digraph[node].add(edge)
    return digraph


def compute_in_degrees(digraph):
    """
    Returns a dictionary with keys corresponding to the
    modes in the input digraph and their values as their
    corresponding input_degrees
    """
    indeg_dict = {}
    for node in digraph:
        indeg_dict[node] = 0
        for adjacent_node in digraph:
            if node != adjacent_node:
                out_deg_nodes_set = digraph[adjacent_node]
                for elem in out_deg_nodes_set:
                    if elem == node:
                        indeg_dict[node] += 1
    return indeg_dict


def in_degree_distribution(digraph):
    """
    Takes a digraph as input and returns a dictionary with
    keys correspond to in-degrees of nodes in the graph.
    The value associated with each particular in-degree is 
    the number of nodes with that in-degree.
    """
    in_deg_dist = {}
    indeg_dict = {}
    for node in digraph:
        indeg_dict[node] = 0
        for adjacent_node in digraph:
            if node != adjacent_node:
                out_deg_nodes_set = digraph[adjacent_node]
                for elem in out_deg_nodes_set:
                    if elem == node:
                        indeg_dict[node] += 1
    for node in indeg_dict:
        num_in_deg = indeg_dict[node]
        if in_deg_dist.has_key(num_in_deg):
            in_deg_dist[num_in_deg] += 1
        else:
            in_deg_dist[num_in_deg] = 1

    return in_deg_dist
