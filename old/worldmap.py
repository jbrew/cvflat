from __future__ import division
import numpy
import wx
from tile import Tile
from image import Image


class WorldMap(wx.Panel):

	# takes width and height in squares
	def __init__(self, parent, palette, tiles_across, tiles_tall, tile_size):
		wx.Panel.__init__(self, parent)
		self.height = tiles_tall*tile_size
		self.width = tiles_across*tile_size
		self.tiles_across = tiles_across
		self.tiles_tall = tiles_tall
		self.tile_size = tile_size
		self.resolution = 5

		self.wmSizer = wx.BoxSizer(wx.VERTICAL)

		self.palette = palette

		self.tile_matrix = [[self.NewTile() for x in range(self.tiles_across)] for y in range(self.tiles_tall)]

		self.img = Image(self.height+1, self.width+1)
		for r in range(self.tiles_tall):
			for c in range(self.tiles_across):
				self.DrawTile(r, c, self.img)		

		img = wx.Image(filepath, wx.BITMAP_TYPE_ANY)

		self.refresh()

	def NewTile(self):
		pixel_size = int(self.tile_size/self.resolution)
		t = Tile(self, pixel_size=pixel_size, pixels_tall = self.resolution, pixels_across = self.resolution)
		t.randomize_type()
		return t

	# draws a tile into the array at the specified row and column
	def DrawTile(self, r, c,img):
		y = r * self.tile_size
		x = c * self.tile_size
		height, width = self.tile_size, self.tile_size
		t = self.tile_matrix[r][c]
		a = t.get_array()
		for r in range(height):
			for c in range(width):
				img.canvas[y+r,x+c] = a[r,c]


	def DrawGrid(self, grid_color):

		# horizontal lines
		for y_tiles in range(self.tiles_tall+1):
			for x_pixels in range(self.width):
				self.img.canvas[y_tiles*self.tile_size, x_pixels] = grid_color

		# vertical lines
		for x_tiles in range(self.tiles_across+1):
			for y_pixels in range(self.height):
				self.img.canvas[y_pixels, x_tiles*self.tile_size] = grid_color

	# given a tile matrix coordinate, returns absolute coordinate
	def get_abs_coordinate(self, row_index, col_index):
		return row_index * self.tile_size, col_index * self.tile_size

	# given an absolute coordinate, returns tile matrix coordinate
	def get_tile_coordinate(self, y_coord, x_coord):
		r = y_coord // self.tile_size
		c = x_coord // self.tile_size
		return r, c

	def get_tile(self, coordinate):
		return self.tile_matrix[coordinate[0]][coordinate[1]]

# conversion to bitmap
###############################
	def ToStaticBitmap(self):
		png = self.ArrayToBitmap(self.img.canvas)
		self.bmp = wx.StaticBitmap(self, -1, png, (10, 5), (png.GetWidth(), png.GetHeight()))
		self.bmp.Bind(wx.EVT_LEFT_UP, self.onClick)
		return self.bmp

	def ArrayToBitmap(self, array):
		height, width = len(array), len(array[0])
		image = wx.EmptyImage(width,height)
		image.SetData( array.tostring())
		wxBitmap = image.ConvertToBitmap()       # OR:  wx.BitmapFromImage(image)
		return wxBitmap


####################################################

	def refresh(self):
		self.wmSizer.Clear()
		self.DrawGrid((50,50,50))
		self.wmSizer.Add(self.ToStaticBitmap())

	def onClick(self, e):
		y, x = e.GetPositionTuple()[0], e.GetPositionTuple()[1]
		r, c = self.get_tile_coordinate(x, y)
		t = self.palette.get_active()
		self.tile_matrix[r][c] = t
		self.DrawTile(r, c, self.img)
		self.refresh()


# tools for drawing directly onto map, rather than via tiles
###########################

	# true if coordinate is in array
	def IsInArray(self, yval, xval):
		return xval in range(self.width) and yval in range(self.height)

"""
	# creates a variegated color grid
	def RandomSquares(self):
		for r in range(self.tiles_tall):
			for c in range(self.tiles_across):
				if numpy.random.uniform() > 0:
					rmin = numpy.random.uniform(110,170)
					rmax = rmin + 60*numpy.random.normal()
					gmin = numpy.random.uniform(110,170)
					gmax = gmin + 60*numpy.random.normal()
					bmin = numpy.random.uniform(110,160)
					bmax = bmin + 60*numpy.random.normal()
					t = Tile(self.pixel_size, self.height, self.width, bgcolor = (255,255,255))
					self.DrawTile(r, c, t.get_array())
	# modifies an array
	def DrawCircle(self, r, array, position, linewidth, color):
		height, width = 2*r, 2*r
		center = position
		for x in range(int(center[0]-r-linewidth), int(center[0]+r+linewidth)):
			for y in range(int(center[1]-r-linewidth), int(center[1]+r+linewidth)):
				distance = numpy.sqrt((x-center[0])*(x-center[0]) + (y-center[1])*(y-center[1]))
				if numpy.absolute(distance - (r-5)) <= linewidth/2:
					if self.IsInArray(y,x):
						array[x,y] = color
		return array

	# draws the specified number of pink circles at random places on the image
	def DrawPinkCircles(self, num_pink_circles):
		num_circles = 2

		positions = [(numpy.random.uniform()*self.height, numpy.random.uniform()*self.width) for x in range(num_circles)]
		
		for p in positions:
			self.DrawCircle(40, self.img.canvas, position = p, linewidth = 2.5, color = (200,100,100))
"""

