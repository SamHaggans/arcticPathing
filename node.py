import data


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

    def get_lat_lon(self):
        lat = data.get_coords()['lat'][self.x][self.y]
        lon = data.get_coords()['lon'][self.x][self.y]
        return [lat, lon]

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
