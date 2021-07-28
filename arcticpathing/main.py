from arcticpathing import utils, data, pathing, display


def get_inputs():
    lat1 = int(input("Enter starting lat: "))
    lon1 = int(input("Enter starting lon: "))
    lat2 = int(input("Enter ending lat: "))
    lon2 = int(input("Enter ending lon: "))

    return get_input_coords(lat1, lon1, lat2, lon2)


def get_input_coords(lat1, lon1, lat2, lon2):
    coords = data.get_coords()

    start = utils.nearest_coord_to_lat_lon(lat1, lon1)[0]

    end = utils.nearest_coord_to_lat_lon(lat2, lon2)[0]

    start_coords = [coords['lat'][start[0]][start[1]], coords['lon'][start[0]][start[1]]]
    end_coords = [coords['lat'][end[0]][end[1]], coords['lon'][end[0]][end[1]]]
    return start, end, start_coords, end_coords


def show_path_info(path_info):
    path_coords = path_info['path']['path_coords']
    path_length = path_info['path']['distance']
    path_cost = path_info['difficulty']
    net_distance = path_info['distance']

    print("Path length: " + str(path_length))
    print("Path cost: " + str(path_cost))
    print("Straight line distance traveled: " + str(net_distance))
    print(path_coords)


def get_path(lat1, lon1, lat2, lon2):
    data.load_dataset('ice_data/RDEFT4_20200229.nc')

    start, end, start_coords, end_coords = get_input_coords(lat1, lon1, lat2, lon2)
    path_info = pathing.find_path(start, end)
    return path_info


def pathing_loop():
    start, end, start_coords, end_coords = get_inputs()

    print(f'Finding path between {start_coords} and {end_coords}')

    path_info = pathing.find_path(start, end)

    show_path_info(path_info)

    path = path_info['path']

    display.show_path_plot(path, 0, 500)


if __name__ == '__main__':
    data.load_dataset('ice_data/RDEFT4_20200229.nc')

    while True:
        pathing_loop()
