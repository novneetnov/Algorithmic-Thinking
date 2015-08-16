import deg_distribution_for_graphs as deg


def test_make_complete_graph():
    num_nodes = 6
    graph = deg.make_complete_graph(num_nodes)
    print graph


def test_compute_in_degrees():
    digraph = deg.EX_GRAPH1
    indeg_dict = deg.compute_in_degrees(digraph)
    print indeg_dict

    digraph = deg.EX_GRAPH2
    indeg_dict = deg.compute_in_degrees(digraph)
    print indeg_dict


def test_in_degree_distribution():
    digraph = deg.EX_GRAPH2
    in_deg_dist = deg.in_degree_distribution(digraph)
    print in_deg_dist

def run():
    #test_make_complete_graph()
    #test_compute_in_degrees()
    test_in_degree_distribution()

run()