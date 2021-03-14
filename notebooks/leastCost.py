from tkinter import *
import math
import time


class GridBox:
    def __init__(self, canvas, row, col, width, iceThickness, widthMin, heightMin):
      self.canvas = canvas
      iceThickness = abs(iceThickness)
      self.iceThickness = iceThickness
      if iceThickness > 9998:
        self.isValid = False
        self.color = "black"
      else:
        self.isValid = True
        self.color = parseRGB((0, 0, 50 + iceThickness*(150/5)))
      
      self.id = canvas.create_rectangle(col * width - widthMin * width, row * width - heightMin * width, col * width + width - widthMin * width, row * width + width - heightMin * width, fill = self.color)
      
      self.canvas.itemconfig(self.id, fill = self.color)
    def update(self, isPath):
      if (isPath):
        self.color = "yellow"
      else:
        if self.isValid:
          self.color = parseRGB((0, 0, 50 + iceThickness*(150/5)))
        else:
          self.color = "black"
      self.canvas.itemconfig(self.id, fill = self.color)
def parseRGB(colorArray):
    r, g, b = colorArray
    b = math.floor(b)
    return f'#{r:02x}{g:02x}{b:02x}'

import xarray as xr
dataset_path = 'RDEFT4_20200515.nc'
xr_ds = xr.open_dataset(dataset_path)
data = xr_ds.sea_ice_thickness

heightMin = 140
heightMax = 280
widthMin = 50
widthMax = 250

scale = 4

canvas_height = (heightMax - heightMin) * scale
canvas_width = (widthMax - widthMin) * scale
master = Tk()
canvas = Canvas(master, 
        width=canvas_width,
        height=canvas_height)

canvas.pack()
master.title("Arctic Pathing")
master.resizable(0, 0)
master.update_idletasks()
master.update()

Grid = []

for x in range(widthMin, widthMax):
  row = []
  for y in range(heightMin, heightMax):
    row.append(GridBox(canvas, y, x, 4, data[y][x].values, widthMin, heightMin))
    master.update_idletasks()
    master.update()
  Grid.append(row)

def findPath(location, iterationCount, destination, path):
  path.append(location)
  surroundingSpaces = getSurroundingSpaces(location)
  if iterationCount == 0:
    minSpace = getMin(surroundingSpaces)
    path.append(minSpace)
    return path
  else:
    surroundingSpaces = getSurroundingSpaces(location)
    potentialPaths = []
    for i in range(len(surroundingSpaces)):
      potentialPaths.append(findPath(surroundingSpaces[i], iterationCount - 1, destination, potentialPaths[i]))
    
    bestPath = potentialPaths[0]
    bestWeight = evalPath(potentialPaths[0], destination)
    for path in potentialPaths:
      if evalPath(path, destination) < bestWeight:
        bestPath = path
        bestWeight = evalPath(path, destination)
    return bestPath
  

def getThickness(location):
  x = location[0]
  y = location[1]
  return data[y][x].values

def getMin(spaces):
  min = spaces[0]
  minVal = getThickness(spaces[0])
  for space in spaces:
    if getThickness(space) < minVal:
      min = space
      minVal = getThickness(space)
  return min

def getSurroundingSpaces(location):
  x = location[0]
  y = location[1]
  spaces = []
  spaces.append([x-1, y-1])
  spaces.append([x, y-1])
  spaces.append([x+1, y-1])
  spaces.append([x-1, y])
  spaces.append([x+1, y])
  spaces.append([x-1, y+1])
  spaces.append([x, y+1])
  spaces.append([x+1, y+1])
  return spaces


def distance(location1, location2):
  print(location1)
  a = location2[0] - location1[0]
  b = location2[1] - location1[1]
  return math.sqrt(a**2 + b**2)

def evalPath(path, destination):
  if len(path) > 0:
    pathCost = 0
    for i in range(len(path)-1):
      aveWeight = (getThickness(path[i]) * getThickness(path[i + 1]))/2
      pathCost += aveWeight * distance(path[i], path[i+1])
    return pathCost*distance(path[len(path)-1], destination)
  else:
    return 999999999999

start = [150, 60]
end = [250, 230]

path = findPath(start, 3, end, [])
for location in path:
  row = location[0]
  col = location[1]
  Grid[row][col].update(True)

while True:
  master.update_idletasks()
  master.update()
  time.sleep(1)

  
