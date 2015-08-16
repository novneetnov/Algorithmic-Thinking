# http://www.codeskulptor.org/#user40_r7oIHXVwGg_1.py
"""
The BFS-visited algorithm returns a set of neighbours of the source node, i.
The CC-visited algorithm returns a set of connected components of the undirected graph G.
The resilience of a graph is computed by attacking(deleting) nodes.
"""
from collections import deque


def bfs_visited(ugraph, start_node):
    """
    Takes the undirected graph ugraph and the node start_node
    and returns the set consisting of all nodes that are visited
    by a breadth-first search that starts at start_node
    """
    visited = set([start_node])
    queue = deque([start_node])
    while len(queue) > 0:
        this_node = queue.pop()
        neighbours = list(ugraph[this_node])
        for nbr in neighbours:
            set_nb = set([nbr])
            if not set_nb.issubset(visited):
                visited = visited.union(set_nb)
                queue.append(nbr)
    return visited


def cc_visited(ugraph):
    """
    Takes the undirected graph ugraph and returns a list of sets,
    where each set consists of all the nodes in a connected component,
    and there is exactly one set in the list
    for each connected component in ugraph.
    """
    rem_nodes = set(ugraph.keys())
    connected_components = []
    while not not rem_nodes:
        arbitrary_node = list(rem_nodes)[0]
        visited = bfs_visited(ugraph, arbitrary_node)
        connected_components.append(set(visited))
        rem_nodes = rem_nodes.difference(visited)
    return connected_components


def largest_cc_size(ugraph):
    """
    Takes the undirected graph ugraph and
    returns the size (an integer) of the
    largest connected component in ugraph
    """
    if not ugraph:
        return 0
    rem_nodes = set(ugraph.keys())
    max_cc_len = float('-inf')
    while not not rem_nodes:
        arbitrary_node = list(rem_nodes)[0]
        visited = bfs_visited(ugraph, arbitrary_node)
        rem_nodes = rem_nodes.difference(visited)
        if len(visited) > max_cc_len:
            max_cc_len = len(visited)
        if max_cc_len >= len(rem_nodes):
            break
    return int(max_cc_len)


def compute_resilience(ugraph, attack_order):
    """
    Takes the undirected graph ugraph, a list of nodes attack_order and iterates through the nodes in attack_order.
    The function should return a list whose k+1th entry is the size of the
    largest connected component in the graph after the removal of the first k nodes in attack_order.
    The first entry (indexed by zero) is the size of the largest connected component in the original graph.
    """
    resilience = [largest_cc_size(ugraph)]
    for attack_node in attack_order:
        neighbors = ugraph[attack_node]
        if ugraph.has_key(attack_node):
            ugraph.pop(attack_node)
        for neighbor in neighbors:
            ugraph[neighbor].remove(attack_node)
        resilience.append(largest_cc_size(ugraph))
    return resilience


