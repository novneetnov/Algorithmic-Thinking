import random
import time
import matplotlib.pyplot as plt
import proj3_solution as proj3
import alg_cluster


def gen_random_clusters(num_clusters):
    """
    :param num_clusters: The number of clusters required
    :return: A list of randomly generated points as clusters
    in square (+-1, +-1) with size num_clusters
    """
    cluster_list = []
    for idx in range(num_clusters):
        x_coord = 2 * random.random() - 1
        y_coord = 2 * random.random() - 1
        cluster_list.append(alg_cluster.Cluster(set([idx]), x_coord, y_coord, 0, 0))
    return cluster_list


def compute_running_time(func1, func2, input_list):
    """
    Computes and returns the running time of func1 and func2 when run on input_list
    """
    time1 = time.time()
    _ = func1(input_list)
    time2 = time.time()
    _ = func2(input_list)
    time3 = time.time()
    return time2 - time1, time3 - time2


def plot_running_time(x_list, y1_list, y2_list):
    """
    Plots the Running Time of two functions viz. y_list1 and y_list2
    """
    plt.figure(figsize=(12, 8), dpi = 80)
    plt.plot(x_list, y1_list, '-b', label='slow_closest_pair')
    plt.plot(x_list, y2_list, '-r', label='fast_closest_pair')
    plt.xlabel('The number of initial clusters')
    plt.ylabel('The running time of the function in seconds')
    plt.title('Running Time of Two Closest Pair Functions(desktop Python 2.7)')
    plt.legend(loc='upper left', prop={'size': 13.5})
    plt.grid(True)
    plt.show()


def run_example(low, high):
    """
    Runs the Program
    """
    x_list = range(low, high + 1)
    y1_list = []
    y2_list = []
    for idx in x_list:
        input_list = gen_random_clusters(idx)
        input_list.sort(key=lambda cluster: cluster.horiz_center())
        (run_time_1, run_time_2) = compute_running_time(proj3.slow_closest_pair,
                                                        proj3.fast_closest_pair,
                                                        input_list)
        y1_list.append(run_time_1)
        y2_list.append(run_time_2)
    plot_running_time(x_list, y1_list, y2_list)

run_example(2, 200)