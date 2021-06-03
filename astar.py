import math

from matplotlib import pyplot as plt
from netCDF4 import Dataset
import numpy as np


def findPath(start, end):
    startCoords = start
    start = Node(start[0], start[1], None, getThickness(start), 0, distance(start, end))
    
    nodes = [start]
    checkNodes = [start]

    while len(checkNodes) > 0:
        
        current = getBestNode(checkNodes)
        if (distance(current.getCoords(), end) == 0):  
          return [getPath(current, startCoords), current.getG(), distance(startCoords, end)]

        checkNodes.remove(current)

        neighbors = getNeighbors(current, nodes)
        for node in neighbors:
            newG = current.getG() + distance(current.getCoords(), node.getCoords()) * weight(current, node)
            if newG < node.getG():
              node.setG(newG)
              node.setF(newG + distance(node.getCoords(), end))
              node.setParent(current)
              checkNodes.append(node)
    print("No path found")
def distance(location1, location2):
  a = location2[0] - location1[0]
  b = location2[1] - location1[1]
  return math.sqrt(a**2 + b**2)

def weight(node1, node2):
  c1 = node1.getCoords()
  c2 = node2.getCoords()
  t1 = getThickness(c1)
  t2 = getThickness(c2)
  return 2**(t1+t2)

def getPath(node, start):
  pathDistance = 0
  path = []
  currentNode = node
  
  while True:
    path.append(currentNode.getCoords())
    pathDistance += distance(currentNode.getCoords(), currentNode.getParent().getCoords())
    currentNode = currentNode.getParent()
    if currentNode is None or currentNode.getCoords() == start:
      break
  
  return [path[::-1], pathDistance]#Return the reversed path


class Node:
    def __init__(self, x, y, parent, val, g, f):
        self.x = x
        self.y = y
        self.parent = parent
        self.val = val
        self.g = g
        self.f = f

    def getCoords(self):
        return [self.x, self.y]

    def getParent(self):
        return self.parent

    def getVal(self):
        return self.val
    
    def getG(self):
        return self.g
    
    def getF(self):
        return self.f
    
    def setG(self, g):
        self.g = g
        
    def setF(self, f):
        self.f = f

    def setParent(self, parent):
        self.parent = parent
    
def getThickness(location):
  x = location[0]
  y = location[1]
  return data[x][y]

def getBestNode(nodes):
    minVal = nodes[0].getF()
    minNode = nodes[0]
    for node in nodes:
        if node.getF() < minVal:
            minNode = node
            minVal = node.getF()
    return minNode

def getNeighbors(node, nodes):
  x = node.getCoords()[0]
  y = node.getCoords()[1]
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
      if s[0] >= 0 and s[1] >= 0 and s[0] < len(data[0]) and s[1] < len(data):
        if getNode(s[0], s[1], nodes, node) is not None:
          neighbors.append(getNode(s[0], s[1], nodes, node))
  return neighbors


def getNode(x, y, nodes, parent):

    for node in nodes:
        if node.getCoords()[0] == x and node.getCoords()[1] == y:
            return node

    if getThickness([x, y]) is not None:
      nodes.append(Node(x, y, parent, getThickness([x, y]), float('inf'), float('inf')))

      return Node(x, y, parent, getThickness([x, y]), float('inf'), float('inf'))
    else:
      return None

def showPath(path, startDim, maxDimension):
  for col in range(startDim, maxDimension):
    for row in range(startDim, maxDimension):
      if [row, col] in path:
        print("+", end="")
      else:
        if data[row][col] < 0:
          print("X", end="")
        else:
          print("=", end="")
    print("")

def showPathPlot(path, startDim, maxDimension):
  for col in range(startDim, maxDimension):
    for row in range(startDim, maxDimension):
      if [row, col] in path:
        nc_data[row][col] = 20
  nc_data[land_mask == 1] = -10
  nc_data[nc_data == -9999] = -20
  plt.xlim(startDim, maxDimension)
  plt.ylim(0, 500)
  nc_data_flipped = np.flip(nc_data.copy(), axis=0)
  # rasterio https://rasterio.readthedocs.io/en/latest/api/rasterio.transform.html#rasterio.transform.rowcol
  # xarray potentially too
  plt.imshow(nc_data_flipped)
  plt.show()

if __name__ == '__main__':
  import xarray as xr
  while True:
    
    
    dataset_path = 'iceData/RDEFT4_20200229.nc'

    nc_ds = Dataset(dataset_path)
    print(nc_ds)
    print(nc_ds['lat'][250][150])
    print(nc_ds['lon'][250][150])
    nc_var = nc_ds['sea_ice_thickness']
    nc_data = nc_var[:]
    
    land_mask = np.fromfile('iceData/gsfc_25n.msk', dtype=np.byte).reshape((448, 304))
    nc_data[land_mask == 1] = None
    nc_data[nc_data == -9999] = 0
    
    data = nc_data

    showPathPlot([], 0, 500)

    x1 = int(input("Enter x1: "))
    y1 = int(input("Enter y1: "))
    x2 = int(input("Enter x2: "))
    y2 = int(input("Enter y2: "))

    pathInfo = findPath([y1, x1], [y2, x2])
    path = pathInfo[0][0]
    pathLength = pathInfo[0][1]
    pathCost = pathInfo[1]
    netDistance = pathInfo[2]

    print("Path length: " + str(pathLength))
    print("Path cost: " + str(pathCost))
    print("Straight line distance traveled: " + str(netDistance))

    showPathPlot(path, 0, 500)