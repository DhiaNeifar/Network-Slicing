from utils import generate_random_values


def slice_instantiation(num_slices, number_VNFs=6):
    required_cpus = generate_random_values(1, 2, (num_slices, number_VNFs))
    required_bandwidth = generate_random_values(1, 2, (num_slices, number_VNFs - 1))
    delay_tolerance = generate_random_values(200000, 200001, num_slices)
    return required_cpus, required_bandwidth, delay_tolerance


if __name__ == '__main__':
    _ = slice_instantiation(10)
