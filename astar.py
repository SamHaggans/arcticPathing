import math

from itertools import product
from matplotlib import pyplot as plt
from netCDF4 import Dataset
import numpy as np


def find_path(start, end):
    start_thick = get_thickness(start)
    init_distance = distance(start, end)

    start = Node(start[0], start[1], None, start_thick, 0, init_distance)

    nodes = [start]
    check_nodes = [start]

    while len(check_nodes) > 0:
        current = get_best_node(check_nodes)
        if (distance(current.get_coords(), end) == 0):
            return [get_path(current, start), current.get_g(), init_distance]

        check_nodes.remove(current)

        neighbors = get_neighbors(current, nodes)
        for node in neighbors:
            new_g = current.get_g() + distance_between_nodes(current, node) * weight(current, node)
            if new_g < node.get_g():
                node.set_g(new_g)
                node.set_f(new_g + distance(node.get_coords(), end))
                node.set_parent(current)
                check_nodes.append(node)
    print("No path found")


def distance(location1, location2):
    a = location2[0] - location1[0]
    b = location2[1] - location1[1]
    return math.sqrt(a ** 2 + b ** 2)

def distance_between_nodes(node1, node2):
    return distance(node1.get_coords(), node2.get_coords())

def weight(node1, node2):
    c1 = node1.get_coords()
    c2 = node2.get_coords()
    t1 = get_thickness(c1)
    t2 = get_thickness(c2)
    return 2 ** (t1 + t2)


def get_path(node, start):
    path_distance = 0
    path = []
    current_node = node
    start = start.get_coords()

    while True:
        path.append(current_node.get_coords())
        path_distance += distance_between_nodes(current_node, current_node.get_parent())
        current_node = current_node.get_parent()
        if current_node is None or current_node.get_coords() == start:
            break

    return [path[::-1], path_distance]  # Return the reversed path


class Node:
    def __init__(self, x, y, parent, val, g, f):
        self.x = x
        self.y = y
        self.parent = parent
        self.val = val
        self.g = g
        self.f = f

    def get_coords(self):
        return [self.x, self.y]

    def get_parent(self):
        return self.parent

    def get_val(self):
        return self.val

    def get_g(self):
        return self.g

    def get_f(self):
        return self.f

    def set_g(self, g):
        self.g = g

    def set_f(self, f):
        self.f = f

    def set_parent(self, parent):
        self.parent = parent


def get_thickness(location):
    x = location[0]
    y = location[1]
    return data[x][y]


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
        x_in_data_bounds = s[0] >= 0 and s[0] < len(data[0])  # Not less than 0 and not out of bounds
        y_in_data_bounds = s[1] >= 0 and s[1] < len(data)
        if x_in_data_bounds and y_in_data_bounds:
            if get_node(s[0], s[1], nodes, node) is not None:
                neighbors.append(get_node(s[0], s[1], nodes, node))
    return neighbors


def get_node(x, y, nodes, parent):
    for node in nodes:
        if node.get_coords()[0] == x and node.get_coords()[1] == y:
            return node
    if get_thickness([x, y]) is not None:
        nodes.append(Node(x, y, parent, get_thickness([x, y]), float('inf'), float('inf')))

        return Node(x, y, parent, get_thickness([x, y]), float('inf'), float('inf'))
    else:
        return None


def showPath(path, start_dim, max_dimension):
    for col, row in product(range(start_dim, max_dimension), range(start_dim, max_dimension)):
        if [row, col] in path:
            print("+", end="")
        else:
            if data[row][col] < 0:
                print("X", end="")
            else:
                print("=", end="")
        print("")


def show_path_plot(path, start_dim, max_dimension):
    for col, row in product(range(start_dim, max_dimension), range(start_dim, max_dimension)):
        if [row, col] in path:
            nc_data[row][col] = 20
    nc_data[land_mask == 1] = -10
    nc_data[nc_data == -9999] = -20
    plt.xlim(start_dim, max_dimension)
    plt.ylim(0, 500)
    nc_data_flipped = np.flip(nc_data.copy(), axis=0)
    plt.imshow(nc_data_flipped)
    plt.show()


if __name__ == '__main__':
    while True:
        dataset_path = 'ice_data/RDEFT4_20200229.nc'

        nc_ds = Dataset(dataset_path)
        print(nc_ds)
        print(nc_ds['lat'][250][150])
        print(nc_ds['lon'][250][150])
        nc_var = nc_ds['sea_ice_thickness']
        nc_data = nc_var[:]

        land_mask = np.fromfile('ice_data/gsfc_25n.msk', dtype=np.byte).reshape((448, 304))
        nc_data[land_mask == 1] = None
        nc_data[nc_data == -9999] = 0

        data = nc_data

        show_path_plot([], 0, 500)

        x1 = int(input("Enter x1: "))
        y1 = int(input("Enter y1: "))
        x2 = int(input("Enter x2: "))
        y2 = int(input("Enter y2: "))

        path_info = find_path([y1, x1], [y2, x2])
        path = path_info[0][0]
        path_length = path_info[0][1]
        path_cost = path_info[1]
        net_distance = path_info[2]

        print("Path length: " + str(path_length))
        print("Path cost: " + str(path_cost))
        print("Straight line distance traveled: " + str(net_distance))

        show_path_plot(path, 0, 500)
