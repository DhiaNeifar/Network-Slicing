import numpy as np

from slice_instantiation import slice_instantiation
from network_slicing import network_slicing


def calc_consumed_resources(solution, required_resources, total_available_resources, total_resources_consumed):
    consumed_resources = np.sum(required_resources[:, np.newaxis] * solution, axis=0, dtype=np.int16)
    total_resources_consumed.append(consumed_resources)
    return total_available_resources - consumed_resources


def embedding(number_slices, number_VNFs, total_number_centers, total_available_cpus, centers_task_execution_delay,
              edges_adjacency_matrix, total_available_bandwidth, edges_delay):
    (required_cpus, required_bandwidth, VNFs_task_execution_delay, E2E_delay) = slice_instantiation(number_slices,
                                                                                                    number_VNFs)
    return network_slicing(number_slices, total_number_centers, total_available_cpus, centers_task_execution_delay,
                           edges_adjacency_matrix, total_available_bandwidth, edges_delay, number_VNFs, required_cpus,
                           required_bandwidth, VNFs_task_execution_delay, E2E_delay)
