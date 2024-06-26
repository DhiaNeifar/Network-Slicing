import numpy as np


from graph_topology import graph_topology
from slice_instantiation import slice_instantiation
from network_slicing import network_slicing
from Visualization import Visualize_Substrate


def consumed_cpus(total_available_cpus, required_cpus, solution):
    consumed_ = solution * required_cpus[:, :, np.newaxis]
    consumed_slices = consumed_.sum(axis=0).sum(axis=0)
    print(total_available_cpus)
    print(consumed_slices)



def main():
    number_nodes = 8
    (total_number_centers, total_available_cpus, longitude, latitude, edges_adjacency_matrix, total_available_bandwidth,
     edges_delay) = graph_topology(number_nodes)

    number_slices = 4
    number_VNFs = 4

    failed_centers = []
    required_cpus, required_bandwidth, delay_tolerance = slice_instantiation(number_slices, number_VNFs=number_VNFs)

    print(total_available_cpus)
    print(required_cpus)
    solution, virtual_links = network_slicing(number_slices, total_number_centers, total_available_cpus,
                                              edges_adjacency_matrix, total_available_bandwidth, edges_delay,
                                              number_VNFs, required_cpus, required_bandwidth, delay_tolerance,
                                              failed_centers)
    print(solution)
    consumed_cpus(total_available_cpus, required_cpus, solution)
    Visualize_Substrate(total_number_centers, longitude, latitude, edges_adjacency_matrix, solution, virtual_links,
                        0, failed_centers)



if __name__ == '__main__':
    main()
