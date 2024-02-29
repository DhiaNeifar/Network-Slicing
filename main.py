import numpy as np


from graph_topology import graph_topology
from slice_instantiation import slice_instantiation
from network_slicing import network_slicing
from Visualization import Visualize_Substrate


def main():
    number_nodes = 10
    (total_number_centers, total_available_cpus, longitude, latitude, edges_adjacency_matrix, total_available_bandwidth,
     edges_delay) = graph_topology(number_nodes)

    number_slices = 5
    number_VNFs = 6
    required_cpus, required_bandwidth, delay_tolerance = slice_instantiation(number_slices, number_VNFs=number_VNFs)

    solution, virtual_links, are_deployed = network_slicing(number_slices, total_number_centers, total_available_cpus,
                                                            edges_adjacency_matrix, total_available_bandwidth,
                                                            edges_delay, number_VNFs, required_cpus, required_bandwidth,
                                                            delay_tolerance)

    Visualize_Substrate(total_number_centers, longitude, latitude, edges_adjacency_matrix, solution, virtual_links)


if __name__ == '__main__':
    main()
