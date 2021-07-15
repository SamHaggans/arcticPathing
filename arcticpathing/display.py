from itertools import product
from matplotlib import pyplot as plt
import numpy as np

from arcticpathing import data


def show_path_plot(path, start_dim, max_dimension):
    ice_data = data.get_data()
    land_mask = np.fromfile('ice_data/gsfc_25n.msk', dtype=np.byte).reshape((448, 304))

    for col, row in product(range(start_dim, max_dimension), range(start_dim, max_dimension)):
        if [row, col] in path:
            ice_data[row][col] = 20
    ice_data[land_mask == 1] = -10
    ice_data[ice_data == -9999] = -20
    plt.xlim(start_dim, max_dimension)
    plt.ylim(0, 500)
    nc_data_flipped = np.flip(ice_data.copy(), axis=0)
    plt.imshow(nc_data_flipped)
    plt.show()
