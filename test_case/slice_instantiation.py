import numpy as np


def slice_instantiation(num_slices, number_VNFs=2):
    required_cpus = np.array([[13, 17], [16, 12], [8, 1]], dtype=np.int16)
    required_bandwidth = np.array([[3], [5], [4]], dtype=np.int16)
    delay_tolerance = np.array([0.05, 0.25, 0.3], dtype=np.float16)
    return required_cpus, required_bandwidth, delay_tolerance


if __name__ == '__main__':
    _ = slice_instantiation(10)
