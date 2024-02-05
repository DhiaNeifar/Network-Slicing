import numpy as np

from Towards_Secure_Slicing import generate_random_values


def slice_instantiation(number_VNFs=6):
    required_cpus = generate_random_values(1, 21, number_VNFs)
    required_bandwidth_per_VNF = generate_random_values(10, 31, number_VNFs - 1)
    required_bandwidth = np.zeros((number_VNFs, number_VNFs))
    for i in range(number_VNFs - 1):
        required_bandwidth[i, i + 1] = required_bandwidth_per_VNF[i]
        required_bandwidth[i + 1, i] = required_bandwidth_per_VNF[i]
    VNFs_task_execution_delay = generate_random_values(0.01, 0.11, number_VNFs, _type='float')
    E2E_delay = generate_random_values(1, 21, 1)
    return number_VNFs, required_cpus, required_bandwidth, VNFs_task_execution_delay, E2E_delay


if __name__ == '__main__':
    _ = slice_instantiation()
