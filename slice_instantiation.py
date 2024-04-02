from utils import generate_random_values


def slice_instantiation(num_slices, number_VNFs=6):
    required_cpus = generate_random_values(10, 31, (num_slices, number_VNFs))
    required_bandwidth = generate_random_values(20, 41, (num_slices, number_VNFs - 1))
    delay_tolerance = generate_random_values(29, 30, num_slices)
    return required_cpus, required_bandwidth, delay_tolerance


if __name__ == '__main__':
    _ = slice_instantiation(10)
