from graph_topology import graph_topology
from slice_instantiation import slice_instantiation
from network_slicing import network_slicing


def main():
    total_number_centers, total_available_cpus, edges_adjacency_matrix, total_available_bandwidth = graph_topology()

    number_slices = 3
    number_VNFs = 2
    required_cpus, required_bandwidth = slice_instantiation(number_slices, number_VNFs=number_VNFs)


    solution, virtual_links, are_deployed = network_slicing(number_slices, total_number_centers, total_available_cpus,
                                                            edges_adjacency_matrix, total_available_bandwidth,
                                                            number_VNFs, required_cpus, required_bandwidth)
    print('\n', solution)
    print(virtual_links[0, 0, :, :])
    print(virtual_links[1, 0, :, :])
    print(virtual_links[2, 0, :, :])
    print(are_deployed)


if __name__ == '__main__':
    main()
