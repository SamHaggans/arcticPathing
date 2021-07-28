from netCDF4 import Dataset
import numpy as np


def load_dataset(dataset_path):  # Must be run before any other data methods
    global data, nc_coords

    nc_ds = Dataset(dataset_path)
    nc_var = nc_ds['sea_ice_thickness']

    nc_coords = {'lat': nc_ds['lat'][:], 'lon': nc_ds['lon'][:]}
    nc_data = nc_var[:]

    land_mask = np.fromfile('ice_data/gsfc_25n.msk', dtype=np.byte).reshape((448, 304))
    nc_data[land_mask == 1] = None
    nc_data[nc_data == -9999] = 0
    data = nc_data


def get_coords():
    return nc_coords


def get_data():
    global data
    return data


def get_thickness(location):
    x = location[0]
    y = location[1]
    return data[x][y]


def get_width():
    return len(data[0])


def get_height():
    return len(data)
