import numpy as np


from Embedding import embedding
from graph_topology import graph_topology
from EpidemicModel import EpidemicModel


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


def EpidemicSlicingSimulation(number_slices, total_number_centers, total_available_cpus, centers_task_execution_delay,
                              edges_adjacency_matrix, total_available_bandwidth, edges_delay, Rounds):
    number_VNFs = 6
    solutions = []
    system_performance = []
    are_deployed = []
    for Round in Rounds:
        if Round:
            for center in Round:
                total_available_cpus[center] = 0
        # Embedding
        solution, slices_deployed = embedding(number_slices, number_VNFs, total_number_centers, total_available_cpus,
                                              centers_task_execution_delay, edges_adjacency_matrix,
                                              total_available_bandwidth, edges_delay)
        solutions.append(solution)
        are_deployed.append(slices_deployed)
        curr_system_performance = np.sum(slices_deployed) / len(slices_deployed)
        system_performance.append(curr_system_performance)
        print(solution)
        print(slices_deployed)
        print(curr_system_performance)
    return system_performance, are_deployed, solutions


def main():
    number_nodes = 10
    (total_number_centers, total_available_cpus, centers_task_execution_delay, edges_adjacency_matrix,
     total_available_bandwidth, edges_delay) = graph_topology(number_nodes)
    number_slices = 15
    initial_center = np.random.choice(total_number_centers)
    spread = 0.3
    Rounds = EpidemicModel(total_number_centers, edges_adjacency_matrix, initial_center, spread=spread)
    system_performance, are_deployed, solutions = EpidemicSlicingSimulation(number_slices, total_number_centers,
                                                                            total_available_cpus,
                                                                            centers_task_execution_delay,
                                                                            edges_adjacency_matrix,
                                                                            total_available_bandwidth, edges_delay,
                                                                            Rounds)
    print(Rounds)


if __name__ == '__main__':
    main()
