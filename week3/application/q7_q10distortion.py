import alg_project3_viz
import proj3_solution
import alg_cluster
import matplotlib.pyplot as plt


DATA_URL = alg_project3_viz.DATA_896_URL
DATA_TABLE = alg_project3_viz.load_data_table(DATA_URL)


def compute_distortion(cluster_list):
    """
    Computes the Distortion of a list of clusters clustered by clustering methods.
    """
    total_distortion = 0
    for cluster in cluster_list:
        total_distortion += cluster.cluster_error(DATA_TABLE)
    return total_distortion


def compute_plot(x_list, y1_list, y2_list):
    """
    Plots the Running Time of two functions viz. y_list1 and y_list2
    """
    plt.figure(figsize=(12, 8), dpi = 80)
    plt.plot(x_list, y1_list, '-b', label='hierarchical clustering')
    plt.plot(x_list, y2_list, '-r', label='k-means clustering(5 iterations)')
    plt.xlabel('The number of output clusters')
    plt.ylabel('The distortion produced by the clustering methods')
    plt.title('Comparison of Distortion by two clustering methods on 896 counties')
    plt.legend(loc='upper right', prop={'size': 13.5})
    plt.grid(True)
    plt.show()


def run_example():
    """
    Q-10 of the Application
    """
    singleton_list = []
    for line in DATA_TABLE:
        singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))

    k_means_distortion = []
    for num_clusters in range(6, 21):
        cluster_list = proj3_solution.kmeans_clustering(singleton_list, num_clusters, 5)
        distortion = compute_distortion(cluster_list)
        k_means_distortion.append(distortion)
    print k_means_distortion

    hierarchical_distortion = []
    cluster_list = singleton_list
    for num_clusters in range(20, 5, -1):
        cluster_list = proj3_solution.hierarchical_clustering(cluster_list, num_clusters)
        distortion = compute_distortion(cluster_list)
        hierarchical_distortion.append(distortion)
    hierarchical_distortion.reverse()
    print hierarchical_distortion

    compute_plot(range(6, 21), hierarchical_distortion, k_means_distortion)

run_example()
