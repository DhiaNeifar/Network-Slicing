import xml.etree.ElementTree as ET
import os
import numpy as np

from utils import generate_random_values


def calc_distance(lat1, lon1, lat2, lon2):
    def deg2rad(deg):
        return deg * (np.pi / 180)

    R = 6371
    dLat = deg2rad(lat2 - lat1)
    dLon = deg2rad(lon2 - lon1)
    a = (np.sin(dLat / 2) * np.sin(dLat / 2) +
         np.cos(deg2rad(lat1)) * np.cos(deg2rad(lat2)) * np.sin(dLon / 2) * np.sin(dLon / 2))
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    return R * c / 300


def graph_topology(number_node, filename='compuserve.xml'):
    tree = ET.parse(os.path.join(os.getcwd(), 'Graphs', filename))
    root = tree.getroot()
    root = root.find('graph')
    total_number_centers = 0
    index = 0
    longitude, latitude = [], []
    while root[index].tag != 'node':
        index += 1
    while root[index].tag == 'node':
        total_number_centers += 1
        longitude.append(float(root[index][1].text))
        latitude.append(float(root[index][4].text))
        index += 1
    edges_adjacency_matrix = np.zeros((total_number_centers, total_number_centers))
    edges_delay = np.zeros((total_number_centers, total_number_centers))
    total_available_bandwidth = np.zeros((total_number_centers, total_number_centers))

    while index < len(root) and root[index].tag == 'edge':
        attributes = root[index].attrib
        source, target = int(attributes['source']), int(attributes['target'])
        edges_adjacency_matrix[source, target], edges_adjacency_matrix[target, source] = 1, 1
        edges_delay[source, target] = calc_distance(longitude[source], latitude[source], longitude[target],
                                                    latitude[target]) if target != 11 else 0
        edges_delay[target, source] = edges_delay[source, target]
        total_available_bandwidth[source, target] = generate_random_values(60, 81, 1)[0] if target != 11 else 10000
        total_available_bandwidth[target, source] = total_available_bandwidth[source, target]
        index += 1
    start = total_number_centers - number_node
    total_available_cpus = generate_random_values(40, 51, number_node)
    total_available_cpus[-1] = 10000
    # centers_task_execution_delay = generate_random_values(0.01, 0.31, total_number_centers, _type='float')
    return (number_node, total_available_cpus, longitude[start:], latitude[start:],
            edges_adjacency_matrix[start:, start:], total_available_bandwidth[start:, start:],
            edges_delay[start:, start:])



if __name__ == '__main__':
    _filename = 'ATT North America.xml'
    graph_topology(_filename)
