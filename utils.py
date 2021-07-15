import math

import numpy as np

import data
from node import Node


def distance(location1, location2):
    a = location2[0] - location1[0]
    b = location2[1] - location1[1]
    return math.sqrt(a ** 2 + b ** 2)


def distance_lat_lon(lat, lon, requested_lat, requested_lon):
    return distance([lat, lon], [requested_lat, requested_lon])


def distance_between_nodes(node1, node2):
    return distance(node1.get_coords(), node2.get_coords())


def weight(node1, node2):
    c1 = node1.get_coords()
    c2 = node2.get_coords()
    t1 = data.get_thickness(c1)
    t2 = data.get_thickness(c2)
    return 2 ** (t1 + t2)


def get_best_node(nodes):
    min_val = nodes[0].get_f()
    min_node = nodes[0]
    for node in nodes:
        if node.get_f() < min_val:
            min_node = node
            min_val = node.get_f()
    return min_node


def get_neighbors(node, nodes):
    x = node.get_coords()[0]
    y = node.get_coords()[1]
    spaces = []
    spaces.append([x-1, y-1])
    spaces.append([x, y-1])
    spaces.append([x+1, y-1])
    spaces.append([x-1, y])
    spaces.append([x+1, y])
    spaces.append([x-1, y+1])
    spaces.append([x, y+1])
    spaces.append([x+1, y+1])
    neighbors = []

    for s in spaces:
        # Not less than 0 and not out of bounds
        x_in_data_bounds = s[0] >= 0 and s[0] < data.get_width()
        y_in_data_bounds = s[1] >= 0 and s[1] < data.get_height()
        if x_in_data_bounds and y_in_data_bounds:
            if get_node(s[0], s[1], nodes, node) is not None:
                neighbors.append(get_node(s[0], s[1], nodes, node))
    return neighbors


def get_node(x, y, nodes, parent):
    thickness = data.get_thickness([x, y])
    for node in nodes:
        if node.get_coords()[0] == x and node.get_coords()[1] == y:
            return node
    if thickness is not None:
        nodes.append(Node(x, y, parent, thickness, float('inf'), float('inf')))

        return Node(x, y, parent, data.get_thickness([x, y]), float('inf'), float('inf'))
    else:
        return None


def nearest_coord_to_lat_lon(requested_lat, requested_lon):
    coords = data.get_coords()
    vectorized_distance = np.vectorize(distance_lat_lon)

    distances = vectorized_distance(coords['lat'], coords['lon'], requested_lat, requested_lon)

    min_distance = np.min(distances)

    return np.argwhere(distances == min_distance)
