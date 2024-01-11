import numpy as np

from MILP import define_topology, define_slices, network_slicing


def Simulation():
    # Define topology
    number_edge = 2
    number_cloud = 3
    total_number_centers, total_available_cpus = define_topology(number_edge=number_edge, number_cloud=number_cloud)

    # Define slices
    number_slices = 1
    number_VNFs = 6

    lambda_, mu = 1.0, 1.0
    num_slices = 2
    inter_arrival_times = np.random.exponential(1 / lambda_, num_slices)
    arrival_times = np.cumsum(inter_arrival_times)
    durations = np.random.exponential(1 / mu, num_slices)
    departure_times = arrival_times + durations

    print(f"arrivals_times: {arrival_times}")
    print(f"departure_times: {departure_times}")

    unsorted_slices_indices = np.arange(1, num_slices + 1, dtype=np.int16)
    sorted_indices = np.argsort(departure_times)
    departure_times = np.array(departure_times)[sorted_indices]
    sorted_slices_indices = np.array(unsorted_slices_indices)[sorted_indices]

    i, j = 0, 0
    while i < num_slices:
        if arrival_times[i] < departure_times[j]:
            print(f'Slice {i + 1} arrived!')
            required_cpus = define_slices(number_slices=number_slices, number_VNFs=number_VNFs)
            solution, deployed_slices = network_slicing(number_VNFs, number_slices, total_number_centers, required_cpus,
                                                        total_available_cpus)
            print(solution)
            print(deployed_slices)
            i += 1
        else:
            print(f'Slice {sorted_slices_indices[j]} ended!')
            j += 1
    while j < num_slices:
        print(f'Slice {sorted_slices_indices[j]} ended!')
        j += 1
    pass


def main():
    Simulation()
    pass


if __name__ == '__main__':
    main()
