import numpy as np

from slice_instantiation import slice_instantiation


def testing():
    number_slices = 4
    number_VNFs = 4
    required_cpus, required_bandwidth, delay_tolerance = slice_instantiation(number_slices, number_VNFs)

    required_cpus_ = np.copy(required_cpus)
    required_cpus_ = required_cpus_.astype(np.float32)
    required_cpus_decimals = required_cpus_ / 10
    required_cpus_units = required_cpus_ / 100
    print(required_cpus)
    print(required_cpus_)
    print(required_cpus_decimals)
    print(required_cpus_units)


    print(required_cpus_ - required_cpus_decimals)

    return


if __name__ == '__main__':
    testing()
