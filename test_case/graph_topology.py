import numpy as np


def graph_topology():
    total_number_centers = 3
    edges_adjacency_matrix = np.zeros((total_number_centers, total_number_centers))
    total_available_bandwidth = np.zeros((total_number_centers, total_number_centers))
    total_available_cpus = np.array([0, 47, 20], dtype=np.int16)
    edges_adjacency_matrix[0, 1], edges_adjacency_matrix[1, 0] = 1, 1
    edges_adjacency_matrix[1, 2], edges_adjacency_matrix[2, 1] = 1, 1
    total_available_bandwidth[0, 1], total_available_bandwidth[1, 0] = 50, 50
    total_available_bandwidth[1, 2], total_available_bandwidth[2, 1] = 30, 30
    return total_number_centers, total_available_cpus, edges_adjacency_matrix, total_available_bandwidth



if __name__ == '__main__':
    graph_topology()
