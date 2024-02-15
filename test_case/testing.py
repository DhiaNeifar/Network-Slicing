import numpy as np


def main():
    adjacency_matrix = np.zeros((5, 5))
    adjacency_matrix[0, 2], adjacency_matrix[2, 0] = 1, 1
    adjacency_matrix[0, 3], adjacency_matrix[3, 0] = 1, 1
    adjacency_matrix[1, 2], adjacency_matrix[2, 1] = 1, 1
    adjacency_matrix[1, 3], adjacency_matrix[3, 1] = 1, 1
    adjacency_matrix[2, 3], adjacency_matrix[3, 2] = 1, 1
    adjacency_matrix[2, 4], adjacency_matrix[4, 2] = 1, 1
    adjacency_matrix[3, 4], adjacency_matrix[4, 3] = 1, 1
    number_VNFs, number_slices = 6, 3
    Virtual_links_1 = np.array([[[[f'slice_{s}_VL{k}_to_VL{k + 1}_PN{i}_to_PN{j}' for j in
                                   range(adjacency_matrix.shape[1])] for i in range(adjacency_matrix.shape[0])] for k in
                                 range(number_VNFs - 1)] for s in range(number_slices)])

    Virtual_links_2 = np.array([[[[f'slice_{s}_VL{number_VNFs - k}_to_VL{number_VNFs - k - 1}_PN{i}_to_PN{j}' for j in
                                   range(adjacency_matrix.shape[1])] for i in range(adjacency_matrix.shape[0])] for k in
                                 range(1, number_VNFs)] for s in range(number_slices)])
    Virtual_links = np.concatenate((Virtual_links_1, Virtual_links_2), axis=1)
    print(Virtual_links.shape)
    pass


if __name__ == '__main__':
    main()
