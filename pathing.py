import utils
import data
from Node import Node


def find_path(start, end):
    start_thick = data.get_thickness(start)
    init_distance = utils.distance(start, end)

    start = Node(start[0], start[1], None, start_thick, 0, init_distance)

    nodes = [start]
    check_nodes = [start]

    while len(check_nodes) > 0:
        current = utils.get_best_node(check_nodes)
        if (utils.distance(current.get_coords(), end) == 0):
            return {
                'path': generate_path_coords(current, start),
                'difficulty': current.get_g(),
                'distance': init_distance
            }

        check_nodes.remove(current)

        neighbors = utils.get_neighbors(current, nodes)
        for node in neighbors:
            distance = utils.distance_between_nodes(current, node)
            new_g = current.get_g() + distance * utils.weight(current, node)
            if new_g < node.get_g():
                node.set_g(new_g)
                node.set_f(new_g + utils.distance(node.get_coords(), end))
                node.set_parent(current)
                check_nodes.append(node)
    print("No path found")


def generate_path_coords(node, start):
    path_distance = 0
    path = []
    path_coords = []
    current_node = node
    start = start.get_coords()

    while True:
        path.append(current_node.get_coords())
        path_coords.append(current_node.get_lat_lon())
        path_distance += utils.distance_between_nodes(current_node, current_node.get_parent())
        current_node = current_node.get_parent()
        if current_node is None or current_node.get_coords() == start:
            break

    # Return the path, the path lat/lon coordinates, and the distance
    return {
        'path': path[::-1],
        'path_coords': path_coords[::-1],
        'distance': path_distance,
    }
