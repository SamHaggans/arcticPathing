from arcticpathing import utils, data, pathing


def get_input_coords(lat1, lon1, lat2, lon2):
    coords = data.get_coords()

    start = utils.nearest_coord_to_lat_lon(lat1, lon1)[0]

    end = utils.nearest_coord_to_lat_lon(lat2, lon2)[0]

    start_coords = [coords['lat'][start[0]][start[1]], coords['lon'][start[0]][start[1]]]
    end_coords = [coords['lat'][end[0]][end[1]], coords['lon'][end[0]][end[1]]]
    return start, end, start_coords, end_coords


def get_path(lat1, lon1, lat2, lon2):
    data.load_dataset('ice_data/RDEFT4_20200229.nc')

    start, end, start_coords, end_coords = get_input_coords(lat1, lon1, lat2, lon2)
    path_info = pathing.find_path(start, end)
    return path_info
