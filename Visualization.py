import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
matplotlib.use('TkAgg')


def Visualize_Substrate(total_number_centers, longitude, latitude, edges_adjacency_matrix, solution, virtual_links):
    virtual_links = np.logical_or.reduce(virtual_links, axis=1)
    virtual_links = virtual_links.astype(np.float16)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    tab20 = plt.get_cmap('tab20')
    jump = 5
    for c in range(total_number_centers):
        ax.scatter(longitude[c], latitude[c], 0, color=tab20(0), s=100)
        ax.text(longitude[c], latitude[c], z=0, s=f'node{c + 1}')

    for i in range(total_number_centers):
        for j in range(i, total_number_centers):
            if edges_adjacency_matrix[i][j]:
                ax.plot([longitude[i], longitude[j]], [latitude[i], latitude[j]], [0, 0], color=tab20(0))



    number_slices, number_VNFs, total_number_centers = solution.shape

    for s in range(number_slices):
        for k in range(number_VNFs):
            for c in range(total_number_centers):
                if solution[s, k, c]:
                    jump_ = jump * (s + 1)
                    ax.scatter(longitude[c], latitude[c], jump_, color=tab20(2 * (s + 1)), s=100)

    for s in range(number_slices):
        for i in range(edges_adjacency_matrix.shape[0]):
            for j in range(edges_adjacency_matrix.shape[1]):
                if virtual_links[s, i, j]:
                    jump_ = jump * (s + 1)
                    ax.plot([longitude[i], longitude[j]], [latitude[i], latitude[j]],
                            [jump_, jump_], color=tab20(2 * (s + 1)))

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([jump * s for s in range(number_slices + 1)], ['Physical Substrate'] +
                  [f'Slice {s + 1}' for s in range(number_slices)])
    x_limits = ax.get_xlim()
    y_limits = ax.get_ylim()
    vertices = [[[x_limits[0], y_limits[0], jump * s], [x_limits[1], y_limits[0], jump * s],
                [x_limits[1], y_limits[1], jump * s], [x_limits[0], y_limits[1], jump * s]]
                for s in range(number_slices + 1)]

    poly = Poly3DCollection(vertices, alpha=0.3)
    colors = [tab20(2 * s) for s in range(number_slices + 1)]
    poly.set_facecolor(colors)
    ax.add_collection3d(poly)


    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_zlabel('Slices')


    plt.show()


