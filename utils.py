import numpy as np
import os
import pickle


def generate_random_values(low, high, size, _type='int'):
    if _type == 'int':
        return np.random.randint(low=low, high=high, size=size, dtype=np.int32)
    return np.random.uniform(low=low, high=high, size=size)


def scale(total_available_cpus, required_cpus):
    total_available_cpus = total_available_cpus[:-1]
    sum_available = np.sum(total_available_cpus, dtype=np.int16)
    scaled_required_cpus = np.copy(required_cpus)
    sum_required = np.sum(scaled_required_cpus, dtype=np.int16)
    if sum_available and sum_available < sum_required:
        scaled_required_cpus *= sum_available
        scaled_required_cpus //= sum_required
        deficit = sum_available - np.sum(scaled_required_cpus, dtype=np.int16)
        count = np.count_nonzero(scaled_required_cpus == 0)
        if deficit < count:
            print(f'The number of VNFs requiring 0 CPUs after scaling: {count} > deficit {deficit}')
        scaled_required_cpus = np.vectorize(lambda x: 1 if x == 0 else x)(scaled_required_cpus)
    return scaled_required_cpus


def check_cpus_consumption(total_available_cpus, required_cpus, solution):
    print(total_available_cpus)
    consumed_ = solution * required_cpus[:, :, np.newaxis]
    print(consumed_)
    consumed_slices = consumed_.sum(axis=0).sum(axis=0)
    print(consumed_slices)


def save_results(data_tosave):
    curr_path = os.getcwd()
    results_path = os.path.join(curr_path, 'results')
    os.makedirs(results_path, exist_ok=True)
    result_index = len(os.listdir(results_path)) + 1
    result_path = os.path.join(results_path, f'Test {result_index}')
    os.makedirs(result_path, exist_ok=True)
    for key, value in data_tosave.items():
        pickle.dump(value, open(os.path.join(result_path, f'{key}.pkl'), 'wb'))


def load_data():
    data = {}
    results = os.path.join(os.getcwd(), 'results')
    test_path = os.path.join(results, f'Test {len(os.listdir(results))}')
    for filename in os.listdir(test_path):
        data[filename[:-4]] = pickle.load(open(os.path.join(test_path, filename), 'rb'))
    return data


if __name__ == '__main__':
    required_cpus_ = np.array([[13, 17], [16, 12], [8, 1]], dtype=np.int16)
    total_available_cpus_ = np.array([0, 0, 0], dtype=np.int16)
    scale(total_available_cpus_, required_cpus_)
