import numpy as np

from slice_instantiation import slice_instantiation
from network_slicing import network_slicing


def calc_consumed_resources(solution, required_resources, total_available_resources, total_resources_consumed):
    consumed_resources = np.sum(required_resources[:, np.newaxis] * solution, axis=0, dtype=np.int16)
    total_resources_consumed.append(consumed_resources)
    return total_available_resources - consumed_resources


def embedding(number_VNFS, total_number_centers, total_remaining_cpus, centers_task_execution_delay,
              edges_adjacency_matrix, total_remaining_bandwidth, edges_delay, total_resources_consumed):
    (number_VNFs, required_cpus, required_bandwidth, VNFs_task_execution_delay, E2E_delay) = slice_instantiation(
        number_VNFS)

    solution, is_deployed = network_slicing(total_number_centers, total_remaining_cpus, centers_task_execution_delay,
                                            edges_adjacency_matrix, total_remaining_bandwidth, edges_delay, number_VNFs,
                                            required_cpus, required_bandwidth, VNFs_task_execution_delay, E2E_delay)

    total_remaining_cpus = calc_consumed_resources(solution, required_cpus, total_remaining_cpus,
                                                   total_resources_consumed)
    return solution, int(is_deployed), total_remaining_cpus
