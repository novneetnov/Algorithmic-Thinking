"""
Generate a loglog plot of the in-distribution degrees of the citation papers.
"""
import alg_load_graph
import matplotlib.pyplot as plt

graph_url = '/home/novneet/PycharmProjects/AlgoThinking1/week1/application/res/alg_phys-cite.txt'


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
    x = dict_graph.keys()
    y = dict_graph.values()
    if 0 in x:
        x.remove(0)
        y.pop()
    plt.figure(figsize=(10, 8), dpi = 80)
    plt.loglog(x, y, 'ro', basex=2, basey=2)
    plt.grid(True)
    plt.xlabel('Log value of value of in-degree')
    plt.ylabel('Log value of number of nodes')
    plt.title('LogLog plot of the normalized in-degree distribution of the citation graph')
    plt.show()


def run():
    citation_graph = alg_load_graph.load_graph(graph_url)
    in_deg_graph = in_degree_distribution(citation_graph)
    print in_deg_graph
    in_deg_norm = normalize_in_deg_dist(in_deg_graph, len(citation_graph))
    print in_deg_norm
    draw_loglog_plot(in_deg_norm)

run()