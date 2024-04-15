import numpy as np

from utils import generate_random_values


def physical_substrate(number_node):
    total_number_centers = 10
    edges_adjacency_matrix = np.zeros((total_number_centers, total_number_centers))
    edges_delay = np.zeros((total_number_centers, total_number_centers))
    total_available_bandwidth = np.zeros((total_number_centers, total_number_centers))

    links = [(0, 1), (0, 3), (0, 4), (0, 8), (1, 2), (1, 5), (1, 7), (2, 3), (2, 4), (2, 5), (3, 4), (5, 6), (6, 7),
             (6, 8), (6, 9), (7, 8), (8, 9)]

    longitude = [0, 1, -4, -6, -4, 2, 7, 4, 3, 8]
    latitude = [-5, 5, 5, -2, -4, 7, 6, 3, -3, -1]

    for link in links:
        source, target = link[0], link[1]
        edges_adjacency_matrix[source, target], edges_adjacency_matrix[target, source] = 1, 1
        edges_delay[source, target] = generate_random_values(0, 1, 1, _type='ah')[0]
        edges_delay[target, source] = edges_delay[source, target]
        total_available_bandwidth[source, target] = generate_random_values(150, 201, 1)[0]
        total_available_bandwidth[target, source] = total_available_bandwidth[source, target]

    total_number_centers = min(total_number_centers, number_node)
    total_available_cpus = generate_random_values(40, 61, number_node)

    return (total_number_centers, total_available_cpus, longitude[:total_number_centers],
            latitude[:total_number_centers], edges_adjacency_matrix[:total_number_centers, :total_number_centers],
            total_available_bandwidth[:total_number_centers, :total_number_centers],
            edges_delay[:total_number_centers, :total_number_centers])
    pass
