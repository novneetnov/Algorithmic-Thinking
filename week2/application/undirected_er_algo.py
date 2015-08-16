import random


def er_algorithm(num_nodes, prob_edge):
    """
    Returns a random undirected graph with number of nodes 'num_nodes' and
    the probability of an edge 'prob_edge'
    """
    node_list = [node for node in range(num_nodes)]
    ugraph = {}
    for node_i in range(num_nodes):
        ugraph[node_i] = set([])
    for node_i in range(num_nodes):
        for node_j in range(node_i + 1, num_nodes):
            random_number = random.random()
            if random_number < prob_edge:
                ugraph[node_i].add(node_j)
                ugraph[node_j].add(node_i)
    return ugraph

#print er_algorithm(4, 0.7)