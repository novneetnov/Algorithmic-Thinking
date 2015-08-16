"""
DPA Algorithm
"""
import random
import matplotlib.pyplot as plt


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


def dpa_algorithm(num_nodes, m):
    sub_digraph = make_complete_graph(m)
    node_numbers = [node for node in range(m) for dummy_idx in range(m)]
    for i in range(m, num_nodes):
        total_in_degree = 0
        for node in sub_digraph:
            total_in_degree += len(sub_digraph[node])
        random_node_set = set([])
        for dummy_idx in range(m):
            random_node_set.add(random.choice(node_numbers))
        sub_digraph[i] = random_node_set
        node_numbers.append(i)
        node_numbers.extend(list(random_node_set))
    return sub_digraph


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


def normalize_in_deg_dist(in_deg_dist, total_nodes):
    norm_in_deg_graph = {}
    for elem in in_deg_dist:
        norm_in_deg_graph[elem] = float(in_deg_dist[elem]) / total_nodes
    return norm_in_deg_graph


def draw_loglog_plot(dict_graph):
    if dict_graph.has_key(0):
        dict_graph.pop(0)
    x = dict_graph.keys()
    y = dict_graph.values()
    plt.figure(figsize=(10, 8), dpi = 80)
    plt.loglog(x, y, basex=2, basey=2)
    plt.grid(True)
    plt.xlabel('Log value of value of in-degree')
    plt.ylabel('Log value of number of nodes')
    plt.title('LogLog plot of the normalized in-degree distribution of the dpa graph')
    plt.show()


def total_edges(digraph):
    edges = 0
    for node in digraph:
        edges += len(digraph[node])
    return edges


def run_example():
    dpa_graph = dpa_algorithm(27770, 13)
    #print dpa_graph
    #print total_edges(dpa_graph)
    in_deg_graph = in_degree_distribution(dpa_graph)
    print in_deg_graph
    in_deg_norm = normalize_in_deg_dist(in_deg_graph, len(dpa_graph))
    print in_deg_norm
    draw_loglog_plot(in_deg_norm)

run_example()
