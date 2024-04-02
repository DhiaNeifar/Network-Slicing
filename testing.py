import numpy as np


from utils import load_data, save_results
from network_slicing import network_slicing


def EpidemicSlicingSimulation():
    data = load_data()
    number_nodes = data['number_nodes']
    total_number_centers = data['total_number_centers']
    total_available_cpus = data['total_available_cpus']
    longitude = data['longitude']
    latitude = data['latitude']
    edges_adjacency_matrix = data['edges_adjacency_matrix']
    total_available_bandwidth = data['total_available_bandwidth']
    edges_delay = data['edges_delay']
    Spread = data['Spread']
    Rounds = data['Rounds']
    number_slices = data['number_slices']
    number_VNFs = data['number_VNFs']
    required_cpus = data['required_cpus']
    required_bandwidth = data['required_bandwidth']
    delay_tolerance = data['delay_tolerance']

    total_available_cpus_copy = np.copy(total_available_cpus)

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

        # No Scaling

        # scaled_required_cpus = scale(total_available_cpus, required_cpus)

        # Embedding
        solution = network_slicing(number_slices, total_number_centers, total_available_cpus, edges_adjacency_matrix,
                                   total_available_bandwidth, edges_delay, number_VNFs, required_cpus,
                                   required_bandwidth, delay_tolerance, failed_centers)
        VNFs_placements.append(solution[0])
        virtual_links.append(solution[1])


    # Results

    data = {'number_nodes': number_nodes,
            'total_number_centers': total_number_centers,
            'total_available_cpus': total_available_cpus_copy,
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
