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
