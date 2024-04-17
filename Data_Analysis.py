from math import ceil

from utils import load_data, check_cpus_consumption
from Visualization import Visualize_Substrate
from system_performance import system_performance


def main():
    data = load_data()

    total_number_centers = data['total_number_centers']
    number_VNFs = data['number_VNFs']
    longitude = data['longitude']
    latitude = data['latitude']
    edges_adjacency_matrix = data['edges_adjacency_matrix']
    total_available_cpus = data['total_available_cpus']
    required_cpus = data['required_cpus']
    VNFs_placements = data['VNFs_placements']
    virtual_links = data['virtual_links']
    Rounds = data['Rounds']
    assigned_cpus = data['assigned_cpus']
    alpha = data['alpha']
    print('Starting Epidemic Slicing')
    print(f'Rounds = {Rounds}')
    failed_centers = []
    for round_index, Round in enumerate(Rounds):
        print(f'Round {round_index + 1}')
        if Round:
            for center in Round:
                total_available_cpus[center] = 0
        failed_centers.extend(Round)
        print('Maximum Number VNFs per node ',
              ceil(number_VNFs // max(1, (total_number_centers - 1 - len(failed_centers)))) + 1)
        assigned = assigned_cpus[round_index] * alpha[round_index]
        check_cpus_consumption(total_available_cpus, assigned, VNFs_placements[round_index])
        Visualize_Substrate(total_number_centers, longitude, latitude, edges_adjacency_matrix,
                            VNFs_placements[round_index], virtual_links[round_index], failed_centers)
        system_performance(total_number_centers, total_available_cpus, assigned, VNFs_placements[round_index], alpha[round_index])


if __name__ == '__main__':
    main()
