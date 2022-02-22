import math

import numpy as np

from arcticpathing import data, constants
from arcticpathing.node import Node


def distance(location1: list, location2: list):
    a = location2[0] - location1[0]
    b = location2[1] - location1[1]
    return math.sqrt(a ** 2 + b ** 2)


def distance_lat_lon(lat: float, lon: float, requested_lat: float, requested_lon: float):
    return distance([lat, lon], [requested_lat, requested_lon])


def distance_between_nodes(node1: Node, node2: Node):
    return distance(node1.get_coords(), node2.get_coords())


def nearest_coord_to_lat_lon(requested_lat: float, requested_lon: float):
    coords = data.get_coords()
    vectorized_distance = np.vectorize(distance_lat_lon)

    distances = vectorized_distance(coords['lat'], coords['lon'], requested_lat, requested_lon)

    min_distance = np.min(distances)
    # convert numpy int64 to int
    return [[int(coord[0]), int(coord[1])] for coord in np.argwhere(distances == min_distance)]


def float_is_equal(float1, float2, range=1 * 10 ** (-1 * constants.DATA_PRECISION)):
    return abs(float1-float2) < range
