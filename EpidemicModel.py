import numpy as np


def EpidemicModel(total_number_centers, edges_adjacency_matrix, initial_center, initial_time, spread=0.1):

    failed_centers = {center: False for center in range(total_number_centers)}
    failure_times = {center: 0.0 for center in range(total_number_centers)}

    # Randomly choose an initial node to fail at time t
    failed_centers[initial_center] = True
    failure_times[initial_center] = initial_time

    # Nodes to be checked in the current iteration
    centers_to_check = [initial_center]
    while centers_to_check:
        new_centers_to_check = []
        for center in centers_to_check:
            neighbors = []
            for neighbor in range(total_number_centers):
                if neighbor != center and edges_adjacency_matrix[center, neighbor] and not failed_centers[neighbor]:
                    neighbors.append(neighbor)
                    time_to_fail = failure_times[center] + np.random.exponential(1 / spread)
                    failed_centers[neighbor] = True
                    failure_times[neighbor] = time_to_fail
                    new_centers_to_check.append(neighbor)
        centers_to_check = new_centers_to_check

    centers = np.arange(0, total_number_centers, dtype=np.int16)
    failure_times = np.array(list(failure_times.values()))
    sorted_indices = np.argsort(failure_times)
    failure_times = np.array(failure_times)[sorted_indices]
    centers = np.array(centers)[sorted_indices]
    return centers, failure_times
