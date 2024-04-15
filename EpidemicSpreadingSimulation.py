import numpy as np


from substrate import physical_substrate
from EpidemicModel import EpidemicModel
from slice_instantiation import slice_instantiation
from utils import save_results
from slack_slicing import slack_slicing
from Visualization import Visualize_Substrate


def EpidemicSlicingSimulation():
    number_nodes = 8
    (total_number_centers, total_available_cpus, longitude, latitude, edges_adjacency_matrix, total_available_bandwidth,
     edges_delay) = physical_substrate(number_nodes)


    _total_available_cpus = np.copy(total_available_cpus)
    Spread = 0.3
    Rounds = EpidemicModel(total_number_centers, edges_adjacency_matrix, spread=Spread)

    number_slices = 5
    number_VNFs = 6

    required_cpus, required_bandwidth, delay_tolerance = slice_instantiation(number_slices, number_VNFs)

    VNFs_placements = []
    virtual_links = []
    slack_variables = []

    print('Starting Epidemic Slicing')
    print(f'Rounds = {Rounds}')
    failed_centers = []
    for round_index, Round in enumerate(Rounds, 1):
        print(f'Round {round_index}')
        if Round:
            for center in Round:
                total_available_cpus[center] = 0
        failed_centers.extend(Round)

        # Embedding
        solution = slack_slicing(number_slices, total_number_centers, total_available_cpus, edges_adjacency_matrix,
                                 total_available_bandwidth, edges_delay, number_VNFs, required_cpus,
                                 required_bandwidth, delay_tolerance, failed_centers)

        VNFs_placements.append(solution[0])
        virtual_links.append(solution[1])
        slack_variables.append(solution[2])

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
            'virtual_links': virtual_links,
            'slack_variables': slack_variables}
    save_results(data)
    return


if __name__ == '__main__':
    EpidemicSlicingSimulation()
