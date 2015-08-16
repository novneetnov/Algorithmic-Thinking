import alg_application2_provided as alg2
import undirected_er_algo as er
import alg_upa_trial as upa
import cc_and_graph_resilience as cc_gr
import math
import random
import matplotlib.pyplot as plt


def load_network_graph():
    graph_url = '/home/novneet/PycharmProjects/AlgoThinking1/week2/application/res/alg_rf7.txt'
    network_graph = alg2.load_graph(graph_url)
    return network_graph


def load_er_graph(num_nodes, prob_edge):
    er_graph = er.er_algorithm(num_nodes, prob_edge)
    return er_graph


def make_complete_graph(num_nodes):
    """
    Returns a complete graph with the given number of nodes
    """
    node_list = [node for node in range(num_nodes)]
    ugraph = {}
    if num_nodes > 0:
        for node in node_list:
            ugraph[node] = set([])
            edge_list = list(node_list)
            edge_list.remove(node)
            for edge in edge_list:
                ugraph[node].add(edge)
    return ugraph


def load_upa_graph(total_nodes, m):
    upa_graph = make_complete_graph(m)
    upa_trial = upa.UPATrial(m)
    for node in range(m, total_nodes):
        upa_graph[node] = upa_trial.run_trial(m)
        neighbors = upa_graph[node]
        for neighbor in neighbors:
            upa_graph[neighbor].add(node)
    return upa_graph


def random_order(ugraph):
    ugraph_nodes = ugraph.keys()
    random.shuffle(ugraph_nodes)
    return ugraph_nodes


def compute_resilience_plot(resilience_lists):
    x = [idx for idx in range(max([len(res) for res in resilience_lists]))]
    y1 = resilience_lists[0]
    y2 = resilience_lists[1]
    y3 = resilience_lists[2]
    plt.figure(figsize=(12, 8), dpi = 80)
    plt.plot(x, y1, '-b', label='Network Graph')
    plt.plot(x, y2, '-r', label='ER Graph, prob_edge = 0.00397')
    plt.plot(x, y3, '-y', label='UPA Graph, m = 2')
    plt.xlabel('Number of nodes removed')
    plt.ylabel('Size of the largest connected component')
    plt.title('Resilience of the Graphs resulting from the node removal')
    plt.legend(loc='upper right', prop={'size': 10.5})
    plt.grid(True)
    plt.show()


def run_example():
    network_graph = load_network_graph()
    num_nodes = len(network_graph)
    print "Total number of nodes in Network Graph : ", num_nodes
    total_edges = 0
    for node in network_graph:
        edge = network_graph[node]
        total_edges += len(edge)
    total_edges /= 2
    print "Total number of edges in Network Graph : ", total_edges

    prob_edge = float((total_edges * 2)) / (num_nodes * (num_nodes - 1))
    er_graph = load_er_graph(num_nodes, prob_edge)
    print "Total number of nodes in ER Graph : ", num_nodes
    total_edges = 0
    for node in er_graph:
        edge = er_graph[node]
        total_edges += len(edge)
    total_edges /= 2
    print "Total number of edges in ER Graph : ", total_edges, " with probability : ", prob_edge

    approx_m = total_edges / num_nodes
    exact_m = int(math.ceil(0.5 * (-math.sqrt(((2 * num_nodes - 1) ** 2) - 8 * total_edges) + (2 * num_nodes - 1))))
    upa_graph = load_upa_graph(num_nodes, approx_m)
    print "Total number of nodes in UPA Graph : ", num_nodes
    total_edges = 0
    for node in upa_graph:
        edge = upa_graph[node]
        total_edges += len(edge)
    total_edges /= 2
    print "Total number of edges in UPA Graph : ", total_edges, " with m : ", approx_m

    attack_network = random_order(network_graph)
    resilience_network = cc_gr.compute_resilience(network_graph, attack_network[:len(attack_network)/5])

    attack_er = random_order(er_graph)
    resilience_er = cc_gr.compute_resilience(er_graph, attack_er[:len(attack_er)/5])

    attack_upa = random_order(upa_graph)
    resilience_upa = cc_gr.compute_resilience(upa_graph, attack_upa[:len(attack_upa)/5])

    print resilience_network[-1], len(network_graph)
    print resilience_er[-1], len(er_graph)
    print resilience_upa[-1], len(upa_graph)



    #compute_resilience_plot([resilience_network, resilience_er, resilience_upa])

run_example()