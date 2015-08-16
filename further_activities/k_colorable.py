"""
Functions to determine if a graph is k-colorable
and its chromatic number.
"""

GRAPH1 = {0: set([1, 2]),
      1: set([0, 2]),
      2: set([0, 1])}

GRAPH2 = {0: set([1, 2, 3]),
      1: set([0, 2, 3]),
      2: set([0, 1, 3]),
      3: set([0, 1, 2])}

GRAPH3 = {0: set([1, 2, 4, 5]),
      1: set([0, 2, 3, 5]),
      2: set([0, 1, 3, 4]),
      3: set([1, 2, 4, 5]),
      4: set([0, 2, 3, 5]),
      5: set([0, 1, 3, 4])}

GRAPH4 = {1: set([2, 8]),
      2: set([1, 3, 4, 6, 8]),
      3: set([2, 4]),
      4: set([2, 3, 5, 6, 8]),
      5: set([4, 6]),
      6: set([2, 4, 5, 7, 8]),
      7: set([6, 8]),
      8: set([1, 2, 4, 6, 7])}


def is_k_colorable(ugraph, k):
    """
    :param ugraph: An undirected graph
    :param k: k colors
    :return: A dictionary with key as node and corresponding value as color if the graph is k-colorable,
             false otherwise
    """

    ans_color = {}
    color_list = range(k)
    for node in ugraph:
        temp_list = []
        neighbours = ugraph[node]
        for neigh in neighbours:
            if neigh in ans_color:
                try:
                    color_list.remove(ans_color[neigh])
                    temp_list.append(ans_color[neigh])
                except ValueError:
                    pass
        if not color_list:
            return False
        ans_color[node] = color_list.pop(0)
        color_list.extend(temp_list)
        color_list.append(ans_color[node])
    return ans_color

#print is_k_colorable(GRAPH1, 3)
#print is_k_colorable(GRAPH2, 3)
#print is_k_colorable(GRAPH3, 4)
print is_k_colorable(GRAPH4, 5)


def is_k_colorable2(ugraph, k):
    """
    :param ugraph: An undirected graph
    :param k: k colors
    :return: A dictionary with key as node and corresponding value as color if the graph is k-colorable,
             false otherwise
    """

    ans_color = {}
    color_list = [0 for _ in range(k)]
    for node in ugraph:
        forbidden_list = []
        neighbours = ugraph[node]
        for neigh in neighbours:
            if neigh in ans_color:
                forbidden_color = ans_color[neigh]
                if forbidden_color not in forbidden_list:
                    forbidden_list.append(forbidden_color)
        if len(forbidden_list) == k:
            return False
        min_color_freq = k + 1
        color = -1
        for idx in range(k):
            if idx not in forbidden_list:
                color_freq = color_list[idx]
                if color_freq < min_color_freq:
                    min_color_freq = color_freq
                    color = idx
        ans_color[node] = color
        color_list[color] += 1
    return ans_color


#print is_k_colorable2(GRAPH1, 3)
#print is_k_colorable2(GRAPH2, 3)
#print is_k_colorable2(GRAPH3, 4)
print is_k_colorable2(GRAPH4, 5)


def compute_chromatic_number(ugraph):
    """
    Returns the chromatic number for the ugraph
    """
    num_nodes = len(ugraph)
    for chromatic_number in range(1, num_nodes + 1):
        if is_k_colorable2(ugraph, chromatic_number):
            return chromatic_number

#print compute_chromatic_number(GRAPH1)
#print compute_chromatic_number(GRAPH2)
#print compute_chromatic_number(GRAPH3)
#print compute_chromatic_number(GRAPH4)


"""
Solution for "Graph coloring" for Further activities

Note that this solution requires itertools and
should be run on desktop Python
"""

import itertools


def has_internal_edge(g, nodeset):
    """
    Check if any pair of nodes in the set nodeset has an
    edge connecting them in g.

    Arguments:
    g -- undirected graph
    nodeset -- subset of nodes in g

    Returns:
    True if there is an edge between any two nodes in nodeset,
    False otherwise.
    """
    for node in nodeset:
        for nbr in g[node]:
            if nbr in nodeset:
                return True
    return False


def is_three_colorable(g):
    """
    Check if g is three colorable.

    Arguments:
    g -- undirected graph

    Returns:
    True if there is a three coloring of g, False otherwise.
    """
    nodes = set(g.keys())

    # Check all subsets of nodes of size 0 to |V| as red set
    for i in range(len(g)+1):
        for red in itertools.combinations(nodes, i):
            red = set(red)

            # Ensure that there are no edges among nodes in red set
            if not has_internal_edge(g, red):
                # Check all subsets of nodes of size 0 to |V|-|red| as green set
                for j in range(len(g)-i+1):
                    for green in itertools.combinations(nodes - red, j):
                        green = set(green)

                        # Ensure that there are no edges among nodes in green set
                        if not has_internal_edge(g, green):
                            # blue set is the remainder of nodes in the graph
                            blue = nodes - red - green

                            # Ensure that there are no edges among nodes in blue set
                            if not has_internal_edge(g, blue):
                                # sets red, green, blue are a three coloring
                                return True

    # There is no three coloring
    return False

def run_example():
    """
    Compute some examples
    """
    print "GRAPH1 is 3 colorable =", is_three_colorable(GRAPH1)
    print "GRAPH2 is 3 colorable =", is_three_colorable(GRAPH2)
    print "GRAPH3 is 3 colorable =", is_three_colorable(GRAPH3)
    print "GRAPH4 is 3 colorable =", is_three_colorable(GRAPH4)

run_example()

