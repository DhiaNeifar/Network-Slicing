import numpy as np


from graph_topology import graph_topology
from Embedding import embedding


def calc_performance(slice_state, total_deployed, total_failed):
    count_current, count_deployed, count_failed = 0, 0, 0
    for index, state in enumerate(slice_state):
        if state:
            count_current += 1
            if total_deployed[index]:
                count_deployed += 1
            if total_failed[index]:
                count_failed += 1
    if count_current:
        return (count_deployed - count_failed) / count_current * 100
    return 0.0


def EpidemicSlicingSimulation(arrival_times, departure_times, centers, failure_times):
    (total_number_centers, total_available_cpus, centers_task_execution_delay, edges_adjacency_matrix,
     total_available_bandwidth, edges_delay) = graph_topology()
    num_slices = len(arrival_times)
    number_VNFs = 6
    total_remaining_cpus, total_remaining_bandwidth = (np.copy(total_available_cpus),
                                                       np.copy(total_available_bandwidth))
    total_resources_consumed = []
    solutions = []
    failure_times += arrival_times[0]
    i, j, k = 0, 0, 0
    total_deployed, total_failed = [0 for _ in range(num_slices)], [0 for _ in range(num_slices)]
    slice_state = [0 for _ in range(num_slices)]
    system_performance = []
    print('Available CPUs per Node:\n')
    print(total_remaining_cpus)
    while i < len(arrival_times) or j < len(departure_times) or k < len(failure_times):
        val1 = arrival_times[i] if i < len(arrival_times) else None
        val2 = departure_times[j] if j < len(departure_times) else None
        val3 = failure_times[k] if k < len(failure_times) else None

        min_val, min_list = min(
            (v, l) for v, l in [(val1, 'arrival_times'), (val2, 'departure_times'), (val3, 'failure_times')] if
            v is not None)

        if min_list == 'arrival_times':
            # Embedding
            solution, is_deployed, total_remaining_cpus = embedding(number_VNFs, total_number_centers,
                                                                    total_remaining_cpus, centers_task_execution_delay,
                                                                    edges_adjacency_matrix, total_remaining_bandwidth,
                                                                    edges_delay, total_resources_consumed)
            print('Solution:\n')
            print(solution)
            print('Remaining CPUs:\n')
            print(total_remaining_cpus)
            solutions.append(solution)
            if is_deployed:
                slice_state[i] = 1
                total_deployed[i] = 1
            if not is_deployed:
                slice_state[i] = 0
                total_failed[i] = 1
            i += 1

        if min_list == 'departure_times':
            # Add resources utilized
            if slice_state[j]:
                total_remaining_cpus += total_resources_consumed[j]
                slice_state[j] = 0
            j += 1
        if min_list == 'failure_times':
            for index, current_slice in enumerate(slice_state):
                if current_slice:
                    for vnf in range(number_VNFs):
                        if solutions[index][vnf, centers[k]]:
                            total_remaining_cpus += total_resources_consumed[index]
                            total_failed[index] = 1
            total_remaining_cpus[k] = 0
            k += 1
        system_performance.append(calc_performance(slice_state, total_deployed, total_failed))
    time_line = np.concatenate((arrival_times, departure_times, failure_times), axis=0)
    sorted_indices = np.argsort(time_line)
    time_line = np.array(time_line)[sorted_indices]
    system_performance = np.array(system_performance)[sorted_indices]
    return system_performance, time_line, centers, failure_times
