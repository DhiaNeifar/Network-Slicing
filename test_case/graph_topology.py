import numpy as np


def graph_topology():
    total_number_centers = 3
    total_available_cpus = np.array([29, 18, 20], dtype=np.int16)

    edges_adjacency_matrix = np.zeros((total_number_centers, total_number_centers), dtype=np.int8)
    total_available_bandwidth = np.zeros((total_number_centers, total_number_centers), dtype=np.int16)
    edges_delay = np.zeros((total_number_centers, total_number_centers), dtype=np.float16)

    edges_adjacency_matrix[0, 1], edges_adjacency_matrix[1, 0] = 1, 1
    edges_adjacency_matrix[1, 2], edges_adjacency_matrix[2, 1] = 1, 1

    total_available_bandwidth[0, 1], total_available_bandwidth[1, 0] = 8, 7
    total_available_bandwidth[1, 2], total_available_bandwidth[2, 1] = 8, 8

    edges_delay[0, 1], edges_delay[1, 0] = 0.05, 0.05
    edges_delay[1, 2], edges_delay[2, 1] = 0.25, 0.25

    return total_number_centers, total_available_cpus, edges_adjacency_matrix, total_available_bandwidth, edges_delay



if __name__ == '__main__':
    graph_topology()
