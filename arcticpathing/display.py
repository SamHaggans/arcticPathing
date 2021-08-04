from itertools import product
from matplotlib import pyplot as plt
import numpy as np

from arcticpathing import data


def get_path_plot(path):
    ice_data = data.get_data()
    land_mask = np.fromfile('ice_data/gsfc_25n.msk', dtype=np.byte).reshape((448, 304))
    for col, row in product(range(0, 304), range(0, 448)):
        if [row, col] in path:
            ice_data[row][col] = 6
    ice_data[land_mask == 1] = -3
    ice_data[ice_data == -9999] = -6
    ice_data = np.flip(ice_data.copy(), axis=0)
    fig, ax = plt.subplots()
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.axis('off')
    plt.xlim(0, 304)
    plt.ylim(0, 448)
    plt.imshow(ice_data)
    return plt
