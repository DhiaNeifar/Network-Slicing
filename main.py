import numpy as np

from graph_topology import graph_topology
from EpidemicModel import EpidemicModel
from EpidemicSpreadingSimulation import EpidemicSlicingSimulation


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
