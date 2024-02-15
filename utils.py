import numpy as np


def generate_random_values(low, high, size, _type='int'):
    if _type == 'int':
        return np.random.randint(low=low, high=high, size=size, dtype=np.int16)
    return np.random.uniform(low=low, high=high, size=size)
