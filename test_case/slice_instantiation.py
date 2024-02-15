import numpy as np


def slice_instantiation(num_slices, number_VNFs=2):
    required_cpus = np.array([[13, 17], [16, 12], [8, 1]], dtype=np.int16)
    required_bandwidth_per_VNF = np.array([[3], [5], [3]], dtype=np.int16)
    required_bandwidth = np.zeros((num_slices, number_VNFs, number_VNFs))
    for i in range(num_slices):
        for j in range(number_VNFs - 1):
            required_bandwidth[i, j, j + 1] = required_bandwidth_per_VNF[i, j]
            required_bandwidth[i, j + 1, j] = required_bandwidth_per_VNF[i, j]
    return required_cpus, required_bandwidth


if __name__ == '__main__':
    _ = slice_instantiation(10)
