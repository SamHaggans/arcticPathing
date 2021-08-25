from itertools import product
from matplotlib import pyplot as plt  # type: ignore
import numpy as np

from arcticpathing import data, constants


def get_path_plot(path: list):
    ice_data = data.get_data()
    land_mask = np.fromfile(constants.LAND_MASK_PATH, dtype=np.byte).reshape((448, 304))
    for col, row in product(range(0, 304), range(0, 448)):
        if [row, col] in path:
            ice_data[row][col] = 6
    ice_data[land_mask == 1] = -3
    ice_data[ice_data == -9999] = -6
    ice_data = np.flip(ice_data.copy(), axis=0)
    fig = plt.figure(figsize=(6.8, 10), dpi=500)
    # Set axes to fill the entire plot to size correctly
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    # Turn off axes and add to the figure
    ax.set_axis_off()
    fig.add_axes(ax)

    plt.xlim(0, 304)
    plt.ylim(0, 448)
    plt.imshow(ice_data)
    return plt
