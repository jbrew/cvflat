from __future__ import division
import wx
import numpy
from tile import Tile
from image import Image

class Palette(wx.Panel):

	def __init__(self, parent, tiles_across, tiles_tall, tile_size):
		wx.Panel.__init__(self, parent)
		self.height = tiles_tall*tile_size
		self.width = tiles_across*tile_size
		self.palSizer = wx.BoxSizer(wx.VERTICAL)

		self.tiles_tall = tiles_across
		self.tiles_across = tiles_across

		self.tile_size = int(self.width / self.tiles_across)
		self.resolution = 5
		self.pixel_size = int(self.tile_size/self.resolution)

		self.active_index = (0,0)

		self.tile_matrix = [[self.NewTile() for x in range(self.tiles_across)] for y in range(self.tiles_tall)]

		blue_tile = Tile(self, pixel_size=self.pixel_size, pixels_tall = self.resolution, pixels_across = self.resolution, bgcolor = (0,100,250))
		green_tile = Tile(self, pixel_size=self.pixel_size, pixels_tall = self.resolution, pixels_across = self.resolution, bgcolor = (0,255,100))
		orange_tile = Tile(self, pixel_size=self.pixel_size, pixels_tall = self.resolution, pixels_across = self.resolution, bgcolor = (255,100,0))
		black_tile = Tile(self, pixel_size=self.pixel_size, pixels_tall = self.resolution, pixels_across = self.resolution, bgcolor = (0,0,0))
		black_tile.full = False

		self.tile_matrix[0][0] = blue_tile
		self.tile_matrix[0][1] = green_tile
		self.tile_matrix[1][0] = orange_tile
		self.tile_matrix[1][1] = black_tile

		self.img = Image(self.height, self.width)

		for r in range(self.tiles_tall):
			for c in range(self.tiles_across):
				self.DrawTile(r, c, self.img)

		self.refresh()

	def get_active(self):
		return self.tile_matrix[self.active_index[0]][self.active_index[1]]

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

	def NewTile(self):
		pixel_size = int(self.tile_size/self.resolution)
		t = Tile(self, pixel_size=pixel_size, pixels_tall = self.resolution, pixels_across = self.resolution)
		return t

	# draws a tile into the array at the specified row and column
	def DrawTile(self, r, c, img):
		y = r * self.tile_size
		x = c * self.tile_size
		height, width = self.tile_size, self.tile_size
		t = self.tile_matrix[r][c]
		a = t.get_palette_array()
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

	def refresh(self):
		for r in range(len(self.tile_matrix)):
			for c in range(len(self.tile_matrix[r])):
				self.DrawTile(r, c, self.img)
		self.palSizer.Clear()
		#self.DrawGrid((50,50,50))

		self.palSizer.Add(self.ToStaticBitmap())

	def onClick(self, e):

		y, x = e.GetPositionTuple()[0], e.GetPositionTuple()[1]
		r, c = self.get_tile_coordinate(x, y)
		self.active_index = (r,c)
		for row in self.tile_matrix:
			for t in row:
				t.active = False
		self.tile_matrix[r][c].active = True

		self.refresh()