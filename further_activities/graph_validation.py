def is_undirected_graph_valid(graph):
    """
    Tests whether the given graph is logically valid.

    Asserts for every unordered pair of distinct nodes {n1, n2} that
    if n2 appears in n1's adjacency set then n1 also appears in
    n2's adjacency set.  Also asserts that no node appears in
    its own adjacency set and that every value that appears in
    an adjacency set is a node in the graph.

    Arguments:
    graph -- The graph in dictionary form to test.

    Returns:
    True if the graph is logically valid.  False otherwise.
    """
    nodes = graph.keys()
    for node in nodes:
        neighbours = graph[node]
        if node in neighbours:
            return False
        for neigh in neighbours:
            if node not in graph[neigh]:
                return False
    return True

graph1 = {"0" : set(["1","2"]),
               "1" : set(["0","2"]),
               "2" : set(["1","0"]) }
print is_undirected_graph_valid(graph1)

graph2 = { "0" : set(["1","2"]),
               "1" : set(["0","2"]),
               "2" : set(["1"]) }
print is_undirected_graph_valid(graph2)

graph4 = { "0" : set(["1","2"]),
               "1" : set(["0","2"]),
               "2" : set(["1","3"]) }
print is_undirected_graph_valid(graph4)

graph5 = { "0" : set(["0"]) }
print is_undirected_graph_valid(graph5)

