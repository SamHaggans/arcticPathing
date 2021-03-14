from tkinter import *
import math


class GridBox:
    def __init__(self, canvas, row, col, width, iceThickness):
      self.canvas = canvas
      self.id = canvas.create_rectangle(col * width, row * width, col * width + width, row * width + width, fill = self.color)
      if (iceThickness < 9998):
        self.isValid = False
      else:
        self.isValid = True
      self.iceThickness = iceThickness
    def updateSelf(self, isPath):
      if (self.isPath):
        self.color = "yellow"
      else:
        self.color = parseRGB(0, 0, self.iceThickness*(250/20))
      self.canvas.itemconfig(self.id, fill = self.color)
def parseRGB(colorArray):
    r, g, b = colorArray
    return f'#{r:02x}{g:02x}{b:02x}'

import xarray as xr
from netCDF4 import Dataset
dataset_path = 'RDEFT4_20200515.nc'
nc_ds = Dataset(dataset_path)
nc_var = nc_ds['sea_ice_thickness']
nc_data = nc_var[:]
xr_ds = xr.open_dataset(dataset_path)
data = xr_ds.sea_ice_thickness



dataHeight = 448
dataWidth = 304

canvas_height = dataHeight * 2
canvas_width = dataWidth * 2
master = Tk()
canvas = Canvas(master, 
        width=canvas_width,
        height=canvas_height)

canvas.pack()
master.title("Coronavirus Spread Simulation")
master.resizable(0, 0)
master.update_idletasks()
master.update()


for x in range(dataWidth):
  for y in range(dataHeight):
    var = GridBox(canvas, y, x, 2, data[y*2][x*2].values)
    master.update_idletasks()
    master.update()

  
