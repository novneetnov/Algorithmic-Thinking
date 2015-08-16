import cc_and_graph_resilience as cc
import example_graphs as graphs


def test_bfs_visited():
    visited = cc.bfs_visited(graphs.GRAPH1, 0)
    print visited


def test_cc_visited():
    connected_component = cc.cc_visited(graphs.GRAPH10)
    print connected_component


def test_largest_cc_size():
    max_cc_length = cc.largest_cc_size(graphs.GRAPH2)
    print max_cc_length


def test_compute_resilience():
    resilience = cc.compute_resilience(graphs.GRAPH2, [1, 3, 5, 7, 2, 4, 6, 8])
    print resilience


def run():
    test_bfs_visited()
    test_cc_visited()
    test_largest_cc_size()
    test_compute_resilience()

run()