# http://www.codeskulptor.org/#user40_rBJIfys5YN3zm37.py
"""
Student template code for Project 3
Student will implement five functions:

slow_closest_pair(cluster_list)
fast_closest_pair(cluster_list)
closest_pair_strip(cluster_list, horiz_center, half_width)
hierarchical_clustering(cluster_list, num_clusters)
kmeans_clustering(cluster_list, num_clusters, num_iterations)

where cluster_list is a 2D list of clusters in the plane
"""

import math
import alg_cluster


######################################################
# Code for closest pairs of clusters

def pair_distance(cluster_list, idx1, idx2):
    """
    Helper function that computes Euclidean distance between two clusters in a list

    Input: cluster_list is list of clusters, idx1 and idx2 are integer indices for two clusters
    
    Output: tuple (dist, idx1, idx2) where dist is distance between
    cluster_list[idx1] and cluster_list[idx2]
    """
    return cluster_list[idx1].distance(cluster_list[idx2]), min(idx1, idx2), max(idx1, idx2)


def slow_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (slow)

    Input: cluster_list is the list of clusters
    
    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.       
    """

    closest_pair = (float('inf'), -1, -1)
    num_clusters = len(cluster_list)
    for idx1 in range(num_clusters):
        cluster1 = cluster_list[idx1]
        for idx2 in range(num_clusters):
            cluster2 = cluster_list[idx2]
            if cluster1 != cluster2:
                new_min_dist = cluster1.distance(cluster2)
                closest_pair = closest_pair if closest_pair[0] < new_min_dist \
                    else (new_min_dist, min(idx1, idx2), max(idx1, idx2))
    return closest_pair


def fast_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (fast)

    Input: cluster_list is list of clusters SORTED such that horizontal positions of their
    centers are in ascending order
    
    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.       
    """
    num_clusters = len(cluster_list)
    if num_clusters <= 3:
        return slow_closest_pair(cluster_list)
    cluster_list.sort(key=lambda cluster: cluster.horiz_center())
    half = int(math.floor(num_clusters / 2))
    left_clusters = [cluster_list[idx] for idx in range(half)]
    right_clusters = [cluster_list[idx] for idx in range(half, num_clusters)]
    left_closest_pair = fast_closest_pair(left_clusters)
    right_closest_pair = fast_closest_pair(right_clusters)
    right_closest_pair = (right_closest_pair[0], right_closest_pair[1] + half, right_closest_pair[2] + half)
    closest_pair = left_closest_pair if left_closest_pair[0] < right_closest_pair[0] else right_closest_pair
    mid = float(cluster_list[half - 1].horiz_center() + cluster_list[half].horiz_center()) / 2
    alt_closest_pair = closest_pair_strip(cluster_list, mid, closest_pair[0])
    closest_pair = closest_pair if closest_pair[0] < alt_closest_pair[0] else alt_closest_pair
    return closest_pair


def closest_pair_strip(cluster_list, horiz_center, half_width):
    """
    Helper function to compute the closest pair of clusters in a vertical strip
    
    Input: cluster_list is a list of clusters produced by fast_closest_pair
    horiz_center is the horizontal position of the strip's vertical center line
    half_width is the half the width of the strip (i.e; the maximum horizontal distance
    that a cluster can lie from the center line)

    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] lie in the strip and have minimum distance dist.       
    """
    useful_list = []
    for idx in range(len(cluster_list)):
        cluster = cluster_list[idx]
        if (horiz_center + half_width) > cluster.horiz_center() > (horiz_center - half_width):
            useful_list.append((cluster, idx))
    useful_list.sort(key=lambda cluster_tuple: cluster_tuple[0].vert_center())
    num_clusters = len(useful_list)
    closest_pair = (float('inf'), -1, -1)
    for idx1 in range(num_clusters - 1):
        cluster1 = useful_list[idx1][0]
        for idx2 in range(idx1 + 1, min(idx1 + 4, num_clusters)):
            cluster2 = useful_list[idx2][0]
            new_min_dist = cluster1.distance(cluster2)
            closest_pair = closest_pair if closest_pair[0] < new_min_dist \
                else (new_min_dist,
                      min(useful_list[idx1][1], useful_list[idx2][1]),
                      max(useful_list[idx1][1], useful_list[idx2][1]))
    return closest_pair


######################################################################
# Code for hierarchical clustering


def hierarchical_clustering(cluster_list, num_clusters):
    """
    Compute a hierarchical clustering of a set of clusters
    Note: the function may mutate cluster_list
    
    Input: List of clusters, integer number of clusters
    Output: List of clusters whose length is num_clusters
    """
    while len(cluster_list) > num_clusters:
        nearest_clusters = fast_closest_pair(cluster_list)
        cluster_i = cluster_list.pop(nearest_clusters[1])
        cluster_j = cluster_list.pop(nearest_clusters[2] - 1)
        cluster_ij = cluster_i.merge_clusters(cluster_j)
        cluster_list.append(cluster_ij)
    return cluster_list

######################################################################
# Code for k-means clustering


def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    Compute the k-means clustering of a set of clusters
    Note: the function may not mutate cluster_list
    
    Input: List of clusters, integers number of clusters and number of iterations
    Output: List of clusters whose length is num_clusters
    """
    # position initial clusters at the location of clusters with largest populations

    cluster_list_copy = [cluster.copy() for cluster in cluster_list]
    cluster_list_copy.sort(key=lambda clus: clus.total_population(), reverse=True)
    k_centers = [cluster_list_copy[idx] for idx in range(num_clusters)]
    for _ in range(num_iterations):
        new_clusters = [alg_cluster.Cluster(set([]), 0, 0, 0, 0) for _ in range(len(k_centers))]
        for cluster in cluster_list_copy:
            min_dist = float('inf')
            nearest_center_idx = -1
            for k_center_idx in range(len(k_centers)):
                k_center = k_centers[k_center_idx]
                new_dist = cluster.distance(k_center)
                if new_dist < min_dist:
                    min_dist = new_dist
                    nearest_center_idx = k_center_idx
            new_clusters[nearest_center_idx].merge_clusters(cluster)
        k_centers = list(new_clusters)
    return k_centers

c_list = [alg_cluster.Cluster(set([1]), 1, 6, 1000, 1),
                alg_cluster.Cluster(set([2]), 1.6, 5.8, 10, 2),
                alg_cluster.Cluster(set([3]), 2.5, 6, 10, 3),
                alg_cluster.Cluster(set([4]), 2.3, 5.3, 10, 4),
                alg_cluster.Cluster(set([5]), 1.4, 5.1, 10, 5),
                alg_cluster.Cluster(set([6]), 5, 5, 1000, 6),
                alg_cluster.Cluster(set([7]), 6, 5, 10, 7),
                alg_cluster.Cluster(set([8]), 5, 4, 10, 8),
                alg_cluster.Cluster(set([9]), 6, 4, 10, 9),
                alg_cluster.Cluster(set([10]), 5, 2, 1000, 10),
                alg_cluster.Cluster(set([11]), 2, 1, 1000, 11)]
print kmeans_clustering(c_list, 4, 1)