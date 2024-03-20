import numpy as np


def generate_random_values(low, high, size, _type='int'):
    if _type == 'int':
        return np.random.randint(low=low, high=high, size=size, dtype=np.int32)
    return np.random.uniform(low=low, high=high, size=size)


def scale(total_available_cpus, required_cpus):
    sum_available = np.sum(total_available_cpus, dtype=np.int16)
    sum_required = np.sum(required_cpus, dtype=np.int16)
    if sum_available and sum_available < sum_required:
        required_cpus *= sum_available
        required_cpus //= sum_required
        deficit = sum_available - np.sum(required_cpus, dtype=np.int16)
        count = np.count_nonzero(required_cpus == 0)
        if deficit < count:
            print(f'The number of VNFs requiring 0 CPUs after scaling: {count} > deficit {deficit}')
        required_cpus = np.vectorize(lambda x: 1 if x == 0 else x)(required_cpus)
    return required_cpus


if __name__ == '__main__':
    required_cpus_ = np.array([[13, 17], [16, 12], [8, 1]], dtype=np.int16)
    total_available_cpus_ = np.array([0, 0, 0], dtype=np.int16)
    scale(total_available_cpus_, required_cpus_)
