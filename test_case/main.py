from graph_topology import graph_topology
from slice_instantiation import slice_instantiation
from network_slicing import network_slicing
from flexible_network_slicing import flexible_network_slicing


# from Lagrangian_Relaxation import network_slicing


def main():
    total_number_centers, total_available_cpus, edges_adjacency_matrix, total_available_bandwidth, edges_delay = (
        graph_topology())

    number_slices = 3
    number_VNFs = 2
    required_cpus, required_bandwidth, delay_tolerance = slice_instantiation(number_slices, number_VNFs=number_VNFs)
    solution, virtual_links, are_deployed, unassigned_cpus = flexible_network_slicing(number_slices,
                                                                                      total_number_centers,
                                                                                      total_available_cpus,
                                                                                      edges_adjacency_matrix,
                                                                                      total_available_bandwidth,
                                                                                      edges_delay, number_VNFs,
                                                                                      required_cpus, required_bandwidth,
                                                                                      delay_tolerance)
    print('\n', solution)
    print(virtual_links[0, 0, :, :])
    print(virtual_links[1, 0, :, :])
    print(virtual_links[2, 0, :, :])
    print(are_deployed)
    print(unassigned_cpus)


if __name__ == '__main__':
    main()
