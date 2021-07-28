from itertools import product
from random import getrandbits
from matplotlib import pyplot as plt
import numpy as np

from arcticpathing import data


def save_path_plot(path, start_dim, max_dimension):
    ice_data = data.get_data()
    land_mask = np.fromfile('ice_data/gsfc_25n.msk', dtype=np.byte).reshape((448, 304))

    for col, row in product(range(start_dim, max_dimension), range(start_dim, max_dimension)):
        if [row, col] in path:
            ice_data[row][col] = 20
    ice_data[land_mask == 1] = -10
    ice_data[ice_data == -9999] = -20
    plt.xlim(start_dim, max_dimension)
    plt.ylim(0, 500)
    filename = "%x.png" % getrandbits(64)
    plt.imsave(f'plots/{filename}', ice_data)
    return filename
