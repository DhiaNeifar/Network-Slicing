import numpy as np


from graph_topology import graph_topology
from EpidemicModel import EpidemicModel
from slice_instantiation import slice_instantiation
from utils import scale, save_results
from network_slicing import network_slicing
from Visualization import Visualize_Substrate


def EpidemicSlicingSimulation():
    number_nodes = 9
    (total_number_centers, total_available_cpus, longitude, latitude, edges_adjacency_matrix, total_available_bandwidth,
     edges_delay) = graph_topology(number_nodes)
    _total_available_cpus = np.copy(total_available_cpus)
    Spread = 0.4
    Rounds = EpidemicModel(total_number_centers, edges_adjacency_matrix, spread=Spread)

    number_slices = 5
    number_VNFs = 5

    required_cpus, required_bandwidth, delay_tolerance = slice_instantiation(number_slices, number_VNFs)

    VNFs_placements = []
    virtual_links = []

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
        solution = network_slicing(number_slices, total_number_centers, total_available_cpus, edges_adjacency_matrix,
                                   total_available_bandwidth, edges_delay, number_VNFs, scaled_required_cpus,
                                   required_bandwidth, delay_tolerance, failed_centers)
        VNFs_placements.append(solution[0])
        virtual_links.append(solution[1])

        Visualize_Substrate(total_number_centers, longitude, latitude, edges_adjacency_matrix, solution[0], solution[1],
                            failed_centers)

    # Results

    data = {'number_nodes': number_nodes,
            'total_number_centers': total_number_centers,
            'total_available_cpus': _total_available_cpus,
            'longitude': longitude,
            'latitude': latitude,
            'edges_adjacency_matrix': edges_adjacency_matrix,
            'total_available_bandwidth': total_available_bandwidth,
            'edges_delay': edges_delay,
            'Spread': Spread,
            'Rounds': Rounds,
            'number_slices': number_slices,
            'number_VNFs': number_VNFs,
            'required_cpus': required_cpus,
            'required_bandwidth': required_bandwidth,
            'delay_tolerance': delay_tolerance,
            'VNFs_placements': VNFs_placements,
            'virtual_links': virtual_links}
    save_results(data)
    return


if __name__ == '__main__':
    EpidemicSlicingSimulation()
