"""
Question 3 in the Application Module
"""
import alg_upa_trial as upa
import time
import matplotlib.pyplot as plt


def copy_graph(graph):
    """
    Make a copy of a graph
    """
    new_graph = {}
    for node in graph:
        new_graph[node] = set(graph[node])
    return new_graph


def targeted_order(ugraph):
    """
    Compute a targeted attack order consisting
    of nodes of maximal degree

    Returns:
    A list of nodes
    """
    # copy the graph
    new_graph = copy_graph(ugraph)

    order = []
    while len(new_graph) > 0:
        max_degree = -1
        for node in new_graph:
            if len(new_graph[node]) > max_degree:
                max_degree = len(new_graph[node])
                max_degree_node = node

        neighbors = new_graph[max_degree_node]
        new_graph.pop(max_degree_node)
        for neighbor in neighbors:
            new_graph[neighbor].remove(max_degree_node)

        order.append(max_degree_node)
    return order


def fast_targeted_order(ugraph):
    new_graph = copy_graph(ugraph)
    num_nodes = len(new_graph)
    degree_sets = []
    for k in range(num_nodes):
        degree_sets.append(set([]))
    for node in new_graph:
        node_degree = len(new_graph[node])
        degree_sets[node_degree].add(node)
    order = []
    for k in range(num_nodes - 1, -1, -1):
        while degree_sets[k]:
            remove_node = degree_sets[k].pop()
            neighbors = new_graph[remove_node]
            for neighbor in neighbors:
                d = len(new_graph[neighbor])
                degree_sets[d].remove(neighbor)
                degree_sets[d - 1].add(neighbor)
                new_graph[neighbor].remove(remove_node)
            new_graph.pop(remove_node)
            order.append(remove_node)
    return order


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


def compute_plot(x, y1, y2):
    plt.figure(figsize=(12, 8), dpi = 80)
    plt.plot(x, y1, '-b', label='Targeted order')
    plt.plot(x, y2, '-r', label='Fast Targeted order')
    plt.xlabel('Total number of nodes of UPA graph with m = 5')
    plt.ylabel('Running time in seconds')
    plt.title('Running time growth (Implemented with Desktop Python 2.7)')
    plt.legend(loc='upper right', prop={'size': 10.5})
    plt.grid(True)
    plt.show()


def run_example():
    exact_m = 5
    x_num_nodes = []
    y_targeted = []
    y_fast_targeted = []
    for num_nodes in range(10, 1000, 10):
        x_num_nodes.append(num_nodes)
        upa_graph = load_upa_graph(num_nodes, exact_m)
        time1 = time.time()
        t_order = targeted_order(upa_graph)
        time2 = time.time()
        y_targeted.append(time2 - time1)
        ft_order = fast_targeted_order(upa_graph)
        time3 = time.time()
        y_fast_targeted.append(time3 - time2)

    compute_plot(x_num_nodes, y_targeted, y_fast_targeted)

run_example()



