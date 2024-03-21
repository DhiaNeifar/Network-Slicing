import numpy as np


from graph_topology import graph_topology
from EpidemicModel import EpidemicModel
from slice_instantiation import slice_instantiation
from utils import scale
from network_slicing import network_slicing
from Visualization import Visualize_Substrate


def EpidemicSlicingSimulation(total_number_centers, total_available_cpus, edges_adjacency_matrix, longitude, latitude,
                              total_available_bandwidth, edges_delay, Rounds):

    number_slices = 5
    number_VNFs = 6

    required_cpus, required_bandwidth, delay_tolerance = slice_instantiation(number_slices, number_VNFs)

    solutions = []
    system_performance = []
    are_deployed = []
    print('Starting Epidemic Slicing')
    print(f'Rounds = {Rounds}')
    failed_centers = []
    for round_index, Round in enumerate(Rounds, 1):
        print(f'Round {round_index}')
        if Round:
            for center in Round:
                total_available_cpus[center] = 0
        failed_centers.extend(Round)
        scaled_required_cpus = scale(total_available_cpus, required_cpus)

        # Embedding
        solution, virtual_links = network_slicing(number_slices, total_number_centers, total_available_cpus,
                                                  edges_adjacency_matrix, total_available_bandwidth, edges_delay,
                                                  number_VNFs, scaled_required_cpus, required_bandwidth,
                                                  delay_tolerance, failed_centers)

        Visualize_Substrate(total_number_centers, longitude, latitude, edges_adjacency_matrix, solution, virtual_links,
                            round_index, failed_centers)
    return system_performance, are_deployed, solutions


def main():
    number_nodes = 12
    start = 3
    (total_number_centers, total_available_cpus, longitude, latitude, edges_adjacency_matrix, total_available_bandwidth,
     edges_delay) = graph_topology(number_nodes, start)

    Rounds = EpidemicModel(total_number_centers, edges_adjacency_matrix, spread=0.4)


    system_performance, are_deployed, solutions = EpidemicSlicingSimulation(total_number_centers, total_available_cpus,
                                                                            edges_adjacency_matrix, longitude, latitude,
                                                                            total_available_bandwidth, edges_delay,
                                                                            Rounds)


if __name__ == '__main__':
    main()
