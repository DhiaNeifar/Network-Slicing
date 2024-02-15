import numpy as np

from utils import generate_random_values


def slice_instantiation(num_slices, number_VNFs=6):
    required_cpus = generate_random_values(1, 21, (num_slices, number_VNFs))
    required_bandwidth_per_VNF = generate_random_values(10, 31, (num_slices, number_VNFs - 1))
    required_bandwidth = np.zeros((num_slices, number_VNFs, number_VNFs))
    for i in range(num_slices):
        for j in range(number_VNFs - 1):
            required_bandwidth[i, j, j + 1] = required_bandwidth_per_VNF[i, j]
            required_bandwidth[i, j + 1, j] = required_bandwidth_per_VNF[i, j]
    VNFs_task_execution_delay = generate_random_values(0.01, 0.11, (num_slices, number_VNFs), _type='float')
    E2E_delay = generate_random_values(1, 21, num_slices)
    return required_cpus, required_bandwidth, VNFs_task_execution_delay, E2E_delay


if __name__ == '__main__':
    _ = slice_instantiation(10)
