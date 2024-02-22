from graph_topology import graph_topology
from slice_instantiation import slice_instantiation
from network_slicing import network_slicing


def main():
    number_nodes = 10
    total_number_centers, total_available_cpus, edges_adjacency_matrix, total_available_bandwidth, edges_delay = (
        graph_topology(number_nodes))

    number_slices = 40
    number_VNFs = 8
    required_cpus, required_bandwidth, delay_tolerance = slice_instantiation(number_slices, number_VNFs=number_VNFs)

    solution, virtual_links, are_deployed = network_slicing(number_slices, total_number_centers, total_available_cpus,
                                                            edges_adjacency_matrix, total_available_bandwidth,
                                                            edges_delay, number_VNFs, required_cpus, required_bandwidth,
                                                            delay_tolerance)
    print(virtual_links)
    print(solution)
    print(are_deployed)



if __name__ == '__main__':
    main()
