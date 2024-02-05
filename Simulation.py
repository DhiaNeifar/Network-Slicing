import numpy as np
import pickle
import os

from MILP import define_topology, define_slices, network_slicing, _print


def is_deployed(_index, _deployed):
    message = f'\nSlice {_index} is '
    if _deployed[0]:
        message += 'deployed!'
    else:
        message += 'not deployed!'
    return message


def save_pickle(_dict):
    for key, value in _dict.items():
        pickle.dump(value, open(os.path.join('pickle data', f'{key}.pkl'), 'wb'))


def all_deployed(_deployed):
    return np.all(np.array(_deployed) == 1)


def used_cpus(_solution, _required_cpus):
    return np.sum(np.sum(_required_cpus[:, :, np.newaxis] * _solution, axis=0), axis=0, dtype=np.int16)


def Simulation():
    # Define topology
    number_edge = 2
    number_cloud = 3
    total_number_centers, total_available_cpus = define_topology(number_edge=number_edge, number_cloud=number_cloud)
    remaining_available_cpus = np.copy(total_available_cpus)

    # Define slices
    number_slices = 1
    number_VNFs = 6

    lambda_, mu = 1.0, 0.05
    num_slices = 500
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
    _print('Total Available CPUs', total_available_cpus)
    consumed_cpu_list, deployed_list = [], []

    i, j = 0, 0
    while i < num_slices:
        if arrival_times[i] < departure_times[j]:
            print(f'\nSlice {i + 1} arrived!')
            required_cpus = define_slices(number_slices=number_slices, number_VNFs=number_VNFs)

            solution, deployed = network_slicing(number_VNFs, number_slices, total_number_centers, required_cpus,
                                                 remaining_available_cpus)
            deployed_list.append(deployed[0])
            _print('Remaining Available CPUs', remaining_available_cpus)
            print(is_deployed(i + 1, deployed))
            consumed_cpu_per_center = used_cpus(solution, required_cpus)
            consumed_cpu_list.append(consumed_cpu_per_center)
            _print('Consumed CPU Per Center', consumed_cpu_per_center)
            remaining_available_cpus -= consumed_cpu_per_center
            _print('Remaining Available CPUs', remaining_available_cpus)
            _print('Solution', solution)
            i += 1
        else:
            print(f'\nSlice {sorted_slices_indices[j]} ended!')
            remaining_available_cpus += consumed_cpu_list[j]
            _print('Remaining Available CPUs', remaining_available_cpus)
            j += 1
    while j < num_slices:
        print(f'\nSlice {sorted_slices_indices[j]} ended!')
        remaining_available_cpus += consumed_cpu_list[j]
        _print('Remaining Available CPUs', remaining_available_cpus)
        j += 1
    data = {
        'total_available_cpus': total_available_cpus,
        'arrival_times': arrival_times,
        'departure_times': departure_times,
        'deployed': deployed_list,
        'sorted_slices_indices': sorted_slices_indices,
        'remaining_available_cpus': remaining_available_cpus,
        'consumed_cpu_list': consumed_cpu_list
    }
    save_pickle(data)


if __name__ == '__main__':
    Simulation()
